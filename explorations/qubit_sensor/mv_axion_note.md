# A μeV string-axion target with an f_a-invariant effective coupling, inside the FLASH band

**A falsifiable prediction offered to the axion dark-matter community**
Romain Provencal (independent researcher, provencal.romain@teleadmin.net), with AI theoretical
co-processors (Claude/Anthropic, Gemini DeepThink/Google) — radically transparent collaboration model.
July 2026. Repository: https://github.com/Teleadmin-ai/oscillating-brane-DM (all supporting calculations
are runnable scripts, referenced inline).

---

## 0. Status and provenance (read first)

This note comes from **Oscillating Brane Theory (OBT)**, an independent-researcher braneworld cosmology
(the universe as a 4D membrane oscillating in a 5D AdS bulk; arXiv-unpublished, not peer-reviewed;
full document and validation suite on the repository site, https://higgs-cosmology.com/). The axion
chain below is part of its **quarantined V9.0 exploration layer** — it is *not* claimed with the
confidence of the framework's core phenomenology, and this note's epistemic posture is deliberately
modest: **we present one concrete, falsifiable coordinate in open parameter space, with its complete
derivation chain and every assumption listed.** The community can price the theory however it likes;
the coordinate is cheap to test and the falsification statement is clean either way.

**The target in one line:** a string ALP at the μeV scale (ν ≈ 242 MHz central, order-of-magnitude
bracket ~0.3–3 μeV) whose **density-weighted haloscope coupling is pinned, independently of its decay
constant, at g_eff ≈ 1.0 × 10⁻¹⁶ · C·θᵢ GeV⁻¹** — grazing the declared FLASH phase-1 sensitivity and
a factor ~5 above its phase-2 goal.

## 1. The derivation chain (each step = a runnable script)

1. **The scale.** OBT's UV completion is a Klebanov–Strassler / LVS type-IIB compactification whose
   flux integers (K=21, M=10, g_s=0.1) reproduce, top-down and with no fine-tuning, the brane tension
   τ₀^{1/3} = 257 MeV ≈ Λ_QCD that the cosmological fit independently requires (bottom-up/top-down
   convergence). The resulting LVS spectrum (V8.2 core, `theory.md`) contains the string
   scale **M_s = M_Pl/√V = 1.19 × 10¹² GeV** (volume V ≈ 4 × 10¹²) and an **ultra-light modulus at
   m_V ~ 10⁻⁶ eV** (order-of-magnitude). This μeV scale predates the axion chain; it was not tuned
   toward any experiment.
2. **The identification** (`mv_coupling.py`): the μeV mode is identified as the **imaginary (axion)
   partner of a blow-up/fibre Kähler modulus** — shift symmetry ⇒ ultra-light, **derivative couplings
   only** (no static fifth force, evading EP/Cassini bounds), photon coupling
   **g_aγγ = (α/2π)·C/f_a** with C = O(1) unknown anomaly coefficient.
3. **The decay constant is not free** (`mv_fa_lvs.py`): the LVS axiverse (Cicoli–Goodsell–Ringwald 2012)
   brackets f_a ∈ [~10¹⁰, ~10¹³] GeV; a blow-up/fibre axion sits naturally at **f_a ~ M_s ≈ 1.2 × 10¹²
   GeV → g_aγγ ≈ 9.8 × 10⁻¹⁶ C GeV⁻¹**.
4. **The relic abundance** (`mv_abundance.py`, standard misalignment): the field oscillates early
   (T_osc ≈ 16 GeV, above the QCD scale), giving
   **Ω_a h² ≈ 1.2 × 10⁻³ (f_a/M_s)² θᵢ² — i.e. ~1 % of the dark matter at the natural point**, rising
   to **100 % at f_a ≈ 1.2 × 10¹³ GeV** (the LVS high end; over-closure forbids larger f_a at θᵢ~1).
   In OBT the *dominant* dark matter is geometric (a projected-Weyl braneworld effect), so a
   sub-dominant axion is internally consistent, and the ~1 % fraction suppresses axion-CDM
   isocurvature by ~10⁻⁴ — safe for a wide range of inflation scales (full-DM corner: isocurvature
   pushes toward low-scale inflation).

## 2. The main result: the f_a-invariant effective coupling (`mv_effective_coupling.py`)

A haloscope measures the power g²ρ_a, i.e. the **effective coupling g_eff = g·√(Ω_a/Ω_DM)** (assuming
the axion fraction clusters like the bulk DM). In this chain g ∝ 1/f_a while Ω_a ∝ f_a² — because the
string-ALP mass is instanton-set, *independent of f_a* (unlike the QCD axion) — so **the f_a dependence
cancels exactly below saturation**:

> **g_eff = (α/2π) · C·θᵢ / f_a,DM = 9.8 × 10⁻¹⁷ · C·θᵢ GeV⁻¹**  (f_a,DM = 1.2 × 10¹³ GeV)

verified numerically to 10⁻⁹ across the three-decade LVS bracket. **The apparent f_a uncertainty
(1 %–100 % dark-matter fraction) does not propagate to the experiment: every point of the bracket
presents the same haloscope target.** The residual theory spread is the honest O(1) pair C·θᵢ and the
order-of-magnitude on the μeV mass itself.

## 3. Where the target sits

| m_a (μeV) | ν (MHz) | g_KSVZ (GeV⁻¹) | g_DFSZ | OBT g_eff (C·θᵢ=1) |
|---|---|---|---|---|
| 0.30 | 73 | 1.2×10⁻¹⁶ | 4.6×10⁻¹⁷ | 9.8×10⁻¹⁷ |
| 0.64 | 155 | 2.5×10⁻¹⁶ | 9.8×10⁻¹⁷ | 9.8×10⁻¹⁷ |
| 1.00 | 242 | 3.9×10⁻¹⁶ | 1.5×10⁻¹⁶ | 9.8×10⁻¹⁷ |
| 1.49 | 360 | 5.8×10⁻¹⁶ | 2.3×10⁻¹⁶ | 9.8×10⁻¹⁷ |
| 3.00 | 725 | 1.2×10⁻¹⁵ | 4.6×10⁻¹⁶ | 9.8×10⁻¹⁷ |

- The flat OBT floor **crosses the QCD band inside the target decade** (above DFSZ below 0.64 μeV,
  above KSVZ below 0.25 μeV). It is a *string ALP near, not on, the QCD relation*: the QCD-axion mass
  at f_a = M_s would be 4.8 μeV, within ~5× of m_V.
- **Helioscopes/astro:** CAST (6.6 × 10⁻¹¹) constrains g, not g_eff; the *entire* bracket sits ≥ 2.8
  orders below it (the natural corner 4.8 orders). The window is genuinely open.
- **Quantum-hardware aside:** we computed (script `axion_photonic_chip.py`) that photonic-chip class
  quantum processors *cannot* see this field (16–18 orders short; optical-cavity storage caps ~60×);
  μeV axions are resonant microwave-cavity + magnet territory — this note's target is for haloscopes.

## 4. The experimental match — FLASH, and the μeV-decade program

The proposed **FLASH** haloscope (FINUDA magnet, Frascati; arXiv:2309.00351) is declared for
**100–300 MHz (QCD-axion masses 0.49–1.49 μeV)** — the OBT central target (242 MHz) sits **inside**
that band:

- FLASH **phase 1** (microstrip SQUID, DFSZ-class ~1 × 10⁻¹⁶ GeV⁻¹): the OBT floor is **0.98× that
  depth** — phase 1 *grazes the whole target*.
- FLASH **phase 2** (100 mK, ~2 × 10⁻¹⁷): cuts a factor **~5 below** the floor — decisive for the
  entire f_a bracket at C·θᵢ = O(1).
- The wings of the mass bracket (0.3–0.5 and 1.5–3 μeV → 73–120 and 360–725 MHz) fall to the
  neighboring programs (lumped-element/DM-Radio-class below; the historic and next-generation
  cavity program above, where reaching the floor means DFSZ/2 to DFSZ/5 depth). Qubit single-photon
  counting (Dixit et al., PRL 126, 141302 (2021)) is the readout class that accelerates such scans.

## 5. Falsifiability (declared before any data)

- **Exclusion:** a scan of the ~0.3–3 μeV decade at g_eff ≲ 1 × 10⁻¹⁷ GeV⁻¹ (≈ floor/10) **kills the
  entire misalignment chain at O(1) angles** — the OBT axion bone dies cleanly (the theory's core is
  separate; this is the falsification of its one derived direct-detection channel). FLASH phase 2
  alone already bites the central half-decade at floor/5.
- **Detection:** a signal at μeV masses with g_eff within ~×3 of 10⁻¹⁶ GeV⁻¹ matches the chain;
  the OBT-vs-QCD-axion discriminant is then the (m, g) position relative to the QCD relation
  (the flat floor is mass-independent; the QCD band scales g ∝ m — distinguishable away from the
  0.25–0.64 μeV crossings). A detection *on* the QCD relation would remain ambiguous — we state
  this plainly.
- **What we will not do:** claim support from a null that only grazes the floor, or dress an anomaly
  elsewhere as this field. (Our own quantum-hardware protocol pre-registers the same discipline.)

## 6. Honest gates (all open, all stated)

1. **Axion-vs-saxion identification** of the μeV LVS mode (the chain's weakest link; the saxion
   partner is heavier, but the identification is an assumption, not a derivation).
2. **The μeV mass itself is order-of-magnitude** (an LVS spectrum scale, not a sharp prediction) —
   hence the decade-wide mass bracket.
3. **C and θᵢ are O(1) unknowns** (the floor scales linearly in each).
4. **Invariance assumptions:** m_a independent of f_a (string ALP); standard misalignment, no
   post-T_osc entropy injection; below over-closure saturation; local axion fraction ∝ bulk fraction.
5. f_a ~ M_s natural within a factor ~O(10) (2π's, volume suppressions) — *absorbed* by the invariance
   for g_eff, but relevant to the raw g if a density-independent probe is used.

## 7. Supporting calculations (all in the repository, runnable)

`explorations/qubit_sensor/`: `mv_coupling.py` (identification + g), `mv_abundance.py` (T_osc, Ω_a h²,
isocurvature trade-off), `mv_fa_lvs.py` (the LVS f_a bracket), `mv_effective_coupling.py` (the
f_a-invariance, QCD-band crossings, FLASH/CAST margins), `chi_alp_sensitivity.py` (why the qubit/
quantum-sensor mass window selects this mode), `axion_photonic_chip.py` (why photonic chips cannot
see it). Core-framework scales (M_s, LVS spectrum): `theory.md` on the repository.

## References

- Balasubramanian, Berglund, Conlon, Quevedo, *JHEP* 03 (2005) 007 (LVS).
- Cicoli, Goodsell, Ringwald, *JHEP* 10 (2012) 146 (the LVS axiverse; decay constants).
- Preskill, Wise, Wilczek; Abbott, Sikivie; Dine, Fischler, *Phys. Lett. B* 120 (1983) (misalignment).
- Sikivie, *PRL* 51, 1415 (1983) (haloscope).
- Gorghetto, Villadoro, *JHEP* 03 (2019) 033 (m_a–f_a, QCD).
- Alesini et al., arXiv:2309.00351 (FLASH: 100–300 MHz, DFSZ-class phases).
- ADMX Collaboration, *PRL* 120, 151301 (2018); *PRL* 127, 261803 (2021) (μeV-decade cavity program).
- Dixit et al., *PRL* 126, 141302 (2021) (qubit single-photon counting for axion DM).
- CAST Collaboration, *Nature Physics* 13, 584 (2017) (helioscope bound).

*Scope note: this proposal detects (or excludes) a light bulk-sector field of the theory. It is one of
OBT's three falsifiable near-term "bones" (with the evolving MOND scale a₀(z) = cH(z)/2π for
Euclid/Rubin, and a 5D-enhanced Penrose–Diósi collapse size-scan for levitated optomechanics).*
