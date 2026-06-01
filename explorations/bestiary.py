#!/usr/bin/env python3
"""
bestiary.py — monster/card/error lifecycle for the OBT-Game (CHERCHEUR mode).

The "bestiary" manages the TYPED objects of the game through the THREE-LEVEL lifecycle of
Romain's §0 (chercheur-game.md), ON TOP of the same game.json that obt_game.py owns (single
source of truth):
  - CANDIDATE : a patch on ONE external theory making OBT+patch+the-rest work on ONE system.
                Could be a coincidence -> NOT in the bestiary (its own 'candidates' bucket).
  - MONSTER   : a candidate validated on >= MIN_SYSTEMS_FOR_MONSTER systems (anti-coincidence),
                stored WITH its list of working systems; WHY still unknown -> in the bestiary.
  - CARD      : a monster whose mechanistic WHY is understood (ideally via a SIMPLE system) and
                certain -> a correction of an external theory, to be added to OBT.
  - ERROR     : a refuted patch (e.g. a coincidence that failed to generalize).
Gates enforced: candidate->monster needs >= 2 systems; monster->card needs WHY + certainty>=high.
All transitions are logged with history so "the magic" (re-test of abandoned cases as cards
accumulate) is measurable.

NO physics, NO catalog I/O, NO state-machine logic — just the object lifecycle.
Generic: external_theory / patch / systems are free-form per case (not hardcoded).

CLI:
  python3 bestiary.py list [candidates|monsters|cards|errors|all]
  python3 bestiary.py show <id>
  python3 bestiary.py add-candidate <name> --theory T --patch P [--system S]
  python3 bestiary.py add-system <id> --system S          # record another working system
  python3 bestiary.py confirm-monster <id> [--judgement "..."]  # candidate -> monster (>=2 systems = floor; YOUR call)
  python3 bestiary.py promote <id> --why "..." --certainty high   # monster -> card
  python3 bestiary.py kill <id> --reason "..."
  python3 bestiary.py abandon <id> --reason "..."
  python3 bestiary.py magic            # report resolution-rate vs card count
  python3 bestiary.py selftest
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(HERE, "game.json")

CERTAINTY_LEVELS = ("low", "medium", "high", "certain")  # card promotion needs >= high
MIN_SYSTEMS_FOR_MONSTER = 2  # candidate -> monster: must work on >= this many systems (anti-coincidence)

# Three-level lifecycle (Romain §0): candidate -> monster -> card.
#   candidate : patch made on ONE system; could be coincidence; NOT in the bestiary proper.
#   monster   : validated on SEVERAL systems (stored), still not understood (no "why").
#   card      : the mechanistic WHY is understood (ideally via a SIMPLE system) -> add to OBT.
OBJ_SCHEMA = {
    "id": None,
    "name": None,
    "external_theory": None,   # the adjacent theory whose param we patched
    "patch": None,             # the one external parameter change
    "systems_validated": [],   # systems where OBT+patch+the-rest works (the anti-coincidence list)
    "why_status": "none",      # none | partial | found
    "why": None,               # the mechanistic debunk text (None until found)
    "certainty": "low",        # low | medium | high | certain
    "status": "candidate",     # candidate | monster | card | error | abandoned
    "created": None,
    "updated": None,
    "history": [],             # list of {t, event, detail}
}


# ---------------------------------------------------------------------------
# state load/save (shared game.json; tolerant if obt_game hasn't created it yet)
# ---------------------------------------------------------------------------
def _now():
    return os.environ.get("OBT_GAME_DATE", "date-unset")


def _default_state():
    return {
        "mode": "CHERCHEUR",
        "state": "PICK_TERRAIN",
        "game": {"candidates": [], "monsters": [], "cards": [], "errors": [], "terrains": []},
        "naked_obt_predictions": [],
        "log": [],
    }


def load():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            st = json.load(f)
    else:
        st = _default_state()
    # be tolerant: ensure buckets exist
    st.setdefault("game", {})
    for b in ("candidates", "monsters", "cards", "errors", "terrains"):
        st["game"].setdefault(b, [])
    st.setdefault("log", [])
    return st


def save(st):
    with open(STATE_FILE, "w") as f:
        json.dump(st, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _new_id(name, st=None):
    """Deterministic, COLLISION-FREE id. _now() is a fixed date here (clock is unavailable),
    so name+date alone collide for same-name/same-day objects; we salt with a monotonic
    seq = total objects ever created across all buckets, guaranteeing uniqueness."""
    seq = 0
    if st is not None:
        g = st.get("game", {})
        seq = sum(len(g.get(b, [])) for b in ("candidates", "monsters", "cards", "errors"))
        seq += len([e for e in st.get("log", []) if "added_candidate" in e])  # robust to moves
    return hashlib.sha1(f"{name}|{_now()}|{seq}".encode()).hexdigest()[:8]


def _find(st, obj_id):
    """Return (bucket_name, index, obj) for an id across all buckets, or (None,None,None)."""
    for bucket in ("candidates", "monsters", "cards", "errors"):
        for i, o in enumerate(st["game"].get(bucket, [])):
            if o.get("id") == obj_id:
                return bucket, i, o
    return None, None, None


def _move(st, obj, from_bucket, to_bucket, event, detail):
    st["game"][from_bucket] = [o for o in st["game"][from_bucket] if o.get("id") != obj["id"]]
    obj["updated"] = _now()
    obj.setdefault("history", []).append({"t": _now(), "event": event, "detail": detail})
    st["game"][to_bucket].append(obj)
    st["log"].append({"t": _now(), event: obj["id"], "detail": detail})


# ---------------------------------------------------------------------------
# operations
# ---------------------------------------------------------------------------
def add_candidate(st, name, external_theory, patch, first_system=None):
    """LEVEL 1: create a CANDIDATE — a patch on ONE external theory that makes OBT+patch+the-rest
    work on ONE system. Could be a coincidence, so it goes to the 'candidates' bucket, NOT the
    bestiary (monsters). Promote to monster only after it works on several systems."""
    m = json.loads(json.dumps(OBJ_SCHEMA))  # deep copy of the schema skeleton
    m.update({
        "id": _new_id(name, st),
        "name": name,
        "external_theory": external_theory,
        "patch": patch,
        "systems_validated": [first_system] if first_system else [],
        "status": "candidate",
        "created": _now(),
        "updated": _now(),
        "history": [{"t": _now(), "event": "created_candidate",
                     "detail": f"patch on {external_theory}" + (f" @ {first_system}" if first_system else "")}],
    })
    st["game"]["candidates"].append(m)
    st["log"].append({"t": _now(), "added_candidate": m["id"], "name": name})
    save(st)
    return m


def add_system(st, obj_id, system):
    """Record one more system where the patch works (for a candidate or a monster).
    This is how a candidate accumulates the evidence needed to become a monster."""
    bucket, _, obj = _find(st, obj_id)
    if obj is None:
        return False, f"id '{obj_id}' not found"
    if system in obj["systems_validated"]:
        return True, f"system '{system}' already recorded ({len(obj['systems_validated'])} total)"
    obj["systems_validated"].append(system)
    obj["updated"] = _now()
    obj.setdefault("history", []).append({"t": _now(), "event": "system_added", "detail": system})
    save(st)
    n = len(obj["systems_validated"])
    hint = "" if n >= MIN_SYSTEMS_FOR_MONSTER or bucket != "candidates" else \
        f" (need >= {MIN_SYSTEMS_FOR_MONSTER} to become a monster)"
    return True, f"system '{system}' added -> {n} system(s){hint}"


def note(st, obj_id, text):
    """Append a free-text note to an object's history (any bucket). This is the SANCTIONED
    way to record a finding on a candidate/monster/card — so the tool stays the single entry
    point and game.json is NEVER hand-edited. Does not change bucket/status."""
    bucket, _, obj = _find(st, obj_id)
    if obj is None:
        return False, f"id '{obj_id}' not found"
    obj["updated"] = _now()
    obj.setdefault("history", []).append({"t": _now(), "event": "note", "detail": text})
    save(st)
    return True, f"note added to {obj_id} ({bucket}); history now {len(obj['history'])} entries"


def confirm_monster(st, obj_id, judgement=None):
    """LEVEL 2: candidate -> MONSTER. The >= MIN_SYSTEMS_FOR_MONSTER systems requirement is a FLOOR
    (anti-coincidence), NOT the whole decision. The actual call is the PLAYER's JUDGEMENT: given the
    patch's NATURE + the systems where it works, do the indices justify "monster"? Subjective by
    design — if you were SURE, it'd already be a card. `judgement` (optional) records that reasoning.
    The monster enters the bestiary WITH its list of working systems; the WHY is still unknown."""
    bucket, _, obj = _find(st, obj_id)
    if obj is None:
        return False, f"id '{obj_id}' not found"
    if bucket != "candidates":
        return False, f"'{obj_id}' is in '{bucket}', only a candidate can be confirmed to a monster"
    n = len(obj["systems_validated"])
    if n < MIN_SYSTEMS_FOR_MONSTER:
        return False, (f"REFUSED: only {n} system(s) — below the floor of {MIN_SYSTEMS_FOR_MONSTER} "
                       f"(else likely a coincidence). Add more systems, then it's YOUR judgement call.")
    obj["status"] = "monster"
    detail = f"player judgement; {n} systems: {obj['systems_validated']}"
    if judgement:
        obj["judgement"] = judgement
        detail += f" — {judgement}"
    _move(st, obj, "candidates", "monsters", "confirmed_monster", detail)
    save(st)
    return True, (f"MONSTER confirmed by JUDGEMENT ({n} systems — floor met, the call was yours). "
                  f"In the bestiary; now hunt the WHY (ideally on a SIMPLE system). "
                  f"If you were sure, it'd be a card — it's a monster precisely because you're not.")


def promote(st, obj_id, why, certainty):
    """LEVEL 3: monster -> CARD. Enforces invariant #8: needs a mechanistic WHY + certainty >= high.
    A candidate canNOT be promoted directly to a card — it must first become a monster
    (validated on >= 2 systems via confirm_monster)."""
    bucket, _, obj = _find(st, obj_id)
    if obj is None:
        return False, f"id '{obj_id}' not found"
    if bucket == "candidates":
        return False, (f"'{obj_id}' is still a CANDIDATE. Confirm it to a monster first "
                       f"(validate on >= {MIN_SYSTEMS_FOR_MONSTER} systems), then promote.")
    if bucket != "monsters":
        return False, f"'{obj_id}' is in '{bucket}', only a monster can be promoted"
    if not why or not why.strip():
        return False, "REFUSED: a card REQUIRES a mechanistic WHY (the debunk). None given."
    if certainty not in CERTAINTY_LEVELS or CERTAINTY_LEVELS.index(certainty) < CERTAINTY_LEVELS.index("high"):
        return False, (f"REFUSED: certainty='{certainty}' too low. A card REQUIRES CERTAINTY "
                       f"(>= 'high'). Keep it a monster, extend tests on other lots (invariant #8).")
    obj["why"] = why
    obj["why_status"] = "found"
    obj["certainty"] = certainty
    obj["status"] = "card"
    _move(st, obj, "monsters", "cards", "promoted_to_card", why)
    save(st)
    return True, ("CARD minted. SORTIE DU MODE CHERCHEUR -> repasse reviewer/webmaster pour "
                  "intégrer cette carte à la théorie (7 fichiers sacrés + site + PDF).")


def kill(st, obj_id, reason):
    """candidate/monster -> ERROR (refuted patch, e.g. a coincidence that didn't generalize)."""
    bucket, _, obj = _find(st, obj_id)
    if obj is None:
        return False, f"id '{obj_id}' not found"
    if bucket == "errors":
        return False, "already an error"
    obj["status"] = "error"
    _move(st, obj, bucket, "errors", "killed", reason)
    save(st)
    return True, f"moved '{obj_id}' (was {bucket[:-1]}) to errors: {reason}"


def abandon(st, obj_id, reason):
    """Mark a monster abandoned (kept in monsters bucket, status=abandoned) so it is
    re-tested each new card — this is where 'the magic' is measured."""
    bucket, idx, obj = _find(st, obj_id)
    if obj is None:
        return False, f"id '{obj_id}' not found"
    if bucket != "monsters":
        return False, f"only a monster can be abandoned (this is in '{bucket}')"
    obj["status"] = "abandoned"
    obj["updated"] = _now()
    obj.setdefault("history", []).append({"t": _now(), "event": "abandoned", "detail": reason})
    st["game"]["monsters"][idx] = obj
    st["log"].append({"t": _now(), "abandoned": obj_id, "detail": reason})
    save(st)
    return True, f"abandoned '{obj_id}' (kept for re-test): {reason}"


def list_objs(st, which="all"):
    valid = ("candidates", "monsters", "cards", "errors")
    if which == "all":
        buckets = valid
    elif which in valid:
        buckets = (which,)
    else:
        raise ValueError(f"list: '{which}' invalid; use one of {valid} or 'all'")
    return {b: st["game"].get(b, []) for b in buckets}


def show(st, obj_id):
    _, _, obj = _find(st, obj_id)
    return obj


def magic_report(st):
    """The 'magic' metric: as cards accumulate, abandoned cases should resolve.
    Reports counts; a rising resolved/abandoned ratio across rounds = the engine works."""
    monsters = st["game"]["monsters"]
    abandoned = [m for m in monsters if m.get("status") == "abandoned"]
    active = [m for m in monsters if m.get("status") == "monster"]
    return {
        "candidates": len(st["game"].get("candidates", [])),
        "cards": len(st["game"]["cards"]),
        "active_monsters": len(active),
        "abandoned_monsters": len(abandoned),
        "errors": len(st["game"]["errors"]),
        "note": ("magic check: with more cards, abandoned monsters should become "
                 "promotable. Re-run retest after each new card and watch this drop."),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _opt(args, key, default=None):
    if key in args:
        i = args.index(key)
        if i + 1 < len(args):
            return args[i + 1]
    return default


def _print_obj(o, full=False):
    if o is None:
        print("  (not found)")
        return
    tag = {"candidate": "🥚", "monster": "🦠", "card": "🃏", "error": "❌",
           "abandoned": "💤"}.get(o.get("status"), "?")
    sysv = o.get("systems_validated", [])
    nsys = len(sysv)
    print(f"  {tag} [{o['id']}] {o['name']}  ({o['status']}, {nsys} system{'s' if nsys != 1 else ''})")
    print(f"      external_theory: {o.get('external_theory')}")
    print(f"      patch          : {o.get('patch')}")
    print(f"      systems        : {sysv}")
    print(f"      why_status     : {o.get('why_status')}  certainty: {o.get('certainty')}")
    if o.get("why"):
        print(f"      why (debunk)   : {o.get('why')}")
    if full:
        for h in o.get("history", []):
            print(f"        - {h.get('t')}: {h.get('event')} :: {h.get('detail')}")


def main(argv):
    st = load()
    if not argv:
        print(__doc__)
        return 0
    cmd = argv[0]

    if cmd == "list":
        which = argv[1] if len(argv) > 1 else "all"
        try:
            objs = list_objs(st, which)
        except ValueError as e:
            print(str(e))
            return 1
        for bucket, items in objs.items():
            print(f"=== {bucket} ({len(items)}) ===")
            for o in items:
                _print_obj(o)
        return 0

    if cmd == "show" and len(argv) > 1:
        _print_obj(show(st, argv[1]), full=True)
        return 0

    if cmd == "add-candidate" and len(argv) > 1:
        m = add_candidate(st, argv[1], _opt(argv, "--theory", "?"), _opt(argv, "--patch", "?"),
                          _opt(argv, "--system"))
        print(f"candidate created: {m['id']} ({argv[1]})")
        _print_obj(m)
        return 0

    if cmd == "add-system" and len(argv) > 1:
        ok, msg = add_system(st, argv[1], _opt(argv, "--system", "?"))
        print(("OK: " if ok else "") + msg)
        return 0 if ok else 1

    if cmd == "confirm-monster" and len(argv) > 1:
        ok, msg = confirm_monster(st, argv[1], _opt(argv, "--judgement"))
        print(("OK: " if ok else "") + msg)
        return 0 if ok else 1

    if cmd == "promote" and len(argv) > 1:
        ok, msg = promote(st, argv[1], _opt(argv, "--why", ""), _opt(argv, "--certainty", "low"))
        print(("OK: " if ok else "") + msg)
        return 0 if ok else 1

    if cmd == "kill" and len(argv) > 1:
        ok, msg = kill(st, argv[1], _opt(argv, "--reason", "no reason given"))
        print(("OK: " if ok else "") + msg)
        return 0 if ok else 1

    if cmd == "abandon" and len(argv) > 1:
        ok, msg = abandon(st, argv[1], _opt(argv, "--reason", "no reason given"))
        print(("OK: " if ok else "") + msg)
        return 0 if ok else 1

    if cmd == "magic":
        print(json.dumps(magic_report(st), indent=2, ensure_ascii=False))
        return 0

    if cmd == "selftest":
        return 0 if _selftest() else 1

    print(__doc__)
    return 0


# ---------------------------------------------------------------------------
# offline self-test (uses a temp game.json, restores the real one)
# ---------------------------------------------------------------------------
def _selftest():
    global STATE_FILE
    print("=== bestiary.py self-test (offline, temp state) ===")
    real = STATE_FILE
    STATE_FILE = os.path.join(HERE, ".bestiary_selftest.json")
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
    ok = True

    def check(name, cond):
        nonlocal ok
        ok = ok and cond
        print(f"  [{'OK' if cond else 'FAIL'}] {name}")

    # LEVEL 1: candidate (one system) -> goes to candidates, NOT bestiary
    st = load()
    m = add_candidate(st, "wide-binary-triples", "hidden-triple contamination model",
                      "raise triple fraction by X", first_system="1kAU")
    mid = m["id"]
    check("candidate created (not a monster)",
          len(load()["game"]["candidates"]) == 1 and len(load()["game"]["monsters"]) == 0)

    # candidate cannot be promoted straight to card
    st = load()
    okp, _ = promote(st, mid, "some why", "certain")
    check("promote refused for a candidate", not okp)

    # confirm_monster REFUSED with only 1 system (anti-coincidence)
    st = load()
    okc, _ = confirm_monster(st, mid)
    check("confirm refused with 1 system", not okc)

    # add a 2nd system -> now confirm works
    st = load()
    add_system(st, mid, "3kAU")
    st = load()
    okc, msg = confirm_monster(st, mid)
    check("confirm OK with 2 systems", okc)
    check("now a monster, not candidate",
          len(load()["game"]["monsters"]) == 1 and len(load()["game"]["candidates"]) == 0)

    # LEVEL 3: promotion gates
    st = load()
    okp, _ = promote(st, mid, "", "high")
    check("promote refused without why", not okp)
    st = load()
    okp, _ = promote(st, mid, "triples mimic boost because ...", "low")
    check("promote refused with low certainty", not okp)
    st = load()
    okp, msg = promote(st, mid, "triples inflate v at fixed sep -> debunk", "high")
    check("promote accepted with why+high", okp)
    check("SORTIE message present", "reviewer/webmaster" in msg)
    check("now in cards", len(load()["game"]["cards"]) == 1 and len(load()["game"]["monsters"]) == 0)

    # abandon path (monster kept for re-test) + magic report
    st = load()
    m2 = add_candidate(st, "m2", "theoryB", "patchB", first_system="sysA")
    st = load(); add_system(st, m2["id"], "sysB")
    st = load(); confirm_monster(st, m2["id"])
    st = load()
    oka, _ = abandon(st, m2["id"], "no why after 3 tries")
    check("abandon ok", oka)
    rep = magic_report(load())
    check("magic: 1 card, 1 abandoned", rep["cards"] == 1 and rep["abandoned_monsters"] == 1)

    # kill path (a candidate that turned out a coincidence)
    st = load()
    m3 = add_candidate(st, "m3", "theoryC", "patchC", first_system="sysX")
    st = load()
    okk, _ = kill(st, m3["id"], "coincidence, failed on other systems")
    check("kill candidate -> errors", okk and len(load()["game"]["errors"]) == 1)

    os.remove(STATE_FILE)
    STATE_FILE = real
    print("  SELFTEST_OK" if ok else "  SELFTEST_FAILED")
    return ok


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
