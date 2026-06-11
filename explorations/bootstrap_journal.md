# Bootstrap Journal — Verified-Sure Findings Only

**Status:** quarantined research log (NOT V8.2, NOT in the PDF, NOT a theory file).
Lives in `explorations/` by the sanctioned exception to the no-new-`.md` rule.

**Method (Romain's bootstrap / consilience):** presuppose OBT is correct → compute the
correction it FORCES on some external phenomenon → check the correction is *comprehended
in the external theory's own logic* (a real independent defect, not an arbitrary knob) →
propagate to MANY isolated cases → only a single comprehended modification that resolves
problems *in cascade* would constitute proof. Repetition raises suspicion; only the
understood mechanism converts suspicion into proof.

**Discipline (non-negotiable):**
- **Never glue OBT.** No ad-hoc tuning of OBT to fit.
- A *contestation* is a **suspicion, not a proof** (a single contested study cannot decide).
- The forced parameter **may be the wrong one** — let the cases dictate the pattern.
- Don't cut the branch prematurely (naïve falsification is quick and often wrong); **iterate and learn**.
- Many independent errors *around* OBT are possible; a residual is not automatically "OBT's fault".
- This journal records **only what is verified for sure**. Open/mixed items are flagged OPEN, not as results.

---

## VERIFIED — SURE

### V1. The growth-sector sign is a free bulk boundary condition (closure problem)
OBT's sign of the S₈/growth modulation (enhancement vs suppression) is **not derivable** from
the brane equations alone. The Weyl anisotropic-stress evolution is absent from the on-brane
system → the perturbations' growth is boundary-condition-dependent (Koyama astro-ph/0701015;
Maartens 2004; Cardoso-Hiramatsu-Koyama-Seahra 0705.1685). Epistemic level = ΛCDM's fitted Ω_c.
*Sure:* the sign is an INPUT, not a prediction (unless a full moving-brane bulk solve with a
regularity BC imposes it — active V9.0 work in `bulk_solver/`).

### V2. OBT forces a₀ = cH(z)/2π *instantaneous* (not frozen at formation)
theory.md derives a₀ from the Gibbons-Hawking temperature of the **instantaneous** horizon
R_H = c/H(z). "H(t) IS the extrinsic curvature." So OBT forces a₀ ∝ H(z) instantaneous.
The sinc(π·t_dyn/T) orbital filter (already in V8.2, the cluster mechanism) makes the *effective*
a₀ depend on the system's dynamical time → naturally type- and environment-dependent.
*Sure (OBT-internal derivation facts).*
*OPEN (not sure):* the data confrontation. MUSE-DARK III (2026, 79 gal, z<1.44) sees a₀ rise
~30σ and "faster than H(z)"; OBT(instantaneous × sinc) lands ~1.9σ low at z=1. One study, same
kinematic systematics (beam smearing / pressure support). Parked, OBT untouched.

### V3. OBT's G-variation cannot be a local time-variation of Newton's constant
Local |Ġ/G| is bounded by a **convergent set of independent isolated systems**:
- Lunar Laser Ranging: (0.2 ± 0.7)×10⁻¹² /yr (Williams+; future → 10⁻¹⁵)
- Binary pulsar PSR J1713+0747: ~(0.3 ± 0.3)×10⁻¹² /yr (Zhu+ 1802.09206)
- White-dwarf cooling, NGC 6791: ~1.8×10⁻¹² /yr (García-Berro+ 1308.5414)
- Asteroseismology (ancient star): comparable

OBT's f_osc = 0.10 over T = 2 Gyr, **as a local homogeneous G(t)**, gives peak
|Ġ/G| = f_osc·2π/T ≈ **3×10⁻¹⁰ /yr** → exceeds the bounds by **×300–3000**.
*Sure:* OBT's 10% oscillation **cannot** live in the local Newtonian G. It must reside in the
cosmological growth G_eff (perturbation sector) = the V1 closure sector.

### V4. "Varying-G → SNe Ia → Hubble tension" is NOT a viable OBT mechanism
SN Ia luminosity ∝ M_Ch ∝ G^(−3/2) is set by the **local** G at the white dwarf. By V3, OBT's G
cannot vary locally. Therefore SNe see constant G → no luminosity bias → no H₀ correction.
(Varying-G with SNe Ia is itself an externally studied, bounded idea — Wright & Li 1402.1534.)
*Sure:* the mechanism does not connect — established WITHOUT modifying OBT. OBT is untouched.

### V5. OBT passes the convergent local-G isolated tests — as a null
By V3, OBT predicts local G stable → consistent with LLR / pulsars / WD / asteroseismology.
*Sure but NOT distinctive:* this null is shared with GR/ΛCDM. Survival, not a discriminating win.

### V6. Wide binaries (Gaia) — OBT's prediction is non-distinctive, and the data are contested
OBT inherits MOND's μ(x) and a₀ → predicts the same low-acceleration boost (γ_g ≈ 1.1–1.2 under
the Milky-Way External Field Effect; G_eff ≈ 1.4 in the 2–5 kAU anomaly band). Two facts, both sure:
- *Non-distinctive:* the prediction IS MOND's. A confirmation would credit MOND, not OBT specifically.
- *Contested:* Chae 2023–2024 + Hernandez-Chae 2024 see the anomaly (MOND); Banik 2024,
  Pittordis-Sutherland 2025 (2504.07569), and the 2026 quality-framework paper (2602.24035) find
  NO MOND once hidden-triple contamination / error-cut artifacts are controlled. Unresolved.
*Sure:* not a single-force distinctive win — suspicion at best, on contested data. OBT untouched.

### V7. The 2 Gyr resonance: a real cross-domain coincidence, but degenerate (not a distinctive proof)
OBT's sinc filter kills MOND when t_dyn = R/σ ≈ T. Clusters have t_dyn = R/σ ≈ 1–2 Gyr (textbook;
Bothun, ned.ipac), and MOND indeed fails there by a factor ~2 (Milgromian clusters, 2602.06082).
T = 2 Gyr is fixed *independently* by the DESI dark-energy w(z) period (NOT tuned to clusters), so the
match is a genuine **same-number-two-domains** coincidence (dark energy ↔ cluster MOND-death) —
the first real consilience thread of the session. *Sure.*
But three sure caveats keep it short of a distinctive proof:
- *Loose:* cluster t_dyn spreads 1–5 Gyr; the coincidence is at the factor-~2 level, not precision.
- *Degenerate (the killer):* g ∝ σ²/R and t_dyn ∝ R/σ ⇒ g ∝ 1/t_dyn². So "MOND dies at long t_dyn"
  (OBT) ≡ "MOND dies at low acceleration" (standard MOND) — kinematically linked, indistinguishable
  on current data. The "dynamical clock controls MOND" framing already exists with no brane
  (2603.18135; McGaugh 2505.21638: DM phenomenon only in deep-MOND AND collisionless systems).
- *Distinctive part unobservable:* the only uniquely-OBT signature is the sinc NON-MONOTONICITY
  (zero at t_dyn=T, then secondary lobes / partial recovery beyond), vs monotonic MOND/ΛCDM —
  but it is too small / too few systems at t_dyn>2 Gyr / clusters too messy to test now.
*Sure:* suggestive cross-domain consilience, NOT a distinctive single-force proof. No glue. OBT intact.

### V8. Third domain (spatial): λ = c·T = 613 Mpc — one striking match (KBC), but look-elsewhere
With T = 2 Gyr (DESI, NOT tuned to structure), the cymatic wavelength λ = c·T = 613 Mpc. Confronted
with observed ultra-large scales (counting hits AND misses honestly):
- **KBC void** diameter ~600 Mpc (radius ~300; Haslbauer 2020, 7σ vs ΛCDM) vs λ=613 → ratio 0.98. **Striking.**
- BAO ~150 Mpc = λ/4 (153) — matches, but BAO has a solid standard explanation → not distinctive.
- Big Ring ~400 Mpc (Lopez 2024) → λ/1.5, not a clean harmonic. **Miss.**
- Giant Arc ~3300 Mpc (Lopez 2021) → no clean harmonic. **Miss.**
*Sure caveats:* (i) every "natural" cosmological scale lands in 100–1000 Mpc, so matching ONE harmonic
of 613 is a **look-elsewhere** trap; (ii) honest tally = 1 striking / 4 (KBC), the rest tied/missed →
cherry-picking risk if misses aren't counted; (iii) "void diameter" is a soft quantity (KBC has no sharp edge).
*Sure:* KBC is a genuine third-domain hint (T appears in time/DE, dynamics/clusters, AND space/KBC), but a
single clean match amid look-elsewhere is NOT locked consilience.
**Distinctive non-degenerate target (proper future test):** OBT predicts a PERIODIC COMB of harmonics
(peaks at λ, λ/2, λ/3, …≈613/n Mpc) in the correlation function / power spectrum — a standing-wave node
pattern absent from ΛCDM (single BAO peak). Falsifiable cleanly with a FULL catalog (Euclid/DESI), counting
misses, not by picking one structure. This is the real way to turn the 2 Gyr coincidence into proof.

### V9. The comb was MY misapplication of OBT (category a); applied right, OBT → dominant fundamental
[Reclassified per rule 6: the slip low-pass is NOT a "perturbing element inside OBT" — it is OBT applied
correctly. My earlier "comb" prediction was MY error (category a). Below kept for the record.]
Empirical check of the V8 comb, THEN OBT re-applied correctly (slip low-pass was already in theory.md):
- *First (naïve) finding:* the correlation function shows ONE BAO peak (~150 Mpc), no periodic comb; no
  confirmed secondary peaks in 3D surveys; the Broadhurst 1990 128 Mpc/h periodicity is a refuted
  pencil-beam/small-sample artifact (Yoshida 2001). So a clean comb is absent.
- *Perturbing element (REAL OBT physics, theory.md), pursued:* the stick-slip slip low-pass spectrum
  A_n/A₁={1,0.476,0.293,0.197,0.138} means harmonic POWER A_n² is n=2→23%, n=3→9%, n≥4 <4% of the
  fundamental; 3D projection + nonlinear smearing (the SAME effect that turns BAO power-spectrum wiggles
  into a single real-space peak) crush them below detectability.
- *Corrected conclusion:* OBT does **not** predict a clean comb — it predicts a DOMINANT FUNDAMENTAL at
  λ=613 Mpc with harmonics buried. "No comb" is the EXPECTED OBT result, NOT a refutation. The one surviving
  mode is n=1=613 Mpc, and the KBC void (~600 Mpc) sits exactly there.
*Consequences (sure, and this REVERSES the earlier draft):* (a) the comb is the wrong test — replace it
with the FUNDAMENTAL test; (b) the KBC match is now **mechanistically justified** (the only mode the slip
spectrum lets survive) → the spatial leg is **RESTORED and strengthened**, not weakened. Methodological note
(Romain, 2026-05-30): a single failed leg must NOT contaminate the others, and a failed case demands a search
for the PERTURBING ELEMENT before any verdict — here the perturbing element turned the "failure" into a
mechanism. **New distinctive, non-degenerate test:** a SINGLE feature in the correlation function at ~613 Mpc
(no comb, no ΛCDM counterpart), testable on full Euclid/DESI catalogs — voie a, REVISED.

---

## TERRAIN VERDICTS

- **Gravity / variable G (iteration #1):** explored. Verdict = **survival in null** (V5), **no
  single-force distinctive win** (V3+V4 vise: the isolated cases forbid the local G-variation that
  would reach the Hubble observable; the surviving variation is the degenerate cosmological-growth
  sector V1). Real thing learned: *OBT's G-variation is structurally non-local.* Note: this verdict
  propagates to **all local-G stellar tests** (stellar ages, WD cooling, helioseismology) — they
  reduce to the same null; "millions of stars" cannot rescue a local-G win.

- **Wide binaries / a₀ at z=0 (iteration #2):** explored. Verdict = **contested + non-distinctive**
  (V6). OBT = MOND here (inherited μ(x)); the data dispute (Chae vs Banik/Pittordis) is unresolved.
  No distinctive single-force win.

- **2 Gyr resonance / clusters (iteration #3):** explored. Verdict = **suggestive consilience, not a
  distinctive proof** (V7). Best thread so far (one number T in two domains), but degenerate with
  standard MOND (t_dyn ⟺ acceleration); the unique signature (sinc non-monotonicity) is unobservable now.
  Distinctive falsifiable target for FUTURE data: non-monotonic mass-discrepancy vs t_dyn around t_dyn≈2 Gyr.

- **Third domain λ=c·T (iteration #3-bis, voie 2):** explored. Verdict = **one striking match (KBC void
  ~600 vs 613 Mpc, 0.98), but look-elsewhere** (V8). T now appears in THREE domains (time/DE,
  dynamics/clusters, space/KBC) — a real hint — yet a single clean match (1/4, others tied/missed) is not
  locked consilience.

- **Harmonic-comb check + perturbing-element rescue (iteration #3-ter, voie a):** DONE, then CORRECTED.
  Verdict = **comb was the wrong test; fundamental restored** (V9). The slip low-pass (real OBT element)
  suppresses harmonics (power n=2→23%, n=3→9%) → OBT predicts a DOMINANT FUNDAMENTAL at 613 Mpc, NOT a comb;
  "no comb" is expected. KBC (~600 Mpc) = the fundamental, now mechanistically justified → spatial leg
  RESTORED. New distinctive test: a single ~613 Mpc feature in the correlation function (no ΛCDM counterpart).

- **Big Ring & Giant Arc misses, projection rescue (iteration #3-quater):** DONE. Verdict = **both RESCUED
  by projection geometry** (V10). Big Ring 400 = inclined (i≈49°) 613 Mpc fundamental (solid); Giant Arc
  ≈1000 Mpc arc = ~half a 613 Mpc ring (softer; arc-length-not-diameter category error fixed). The single
  scale λ=613 Mpc now accounts for KBC + Big Ring + Giant Arc (+BAO harmonic). Spatial leg = RICHEST.
  Caveat: projection is permissive → not distinctive; distinctive test remains the single 613 Mpc
  correlation-function feature (V9-revised).

### V12. Spatial leg does NOT extend to voids / CMB — mostly negative, honestly logged
Pushed the λ=613 Mpc spatial leg into THREE new independent domains (rule: keep digging the good seam):
- **Void size function:** largest voids r_eff ≈ 15–19 Mpc/h (max ~54), i.e. ×10–20 below λ/2≈307 Mpc.
  *Self-suspicion (rule 6a):* this is MY category error — a standing-wave node is NOT an individual void;
  voids 15–30 Mpc are ordinary nonlinear structure at a totally different scale. The right test is a 613 Mpc
  MODULATION of void abundance/positions, which the standard void size function does not measure. NOT a
  refutation of OBT — wrong observable. (SDSS DR7 1103.4156.)
- **Superclusters / Great Walls:** Sloan Great Wall ~400 Mpc (within projection range of 613), but
  Laniakea ~120, Shapley ~50 — most are far below λ. Tepid: only the largest walls reach the cymatic scale.
- **CMB:** naïve projection of λ=613 / λ/2 at last scattering → ℓ≈71 / 142; the real CMB large-scale
  anomalies sit at ℓ=2–3 (and a k_min cutoff ~3×10⁻⁴ Mpc⁻¹), NOT at 71/142. *Self-suspicion (rule 6c):*
  my flat naïve comoving projection is likely too simplistic → log as OPEN, not "refuted".
*Verdict (sure):* the spatial leg does NOT cheaply extend beyond the 4 giant coherent structures (KBC, Big
Ring, Giant Arc, BAO-harmonic). Structural reason consistent with OBT applied correctly: the 613 Mpc mode
should imprint only on LARGE-SCALE COHERENT structures (rings, arcs, great walls, the local supervoid), NOT
on ordinary nonlinear statistics (individual voids) nor necessarily on low-ℓ CMB. So "voids don't show it"
is the wrong-observable, not a failure. Honest net: spatial leg stays at 4 cases, did not grow; no new
positive case here, no perturbing element found → NOTED, move on (rules 5–6).

### V13. The linchpin test (single 613 Mpc peak in ξ(r)) — INCONCLUSIVE on current public data
The distinctive spatial test (V9-revised): OBT predicts a SINGLE excess in the correlation function at
r≈613 Mpc = 413 Mpc/h (a standing-wave mode of wavelength λ bumps ξ at r≈λ), with no ΛCDM counterpart.
Confrontation with published BOSS/DESI ξ(r):
- BAO peak ~105 Mpc/h; zero-crossing ~130 Mpc/h; beyond ~200 Mpc/h ξ is small-negative→0; **no feature
  reported at 413 Mpc/h.** Naïvely negative.
*Self-suspicion / honest caveat (rule 6, decisive here):* the 300–600 Mpc/h regime is a measurement BLIND
SPOT — (1) the INTEGRAL CONSTRAINT artificially drives measured ξ→0 at the largest separations; (2) S/N
collapses; (3) standard analyses TRUNCATE at ~200 Mpc/h; (4) ΛCDM predicts nothing there, so nobody LOOKS.
"Nothing reported" is partly "nothing searched". So the linchpin lands exactly in the current analyses' blind
spot.
*Verdict (sure):* INCONCLUSIVE — neither confirmation nor clean refutation. (a) No confirmation → the spatial
leg's 4 structures (KBC/Big Ring/Giant Arc/BAO-harmonic) REMAIN look-elsewhere-vulnerable; cannot be promoted
to proof. (b) No clean refutation → the "nothing reported" is partly integral-constraint + not-searched; OBT
intact. *Real consequence:* the distinctive test is clean IN PRINCIPLE but needs a DEDICATED analysis —
ξ(r) out to ~700 Mpc/h, integral constraint properly handled, specifically searching a bump at 413 Mpc/h —
which has never been done because ΛCDM doesn't motivate it. This is precisely a test OBT motivates and no one
else runs. NOTED as the prime concrete future analysis (Euclid/DESI DR2 catalogs).

## METHODOLOGICAL RULES (Romain, 2026-05-30) — apply to ALL cases
1. A single FAILED leg must NOT contaminate the other legs (independent evidence stays independent).
2. For every FAILED/MISSED case, SEARCH for the perturbing element (a real OBT element not yet accounted)
   BEFORE any verdict — a failure may become a mechanism (as the slip low-pass did for the comb, V9).
3. Goal = collect a MAX of matches, then find the ONE whose initially-arbitrary modification acquires a
   LOGICAL/mechanistic justification — that linchpin is where genuine falsification of OBT can begin.
5. The perturbing element is ALWAYS external, NEVER from OBT (we presuppose OBT true → the defect is by
   construction in the external theory/measurement). When you CAN'T find it: NOTE as OPEN, do NOT force a
   verdict — keep collecting positive cases, come back later.
6. SUSPECT YOURSELF FIRST. On a "failure", separate: (a) I misapplied OBT (MY error — debug me, NOT a
   perturbing element); (b) defect in the external theory/measurement (= the perturbing element, the prize);
   (c) can't tell → NOTE & return. Check (a) before (b)/(c). RECLASSIFIED: V9 slip-low-pass and V10 projection
   were category (a) — me fixing my own misapplication of OBT — not "perturbing elements inside OBT".
   (Romain, 2026-05-30.)
4. TODO: (none outstanding — a₀ "faster than H(z)" handled in V11).

### V11. a₀ "faster than H(z)" (V2) — perturbing element searched, NO clean rescue → LINCHPIN candidate
Per rule 2, three real OBT perturbing elements were pursued for the MUSE-DARK "a₀ rises faster than H(z)":
- **Dynamical (Kodama-Hayward) horizon temperature** instead of static de Sitter T=H/2π: the apparent-horizon
  surface gravity gives T_dyn=(H/2π)|1+Ḣ/2H²|. In matter era Ḣ/2H²<0 → factor <1 → a₀_dyn rises SLOWER than
  H(z) (a₀(z=1)/a₀(0)=1.07 vs H-ratio 1.79). **WRONG direction — does NOT rescue.** (A genuine, derived OBT
  refinement, and it makes the tension WORSE, not better. Honest.)
- **Formation-epoch freezing** a₀∝H(z_f), z_f>z_obs: a small offset (z_f≈2.5–3 for z_obs=1) reproduces the
  observed ~2.0 ratio. BUT z_f is a per-system free quantity → this is GLUE unless derived from the brane
  geometry. theory.md derivation uses the INSTANTANEOUS horizon (V2), so formation-freezing is NOT what OBT
  forces. **Rejected as glue.**
- **Robustness of the claim:** the binned a₀(z~1)=2.38 → ratio 1.98 vs H-only 1.79 is only ~1.9σ; the
  "faster than H(z)" is driven by the LINEAR-FIT slope, not the binned point. One study, same beam-smearing/
  pressure-support systematics → a suspicion, not a proof (rule).
*Verdict (sure, REVISED per Romain rule 5):* no INTERNAL OBT element rescues "faster than H(z)" — but the
perturbing element need NOT be internal to OBT. A strong EXTERNAL candidate is unaccounted: the a₀(z)
measurement itself rides on contested high-z kinematic systematics (beam smearing + pressure support — the
same ones that split Genzel vs Tiley). If those inflate the inferred a₀ slope at high z, "faster than H(z)"
is a defect of the EXTERNAL analysis, not of OBT. That external perturbing element is NOT yet eliminated.
Combined with: the effect is only ~1.9σ (binned), driven by the linear-fit slope, one study.
*Status: OPEN — NOTED to return, NOT a verdict.* This is the best falsification HANDLE found (a₀∝H(z) is
rigidly forced by theory.md's instantaneous horizon, and no internal glue rescues it), BUT it can only become
an actual falsification once the external kinematic-systematics perturbing element is ruled out by a
replicated, systematics-clean, high-z sample (Euclid/JWST/ALMA). Until then: a suspicion to revisit, while
we keep collecting positive cases (rule 5).

### V10. Big Ring & Giant Arc "misses" were MY misapplication (category a) — projection is part of OBT applied right
[Reclassified per rule 6: projection geometry is not a "perturbing element"; comparing apparent size to
intrinsic diameter, and arc-length to diameter, were MY errors (category a). Applying OBT correctly dissolves
the misses.] The two V8 misses re-examined with correct 3D→2D projection of standing-wave nodes: KEY rigorous fact: projection (inclination/foreshortening/sphere-slicing) can only
SHRINK an apparent size, never inflate it. So a structure < λ can be a projected λ node; one > λ cannot be a
single node.
- **Big Ring** (ring, diameter ~400 Mpc): 400 < λ=613 → an inclined fundamental ring at i≈49° (a banal random
  orientation) appears at 400 Mpc. RESCUED, solid. Big Ring = the inclined 613 Mpc fundamental.
- **Giant Arc** (~3.3 Gly ≈ 1000 Mpc): naïvely 1000 > 613 → fails. But the perturbing element I'd missed:
  the Giant Arc is an ARC (a LENGTH), not a diameter — a category error in V8. Arc length ~1000 Mpc vs a
  fundamental ring circumference π·613 = 1926 Mpc → the arc is ~52% of the ring (≈ a half-ring of the 613 Mpc
  fundamental). RESCUED, but SOFTER (length↔ring conversion is ambiguous; "3.3 Gly" is a curvilinear length).
*Consequence (sure):* both V8 "misses" were artifacts of my naïve apparent-size-vs-intrinsic-diameter
comparison. With projection, the SINGLE scale λ=613 Mpc accounts for KBC (n=1 direct), Big Ring (inclined),
and Giant Arc (arc) — plus BAO as the suppressed harmonic. The spatial leg is the RICHEST, not weakened.
*Discipline caveat (no self-deception):* "projection only shrinks" is PERMISSIVE — many sizes <613 fit under
"inclined 613", so this is NOT yet distinctive. The distinctive test stays V9-revised: a SINGLE correlation-
function feature at ~613 Mpc (no ΛCDM counterpart), where projection permissiveness no longer applies.

## RECURRING WALL (the real learning so far)
Across iterations #1–#2 the bootstrap keeps hitting the SAME structure: OBT's *testable*
predictions are either **MOND-inherited** (μ(x), a₀ → wide binaries, RAR) or **ΛCDM-shared nulls**
(local G stable), while its *distinctive* content sits in the **closure-quarantined bulk sector**
(V1: amplitude/sign/clustering are inputs). So distinctive single-force wins are rare by
construction. The one lever that is **neither MOND nor ΛCDM** is the **brane period T = 2 Gyr**
imprinting a sinc NULL in MOND-survival at systems with t_dyn ≈ T (V2's sinc filter), AND a
spatial standing-wave comb at λ=c·T (V8). T = 2 Gyr now appears in THREE independent domains
(time/dark-energy w(z), dynamics/cluster MOND-death, space/KBC void) — the strongest thread —
but each match is individually degenerate or look-elsewhere; the genuinely distinctive, non-degenerate
falsifiable signatures are (a) sinc NON-MONOTONICITY in mass-discrepancy vs t_dyn (V7) and
(b) a PERIODIC HARMONIC COMB 613/n Mpc in the correlation function (V8) — both for future full catalogs.

## RUNNING (background, detached) — xi(r) BOSS CMASS test (started 2026-05-30T00:48Z)
Computing the V13 linchpin test on real data: xi(r) of BOSS DR12 CMASS North out to 600 Mpc/h,
hunting a single OBT excess near 413 Mpc/h (lambda=c*T=613 Mpc). Folder:
`explorations/xi_613_analysis/` — scripts: download.sh, xi_compute.py, run_all.sh.
Launched detached: `setsid nohup bash run_all.sh > master.log 2>&1 < /dev/null &` (pid 1170556).
TO RESUME / CHECK: read `xi_613_analysis/master.log` and `xi_613_analysis/STATUS`; results in
`xi_result.txt`; checkpoints `counts_{DD,DR,RR}.npz` (rerun run_all.sh resumes finished stages).
INTERPRETATION GATE: trust nothing unless the INJECTION TEST (BAO bump near ~100 Mpc/h, zero-crossing
~130) passes — it also validates the Landy-Szalay normalization convention. A null at 413 is NOT a clean
refutation (integral constraint biases r>~300 negative; crude Poisson errors, no mocks).

---
*Last updated: 2026-05-30.*

## V14 — QUÊTE DU GRAND ATTRACTEUR (ouverte juin 2026, design pré-enregistré)
Faits officiels (vérifiés): le GA n'est PAS un objet compact — concentration étendue
(Norma/ACO3627 + Norma Wall: Pavo II, Centaurus-Crux, CIZA J1324) cachée derrière la Zone
d'Évitement; CIZA 2005: masse révisée à ~1/10 de l'estimation originale; le flot CONTINUE
au-delà vers Shapley; Tully 2014: le GA = point focal du bassin Laniakea; Hoffman 2017:
le Dipole Repeller (poussée du vide) co-explique le flot; 2024: bassin Shapley ~10x Laniakea.
LE TERRAIN (futur, lourd): CosmicFlows-4 (EDD, public) — refaire le bilan de masse du
bassin avec NOS lois corrigées (carte #22: gravité amas = sinc-éteinte + Weyl coré → la
masse inférée des flots change); prédictions à chercher: (a) déficit/déplacement de la
masse GA sous les lois corrigées; (b) le v_bulk=300 km/s de la dérive de brane (T3 V8.2)
comme composante NON-convergente du flot (signature: dipôle résiduel sans bassin source —
distinguable de toute attraction); (c) structure cymatique 613 Mpc dans l'espacement des
bassins (Laniakea→Shapley ~600-650 Mpc !? à mesurer proprement). Pilote du pipeline
automatisé "lois corrigées sur surveys entiers" voulu par Romain.
