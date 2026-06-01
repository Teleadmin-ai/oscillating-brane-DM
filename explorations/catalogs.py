#!/usr/bin/env python3
"""
catalogs.py — generic catalog data layer for the OBT-Game (CHERCHEUR mode helper).

Design goals (per Romain): NOT hardcoded. One generic TAP/ADQL client usable for many
different future cases, different surveys, different selection criteria. Strategy =
"TAP first, auto-cache": run an ADQL query against a registered TAP service, stream the
result, and auto-cache it as Parquet under /DATA (NEVER on /, which is small).

This module is PURE DATA PLUMBING. It contains NO OBT physics and NO game logic — it
just fetches/caches/filters tables. The game logic (gate, monsters, cards) lives in
obt_game.py; the OBT formulas live elsewhere. Keeping them separate is deliberate.

Public API
----------
  list_services()                         -> dict of registered TAP endpoints
  list_tables(service, match=None)        -> [(table, desc)] schema discovery
  list_columns(service, table)            -> [(col, unit, desc)] schema discovery
  tap_query(service, adql, ...)           -> pandas.DataFrame (auto-cached on /DATA)
  sieve(df, **conditions)                 -> filtered DataFrame (generic predicates)
  preview(df, cols, sort, top, where)     -> (head_df, stats_df) to SEE/judge systems
  propagate(df, select)                   -> (matched, n, total): does my patch hold elsewhere?
  propagate_verify(df, applies, patch_ok, where) -> FACTS dict (auto-propagation + OBT check)
  save_lot(df, name) / load_lot(name)     -> persist/restore a candidate lot (Parquet)
  cache_info()                            -> what's cached on /DATA + sizes
  run_agent(prompt, ...)                  -> launch a Claude agent on a sub-lot (stub:
                                             writes a mission file; wired to Agent later)

Everything is parameterized: the caller passes the service key, the ADQL text (or a
column/where spec), and the conditions. No survey-specific columns are baked in.
"""

import hashlib
import json
import os
import shutil
import time

# ----------------------------------------------------------------------------
# Cache lives on /DATA (45 GB) — explicitly NOT on / (small). Overridable by env.
# ----------------------------------------------------------------------------
CACHE_ROOT = os.environ.get("OBT_GAME_CACHE", "/DATA/obt_game_cache")
CATALOG_DIR = os.path.join(CACHE_ROOT, "catalogs")   # raw query results (parquet)
LOT_DIR = os.path.join(CACHE_ROOT, "lots")           # named candidate lots
MISSION_DIR = os.path.join(CACHE_ROOT, "missions")   # agent mission files

# Registered TAP services. Add more freely — this is the ONLY place endpoints live.
SERVICES = {
    "gaia": "https://gea.esac.esa.int/tap-server/tap",
    "vizier": "http://TAPVizieR.cds.unistra.fr/TAPVizieR/tap",
    "simbad": "https://simbad.cds.unistra.fr/simbad/sim-tap",
    "ned": "https://ned.ipac.caltech.edu/tap",
    # SDSS / DESI added when needed; SDSS also has a non-TAP SQL endpoint.
}


def _ensure_dirs():
    for d in (CATALOG_DIR, LOT_DIR, MISSION_DIR):
        os.makedirs(d, exist_ok=True)


def list_services():
    """Return the registered TAP services (key -> URL)."""
    return dict(SERVICES)


def _cache_key(service, adql):
    h = hashlib.sha1(f"{service}\n{adql}".encode()).hexdigest()[:16]
    return os.path.join(CATALOG_DIR, f"{service}_{h}.parquet")


def tap_query(service, adql, force=False, timeout=1800, maxrec=2_000_000, verbose=True):
    """Run an ADQL query against a registered TAP service; auto-cache to /DATA as Parquet.

    Parameters
    ----------
    service : str   key in SERVICES (e.g. 'gaia')
    adql    : str   the ADQL query text (caller-supplied; not hardcoded here)
    force   : bool  re-run even if a cached result exists
    timeout : int   seconds before giving up (applied to the HTTP session)
    maxrec  : int   row cap requested from the service
    Returns a pandas.DataFrame. Cached file path is reused on identical (service, adql).
    """
    import pandas as pd

    _ensure_dirs()
    if service not in SERVICES:
        raise ValueError(f"unknown service '{service}'. Known: {list(SERVICES)}")
    path = _cache_key(service, adql)
    if os.path.exists(path) and not force:
        if verbose:
            print(f"[catalogs] cache HIT {os.path.basename(path)}")
        return pd.read_parquet(path)

    import pyvo

    if verbose:
        print(f"[catalogs] TAP query -> {service} ({SERVICES[service]})")
        print(f"[catalogs] ADQL: {adql[:160]}{'...' if len(adql) > 160 else ''}")
    t0 = time.time()
    tap = pyvo.dal.TAPService(SERVICES[service])
    # actually enforce the timeout on the underlying HTTP session (else it's a lie)
    try:
        tap._session.timeout = timeout
    except Exception:
        pass
    result = tap.search(adql, maxrec=maxrec)
    df = result.to_table().to_pandas()
    # byte-string columns -> str (VOTable quirk) so Parquet/filters behave
    for c in df.columns:
        if df[c].dtype == object:
            df[c] = df[c].apply(lambda v: v.decode() if isinstance(v, bytes) else v)
    df.to_parquet(path, index=False)
    if verbose:
        print(f"[catalogs] {len(df):,} rows in {time.time()-t0:.1f}s -> cached "
              f"{os.path.basename(path)} ({os.path.getsize(path)/1e6:.1f} MB)")
    return df


def sieve(df, **conditions):
    """Generic filter. Each condition is column=(op, value) or column=value (==).
    Ops: 'gt','ge','lt','le','eq','ne','between'(value=(lo,hi)),'isin'(value=list).
    Example: sieve(df, parallax=('gt', 5), phot_g_mean_mag=('between',(8,12)))."""
    out = df
    for col, cond in conditions.items():
        if col not in out.columns:
            raise KeyError(f"sieve: column '{col}' not in dataframe {list(out.columns)[:8]}...")
        if not isinstance(cond, tuple):
            op, val = "eq", cond
        else:
            op, val = cond
        s = out[col]
        if op == "gt":
            out = out[s > val]
        elif op == "ge":
            out = out[s >= val]
        elif op == "lt":
            out = out[s < val]
        elif op == "le":
            out = out[s <= val]
        elif op == "eq":
            out = out[s == val]
        elif op == "ne":
            out = out[s != val]
        elif op == "between":
            lo, hi = val
            out = out[(s >= lo) & (s <= hi)]
        elif op == "isin":
            out = out[s.isin(val)]
        else:
            raise ValueError(f"sieve: unknown op '{op}'")
    return out


def list_tables(service, match=None, maxn=60):
    """Discover the TABLES of a TAP service (schema discovery), optionally filtered by a
    case-insensitive substring `match`. Returns a list of (table_name, description)."""
    if service not in SERVICES:
        raise ValueError(f"unknown service '{service}'. Known: {list(SERVICES)}")
    import pyvo

    tap = pyvo.dal.TAPService(SERVICES[service])
    out = []
    for name, t in tap.tables.items():
        if match and match.lower() not in name.lower():
            continue
        desc = (getattr(t, "description", "") or "").strip().replace("\n", " ")
        out.append((name, desc[:90]))
        if len(out) >= maxn:
            break
    return out


def list_columns(service, table):
    """Discover the COLUMNS of a TAP table. Returns a list of (column, unit, description)."""
    if service not in SERVICES:
        raise ValueError(f"unknown service '{service}'. Known: {list(SERVICES)}")
    import pyvo

    tap = pyvo.dal.TAPService(SERVICES[service])
    tbl = tap.tables[table]
    out = []
    for c in tbl.columns:
        unit = (getattr(c, "unit", "") or "")
        desc = (getattr(c, "description", "") or "").strip().replace("\n", " ")
        out.append((c.name, unit, desc[:80]))
    return out


def preview(df, cols=None, sort=None, top=20, where=None):
    """Return (head_df, stats_df) for a table: a top-N slice (optionally column-subset,
    sorted, filtered by a pandas query `where`) + per-column min/median/max/count.
    This is the 'let me SEE the systems to judge them' helper — pure pandas, generic."""
    out = df
    if where:
        out = out.query(where)
    if cols:
        keep = [c for c in cols if c in out.columns]
        out = out[keep] if keep else out
    if sort and sort in out.columns:
        out = out.sort_values(sort, ascending=False)
    head = out.head(top)
    num = out.select_dtypes("number")
    stats = num.describe().loc[["min", "50%", "max", "count"]] if len(num.columns) else None
    return head, stats


def propagate(df, select, label="patch"):
    """Apply a patch's SELECTION RULE (a pandas query string, e.g. "vobs > 1.1*vnewton")
    to a lot and report how many / which systems satisfy it — i.e. "does my patch hold on
    OTHER systems too?". Returns (matched_df, n_match, n_total). The expression is MINE
    (the player's); the tool just counts where it holds. This drives candidate->monster->card."""
    n_total = len(df)
    try:
        matched = df.query(select)
    except Exception as e:
        raise ValueError(f"propagate: bad select expression '{select}': {e}. "
                         f"(Tip: wrap column names with dots/spaces in `backticks`.)")
    return matched, len(matched), n_total


def propagate_verify(df, applies, patch_ok, where=None):
    """AUTO-PROPAGATION + OBT-VALIDITY CHECK (pure calculation, no judgement).
    The player supplies, as pandas expressions (free-form, not hardcoded):
      - `where`    : optional pre-filter restricting to the relevant population.
      - `applies`  : on which systems the patch is SUPPOSED to be relevant
                     (the model where it could work).
      - `patch_ok` : the FACTUAL condition that OBT+patch holds for a system.
    The tool reports, over the population where the patch applies, the FACTS:
      how many systems satisfy `patch_ok`, which ones, and which ones break — nothing
      it can be wrong about. Classifying (coincidence? monster? card?) stays the player's.
    Returns a dict of facts."""
    pop = df.query(where) if where else df
    try:
        applic = pop.query(applies)
    except Exception as e:
        raise ValueError(f"propagate_verify: bad 'applies' expr '{applies}': {e}")
    try:
        holds = applic.query(patch_ok)
    except Exception as e:
        raise ValueError(f"propagate_verify: bad 'patch_ok' expr '{patch_ok}': {e}")
    n_app = len(applic)
    n_ok = len(holds)
    breaks = applic.drop(holds.index) if n_app else applic
    return {
        "n_population": len(pop),
        "n_applies": n_app,
        "n_holds": n_ok,
        "n_breaks": n_app - n_ok,
        "frac_holds": (n_ok / n_app) if n_app else 0.0,
        "holds_df": holds,
        "breaks_df": breaks,
    }


def save_lot(df, name):
    """Persist a named candidate lot to /DATA (Parquet). Returns the path."""
    _ensure_dirs()
    path = os.path.join(LOT_DIR, f"{name}.parquet")
    df.to_parquet(path, index=False)
    print(f"[catalogs] saved lot '{name}': {len(df):,} rows -> {path}")
    return path


def load_lot(name):
    import pandas as pd

    path = os.path.join(LOT_DIR, f"{name}.parquet")
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    return pd.read_parquet(path)


def cache_info():
    """Report what is cached on /DATA and how much space is used/free."""
    _ensure_dirs()
    info = {"cache_root": CACHE_ROOT, "catalogs": [], "lots": [], "missions": []}
    for key, d in (("catalogs", CATALOG_DIR), ("lots", LOT_DIR), ("missions", MISSION_DIR)):
        for f in sorted(os.listdir(d)):
            fp = os.path.join(d, f)
            info[key].append({"name": f, "MB": round(os.path.getsize(fp) / 1e6, 2)})
    _total, _used, free = shutil.disk_usage(CACHE_ROOT)
    info["disk_free_GB"] = round(free / 1e9, 1)
    return info


def run_agent(prompt, label="mission", lot_name=None, background=True):
    """Launch a Claude agent on a sub-lot. SKELETON: writes a mission file under /DATA
    and (optionally) shells out to `claude` if available. Wiring to the in-harness Agent
    tool is done by the pilot; this gives the script a uniform way to dispatch work.

    The prompt MUST carry the chercheur-mode rules for the agent's mission (the pilot
    supplies them from chercheur-game.md §7 playbook). Returns the mission file path."""
    _ensure_dirs()
    mid = hashlib.sha1(f"{label}{time.time()}".encode()).hexdigest()[:8]
    mission = {
        "id": mid,
        "label": label,
        "lot": lot_name,
        "prompt": prompt,
        "created": os.environ.get("OBT_GAME_DATE", "date-unset"),
        "status": "created",
    }
    path = os.path.join(MISSION_DIR, f"{label}_{mid}.json")
    with open(path, "w") as f:
        json.dump(mission, f, indent=2, ensure_ascii=False)
    print(f"[catalogs] mission file written: {path}")
    claude = shutil.which("claude")
    if background and claude:
        print(f"[catalogs] (claude CLI found at {claude}; dispatch wired by pilot)")
    return path


# ---- self-test (no network): exercise sieve / cache_info / lots on a fake table ----
def _selftest():
    import pandas as pd

    print("=== catalogs.py self-test (offline) ===")
    df = pd.DataFrame({
        "ra": [10.0, 20.0, 30.0, 40.0],
        "dec": [-5.0, 0.0, 5.0, 10.0],
        "parallax": [2.0, 6.0, 12.0, 0.5],
        "sep_au": [1000, 3000, 5000, 9000],
    })
    s = sieve(df, parallax=("gt", 1.0), sep_au=("between", (2000, 6000)))
    assert len(s) == 2, f"sieve expected 2 rows, got {len(s)}"
    p = save_lot(s, "selftest_lot")
    back = load_lot("selftest_lot")
    assert len(back) == 2
    os.remove(p)
    # preview: head + stats
    head, stats = preview(df, cols=["parallax", "sep_au"], sort="parallax", top=2)
    assert len(head) == 2 and stats is not None, "preview failed"
    # propagate (simple): count where a rule holds
    _, n, tot = propagate(df, "parallax > 1.0")
    assert n == 3 and tot == 4, f"propagate expected 3/4, got {n}/{tot}"
    # propagate_verify: facts over an applies-population. parallax>1 -> 3 systems
    # (sep_au=1000,3000,5000); patch_ok sep_au<4000 -> 2 hold (1000,3000), 1 breaks (5000).
    r = propagate_verify(df, applies="parallax > 1.0", patch_ok="sep_au < 4000")
    assert r["n_applies"] == 3 and r["n_holds"] == 2 and r["n_breaks"] == 1, f"verify facts wrong: {r}"
    m = run_agent("TEST prompt (chercheur rules go here)", label="selftest")
    os.remove(m)
    ci = cache_info()
    print(f"  preview/propagate/verify OK; disk free on cache: {ci['disk_free_GB']} GB "
          f"(cache_root={ci['cache_root']})")
    print("  SELFTEST_OK")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        _selftest()
    elif len(sys.argv) > 1 and sys.argv[1] == "cache":
        print(json.dumps(cache_info(), indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "services":
        print(json.dumps(list_services(), indent=2))
    else:
        print(__doc__)
