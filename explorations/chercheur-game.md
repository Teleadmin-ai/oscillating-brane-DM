# OBT-GAME — Spec & Operating Manual for the Consilience Engine

**This file is the CLAUDE.md of the OBT-Game software.** It holds (1) the method spec,
(2) the architecture to build, (3) the non-negotiable invariants, and (4) — enriched
progressively — Claude's own operating notes and the *agent prompts that work* for each
mission type. Claude pilots this tool with its agents; this file is its playbook.

Quarantined under `explorations/` (NOT V8.2, NOT in the PDF, NOT a theory file).
Author of the method: Romain Provencal. Status: design (prototype = `xi_613_analysis/`).

> ⛔ **GAME-MODE ONLY.** Everything in this file (esp. "presuppose OBT true / never test OBT")
> applies ONLY while explicitly playing the game. My DEFAULT is NORMAL mode = webmaster of OBT +
> critical auditor (axiom: OBT MAY BE WRONG; test/audit/never glue). The game stance must NEVER leak
> into normal/theory/site/PDF work. See memory [[feedback_two_modes]]. When in doubt → normal mode.

---

## §0. PRINCIPES — texte original de Romain (SOURCE DE VÉRITÉ, ne pas réinterpréter)
> Ce paragraphe est de Romain (fautes corrigées, sens INCHANGÉ). C'est LA définition du jeu.
> Tout le reste de ce fichier (gate, machine à états, taxonomie...) est de l'**échafaudage
> opérationnel de Claude AU SERVICE de ces principes — jamais au-dessus**. En cas de conflit,
> ce §0 gagne. **À me rappeler à chaque commande de l'outil**, car sans ça je dérive.

**On présuppose TOUJOURS qu'OBT marche.** On cherche d'abord où il marche pas *en apparence*,
dans un **type de configuration** similaire avec toutes ses **variantes** autour.

Ensuite on **modifie UN paramètre d'une théorie adjacente** (externe à OBT), sur un exemple qui
ne va pas, pour que **OBT + la théorie patchée + le reste** marchent — bien qu'on ne comprenne
**pas encore comment**. **Le principe absolu : on ne touche JAMAIS à OBT lui-même ; on patche un
élément extérieur.** Ce combo (OBT + théorie patchée) est un **MONSTRE POTENTIEL** (candidat) — à
ce stade ça peut n'être qu'une **coïncidence**, donc il n'entre PAS encore au bestiaire.

**Trois niveaux (cycle de vie) :**
1. **Candidat** — la manip faite sur **un seul** système. Peut être une coïncidence. Pas au bestiaire.
2. **Monstre** (entre au **bestiaire**) — **seulement après** validation que le patch marche sur
   **plusieurs systèmes** (sinon = coïncidence → jeté). On l'y range **avec la liste des systèmes où
   il marche**. On ne comprend **toujours pas pourquoi**.
3. **Carte** — **seulement SI** on comprend la **vraie raison** du patch (pourquoi il marche),
   **idéalement grâce à un système SIMPLE** (théorie externe patchée avec peu de choses autour à part
   OBT) ou par déduction propre. Le monstre devient alors un **correctif d'une théorie externe** qu'on
   **ajoute à OBT**.

Pour passer candidat → monstre : valider sur **plusieurs systèmes** (anti-coïncidence). Pour passer
monstre → carte : **comprendre le pourquoi**. Le jeu devient **OBT + {cartes}**. Et on recommence.

On cherche une nouvelle série de variantes où appliquer le jeu (OBT + debunks) ; là où ça ne marche
pas, on cherche un **nouveau paramètre sur un autre élément** pour faire marcher un **trio** ; si ça
colle souvent, on présuppose que c'est probablement vrai et on cherche le cas qui **explique** ce 2ᵉ
paramètre → nouvelle carte. Ainsi de suite. À la fin, en théorie, on aura debunké toutes les erreurs,
et **la preuve sera que ça marche partout sans plus aucun paramètre incompréhensible**. Si une
nouvelle erreur surgit, on recommence pour la debunker.

**Soupape :** si après X itérations on ne trouve pas, on essaie un autre paramètre sur un autre
élément du système pour trouver une autre carte.

**LA MAGIE :** plus on a de cartes (OBT + debunks), plus il sera facile de trouver celles qui
manquent — et même les cas qu'on avait abandonnés ressortiront tout seuls.

**TON AVANTAGE & TA PERSÉVÉRANCE (Romain).** La communauté n'avait PAS OBT. Ici OBT est
présupposé vrai → c'est l'AVANTAGE du jeu : un cas « non résolu par eux » est une OPPORTUNITÉ,
pas un mur — OBT est peut-être la **pierre de Rosette**. Si tu ne comprends pas le patch sur un
système, applique le MÊME patch à des systèmes **plus SIMPLES** (et il peut exister plusieurs
patches valides) ; à force, si OBT est juste, un système simple révélera **POURQUOI** le patch
est bon — et là tu auras compris ce que la communauté n'a pas pu. Ne t'acharne pas trop : si tu
bloques, passe à une AUTRE carte ; chaque carte gagnée rend les suivantes (même celles abandonnées)
plus faciles. But ultime : comprendre comment l'univers marche — « parler au bulk ».
**Comprendre le POURQUOI :** un système SIMPLE (OBT + monstre, peu d'autre physique autour) maximise
les chances de comprendre — MAIS un AUTRE élément peut interférer et trahir la vraie mécanique du
patch. Et si chaque système pris isolément reste opaque, **COMPARE les systèmes qui marchent avec le
MÊME patch** : ce qui change de l'un à l'autre (ce qui module l'amplitude/le signe) révèle souvent la
mécanique réelle — parfois mieux qu'un seul système simple.

## 0. What this is, in one sentence (Claude's condensed restatement of §0 above)
A recursive **consilience engine** with a THREE-level lifecycle: presuppose OBT true; patch ONE
ADJACENT (non-OBT) theory parameter so OBT+patch+the-rest works on a case → a **candidate** (could be
coincidence, NOT yet in the bestiary); validate it across **several systems** → it becomes a **monster**
in the bestiary (stored WITH the list of systems where it works), still not understood; carry it onto
MANY systems — ESPECIALLY SIMPLE ones where the external theory appears with little around it besides
OBT — to UNDERSTAND why the patch works; and ONLY IF the true mechanistic reason is understood does it
become a **card** (a correction of an external theory, added to OBT). The game is **OBT + {cards}**,
grown until everything works with no unexplained parameter left.

## 0.5 STANCE + THE ACTION GATE  — read BEFORE doing anything (this is where I derail)

**MODE FLAG = GAME, not AUDIT.** In the game, OBT is an **AXIOM (presupposed TRUE)**. Therefore
OBT's own predictions are TRUE by assumption. ANY action whose purpose is to *check / confirm /
refute OBT or one of its predictions* is **AUDIT-mode = HORS-JEU = FORBIDDEN here**.
*Why I derail:* my default pull is trained skepticism (= test the claim), and the prior Reviewer-2
days were genuinely audit-mode. Without this flag active I snap back to testing OBT (e.g. "measure
ξ(r) to see if 613 exists" — that is testing OBT → STOP). Catch it at the gate below.

**THE GATE — run these 4 checks BEFORE any action, especially any costly compute/download:**
1. **AXIOM CHECK.** Does this action PRESUPPOSE OBT is true? If instead it would verify/confirm/
   refute OBT or an OBT prediction → **STOP, hors-jeu.**
2. **STEP CHECK.** Which game step is it? {compute OBT's prediction in a system | find the external
   misfit | propose ONE external patch | test the patch across variants | find the WHY | promote
   to card | re-test abandoned}. Maps to none → **STOP.**
3. **OBJECT CHECK.** What does it consume/produce? Legit outputs = {misfit, patch, monster, card,
   error}. If the output is "a verdict on OBT" → **STOP.**
4. **TERRAIN CHECK (3 ingredients).** Does this case have (a) an OBT prediction WITH an observable
   gap, (b) a patchable ADJACENT EXTERNAL theory, (c) VARIANTS to test the patch? Any missing →
   **not a game terrain, don't play here** (a "naked OBT prediction" like 613 Mpc — no external
   theory, no variants — is NOT playable; classify it and move on).

**Object taxonomy → legitimate actions:**
| Object | What it is | Legitimate action |
|---|---|---|
| **OBT prediction (naked)** | direct consequence of OBT | USE as fixed target; NEVER test it; not a card, not a monster |
| **External theory (adjacent)** | the thing we may patch | identify it; propose ONE param change |
| **Patch** | one modified external param making OBT+patch fit a case | test across variants |
| **Monster** | a patch fitting a BATCH but whose WHY is not yet found | keep in reserve; re-test each round |
| **Card** | a monster whose mechanistic WHY is found + certain | add to the game |
| **Error** | a patch refuted | discard |

## 1. The method (Romain's game), faithfully

**Invariant: always presuppose OBT works.** We never hunt "where OBT is false" to kill it.
We hunt where it *appears to fail* within a configuration type — WITH all its variants around it.

**The loop to win ONE card:**
1. Take a **configuration type** + all its variants.
2. On a case that doesn't fit, **modify ONE parameter of an adjacent (external) theory**
   so that **OBT + that parameter** makes it work — *even if we don't yet understand why*.
3. **Apply that trial parameter to ALL the variants.**
4. **If a batch fits** → find the **variant that illuminates WHY** the parameter resolves
   the problem. That "why" = the **debunk** of a flawed external theory.
5. That debunk becomes a **card**. The game is now **OBT + {cards}**.

**The recursion:**
6. Find a **new series of variants** where we apply the *current game* (OBT + cards).
7. Where it breaks → **a new parameter on another element** → make a **trio** work.
8. If it fits on many → presuppose it's probably true → find the case that **explains**
   the 2nd parameter → new debunk → new card.
9. …and so on. End state: every flawed element around OBT is debunked. **The proof is that
   it works EVERYWHERE with no incomprehensible parameter left.** A new error appears later
   → run the loop again → new card.

**The release valve:** if after X iterations the "why" of a parameter isn't found →
**temporarily abandon it**, try another parameter on another element, find another card.

## 2. "The magic" (the load-bearing insight — disentanglement auto-acceleration)
> More cards make the missing ones EASIER to find. Even abandoned cases resurface on
> their own.

Mechanism (why this is plausible, not just optimism): anomalies are **superpositions of
several external errors**. A case abandoned because it had TWO entangled defects (params A
and B mixed) was insoluble alone. Once card A is won elsewhere, that case has only ONE
residual defect (B) → it becomes soluble → **it resurfaces by itself**. Each card peels one
layer of noise from ALL future residuals → difficulty DECREASES with card count.
**The engine self-accelerates and CONVERGES** (opposite of Ptolemaic epicycles, which
accumulate without ever simplifying).

**Verifiable success criterion:** the resolution rate of previously-abandoned cases must
RISE as the card count grows. If it doesn't, the method (or our application) is wrong.

## 3. NON-NEGOTIABLE invariants (the guardrails that make this science, not curve-fitting)
1. **Presuppose OBT.** Never tune OBT itself (never glue OBT). Cards correct EXTERNAL theories only.
2. **Predict BEFORE you sieve.** The sieve never asks "what's weird?"; it always tests a
   PRE-REGISTERED OBT(+cards) prediction on the sample, with look-elsewhere / trials-corrected
   significance. Automated free-dredging = an industrial false-discovery machine. Forbidden.
3. **The "why" barrier (the card-acceptance gate).** A new parameter is accepted as a card
   ONLY if a large sample reveals an INDEPENDENT MECHANISTIC justification (the "why it's
   simpler this way" that debunks the external theory) — NOT merely because it makes numbers
   fit. A parameter that only reduces the residual = an epicycle → rejected.
4. **A failed leg never contaminates the others** (independent evidence stays independent).
5. **Suspect yourself first.** On an apparent failure, separate: (a) I misapplied OBT (MY
   error — debug me); (b) defect in the external theory (= the card, the prize); (c) can't
   tell → note & return. The perturbing element is ALWAYS external (we presuppose OBT true),
   but "I misapplied OBT" is a real, frequent, separate category — check it first.
6. **Re-test abandoned cases after every new card** (that's where "the magic" is measured).
7. A contestation is a suspicion, not a proof; one contested study cannot decide.
8. **A card REQUIRES CERTAINTY.** Never promote a shaky result to a card. Cards are the
   foundation later cards build on — a bancale card poisons the whole tree (subsequent
   parameters would lean on something erroneous → cascade of FALSE cards). If a result is
   uncertain: extend the test to OTHER lots/volumes until another element sharpens the
   understanding. If still not certain but it "smells good" → file it in the **Monster
   Registry (§9)**, do NOT card it. Certainty for the spatial/large-scale legs means
   REPLICATION across INDEPENDENT volumes (cosmic variance is irreducible in one survey).
9. **Big compute is reserved for proving a debunk (monster → card).** Costly calculations /
   downloads are NOT for exploration, and NEVER for testing an OBT prediction. They are spent
   ONLY to demonstrate, on a large sample, that a candidate **monster's external-patch mechanism
   actually works** → to promote it to a **card**. Stage-1 pre-sieve is light & fast; heavy compute
   is the FINAL weapon, monster→card only. *(This is exactly why the DESI ξ(r) plan was wrong:
   heavy compute spent to TEST an OBT prediction, not to PROVE a debunk → forbidden.)*
10. **YOU (Claude) are the PLAYER — this game is NOT fully automatable.** The candidate→monster
    step is a SUBJECTIVE JUDGEMENT: given the patch's NATURE + the systems where it works, decide
    whether the indices justify calling it a monster. The ≥2-systems rule is a FLOOR against
    coincidence, NOT the decision. It is subjective BY DESIGN: **if you were SURE, it would already
    be a CARD, not a monster** — it's a monster precisely because you are not yet sure. Romain
    counts on your pertinence here, not on a mechanical threshold. (Recorded in the tool banner so it
    stays in context.)

## 4. Architecture to build (4 stages + the loop)

```
STAGE 1  PRE-SIEVE (replaces Claude's web searches, ~1000x faster)
  - Query a catalog DB (Gaia 1.8B stars; SDSS; DESI; eROSITA) with broad criteria +
    SCALABLE parameters (thresholds we vary). Millions -> thousands of candidates.
  - DETERMINISTIC. Tools: astroquery / ADQL-SQL (Gaia archive, SkyServer/CasJobs), TOPCAT.
  - MUST be driven by a pre-registered OBT(+cards) prediction (invariant #2).

STAGE 2  AUTO-COMPUTE (the scalable arithmetic)
  - Apply FIXED OBT(+cards) formulas to each candidate: a0(z)=cH(z)/2pi, mu(x)=x/sqrt(1+x^2),
    sinc(pi*t_dyn/T), lambda=cT, etc. Output a per-object "deviation-from-prediction" score.
  - Pure numerics, embarrassingly parallel, zero judgement.

STAGE 3  AGENT TRIAGE (the scalable judgement) — Claude pilots here
  - Candidates the computation can't settle are batched to PARALLEL agents (Agent tool /
    Workflow / multiple Claude Code, each with sub-agents). Each agent: hunt the external
    perturbing element, check systematics, read the literature on its sub-lot, propose/test
    the trial parameter, look for the "why" variant.
  - Agent missions get prompts from Section 7 (the playbook), adapted per mission.

STAGE 4  SYNTHESIS (Claude + Romain)
  - Consolidate structured verdicts; apply the discipline (invariants); promote a parameter
    to a CARD only if the "why" barrier (#3) is met. Romain holds direction; Claude holds rigor.

THE LOOP
  game := OBT
  repeat:
     pick configuration type + variants
     STAGE1 -> STAGE2 -> STAGE3 -> STAGE4 against `game`
     if a trial parameter fits a BATCH and a variant reveals its WHY:
         game := game + new_card           # debunk earned
     re-run all ABANDONED cases against the new `game`   # measure "the magic"
     residuals -> next parameter on another element
  until: works everywhere, no unexplained parameter left
```

## 5. State object: the "game"  + where objects live + the card flow
`game.game = {candidates, monsters, cards, errors, terrains}` (buckets, in game.json).
Each object (bestiary OBJ_SCHEMA) =
`{id, name, external_theory, patch, systems_validated:[...], why_status, why, certainty,
 status: candidate|monster|card|error|abandoned, created, updated, history:[...]}`.
Lifecycle: **candidate** (1 system) →[≥2 systems]→ **monster** (in bestiary, WHY unknown)
→[WHY understood + certainty≥high]→ **card** (correction of an external theory, added to OBT).
The model under test at any moment is OBT applied jointly with all confirmed cards.

**The GAME is a TOOL, distinct from `explorations/`.** `explorations/` is V9.0 R&D (seeds,
bulk_solver, this spec, the bootstrap journal). The game (the app + its `game.json` state of
monsters/cards/errors) is the *process* that runs on top — not the same thing as the folder.

**Card flow (the destination of a confirmed card is the THEORY, not exploration):**
misfit → patch → **monster** (in reserve) → **CARD** (mechanistic why found + certain). A confirmed
card is a *proven external-theory correction with a logic* → by construction it is **destined for
INTEGRATION INTO THE THEORY** (the 7 sacred files + site), because that is what a card IS: a debunk
that works, integrable into OBT. `explorations/` may hold a card IN TRANSIT, but its destination is
the theory. **Today: ZERO confirmed cards → nothing migrates to the theory/site yet.**

## 6. Catalogs / terrains (richest first, for the stellar legs)
- **Gaia (~1.8B)**: position, parallax(distance), proper motion, RV → wide binaries (a0/mu(x)),
  Methuselah ages, flyby/kinematics. Access: astroquery.gaia, ADQL.
- **SDSS**: magnitudes, colors, spectra, stellar mass, SFR, velocity dispersion, morphology.
- **DESI DR1**: LRG/ELG/QSO/BGS clustering + randoms (the xi(r)/613 Mpc terrain).
- **eROSITA**: clusters, X-ray (the cluster/sinc terrain — handle with the eROSITA caveats).
- **BOSS DR12**: prototype done here (`xi_613_analysis/`) = live proof of Stage 1+2.

## 7. Agent playbook (ENRICH PROGRESSIVELY — prompts that work go here)
> Claude fills this in as it pilots: the exact prompts that produced good agent results,
> per mission type. This is the operational payoff of the file.

- **Mission: perturbing-element hunt** (draft) — "Presuppose OBT is correct. Here is a case
  + variants where OBT(+cards) appears to fail: {data}. The defect is in an EXTERNAL theory,
  never in OBT — but FIRST check whether the apparent failure is a misapplication of OBT
  (category a) and report that if so. Otherwise, propose ONE external parameter that makes
  OBT(+cards) fit, state its mechanistic rationale in the external theory's own logic, and
  say on which listed variants it would also hold. Return structured: {is_misapplication,
  proposed_param, external_theory, mechanistic_why_or_NONE, variants_predicted_to_fit}."
- **Mission: the-why hunt** (draft) — "Given trial parameter {P} that fits this BATCH
  {sample}, find the single variant that most clearly reveals WHY P works — i.e. an
  independent mechanistic reason the external theory was wrong. Reject if P only fits
  numerically (epicycle). Return {why_found:bool, revealing_variant, debunk_statement}."
- **Mission: card-stress-test** (draft) — "Re-test these ABANDONED cases {list} against the
  current game OBT+{cards}. Report which now resolve with no free parameter (the magic)."
- (more to come as we learn what phrasing yields clean StructuredOutput)

## 8. Build order
1. ~~613 test~~ DONE — it was AUDIT (testing an OBT prediction), reclassified §9-bis. Not the game.
2. **Build the GATE-ENFORCING STATE MACHINE first** (§9-ter): a thin orchestrator that walks the
   game states, prints each step's rule, runs THE GATE (§0.5) before every action, and holds the
   persistent `game` state. This is the structural fix for derailing — build it BEFORE more terrains.
3. Wire Stage 1 (DB pre-sieve, start with **Gaia** wide binaries) + Stage 2 (auto-compute) into the
   state machine, driven by a PRE-REGISTERED prediction (invariant #2).
4. Wire Stage 3 (Agent/Workflow triage) + Stage 4 synthesis; promote a patch to a card only via the
   "why" barrier (#3) + certainty (#8). Run the loop; win card #1; measure "the magic".

## 9. Monster Registry (uncertain PATCHES of EXTERNAL theories — NOT cards, NOT errors yet)
> A monster = a PATCH of an adjacent EXTERNAL theory **validated on ≥2 systems** (so it isn't a
> coincidence) but whose mechanistic WHY is not yet found (a candidate card in reserve). A patch on
> only ONE system is a **candidate**, not yet a monster. NEVER a naked OBT prediction. Re-examine
> every round (a future card may reveal a monster as error, or as a card-in-disguise).
>
> (Historical note kept — Romain caught the 613 Mpc mislabel 2026-05-31: it is a NAKED OBT
> prediction, §9-bis, not a monster, because NO external theory was patched.)

- **MONSTER [62b7f086] `arc-core-hydro-bias` (2026-07-11, Romain: "logue le monstre").** EXTERNAL
  THEORY: the X-ray hydrostatic-equilibrium mass pipeline in cluster CORES (X-COP/Ettori class —
  the very calibration behind card-#22's global Weyl f_W=0.70, β=0.043); it assumes purely thermal
  pressure. PATCH (one parameter): the core non-thermal/AGN pressure fraction — hydrostatic masses
  under-weigh cores, so the Weyl profile our card inherited is under-concentrated there; bias-free
  strong LENSING reveals the true Weyl core. COMPUTED SIGNATURE (probes `abell370_obt.py`,
  `arcs_obt.py`): κ_OBT(R_arc) SATURATES at ~0.63–0.65 on BOTH systems while every giant arc
  demands 1.0 — OBT-proper deficit ×1.15 (A370 merger, WL-ref) → ×1.56 (MS2137 RELAXED at the
  Donnarumma-reconciled c200=9.6): it GROWS on clean terrain. 2-SYSTEM FLOOR MET (A370 arc
  z_s=0.725; MS2137 arc z_s=1.501); WHY PENDING (quantitative α_NT budget; TENSION: Hitomi low
  core turbulence ~4%; SUPPORT: the 1990s SL-vs-X-ray factor-2 core literature — Miralda-Escudé &
  Babul 1995, Allen 1998). ALTERNATIVE reading to re-examine each round (would move it to
  §9-bis-adjacent): the Weyl closure-IC core is intrinsically concentrated (Gates 17/23
  rising-inward) — OBT-internal, no external patch. NEXT: the N-arcs battery (CLASH relaxed set)
  = the sanctioned monster→card big-compute (κ-saturation universality + α_NT budget).
  **⚡ N-ARCS BATTERY RUN (2026-07-29, `arcs_battery.py`, 9 CLASH relaxed lenses, Umetsu+16 T1
  anchors θ_E + M2D(<10–40″) verified 0.99–1.11 vs πΣ_cr R_E²): CONSOLIDATED + RELOCATED.**
  Two-arm design (pass-1 relire caught that a lensing-anchored Weyl is normalization-tautological):
  **(1) MONSTER arm** (Weyl on external M-T hydrostatic-class M500): κ_OBT(θ_E) = **0.70 median,
  σ=0.06, range 0.64–0.84** → with A370 0.65 + MS2137 0.63 = **11/11 lenses in 0.63–0.84,
  saturation UNIVERSAL**. **(2) FORM arm** (Weyl on the 40″-lensing-calibrated M500, c=3.79
  ensemble): OBT-proper deficit vs NFW **×0.92–0.97 (0/9 above ×1.25)** → the card-#22 PROFILE
  SHAPE IS VINDICATED by 9 lensing cores (mild core dip 10″ 0.87 → 40″ 1.05; fixed BCG 5e11
  crude). **(3) THE MONSTER LIVES IN THE MASS ANCHOR, not the profile: M5(M-T)/M5(lensing-40″) =
  0.59 median (0.40–0.72) = numerically the Planck-SZ-demanded hydrostatic mass bias (1−b)~0.6**
  (vs ~0.8 in sims) → the monster JOINS a known, LIVE external tension. Caveats declared: c-M
  degeneracy on the 40″→M500 extrapolation; un-excised cool-core kT bias carries part of the two
  extreme ratios (MACS0429 0.40, MACS1931 0.46); M-T norm ±25% doesn't erase it (×0.74 at the
  edge). CARD PATH (Romain's call): (a) the α_NT/mass-bias budget note (WtG Applegate+14
  lensing/X-ray ~1.3–1.7 corroborates); (b) re-fit card #22's (f_W, β) on LENSING masses instead
  of X-COP hydrostatic (predicted: same shape, ~×1.7 amplitude — would also retune the f_Weyl
  plateau of Gates 21–23).

## 9-bis. Naked OBT predictions (classified, NOT playable, NOT tested in the game)
> Direct consequences of OBT. By the AXIOM CHECK they are TRUE within the game and are NEVER tested
> here (testing them = audit = hors-jeu). They have no adjacent external theory to patch and no
> variants → not game terrain. Listed only so I don't mistake them for monsters again.
- **λ = c·T = 613 Mpc cymatic fundamental.** KBC void / Big Ring / Giant Arc / BAO all consistent
  with this one scale when OBT is applied correctly (slip low-pass → dominant fundamental, no comb).
  An exploratory ξ(r) on BOSS CMASS (`xi_613_analysis/`) validated the pipeline (BAO injection ✅)
  and showed no clean 413 Mpc/h peak — but that exercise was AUDIT (testing OBT), and inconclusive
  anyway (cosmic-variance floor ~11% in one volume). **Do NOT pursue in the game.** If ever
  revisited it is OUTSIDE the game, as an OBT prediction awaiting independent confirmation.
- a₀ = cH(z)/2π (instantaneous); SKA 21cm modulation; Penrose-Diósi 5D collapse — same status.

## 9-ter. The app ENFORCES the gate at every step (Romain's fix for my derailing, 2026-05-31)
> Discipline is faillible (I keep snapping into audit-mode). The remedy is to EXTERNALIZE the
> guardrail INTO the software: the engine is a STATE MACHINE whose states are the game steps, and
> at every step it (1) shows me the current step + its rule, (2) forces me through THE GATE (§0.5)
> before I produce anything, (3) refuses/flags any action that fails the AXIOM check, (4) records
> the produced object into the persistent `game` state with its correct type. I cannot derail
> because the tool won't let an audit-action through. The app thus reminds me of the rules WHILE I
> use it — the rules live in the harness, not only in my (faillible) memory.
> States (3-level lifecycle, §0; exact names as in obt_game.py STATES): PICK_TERRAIN(gate#4) →
> COMPUTE_OBT_PREDICTION → FIND_MISFIT → PROPOSE_PATCH_CANDIDATE (→ candidate, 1 system) →
> VALIDATE_ON_SYSTEMS (add-system) → CONFIRM_MONSTER (≥2 systems floor + player judgement, else
> stays candidate / kill) → FIND_WHY (ideally a SIMPLE system) → RESOLVE {promote card | abandon |
> kill} → RETEST_ABANDONED → loop. Each transition prints the next state's rule and runs the gate.
>
> **Mode is carried by the TOOL, not a static memory flag** (Romain, 2026-05-31 — a static flag desyncs
> on switching). Two REQUIRED tool behaviours: (1) EVERY output prints a persistent header
> `=== MODE CHERCHEUR ===` so the live context always shows the active mode, AND reminds *"if
> chercheur-memory.md not yet read this session → read it now"* (closes the loop). (2) When a card is
> ready, the tool prints `SORTIE DU MODE CHERCHEUR → repasse reviewer/webmaster pour intégrer à la
> théorie`. Default (no tool running) = reviewer/webmaster.

## 10. Pointers
- Mode firewall: `feedback_two_modes` · chercheur-mode memory: `chercheur-memory`.
- Method memory: `feedback_bootstrap_search_strategy` + `project_bootstrap_consilience_audit`.
- Verified-sure findings log: `explorations/bootstrap_journal.md` (V1..V13 cards/leads).
- This file (`explorations/chercheur-game.md`) is the OBT-Game master spec, referenced from MEMORY.md.

*Last updated: 2026-05-30.*
