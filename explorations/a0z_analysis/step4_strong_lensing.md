# Step 4 — the strong-lensing a0(z) lever (the amplifier's lead), computed and CLOSED

**Status: quarantined reviewer-mode analysis (July 2026). Script: `slacs_a0z.py` (deterministic, identities-only
asserts, output reproducible). Data: CDS J/ApJ/705/1099 (Auger+ 2009, SLACS IX), local cache, byte-parsed per the
ReadMe; 70/85 grade-A lenses with complete fields. Not a sacred file, not in the PDF.**

## What was tested

The AI-amplifier lead (`amplifier_a0z.py`, June 2026): *SLACS/BELLS/SL2S strong lensing = a NON-kinematic a0(z)
probe (no V_c 4x lever) on samples already spanning z~0.1-0.8 → maybe the missing cross-lever NOW, not
Euclid-future.* Its own flagged caveat: the g~a0 regime selection. This step decides by calculation.

## The four results

1. **THE REGIME THEOREM (structural, exact).** At the Einstein radius of any circularly-symmetric lens,
   `g(R_E) = G M_E/R_E² = π G Σ_cr(z_l, z_s)` — because `M_E = π R_E² Σ_cr` *defines* R_E. The acceleration at
   θ_E is a constant of the (z_l, z_s) **geometry**, independent of the lens: **a lower-mass lens shrinks R_E, it
   does not lower g_E.** Grid scan: the absolute floor is x_E = g_E/a0 ≈ 2.8 (at the z_l=2 grid edge; ≈ 3.3 for
   real samples z_l ≤ 1). **The "g~a0 subset" the lead hoped for cannot exist at θ_E in strong lensing.** SLACS
   empirically sits at x_E ≈ 10–23 (median 15); the paper's own M(<R_E) reproduces π R_E² Σ_cr to 0.2 %
   (parsing/cosmology validation).

2. **THE LEAD'S KERNEL WAS RIGHT (projection resurrects deep-MOND).** The naive local sensitivity at x~15 is
   1/(2x²) ≈ 0.2 %. But the lensing mass is a **cylinder**: the line of sight crosses the outer deep-MOND phantom.
   Forward model (Hernquist M*_Salpeter at R_eff → OBT exact RAR → projected Σ → M_2D(<R_E)): the projected
   phantom is **~7 % of M_E** (5–95 %: 3.6–12.7 %) and the direct sensitivity is **d ln M_E/d ln a0 = 0.067 =
   ×16 the naive local**. (Context: matching SLACS' observed lensing masses under const-a0 needs
   M* ≈ +0.08 dex over Salpeter — the known high-g IMF degeneracy; EFE/L_max truncation checked at 0.1 %.)

3. **BUT THE SIGNAL IS TOO SMALL FOR THE FLOORS.** The a0(z)=A0·E(z)/E(z_med) vs a0=A0 differential across
   SLACS: **slope +0.0246 dex/z** (span 0.013 dex over z_l 0.06–0.51).
   - *Statistical floor (M\*-leg):* per-lens e_logM* = 0.08 dex, N=70, std(z)=0.09 → σ_slope = 0.105 dex/z →
     **the signal is 0.23 σ in SLACS. Statistically dead now** (needs ×13 for 3σ).
   - *Coherent-systematics wall:* an IMF/M\*-L z-drift mimics the signal 1:1; the literature-debated drift class
     (0.05–0.1 dex/z) sits a **factor 2–4 above** the signal.
   - *IMF-free σ-leg* (isotropic Jeans at matched M_E, aperture R_eff/2): Δσ/σ slope = −1.7 %/z → 0.20 σ;
     few-% coherent anisotropy/profile systematics sit ~2× above. Same wall, different clothes.

4. **EUCLID-N (~1e5 strong lenses):** statistics heal (σ_slope → 0.001 dex/z → ~28 σ reachable), the coherent
   wall does not: the signal at the Euclid range is ~0.028 dex/z vs the 0.05–0.1 dex/z IMF-drift class = a factor
   1.8–3.6 above. **The route becomes an IMF-systematics race (a ~2–4× control improvement needed), not a free
   measurement.**

## Verdict

- The lead's **"doable NOW" claim is refuted**: 0.2 σ in SLACS, and the g~a0 subset is impossible by theorem.
- The lead's **physics kernel was right and is now quantified**: projection resurrects ×16 the naive a0-leverage
  (worth knowing — it is why the route is merely *hard*, not *absurd*).
- At Euclid-N the strong-lensing route is a **systematics race** (factor 2–4 IMF control), not a clean lever.
- **The decisive clean cross-lever remains the WEAK-lensing RAR a0(z)** (Euclid/Rubin, `euclid_case.md`) —
  exactly step 2's conclusion, now with the strong-lensing loophole closed by numbers.

## Honest limits of this step

- SLACS-only (BELLS absent from Vizier; SL2S-IV lacks per-lens z_s there): the z-lever tested is 0.06–0.51.
  Extending to z~0.8 changes the slope only mildly (d lnE/dz grows 0.53→0.60); the verdict cannot flip.
- Spherical Hernquist stars (SLACS is ~80 % elliptical), isotropic Jeans, R_eff/2 aperture convention: all
  declared; they touch the *differential* signal only at second order.
- The 0.05–0.1 dex/z IMF-drift "class" is a literature-debate bracket, not a measurement — the verdict's
  systematics ratio is a factor-2-class statement, honestly labeled.
