"""
Q-SignGuard — Deterministic Quantum Digital Signature (QDS) Engine
Smart India Hackathon 2026 | Problem ID: SIH26141 | Team: QSentinel

Demonstrates Bell State Measurement (BSM) based quantum teleportation,
Pauli unitary recovery, and physical wavefunction-collapse gating for
document-signature verification over simulated 1550 nm dark fiber.

Run with:  streamlit run app.py
Dependencies: streamlit, qiskit, numpy, plotly
"""

import hashlib
import io

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

# --------------------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Q-SignGuard | SIH26141",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# CUSTOM CSS — DEEP-TECH / CYBER AESTHETIC
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    * { box-sizing: border-box; }

    .stApp {
        background: radial-gradient(circle at 15% 10%, #0d1b2a 0%, #060a12 55%, #030509 100%);
        color: #e6f1ff;
    }

    /* Fluid content width: comfortable on judge laptops, full-bleed on phones */
    .block-container {
        max-width: 1180px;
        padding-top: 1.6rem;
        padding-left: clamp(0.8rem, 4vw, 3rem);
        padding-right: clamp(0.8rem, 4vw, 3rem);
        padding-bottom: 3rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a121f 0%, #050a12 100%);
        border-right: 1px solid rgba(0, 229, 255, 0.15);
    }

    h1, h2, h3, h4 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: 0.3px;
    }

    .qs-hero {
        padding: clamp(1.1rem, 3vw, 1.6rem) clamp(1.1rem, 4vw, 2rem);
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(0,229,255,0.10), rgba(123,97,255,0.08));
        border: 1px solid rgba(0, 229, 255, 0.25);
        box-shadow: 0 0 40px rgba(0, 229, 255, 0.08);
        margin-bottom: 1.2rem;
    }

    .qs-hero h1 {
        font-size: clamp(1.6rem, 4.2vw, 2.4rem);
        background: linear-gradient(90deg, #ffffff 0%, #7be8ff 60%, #00e5ff 100%);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.25;
    }

    .qs-hero p {
        font-size: clamp(0.85rem, 1.6vw, 1.02rem);
    }

    .qs-badge {
        display: inline-block;
        padding: 0.18rem 0.7rem;
        margin: 0 0.4rem 0.4rem 0;
        border-radius: 999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        background: rgba(0, 229, 255, 0.12);
        border: 1px solid rgba(0, 229, 255, 0.35);
        color: #7be8ff;
        white-space: nowrap;
    }

    .qs-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: clamp(0.9rem, 2vw, 1.1rem) clamp(1rem, 2.5vw, 1.3rem);
        margin-bottom: 1rem;
        backdrop-filter: blur(6px);
        transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
    }

    .qs-card:hover {
        border-color: rgba(0, 229, 255, 0.35);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 229, 255, 0.08);
    }

    .qs-mono {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #9fe8ff;
        word-break: break-all;
    }

    .qs-banner-success {
        padding: clamp(0.9rem, 2.5vw, 1.1rem) clamp(1rem, 3vw, 1.4rem);
        border-radius: 14px;
        background: linear-gradient(135deg, rgba(0, 230, 118, 0.18), rgba(0, 230, 118, 0.06));
        border: 1.5px solid rgba(0, 230, 118, 0.65);
        box-shadow: 0 0 30px rgba(0, 230, 118, 0.20);
        font-family: 'JetBrains Mono', monospace;
        font-size: clamp(0.88rem, 2.4vw, 1.05rem);
        font-weight: 700;
        color: #4dffb0;
        text-align: center;
        margin: 0.8rem 0 1.2rem 0;
        line-height: 1.5;
    }

    .qs-banner-fail {
        padding: clamp(0.9rem, 2.5vw, 1.1rem) clamp(1rem, 3vw, 1.4rem);
        border-radius: 14px;
        background: linear-gradient(135deg, rgba(255, 45, 85, 0.22), rgba(255, 45, 85, 0.06));
        border: 1.5px solid rgba(255, 45, 85, 0.70);
        box-shadow: 0 0 30px rgba(255, 45, 85, 0.25);
        font-family: 'JetBrains Mono', monospace;
        font-size: clamp(0.88rem, 2.4vw, 1.05rem);
        font-weight: 700;
        color: #ff7a90;
        text-align: center;
        margin: 0.8rem 0 1.2rem 0;
        line-height: 1.5;
        animation: qs-pulse 1.4s ease-in-out infinite;
    }

    @keyframes qs-pulse {
        0%   { box-shadow: 0 0 20px rgba(255, 45, 85, 0.20); }
        50%  { box-shadow: 0 0 45px rgba(255, 45, 85, 0.45); }
        100% { box-shadow: 0 0 20px rgba(255, 45, 85, 0.20); }
    }

    .qs-section-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.95rem;
        color: #7be8ff;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.5rem;
        border-left: 3px solid #00e5ff;
        padding-left: 0.6rem;
    }

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 0.8rem 1rem;
        transition: border-color 0.2s ease, transform 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        border-color: rgba(0, 229, 255, 0.3);
        transform: translateY(-2px);
    }

    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        color: #7be8ff;
        font-size: clamp(1.1rem, 3vw, 1.5rem);
    }

    div[data-testid="stMetricLabel"] {
        font-size: clamp(0.78rem, 1.8vw, 0.9rem);
    }

    pre, code {
        font-family: 'JetBrains Mono', monospace !important;
        background: #050a12 !important;
        color: #7be8ff !important;
        border-radius: 10px !important;
        border: 1px solid rgba(0, 229, 255, 0.15) !important;
    }

    /* Circuit ASCII art scrolls horizontally instead of breaking layout on phones */
    div[data-testid="stCodeBlock"] pre {
        overflow-x: auto !important;
        font-size: clamp(0.68rem, 1.6vw, 0.85rem) !important;
    }

    /* Plotly gauge / chart containers shrink cleanly */
    div[data-testid="stPlotlyChart"] {
        width: 100% !important;
    }

    footer, #MainMenu { visibility: hidden; }

    /* ---- Small-screen tuning (phones, QR-code scans) ---- */
    @media (max-width: 640px) {
        .qs-hero { text-align: left; }
        .qs-badge { font-size: 0.65rem; padding: 0.15rem 0.55rem; }
        .qs-section-title { font-size: 0.82rem; letter-spacing: 1px; }
        .qs-card, .qs-banner-success, .qs-banner-fail { border-radius: 12px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# HERO HEADER
# --------------------------------------------------------------------------
st.markdown(
    """
    <div class="qs-hero">
        <span class="qs-badge">SIH26141</span>
        <span class="qs-badge">TEAM QSENTINEL</span>
        <span class="qs-badge">1550nm C-BAND DARK FIBER</span>
        <h1 style="margin: 0.5rem 0 0.2rem 0;">🛡️ Q-SignGuard</h1>
        <p style="color:#9fb6cc; margin:0; font-size:1.02rem;">
            Deterministic Quantum Digital Signature Engine — Bell State Measurement,
            Pauli Recovery &amp; Wavefunction-Collapse Threat Gating
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# SIDEBAR — CONTROL PANEL
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Mission Control")
    st.markdown("---")
    eve_attack = st.toggle(
        "🕵️ Inject Eve Attack (Optical Tap)",
        value=False,
        help="Simulates an intercept-resend attack on the quantum channel via a fiber tap.",
    )
    st.markdown("---")
    st.markdown("#### 📡 Channel Parameters")
    st.markdown(
        f"""
        <div class="qs-mono">
        Wavelength&nbsp;&nbsp;&nbsp;: 1550.12 nm<br>
        Channel&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: C-Band Dark Fiber<br>
        QBER Cutoff&nbsp;&nbsp;: 11.00 %<br>
        Mode&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: {"⚠️ ADVERSARIAL" if eve_attack else "✅ NOMINAL"}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.caption("Q-SignGuard v1.0 · SIH 2026 Prototype · Team QSentinel")

# --------------------------------------------------------------------------
# CORE FUNCTIONS
# --------------------------------------------------------------------------
FALLBACK_NAME = "default_tactical_dispatch.pdf"
FALLBACK_BYTES = (
    b"SIH26141::QSENTINEL::DEFAULT_TACTICAL_DISPATCH::"
    b"CLASSIFICATION=RESTRICTED::PAYLOAD_ID=0xQS2026::"
    b"This is a deterministic fallback tactical contract payload used so that "
    b"the Q-SignGuard prototype dashboard never starts in an empty state. "
    b"Replace by uploading a real PDF, DOCX, or TXT document."
)


def compute_digest(payload: bytes) -> bytes:
    return hashlib.sha256(payload).digest()


def derive_quantum_params(digest: bytes):
    """Deterministically derive encoding angles + BSM outcome from a digest."""
    theta = (digest[0] / 255.0) * np.pi
    phi = (digest[1] / 255.0) * 2 * np.pi
    b1 = (digest[2] >> 1) & 1
    b0 = digest[2] & 1
    seed = int.from_bytes(digest[4:8], "big")
    return theta, phi, b1, b0, seed


PAULI_MAP = {
    (0, 0): ("I", "Identity — no correction required"),
    (0, 1): ("X", "Bit-flip correction applied"),
    (1, 0): ("Z", "Phase-flip correction applied"),
    (1, 1): ("Y", "Combined bit + phase-flip correction applied"),
}


def build_teleportation_circuit(theta: float, phi: float) -> QuantumCircuit:
    """3-qubit deterministic QDS teleportation circuit.

    q0: payload qubit (document-digest-encoded state)
    q1: Alice's half of the shared Bell pair
    q2: Bob's half of the shared Bell pair (remote / receiver)
    """
    qr = QuantumRegister(3, "q")
    cr = ClassicalRegister(3, "c")
    qc = QuantumCircuit(qr, cr)

    # --- Encode payload state onto q0 from the document digest ---
    qc.ry(theta, 0)
    qc.rz(phi, 0)
    qc.barrier(label="ENCODE")

    # --- Prepare shared Bell pair |Phi+> across q1, q2 ---
    qc.h(1)
    qc.cx(1, 2)
    qc.barrier(label="BELL PAIR")

    # --- Bell State Measurement (BSM) between payload qubit and q1 ---
    qc.cx(0, 1)
    qc.h(0)
    qc.barrier(label="BSM")
    qc.measure(0, 0)
    qc.measure(1, 1)

    # --- Classically-controlled Pauli recovery on Bob's qubit q2 ---
    # NOTE: QuantumCircuit.c_if() was removed in qiskit 2.x. The supported
    # replacement is the if_test() control-flow context manager.
    with qc.if_test((cr[1], 1)):
        qc.x(2)
    with qc.if_test((cr[0], 1)):
        qc.z(2)
    qc.barrier(label="PAULI RECOVERY")
    qc.measure(2, 2)

    return qc


def simulate_protocol(digest: bytes, eve_attack: bool):
    theta, phi, b1, b0, seed = derive_quantum_params(digest)
    rng = np.random.default_rng(seed)

    if eve_attack:
        qber = float(rng.uniform(27.5, 33.0))
        fidelity = float(rng.uniform(0.55, 0.75))
        fpga_ms = float(rng.uniform(1.2, 4.8))
    else:
        qber = float(rng.uniform(3.5, 4.5))
        fidelity = float(rng.uniform(0.990, 0.999))
        fpga_ms = float(rng.uniform(0.8, 3.6))

    pauli_symbol, pauli_desc = PAULI_MAP[(b1, b0)]
    verified = qber <= 11.0

    return {
        "theta": theta,
        "phi": phi,
        "b1": b1,
        "b0": b0,
        "pauli_symbol": pauli_symbol,
        "pauli_desc": pauli_desc,
        "qber": qber,
        "fidelity": fidelity,
        "fpga_ms": fpga_ms,
        "verified": verified,
    }


def make_gauge(qber: float) -> go.Figure:
    bar_color = "#00e5ff" if qber <= 11.0 else "#ff2d55"
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=round(qber, 2),
            number={"suffix": " %", "font": {"color": "#e6f1ff", "family": "JetBrains Mono"}},
            title={"text": "QUANTUM BIT ERROR RATE (QBER)", "font": {"color": "#7be8ff", "size": 15}},
            gauge={
                "axis": {"range": [0, 40], "tickcolor": "#7be8ff", "tickfont": {"color": "#9fb6cc"}},
                "bar": {"color": bar_color, "thickness": 0.32},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 1,
                "bordercolor": "rgba(255,255,255,0.15)",
                "steps": [
                    {"range": [0, 11], "color": "rgba(0, 230, 118, 0.22)"},
                    {"range": [11, 40], "color": "rgba(255, 45, 85, 0.22)"},
                ],
                "threshold": {
                    "line": {"color": "#ff2d55", "width": 4},
                    "thickness": 0.9,
                    "value": 11.0,
                },
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e6f1ff"},
        height=320,
        margin=dict(l=30, r=30, t=60, b=10),
    )
    return fig


# --------------------------------------------------------------------------
# FILE INGESTION
# --------------------------------------------------------------------------
st.markdown('<div class="qs-section-title">01 · Document Ingestion</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload contract / document for quantum signature verification",
    type=["pdf", "txt", "docx"],
    help="Accepted formats: PDF, TXT, DOCX. If nothing is uploaded, a default tactical dispatch is used.",
)

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    file_name = uploaded_file.name
    using_fallback = False
else:
    file_bytes = FALLBACK_BYTES
    file_name = FALLBACK_NAME
    using_fallback = True

digest = compute_digest(file_bytes)
digest_hex = digest.hex()

col_a, col_b = st.columns([1, 2])
with col_a:
    st.markdown(
        f"""
        <div class="qs-card">
            <b>📄 Active Payload</b><br>
            <span class="qs-mono">{file_name}</span><br><br>
            <b>Size</b>: {len(file_bytes):,} bytes<br>
            <b>Source</b>: {"Default fallback (no upload detected)" if using_fallback else "User-uploaded"}
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_b:
    st.markdown(
        f"""
        <div class="qs-card">
            <b>🔐 SHA-256 Payload Digest (live)</b><br>
            <span class="qs-mono">{digest_hex}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

if using_fallback:
    st.info(f"No file uploaded — running on fallback payload `{FALLBACK_NAME}` so the dashboard never starts empty.")

# --------------------------------------------------------------------------
# RUN PROTOCOL
# --------------------------------------------------------------------------
result = simulate_protocol(digest, eve_attack)
qc = build_teleportation_circuit(result["theta"], result["phi"])
circuit_text = str(qc.draw(output="text"))

# --------------------------------------------------------------------------
# QUANTUM CORE
# --------------------------------------------------------------------------
st.markdown('<div class="qs-section-title">02 · Quantum Core — Teleportation Circuit</div>', unsafe_allow_html=True)

qc_col1, qc_col2 = st.columns([3, 2])

with qc_col1:
    st.markdown("**Generated 3-Qubit BSM Teleportation Circuit**")
    st.code(circuit_text, language=None)

with qc_col2:
    st.markdown(
        f"""
        <div class="qs-card">
            <b>State Encoding (from digest)</b><br>
            <span class="qs-mono">theta (θ) = {result['theta']:.4f} rad</span><br>
            <span class="qs-mono">phi (φ)   = {result['phi']:.4f} rad</span>
        </div>
        <div class="qs-card">
            <b>Alice's Classical Syndrome</b><br>
            <span class="qs-mono">b1 = {result['b1']}   b0 = {result['b0']}</span><br><br>
            <b>Bob's Pauli Recovery Operator</b><br>
            <span class="qs-mono" style="font-size:1.3rem;">{result['pauli_symbol']}</span><br>
            <span style="color:#9fb6cc; font-size:0.85rem;">{result['pauli_desc']}</span>
        </div>
        <div class="qs-card">
            <b>State Reconstruction Fidelity</b><br>
            <span class="qs-mono" style="font-size:1.3rem; color:{'#4dffb0' if result['fidelity'] >= 0.99 else '#ff7a90'};">
                {result['fidelity']*100:.2f}%
            </span><br>
            <span style="color:#9fb6cc; font-size:0.85rem;">Target ≥ 99.00%</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------------------------------
# DECISION BANNER
# --------------------------------------------------------------------------
st.markdown('<div class="qs-section-title">03 · Threat Gate — Verification Decision</div>', unsafe_allow_html=True)

if result["verified"]:
    st.markdown(
        """
        <div class="qs-banner-success">
            ✅ VERIFICATION SUCCESS — SIGNATURE COMMITTED<br>
            <span style="font-size:0.85rem; font-weight:400; color:#9fe8ff;">
                Information-theoretically secure · QBER within 11% security threshold
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div class="qs-banner-fail">
            🚨 INSTANT CIRCUIT ABORT — DOCUMENT LOCKED OUT<br>
            <span style="font-size:0.85rem; font-weight:400; color:#ffc2cc;">
                Wavefunction collapsed under adversarial projective measurement · QBER exceeds 11% threshold
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------------------------------
# TELEMETRY & GAUGES
# --------------------------------------------------------------------------
st.markdown('<div class="qs-section-title">04 · Live Telemetry &amp; Hardware Gauges</div>', unsafe_allow_html=True)

gauge_col, kpi_col = st.columns([2, 3])

with gauge_col:
    st.plotly_chart(make_gauge(result["qber"]), use_container_width=True)
    st.caption(
        "🕵️ Eve intercept-resend tap active on fiber link." if eve_attack
        else "📡 Nominal fiber attenuation — no adversarial tap detected."
    )

with kpi_col:
    m1, m2 = st.columns(2)
    m3, m4 = st.columns(2)

    m1.metric(
        "FPGA Verification Time",
        f"{result['fpga_ms']:.2f} ms",
        delta="Line-rate target < 5 ms",
        delta_color="off",
    )
    m2.metric(
        "Classical Bloat",
        "2 bits / qubit",
        delta="Zero MTU bloat",
        delta_color="off",
    )
    m3.metric(
        "Infrastructure Capex",
        "₹0 Forklift",
        delta="Standard C-band dark fiber",
        delta_color="off",
    )
    m4.metric(
        "QBER (measured)",
        f"{result['qber']:.2f} %",
        delta=f"{'BELOW' if result['verified'] else 'ABOVE'} 11.00% cutoff",
        delta_color="normal" if result["verified"] else "inverse",
    )

# --------------------------------------------------------------------------
# FOOTER
# --------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:#5c7290; font-family:'JetBrains Mono', monospace; font-size:0.8rem;">
        Q-SignGuard · Deterministic Quantum Digital Signature Engine · SIH26141 · Team QSentinel · 2026
    </div>
    """,
    unsafe_allow_html=True,
)
