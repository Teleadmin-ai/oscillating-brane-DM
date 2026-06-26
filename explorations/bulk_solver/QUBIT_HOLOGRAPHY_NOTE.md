# "It from qubit" / braneworld holography — V9.0 direction for the closure problem

**Status: V9.0 conceptual direction, quarantined (NOT V8.2, NOT theory, NOT PDF).**
Romain's idea (June 2026, from a Wheeler discussion) + my critical evaluation. Park for a
dedicated V9.0 session; keep the card game (CHERCHEUR) separate.

## The idea (Romain)
Wheeler's "it from bit" (1989) → its generative mutation "it from qubit" → holographic
principle ('t Hooft/Susskind) → AdS/CFT (Maldacena) → Ryu-Takayanagi (entanglement entropy of
a boundary region = area of a minimal surface in the bulk) → Van Raamsdonk (geometric
connectivity *is* entanglement) → ER=EPR. Applied to OBT's RS bulk: **braneworld holography**
(Gubser; de Haro–Skenderis–Solodukhin) says 5D RS bulk gravity is dual to a CFT + gravity on
the brane, and the **projected Weyl tensor E_μν ↔ ⟨T_μν⟩_CFT** (the "dark radiation" = the CFT
stress tensor). Romain's framing of the solver's hard part: *"we compute the boundary but not
the center"* = exactly the **bulk reconstruction problem** (HKLL near the boundary;
entanglement-wedge reconstruction for the deep interior). The center is non-local from the
boundary → encoded in **entanglement** (a qubit, not a local bit). Hence: the closure "missing
bit" might be the boundary entanglement datum.

## My critical evaluation (do NOT rubber-stamp the enthusiasm)
**What is right + already in OBT's DNA:** the lineage is exact; E_μν ↔ ⟨T_μν⟩_CFT in RS is a
real, established result; and OBT already carries Skenderis holographic renormalization,
MERA/HaPPY (109 layers, ln χ = S_BH), ER=EPR, and the projected Weyl tensor. Bulk is AdS₅ →
the rigorous case. Good lineage, right box.

**The critical caveat (the shared-discussion partner under-stated it):** holography
**RELOCATES** the closure under-determination, it does **NOT dissolve** it. E_μν = ⟨T_μν⟩_CFT is
a *dictionary*; the **CFT STATE** (vacuum / thermal / coherent — which boundary entanglement?)
remains a CHOICE = exactly the bulk boundary condition in new clothes. RT gives the entanglement
entropy *given* the state/geometry; it does not conjure the state. So "the missing bit = the CFT
state = the boundary entanglement structure" is the SAME input, relocated. Claiming the
under-determination is "only apparent" is optimistic.

**What the gate program already established (the partner couldn't know this):**
- **Gate 9 (Indicial Theorem)** already DERIVED the *sign* of the closure in the linear-bulk
  chain (AdS warp degenerate indicial exponents (½,½) → c_phys ∈ (0,1] strictly positive →
  suppression). The sign is done (in that chain).
- **Gate 10** already OPENED the holographic route (RS/CFT dictionary, E_μν=⟨T_μν⟩_CFT) — and the
  **thermal glueball branch is DEAD** (under-produces); the radion-condensate misalignment was
  banked. So the *simplest* CFT state (thermal) does not give the DM amplitude.
- **Gate 24** concluded: the brane derives the FORM; the **AMOUNT (5:1, factor-2 cluster) stays a
  closure/IC datum**. Holography (so far) does not change that.
→ So the qubit route, while correct in lineage, **partly re-treads Gates 9/10/24**; the amplitude
  remains an input even holographically.

**The genuinely NEW, valuable thread (where Romain's intuition could pay off):** fix the boundary
entanglement **by INFLATION**. OBT already has: the ℓ=0 inflationary fossil (global phase
coherence), PBH genesis from the squeezed inflationary vacuum (Martin–Vennin 2015), the ER=EPR
network. **If** the closure datum (the CFT state / boundary entanglement) is set by the
inflationary vacuum's entanglement structure, then the "missing bit" becomes an **inflationary
prediction, not a free choice** — the exact *input → prediction* step the gates flagged as the
only remaining gap. This is the one angle that would do more than re-describe.

**Computational angle (real):** a **tensor network (MERA/HaPPY)** represents "the bulk as a
network of qubits"; network depth = warp/RG depth → OBT's exponential 10³² hierarchy becomes a
LINEAR depth → a structural bypass of the CFL wall that the forward-integration solver hits.
OBT already references MERA/HaPPY. This is the most concrete solver idea.

## Guardrails (agreed)
1. This is interpretation/language, **not yet an observable prediction** — a reviewer will say
   "nice, so what?" until it constrains something measurable.
2. AdS/CFT is rigorous in **AdS** (OBT's bulk AdS₅ → protected); the junction to the effectively
   **dS** dark-energy sector is conjectural (dS/CFT is a slippery open front). Keep the qubit for
   closing the AdS bulk + brane dynamics; be cautious at the accelerated sector.

## Concrete V9.0 to-dos when this is picked up
- Derive the E_μν ↔ ⟨T_μν⟩_CFT dictionary precisely for OBT's RS setup: which solver quantity maps
  to which CFT/entropy quantity (de Haro–Skenderis Fefferman–Graham expansion; OBT already has the
  Skenderis counterterm dictionary c₁/c₂/c_log).
- Test the **inflation-entanglement → CFT state → E_μν amplitude** chain: can the squeezed-vacuum
  entanglement fix the closure datum (sign + amplitude), turning the IC into a prediction?
  Cross-check against Gate 9's sign (independent route → validation if they agree).
- Prototype a tensor-network (MERA-like) representation of the warped bulk to beat the CFL wall;
  compare to the double-null forward solver on a Gate-0/Gate-1 validated case.
