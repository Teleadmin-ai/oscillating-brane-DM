# The Euclid case for $a_0(z)$ — the decisive test of OBT's one distinctive prediction

*Reviewer/webmaster mode, cool head. This is the argumentaire for the single near-term measurement that decides
OBT's distinctive lever. It is built on the audited honest scope (steps 1→3→2 + anchor dig): the EVOLUTION is
robust and Euclid-decisive; the RATE is systematics-limited and needs the cross-lever; OBT claims the FORM
$a_0\propto H(z)$ and the evolution, not the $a_0$ coefficient.*

## 1. The claim, in one line
OBT derives the MOND acceleration scale from the cosmic horizon, so it must **evolve**:
$$a_0(z) = \frac{cH(z)}{2\pi} = a_0(0)\,E(z),\qquad E(z)=\sqrt{\Omega_m(1+z)^3+\Omega_\Lambda}\ \ (E(1)=1.76,\ E(2)=2.97).$$
**Milgrom's standard MOND takes $a_0$ to be a universal constant.** A measured evolution of $a_0$ with redshift
falsifies constant-$a_0$ MOND and is the unique, currently-near-testable signature separating OBT from it.

## 2. Why this is THE test (and not another consistency check)
Of OBT's signatures, $a_0(z)$ is the only one that is simultaneously **distinctive** (not shared with $\Lambda$CDM
*or* constant-MOND), **already hinted** (three datasets: $a_0$ roughly doubles by $z\sim1$ — MUSE-DARK III RAR,
Übler+2017 BTFR zero-point, KROSS), and **near-term decisive** (Euclid). Audited honest status:
- the **evolution** ($a_0\neq$ const) is robust;
- the **rate** ($cH(z)/2\pi$ vs the observed $\sim1.5\times$-faster) is **undetermined** — the three current hints
  are all **kinematic** (rotation/dispersion), so they share the $V_c^4$ "4× lever" ($a_0=V_c^4/GM_{\rm bar}$) and a
  shared high-$z$ velocity/baryonic systematic inflates them identically. A coherent $\sim10\%$ $V_c$ bias alone
  fakes the $1.5\times$. So the rate needs an **orthogonal-lever** measurement.

## 3. What Euclid uniquely provides — the lensing leg (the orthogonal lever)
- Euclid Wide Survey: $\sim14{,}000$ deg², shapes of $\sim1.5\times10^9$ galaxies, weak lensing to $z\sim2$;
  **DR1-Foundation Nov 2026, weak-lensing products mid-2027** (ESA Euclid DR1 timeline).
- The **weak-lensing RAR** measures $g_{\rm obs}$ from the excess surface density $\Delta\Sigma$ around lens
  galaxies — **no $V_c$**. Its systematic lever is $g_{\rm obs}$ (2×; 2-halo / intrinsic-alignment / photo-z),
  *orthogonal* to the kinematic $V_c$ (4×; beam-smearing / asymmetric-drift / inclination). Proof of concept:
  Brouwer et al. 2021 measured the lensing RAR with KiDS-1000 two decades below $a_0$ (lens $\langle z\rangle\sim0.2$).
- **Euclid extends this to redshift bins to $z\sim1.5$ with $\gg$KiDS statistics → the first $a_0(z)$ from lensing.**
- The **joint kinematic + weak-lensing RAR method already exists** (e.g. arXiv:2310.15248) — the cross-lever is
  methodologically ready; Euclid supplies the high-$z$ lensing leg it currently lacks.

## 4. The measurement design (the cross-lever)
1. **Euclid lensing-$a_0(z)$** — isolated-lens RAR in $z$-bins over $z\sim0.3$–$1.5$: $\Delta\Sigma\to g_{\rm obs}$;
   baryonic $g_{\rm bar}$ from Euclid+ground photometry (stars) **+ cold gas** (the dominant $g_{\rm bar}$
   systematic — pair with HI/CO subsamples or marginalize a calibrated gas prior).
2. **Matched kinematic-$a_0(z)$** — MUSE-DARK / KROSS / JWST / ELT H$\alpha$ rotation at the *same* $z$ (the $V_c$ leg).
3. **The comparison** — lensing-$a_0(z)$ vs kinematic-$a_0(z)$ at matched $z$ (and matched host size/mass).
4. **Orthogonal bonus legs** — $\Sigma_\dagger(z)=a_0/G$ (critical surface density, *no* $V_c$) and $r_t(z)$ from the
   same lensing RAR: an over-determined set ($a_0$, BTFR, $\Sigma_\dagger$, $r_t$ have powers $+1,-1,+1,-\tfrac12$ of
   $E(z)$ — a single $E(z)$ must fit all).
5. **Clean anchor** — at $z\sim0.2$ the lensing RAR (Brouwer) already agrees with the kinematic $a_0\sim1.2$ → the
   lensing-vs-kinematic method offset is $\sim0$ at $z=0$, so a high-$z$ split is a clean systematic signal, not a
   zero-point artifact.

## 5. The forecast (this work, `a0z_forecast.py`, verified vs MUSE-DARK 16$\sigma$)
- Euclid lensing RAR, $z\sim0.3$–$1.5$, $\sim1$–$2\%$ per-$z$-bin on $a_0$ → $\sigma_\alpha\approx0.02$.
- **Evolution ($\alpha\neq0$): decisive** — $>5\sigma$ on $\alpha\neq0$ *even with $20\%$ per-bin systematics*;
  constant-$a_0$ MOND settled.
- **Rate ($\alpha=1$ vs $1.5$): only the cross-lever decides it** — statistically the gap is $\sim24\sigma$ *if*
  there were no coherent bias, but a coherent $\beta_{\rm sys}\sim0.5$ (the $\sim10\%$ $V_c$ / $\sim40\%$ gas
  budget) sits on the kinematic leg and **does not average down**. The lensing leg does not carry the $V_c$ lever,
  so the kinematic-vs-lensing *difference* isolates it (worked example: a true $\alpha=1$ with a $10\%$ $V_c$ +
  $10\%$ gas bias reads $\hat\alpha_{\rm kin}=1.57$ but $\hat\alpha_{\rm lens}=1.29$ — a $0.28$ split).

## 6. The decision tree — what Euclid will actually tell us
| Euclid lensing-$a_0(z)$ vs kinematic-$a_0(z)$ | meaning |
|---|---|
| both $\approx0$ (no evolution) | **OBT refuted**, constant-$a_0$ MOND vindicated |
| both $\approx1.5$, robust to measured gas | the rate is **real** → OBT's $cH(z)/2\pi$ *coefficient/rate* refuted (but $a_0$ still evolves — MOND-constant still dead; a faster rate would need a new horizon-coefficient origin) |
| kinematic $\approx1.5$ but lensing $\approx1.0$ | the **$V_c$ systematic** inflated the kinematic hints → OBT's $cH(z)/2\pi$ **safe** |
| both $\approx1.5$ but shrink under measured gas | **gas-census systematic** → $cH(z)/2\pi$ safe |
| both $\approx1.0$ | OBT's $cH(z)/2\pi$ **confirmed** |

Every branch is informative — there is no null outcome. This is what makes it a real test.

## 7. Honest caveats (the cool head)
- **The lensing RAR has its own systematics** (2-halo, intrinsic alignments, photo-$z$, the baryonic/gas
  $g_{\rm bar}$). The cross-lever's power is precisely that these are **different** from the kinematic $V_c$
  systematics: a *shared* real $a_0$-evolution shifts both legs together, while *orthogonal* systematics shift them
  apart. The comparison is robust even though each leg individually is systematics-limited.
- **OBT predicts the FORM, not the coefficient.** The thermodynamic content is $a_0\propto H(z)$ (a horizon-set
  scale) + its evolution; the $1/2\pi$ coefficient is an O(1) prior-art coincidence (Milgrom/Verlinde/McCulloch),
  consistent with the measured $a_0=1.20\pm0.24_{\rm syst}$ at $\le0.7\sigma$. So the **sharp** Euclid tests are
  (i) is $a_0$ evolving? and (ii) is the rate consistent with $E(z)$ ($\alpha\simeq1$)? — *not* the absolute value.
- **$E(z)$ vs $(1+z)$** are nearly degenerate below $z\sim1.5$; pushing the kinematic leg to $z\sim2$–3 (JWST/ELT)
  breaks it. Use MOND-regime ($g_{\rm bar}\sim a_0$) tracers only — never the compact, $a_0$-blind disks.

## 8. The ask
A **$z$-binned Euclid weak-lensing RAR** (extend Brouwer-KiDS to $z\sim1.5$) **+ matched kinematic-$a_0(z)$**
(MUSE/JWST/ELT) **+ measured cold gas** (HI/CO subsamples). This single, feasible-now programme converts
$a_0(z)$ from "evolution hinted, rate ambiguous" into a **decided rate**, and over-determines the horizon origin
of $a_0$ via $\Sigma_\dagger(z)$ and $r_t(z)$. Euclid DR1 (2026/2027) + the existing joint-RAR pipeline make it
the sharpest near-term play on physics *through the horizon* — and OBT has staked, in advance and in the open,
exactly what each outcome means.

---
*Sources: Euclid DR1 timeline & Wide Survey (ESA/cosmos.esa.int; Euclid preparation forecasts arXiv:1910.09273,
2512.09748); Brouwer et al. 2021 A&A 650 A113 (KiDS-1000 lensing RAR); joint kinematic+lensing RAR arXiv:2310.15248;
MUSE-DARK III arXiv:2604.22613; Übler et al. 2017 ApJ 842 121; Harrison et al. 2017 MNRAS 467 1965 (KROSS);
McGaugh, Lelli & Schombert 2016 PRL 117 201101 ($a_0=1.20\pm0.02\pm0.24$). Forecast & cross-lever: this folder
(`a0z_forecast.py` [= scripts/], `overdetermination.py`, `systematics_dissection.py`, `step2_crosslever_feasibility.md`,
`step3_real_papers.md`, `anchor_tension.py`).*
