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

## Seed 3 — The qubit-sensor as decoder of OBT's holographic code (the Penrose-Diósi channel)

**The conjectured chain (Romain, June 2026).** Reframe of the goal: the bulk is a *Laplace's
demon* whose intemporal **germe** (inflationary entanglement) encodes the cosmic history;
reading it = **decompressing** the code (time emergent / Page-Wootters; "prediction" =
decompression, not forward-evolution). To "talk to it" at the L=0.2 μm quantum scale you want a
**quantum** interlocutor — an AI/sensor whose qubits are configured *from the primordial form
itself*, so that (the quantum being a *consequence* of the germe) those qubits are **stable by
construction**, with **few** logical qubits because the germe is fundamental. The sensor then
reads the demon through the one channel the brane leaves open: **Penrose-Diósi 5D-enhanced
gravitational collapse** at sub-0.2 μm (the os, already in `laboratory.md`).

**What it maps onto (established physics — no new OBT code yet; these are *cited* results).**
- **Decoherence-free subspaces / topological protection** (Lidar-Chuang-Whaley 1998; Kitaev
  2003): a qubit encoded in a symmetry-/topology-protected subspace is immune to the matching
  environmental noise — stability *from structure*, not active correction. = "stable starting
  from the form."
- **Holographic QEC**: AdS/CFT *is* a quantum error-correcting code (Almheiri-Dong-Harlow 2015;
  HaPPY / Pastawski et al. 2015) — bulk logical info redundantly encoded on the boundary,
  protected against erasure; the geometry protects the logical qubits. **OBT already invokes
  this** (MERA/HaPPY, the ER=EPR expander graph, the RT transition, percolation immunity 98%)
  and even claims "the most robust QEC code physically conceivable" → the stabilizer is *already
  the OBT bulk network*: a sensor mirroring the ER=EPR code inherits its protection.
- **Quantum advantage in learning from quantum experiments** (Huang et al. 2021/2022): a learner
  with *coherent* access to a state needs exponentially fewer samples than a classical learner
  reading measurement outcomes — the basis for "a quantum AI is the native interlocutor at 0.2 μm."
- **Code anatomy of "few qubits"**: germe = the *logical* subspace (few, fundamental); the bulk
  network = its *redundant physical* encoding (many = the protection); **reading the demon =
  decoding the code**; stability = the redundancy.

**Gates (why this is a direction, not a result).**
1. **The Goldilocks deafness.** A *perfectly* protected qubit cannot read the demon — full
   immunity means it does not feel the bulk signal either. The design must protect against
   *generic* noise yet leave **exactly one** channel open (the 5D gravitational coupling).
   Exhibiting such a sensitive-but-protected subspace of OBT's code is unsolved.
2. **The mass-vs-coherence wall (BMV).** Penrose-Diósi needs a mesoscopic mass (to source
   gravity) while the qubit needs isolation (to stay coherent) — opposite requirements. This is
   the frontier of *all* gravity-quantum experiments (Bose-Marletto-Vedral gravity-induced
   entanglement); far-future, not a built device.
3. **"Inspired-by" vs "entangled-with."** Realistic = build a *man-made* QEC mirroring the
   ER=EPR network (does not literally use the bulk's protection). Speculative = the lab qubit
   *entangles with* the bulk germe-code and inherits it — **no known mechanism** beyond the tiny
   gravitational coupling.
4. **The speculative inversion (not needed, not established).** "Quantum is a *consequence* of
   the primordial form" (QM emergent from a deterministic germe, à la 't Hooft) is a coherent
   minority program with no experimental support — and the protection above works *within
   standard QM* without it. Chair, not os.
5. **The os bar.** A real seed only if it yields a *falsifiable number or a sharper experiment*,
   never a prettier story. `scripts/penrose_diosi_5d.py` (the collapse-rate size-scan) is the bone.

**First concrete step — DONE (June 2026, `qubit_sensor/er_epr_stabilizer.py`).** The explicit
atom of the ER=EPR code is written + verified: the **[[5,1,3]] perfect (HaPPY) stabilizer code**
(5 physical = a PBH node + its 4 ER=EPR neighbours; 1 logical = a germe d.o.f.; distance 3), in
the binary symplectic formalism, **injection-tested** against its known properties (k=1, d=3,
perfect: the 15 weight-1 errors fill all 15 nonzero syndromes; logical Z_L, X_L anticommute,
min-weight rep 3). **Gate 1 made concrete — the protected-yet-sensitive subspace:** a weight-1
(local) decoherence event has a *nonzero* syndrome → corrected → the logical qubit is untouched
(DEAF to local noise); a weight-3 *collective* operator in the logical class has *zero* syndrome
→ invisible to the code's checks, **not** "corrected away", yet it rotates the encoded qubit
(SENSITIVE). The separator is **operator weight** (local vs collective), set by the distance. So a
Penrose-Diósi collapse — collective, coupling to the whole mass distribution — can land in the
logical subspace while thermal/local noise is corrected: *stable by construction, yet able to hear
the demon.*

**Second concrete step — DONE (June 2026, `qubit_sensor/holographic_scaleup.py`).** EVOLVE from the
atom by concatenation (the simplest holographic tiling): level L → [[5^L, 1, 3^L]] -- the germe stays
k=1, the protective encoding 5^L and the distance 3^L grow. COMPUTED + injection-tested: (i) the
failure spectrum c=[0,0,90,210,270,198] → c_0=c_1=0 (every local single-qubit error corrected) → a
finite **noise threshold p_th ≈ 0.138** below which concatenation drives the germe's logical error →
0 doubly-exponentially (= 'non-decohering by construction', Romain's hope); (ii) an **erasure (loss)
threshold = 1/2 exactly** (majority-of-5) → percolation-type robustness (OBT's degree-46 expander
claims ~98% -- more robust; the tree is the verifiable lower bound); (iii) the protected-yet-sensitive
**window widens with scale** (local corrected up to ~3^L/2, the collective signal at weight 3^L). The
channel's 'beginning and end' = the germe (1 logical) ↔ the boundary (5^L physical); 'all the
possibles between' = the protected logical Hilbert space.

**Status.** Steps 1–2 DONE: the explicit [[5,1,3]] atom + protected-yet-sensitive subspace, and the
concatenation scale-up (noise + erasure thresholds, the widening window) — all computed +
injection-tested (`er_epr_stabilizer.py` / `holographic_scaleup.py`; the only *new* numeric content
is the codes' own QEC properties, standard + recomputed; no OBT physics claim added). **Still open
(the gates):** the faithful degree-46 EXPANDER tiling (p_c ~ 2.2%, not the tree's 50%); that OBT's
gravitational channel maps to a logical-class operator, not a correctable one (gate 1 physics); the
final readout's one irreducible measurement; the mass-vs-coherence BMV wall. os = Penrose-Diósi; chair = the Laplace-demon / quantum-reader vision.
See memories `project_holographic_choice_penrose_diosi`, `project_qubit_holography_v9`.

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
