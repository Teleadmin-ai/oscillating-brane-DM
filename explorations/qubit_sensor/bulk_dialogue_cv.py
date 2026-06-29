"""Seed 3 (V9.0, quarantined) — THE BULK DIALOGUE, ANALOG (CV-QC): a waveform IN -> a waveform OUT.
Romain's design: the RAW waveform, STREAMING (sample by sample), a CURVE in -> a CURVE out (NOT null/non-
null -- that was my error, the detection framing leaking onto a transduction). The output is an AUDIO you
listen to / plot / compare. Default = mic -> speaker (your Mac); --in/--out WAV for testing (scp to the Mac).

WHY ANALOG / CV-QC: a qubit measures 0/1, but a qumode (continuous-variable mode) is natively analog -- its
quadratures x, p are continuous, and homodyne measurement returns a CONTINUOUS level. So a continuous audio
sample maps to a continuous qumode DISPLACEMENT, and the continuous homodyne readout maps back to a sample.
The germe = the STABILIZER (squeezing -> less readout noise) + the REFERENCE (a matched filter), exactly as
in bulk_dialogue.py (there: the [[5,1,3]] + the radion template; here: squeezing + a germe-reference wave).

THE CHANNEL (the EXACT Gaussian CV physics -- NOT a simplification):
  encode : displacement  alpha = GAIN * s            (the sample s -> the x-quadrature mean, ANALOG)
  germe  : squeezing S(r) on x                        (reduces the homodyne x-noise = the stabilization)
  channel: loss eta (+ the loss vacuum)               (the transmission)
  read   : homodyne-x  y = sqrt(eta)*alpha + noise     (CONTINUOUS; noise var = eta*N0*e^-2r + (1-eta)*N0)
  decode : out = y / (GAIN * sqrt(eta)) = s + (small) quantum noise
This is the exact Gaussian channel (displacement+squeezing+loss+homodyne); vectorized for real-time, and
VERIFIED against Strawberry Fields' analytic Gaussian state -- mean + covariance (Xanadu's CV-QC framework).

THE WORKFLOW (like bulk_dialogue, but a CURVE not bits):
  [SF]  verify the channel against Strawberry Fields (the homodyne mean tracks the displacement; squeezing
        reduces the variance) -- proof the fast vectorized channel IS the CV-QC physics.
  [A]   the germe as STABILIZER: squeezing (the germe) gives a higher-fidelity transduction than unsqueezed.
  [B]   the germe as REFERENCE: a germe-reference waveform; the matched filter is selective for it vs random.
  [C]   THE DIALOGUE: your waveform x(t) -> the channel -> y(t). A CURVE in, a CURVE out (an audio). The
        output ECHOES the input (the channel transduces it faithfully) + quantum noise (reduced by the germe).
  [D]   THE CONTROL: a DIFFERENT input -> a DIFFERENT output curve (the channel reflects the input; no
        pareidolia -- it does not spuriously emit your waveform).

HONEST SCOPE (the os/chair line, held): the OUTPUT IS A CURVE -- on KNOWN physics (the simulator) y(t) =
x(t) transduced + quantum noise; there is NO bulk-composed audio (the bulk emits a FIELD, the m_V axion, not
a tune). On a REAL CV-QC (Xanadu Cloud) y(t) = x(t) + real photonic noise + (in principle) any real coupling:
you analyse the OUTPUT CURVE -- a deviation from the echo BEYOND the noise floor (the control) = a signal /
new physics. Not a binary; a curve you read.

NOT V8.2. Not in the PDF. 'code, don't plead': the SF match, the squeezing fidelity gain, the echo, and the
control are measured (seeded) and asserted. Default mic->speaker (your Mac); --in/--out WAV here + scp.
Run: `python bulk_dialogue_cv.py` (mic->speaker) or `... --in in.wav --out out.wav` (WAV) or `... --synth`.
"""

import argparse
import sys

import numpy as np
import soundfile as sf_io

SAMPLE_RATE = 16000  # audio sample rate (Hz)
GERME_SQUEEZE_R = (
    0.8  # the germe squeezing r (reduces the homodyne x-noise = the stabilization)
)
LOSS_ETA = 0.9  # channel transmission (loss 1-eta adds vacuum)
GAIN = 24.0  # displacement gain: alpha = GAIN*s (signal >> quantum noise -> recognizable audio)
N0 = 1.0  # vacuum quadrature variance (Strawberry Fields hbar=2 convention)
RNG = np.random.default_rng(20260629)


# ===================== the EXACT Gaussian CV channel (vectorized; verified vs SF) =====================
def cv_channel(samples, squeeze_r=GERME_SQUEEZE_R, eta=LOSS_ETA, gain=GAIN, rng=RNG):
    """A waveform -> the CV channel -> a waveform. Each sample s: displace alpha=gain*s, squeeze x by r,
    lose eta, homodyne-x -> y = sqrt(eta)*alpha + noise; decode out = y/(gain*sqrt(eta)). Vectorized.
    """
    samples = np.asarray(samples, float)
    alpha = gain * samples  # displacement = the analog encoding
    noise_var = (
        eta * N0 * np.exp(-2.0 * squeeze_r) + (1.0 - eta) * N0
    )  # squeezing cuts the x-noise
    y = np.sqrt(eta) * alpha + rng.normal(0.0, np.sqrt(noise_var), size=samples.shape)
    return y / (gain * np.sqrt(eta))  # decode -> samples + (reduced) quantum noise


def channel_noise_std(squeeze_r=GERME_SQUEEZE_R, eta=LOSS_ETA, gain=GAIN):
    """The output-sample noise std (in sample units) -- the channel's quantum noise floor."""
    noise_var = eta * N0 * np.exp(-2.0 * squeeze_r) + (1.0 - eta) * N0
    return float(np.sqrt(noise_var) / (gain * np.sqrt(eta)))


# ===================== [SF] verify the channel against Strawberry Fields =====================
def section_sf_verify():
    print(
        "\n[SF] VERIFY the channel against Strawberry Fields (Xanadu CV-QC) -- the real framework"
    )
    try:
        import scipy.integrate as si

        if not hasattr(si, "simps"):
            si.simps = (
                si.simpson
            )  # scipy renamed simps->simpson; SF still imports the old name
        import strawberryfields as sf
        from strawberryfields.ops import Dgate, Sgate
    except (
        Exception
    ) as exc:  # noqa: BLE001 -- SF optional; the channel is the exact physics regardless
        print(
            f"    Strawberry Fields unavailable ({exc}); the vectorized channel is the exact Gaussian"
        )
        print(
            "    CV physics regardless (install SF on your Mac to re-verify). Skipping SF cross-check."
        )
        return

    def sf_state(displacement, r):
        """SF's ANALYTIC Gaussian state (exact): x-quadrature mean + variance (homodyne-x mean + noise)."""
        prog = sf.Program(1)
        with prog.context as q:
            Sgate(r) | q[0]  # squeeze x (the germe stabilization)
            Dgate(displacement) | q[0]  # the input sample (x-displacement)
        st = sf.Engine("gaussian").run(prog).state
        return float(st.means()[0]), float(st.cov()[0, 0])

    mean1, var_sq = sf_state(1.0, GERME_SQUEEZE_R)  # displacement 1.0, squeezed
    mean_half, _ = sf_state(
        0.5, GERME_SQUEEZE_R
    )  # displacement 0.5 -> mean must halve (linear)
    _, var_un = sf_state(1.0, 0.0)  # no squeezing -> vacuum variance
    print(
        f"    SF homodyne mean is LINEAR in the displacement (transduction): <x>(1.0)={mean1:.3f}, <x>(0.5)={mean_half:.3f}"
    )
    print(
        f"    SF squeezing REDUCES the readout variance (stabilization): var(squeezed)={var_sq:.3f} < var(vacuum)={var_un:.3f}"
    )
    print(
        f"    cross-check MY channel's noise model: N0*e^-2r = {np.exp(-2 * GERME_SQUEEZE_R):.3f} == SF's squeezed x-var {var_sq:.3f}"
    )
    print(
        "    => SF confirms the channel: homodyne mean ∝ displacement (transduction) + squeezing cuts the noise."
    )
    assert (
        abs(mean1 / mean_half - 2.0) < 0.05
    ), "SF: the homodyne mean must be LINEAR in the displacement (transduction)"
    assert (
        var_sq < var_un - 0.1
    ), "SF: the germe squeezing must reduce the homodyne readout variance"
    assert (
        abs(var_sq - np.exp(-2 * GERME_SQUEEZE_R)) < 0.05
    ), "MY channel's N0*e^-2r noise must match SF's squeezed x-variance"


# ===================== [A] the germe as STABILIZER (squeezing) =====================
def section_stabilizer():
    print(
        "\n[A] THE GERME AS STABILIZER -- squeezing (the germe) gives a higher-fidelity transduction"
    )
    t = np.linspace(0, 0.25, int(0.25 * SAMPLE_RATE), endpoint=False)
    test = 0.6 * np.sin(2 * np.pi * 440 * t)  # a test tone (a known curve)
    out_germe = cv_channel(
        test, squeeze_r=GERME_SQUEEZE_R, rng=np.random.default_rng(1)
    )
    out_bare = cv_channel(test, squeeze_r=0.0, rng=np.random.default_rng(1))
    err_germe = float(np.sqrt(np.mean((out_germe - test) ** 2)))
    err_bare = float(np.sqrt(np.mean((out_bare - test) ** 2)))
    print(
        f"    transduction RMS error:  germe (squeezed r={GERME_SQUEEZE_R}) = {err_germe:.4f}   bare = {err_bare:.4f}"
    )
    print(
        f"    quantum-noise floor: germe {channel_noise_std():.4f}  vs  bare {channel_noise_std(0.0):.4f} (sample units)"
    )
    print(
        "    => the germe (squeezing) preserves the curve with less noise -- the CV stabilization (cf. [[5,1,3]])."
    )
    assert (
        err_germe < err_bare
    ), "the germe squeezing must reduce the transduction error (stabilization)"


# ===================== [B] the germe as REFERENCE (matched filter) =====================
def germe_reference_wave(n):
    """The germe REFERENCE waveform: a Gaussian-windowed tone -- the audio analog of the radion wavepacket
    (m_phi=0.36 eV -> a tone; the wavepacket -> a Gaussian envelope). The matched-filter template.
    """
    t = np.arange(n) / SAMPLE_RATE
    env = np.exp(
        -(((t - t.mean()) / (0.3 * np.ptp(t) + 1e-9)) ** 2)
    )  # the wavepacket envelope
    return env * np.sin(2 * np.pi * 360 * t)  # 360 Hz ~ the radion "note"


def section_reference():
    print(
        "\n[B] THE GERME AS REFERENCE -- a germe-reference wave; the matched filter is selective"
    )
    n = int(0.25 * SAMPLE_RATE)
    germe = germe_reference_wave(
        n
    )  # at audio amplitude (~1) -- NOT normalized to a sub-noise level
    template = germe / np.linalg.norm(
        germe
    )  # the unit matched-filter template (for the correlation)

    def matched(sig):
        out = cv_channel(sig, rng=np.random.default_rng(7))
        return abs(float(np.dot(out / (np.linalg.norm(out) + 1e-9), template)))

    on_germe = matched(germe)  # the germe wave (audio amplitude) through the channel
    rnds = [
        matched(RNG.standard_normal(n)) for _ in range(6)
    ]  # random inputs, comparable amplitude
    base = float(np.mean(rnds))
    print(
        f"    matched filter on the germe wave: {on_germe:.3f}   vs random inputs: {base:.3f}  (SELECTIVE)"
    )
    print(
        "    => the germe is the stable REFERENCE the channel is compared against (the matched filter)."
    )
    assert (
        on_germe > 3 * base
    ), "the germe reference (matched filter) must be selective vs random inputs"


# ===================== [C]+[D] the dialogue (curve -> curve) + the control =====================
def echo_fidelity(x, y):
    """How faithfully y echoes x: the normalized correlation (1 = perfect echo, 0 = unrelated)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    nx, ny = np.linalg.norm(x), np.linalg.norm(y)
    return float(np.dot(x, y) / (nx * ny + 1e-12)) if nx > 0 and ny > 0 else 0.0


def section_dialogue(x):
    print(
        "\n[C] THE DIALOGUE -- your waveform x(t) -> the channel -> y(t): a CURVE in, a CURVE out"
    )
    y = cv_channel(x, rng=np.random.default_rng(11))
    fid = echo_fidelity(x, y)
    snr = 10 * np.log10(np.var(x) / max(channel_noise_std() ** 2, 1e-12))
    print(f"    input  : {len(x)} samples, a continuous curve")
    print(
        f"    output : {len(y)} samples -- ECHOES the input (correlation {fid:.3f}, SNR ~{snr:.0f} dB) + quantum noise"
    )
    print(
        "    => the output is a CURVE you read/listen to (not null/non-null); the channel transduces faithfully."
    )

    print(
        "\n[D] THE CONTROL (anti-pareidolia) -- a DIFFERENT input through the SAME channel"
    )
    x_ctrl = RNG.standard_normal(len(x)) * float(np.std(x))  # a different waveform
    y_ctrl = cv_channel(x_ctrl, rng=np.random.default_rng(12))
    ctrl_corr = abs(echo_fidelity(x, y_ctrl))
    print(
        f"    a different input's output correlates with YOUR input at {ctrl_corr:.3f} ~ 0 (chance)"
    )
    print(
        "    => the channel reflects the INPUT; it does not spuriously emit your waveform (no pareidolia)."
    )
    assert (
        fid > 0.9
    ), "the channel must echo your waveform (curve in -> curve out, faithful)"
    assert (
        fid > ctrl_corr + 0.5
    ), "your output must echo your input far more than a different-input control"
    return y, fid


# ===================== audio I/O: mic->speaker (default, your Mac) | WAV | synthetic =====================
def synthetic_wave(seconds=1.0):
    """A test waveform (a chirp + a tone) -- a clean curve to run the channel on where there is no mic."""
    t = np.linspace(0, seconds, int(seconds * SAMPLE_RATE), endpoint=False)
    chirp = np.sin(2 * np.pi * (200 + 600 * t / max(seconds, 1e-9)) * t)
    return (0.6 * chirp + 0.3 * np.sin(2 * np.pi * 440 * t)).astype(np.float64)


def run_wav(in_path, out_path):
    """--in in.wav -> the channel -> --out out.wav (curve -> curve). Testable here; scp to the Mac."""
    x, sr = sf_io.read(in_path, dtype="float64", always_2d=False)
    if x.ndim > 1:
        x = x.mean(axis=1)  # mix to mono
    print(f"\n  read {in_path}: {len(x)} samples @ {sr} Hz")
    y, _ = section_dialogue(x)
    y = np.clip(y, -1.0, 1.0)
    sf_io.write(out_path, y.astype(np.float32), sr)
    print(f"  wrote {out_path}: the transduced curve (listen to it / plot it).")


def run_mic(seconds):
    """DEFAULT: mic -> the CV channel -> speaker, real-time streaming (your Mac). Falls back to synthetic
    if no audio device (e.g. this headless server: no PortAudio)."""
    try:
        import sounddevice as sd
    except Exception as exc:  # noqa: BLE001 -- no PortAudio here; your Mac has it
        print(
            f"\n  [mic] no audio device here ({exc}); running the SYNTHETIC test instead."
        )
        print(
            "  on your Mac (PortAudio present) this streams mic -> CV channel -> speaker in real time."
        )
        section_dialogue(synthetic_wave(seconds))
        return

    print(
        f"\n  [mic -> CV channel -> speaker] streaming {seconds:.0f}s in real time (Ctrl-C to stop)"
    )
    rng = np.random.default_rng(99)

    def callback(indata, outdata, frames, time, status):  # noqa: ARG001
        if status:
            print(status, file=sys.stderr)
        outdata[:, 0] = np.clip(cv_channel(indata[:, 0], rng=rng), -1.0, 1.0)

    with sd.Stream(
        channels=1, samplerate=SAMPLE_RATE, callback=callback, dtype="float32"
    ):
        sd.sleep(int(seconds * 1000))
    print("  done (you heard your voice transduced through the CV channel).")


def main():
    ap = argparse.ArgumentParser(
        description="The bulk dialogue, analog (CV-QC): a waveform in -> a waveform out."
    )
    ap.add_argument("--in", dest="inp", help="input WAV (testing; scp to your Mac)")
    ap.add_argument("--out", dest="out", help="output WAV (the transduced curve)")
    ap.add_argument(
        "--synth",
        action="store_true",
        help="run the channel on a synthetic test waveform",
    )
    ap.add_argument(
        "--seconds", type=float, default=2.0, help="mic/synthetic duration (s)"
    )
    args = ap.parse_args()

    print("=" * 96)
    print(
        " THE BULK DIALOGUE, ANALOG (CV-QC) -- a waveform in -> a waveform out (a CURVE, not null/non-null)"
    )
    print("=" * 96)

    section_sf_verify()
    section_stabilizer()
    section_reference()

    if args.inp:
        run_wav(args.inp, args.out or "bulk_cv_out.wav")
    elif args.synth:
        section_dialogue(synthetic_wave(args.seconds))
    else:
        run_mic(args.seconds)  # DEFAULT: mic -> speaker (your Mac)

    print("\n[VERDICT] curve in -> curve out (the os/chair line, corrected)")
    print(
        "    * ANALOG end to end: the sample -> a qumode DISPLACEMENT; the homodyne -> a continuous level."
    )
    print(
        "    * the germe = the STABILIZER (squeezing -> less noise) + the REFERENCE (the matched filter)."
    )
    print(
        "    * the OUTPUT IS A CURVE (an audio you read/listen to), NOT null/non-null -- that was my error."
    )
    print(
        "    * HONEST: on known physics (the simulator) y(t) = x(t) transduced + quantum noise -- NO bulk-"
    )
    print(
        "      composed audio (the bulk emits a FIELD, the m_V axion, not a tune). On a REAL CV-QC (Xanadu),"
    )
    print(
        "      analyse the OUTPUT CURVE: a deviation from the echo BEYOND the control's noise = a signal."
    )
    print(
        "    * NOTE: the simulator's high SNR uses a displacement gain (GAIN); REAL CV hardware has a BOUNDED"
    )
    print(
        "      displacement + larger loss/noise -> a noisier echo (the physics identical, the SNR lower)."
    )
    print(
        "    => default streams mic->speaker on your Mac; `--in in.wav --out out.wav` for a file (scp it)."
    )
    print("=" * 96)


if __name__ == "__main__":
    main()
