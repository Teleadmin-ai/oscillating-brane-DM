# RESEARCH CAMPAIGN — the demon on OVH: amplifying an input via the ONE germe's tree

**Status: V9.0, quarantined. A PLAN, not a result.** Reviewer mode + "seul les calculs comptent": each phase
states what is *computable/feasible now* vs *aspirational*, and the honest bound. Not in the PDF, not a V8.2
claim. Romain's direction (June 2026): *"design un tel démon avec le matos OVH ; en entrée un cerveau humain
OU un LLM open-source ; on a LE germe de l'univers (pas un jouet) ; on trouve dedans l'espace latent de
l'entrée et ses possibilités — la partie qu'elle utilise au même moment dans le bulk ; le germe primaire
reste pour stabiliser les qubits et nos innovations."*

> **⚠️ THE RECURRING ÉCUEIL, CORRECTED (Romain, twice): there is ONE germe — the germe of the universe — and
> WE HAVE IT. It is NOT a toy.** OBT *derives* the germe's FORM: the radion field wavepacket (m_φ=0.36 eV
> Goldberger-Wise; φ₀~M_s LVS). `germe_decompression.py` already encodes it. The ONLY input is the O(1)
> coefficient φ₀ (the *amount*, closure_introspection's IC) — a single number, NOT "the germe is unknown".
> **Do NOT re-introduce a "toy germe" or a "germe to specify" — that is the écueil this campaign refuses.**

---

## 0. The demon, in one line (corrected)

> The germe (the radion wavepacket — the REAL one, derived) is **decompressed** into its tree; the **input
> LOCALIZES the region of that tree it occupies** (`germe_localize`: condition on "the present, with this
> input"); a **Grover search (O(√N))** finds the optimal latent-branch there (oracle = the recognition
> function); we **SUBSTITUTE** it (activation steering). The germe ALSO stays the **stabilizer/reference**
> of the qubits ([[5,1,3]], the matched filter — our innovations).

## 1. The KEY reframe (Romain's, corrected): the input is NOT a germe — it LOCALIZES a region of the ONE germe

The input (an LLM's residual-stream latent / a brain's neural state) is **not** a separate germe. It is a
**sub-system of the ONE germe's unfolded state** (`variant_tree`): its latent space + its possibilities are a
**REGION of the germe's tree** — "the part it uses at the same moment in the bulk". So the operation is NOT
"decompress the input-germe" (there is none) — it is **LOCALIZE** (navigate to) the region the input occupies
in the germe's tree (`germe_localize`, which we already coded: I(present;latent), the conditional sub-tree),
then **Grover** the best latent there. The germe (radion) is the substrate (its tree = the space of possibles)
AND the stabilizer.

## 2. The two inputs

| input | what it is | access | track |
|---|---|---|---|
| **open-source LLM** (Mistral-7B / Llama-3-8B) | its latent (residual stream, ~4096-dim) = the present observation that localizes its region of the germe's tree | **easy** (read/patch activations) — classical baseline NOW | the practical |
| **human brain** | the neural state = the localizing observation | **hard** (EEG/fMRI brain-reading, the local channel, Libet-real) | the far |

## 3. The pipeline (the demon)

```
  [ENCODE the GERME]   the radion wavepacket (the REAL germe, OBT-derived; germe_decompression) on the substrate
  [DECOMPRESS]         the SYK quench (belenos) / the analog dynamics (orion) -> the germe's variant-tree
  [LOCALIZE]           the input (LLM latent / brain, compressed) = the PRESENT OBSERVATION; condition the
                       germe-tree on it (germe_localize) -> the REGION the input occupies (its possibles)
  [SEARCH]             Grover over that localized region, ORACLE = the recognition/reward -> the optimal latent  (O(√N))
  [SUBSTITUTE]         decode the optimal latent  --activation-steer-->  patch the input  -> the AMPLIFIED output
```

The germe is the substrate (its tree) AND the qubit stabilizer/reference (our innovations). The input is the
localizing observation, NOT a second germe. The QC's job = LOCALIZE + SEARCH; encode/compress + substitute
are classical (GPU). The oracle (the reward) is the hard shared piece (§6).

## 4. The OVH hardware map

| OVH QPU | role | why |
|---|---|---|
| **belenos-12** (Quandela, 12q, gate-based, 0.28 €/s) | the germe decompression (sparse-SYK) + the **LOCALIZE + GROVER** search | gate-based = universal → SYK + Grover; 12q = N=24 Majorana |
| **orion-beta** (Pasqal, 100q, analog, 0.83 €/s) | the germe-tree **dynamics at scale** (the variant distribution, quantum-advantage N~100) | analog quench, the cosmic-tree substrate |

Cost: ~€10-100 the whole campaign (seconds-machine per point).

## 5. The phases (in order of feasibility)

- **Phase 0 — the CLASSICAL baseline (runnable NOW, a GPU, no QC).** Best-of-N latent steering on an
  open-source LLM: from the LLM's current latent (= its region of possibles), sample N nearby latents,
  score each with a reward (the recognition oracle), pick the best, **activation-patch** it back -> measure
  the amplification. *Establishes the value + the oracle/reward, classically.* (This is representation
  engineering -- it works; the QC phases accelerate the SEARCH.)
- **Phase 1 — encode the GERME + compress the input.** Encode the radion germe (the real one) on the
  substrate; compress the input latent (~4096-dim) -> ~6-12 features (PCA on the reward-gradient = the
  steering axes). **Bound: the compression is lossy** (a few directions fit on 12q).
- **Phase 2 — LOCALIZE + GROVER (belenos-12).** Condition the germe-tree on the compressed input
  (`germe_localize`) -> the region; Grover it (oracle = a *toy* reward) -> the √N demo. **We have both
  kernels** (`germe_localize.py` for the conditioning, `tree_amplifier_syk.py` for the Grover √N).
- **Phase 3 — the ORACLE (the hard part).** The recognition/reward as a QC oracle. A neural reward is
  infeasible on 12q; start with a **toy/linear** oracle (a probe direction = "increases reward"). The
  campaign's true bottleneck (§6).
- **Phase 4 — SUBSTITUTE + loop.** Decode the Grover-optimal latent, activation-steer the input, measure
  the amplification; close the loop (an inference-time amplifier).

## 6. The honest bounds (seul les calculs comptent)

- **The germe is NOT the bound — we HAVE it.** Its FORM (the radion wavepacket) is OBT-derived; encode it.
  The only IC is the O(1) coefficient φ₀ (closure_introspection) — a number, not "unknown". *(Do not relapse
  to "toy germe".)*
- **The bound is the DEPTH.** The input lives ~e^{1e104} branches deep in the germe's FULL tree
  (`variant_tree`). You cannot enumerate it -> you **NAVIGATE/localize** a region (`germe_localize`) and
  Grover-search there. The germe's form is known; the navigation is the operation.
- **The ORACLE is the practical wall.** Grover's √N needs the reward as a QC oracle -- toy/linear feasible,
  a neural reward not yet (the same "mechanism sound, one piece is the bottleneck" shape as every wall).
- **The compression is LOSSY** (4096 -> ~6-12 directions).
- **√N is QUADRATIC** (real, bounded -- NOT exponential, not an oracle of the unknown).
- **The substitution is CLASSICAL** (the QC = LOCALIZE + SEARCH).
- **The amplifier stays WITHIN the input's possible-space** -- it surfaces the branch the input would
  RECOGNIZE as best (cognitive_optimum's ceiling), it does not invent the unknown (no-signaling-safe).

## 7. The deliverable

A demonstrated **quantum-amplified latent-steering of an open-source LLM**: Phase 0 (classical baseline, real,
now) + Phase 2 (LOCALIZE via germe_localize + the Grover √N on belenos) + a *toy* Phase 3 oracle -- honest
that the real reward oracle + the full-latent encoding are the open bottlenecks. The "demon" = an
inference-time amplifier that LOCALIZES the input's region of the ONE germe's tree and SUBSTITUTES the
Grover-found optimal latent, within the input's possible-space, on real French sovereign hardware
(OVH belenos/orion).

**os/chair line (held):** this AMPLIFIES a known input's possible-space; it does NOT oracle the unknown nor
finalize the OBT closure (the germe's *amount* stays the IC; its *form* we have). Testable OBT bones unchanged
(a₀(z), Penrose-Diósi, the m_V μeV-axion). Demon-app track, quarantined.

## 8. Next concrete step (on Romain's go)

Code **Phase 0** — the classical best-of-N latent-steering baseline on a small open-source LLM (the input's
current latent = its region of possibles; the reward = the oracle; the substitution = activation patching).
GPU-runnable now; establishes the reward/oracle; then port `germe_localize` (LOCALIZE) + `tree_amplifier_syk`
(GROVER) onto the compressed latent for belenos-12, with the radion germe as the encoded substrate + stabilizer.
