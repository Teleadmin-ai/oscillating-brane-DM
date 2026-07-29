# The cluster lensing-vs-dynamics scissor, and an audit of the whole arcs chain

**Reviewer mode.** Romain: *« creuse le ciseau lentillage-vs-dynamique sur les amas »* and *« et
verify tes calculs et tes script »*. Scripts: `scissor_clusters.py`, `verify_arcs_chain.py`
(quarantined, not sacred, not in the PDF).

---

## Part 1 — The audit (`verify_arcs_chain.py`)

Every load-bearing number of `arcs_obt.py`, `arcs_battery.py`, `alpha_nt_budget.py` and
`card22_lensing_refit.py` was re-derived by an independent route.

| check | what it tests | result |
|---|---|---|
| V1 | X-COP bin correspondence (T_X/KT must be constant) | **PASS** — 0% scatter for most clusters, worst 5.9% |
| V2 | Merten Table 6 (ρ_s, r_s) regenerates Table 7 (M200c, c200c) | **PASS** — M200 ratio 1.01 ± 0.08, c200 0.99 ± 0.03 → my h-convention is confirmed |
| V3 | two independent CLASH lensing analyses at matched radii | **DATA FINDING** (below) |
| V4 | the numeric 3D→2D projection path vs the analytic NFW formula | **PASS** — worst 0.65% |
| V5 | distances and Σ_cr vs `astropy.cosmology` | **PASS** — 0.003% |
| V6 | the α_NT hydrostatic algebra vs direct numerical differentiation | **PASS** — exact |
| V7 | the M-T bridge re-fitted from X-COP's own data | **PASS** — normalisation ratio 0.82 vs the note's 0.87 |
| V8 | rar_obt inverts μ(x) = x/√(1+x²) | **PASS** — 2×10⁻¹⁶ |
| V9 | impact of V3 on the re-fit | verdict **robust** |

**No code bug was found.** V4 matters most: κ_OBT comes from the numeric path and κ_NFW from the
analytic formula, so a bias there would have manufactured the "OBT-proper deficit" out of nothing.
It is good to 0.65%.

**V3 is a genuine data finding, and it closes the arc question.** The Merten SaWLens NFW and the
Umetsu/Zitrin M2D are two independent lensing analyses of the same nine clusters. Their ratio at
matched projected radii:

| 10″ | 20″ | 30″ | 40″ | at the arc radius |
|---|---|---|---|---|
| 0.70 | 0.81 | 0.89 | 0.91 | **0.80** |

The smooth spherical NFW under-represents the projected core mass of the 2D models by ~30% at 10″,
healing to ~10% at 40″ — exactly the ellipticity + substructure + BCG content the 2D models carry
and no single spherical NFW can. Consequence: κ_NFW(θ_E) = 0.79 × 1/0.80 = **0.99 ≈ 1**. The arc
deficit that started the whole monster is now explained *internally by the data*, not merely by a
cited simulation budget. The downgrade verdict is confirmed, and V9 shows it survives correcting
for the effect (OBT-proper stays ≈ 0.9).

**One flag, not a failure:** X-COP's own M500–T slope is 1.35 where the note used the Arnaud-class
1.71. The normalisations at 5 keV agree (ratio 0.82 vs the 0.87 used), and re-deriving the anchor
gap cluster-by-cluster with X-COP's own relation gives 0.74 against the note's 0.75 — so the note's
single-factor de-biasing was adequate. The slope difference means the bridge factor is mildly
temperature-dependent; it does not move the conclusion.

---

## Part 2 — The scissor (`scissor_clusters.py`)

### The mechanism, and why it is not free

Under ARA the oscillating MOND scale is averaged by the **tracer**, not by the field. Photons average
nothing. So for one cluster:

    M_lens(r) = [ g_MOND(g_bar, a₀)      + g_Weyl ] r²/G      (photons, W = 1)
    M_dyn(r)  = [ g_MOND(g_bar, W(r) a₀) + g_Weyl ] r²/G      (gas / galaxies, W < 1)

X-ray masses **must** come out below lensing masses, with the deficit **rising outward** and
**vanishing at galaxy-disc scales** (adiabatic there). Sign, radial shape and scale ladder all match
what is observed. OBT therefore offers a mechanism for the hydrostatic mass bias at no extra cost.

### But it is bounded — the result of this dig

Write a₀(t) = a₀₀[1 + ε s(t)], s ∈ [−1,1], ⟨s⟩ = 0, ⟨s²⟩ = ½. A slow tracer feels √⟨a₀²⟩; photons and
adiabatic tracers feel the instantaneous value. Then

    W = √(1 + ε²/2) / (1 + ε s_now)

| ε | W (at peak) | b at R500 |
|---|---|---|
| 0.10 | 0.911 | 0.018 |
| 0.50 | 0.707 | 0.065 |
| 1.00 | 0.612 | 0.088 |

**Over the whole physical range ε ∈ [0,1], at the most favourable phase, W cannot fall below 0.612
→ the cluster bias is capped at b ≤ 0.09, i.e. (1−b) ≥ 0.91.** Against the measured 0.75 (this
work), 0.76 (CCCP), 0.69 (WtG), 0.58 (Planck), the scissor covers about **a third of the smallest
of them and none of the largest**. OBT explains part of the hydrostatic bias; it does not explain it
away.

Two structural reasons the cap is low: at R500 the Weyl carries ~58% of the total and is
**channel-independent**, so the scissor only acts on the MOND remainder; and in the deep-MOND regime
the boost goes as √(W a₀ g_bar), so a factor W in a₀ costs only √W.

### Three things this exposes

**1. The sinc is not merely un-audited — it is out of range.** Card #22's window reaches W ≈ 0.11 at
R500, *below the 0.612 floor that any bounded positive a₀ oscillation can produce*. It matches the
measured bias precisely **because** it exceeds what the theory can supply. That is a critique of the
card's fitted window, not a success of the theory.

**2. The modulation depth ε is an underived input.** The sinc machinery implicitly takes ε = 1 (a₀
swinging to zero every 2 Gyr). OBT's own motor amplitude is f_osc = 0.10, which would give b ≈ 0.02 —
a scissor of essentially nothing. Nothing in V8.2 fixes ε, and the entire ARA cluster phenomenology
scales with it. **This is the load-bearing unproven input of the ARA sector**, and it deserves the
same flag the growth-sign bit carries.

**3. The sign is phase-dependent.** For s_now < 0 (currently below the mean of the oscillation) W > 1
and the scissor **reverses** — dynamics would exceed lensing. The observed sign therefore constrains
where we sit in the cycle: a chronology statement to be checked against OBT's own phase-0.9
anchoring, not assumed.

### Card #22's window re-run — the "pending" flag now has a number

CLAUDE.md has carried *"the fit used bare-sinc g1, re-run with mild g1 pending"* since June.
Executed:

| window | f_W | r_c / R500 | χ²/N |
|---|---|---|---|
| \|sinc\| (as coded) | 0.73 | 0.039 | 48.5 |
| **bounded (audit, ε=1)** | **0.57** | **0.031** | **45.1** |
| W = 1 (no averaging) | 0.54 | 0.030 | 44.6 |

The bounded window moves the Weyl amplitude by −22% **and fits X-COP better** (χ²/N 45.1 vs 48.5).
The card's *debunk* (two OBT scales beating a four-parameter ad-hoc form, Weyl-dominated) is
unaffected in kind; its published *numbers* were window-locked, and this is the size of the lock.

### The two threads converge on one number

The bounded-window X-COP fit gives f_W = 0.57 and the CLASH lensing fit gives f_W = 0.59 — nearly
identical — but they are normalised to mass scales that differ by ×1.34, so in **absolute** Weyl the
lensing channel still wants ~×1.4 more. The scissor supplies at most ×1.1 of that. **The residual is
precisely the unexplained factor the α_NT note priced.** Both threads of this session land on the
same missing ×1.3.

### Named falsifiers

1. A hydrostatic bias that is strongly **mass-dependent at fixed overdensity** kills the ARA reading
   — at fixed Δ, t_dyn is mass-independent (proved analytically and numerically), so the ARA bias
   must be too.
2. A bias that **vanishes at large radius** kills it: the window only opens outward.
3. A lensing-vs-dynamics discrepancy at **galaxy-disc** scales kills it: adiabatic there, prediction
   exactly zero.
4. **BLADE B, the clean positive test:** satellite kinematics vs galaxy-galaxy lensing at 100–250
   kpc, where the Weyl fraction is small and the MOND term carries the signal. Predicted deficit at
   the cap: a few to ~15% in g (≤ 0.07 dex). A null there at that precision closes the mechanism.

### Scope

Spherical; one fiducial cluster shape; the Weyl held at the card's globals; gas from a
universal-closure model; the a₀(t) waveform taken as a bounded sinusoid (its true shape is not
derived in V8.2); ⟨g(a₀²)⟩ approximated by g(⟨a₀²⟩), the theory's own declared treatment, which
carries a second-order Jensen residual at large ε; the measured biases are declared literature
values, not re-derived here, except this work's 0.75.

### One item for Romain's decision

The theory files already carry the audit-corrected *"mild W ~ 0.7"* statement, which this
computation **confirms** (0.707 is exactly the ε ≥ 0.5 saturation). What they do **not** carry is
that the ARA amplitude scales with an **underived modulation depth ε**, and that the whole cluster
sinc phenomenology is bounded by it. Whether to add that caveat to theory.md's Dynamic-Averaging
section is a sacred-file decision, i.e. yours.
