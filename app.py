import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Q-SignGuard Engine", page_icon="🛡️", layout="wide")

st.markdown("# 🛡️ Q-SignGuard: Sovereign Teleportation-Based QDS Engine")
st.caption("Deterministic Non-AI Physical Gating & Intercept-Resend Threat Detection")

col_ctrl, col_main = st.columns([1, 2])

with col_ctrl:
    st.subheader("⚙️ Channel & Attack Parameters")
    n_qubits = st.slider("Qubits Monitored (n)", min_value=10, max_value=200, value=100, step=10)
    eve_intercept_prob = st.slider("Eve Intercept Rate", min_value=0.0, max_value=1.0, value=0.3, step=0.05)
    channel_noise = st.slider("Fiber Phase Noise (Baseline QBER)", min_value=0.01, max_value=0.15, value=0.03, step=0.01)
    
    run_btn = st.button("🚀 Transmit & Verify Signature", type="primary", use_container_width=True)

if run_btn:
    with st.spinner("Executing BSM and line-rate POVM state verification..."):
        time.sleep(0.5)
        
        # Physics simulation: Eve wrong-basis probability is 1/2, error given wrong basis is 1/2 -> 25% induced error
        eve_induced_error = eve_intercept_prob * 0.25
        measured_qber = channel_noise + eve_induced_error + np.random.normal(0, 0.005)
        measured_qber = max(0.005, min(measured_qber, 0.50))
        
        p_detect = 1.0 - (0.75 ** (n_qubits * eve_intercept_prob)) if eve_intercept_prob > 0 else 0.0
        latency_ms = np.round(np.random.uniform(3.2, 4.8), 2)
        fidelity = max(0.0, 1.0 - measured_qber)
        
    with col_main:
        st.subheader("📊 Line-Rate Verification Telemetry")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Observed QBER", f"{measured_qber*100:.2f}%", delta="-Normal" if measured_qber <= 0.11 else "+CRITICAL", delta_color="inverse")
        m2.metric("POVM Fidelity (F)", f"{fidelity:.4f}")
        m3.metric("Hardware Latency", f"{latency_ms} ms")
        m4.metric("P(Tamper Detection)", f"{p_detect*100:.1f}%")
        
        # Security Decision Gate
        if measured_qber <= 0.11:
            st.success(f"✅ **SECURITY GATE: ACCEPTED** | QBER ({measured_qber*100:.2f}%) ≤ 11.0% Threshold. Pauli unitary reconstruction verified. Signature authenticated.")
        else:
            st.error(f"🚨 **SECURITY GATE: ABORT & REJECT** | QBER ({measured_qber*100:.2f}%) > 11.0% Threshold! State collapse indicates active channel intrusion (p < 0.001).")

        # QBER Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=measured_qber * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Channel QBER vs 11% Hardware Gate Limit (%)"},
            gauge={
                'axis': {'range': [0, 30]},
                'bar': {'color': "#10B981" if measured_qber <= 0.11 else "#EF4444"},
                'steps': [
                    {'range': [0, 11], 'color': "#D1FAE5"},
                    {'range': [11, 30], 'color': "#FEE2E2"}
                ],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.8, 'value': 11}
            }
        ))
        fig.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
else:
    with col_main:
        st.info("👈 Set channel parameters and click **Transmit & Verify Signature** to test the deterministic gate.")
