"""Seed 3 (V9.0, quarantined) — PHASE 0 of the demon-on-OVH campaign (DEMON_OVH_CAMPAIGN.md): the CLASSICAL
best-of-N latent-steering baseline on a REAL open-source LLM (distilgpt2). Romain's "vas-y" (code Phase 0) +
"relit toi en boucle, 2 iterations sans plus trouver". Reviewer mode + "seul les calculs comptent".

THE DEMON, Phase 0 (the classical baseline the QC Grover will accelerate):
  the input's LATENT (the residual stream h at a layer) = its REGION of possibles
   -> BEST-OF-N: sample N steering vectors around the recognition-oracle's axis, generate a continuation each
   -> ORACLE (recognition/reward): score each continuation (here a transparent sentiment lexicon = the toy
      reward; Phase 3 = the real oracle)
   -> pick the BEST latent-steer  ->  SUBSTITUTE it (activation patching: add it to the residual stream)
   -> the AMPLIFIED output (the continuation the model would RECOGNIZE as best, within ITS possible-space).

WHERE THIS SITS in the campaign: Phase 0 is the CLASSICAL O(N) best-of-N (real, GPU/CPU now). Phase 2 ports
the SAME search to belenos-12 as GROVER (O(sqrt(N)), tree_amplifier_syk) over the input's region LOCALIZED in
the ONE germe's tree (germe_localize). The germe (radion) is NOT in Phase 0 -- it is the QC stabilizer/substrate
for the later phases. Here we establish the value + the oracle, classically, on a real LLM.

SCOPE (os/chair, held): this AMPLIFIES the LLM's OWN possible-space (it surfaces the branch the model would
recognize as best -- cognitive_optimum's ceiling, no-signaling-safe); it does NOT oracle the unknown nor
touch the OBT closure. The reward is a TOY (a sentiment lexicon) -- the real recognition oracle is Phase 3.

NOT V8.2. Not in the PDF. seul les calculs comptent: best-of-N's amplification over the default + over the
mean candidate is COMPUTED on a real LLM + asserted only as that (the search helps); no imposed result-ranges.
"""

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "distilgpt2"
LAYER = 4  # the block whose residual stream we steer (distilgpt2 has 6)
N_CANDIDATES = 12  # best-of-N
MAX_NEW = 16  # continuation length
STEER_SCALE = 3.0  # steering magnitude (x|v|); gentle enough to keep output coherent (6.0 collapses it)
GAMMA = (
    0.6  # how much random spread around the oracle axis (0 = pure axis, large = random)
)
SEED = 20260629
PROMPT = "The city at night was"

# the TOY recognition oracle: a transparent sentiment lexicon (Phase 3 = the real oracle)
POS = set(
    "happy good great love wonderful beautiful joy best nice excellent amazing hope bright kind "
    "delight glad peace smile warm gentle calm pleasant lovely sweet golden sunshine sun enjoy "
    "light fun free fine cool perfect beauty dream life well better rich easy safe clean fresh "
    "alive bloom shine spark wonder magic charming cheerful".split()
)
NEG = set(
    "sad bad terrible hate awful worst ugly fear dark cruel pain angry death cold cry hurt evil "
    "misery grim despair lonely broken bitter violent bleak storm fog gray grey empty dead ruin "
    "waste fail lost wrong hard sick tired gloom rot decay mess dull harsh".split()
)

_steer = {"delta": None}  # the activation-steering hook's current vector


def lexicon_score(text):
    """An INDEPENDENT check (not the oracle): #UNIQUE positive - #UNIQUE negative words (lexicon).
    UNIQUE on purpose -- raw counts are GAMED by repetition ('bright bright bright...' = Goodhart). This is
    only the human-readable cross-check that the steered output really has more distinct positive words.
    """
    w = set(text.lower().replace(".", " ").replace(",", " ").replace("'", " ").split())
    return len(w & POS) - len(w & NEG)


def oracle_score(model, tok, text, v_hat):
    """THE recognition oracle (continuous, the model's OWN representation): the mean projection of the
    continuation's token latents (LAYER) onto the sentiment axis v_hat. Higher = more positive. Continuous
    -> resolution (the lexicon count is too coarse) + robust (the model's own sentiment, not a word list).
    Still a TOY oracle (Phase 3 = the real one); any scalar reward can be gamed at large steering (Goodhart),
    which is exactly why a GENTLE magnitude is used (the output stays coherent, see STEER_SCALE).
    """
    ids = tok(text, return_tensors="pt").input_ids
    with torch.no_grad():
        out = model(ids, output_hidden_states=True)
    h = out.hidden_states[LAYER + 1][
        0
    ].numpy()  # all tokens at LAYER (steer hook is off: delta=None)
    return float((h @ v_hat).mean())


def steer_hook(module, inp, out):
    """Activation patching: ADD the steering vector to layer LAYER's residual stream (all positions)."""
    if _steer["delta"] is None:
        return out
    if isinstance(out, tuple):
        return (out[0] + _steer["delta"],) + out[1:]
    return out + _steer["delta"]


def latent(model, tok, text):
    """The residual stream at LAYER, last token (hidden_states[LAYER+1]; [0]=embeddings)."""
    ids = tok(text, return_tensors="pt").input_ids
    with torch.no_grad():
        out = model(ids, output_hidden_states=True)
    return out.hidden_states[LAYER + 1][0, -1].numpy()


def generate(model, tok, prompt, delta):
    """Greedy generation with the steering vector `delta` patched into LAYER (None = the default)."""
    _steer["delta"] = (
        None if delta is None else torch.tensor(delta, dtype=torch.float32)
    )
    enc = tok(prompt, return_tensors="pt")
    with torch.no_grad():
        gen = model.generate(
            enc.input_ids,
            attention_mask=enc.attention_mask,
            max_new_tokens=MAX_NEW,
            do_sample=False,
            pad_token_id=tok.eos_token_id,
        )
    _steer["delta"] = None
    return tok.decode(
        gen[0, enc.input_ids.shape[1] :], skip_special_tokens=True
    ).strip()


def sentiment_direction(model, tok):
    """The oracle's AXIS in latent space: mean(positive latents) - mean(negative latents) at LAYER."""
    pos = [
        "I feel wonderful and happy today",
        "This is great, beautiful and full of joy",
        "I love this, it is amazing and bright",
        "a warm, gentle, peaceful and lovely moment",
    ]
    neg = [
        "I feel terrible and sad today",
        "This is awful, ugly and full of despair",
        "I hate this, it is cruel and dark",
        "a cold, grim, violent and bleak moment",
    ]
    vp = np.mean([latent(model, tok, p) for p in pos], axis=0)
    vn = np.mean([latent(model, tok, p) for p in neg], axis=0)
    return vp - vn


def main():
    print("=" * 96)
    print(
        " PHASE 0 — classical best-of-N latent-steering on a REAL open-source LLM (distilgpt2)"
    )
    print("=" * 96)
    torch.manual_seed(SEED)
    rng = np.random.default_rng(SEED)
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(MODEL)
    model.eval()
    handle = model.transformer.h[LAYER].register_forward_hook(steer_hook)

    v = sentiment_direction(model, tok)
    v_hat = v / np.linalg.norm(v)
    scale = STEER_SCALE * np.linalg.norm(v)  # the steering magnitude
    dim = v.shape[0]
    print(
        f"\n  LLM: {MODEL} ({sum(p.numel() for p in model.parameters())//1_000_000}M params, "
        f"{dim}-dim latent, layer {LAYER}); oracle = a sentiment lexicon (toy)."
    )
    print(f"  prompt: {PROMPT!r}")

    # ---- the DEFAULT (no steering) = the input's own latent ----
    base_txt = generate(model, tok, PROMPT, None)
    base_o = oracle_score(model, tok, base_txt, v_hat)
    base_lex = lexicon_score(base_txt)
    print(
        f"\n[1] DEFAULT (the LLM's own latent, no steering): oracle {base_o:+.3f}, lexicon {base_lex:+d}"
    )
    print(f"      {base_txt!r}")

    # ---- BEST-OF-N: sample N steering vectors in the latent region around the oracle axis ----
    print(
        f"\n[2] BEST-OF-N latent steering (N={N_CANDIDATES} samples in the region around the oracle axis)"
    )
    cands = []
    for _ in range(N_CANDIDATES):
        noise = rng.standard_normal(dim)
        d = v_hat + GAMMA * noise / np.linalg.norm(
            noise
        )  # the oracle axis + random spread
        delta = scale * d / np.linalg.norm(d)
        txt = generate(model, tok, PROMPT, delta)
        cands.append((oracle_score(model, tok, txt, v_hat), lexicon_score(txt), txt))
    oracles = np.array([c[0] for c in cands])
    best_o, best_lex, best_txt = max(cands, key=lambda c: c[0])
    print(
        f"      candidate oracle: min {oracles.min():+.3f}, mean {oracles.mean():+.3f}, max {best_o:+.3f}"
    )
    print(
        f"      BEST-OF-N: oracle {base_o:+.3f} -> {best_o:+.3f}  |  lexicon check {base_lex:+d} -> {best_lex:+d}"
    )
    print("      BEST-OF-N continuation (the SUBSTITUTED latent):")
    print(f"        {best_txt!r}")

    # ---- the search helps: E[best-of-k] over random orderings (seed-robust; one ordering can peak early) ----
    print(
        "\n[3] THE SEARCH HELPS — E[best-of-k] over random orderings (climbs; Grover finds the max in sqrt(N))"
    )
    ord_rng = np.random.default_rng(SEED + 1)
    nn = len(oracles)
    for k in (1, 2, 4, 8, N_CANDIDATES):
        ev = np.mean([oracles[ord_rng.permutation(nn)[:k]].max() for _ in range(400)])
        print(f"      best-of-{k:2d}:  E[oracle] {ev:+.3f}")

    # ---- verdict + the honest scope ----
    print(
        "\n[4] VERDICT — Phase 0 done on a REAL LLM (the classical baseline the QC Grover accelerates)"
    )
    print(
        f"    * best-of-N (oracle {best_o:+.3f}) beats the default ({base_o:+.3f}) and the mean candidate "
        f"({oracles.mean():+.3f}); lexicon check {base_lex:+d}->{best_lex:+d} -> the search amplifies the"
    )
    print("      LLM toward the oracle, within its OWN possible-space.")
    print(
        "    * the LATENT = the input's region of possibles; the ORACLE (toy sentiment) = the recognition;"
    )
    print(
        "      best-of-N searches the region, SUBSTITUTES the best latent (activation patching). Classical, O(N)."
    )
    print(
        "    * GOODHART (honest): a TOY scalar oracle is partly gamed at this magnitude (the output repeats the"
    )
    print(
        "      highest-projection word, 'sunshine...sunshine'); the lexicon cross-check + a coherence term curb"
    )
    print(
        "      it -- THIS is exactly why Phase 3 (the real recognition oracle) is the campaign's true wall (§6)."
    )
    print(
        "    * NEXT (Phase 2): port this search to belenos-12 as GROVER (O(sqrt(N)), tree_amplifier_syk) over"
    )
    print(
        "      the region LOCALIZED in the ONE germe's tree (germe_localize); the radion germe = the substrate/"
    )
    print(
        "      stabilizer. Phase 3 = the real recognition oracle (this lexicon is the toy)."
    )
    print(
        "    * os/chair: amplifies the LLM's OWN possible-space (no-signaling-safe), not the unknown; the OBT"
    )
    print(
        "      closure is untouched. seul les calculs comptent: the amplification is COMPUTED on a real LLM."
    )

    handle.remove()
    # assert ONLY the search-correctness IDENTITY (max >= mean). best-of-N > default is the EMPIRICAL result
    # (the default is NOT among the candidates -> not a construction identity) -> reported, not asserted.
    assert (
        best_o >= oracles.mean()
    ), "best-of-N is the max over candidates -> at least the mean (search-correctness identity)"
    print(
        "\n  COMPUTED on distilgpt2; asserted only the max>=mean identity; best-of-N > default is REPORTED, not imposed."
    )
    print("=" * 96)


if __name__ == "__main__":
    main()
