# explorations/

Heuristic, out-of-scope explorations — **NOT part of Oscillating Brane Theory V8.2.**

Nothing in this folder is in the PDF, the validation pipeline, the seven sacred
theory files, or any academic claim of V8.2. These are speculative seeds for a
possible future V9.0 on holographic quantum gravity, kept deliberately separate
to protect the epistemological integrity of V8.2 — which is a macroscopic
phenomenological cosmology paper and must remain one.

Each seed below records: the conjectured chain, what was actually **verified**
(with runnable code), and the **gates** that keep it a research direction rather
than a result. The discipline throughout: *code, don't plead* — every numeric
claim comes from an audited script with known-case injection tests.

---

## Seed 1 — Riemann zeros as the spectrum of a PBH AdS₂ throat (Hilbert-Pólya)

**The conjectured chain.** Riemann zeros ↔ Berry-Keating `H = xp` ↔ Conformal
Quantum Mechanics (de Alfaro-Fubini-Furlan 1976) ↔ AdS₂ boundary dual ↔
near-horizon throat of a (near-)extremal black hole = AdS₂×S² ↔ the tidal-charge
PBH capillaries of OBT. If the zeros were the eigenvalues of the throat's
spectral problem, that would realize Hilbert-Pólya inside the theory's geometry.

**Scripts**
- `decoherence_riemann.py` — Riemann explicit formula: a truncated sum over
  non-trivial zeta zeros rebuilds the discrete Chebyshev ψ(x) prime-power
  staircase. Illustrates "continuous modes → discrete structure."
- `riemann_berry_keating.py` — verifies the Berry-Keating semiclassical count
  N(T)=(T/2π)log(T/2π)−T/2π+7/8 against the actual zeros (|residual| ≤ 0.33 over
  the first 30 zeros).
- `tidal_charge_ads2.py` — tidal-charge brane BH f(r)=1−2GM/r+q/r²: horizon
  structure vs sign of q, extremality, near-horizon AdS₂×S², and the T_H(q) table.

**Verified this session (May 2026)**
- Berry-Keating smooth count reproduces the **average density** of Riemann zeros. ✓
- Extremal tidal charge (q=(GM)²) ⇒ near-horizon = **AdS₂(r₀)×S²(r₀)** exactly. ✓
- ζ(−1)=−1/12 obtained via the functional equation (the Casimir value — Fil A). ✓

**Three gates (why this is a direction, not a result)**
1. **Tidal-charge sign / extremality.** An AdS₂ throat requires q>0 *near-extremal*
   (q≈(GM)²). The default braneworld sign is **negative** → single horizon, never
   extremal, no throat. Worse, the sign is a **5D bulk integration constant**: the
   brane junction equations are not closed, so q cannot be fixed without solving
   the full AdS₅ bulk. And near-extremality forces T_H→0, **contradicting** the hot
   (T_H~900 K) Schwarzschild-like fast-scrambler PBHs that V8.2's Γ_rad=ln(S_BH)/2π
   relies on. The same PBH cannot be both.
2. **Generic statistics ≠ the zeros.** GUE level statistics (Montgomery-Odlyzko)
   are generic to *any* quantum-chaotic spectrum. "Same statistics as the zeros" is
   necessary, not sufficient — it is not yet a prediction.
3. **The operator itself.** No self-adjoint operator reproducing the individual
   zeros is known to anyone (Hilbert-Pólya, open). Berry-Keating gives only the
   smooth density; the fluctuating arithmetic part (the primes' fingerprint) is
   unaccounted.

**The real physics underneath.** The near-extremal (small-T) regime has a
"nearly-AdS₂" throat with a Schwarzian boundary mode — exactly the SYK / JT-gravity
regime where maximal chaos and GUE-like spectra live. Beautiful and well-studied;
the blockers are the three gates above, not the physics of the middle of the chain.

---

## Seed 2 — Void "entanglement" signature

**The idea.** If the bulk is holographically entangled with several branes
(thermofield-double / ER=EPR), could that leave a trace on the largest cosmic
structures — the voids?

**Script**
- `void_entanglement.py` — order-of-magnitude anchors for the two routes.

**Verdict this session (May 2026): does NOT become falsifiable as entanglement.**
- **Thermal route** (a brane entangled with a partner sees a thermal vacuum at the
  horizon entanglement temperature): T = ℏH₀/(2πk_B) ≈ **2.7×10⁻³⁰ K**, ~10⁻³⁰ of
  the CMB. Unobservable, even in the cleanest voids.
- **The only falsifiable handle** is the **classical cymatic scale** λ=cT≈**613 Mpc**
  (k≈0.0103 Mpc⁻¹) — a preferred scale in void clustering / void-ISW, testable by
  Euclid/DESI. But this is a **classical standing wave** (Chladni), already in V8.2
  (KBC void, Big Ring, Giant Arc), **not** entanglement.
- **No discriminant.** Classical standing wave = nodes at fixed comoving positions;
  entanglement = position-independent correlation at separation ~λ. Distinct in
  principle, but cosmic variance (one universe, few independent ~600 Mpc cells) +
  Maldacena 2015 (cosmological Bell tests unobservably tiny in standard scenarios)
  make the distinction impossible.

**Status.** Metaphysical interpretation, not prediction. The testable void content
(the 613 Mpc cymatic scale) is classical and already belongs to V8.2; the
"entanglement / multiverse" layer adds interpretation, not a falsifiable number, and
is *less* economical than the classical Chladni explanation (Occam).

---

## Peer-review caveat carried from `decoherence_riemann.py`

The residual ~9% overshoot near each ψ(x) step is the **Gibbs phenomenon** — a
truncation artifact, constant amplitude, narrowing width ~1/N. It is *not* a perfect
right-angle staircase. The genuine physics kernel (finite mode bandwidth → finite
resolution → Fourier/Gabor uncertainty → Heisenberg under p=ℏk) lives in the
transition **width** ~1/N, **not** in the overshoot. Identifications of the overshoot
with Compton wavelength / Zitterbewegung are evocative but not literal.

## Rules

Do NOT pull anything from `explorations/` into the seven sacred files or the PDF.
Do NOT delete the folder. It is deliberately quarantined — V8.2 stays a pure
macroscopic phenomenological cosmology paper; these holographic-QG ideas live here
until (and unless) they are formally derived and clear their gates.

## Run

```
pip install numpy scipy matplotlib mpmath
python <script>.py
```
