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

## V15 — TERRAIN DIPÔLE COSMIQUE (recon juin 2026, OUVERT — pas de candidat)
Faits bankés (Secrest 2021, verbatim): dipôle quasars CatWISE D=0.01554 @ (l,b)=(238.2,28.8),
27.8° du dipôle CMB, ~2x le cinématique attendu (0.0073), 4.9σ — l'anomalie Ellis-Baldwin.
Compositions OBT testées avec NOTRE vecteur de dérive mesuré (carte #23: 300 km/s @ (299,+15)):
(a) soustraction de référentiel (matière partage la dérive) -> v_eff=238 km/s < 370 -> dipôle
RÉDUIT, contredit; (b) dipôle d'expansion additif (terme de flux x(1+α)β_d=0.0038) -> somme
0.0105 @ ~(282,+35) -> amplitude sous-prédite ET mauvais côté (observé 238 vs prédit 282).
VERDICT: le lien naïf dérive->dipôle de comptage ÉCHOUE dans les deux sens calculables.
EXIGENCE NOMMÉE (théorie d'abord): dérivation OBT propre de qui ressent la dérive dans les
comptages (le (1-3w) immunise la RADIATION du FORÇAGE, mais le dipôle CMB est notre VITESSE
— l'analyse de référentiel complète est subtile); tant qu'elle n'existe pas, le terrain est
fermé aux cartes. La discipline du jeu: pas de glue au dernier acte.

## V16 — RÉTRACTATION DE LA CARTE #24 (juin 2026) + deux règles de méthode frappées
Le test fumant (cf4_recon): mêmes 943 SNe CF4, modules bruts, binnés deux façons —
le déclin "vide" n'existe QUE binné par distance estimée (+2.5→−2.4%), disparaît binné
par redshift (−1.3,+1.7,−0.3,+0.3,+0.6%) = artefact Malmquist-de-bord, amplifié par le
posterior d'enveloppe. Et H0_out=67.00 ÉLUCIDÉ: la colonne DMsnIa de CF4 porte son propre
zéro-point (~0.2 mag du système SH0ES; moyenne brute 67.8) — le "67=Planck" était une
convention de calibration, pas de la cosmologie. RÈGLES FRAPPÉES: (1) JAMAIS binner un
monopôle de flot par distance estimée (z-binning ou forward modeling); (2) JAMAIS lire
une convention de zéro-point comme une mesure cosmologique. Survivent: les offsets/dérives
de points-zéros (phase 1), la règle une-amplitude, la trace méthodologique complète.
KBC et le bord cymatique 306 Mpc → retour au statut de prédictions pré-enregistrées NON
testées. NOTE OUTIL: ajouter une commande retract-card (architecture) — session future.

## V16-bis — CORRECTION DU MÉCANISME DE RÉTRACTATION (défi de Romain, juin 2026)
La rétractation #24 TENAIT mais son HISTOIRE était fausse: le cross-match direct 467 paires
CF4/Pantheon+ mesure +0.055 mag (pas ~0.2) → l'histoire "zéro-point" réfutée. Le paramètre
sous-estimé (littéralement la question de Romain): le terme de décélération FRW (1−q0)z/2,
ABSENT des pipelines CF4 (kbc_phase4, cf4_recon) — +7.8% à z=0.1. Restauré: H0_out=70.1
(pas 67.00 — le "=Planck" était l'omission), profil z-binné PLAT (−3.4,+0.4,−0.8,+0.8,
+2.3,+0.0), déclin lointain disparu. Décomposition finale du mirage #24: omission-q0
(dominante) + offset de trame réel +0.055 mag + Malmquist-de-bord/posterior (binning-d).
3e RÈGLE FRAPPÉE: les corrections cinématiques FRW font partie de l'instrument — H0=V/d
nu fabrique des pseudo-profils au % au-delà de z~0.03. Leçon de process: le défi de
Romain ("n'as-tu pas sous-estimé un paramètre?") a corrigé une rétractation juste mais
mal expliquée — l'audit de l'audit fait partie du jeu.

## V17 — the nu_e-for-pressure floor: derivation attempt #2 → card #26 REFUSED (bounded regime-split budget)
**June 2026, probe `nu_floor_budget`.** The #17/#18/#25 open question ("why do EFE-regime dispersions sit
+0.1..+0.2 dex above our prediction?") attacked head-on. Finding: **the floor is not one thing — it splits
by REGIME**, and no single mechanism closes it:
- **MW EFE set (N=21) is DEEP-EXTERNAL (median z/e = 0.01), floor +0.58 dex under Chae nu_e — but +0.29
  even under the no-EFE isolated ceiling**: this floor is dominated by the tidally inflated ultrafaints,
  i.e. it IS card #17 (sigma-excess vs eta_peri, p=0.004). Already explained; not a new card.
- **M31 EFE set (N=11) is the true TRANSITION regime (z/e = 0.24), floor +0.197**: three bounded smalls —
  (i) prescription spread capped by the no-EFE ceiling at <= +0.08 (summed-field goes the WRONG way,
  +0.342); (ii) M/L 2→3 worth <= +0.09 (floor +0.109 at the stellar-pop edge); (iii) residual #17 tides
  at eta 0.07-0.12 worth ~ +0.05-0.10. Jointly they COVER the floor; individually none closes it; no
  certainty on the split → **not card material** (golden rule: a card requires certainty).
- **DEEP-EXTERNAL COROLLARY (the useful new number)**: the exact z→0 limit of Chae's RC-fit,
  nu_e(0;e) = 1/2 + (B_e−A_e)/(2A_e), sits ~×1.7 BELOW the standard quasi-Newton boost 1/mu(e)
  (CratII: 5.27 vs 9.06; AntII: 5.76 vs 10.05) = **+0.12 dex of sigma** — explaining most of the
  "ours vs published" double bookkeeping carried by card #25 (+0.36/+0.11 dex). Our convention is the
  CONSERVATIVE end of the EFE-prescription family in deep-external; the ordinal statements (the #17
  trend, #25's AntII>CratII) are convention-robust, the absolute baselines are not.
Status: the floor question is now CLOSED as "bounded, regime-split, no new physics required" — the
previous "origin open" (the #18 failed attempt) upgraded to a quantified decomposition. The derivation
of the true pressure-system EFE normalization (full AQUAL solve for a point mass in an external field)
remains the one path that could still mint a card here — parked, theory-gated like the dipole.

## V18 — the sinc t_dyn convention PINNED (reviewer-mode item, June 2026)
Triggered by the DF2 terrain scouting (card #27 hunt): the W(t_dyn) filter's averaging window was
under-specified for diffuse pressure systems. Full theory.md read + pin (note added after the kinematic
hierarchy table): **global form t_dyn = R/sigma_v with R = OUTERMOST tracer radius** (the table's anchors:
MW 50 kpc outer disk -> 220 Myr; clusters 2 Mpc -> 2 Gyr — NEVER r_half), **radial form t_dyn(r) =
2 pi r / V_c(r)** for resolved profiles (the #22 X-COP form, empirically validated chi2/N=1.04, MOND
survives in BCG cores W~0.96), t_cross for transients (Bullet). The two forms agree on every overlapping
verdict. SENSITIVE ZONE flagged in theory.md: diffuse pressure systems (DF2/DF4 UDGs, Crater II/Antlia 2,
compact groups) are convention-limited (CratII W 0.35-0.94 across conventions) -> **game terrains DF2/DF4
and Hickson groups are GATED** until the orbital-averaging derivation specifies the tracer-weighted window
for pressure systems (named open theory item). Convention-safe: all compact classical dwarfs (W>=0.94
under every convention, <=1.6% in sigma) -> cards #14/#18/#25 unaffected; clusters extinguished under
every convention -> #22 unaffected. No V8.2 value changed — this is a clarification + an honest gate.

## V19 — the tracer-weighted window DERIVED (ARA refinement) → DF2/DF4 DE-GATED (June 2026)
Reviewer-mode derivation closing V18's open item (theory.md ARA subsection + scripts/sinc_tracer_window.py).
**The physics**: each tracer is a driven oscillator under the brane's amplitude modulation. ADIABATIC
regime (internal period T_int < T): the orbit tracks instantaneous a0(t) -> F=1, NO averaging — and the
galactic anchor a0=cH0/2pi is calibrated on adiabatic systems, so F=1 by normalization. AVERAGING regime
(T_int > T): the slow orbit averages the fast drive over its own period -> the V8.2 |sinc| boxcar envelope.
Crossover at T_int=T; resonance band [T/2,2T] keeps the O(1) EFT flag. T_int = T_orb/sqrt(2) (epicyclic)
for rotation; the radial-period distribution for pressure systems; system filter = light-weighted <F>.
**Data-mandated**: SPARC 174/175 galaxies sub-crossover (median T_kappa=0.54 Gyr) -> ARA predicts zero
suppression catalog-wide = what the RAR shows; the raw per-orbit boxcar would crush the outer points of
the 20 band galaxies by 36-97% — EXCLUDED by card #3's declining-curve residuals (+0.000+-0.089). X-COP
(#22) preserved on both ends (adiabatic BCG cores W~1; cluster bulk T_r=3-6 Gyr extinct).
**Windows (Plummer MC, light-weighted)**: DF2 W=0.83 [0.70-1] -> sigma effect <=5-9%; DF4 0.74; CratII
0.73 [0.52-1] (-8%, subdominant to #17/#25 tides); AntII 0.66 (+non-eq caveat).
**GATES UPDATED**: DF2/DF4 game terrains OPEN (adiabatic-dominated; OBT prediction = EFE-MOND there, a
consistency arena, NOT OBT-distinctive); feeble giants usable with stated brackets; groups stay
band-flagged. **NEW OBT-distinctive future falsifiable minted**: declining MOND boost beyond the epicyclic
resonance T_orb > sqrt(2) T ~ 2.8 Gyr — ultra-extended HI discs; first candidates UGC 9133 (T_kappa=2.05
Gyr), NGC 289 / UGC 128 (1.87). Honest: adiabatic+averaging limits derived; band interpolation stays EFT;
Plummer/isotropy +-10-20% folded into brackets.

## V20 — ARA falsifiable: barreau 1 DONE (band data-bounded) + the Malin 1 terrain identified (June 2026)
**Barreau 1 (reviewer, scripts/sinc_tracer_window.py band-entry stack)**: SPARC outermost-point RAR
residuals vs T_kappa: 0-0.5 Gyr +0.028+-0.016; 0.5-1 -0.003+-0.011; 1-1.5 -0.048+-0.028; 1.5-2.2
-0.074+-0.030; combined T_k>1: -0.068+-0.020 (3.4 sigma) -> **W_band > 0.61 (95%)** — the ARA band's
O(1) EFT flag is squeezed to [0.61,1] by data. The declining entry trend is REAL but DEGENERATE with
the EFE (both suppress outer residuals; Chae's 4-sigma EFE detection lives in the same zone) -> the
e-vs-T_kappa cross-regression is the named separating computation (we have the #16 e_env machinery).
**Barreau 2 (recon)**: the external claim EXISTS — Gentile et al. 2010 (A&A 516, A11): MOND fit of
Malin 1 requires NEGATIVE outer M/L = constant-a0 OVER-prediction at ultra-extended radii = exactly the
ARA suppression shape. Terrain identified for a possible OBT-vs-MOND distinctive card (#29 candidate):
patch = the (already-derived, non-glue) ARA window W(T_kappa) bounded [0.61,1]. CAVEATS pre-logged:
Malin 1 data quality (i~38 deg, warp — Lelli 2010 reinterpretation; the kappa-model fit shows inclination
is the soft spot); the EFE degeneracy must be handled in-fit. **Barreau 3 named**: the lensing-vs-dynamics
split — photons (crossing ~Myr << T) average NOTHING -> lensing keeps the FULL boost at all radii while
slow dynamical tracers beyond the resonance lose it; MOND predicts both full, LCDM both halo-like ->
unique OBT scissor. The Brouwer lensing-full-boost leg (card #5 data) is already consistent; the missing
leg = satellite kinematics around isolated hosts at 50-300 kpc.

## V21 — THE SCISSOR, blade A closed (the simple half); blade B deferred by design (June 2026)
Romain's mid-session rule applied: "mieux vaut commencer par simple... mais je me mefie" -> ONLY the
cheap blade today. **Blade A (probe scissor_lens, cached Brouwer KiDS-isolated ESD, #5 conversion)**:
at r_eff ~ 100-450 kpc — where ANY orbiting tracer sits at T_kappa = 3-30 Gyr, deep post-band — the
LENSING channel shows +0.129 +- 0.010 dex vs the exact OBT RAR: at or ABOVE full boost, with the +0.13
attributable to the known 2-halo term (the #5 nuisance, modeled there). NO trace of the -0.3 to -1 dex
suppression the ORBITAL channel would carry under ARA at the same T_kappa. The scissor's discriminating
gap (0.4-1+ dex) dwarfs the 2-halo nuisance -> the photon-instantaneous half of the OBT prediction
stands. **Blade B (the swamp, DEFERRED)**: satellite-kinematics at 50-300 kpc is the Klypin-Prada
battlefield — the anisotropy bracket (beta in [-0.5,0.5]) swings the inferred V_c by ~25%, likely
swallowing the discriminant at LV-cache sample sizes (pre-assessed: MW sigma_GSR ~95 -> V_c 134-165
vs MOND-full 180 vs ARA ~85-105: inconclusive zone). DECISIVE DATA NAMED: (a) SDSS/DESI satellite-
kinematics stacks (hundreds of hosts; anisotropy constrained by profile shape); (b) MW V_c(50-120 kpc)
from Gaia stream modeling; (c) M31 mass profile from its satellite system with proper Jeans brackets.
The scissor stays a MONSTER under encirclement — blade A in hand, blade B named, no card attempted.
Also pre-logged for blade B: the ARA fourth-root mercy (W=0.1 still gives V_c ~ 100 for the MW —
the suppression is large in g but gentle in V; the MW outer halo numbers may actually FAVOR ARA over
constant-MOND's 180-flat: a future hunt of its own, "the missing MOND plateau of the Milky Way").

## V22 — digging around: the band sextet (6/6) + the wall's ADDRESS (June 2026)
**(1) Replication leg of #29 landed from the cache (probe band_trio)**: all 6 SPARC band-crossers show
in-band points below their own sub-band points — median internal split -0.103 dex, sign test p=1/64,
galaxy-level systematics cancel in the split, per-object EFE budgets (e_env 0.024-0.04 -> <=0.04 dex)
cannot pay it. With Malin 1: SEVEN band-crossers carry the pattern. #29/#30 scope upgraded in place.
**(2) STRUCTURAL DISCOVERY while pre-assessing the 'missing MW plateau' hunt**: the deep-averaging zone
(T_int >> 2T) is BULK-GATED. ARA's per-tracer fixed point is ill-defined in the |sinc| oscillating tail
(nodes), and V8.2's own three-component law says what physically happens: as the sinc kills MOND, the
WEYL sector takes over — and its amplitude/profile is the closure-problem input (the 5:1, the cored
f_W~0.7 of #22). So beyond T_int ~ 2T (MW halo 150-300 kpc, scissor blade B, diffuse groups) OBT has
NO parameter-free prediction until V9.0 specifies the galactic Weyl floor. THE WALL HAS AN ADDRESS:
it begins exactly where the internal period crosses ~2T = 4 Gyr. Every deep-radius terrain (dipole,
growth sign, blade B, MW plateau, groups) is the SAME wall = the bulk's customs zone. The game's
conquered domain is exactly T_int < 2T; the band [T/2,2T] is mapped and measured; beyond is V9.0 land.

## V23 — GATE 10 OPENED: the holographic route to the Weyl-DM (June 2026, QUARANTINED V9.0)
The attack toward the bulk, by the one dictionary not yet played: RS/CFT (E_munu = <T_munu>_CFT —
the closure freedom IS the dual-sector state; CDM-like Weyl-DM requires a CONFINED/COLD dual state).
**Finding 1 (thermal branch DEAD)**: the 3->2 glueball relic scan at Lambda_dark = 0.4-5 eV under-
produces by >=15x for any N_eff-allowed xi (needs xi~0.5-1, excluded). [Self-check caught my own
script's READ line contradicting its own table — fixed before banking. The #24 reflex.]
**Finding 2 (THE BANKED NUMBER — misalignment branch)**: a coherent radion condensate (fast free
mode at m_phi = 0.36 eV around the GW minimum, distinct from the slow 2-Gyr forced motor) displaced
phi_0 at inflation gives Omega h^2 = 0.12 for phi_0 = 0.26 M_s — an O(1) fraction of the DERIVED
LVS string scale (M_s = 1.19e12 GeV), zero new parameters beyond the axion-angle-class fraction.
Cold, collisionless (coherent), N_eff-safe, stable (tau ~ Mpl^2/m^3 >> t_U). The closure input
"Omega_DM ~ 5 Omega_b" acquires its first candidate CALCULATION inside OBT's own derived scales.
**Finding 3 (THE INTERNAL KILL-TEST = Gate 11's question)**: a 0.36-eV condensate is plain CDM at
all scales -> it would pile halos onto GALAXIES and destroy OBT's own zero-halo galactic success.
OBT requires CLUSTER-SELECTIVE clustering (the #22 anatomy). The route lives or dies on a scale-
selection mechanism for the condensate's gravitating coupling — the nonlinear-bulk question again,
now sharpened to ONE object (the condensate's effective source term) and ONE banked number (~0.3).
Script: explorations/bulk_solver/gate10_weyl_cft.py. Status: V9.0 seed, NOT V8.2 content.

## V24 — GATE 11: the kill-test executed; the condensate transmutes into the PEG GENESIS (June 2026, V9.0)
Methodical mechanism inventory FIRST (M1 slip-adiabaticity dead 1e30; M2 invented couplings refused as
glue; M5 bulk-depth um-vs-kpc dead; M6 sinc inapplicable — condensate <rho> is static; R2 'condensate
mimics mu(x)' FORBIDDEN BY OUR OWN 31 CARDS). Then the numbers:
**1. KILL CONFIRMED**: all-DM condensate adds +0.43 dex to deep-MOND RAR points — dead by x25; the
RAR scatter bounds any galactic condensate fraction to f < ~4%. Gate 10's prettiest reading is killed
by OBT's own galactic success. (phi_0 = 0.26 M_s reading retired.)
**2. THE CONSISTENCY THEOREM (the transmutation)**: M_Kaup = 0.633 Mpl^2/m vs M_crit = L Mpl^2/2 ->
M_K/M_crit = 1.27/(mL) ~ O(1) AUTOMATICALLY because the GW radion has m ~ 1/L. Numbers: M_K(m_phi) =
3.5 M_crit; M_K(m_1) = 0.67 M_crit; birth granularity (horizon mass at H=m) = 2.7 M_crit. The
condensate is born grainy at the peg scale and its lumps cap at the perforation threshold — both
structural in L, zero tuning.
**3. SURVIVING BRANCH**: condensate = the PEG-PROGENITOR sector (Omega_cond = 1% Omega_DM at
phi_0 = 0.026 M_s, natural few-% displacement): galactic kill passed trivially (+0.004 dex);
**PBH GENESIS DERIVED** (super-Kaup minicluster collapse -> sub-GL 5D capillaries = the pegs), the
**EMF CEILING DERIVED** (M_K ~ 1e-10 Msun from Mpl, m_phi alone — V8.2 had it as input via the
inflationary spike), the log-normal EMF = the minicluster mass function (computable next).
**4. SHARPENED NEGATIVE for the 99%**: no cold bulk-resident SUBSTANCE can avoid galaxies by any
known mechanism -> the cluster-scale Weyl-DM must be scale-selected by its RESPONSE/FORMATION physics
(sourced where the boost dies — the sinc anatomy), not by its nature. THE V9.0 OBJECT IS A RESPONSE,
NOT A GAS. Script: gate10_weyl_cft.py + gate11_selectivity.py. Quarantined.

## V25 — GATE 12 RE-VERIFIED (Romain: "tu pourrais t'etre trompe") — audit holds, Gate 10 bug found (June 2026)
Romain pushed me to recompute and re-check. Done by THREE independent methods + the decisive test
my first Gate-12 pass had skipped: CALIBRATION on the QCD axion (known M_mc).
**RESULT 1 — Gate 12 (the audit) CONFIRMED**: the formula M_mc=(4pi/3) rho_comp,0/k_osc^3 reproduces
the QCD-axion minicluster mass at 4e-12..4e-11 Msun (T_osc~1-2 GeV) = squarely in the literature band
(Kolb-Tkachev 1994, Eggemeier 2020, 1e-14..1e-10). So the formula is trustworthy. Applied to the
radion (m=0.36 eV, onset H=m at T_osc~16 TeV): M_mc = 5e-25 Msun (~1e5 kg), ~15 orders BELOW the EMF
window. Gate 11's "PBH genesis / EMF ceiling derived" stays RETRACTED — the error was confusing the
TOTAL horizon mass (Mpl^2/m) with the DM-grain mass (= horizon x rho_phi/rho_tot ~ 1e-17). Physical
reason: the radion oscillates EARLY (m fixed, large) -> tiny horizon -> tiny grain; the QCD axion
oscillates LATE (1 GeV, thermal mass) -> big grain. Double-constraint (right abundance AND grain in
EMF) is unsatisfiable within OBT's derived m -> condensate and PBH pegs are SEPARATE sectors.
**RESULT 2 — a real BUG found, but in GATE 10 not Gate 12**: the relic-abundance normalization used
S0_RHOC = 3.6e9 GeV^-1; the correct s0/(rhoc/h^2) = 2891.2/1.0537e-5 = 2.74e8 GeV^-1 -> Gate 10 was
x13.1 too big. Corrected, the radion condensate carries the FULL dark matter at phi_0 = M_s EXACTLY
(the derived LVS string scale, the most natural O(1) displacement) — cleaner than Gate 10's 0.26 M_s.
(All-DM still killed by Gate 11's galactic halo test -> the condensate is sub-dominant.)
**NET**: main conclusion (Gate 12) survives the killer test (QCD axion); an auxiliary number (Gate 10
abundance) had a x13 bug that, fixed, beautifies the picture (phi_0 = M_s). The M_Kaup~M_crit~Mpl^2/m
scale identity remains real (dimensional). The #24 reflex — re-checking even our own audit — paid off
in BOTH directions: confirmed the audit, caught a separate bug. Scripts: gate12_minicluster.py (first
pass) + gate12_recheck.py (the validated re-verification).

## V26 — GATE 13: the cluster Weyl-DM is NOT sinc-sourced — the closure wall, confirmed empirically (June 2026)
Attacked the V9.0 frontier (the non-linear cluster-selective Weyl-DM response). Hypothesis (from Gate 11):
"the cluster Weyl-DM is sourced where the MOND boost dies (sinc extinction)" -> its radial profile should
track (1-W(r)). Tested on the 12 X-COP clusters (hydrostatic M(r) + gas + REAL stellar mass), zero
per-object params: f_Weyl(r) = [g_obs - g_N - Dg_MOND*W]/g_obs vs (1-W(r)).
**RESULT — REFUTED (a clean negative)**: global Spearman(1-W, f_Weyl) = -0.63; f_Weyl is HIGH at the
CORE, not the edge. Verified with the real BCG stellar mass (not a proxy): M_tot/M_bar = 5-8 at r~40 kpc,
where g_N/a0 = 360-1090 (deep Newtonian -> MOND boost mu->1 is ZERO) AND W~0.99 (sinc inactive). The
Weyl-DM dominates exactly where NEITHER the sinc NOR MOND act. So the sinc is NOT the cluster-selectivity
mechanism; it remains valid only for tracer dynamics / the cluster periphery (ARA, cards #29-31).
**THE WALL, reached from the cluster face**: the AMPLITUDE/selectivity of E_00 (cluster ~0.85, galaxy ~0)
is the irreducible closure input (Koyama-Maartens) — now CONFIRMED empirically on 12 clusters. The classic
MOND "cluster problem" (residual factor 2-8 even at g>>a0) IS that input. What stays derivable: the FORM
(self-similar cored, card #22, chi2/N=1.04) via bulk regularity. Form constrained, amplitude IC — EXACTLY
parallel to cosmological gates 0-9. The non-linear solve does NOT crack the selectivity; the bulk keeps
the dark-matter amplitude as its own datum. Gate 11's "RESPONSE sourced where the boost dies" framing is
CORRECTED: the periphery is sinc-shaped, but the core/amplitude is pure closure input. Script:
gate13_weyl_response.py. Quarantined; sacred files untouched.

## V27 — GATE 14: the Weyl-DM selectivity variable is WELL DEPTH, not the sinc (June 2026)
Searched for the OTHER oscillation/brane mechanism for clusters after Gate 13 killed the sinc. A bug
caught first (the #24/#12 reflex): a0 was x1000 wrong in BOTH gate13 and gate14 (3703.7 vs the correct
3.702e6 (km/s)^2/Mpc; 3.70 vs 3702 per kpc) — flagged by galaxies giving f_Weyl=0.64 (must be ~0). FIXED.
**With correct a0**: the selectivity-variable comparison is decisive —
  f_Weyl vs (1-W) [sinc/t_dyn] : Spearman -0.05  -> NOT the organizer (Gate 13 conclusion holds, sharpened)
  f_Weyl vs V_c   [well depth] : Spearman +0.61  -> THE organizer
Galaxies (shallow): f_Weyl~0.12+/-0.25 (compatible with 0, MOND works, no halo). Clusters (deep): ~0.82.
So the cluster Weyl-DM is organized by POTENTIAL-WELL DEPTH, not dynamical time. Mechanism candidate:
brane FLEXURE by mass via the Israel junction (buckling above a critical |Phi|) — a geometric brane
effect, baryon-determined, zero particles.
**HONEST CAVEATS**: (1) the transition V_c~400-700 is a DATA GAP (0 whole systems, only cluster cores
rising) -> GROUPS are the missing decisive test; (2) SPARC (max 383) OVERLAPS X-COP cores (min 311) yet
f_Weyl differs at equal LOCAL V_c -> the true variable is GLOBAL |Phi| (cluster cores sit in deep global
wells), not local V_c; (3) empirical correlation, the flexure mechanism + threshold + link-to-oscillation
are NOT derived. **NET PROGRESS toward Romain's "no dark matter"**: the cluster Weyl amplitude is no
longer a free per-cluster constant — it is a universal function f_Weyl(|Phi|) of baryonic well depth,
reducing the closure freedom from "arbitrary amplitude" to "one universal function + a threshold to
derive". But it is NOT yet "the oscillation": galaxies = tilt (oscillation/horizon a0); clusters = brane
flexure (well depth) — two distinct brane effects, both matter-free. NEXT: groups (CLoGS/Lovisari) at
V_c~400-700 + recompute with global |Phi|. Scripts: gate13 (a0-fixed), gate14_welldepth.py. Quarantined.

## V28 — GATE 15: the groups bridge the gap — f_Weyl(well depth) is ONE continuous law (June 2026)
Harvested X-ray GROUPS (Lagana 2013, J/A+A/555/A66: r500/kT/Mgas/Mtot/Mstar resolved, ReadMe-confirmed
units kpc/1e12/1e13/1e12, f_bar=0.08-0.13 physical) to fill the galaxy/cluster gap and test Romain's
unification (tilt + Weyl = ONE brane movement, a local variant). Test: f_Weyl = 1 - g_MOND/g_obs with the
FULL MOND boost (W=1, isolating well depth from the sinc), at the characteristic radius, vs global V_c.
**RESULT — unification SUPPORTED**: f_Weyl is ONE continuous, monotone curve of V_c, smoothly bridged by
the groups: galaxies V_c~110 f_Weyl=-0.01 (MOND works, pure tilt, no Weyl); GROUPS V_c~489 f_Weyl=+0.15;
clusters V_c~1563 f_Weyl=+0.29 at r500 (~0.67 at core). Spearman +0.51, N=160. The group regime is now
POPULATED -> the transition is MEASURED to be CONTINUOUS, not a two-population jump. Tilt (linear,
galaxies) and Weyl (nonlinear, clusters) are endpoints of a single f_Weyl(|Phi|) relation = "one brane
movement, a local variant", as conjectured.
**HONEST CAVEATS**: (1) the rise is GRADUAL, not a sharp buckling threshold (smeared over V_c~200-1500) ->
"graded nonlinearity with well depth", not a clean |Phi|_crit; (2) amplitude is sinc-dependent (full-boost
residual at r500 ~0.29 vs ~0.82 with sinc-killed periphery+core) -> Weyl has TWO contributions, well-depth
residual (this gate) AND sinc extinction (Gate 13/14), both ending up tracking depth (core=deepest |Phi|);
(3) only 9 groups, empirical, mechanism (nonlinear brane deflection coupling to |Phi|) is a candidate not
derived. **NET**: a single continuous f_Weyl(well depth) law galaxies->groups->clusters supports the
unified one-brane-movement picture; the cluster Weyl amplitude is a graded function of well depth (not a
free per-cluster constant). Geometric, baryon-determined, zero particles. V9.0 target: derive the
nonlinear brane-deflection mechanism. Data: lagana13.csv. Scripts: gate15_threshold.py. Quarantined.

## V29 — GATE 16: the clean clue — Weyl ~ M_bar^1.42 (super-linear = nonlinearity) (June 2026)
Accumulating clues on the brane-deflection mechanism, simplest first: the exponent + primary variable
of the Weyl law. CIRCULARITY CAUGHT FIRST (the re-check reflex): V_c, |Phi|, M_tot are ALL derived from
M_tot, which CONTAINS M_Weyl -> their high "tightness" (Spearman 0.94-0.98) is inflated/circular, DISCARDED.
The only variables INDEPENDENT of M_Weyl are M_bar (observed gas+stars) and kT (X-ray, groups).
**CLEAN CLUE (21 systems, M_bar independent)**: M_Weyl ~ M_bar^1.42 (scatter 0.81 dex, Spearman +0.86)
-> Weyl/baryon ratio ~ M_bar^0.42 = SUPER-LINEAR: the deficit grows faster than baryons (groups f_Weyl
0.15 -> clusters 0.29). Super-linearity (q>1) IS the signature of nonlinearity/selectivity: if the brane
response were linear in mass (q=1) there'd be no selectivity (constant Weyl/baryon); q=1.42 means bigger/
deeper systems get proportionally MORE Weyl -> consistent with Romain's linear(galaxies)->nonlinear
(clusters) one-brane-movement picture, the exponent sitting between 1 (linear/baryons) and 2 (quadratic/
deflection). DEPTH(kT) vs MASS(M_bar): NOT separable at N=9 groups (partial Spearman +0.07 vs +0.17, both
weak, kT-M_bar correlated). HONEST: modest incremental clue; scatter 0.8 dex; circular V_c/|Phi| discarded;
the depth-vs-mass primary-variable question needs a bigger clean sample (more groups with measured kT).
NET accumulated so far (Gates 13-16): selectivity is NOT the sinc (13); tracks well depth/size not t_dyn
(14); is ONE continuous law galaxies->groups->clusters (15); scales super-linearly M_bar^1.42 =
nonlinear/selective (16). All consistent with one nonlinear brane-deflection mechanism; the mechanism
itself + depth-vs-mass disentangling remain open. Scripts: gate16_exponent.py. Quarantined.

## V30 — GATE 17: depth-vs-mass is DEGENERATE; the Weyl is centrally concentrated (June 2026)
Romain asked for more groups to disentangle depth(kT/|Phi|) vs mass(M_bar). FIRST FINDING (decisive,
no harvest needed): whole-system points CANNOT disentangle them — kT and M_bar lie on a TIGHT 1D
scaling sequence (Spearman 0.93, M_bar~kT^1.26, scatter only 0.10 dex). Depth and baryonic mass are
degenerate on it; more groups just add points to the same line. This is physics (virial scaling
relations), not a statistics shortfall.
SECOND: the only shape-different disentangler is the RADIAL profile within clusters (rho_bar steep vs
|Phi| flat). Gate 17 (X-COP, 12 clusters, full-MOND M_Weyl, local densities via dM/dr): rho_Weyl/rho_bar
= 11.7 (inner third) -> 2.5 (outer), log-slope gamma_Weyl=-2.89 vs gamma_bar=-1.72. So the Weyl density
is MORE concentrated/steeper than the gas -> it does NOT track the local baryon density; it tracks the
total dynamical mass / potential (centrally peaked, BCG+cusp). BUT this is near-tautological (M_Weyl is
the majority of M_tot at the core, factor 5-8, so rho_Weyl ~ rho_tot by construction) AND contaminated
by gas thermodynamics (cool cores / feedback shape rho_bar independently). So the radial test is NOT a
clean depth-vs-mass disentangler either.
NET (the honest limit): depth and baryonic mass are INTRINSICALLY degenerate in equilibrium clusters
(1D for whole systems; Weyl~rho_tot + gas-contaminated radially). "More groups" does not break it. Weak
indication: the Weyl is centrally concentrated and traces the total potential/dynamical mass (halo-like),
consistent with a deflection sourced by the well. DEFINITIVE disentangling is theory-gated OR needs data
that breaks the scaling relation: (a) gas-rich vs gas-poor systems at FIXED kT (same depth, different
M_bar), or (b) weak-lensing masses (hydrostatic-independent). Accumulated picture Gates 13-17: not sinc;
tracks well depth/size not t_dyn; one continuous law galaxies->clusters; super-linear M_bar^1.42;
centrally concentrated tracing the total potential. All consistent with ONE nonlinear brane-deflection
mechanism (Romain's picture); the mechanism's derivation + the depth/mass primary remain open, the
latter now KNOWN to be scaling-degenerate. Scripts: gate17_radial.py. Quarantined.

## V31 — GATE 18: weak lensing BREAKS the degeneracy — Weyl tracks baryonic MASS, not depth (June 2026)
Romain's instinct (gas-rich vs gas-poor at fixed kT) executed CLEANLY via CCCP (Mahdavi 2013): M_WL
(weak-lensing mass, hydrostatic-INDEPENDENT) + M_Gas + kT for 50 clusters (kT 3.1-12.1 keV). The
hydrostatic circularity (Gate 17) is bypassed because M_WL does not use the gas.
**RESULT — it is baryonic MASS, not well depth (kT)**:
  TEST 1 (cleanest): at fixed kT, M_WL ~ M_Gas | kT = +0.68 (strong), M_WL ~ kT | M_Gas = -0.14 (null).
    -> the TOTAL lensing mass follows the baryon content, NOT the depth.
  TEST 2: M_Weyl,WL = M_WL - nu*M_bar (non-circular): M_Weyl ~ M_Gas|kT = +0.50, ~kT|M_Gas = -0.10,
    exponent M_Weyl ~ M_Gas^1.57 (super-linear, matches Gate 16's M_bar^1.42).
**IMPLICATION (refines/corrects the picture)**: the Weyl-DM PRIMARY variable is baryonic MASS (super-
linear, ~M_bar^1.5), NOT potential-well depth. Gate 14's "well depth V_c" was a CIRCULAR proxy (V_c
contains M_tot which contains M_Weyl); the clean lensing test shows depth (kT) drops out once mass is
controlled. Selectivity galaxies/clusters comes from the SUPER-LINEARITY in M_bar (f_Weyl ~ M_bar^0.5:
small galaxies little Weyl, big clusters lots), not from a depth threshold. Consistent with a nonlinear
brane DEFLECTION sourced by mass-energy (Israel: the brane bends to S_munu ~ mass), the response
super-linear -> Romain's one-brane-movement, with the source now pinned to baryonic MASS.
**HONEST CAVEATS**: kT-M_Gas correlated (+0.82) so leverage is limited (partials handle it, +0.68 vs
-0.14 is clear); kT is a NOISIER mass proxy than M_Gas, which contributes to the result (so read it as
"depth alone does not set the total mass; baryon content does"); clusters only (3-12 keV, no groups/
galaxies in this set); lensing masses noisy (~30%); M_star approximated as 0.15 M_Gas. NET (Gates
13-18): not sinc(13); Gate14's well-depth was circular; the clean disentangler (18) says BARYONIC MASS,
super-linear M_bar^1.5; one continuous law(15); centrally concentrated(17). One nonlinear brane
deflection sourced by baryonic mass-energy. Data: cccp/table1,2.tex. Script: gate18_lensing.py. Quarantined.

## V32 — GATE 19: the nonlinear mechanism IDENTIFIED — SMS quadratic pi_munu (rho^2) (June 2026)
Deriving the nonlinear brane-deflection mechanism behind the Weyl-DM (empirical M_Weyl~M_bar^1.57).
SMS has EXACTLY ONE nonlinear term: G_munu = 8piG T + kappa5^4 pi_munu - E_munu, with pi_munu ~ rho^2
(the high-energy brane correction; the only super-linear handle). So the nonlinear response form is
intrinsically QUADRATIC. Data confirm it: rho_Weyl ~ rho_bar^p locally with p=1.49 (374 X-COP bins,
Spearman +0.98), matching the system law (1.57) and radial slope (1.68) — all QUADRATIC-CLASS, p>1,
the signature of pi_munu. 
DERIVATION STATUS (honest, the program's pattern again):
 * FORM (super-linear ~rho^2, quadratic-class) = DERIVED from SMS pi_munu (unique nonlinear term),
   confirmed by data p~1.5-1.7.
 * AMPLITUDE (the 5:1) = closure/IC. The DIRECT pi_munu amplitude is ~10^-40 (theory.md) -> 40 orders
   too small to BE the dark matter; the free bulk Weyl E_munu carries the amplitude (integration
   constant), with Bianchi (nabla E = kappa5^4 nabla pi) tying the SOURCED part to the rho^2 form. The
   universal p~1.5 across 12 clusters is empirical evidence the Weyl FOLLOWS the quadratic form even
   though the bulk amplifies its amplitude.
 * exact exponent (1.49 vs 2) = bulk projection softening + homogeneous-part + dM/dr noise (model-level).
CAVEATS: rho_Weyl is derived from M_tot which contains baryons -> residual circularity in the local
fit (noted; the system-level lensing exponent 1.57 from Gate 18 is the clean cross-check); p<2 not
derived exactly. NET: the MECHANISM is identified (SMS quadratic high-energy correction pi_munu ~ rho^2,
the unique nonlinear brane term), its super-linear FORM derived and data-confirmed (p~1.5-1.7); the
AMPLITUDE remains the closure/IC datum. "One brane movement" is now precise: the brane's quadratic
high-energy response to baryonic mass-energy, amplified to observable level by the free bulk Weyl.
Full derivation (amplitude) = the 5D bulk solve, closure-blocked. Script: gate19_mechanism.py. Quarantined.

## V33 — GATE 20 CONSOLIDATION: mistrust caught a clip bug; the exponent is ~1.2 not 1.5 (June 2026)
Romain: consolidate prudently, mistrust, re-verify. Did so by trying to BREAK Gates 13-19.
**BUG CAUGHT (the #24/#12 reflex)**: Gate 18's "M_Weyl ~ M_Gas^1.57" was a CLIP ARTIFACT —
np.clip(Mweyl,1e11) floors negative/small Weyl values and inflates the log-log slope. CCCP clusters:
WITH clip q=1.57, WITHOUT clip q=0.79. The clean wide-range exponent (Lagana groups + X-COP clusters,
hydrostatic, NO clip, N=20, M_bar spanning 12.3-14.5 dex): M_Weyl ~ M_bar^1.19 [1.05,1.34] bootstrap.
So the real exponent is ~1.2 (MODESTLY super-linear), NOT ~1.5.
**WHAT HOLDS (robust)**: (1) MASS not depth — M_WL~M_Gas|kT = +0.66 [0.55,0.75], survives controlling
M_hydro (+0.70), M_WL~kT|M_Gas = -0.24 (depth anti-, weak); Gate 18's CORRELATION is solid (only the
exponent was bugged). (2) Not the sinc (13). (3) Amplitude = IC/closure (multi-face). (4) Modest
super-linearity q~1.2 (f_Weyl ~M_bar^0.2: groups 0.15 -> clusters 0.4, consistent).
**WHAT FALLS/CORRECTED**: Gate 18 exponent 1.57 -> clip artifact (true ~1.2). Gate 19's "quadratic SMS
p~1.5-2, form derived" -> NOT supported: q=1.19 is much closer to LINEAR(1) than QUADRATIC(2); the
quadratic pi_munu is still the only nonlinear SMS term but the DATA DO NOT CONFIRM a quadratic exponent,
so the mechanism's exact form is NOT pinned. Gate 19 local p=1.49 was circular + dM/dr-noisy.
CAVEAT on 'baryon-specific': M_Gas is also the tightest M_500 proxy and the M_hydro control is
contaminated by (possibly gas-correlated) hydrostatic bias, so 'baryon-specific vs total-mass' stays
ambiguous; the robust statement is "mass not depth". 
NET: SOLID = Weyl tracks baryonic MASS not depth, modest super-linearity q~1.2, IC amplitude, not sinc.
WITHDRAWN/weakened = exponent ~1.5 and the quadratic-mechanism derivation (Gate 19). DO NOT take the 5D
bulk-solve last step on a quadratic premise — the data only support weakly-super-linear mass-tracking,
mechanism-form OPEN. Mistrust before the leap: justified, it saved a false foundation. Script:
gate20_consolidate.py. Quarantined.

## V34 — GATE 21: the FORM is a SATURATED TRANSITION (factor-2 plateau), not a power law (June 2026)
Constraining the mechanism's form over the widest available lever (no new harvest needed): combined
SPARC galaxies (f_Weyl~0 anchor) + Lagana groups + X-COP & CCCP clusters, same definition f_Weyl =
1 - g_MOND/g_obs (full MOND, W=1) at the characteristic radius, M_bar spanning 7.7-14.5 dex (6.8 decades).
**RESULT — saturated transition (sigmoid)**: f_Weyl ~ 0 for galaxies (logM_bar < 12, median ~0 across
4 decades 8.5-12), rises through groups (12-13.4), PLATEAUS at ~0.45 for clusters (logM 13.4-14.8:
0.458 then 0.441 — flat over 1.4 decades). So NOT a single power law and NOT quadratic (which would
diverge): the Weyl SATURATES at f_Weyl~0.45, i.e. M_tot/M_MOND ~ 1.8 = the classic universal MOND
cluster factor-~2 (Sanders), here reproduced and shown mass-INDEPENDENT in the cluster plateau.
Transition center ~M_bar 5e12-1e13 (kT~2-3 keV, V_c~500-700). 
**IMPLICATION for the mechanism**: Gate 20's q~1.2 was the LOCAL slope of the RISE, not a global law;
the quadratic SMS reading (Gate 19) is further excluded by the PLATEAU (a rho^2 response would not
saturate). The mechanism is a THRESHOLD-and-SATURATE: the brane nonlinear response turns on around
M_bar~1e13 and saturates at the factor-2 level for all clusters. This is a genuine FORM constraint:
the 5D bulk solve must reproduce (a) zero Weyl for galaxies, (b) a rise at group scales, (c) a
mass-independent factor-2 plateau for clusters.
**CAVEATS**: the transition zone (logM 12-13.4) is SPARSE (only ~13 systems: Lagana groups + a few) ->
the RISE shape (sharp threshold vs gradual) is NOT yet pinned; mixed methods (RAR galaxies, hydrostatic
groups, hydro+lensing clusters) carry cross-systematics that could shift levels; the galaxy bins are
noisy (median ~0 with +-0.25 scatter). To pin the rise (and thus the mechanism's turn-on), still need
more GROUPS at logM_bar 11.5-13.5 (Sun 2009 / Lovisari 2015, arXiv rate-limited this session).
NET: the FORM is a saturated transition (0 -> rise -> factor-2 plateau), reproducing the universal MOND
cluster factor-2; power-law and quadratic are excluded; the rise shape awaits more groups. Script:
gate21_form.py. Quarantined.

## V35 — GATE 22: rise densified (Sun09) — a MODERATELY SHARP transition at M_bar~4e12 (June 2026)
Densified the transition zone with 23 Sun09 groups (ar5iv T12: T500/r500/M500/fgas500, units verified
NGC1550 1keV/465kpc/3.18e13/0.097) -> 32 groups total in the rise (was ~9). f_Weyl(M_bar): ~0 for
galaxies (logM<11.8, 3 flat decades), turns on at logM_bar~12.2 (0.09), rises through 12.6-13.0 (0.29),
PLATEAUS ~0.45 for clusters (logM 13.4-14.6: 0.46/0.46/0.44). The transition is MODERATELY SHARP,
centred at M_bar ~ 4e12 (kT~1.5 keV, V_c~450), going 0 -> factor-2 plateau over ~1-1.5 decade. NEITHER
a discontinuous threshold (no 0->0.45 jump) NOR a soft power law (saturates; rise steeper than a power
law) => a REGIME CHANGE of the brane response at a soft mass threshold ~4e12 Msun(bar).
THE 5D BULK SOLVE MUST REPRODUCE (now three pinned features): (1) zero Weyl for galaxies (M_bar<~1e12);
(2) a moderately sharp turn-on centred at M_bar~4e12 over ~1 decade; (3) a mass-independent factor-2
(f_Weyl~0.45) cluster plateau. CAVEATS: M_star per-catalog inconsistency (Sun09 0.5*M_gas estimate,
Lagana/X-COP real, CCCP 0.15*M_gas) shifts group placement ~0.1 dex; mixed mass methods (RAR/hydro/
lensing); group scatter real (Spearman +0.43); Lovisari15 not added (ar5iv longtable not parseable;
32 groups already define the rise). NET: the FORM is now well-constrained = saturated regime-change
transition (galaxies 0 / turn-on ~4e12 / factor-2 plateau). Data: sun09 ar5iv T12. Script: gate22_rise.py.
Quarantined. NEXT: this 3-feature form is the target spec for the 5D solve (the last step).

## V36 — GATE 23: final consolidation — features refined, mass-independence confirmed by 2 methods (June 2026)
Stress-tested the 3 pinned features before the 5D solve. F1 (zero Weyl for galaxies): robust.
F2 (turn-on): M_bar turn-on shifts ~0.5 dex with M_star (Sun09 logM_bar 12.6->13.1 gas-only->+gas), but
is STABLE in M_tot/kT (logM_tot~13.7-13.9, kT~1.5-1.7 keV) -> specify the threshold in OBSERVABLES
(kT~1.5-1.7 keV / M_tot~5-8e13), not M_bar. F3 (factor-2 plateau): NUANCED but its core HOLDS:
 - MASS-INDEPENDENT confirmed by BOTH methods (slope -0.07/dex flat, N=61) -- the key claim.
 - METHOD-dependent VALUE: X-COP hydro 0.29 vs CCCP lensing 0.46; the clean true-mass value is the
   LENSING 0.46 (factor ~1.85); hydro lower = standard hydrostatic-bias direction (clean numerical
   demo not done -- rayon/M_star also differ between the two sets, honest caveat).
 - RADIUS-dependent: f_Weyl rises inward (X-COP 0.59 at 0.4 r_last -> 0.29 at r_last) -> the plateau is
   an r500 value, not radius-universal; the Weyl is centrally concentrated (consistent Gates 13/17).
REFINED 5D-SOLVE TARGET SPEC: (1) zero Weyl for galaxies; (2) turn-on at kT~1.5-1.7 keV (M_tot~5-8e13),
M_star-robust; (3) mass-independent f_Weyl(r500)~0.46 (true/lensing mass), rising inward.
NET: consolidation STRENGTHENED the mass-independence (2 independent methods) and the threshold
(kT-robust), and correctly DOWNGRADED 'universal 0.45' to a method/radius-dependent value with robust
mass-independence. The spec is now as tight as the data allow. Remaining caveats (mixed methods, M_star,
hydro bias not isolated) are the floor; further consolidation would need a single homogeneous
lensing+gas+stars sample over groups->clusters (not in hand). Script: gate23_stress.py. Quarantined.

## V37 — CONSOLIDATION CLOSED: final script audit clean; the 5D-solve spec is locked (June 2026)
Last consolidation pass (no new data possible): audited ALL gate13-23 scripts for hidden bugs (the #24
reflex applied systematically). FINDINGS: (a) a0 convention is CLEAN everywhere (3.702e6/Mpc, 3702/kpc)
-- the x1000 bug was fully fixed; (b) the only consequential clip bug is Gate 18's clip(Mweyl,1e11)
(caught by Gate 20, now marked in-place); (c) other clips are inoffensive (Gate 13's +-0.2/1.2 only
bounds Spearman ranks; Gate 21's 0.03 floor acts below an already-excluded threshold; Gate 16's 1e9
floor is below all real masses). No further systematic bug. 
**CONSOLIDATION IS EXHAUSTED** with the data in hand. The locked, stress-tested 5D-SOLVE TARGET SPEC:
  F1. zero Weyl for galaxies (M_bar < ~1e12) -- MOND-complete suffices, robust.
  F2. a moderately sharp turn-on at kT ~ 1.5-1.7 keV (M_tot ~ 5-8e13), M_star-robust, over ~1 decade.
  F3. a MASS-INDEPENDENT f_Weyl(r500) ~ 0.46 (lensing/true mass; factor ~1.85), rising inward
      (centrally concentrated), confirmed mass-independent by TWO independent methods.
And the established epistemic frame (Gates 0-23): the brane DERIVES the FORM (mass-tracking not depth,
saturated transition, mass-independent plateau); the AMPLITUDE (the factor ~2 / the 5:1) is the
closure/IC datum, not derivable on the brane alone. The 5D solve's job is to test whether a bulk
regularity condition PROMOTES the amplitude from IC to derived -- the single open question. Further
data-side consolidation would need a homogeneous lensing+gas+stars groups->clusters sample (not in
hand). READY for the 5D solve attempt. Quarantined.

## V38 — GATE 24: THE 5D SOLVE (the last step) — closure CONFIRMED, amplitude is the bulk's datum (June 2026)
Romain: go, multiple passes, self-check + re-verify after each. Done (4 passes, gate24_solve5d.py).
PASS 1: static master equation psi''=(k^2-1/4z^2)psi, solution sqrt(z)[A I0+B K0], ODE verified to 1e-5;
  two modes: K0 regular/normalizable (RS2), I0 irregular (= the free Weyl charge).
PASS 2: REGULAR RS2 mode (K0) + Israel source -> Garriga-Tanaka Yukawa f_Weyl=2L^2/3r^2 ~ 1e-56..1e-59
  at cluster radii (cross-check (kL)^2=4.2e-59). The baryonic mass does NOT source cluster dark matter
  on the brane via the normalizable mode. SOLID (established RS2 result).
PASS 3: the FREE mode (I0 / Weyl charge / dark radiation) carries the factor-2. Poisson projection
  (EXACT: E_00 = k^2 Phi_Weyl) + self-similar clusters -> f_Weyl ~ A/R^2 ~ A*M^(-2/3) at fixed A.
  OBSERVED f_Weyl ~ 0.45 MASS-INDEPENDENT -> requires the Weyl charge to scale A ~ M^(2/3). The brane
  eqs + regularity do NOT fix A (closure: A = bulk integration constant) -> neither the amplitude (0.46)
  NOR its mass-scaling (mass-independence) is derived; only the radial mode STRUCTURE is fixed.
PASS 4 / VERDICT: the regularity condition does NOT promote the amplitude. The cluster Weyl-DM IS the
  free bulk Weyl mode (geometry, not particles); its amplitude, mass-scaling (-> mass-independence),
  and turn-on are all closure/IC. CLOSURE CONFIRMED from the static-cluster face, consistent with the
  cosmological Gates 0-9 and the sacred-file framing (geometric DM at LCDM's Omega_c epistemic level).
SELF-AUDIT + RE-VERIFY: PASS1/2 solid; PASS3's f_Weyl~k^2 is exact (Poisson Laplacian), conclusion
  robust; numbers re-checked consistent. HONEST CAVEAT: this is an ANALYTIC/MODE solve (regular vs free
  mode + Poisson projection), NOT a full numerical 5D solve of a realistic extended cluster; but the
  closure result is a THEOREM (Koyama-Maartens) the mode solve confirms -- a numerical solve would not
  overturn 'amplitude = bulk integration constant'. The 'derived profile' is qualitative (mode structure).
**END OF THE GATE PROGRAM 0-24 on the Weyl-DM**: the brane DERIVES THE FORM (a0=cH/2pi, mu(x), the sinc
filter, mass-tracking not depth, the saturated transition, the radial mode structure); the BULK HOLDS
THE AMOUNT (the factor-2, the 5:1, the abundance) as its closure/IC datum. OBT reinterprets dark matter
as geometry and derives its laws; it does not derive its amount. Spirit (laws) is derived; body (amount)
is the bulk's own. The frontier is now completely mapped from every face. Quarantined; V8.2 unchanged.

## EXPLOITATION DU CISEAU LUMIÈRE-MATIÈRE — how to read the brane/bulk frontier (June 2026, Romain: "B, note these reflections, on y revient ensuite")
CONTEXT: Gate program 0-24 closed (brane derives the FORM, bulk holds the AMOUNT as its closure/IC datum).
Romain's intuition: light escapes the brane's TIME (zero proper time; under ARA the photon channel has W=1, it
does NOT average the 2 Gyr oscillation, unlike slowly-orbiting matter which has W<1 beyond the resonance band).
The lensing-vs-dynamics SCISSOR is the observable of the time(brane)/timeless(bulk) frontier. Question Romain
asked: how to exploit this CONCRETELY.

THE PRINCIPLE: the scissor (light un-averaged vs matter time-averaged) IS the instrument. Their DIFFERENCE is
the signal -- the only observable separating the time-regime (matter, which lives the oscillation) from the
timeless-regime (light, the channel closest to the timeless bulk).

EXPLOITATION A -- THE DISTINCTIVE TEST (concrete, doable now). On the same host, at radii where T_orb > T=2 Gyr
(~50-300 kpc): g_lens (light, full boost = blade A, ALREADY measured: Brouwer/KiDS +0.13 dex) vs g_dyn
(satellites/halo stars, time-averaged boost). OBT predicts g_lens > g_dyn. NEITHER MOND-constant (both full)
NOR LCDM (both follow the halo) gives this gap -> the signature no continuum can mimic. THE MISSING MEASUREMENT
= BLADE B: satellite-kinematics stacks (SDSS/DESI) around isolated hosts vs lensing stacks (KiDS) on matched
hosts. <<< ROMAIN CHOSE THIS ("B"), the next hunt, to RETURN TO LATER (not launched now).

EXPLOITATION B -- THE LENSING "WEYL-METER". The bulk holds the amplitude (factor-2, 5:1) as its IC datum
(Gate 24). Lensing, not averaging, measures the FULL Weyl -> lensing IS the direct readout of the bulk's
closure datum (the amount the brane cannot derive). Already done unnamed (Gate 18, CCCP).

EXPLOITATION C -- THE BRANE "PHASE-METER" (cosmic clock). Lens sees instantaneous, dynamics sees
retarded/averaged -> the scissor RATIO encodes the oscillation phase phi(t). Mapping scissor vs redshift
(Euclid lensing + DESI dynamics) = an independent dating of the brane. Harder (needs varied z), concrete in
principle.

UNIFIED VISION -- BULK TOMOGRAPHY BY PHOTONS. Photons are the timeless readout channel. OBT ALREADY has three
photon-observables, each reading a facet of the bulk: birefringence (beta=0.34 deg, Chern-Simons 5D -> v_bulk
drift/MOTION, card #23), the lensing scissor (Weyl AMPLITUDE), dark flow (brane INERTIA, card #23). Combining
them = a tomography of the bulk (its drift AND its Weyl) from the channels that escape the brane's time.

BORDERS (honest, not to overclaim): NOT "see the future" -- light escapes the AVERAGING, not time itself; NOT a
tabletop gadget -- gravitational, macroscopic, the "Weyl-meter" is a telescope. The only LOCAL avenue OBT offers
(5D Geometric Bypass + Penrose-Diosi collapse at 0.2 um, laboratory.md) is a SEPARATE story at scale L.

NEXT STEP WHEN WE RETURN = BLADE B: harvest satellite-kinematics stacks (SDSS/DESI) at 50-300 kpc, confront
quantitatively to blade A lensing on matched hosts. If g_lens > g_dyn emerges at large radii -> the 5th
OBT-distinctive family and the most profound: the direct measure of the brane/bulk frontier. Whether this
becomes an OBT-Game card (external debunk: "lensing and dynamics must agree" = the implicit MOND/LCDM premise)
or a reviewer-side prediction is to be decided when we return. NOT launched now per Romain.

## BLADE B — lensing-vs-dynamics SCISSOR, dynamics side: strong ciseau REFUTED, the boost does not extinguish (June 2026, reviewer mode, quarantined)
Romain: "go la lame B". Executed on the only hosts with resolved satellite orbits at r>>crossover:
MW + M31 (McConnachie 2012, galactocentric D(MW)/V(MW), D(M31)/V(M31)). Script: explorations/bladeB_satellites.py.
SETUP: ciseau => light (lensing) keeps the full boost W=1; SLOW tracers (T_orb>T) average -> W=ARA|sinc|<1;
the STRONG ciseau => distant-satellite dynamics COLLAPSE toward Newtonian while lensing stays full MOND.
Crossover (T_kappa=T_orb/sqrt2=T) at ~81 kpc (MW), ~102 kpc (M31). sigma_los=FAC*Vcirc, FAC=1/sqrt3
(isotropic gamma=3), VALIDATED on the MW inner (sigma=98 vs MOND 102, W_inner=0.88 ~ full boost as ARA predicts).
RESULT (W_dyn = the a0-boost the slow tracers feel; lensing=1; deep-MOND ciseau = -0.25*log10(W_dyn)):
 - MW  OUTER (N=12, <r>=152 kpc): W_dyn=0.24 [0.10,0.49]. Newton (W=0) excluded +3.5s; -2.2s below full MOND.
 - M31 OUTER (N=16, <r>=182 kpc, the CLEANER host): W_dyn=0.70 [0.38,1.19] = consistent with FULL MOND (-0.7s);
   Newton excluded +4.9s. (M31 inner W=0.12 is a corrupted N=5 bin w/ M32 stripped-cE -> ignored.)
 - bare-sinc ARA predicts W~0.06-0.11 (extinction) at these radii -> DISFAVORED by both hosts.
VERDICT: the STRONG ciseau (Newtonian collapse) is REFUTED (3.5-4.9 sigma). The MOND boost is RETAINED out to
150-260 kpc. The MW's lower W~0.24 is most plausibly its co-rotating satellite plane (card #13: tangential beta
lowers sigma_r), so M31 is the trustworthy host -> ~full MOND -> NO detectable ciseau. Combined robust bound
W_dyn >~ 0.3 -> any ciseau <= ~0.13 dex. The blade-B "satellite ciseau" delivers NO new distinctive signal;
it BOUNDS the ciseau to the band-scale.
DEEPER FINDING: the boost does NOT sinc-extinguish at long period (W~0.3-0.7 at T_kappa~3-6 Gyr, NOT ~0). The
bare sinc over-predicts the suppression by ~3-7x -> the suppression SATURATES (a0 has a substantial DC floor;
orbital averaging only strips the small oscillating part).
IMPLICATION (flagged for Romain, NOT acted on -- touches sacred theory.md): this is in TENSION with the
ARA/theory.md statement "cluster bulk T_r 3-6 Gyr is sinc-EXTINCT" (the SAME period range where galaxy satellites
show W~0.3-0.7, not 0), but is CONSISTENT with Gate 13 (the cluster Weyl-DM is MASS/well-depth driven, NOT
sinc-driven; sinc inactive where Weyl dominates). Coherent picture: sinc = a MILD galaxy-band dip only
(cards #29/#30, -0.068 dex); the cluster factor-2 is the Weyl (closure IC, Gates 13-24, mass-driven). The
lensing-vs-dynamics ciseau is real but MODERATE (band-scale ~0.07 dex), not a strong collapse.
CAVEATS: N~12-16/host, anisotropy systematic (MW plane), 2 hosts only, eccentric-orbit T_int approximate,
high-velocity members (Leo I; And XII/XIV) only mildly inflate (2.5sig-clip changes nothing). NEXT sharper test
(if wanted): SPARC circular-orbit dynamics RAR (ARA T_kappa applies cleanly) vs Brouwer lensing RAR at matched
g_bar -> pin the band ciseau with high statistics.
