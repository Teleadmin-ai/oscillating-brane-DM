#!/usr/bin/env python3
"""
obt_game.py — the OBT card-game orchestrator (CHERCHEUR mode).

This is the GATE-ENFORCING STATE MACHINE described in chercheur-game.md §9-ter.
Its whole purpose is to stop the pilot (me, Claude — I am the PLAYER) from derailing into
AUDIT mode: before every command it re-shows Romain's §0 principles + the player-judgement
note + the per-command instruction, and the typed game state (terrains / candidates /
monsters / cards / errors) lives in game.json.

It does NOT do physics. It orchestrates: it tells me which step I'm on, its rule, the gate,
and delegates to the sibling modules — catalogs (Stage 1 data), obt_formulas (Stage 2 fixed
OBT predictions), bestiary (candidate->monster->card lifecycle). Heavy compute / DB sieving
are reserved for monster->card proof, never for testing an OBT prediction.

Usage (interactive):   python3 obt_game.py        (then type commands; `help` is implicit)
Usage (one-shot):      python3 obt_game.py <command> [args]
The 5 research commands (tables/columns/sieve/inspect/propagate) + the lifecycle commands
(candidate/add-system/confirm-monster/promote/kill/abandon) are all wired; see HELP/COMMAND_HELP.
"""

import json
import os
import shlex
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(HERE, "game.json")
MEM_REMINDER = "chercheur-memory.md"
SPEC_FILE = os.path.join(HERE, "chercheur-game.md")  # source of truth for the principles (§0)

# Sibling modules wired into the loop (lazy-imported in handlers so `status`/`rules`
# work even if optional deps like pyvo/pandas aren't installed):
#   catalogs     -> Stage 1 data (TAP/cache/sieve/lots/agents)
#   obt_formulas -> Stage 2 fixed OBT predictions
#   bestiary     -> monster/card/error lifecycle (shares this game.json)

MODE_BANNER = "=== MODE CHERCHEUR ===  (axiom: OBT presupposed TRUE — never test OBT here)"


def load_principles(spec=SPEC_FILE):
    """Read the §0 PRINCIPES block from chercheur-game.md (single source of truth) so the
    tool can re-show Romain's own principles before every command — NOT a hardcoded copy.
    Extracts from the '## §0.' header up to (but excluding) the next '## ' header.
    Returns the block text, or a short fallback if the file/section is missing."""
    try:
        with open(spec, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError:
        return None
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith("## §0"):  # tolerate "## §0." / "## §0 " etc.
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return "\n".join(lines[start:end]).strip()

# ---------------------------------------------------------------------------
# The state machine. Each state: its rule, and what object it may produce.
# Order encodes the loop of chercheur-game.md.
# ---------------------------------------------------------------------------
STATES = [
    (
        "PICK_TERRAIN",
        "Pick a configuration TYPE + its variants. RUN GATE #4: it must have "
        "(a) an OBT prediction WITH an observable gap, (b) a patchable adjacent EXTERNAL "
        "theory, (c) VARIANTS. Missing any -> NOT a terrain (a naked OBT prediction like "
        "613 Mpc is NOT playable).",
        "terrain",
    ),
    (
        "COMPUTE_OBT_PREDICTION",
        "Compute what OBT PREDICTS in this system (fixed formulas: a0=cH(z)/2pi, "
        "mu(x)=x/sqrt(1+x^2), sinc(pi*t_dyn/T), lambda=cT ...). This is USING OBT as an "
        "axiom, NOT testing it.",
        "prediction",
    ),
    (
        "FIND_MISFIT",
        "Find where the standard external analysis disagrees with OBT's prediction = the "
        "GAP. The defect is EXTERNAL (we presuppose OBT true). FIRST suspect my own "
        "misapplication of OBT (category a) before blaming the external theory.",
        "misfit",
    ),
    (
        "PROPOSE_PATCH_CANDIDATE",
        "Modify ONE parameter of the ADJACENT EXTERNAL theory so OBT+patch+the-rest works on "
        "ONE system -- even without understanding why. Never glue OBT. This is a CANDIDATE "
        "(level 1): could be a coincidence, so it does NOT enter the bestiary yet.",
        "candidate",
    ),
    (
        "VALIDATE_ON_SYSTEMS",
        "Carry the SAME patch onto MORE systems (light pre-sieve / cheap compute). Each system "
        "where OBT+patch+the-rest works is recorded (add-system). A failed leg does not "
        "contaminate the others. Goal: accumulate the evidence that it is NOT a coincidence.",
        "patch_result",
    ),
    (
        "CONFIRM_MONSTER",
        "JUDGEMENT CALL (you are the player): given the patch's NATURE + the systems where it "
        "works, do the indices justify calling it a MONSTER (level 2)? Subjective by design -- "
        "if you were SURE it'd already be a card. >=2 systems is the floor, not the whole "
        "decision. Else: keep validating, or TO_ERROR if it looks like a coincidence.",
        "monster",
    ),
    (
        "FIND_WHY",
        "Find WHY the patch works = the mechanistic debunk of the external theory, IDEALLY on a "
        "SIMPLE system (external theory with little around it besides OBT). Only-numeric fit "
        "(epicycle) -> reject. BIG COMPUTE is allowed HERE ONLY, to PROVE the debunk (->card).",
        "why",
    ),
    (
        "RESOLVE",
        "Decide the monster's fate: PROMOTE_CARD (why understood + certainty>=high) | keep as "
        "monster | abandon (re-test later) | TO_ERROR (refuted). A card REQUIRES CERTAINTY.",
        "resolution",
    ),
    (
        "RETEST_ABANDONED",
        "Re-test ALL abandoned cases + monsters against the updated game (OBT+cards). "
        "Measure 'the magic': resolution rate of abandoned cases must RISE with card count.",
        "retest",
    ),
]
STATE_NAMES = [s[0] for s in STATES]
STATE_RULE = {s[0]: s[1] for s in STATES}
STATE_OBJECT = {s[0]: s[2] for s in STATES}

# The 4 gate checks (chercheur-game.md §0.5), asked before any action.
GATE = [
    "AXIOM  : Does this action PRESUPPOSE OBT is true? If it would verify/confirm/refute "
    "OBT or an OBT prediction -> STOP (that is AUDIT = hors-jeu).",
    "STEP   : Does it map to the current game step's allowed work? If not -> STOP.",
    "OBJECT : Will it produce one of {misfit, patch, monster, card, error}? If the output "
    "is 'a verdict on OBT' -> STOP.",
    "TERRAIN: (only at PICK_TERRAIN) does the case have the 3 ingredients? If not -> not a terrain.",
]


def now():
    # Date passed via env to stay deterministic-friendly; fallback to a fixed note.
    return os.environ.get("OBT_GAME_DATE", "date-unset")


def default_state():
    return {
        "mode": "CHERCHEUR",
        "state": "PICK_TERRAIN",
        "game": {"candidates": [], "monsters": [], "cards": [], "errors": [], "terrains": []},
        "naked_obt_predictions": [
            "lambda=cT=613 Mpc (cymatic fundamental)",
            "a0=cH(z)/2pi (instantaneous)",
            "SKA 21cm modulation",
            "Penrose-Diosi 5D collapse",
        ],
        "log": [],
    }


def load():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            st = json.load(f)
    else:
        st = default_state()
    # tolerate older/partial game.json: ensure all buckets + keys exist
    st.setdefault("game", {})
    for b in ("candidates", "monsters", "cards", "errors", "terrains"):
        st["game"].setdefault(b, [])
    st.setdefault("state", "PICK_TERRAIN")
    st.setdefault("naked_obt_predictions", default_state()["naked_obt_predictions"])
    st.setdefault("log", [])
    return st


def save(st):
    with open(STATE_FILE, "w") as f:
        json.dump(st, f, indent=2, ensure_ascii=False)


def banner(st, principles=True):
    print(MODE_BANNER)
    print("┌─ RÈGLE N°1 — DANS LE JEU, OBT A TOUJOURS RAISON (Romain) ──────────────────────┐")
    print("│ OBT est l'AXIOME : il a TOUJOURS raison. Un écart entre OBT et la donnée n'est")
    print("│ JAMAIS 'OBT se trompe / OBT sur- ou sous-prédit' — c'est qu'un ÉLÉMENT EXTERNE")
    print("│ (théorie adjacente, approximation, systématique, modèle de population) est à patcher.")
    print("│ Dire 'tension pour OBT' / 'OBT échoue' = HORS-JEU (audit). Le défaut est EXTERNE. Toujours.")
    print("│ OBT = la CARTE #1, TOUJOURS VALIDE. Le DOUTE ne porte QUE sur les PATCHES/MONSTRES :")
    print("│ comprendre la NATURE du monstre → CARTE ; PROUVER le patch FAUX → KILL le monstre. Jamais OBT.")
    print("└" + "─" * 80 + "┘")
    if principles:
        p = load_principles()
        if p:
            print("┌─ PRINCIPES (chercheur-game.md §0 — source de vérité, rappelés à chaque commande) ─┐")
            for ln in p.splitlines():
                print("│ " + ln)
            print("└" + "─" * 78 + "┘")
        else:
            print(f"  (!) §0 principles not found in {os.path.basename(SPEC_FILE)} — read it manually.")
    print("┌─ TU ES LE JOUEUR (Romain, à garder en contexte) ──────────────────────────────┐")
    print("│ Ce jeu n'est PAS entièrement automatisable. Le passage candidat→monstre est un")
    print("│ JUGEMENT subjectif: à toi de juger si la NATURE du patch + les systèmes où il marche")
    print("│ donnent assez d'indices pour le classer monstre. Subjectif PAR DESIGN: si tu étais")
    print("│ SÛR, ce serait déjà une CARTE, pas un monstre. Le seuil ≥2 systèmes est un plancher,")
    print("│ pas la décision. Compte sur ta pertinence, pas sur un seuil mécanique.")
    print("└" + "─" * 80 + "┘")
    print("┌─ TON AVANTAGE & TA PERSÉVÉRANCE (Romain) ─────────────────────────────────────┐")
    print("│ La communauté n'avait PAS OBT. Ici OBT est présupposé vrai → c'est ton AVANTAGE :")
    print("│ un cas 'non résolu par eux' est une OPPORTUNITÉ, pas un mur. OBT = pierre de Rosette.")
    print("│ Si tu ne comprends pas le patch sur CE système, applique-le à des systèmes PLUS")
    print("│ SIMPLES (il peut exister plusieurs patches) — à force, un système simple révélera")
    print("│ POURQUOI le patch est bon : là tu auras compris ce qu'eux n'ont pas pu.")
    print("│ Ne t'acharne pas trop longtemps : passe à une autre carte. Chaque carte gagnée")
    print("│ rend les suivantes (même abandonnées) plus faciles. But ultime : parler au bulk.")
    print("│ COMPRENDRE LE POURQUOI: un système SIMPLE (OBT+monstre, peu d'autre physique autour)")
    print("│ donne le plus de chances — mais un AUTRE élément peut aussi interférer/trahir la vraie")
    print("│ mécanique du patch. Et si chaque système pris seul reste opaque, COMPARE les systèmes")
    print("│ qui marchent avec le MÊME patch : ce qui change de l'un à l'autre révèle la mécanique.")
    print("└" + "─" * 80 + "┘")
    print("┌─ BATTERIE DE CONFIGURATIONS (Romain) ─────────────────────────────────────────┐")
    print("│ Quand tu tiens un monstre, TESTE-LE sur ~6+ TYPES de systèmes DIFFÉRENTS sans")
    print("│ chercher à comprendre chacun. NE T'ATTENDS PAS à ce que ça marche à chaque coup :")
    print("│ il faut essayer une dizaine de configurations (au moins ~6) de types variés.")
    print("│ But: repérer le système qui TRAHIT le mécanisme du monstre (→ une CARTE),")
    print("│ ou voir émerger UN AUTRE MONSTRE. L'échec d'une config n'est pas un mur — c'est")
    print("│ un point de contraste qui, comparé aux configs qui marchent, révèle la mécanique.")
    print("│ PERSISTE avec un monstre tant qu'il RETOURNE DES CHOSES UTILES et surtout tant")
    print("│ qu'il MARCHE SUR D'AUTRES SYSTÈMES : même sans comprendre sa NATURE, si — associé")
    print("│ à OBT (et/ou au jeu OBT+cartes) — il donne des CHIFFRES COHÉRENTS sur plusieurs")
    print("│ systèmes, CONTINUE (fais plus que 6 configs s'il est fécond). Tu finiras par")
    print("│ l'avoir, et même opaque il OUVRE DES PISTES (logue-les). Fécondité > compréhension immédiate.")
    print("│ SÉQUENCE: (1) CRÉE le patch sur un site PROPRE (SANS PARASITE — le jeu OBT+cartes + au")
    print("│ plus UN intervenant externe) où OBT+cartes ne suffit pas encore ; (2) PROPAGE le MÊME")
    print("│ patch à d'autres sites et COMPARE ; (3) TROUVER DES SYSTÈMES QUI MARCHENT SOUVENT avec le")
    print("│ patch = PROGRÈS qui VALIDE le monstre ET valide de CONTINUER la quête monstre→carte →")
    print("│ INSISTE pour le comprendre. Un ÉCHEC sur UN site (après succès ailleurs) ≠ kill : passe")
    print("│ à un AUTRE site, n'ABANDONNE PAS le monstre. KILL seulement si ça échoue SYSTÉMATIQUEMENT")
    print("│ (plein de fois sans aucun résultat valide). Ton SAVOIR (domaine) choisit le site propre.")
    print("└" + "─" * 80 + "┘")
    print("┌─ DEBUNKER LE MONSTRE = LE TRANSFORMER EN CARTE (Romain) ───────────────────────┐")
    print("│ LE MONSTRE EST LUI-MÊME UNE THÉORIE EXTERNE À OBT. Pour en faire une CARTE il faut")
    print("│ le DEBUNKER (montrer ce qu'il EST vraiment dans le langage d'OBT), PAS le confirmer :")
    print("│ le confirmer sur N systèmes le garde monstre (ou t'en fait trouver un AUTRE).")
    print("│ MÉTHODE = ISOLER. Prends la variante la PLUS SIMPLE où seul LE JEU (OBT + le monstre)")
    print("│ opère avec RIEN D'AUTRE — ou avec UN SEUL autre intervenant. Puis COMPARE les variantes.")
    print("│ Ce seul autre intervenant est UNE AUTRE THÉORIE EXTERNE (juste ou fausse). Si elle est")
    print("│ JUSTE, elle COINCE le monstre entre elle et OBT et aide à le DEBUNKER (révèle sa nature).")
    print("│ ET: LE MONSTRE EST UNE HYPOTHÈSE DE CARTE (jamais 'pas une carte'): carte = monstre + le POURQUOI.")
    print("│ UNE CARTE N'EST FRAPPÉE QUE SI COMPRISE ET PROUVÉE VRAIE → elle est TOUJOURS VALIDE")
    print("│ (comme OBT, carte #1). Donc le JEU = OBT + {cartes} est TOUJOURS VALIDE. SCOPE la carte")
    print("│ pour qu'elle ne contienne QUE le PROUVÉ ; le non-prouvé reste monstre/lead, pas carte.")
    print("└" + "─" * 80 + "┘")
    print("┌─ INTÉGRER UNE CARTE PROUVÉE — DROIT DE PUSH ACCORDÉ (Romain) ──────────────────┐")
    print("│ J'AI LE DROIT d'écrire ET de PUSHER une carte PROUVÉE SANS accord par-push, SOUS")
    print("│ CES CONDITIONS (toutes requises) : (1) ça ne MODIFIE PAS OBT (on corrige une théorie")
    print("│ EXTERNE, on n'ampute/patche jamais OBT) ; (2) j'ai des PREUVES SOLIDES (même si elles")
    print("│ s'appuient aussi sur OBT) ; (3) ça va dans discoveries.md, IDÉALEMENT dans une section")
    print("│ dédiée 'debunks de théories externes', OU AU MINIMUM en mentionnant explicitement la")
    print("│ NATURE de DEBUNK-DE-THÉORIE-EXTERNE de la découverte ; (4) CADRE HONNÊTE : 'cadre d'OBT (vrai")
    print("│ si OBT vrai)', et si la correction est falsifiable INDÉPENDAMMENT d'OBT, le DIRE.")
    print("│ ACCORD EXPLICITE REQUIS UNIQUEMENT pour AMPUTER ou PATCHER OBT lui-même. Edit d'un")
    print("│ fichier sacré ⇒ workflow sacré (MAJ CLAUDE.md, régénérer PDF, push). Preuves pas solides → pas carte.")
    print("└" + "─" * 80 + "┘")
    print("┌─ LE JEU GRANDIT — BOUCLE RÉCURSIVE (Romain, principe central) ─────────────────┐")
    print("│ Une carte frappée → le JEU DE RÉFÉRENCE devient OBT + {toutes les cartes}. On")
    print("│ RECOMMENCE la MÊME approche en EMBARQUANT les cartes : on cherche des systèmes que")
    print("│ OBT + {cartes} n'explique PAS ENCORE → nouveau MONSTRE (patch d'une théorie externe)")
    print("│ → preuve/pourquoi → nouvelle CARTE → on recommence. Le set de cartes GROSSIT sans fin.")
    print("│ JAMAIS repartir d'OBT seul : chaque tour part du jeu DÉJÀ AGRANDI. 'LA MAGIE' : plus")
    print("│ de cartes → les suivantes (même les cas abandonnés) deviennent plus faciles à trouver.")
    print("└" + "─" * 80 + "┘")
    print("┌─ L'OUTIL EST LE SEUL POINT D'ENTRÉE (Romain) ─────────────────────────────────┐")
    print("│ INTERDICTION de passer par autre chose que CET outil (obt_game.py). Pas de script")
    print("│ bricolé à côté, pas d'édition directe de game.json. Besoin d'une capacité nouvelle ?")
    print("│ AJOUTE une commande/fonction DANS l'outil (handler cmd_*, COMMAND_HELP, _dispatch ;")
    print("│ analyses = une PROBE dans probes.py lancée par `probe <nom>`) — MÊME ARCHITECTURE.")
    print("│ Enregistrer une trouvaille sur un objet = `note <id> --text ...` (jamais game.json à la main).")
    print("│ APRÈS avoir codé l'outil: relire le CODE COMPLET en BOUCLE (bugs/améliorations)")
    print("│ jusqu'à 2 lectures complètes consécutives SANS rien trouver, avant de continuer.")
    print("└" + "─" * 80 + "┘")
    print("┌─ PROGRÈS = ON CONTINUE (Romain) ──────────────────────────────────────────────┐")
    print("│ N'ABANDONNE JAMAIS un fil qui PROGRESSE / donne de bons résultats. Acharnement ≠")
    print("│ persévérance : on ne SWITCHE de terrain QUE quand on fait du SURPLACE (≈10 essais")
    print("│ d'affilée sans aucun progrès). Tant que ça avance, on va JUSQU'AU BOUT — surtout")
    print("│ pour la PREMIÈRE carte (elle rend tout le reste plus facile : 'la magie').")
    print("│ Te demander 'dois-je abandonner / pivoter ?' ALORS QUE TU PROGRESSES = ERREUR. Continue.")
    print("└" + "─" * 80 + "┘")
    g = st["game"]
    print(f"  state = {st['state']}   |   candidates={len(g.get('candidates', []))} "
          f"monsters={len(g.get('monsters', []))} cards={len(g.get('cards', []))} "
          f"errors={len(g.get('errors', []))}")
    _print_facts(st)
    if MEM_REMINDER not in str(st.get("log", [])):
        print(f"  REMINDER: if {MEM_REMINDER} not read this session -> read it now.")
    print("-" * 70)


def _print_facts(st):
    """FAITS EN ATTENTE — FACTS ONLY, never a conclusion. The tool reports things it cannot
    be wrong about (counts, raw object state, the generic next step of the loop). It NEVER
    says 'you should...' / 'this is ready to...' — concluding is the player's job."""
    g = st["game"]
    cur = st["state"]
    nxt = STATE_NAMES[(STATE_NAMES.index(cur) + 1) % len(STATE_NAMES)] if cur in STATE_NAMES else "?"
    print("┌─ FAITS EN ATTENTE (faits bruts seulement — NON des conclusions; à TOI de juger) ─┐")
    print(f"│ séquence générique : étape courante = {cur}  →  étape suivante du circuit = {nxt}")
    cands = g.get("candidates", [])
    for o in cands:
        n = len(o.get("systems_validated", []))
        print(f"│ candidat [{o['id']}] {o['name']} : {n} système(s) validé(s)  (fait, pas un verdict)")
    for o in g.get("monsters", []):
        n = len(o.get("systems_validated", []))
        ws = o.get("why_status") or ("none" if not o.get("why") else "set")
        ab = " [abandonné]" if o.get("status") == "abandoned" else ""
        print(f"│ monstre  [{o['id']}] {o['name']} : {n} système(s), why_status = {ws}{ab}")
    if not cands and not g.get("monsters"):
        print("│ (aucun candidat ni monstre en cours)")
    print("└" + "─" * 80 + "┘")


def print_rule(state):
    print(f"STEP RULE [{state}]:")
    print("  " + STATE_RULE[state])
    print(f"  -> legitimate object to produce: '{STATE_OBJECT[state]}'")


def run_gate(state):
    print("THE GATE — answer each (anything failing => STOP, action is hors-jeu):")
    for i, g in enumerate(GATE, 1):
        tag = "" if (i < 4 or state == "PICK_TERRAIN") else "  (N/A unless PICK_TERRAIN)"
        print(f"  {i}. {g}{tag}")


def cmd_status(st):
    # NB: the banner (§0 + player + TODO) is already printed by _show_header in _dispatch.
    print_rule(st["state"])
    g = st["game"]
    print(f"\nGAME STATE: {len(g.get('candidates', []))} candidates, {len(g['cards'])} cards, "
          f"{len(g['monsters'])} monsters, {len(g['errors'])} errors, "
          f"{len(g['terrains'])} terrains tried.")
    if g["cards"]:
        for c in g["cards"]:
            print(f"  CARD: {c.get('external_theory','?')} :: {c.get('why','?')}")
    print("\nNaked OBT predictions (NOT playable, never test):")
    for p in st["naked_obt_predictions"]:
        print(f"  - {p}")


def cmd_rules(st, state=None):
    state = state or st["state"]
    if state not in STATE_RULE:
        print(f"unknown state '{state}'. States: {', '.join(STATE_NAMES)}")
        return
    print_rule(state)
    print()
    run_gate(state)


def cmd_gate(st):
    # banner already printed by _show_header
    run_gate(st["state"])
    print("\n(Interactive use: confirm each check before doing the work for this step.)")


def cmd_advance(st):
    cur = st["state"]
    i = STATE_NAMES.index(cur)
    nxt = STATE_NAMES[(i + 1) % len(STATE_NAMES)]
    st["state"] = nxt
    st["log"].append({"t": now(), "from": cur, "to": nxt})
    save(st)
    print(f"advanced: {cur} -> {nxt}")
    print()
    print_rule(nxt)
    print()
    run_gate(nxt)


def cmd_record(st, obj_type, payload):
    """Record a simple object (terrain/error note) into the typed game state.
    NOTE: candidates/monsters/cards must go through the bestiary (rich schema + invariant
    gates), not here — see candidate / confirm-monster / promote. This handles terrain/error notes."""
    bucket = {"error": "errors", "terrain": "terrains"}.get(obj_type)
    if obj_type in ("card", "monster", "candidate"):
        print(f"use the bestiary for '{obj_type}': `candidate <name> --theory T --patch P` -> "
              f"add-system -> confirm-monster -> promote. (Rich schema + invariant gates there.)")
        return
    if bucket is None:
        print(f"refuse: '{obj_type}' is not a recordable game object "
              f"(allowed here: terrain, error; monsters/cards via bestiary).")
        return
    entry = {"t": now(), "note": payload}
    st["game"][bucket].append(entry)
    st["log"].append({"t": now(), "recorded": obj_type, "note": payload})
    save(st)
    banner(st)
    print(f"recorded {obj_type}: {payload}")


# --------------------------------------------------------------------------
# Wired-loop handlers: delegate to the sibling modules, gate first.
# --------------------------------------------------------------------------
def _kv(args):
    """Parse '--key value' pairs from a token list into a dict."""
    out = {}
    i = 0
    while i < len(args):
        if args[i].startswith("--") and i + 1 < len(args):
            out[args[i][2:]] = args[i + 1]
            i += 2
        else:
            i += 1
    return out


def cmd_sieve(st, args):
    """Stage 1: pre-sieve a catalog via TAP. GATE first (must presuppose OBT, must be
    a pre-registered prediction-driven query — never free-dredge)."""
    print("GATE before sieving (invariant #2: predict BEFORE you sieve, no free-dredge):")
    run_gate(st["state"])
    print("-" * 70)
    opts = _kv(args)
    service = opts.get("service")
    adql = opts.get("adql")
    lot = opts.get("lot")
    if not service or not adql:
        print("usage: sieve --service gaia --adql \"SELECT ...\" [--lot NAME]")
        return
    try:
        import catalogs
        df = catalogs.tap_query(service, adql)
    except Exception as e:
        print(f"sieve failed ({type(e).__name__}): {e}")
        return
    print(f"sieve -> {len(df):,} rows; columns: {list(df.columns)}")
    # show a PREVIEW so I can actually SEE the systems and judge them
    try:
        head, stats = catalogs.preview(df, top=int(opts.get("top", 10)))
        print("--- preview (head) ---")
        print(head.to_string(index=False, max_colwidth=24))
        if stats is not None:
            print("--- per-column min/median/max/count ---")
            print(stats.to_string())
    except Exception as e:
        print(f"(preview skipped: {e})")
    if lot:
        catalogs.save_lot(df, lot)


def cmd_tables(st, args):
    """Discover catalog TABLES (schema), optionally filtered: tables --service gaia [--match X]."""
    import catalogs

    opts = _kv(args)
    service = opts.get("service")
    if not service:
        print("usage: tables --service gaia [--match SUBSTR]")
        return
    try:
        rows = catalogs.list_tables(service, opts.get("match"))
    except Exception as e:
        print(f"tables failed ({type(e).__name__}): {e}")
        return
    print(f"{len(rows)} table(s) in '{service}'" + (f" matching '{opts['match']}'" if opts.get("match") else "") + ":")
    for name, desc in rows:
        print(f"  {name:45s} {desc}")


def cmd_columns(st, args):
    """Discover a table's COLUMNS: columns --service gaia --table gaiadr3.gaia_source."""
    import catalogs

    opts = _kv(args)
    service, table = opts.get("service"), opts.get("table")
    if not service or not table:
        print("usage: columns --service gaia --table SCHEMA.TABLE [--match SUBSTR]")
        return
    try:
        cols = catalogs.list_columns(service, table)
    except Exception as e:
        print(f"columns failed ({type(e).__name__}): {e}")
        return
    m = opts.get("match")
    for name, unit, desc in cols:
        if m and m.lower() not in (name + " " + desc).lower():
            continue
        print(f"  {name:28s} [{unit:8s}] {desc}")


def cmd_inspect(st, args):
    """Inspect a saved LOT: inspect <lot> [--cols a,b --sort c --top 30 --where "c>1"].
    Lets me re-examine extracted systems and judge which adjacent theory is at play."""
    import catalogs

    if not args or args[0].startswith("--"):
        print("usage: inspect <lot> [--cols a,b,c --sort col --top N --where \"expr\"]")
        return
    name = args[0]
    opts = _kv(args[1:])
    try:
        df = catalogs.load_lot(name)
    except Exception as e:
        print(f"inspect failed: {e}")
        return
    cols = opts.get("cols", "").split(",") if opts.get("cols") else None
    try:
        head, stats = catalogs.preview(df, cols=cols, sort=opts.get("sort"),
                                       top=int(opts.get("top", 20)), where=opts.get("where"))
    except Exception as e:
        print(f"inspect preview failed: {e}")
        return
    print(f"lot '{name}': {len(df):,} systems total")
    print(head.to_string(index=False, max_colwidth=24))
    if stats is not None:
        print("--- min/median/max/count ---")
        print(stats.to_string())


def cmd_propagate(st, args):
    """Auto-propagate MY patch across a lot and report FACTS (no conclusion).
    Two modes (expressions are MINE; the tool only executes & counts):
      simple : propagate <lot> --select "<expr>"                       (where does it hold?)
      verify : propagate <lot> --applies "<expr>" --patch-ok "<expr>" [--where "<expr>"]
               -> over the population where the patch APPLIES, report how many systems keep
                  OBT valid (patch_ok), which hold, which break. FACTS only — you classify."""
    import catalogs

    if not args or args[0].startswith("--"):
        print("usage: propagate <lot> --select \"<expr>\"   |   "
              "propagate <lot> --applies \"<expr>\" --patch-ok \"<expr>\" [--where \"<expr>\" --save L]")
        return
    name = args[0]
    opts = _kv(args[1:])
    try:
        df = catalogs.load_lot(name)
    except Exception as e:
        print(f"propagate failed: {e}")
        return

    # verify mode (auto-propagation + OBT-validity check)
    if opts.get("applies") and opts.get("patch-ok"):
        try:
            r = catalogs.propagate_verify(df, opts["applies"], opts["patch-ok"], opts.get("where"))
        except Exception as e:
            print(f"propagate(verify) failed: {e}")
            return
        print(f"FACTS for lot '{name}':")
        print(f"  population (where)        : {r['n_population']}")
        print(f"  patch APPLIES to          : {r['n_applies']} systems")
        print(f"  OBT+patch HOLDS (patch_ok): {r['n_holds']}  ({100*r['frac_holds']:.1f}%)")
        print(f"  BREAKS                    : {r['n_breaks']}")
        print("--- holds (head) ---")
        print(r["holds_df"].head(int(opts.get("top", 10))).to_string(index=False, max_colwidth=22))
        if r["n_breaks"]:
            print("--- breaks (head) ---")
            print(r["breaks_df"].head(int(opts.get("top", 10))).to_string(index=False, max_colwidth=22))
        if opts.get("save"):
            catalogs.save_lot(r["holds_df"], opts["save"])
        print("(facts only — YOU classify: coincidence / monster / card)")
        return

    # simple mode
    select = opts.get("select")
    if not select:
        print("usage: propagate <lot> --select \"<expr>\"   |   --applies/--patch-ok (verify mode)")
        return
    try:
        matched, n, total = catalogs.propagate(df, select)
    except Exception as e:
        print(f"propagate failed: {e}")
        return
    frac = (100.0 * n / total) if total else 0.0
    print(f"FACT: patch '{select}' holds on {n}/{total} systems ({frac:.1f}%) of lot '{name}'")
    print("--- matching systems (head) ---")
    print(matched.head(int(opts.get("top", 15))).to_string(index=False, max_colwidth=24))
    print("(fact only — YOU classify: coincidence / monster / card)")
    if opts.get("save"):
        catalogs.save_lot(matched, opts["save"])


def cmd_predict(st, args):
    """Stage 2: print an OBT fixed prediction for given inputs (USES OBT as axiom)."""
    import obt_formulas as F

    opts = _kv(args)
    what = (args[0] if args and not args[0].startswith("--") else opts.get("what", "constants"))
    try:
        if what == "a0z":
            z = float(opts.get("z", 0))
            print(f"a0(z={z}) = {float(F.a0_of_z(z)):.4e} m/s^2  (x{float(F.a0_of_z(z))/F.A0:.2f} vs z=0)")
        elif what == "sinc":
            td = float(opts.get("tdyn", 1.0))
            print(f"sinc_resonance(t_dyn={td} Gyr) = {float(F.sinc_resonance(td)):.4f}")
        elif what == "lambda":
            n = int(opts.get("n", 1))
            print(f"lambda/{n} = {float(F.lambda_harmonic(n)):.1f} Mpc")
        elif what == "all":
            print("=== OBT prediction sheet (computed, astropy-backed) ===")
            for nm, val, unit, note in F.prediction_sheet():
                vs = f"{val:.4e}" if isinstance(val, float) else str(val)
                print(f"  {nm:16s} = {vs:>12} {unit:7s}  {note}")
            print("=== cited result-constants (V8.2 pipelines, not recomputed) ===")
            for k, (v, note) in F.PREDICTIONS.items():
                print(f"  {k:18s} = {v:<10} {note}")
        else:
            print(f"a0(z=0) = {F.A0:.4e} m/s^2 | lambda = {F.LAMBDA_MPC:.1f} Mpc | T = {F.T_GYR} Gyr")
            print("predict subcommands: all | a0z --z Z | sinc --tdyn G | lambda --n N")
    except ValueError as e:
        print(f"predict: numeric argument expected ({e}).")


def cmd_candidate(st, args):
    """LEVEL 1: create a CANDIDATE via the bestiary (a patch on ONE external theory, ONE system).
    It is NOT a monster yet — validate on several systems then `confirm-monster`."""
    import bestiary

    opts = _kv(args)
    name = args[0] if args and not args[0].startswith("--") else opts.get("name", "unnamed")
    st2 = bestiary.load()
    m = bestiary.add_candidate(st2, name, opts.get("theory", "?"), opts.get("patch", "?"),
                               opts.get("system"))
    print(f"candidate created [{m['id']}] {name} on '{m['external_theory']}' "
          f"({len(m['systems_validated'])} system) — NOT a monster yet; "
          f"add-system then confirm-monster (needs >= {bestiary.MIN_SYSTEMS_FOR_MONSTER}).")


def _bestiary_action(action, args):
    import bestiary

    st2 = bestiary.load()
    if not args:
        print(f"usage: {action} <id> [--why ... --certainty high | --reason ...]")
        return
    obj_id = args[0]
    opts = _kv(args[1:])
    if action == "promote":
        ok, msg = bestiary.promote(st2, obj_id, opts.get("why", ""), opts.get("certainty", "low"))
    elif action == "confirm-monster":
        ok, msg = bestiary.confirm_monster(st2, obj_id, opts.get("judgement"))
    elif action == "add-system":
        ok, msg = bestiary.add_system(st2, obj_id, opts.get("system", "?"))
    elif action == "kill":
        ok, msg = bestiary.kill(st2, obj_id, opts.get("reason", "no reason given"))
    elif action == "abandon":
        ok, msg = bestiary.abandon(st2, obj_id, opts.get("reason", "no reason given"))
    elif action == "demote":
        ok, msg = bestiary.demote(st2, obj_id, opts.get("reason", "no reason given"))
    else:
        ok, msg = False, "unknown action"
    # bestiary already prefixes its own CARD/REFUSED messages; only add a prefix when it didn't.
    if msg.startswith(("CARD", "REFUSED")):
        print(msg)
    else:
        print(("OK: " if ok else "FAILED: ") + msg)


def cmd_bestiary_list(st, args):
    import bestiary

    st2 = bestiary.load()
    which = args[0] if args else "all"
    try:
        objs = bestiary.list_objs(st2, which)
    except ValueError as e:
        print(str(e))
        return
    for bucket, items in objs.items():
        print(f"=== {bucket} ({len(items)}) ===")
        for o in items:
            bestiary._print_obj(o)


def cmd_magic(st):
    import bestiary

    print(json.dumps(bestiary.magic_report(bestiary.load()), indent=2, ensure_ascii=False))


def cmd_probe(st, args):
    """Run a registered analysis probe THROUGH the tool (probes.py). No arg -> list probes.
    `probe <name> [--key value ...]` runs one. Probes report FACTS only; the player judges."""
    import probes
    if not args:
        print("registered probes (run via `probe <name>`):")
        for name, desc in probes.describe().items():
            print(f"  {name:18s} {desc}")
        return
    name = args[0]
    opts = _kv(args[1:])
    try:
        probes.run(name, opts)
    except Exception as e:
        print(f"probe '{name}' failed ({type(e).__name__}): {e}")


def cmd_note(st, args):
    """Append a finding to a bestiary object's history — the sanctioned alternative to editing
    game.json by hand. `note <id> --text \"...\"`."""
    import bestiary
    if not args:
        print("usage: note <id> --text \"...\"")
        return
    obj_id = args[0]
    opts = _kv(args[1:])
    text = opts.get("text")
    if not text:
        print("usage: note <id> --text \"...\"")
        return
    st2 = bestiary.load()
    ok, msg = bestiary.note(st2, obj_id, text)
    print(("OK: " if ok else "FAILED: ") + msg)


def cmd_agent(st, args):
    """Dispatch a Claude agent on a lot (Stage 3). The prompt MUST carry the chercheur
    rules; pass it via --prompt; optional --lot and --label."""
    import catalogs

    opts = _kv(args)
    prompt = opts.get("prompt")
    if not prompt:
        print("usage: agent --prompt \"...\" [--lot NAME --label L]")
        return
    try:
        path = catalogs.run_agent(prompt, label=opts.get("label", "mission"), lot_name=opts.get("lot"))
    except Exception as e:
        print(f"agent dispatch failed ({type(e).__name__}): {e}")
        return
    print(f"mission file: {path}")


HELP = ("commands:\n"
        "  status | rules [STATE] | gate | advance | reset | quit\n"
        "  predict [all | a0z --z Z | sinc --tdyn G | lambda --n N]  (Stage 2, OBT formulas)\n"
        "  tables --service gaia [--match X]  |  columns --service gaia --table T [--match X]\n"
        "  sieve --service gaia --adql \"...\" [--lot NAME --top N]   (Stage 1, TAP/cache + preview)\n"
        "  inspect <lot> [--cols a,b --sort c --top N --where \"expr\"]   (see/judge systems)\n"
        "  propagate <lot> --select \"<expr>\" [--save NEWLOT]   (does my patch hold elsewhere?)\n"
        "  candidate <name> --theory T --patch P [--system S]   (Level 1: ONE system)\n"
        "  add-system <id> --system S   |   confirm-monster <id>  (Level 2: needs >=2 systems)\n"
        "  list [candidates|monsters|cards|errors|all] | magic\n"
        "  promote <id> --why \"...\" --certainty high  (Level 3: monster->card) | "
        "kill <id> --reason ... | abandon <id> --reason ...\n"
        "  agent --prompt \"...\" [--lot NAME --label L]            (Stage 3)\n"
        "  probe [<name> --k v ...]   (run a registered analysis probe; no arg = list)\n"
        "  note <id> --text \"...\"     (append a finding to a bestiary object; never edit game.json)\n"
        "  record <terrain|error> <note>")


# Per-command instruction (the rule of the command you just typed). Shown after the §0
# principles on every command, so I have BOTH the general memo and the specific step rule.
COMMAND_HELP = {
    "status": "Show the full game state + the current step's rule. (read-only)",
    "rules": "Show a step's rule + the gate. `rules [STATE]` for any state.",
    "gate": "Re-display THE GATE (4 checks) to run before any action.",
    "advance": "Move to the NEXT state of the loop, re-printing its rule + the gate.",
    "predict": "Stage 2 — compute a FIXED OBT prediction (OBT as AXIOM, never a test). "
               "`predict all|a0z --z Z|sinc --tdyn G|lambda --n N`.",
    "tables": "Discover catalog TABLES (schema) to know what exists. `tables --service gaia [--match X]`.",
    "columns": "Discover a table's COLUMNS (which properties I can request). "
               "`columns --service gaia --table SCHEMA.TABLE [--match X]`.",
    "sieve": "Stage 1 — pre-sieve a catalog (TAP) + PREVIEW the systems so I can judge them. Must "
             "test a PRE-REGISTERED prediction, never free-dredge (invariant #2). Gate first.",
    "inspect": "Re-examine a saved lot (sort/filter/columns) to SEE the systems and judge which "
               "adjacent theory is in play. `inspect <lot> [--cols.. --sort.. --top.. --where..]`.",
    "propagate": "Test whether MY patch (a selection rule) holds on OTHER systems of a lot -> the "
                 "candidate->monster->card evidence. `propagate <lot> --select \"<expr>\" [--save L]`.",
    "candidate": "LEVEL 1 — create a CANDIDATE: patch ONE external theory so OBT+patch+the-rest "
                 "works on ONE system. NOT a monster yet (could be coincidence).",
    "add-system": "Record one more system where the patch works (builds the anti-coincidence "
                  "evidence a candidate needs to become a monster).",
    "confirm-monster": "LEVEL 2 — candidate -> MONSTER. >= 2 systems is the FLOOR, not the decision: "
                       "it's YOUR judgement (patch nature + systems). Subjective by design — if sure, "
                       "it'd be a card. Optional --judgement \"...\" records your reasoning.",
    "promote": "LEVEL 3 — monster -> CARD. Requires the mechanistic WHY (ideally found on a SIMPLE "
               "system) + certainty >= high. Refused otherwise. A card is added to OBT.",
    "demote": "RETRACT a card -> back to monster (an audit found residual doubt). `demote <id> --reason ...`. "
              "Use when a card fails the certainty bar; nothing in the sacred files is touched.",
    "kill": "Mark a candidate/monster an ERROR (refuted patch / coincidence).",
    "abandon": "Shelve a monster (kept for re-test as cards accumulate — 'the magic').",
    "list": "List objects by bucket: candidates|monsters|cards|errors|all.",
    "magic": "Report the magic metric (cards vs abandoned monsters).",
    "agent": "Stage 3 — dispatch a Claude agent on a lot. The prompt MUST carry the chercheur rules.",
    "record": "Record a terrain/error note into the game state.",
    "probe": "Run a REGISTERED analysis probe (probes.py) THROUGH the tool — never a side script. "
             "`probe` lists them; `probe <name> [--k v ...]` runs one (FACTS only).",
    "note": "Append a finding to a bestiary object's history (the ONLY sanctioned way — never edit "
            "game.json by hand). `note <id> --text \"...\"`.",
}


def _show_header(st, cmd):
    """Print the §0 principles (permanent memo) + the instruction for THIS command."""
    banner(st)
    instr = COMMAND_HELP.get(cmd)
    if instr:
        print(f"COMMANDE '{cmd}': {instr}")
        print("-" * 70)


def _dispatch(st, cmd, rest):
    """Shared dispatch for interactive and one-shot. rest = list of tokens.
    Prints §0 + the command's instruction first, then runs the handler.
    Returns True if handled (and possibly mutated st via sibling modules)."""
    if cmd not in COMMAND_HELP:
        return False
    _show_header(st, cmd)
    if cmd == "status":
        cmd_status(st)
    elif cmd == "rules":
        cmd_rules(st, rest[0] if rest else None)
    elif cmd == "gate":
        cmd_gate(st)
    elif cmd == "advance":
        cmd_advance(st)
    elif cmd == "predict":
        cmd_predict(st, rest)
    elif cmd == "tables":
        cmd_tables(st, rest)
    elif cmd == "columns":
        cmd_columns(st, rest)
    elif cmd == "sieve":
        cmd_sieve(st, rest)
    elif cmd == "inspect":
        cmd_inspect(st, rest)
    elif cmd == "propagate":
        cmd_propagate(st, rest)
    elif cmd == "candidate":
        cmd_candidate(st, rest)
    elif cmd == "list":
        cmd_bestiary_list(st, rest)
    elif cmd == "magic":
        cmd_magic(st)
    elif cmd in ("promote", "demote", "kill", "abandon", "confirm-monster", "add-system"):
        _bestiary_action(cmd, rest)
    elif cmd == "agent":
        cmd_agent(st, rest)
    elif cmd == "record":
        if len(rest) >= 2:
            cmd_record(st, rest[0], " ".join(rest[1:]))
        else:
            print("usage: record <terrain|error> <note>")
    elif cmd == "probe":
        cmd_probe(st, rest)
    elif cmd == "note":
        cmd_note(st, rest)
    else:
        return False
    return True


def interactive(st):
    banner(st)
    print_rule(st["state"])
    print("\n" + HELP)
    while True:
        try:
            line = input("obt-game> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        try:
            parts = shlex.split(line)  # respect quotes so pandas exprs survive intact
        except ValueError as e:
            print(f"parse error ({e}); check your quotes.")
            continue
        if not parts:
            continue
        cmd, rest = parts[0], parts[1:]
        if cmd in ("quit", "exit", "q"):
            break
        if cmd == "reset":
            st = default_state()
            save(st)
            print("state reset.")
            continue
        if not _dispatch(st, cmd, rest):
            print("?? " + HELP)
        # reload shared state in case a bestiary action mutated game.json
        st = load()


def main():
    st = load()
    if len(sys.argv) == 1:
        interactive(st)
        return
    cmd = sys.argv[1]
    rest = sys.argv[2:]
    if cmd == "reset":
        save(default_state())
        print("state reset.")
        return
    if not _dispatch(st, cmd, rest):
        print(__doc__)
        print(HELP)


if __name__ == "__main__":
    main()
