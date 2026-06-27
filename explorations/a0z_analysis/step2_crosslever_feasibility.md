# Step 2 — the cross-lever test on real data: feasibility + the low-z first blade (June 2026)

Reviewer mode. Romain's option 2 was "build the cross-lever test (lensing-a0 vs kinematic-a0) on existing
data." Step 3 already flagged that all current a0(z) confirmations are KINEMATIC. Step 2 checks whether the
lensing leg can be supplied now — and the honest answer is **no, the decisive (high-z) leg is genuinely future**,
but the existing low-z data give a clean first blade.

## Data inventory for the cross-lever

| leg | lever | data that exists | z-range | status |
|---|---|---|---|---|
| **kinematic** a0(z) | V_c **4×** | MUSE-DARK III, KROSS (Hα) | z ~ 0.3–1.4 | EXISTS (the ×1.5) |
| **lensing** a0(z) | g_obs **2×**, no V_c | Brouwer+2021 KiDS-1000 RAR (the ONLY weak-lensing RAR) | lens ⟨z⟩ ~ 0.2 (0.1–0.5) | **adopts a0=1.2, does NOT fit a0 independently; no a0(z)** |

The decisive cross-lever needs lensing-a0 **and** kinematic-a0 at **matched high z** (where a0 evolves and the
4×-vs-2× lever difference bites). The lensing leg there **does not exist**: Brouwer is low-z and fixes a0 to the
SPARC value rather than measuring it. So **the cross-lever cannot be run on current data** — it is an Euclid (and
Rubin) measurement (z ~ 0.3–1.5 lensing RAR in z-bins), ≲2027.

## The one blade available now: the low-z method offset

At low z both methods exist: Brouwer's **lensing** RAR (⟨z⟩~0.2) is consistent with the **same** a0 ~ 1.2×10⁻¹⁰
that the **kinematic** SPARC RAR gives at z~0 (Brouwer adopt it and find "good agreement with the MG
predictions"). So the **lensing-vs-kinematic method offset is consistent with ZERO at low z**. Consequence: the
cross-lever has **no zero-point offset to subtract** — a high-z lensing-vs-kinematic *split*, when Euclid
measures it, would be a clean signature of the high-z V_c systematic (the 4× lever), not a method artifact.
(This is the z=0 anchor of the lensing-vs-dynamics "scissor"; the high-z blade is the future measurement.)

## What Euclid delivers (forecast, hardened_forecast.py)

Euclid lensing RAR over z~0.3–1.5 reaches σ(a0)/a0 ~ 1–2% per z-bin → σ_alpha ~ 0.02 (evolution decisive). The
**crucial** point is not the precision but the **lever**: the lensing a0(z) rides g_obs (2×, lensing 2-halo/IA
systematics), NOT V_c (4×, beam/AD/inclination). So lensing-a0(z) vs kinematic-a0(z):
- both ~1.5 and robust to gas → **rate REAL** → OBT cH(z)/2π refuted (evolution survives);
- kinematic ~1.5 but lensing ~1.0 → the **V_c systematic** was inflating the kinematic → OBT rate safe;
- both ~1.0 → OBT cH(z)/2π **confirmed**.

## Step-2 verdict (honest)
The cross-lever is the right decisive test and, from the low-z blade, it will be **clean** (zero method offset
at z=0). But it **cannot be run on existing data** — the high-z lensing-a0(z) leg does not exist (Brouwer is
low-z and adopts a0). So step 2's real output is a **feasibility + roadmap result**, not a cross-lever result:
the pépite's rate-deciding measurement is **Euclid/Rubin lensing-a0(z) in z-bins** (matched to MUSE/JWST
kinematic-a0(z), + ALMA gas). Near-term "play" = advocate/design exactly that, not squeeze a result from data
that cannot give one. This is the data-reality answer to "build the cross-lever now": you can't yet — and that
is itself the sharpest statement of where the pépite stands.

Sources: Brouwer et al. 2021, A&A 650, A113 (arXiv:2106.11677); McGaugh, Lelli & Schombert 2016 (SPARC a0=1.2);
MUSE-DARK III arXiv:2604.22613; KROSS Harrison 2017; Übler 2017 ApJ 842,121. See step3_real_papers.md.
