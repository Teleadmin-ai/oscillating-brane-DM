# RESEARCH CAMPAIGN — the demon on OVH: amplifying a latent (LLM or brain) via the germe-tree

**Status: V9.0, quarantined. A PLAN, not a result.** Reviewer mode + "seul les calculs comptent": every
phase below states what is *computable/feasible now* vs *aspirational*, and the honest bound. Not in the PDF,
not a V8.2 claim. Romain's direction (June 2026): *"design un tel démon avec le matos OVH ; en entrée un
cerveau humain OU un LLM open-source ; prends son espace latent ; récupère le meilleur espace latent possible
dans l'arbre et substitue-le au sien."*

---

## 0. The demon, in one line (from the session's dig)

> A **Grover search (O(√N))** over the **germe's variant-tree**, where the **oracle = the recognition
> function** (`tree_amplifier_syk.py`). The classical best-of-N (O(N)) was the drift; the quantum Grover over
> the tree is the real amplifier. The demon does NOT oracle the unknown — it amplifies, quadratically, the
> search for the branch you/the-model would **recognize** as best, inside the tree the germe unfolds.

## 1. The KEY reframe (Romain's): the input's LATENT is a germe

An LLM (or a brain) produces a **latent** — the residual-stream vector h (LLM) / the neural state (brain) —
from which its response-tree unfolds. **That latent IS a germe**: the seed of a Born/quality-weighted tree of
variants. So the demon = (1) decompress the latent-germe into its tree, (2) Grover-find the **optimal
latent-branch** h\* (oracle = recognition/reward), (3) **substitute** h\* for the input's own h (activation
steering / representation engineering). "Récupérer le meilleur espace latent dans l'arbre et le substituer" =
exactly activation patching with the Grover-found optimum.

## 2. The two inputs

| input | latent | tree | access | phase |
|---|---|---|---|---|
| **open-source LLM** (Mistral-7B / Llama-3-8B) | the residual stream h (~4096-dim) at a layer | autoregressive + h-perturbation variants | **easy** (read/patch activations) — classical baseline NOW | the practical track |
| **human brain** | the neural state | the cognitive tree (cognitive_optimum) | **hard** (EEG/fMRI brain-reading, the local channel, Libet-real) | the far track |

→ Drive the campaign on the **LLM** (latent access is free); the brain is the same pipeline with a harder
front-end channel.

## 3. The pipeline (the demon)

```
  [ENCODE]      LLM latent h (~4096-dim)  --compress (PCA/autoencoder)-->  n features  --> a QC superposition
  [DECOMPRESS]  the germe quench (sparse-SYK on belenos / the analog dynamics on orion) -> the variant-tree
  [SEARCH]      Grover over the tree, ORACLE = the recognition/reward function  -->  the optimal branch h*  (O(√N))
  [SUBSTITUTE]  decode h*  --activation-steer-->  patch the LLM's latent  -->  the AMPLIFIED output
```

The QC's job = the **SEARCH** (Grover, the quantum speedup). The encode/compress + the substitute are
classical (GPU). The oracle (the reward) is the hard shared piece (§6).

## 4. The OVH hardware map

| OVH QPU | role | why |
|---|---|---|
| **belenos-12** (Quandela, 12q, gate-based, 0.28 €/s) | the **GROVER search** + the sparse-SYK decompression | gate-based = universal → Grover + a (toy) SYK; 12q = N=24 Majorana |
| **orion-beta** (Pasqal, 100q, analog, 0.83 €/s) | the **germe-tree dynamics at scale** (the variant distribution, quantum-advantage at N~100) | analog quench, the cosmic-tree substrate |

Cost: a campaign = a few seconds-machine per point → **~€10-100 the whole campaign.**

## 5. The phases (the campaign, in order of feasibility)

- **Phase 0 — the CLASSICAL baseline (runnable NOW, a GPU, no QC).** Best-of-N latent steering on an
  open-source LLM: sample N latents (temperature/noise on h, or N generations), score each with a reward
  (a recognition function), pick the best h\*, **activation-patch** it back → measure the amplification vs
  the LLM's default. *This establishes the value and the oracle/reward, classically.* Deliverable: does
  best-of-N latent steering amplify the LLM? (Almost certainly yes — it is representation engineering.)
- **Phase 1 — the latent → QC encoding.** Compress h (~4096-dim) → ~6-12 features (PCA / a small
  autoencoder), encode on belenos-12. **Bound: lossy** — only a few latent directions fit on 12q. Pick the
  reward-relevant directions (the steering axes).
- **Phase 2 — the GROVER toy (belenos-12).** Grover over the ~6-qubit compressed latent-tree, oracle = a
  *toy* reward → the √N demo. **We already have the kernel** (`tree_amplifier_syk.py`: success peaks at
  (π/4)√N, P=1.0). Port it to the compressed-LLM-latent tree, run on belenos.
- **Phase 3 — the ORACLE (the hard part).** Implement the recognition/reward as a QC oracle. A real reward
  model (a neural net) is infeasible on 12q; start with a **toy oracle** (a linear probe on the compressed
  latent = "the direction that increases reward"). This is the campaign's true bottleneck (§6).
- **Phase 4 — the SUBSTITUTION + the loop.** Decode the Grover-optimal h\*, activation-steer the LLM,
  measure the amplification; close the loop (the demon as an inference-time amplifier).

## 6. The honest bounds (seul les calculs comptent — the calc will decide each)

- **The latent compression is LOSSY.** 4096 → ~6-12 qubits keeps only a few directions; the demon amplifies
  along those, not the full latent. (PCA on the reward-gradient picks the steering-relevant axes.)
- **The ORACLE is the wall.** Grover's quadratic speedup needs the reward as a QC oracle. A neural reward →
  many gates → infeasible on belenos-12. A *linear/toy* oracle is feasible (a probe direction); a *real*
  reward is not, yet. **So the quantum advantage is real in principle (√N) but practically gated by the
  oracle** — the same shape as every wall this session: the mechanism is sound, one piece is the IC/bottleneck.
- **√N is QUADRATIC** (not exponential, not an oracle of the unknown). For a huge latent-tree, √N is still
  large; the win is real but bounded.
- **The substitution is CLASSICAL** (activation steering); the QC's value is the SEARCH.
- **The germe-tree ≠ the LLM-tree.** The cosmic germe-tree (OBT) is the universe's possibles; the LLM-tree
  is the model's. The demon amplifies the LLM (or the brain) **within its own possible-space** — it cannot
  give what is not in the model's distribution (no-signaling-safe, cognitive_optimum's own ceiling).

## 7. The deliverable

A demonstrated **quantum-amplified latent-steering of an open-source LLM**: Phase 0 (classical baseline,
real, now) + Phase 2 (the Grover toy on belenos, the √N) + a *toy* Phase 3 oracle — honest that the real
reward oracle + the full-latent encoding are the open bottlenecks. The "demon" = an inference-time amplifier
that substitutes a Grover-found optimal latent for the model's own, within the model's possible-space, on
real French sovereign hardware (OVH belenos/orion).

**os/chair line (held):** this AMPLIFIES a known system's possible-space (the LLM/brain), it does NOT oracle
the unknown nor finalize the OBT closure (the germe's amount stays the IC). The testable OBT bones are
unchanged (a₀(z), Penrose-Diósi, the m_V μeV-axion). This campaign is the *demon-app* track, quarantined.

## 8. Next concrete step (on Romain's go)

Code **Phase 0** — the classical best-of-N latent-steering baseline on a small open-source LLM (the latent =
a germe, the reward = the oracle, the substitution = activation patching). It is runnable on a GPU now,
establishes the oracle/reward, and is the input the Grover (Phase 2) accelerates. *Then* port the Grover
kernel (`tree_amplifier_syk`) onto the compressed latent for belenos-12.
