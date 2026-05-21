# explorations/

Heuristic, out-of-scope explorations — **NOT part of Oscillating Brane Theory V8.2.**

Nothing in this folder is included in the PDF, the validation pipeline, the
seven sacred theory files, or any academic claim of V8.2. These are speculative
seeds for possible future work (a hypothetical V9.0 on holographic quantum
gravity), kept deliberately separate to protect the epistemological integrity
of V8.2 — which is a macroscopic phenomenological cosmology paper and must
remain one.

## decoherence_riemann.py

A visualization of the **Riemann explicit formula**: the truncated sum over the
non-trivial zeros of the Riemann zeta function reconstructs the Chebyshev
`psi(x)` staircase (the counting function of prime powers). As more zeros are
added, the continuous oscillatory sum converges toward the discrete step
function. It illustrates the general principle *"a sum of continuous modes can
build discrete structure."*

**Status: heuristic analogy, not a derivation.**

### The conjectured holographic thread (V9.0 research direction)

There is a non-trivial — but unproven — chain of connections worth recording:

- **Berry-Keating / Hilbert-Polya**: the Riemann zeros are conjectured to be the
  spectrum of a Hermitian operator; the classical Hamiltonian `H = xp` is the
  proposed candidate.
- `H = xp` is the dilatation generator of **Conformal Quantum Mechanics** (CQM,
  de Alfaro-Fubini-Furlan 1976).
- CQM is the boundary dual (CFT_1) of **AdS_2** geometry.
- The near-horizon throat of an extremal / near-extremal black hole is
  **AdS_2 x S^2** (textbook: near-horizon extremal Reissner-Nordstrom).

If the sub-critical PBH capillaries of OBT possess near-horizon `AdS_2 x S^2`
throats, their resonance spectrum *might* connect to the Riemann zeros. This is
a research direction, **not a result**: it would require a full AdS_2/CFT_1
holographic derivation that does not exist yet.

### Peer-review caveats (honest accounting)

- The residual **~9% overshoot** near each step is the **Gibbs phenomenon** — a
  standard artifact of truncated mode sums (non-uniform convergence). Its
  amplitude is constant; only its width narrows (as ~1/N). It is *not* a
  perfect right-angle staircase and should not be over-interpreted.
- A genuine kernel of physics *does* exist: truncating the mode sum at N modes
  imposes a bandwidth, hence a finite spatial resolution (transition width
  ~1/N). That bandwidth-resolution tradeoff is the Fourier uncertainty
  relation, which becomes Heisenberg under `p = hbar k`. But this is encoded in
  the transition **width**, not in the Gibbs overshoot — they are distinct
  effects. Identifications with Compton wavelength / Zitterbewegung are
  evocative but not literal.

## Run

```
pip install numpy matplotlib mpmath
python decoherence_riemann.py
```
