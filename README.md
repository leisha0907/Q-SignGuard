# 🛡️ Q-SignGuard

**Deterministic Quantum Digital Signature (QDS) Engine**
Smart India Hackathon 2026 · Problem ID **SIH26141** · Team **QSentinel**

Live app: `https://q-signguard.streamlit.app/` 

---

## 1. Problem Statement

Classical digital signatures (RSA, ECDSA) rely on computational hardness
assumptions that are broken by Shor's algorithm on a sufficiently large
quantum computer. Q-SignGuard demonstrates a **quantum-secure signature
verification pipeline** for high-value documents (contracts, dispatch
orders) that is information-theoretically secure rather than
computationally secure — its security holds even against an adversary
with unlimited computing power, because it relies on the physics of
quantum measurement, not on math being hard to invert.

## 2. What the Prototype Demonstrates

| Stage | What happens |
|---|---|
| **Document ingestion** | User uploads a PDF/TXT/DOCX contract. A live SHA-256 digest is computed over the raw bytes. |
| **State encoding** | The digest deterministically sets encoding angles (θ, φ) for a payload qubit — i.e. the document's fingerprint is embedded into a quantum state. |
| **Quantum teleportation circuit** | A real 3-qubit circuit is built with Qiskit: payload qubit + a shared Bell pair (⟩Φ+⟩), Bell State Measurement (BSM), and Pauli recovery structure — rendered live as ASCII circuit art. |
| **Syndrome & recovery** | Classical syndrome bits (b1, b0) and the resulting Bob-side Pauli correction (I / X / Y / Z) are shown, along with reconstruction fidelity (target ≥ 99%). |
| **Threat gate (Eve)** | A sidebar toggle simulates an intercept-resend optical-tap attack. Clean-channel QBER sits ~3.5–4.5%; an active tap forces QBER ≥ 27.5%. |
| **Decision** | If QBER ≤ 11% (the standard QKD security threshold), the signature is committed (green banner). Above that, the circuit aborts instantly and the document is locked out (red banner) — this is the wavefunction-collapse-based tamper detection. |
| **Telemetry** | A live Plotly QBER gauge (with the 11% threshold marked) plus KPI cards: FPGA verification time, classical bit overhead, and infrastructure capex. |

## 3. Tech Stack

- **Streamlit** — UI/dashboard shell
- **Qiskit** — quantum circuit construction + ASCII visualization
- **NumPy** — deterministic digest → angle/QBER/fidelity derivation
- **Plotly** — QBER gauge telemetry
- **hashlib (stdlib)** — SHA-256 document digesting

No GPU, no quantum hardware access, and no `qiskit-aer` execution backend
are required — the app is self-contained and runs anywhere Python does.

## 4. Running Locally

```bash
git clone <your-repo-url>
cd q-signguard
pip install -r requirements.txt
streamlit run app.py
```

Open the printed local URL (typically `http://localhost:8501`). If you
don't upload a file, the app automatically falls back to a bundled
`default_tactical_dispatch.pdf` payload so the dashboard is never empty
— useful for a quick judge walkthrough with zero setup.

## 5. Demo Script (suggested judge walkthrough)

1. Load the app — note the SHA-256 digest of the default fallback document and the green "Signature Committed" banner with QBER ~4%.
2. Point out the live-rendered Qiskit circuit and the Pauli recovery panel (I/X/Y/Z + fidelity ≥ 99%).
3. Upload a real document — show the digest change, and that θ/φ/b1/b0 change deterministically with it.
4. Flip **"Inject Eve Attack (Optical Tap)"** in the sidebar — QBER jumps to ≥27.5%, the gauge crosses into the red zone, and the banner instantly switches to "Circuit Abort — Document Locked Out."
5. Flip Eve off again to show the system recovers to nominal operation — no manual reset needed, it's fully reactive to channel state.

## 6. Deployment Notes (Streamlit Community Cloud)

**Dependency pins matter here — please read before touching `requirements.txt`.**

As of this build, Streamlit Community Cloud is defaulting new deploys to
**Python 3.14**, a very new interpreter release. Several native-extension
packages don't yet have prebuilt wheels for it, which can cause either:

- a **build-time failure** (pip tries to compile a package from source and
  is missing a required tool, e.g. `cmake`), or
- a **runtime segmentation fault** (a native extension loads but is
  ABI-incompatible with the interpreter — this shows up as a crash with
  no Python traceback in the deploy logs).

The pinned versions in `requirements.txt` were verified against live
deploy logs to install from prebuilt wheels on this environment:

- `qiskit==2.5.2` — do **not** downgrade to `qiskit<2.0`; older releases
  depend on `symengine`, which has no Python 3.14 wheel and fails to
  build from source in Streamlit Cloud's build image.
- `numpy==2.5.3` — has a prebuilt cp314 wheel; older pins (e.g. `1.26.4`)
  fall back to a slow source build.
- `qiskit-aer` is intentionally **not** included — `app.py` never imports
  it, and it's an extra native-extension package with no functional
  benefit here.

If you need to pin an older, more widely-tested Python version instead
(e.g. 3.11), note that `runtime.txt` has been unreliable on Community
Cloud recently — the supported path is: delete the deployed app, then
redeploy the same repo and explicitly choose the Python version in the
**Advanced settings** dialog at deploy time (Python version cannot be
changed on an already-deployed app).

## 7. Project Structure

```
.
├── app.py              # Single-file Streamlit application (entire prototype)
├── requirements.txt    # Locked, wheel-verified dependency set
└── README.md           # This file
```

## 8. Team

**Team QSentinel** — Smart India Hackathon 2026 · Problem ID SIH26141
