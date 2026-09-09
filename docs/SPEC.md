# Q-SignGuard: System Architecture & Target Specification (v1.1)

**Project Team:** QSentinel
**Problem ID:** SIH26141
**Classification:** Information-Theoretic Quantum Digital Signature (QDS) Engine — Target Architecture
**Compliance Target (Roadmap, not yet implemented):** ETSI GS QKD 014 / CycloneDX CBOM v1.6

---

> ### ⚠️ Document Status: Target Architecture / Roadmap
> This document describes the **production system Q-SignGuard is designed
> toward** — not the current hackathon prototype as-built. Everything in
> Section 1 is implemented and demoable today at
> `https://q-signguard.streamlit.app/`. Everything from Section 3 onward
> (the REST/gRPC API, FPGA line-rate execution, ETSI/CycloneDX compliance)
> is **design intent for a future production build**, included here to
> show the path from prototype to deployable system. No endpoint in this
> document is currently live — the deployed Streamlit app is a dashboard,
> not an API server.

---

## 1. What's Implemented in the Current Prototype

Live, demoable today, single-process, no external services:

| Component | Status |
|---|---|
| Streamlit dashboard (`app.py`) | ✅ Implemented |
| SHA-256 document digesting | ✅ Implemented |
| Digest → qubit state encoding (θ, φ) | ✅ Implemented |
| Qiskit 3-qubit teleportation circuit (built + rendered as ASCII) | ✅ Implemented |
| Syndrome bits (b1, b0) → Pauli recovery mapping (I/X/Y/Z) | ✅ Implemented, derived deterministically from digest |
| Eve intercept-resend simulation (sidebar toggle) | ✅ Implemented |
| QBER gate at 11% threshold, pass/abort banners | ✅ Implemented |
| Plotly QBER gauge + KPI telemetry cards | ✅ Implemented |
| Real optical hardware / dark fiber link | ❌ Not implemented — QBER/fidelity values are digest-seeded pseudo-random numbers modeling expected clean vs. attacked channel behavior |
| FPGA execution | ❌ Not implemented — "FPGA Verification Time" is a simulated KPI, not measured on real hardware |
| REST/gRPC API server | ❌ Not implemented — see Section 3 |
| ETSI GS QKD 014 / CycloneDX CBOM compliance | ❌ Not implemented — see Section 4 |

## 2. Core Security Model

This is the theoretical model the prototype's simulated QBER/fidelity
values are built around — the physics Q-SignGuard's threat gate is
designed to reflect once connected to a real quantum channel.

* **Detection Probability:** $P(\text{detection}) = 1 - \left(\frac{3}{4}\right)^n$ over $n$ conjugate measurement bases ($X$ and $Z$).
* **Deterministic Threshold:** Rejection boundary hardcoded at $\text{QBER} > 11.0\%$ ($p < 0.001$).
* **Fidelity Gate:** Minimum projection fidelity target $F = \langle \psi | \rho_{\text{rx}} | \psi \rangle \ge 0.99$.

---

## 3. Target API Specification (Design Intent — Not Yet Built)

> The interface below is a **proposed design** for a future production
> service, not a live endpoint. It illustrates how Q-SignGuard's
> verification logic would be exposed to an external system (e.g. a
> document-management platform or SIEM) once the prototype's in-app
> simulation is replaced with a real quantum-channel backend.

Proposed base endpoint (placeholder — no server currently exists here):
`https://api.q-signguard.example/v1`
Protocol: HTTPS / JSON (gRPC proposed for FPGA runtime)

### Endpoint: `/verify-signature` *(proposed)*
Would submit teleportation classical bits and channel telemetry for
line-rate physical gating.

* **Method:** `POST`
* **Headers:** `Content-Type: application/json`

#### Request Payload (proposed shape)
```json
{
  "transaction_id": "tx_c4isr_8829104",
  "qubits_monitored": 100,
  "classical_token": {
    "b0": 1,
    "b1": 0,
    "bsm_basis": "Bell-Phi-Plus"
  },
  "channel_telemetry": {
    "observed_qber": 0.042,
    "dark_count_rate_hz": 120,
    "baseline_attenuation_db": 3.2
  }
}
```

#### Response — Pass Case (proposed shape)
```json
{
  "status": "ACCEPTED",
  "decision_code": "GATE_PASS_01",
  "latency_ms": 3.82,
  "metrics": {
    "qber": 0.042,
    "povm_fidelity": 0.958,
    "tamper_detection_probability": 0.9998,
    "p_value": 0.0001
  },
  "audit": {
    "algorithm": "QDS-Teleportation-POVM",
    "cbom_compliance": "CycloneDX-1.6-Passed"
  }
}
```

#### Response — Abort Case (proposed shape)
```json
{
  "status": "ABORT_AND_REJECT",
  "decision_code": "INTRUSION_DETECTED",
  "latency_ms": 4.12,
  "metrics": {
    "qber": 0.148,
    "povm_fidelity": 0.852,
    "tamper_detection_probability": 1.0,
    "p_value": 0.00001
  },
  "alert": {
    "threat_type": "Intercept-Resend / Active Tap",
    "mitigation": "Quantum state collapsed; classical key revoked; SIEM alert dispatched"
  }
}
```

---

## 4. Target Compliance Artifact — CycloneDX CBOM (Design Intent)

> Illustrative only. No CBOM tooling is currently wired into this repo;
> this is the shape a compliance artifact would take once one is added.

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.6",
  "component": {
    "name": "Q-SignGuard Core",
    "type": "cryptographic-asset",
    "cryptoProperties": {
      "assetType": "protocol",
      "algorithmProperties": {
        "primitive": "quantum-digital-signature",
        "parameterSetIdentifier": "ITS-Teleportation-POVM-100q",
        "executionEnvironment": "FPGA line-rate",
        "nistQuantumSecurityLevel": "Level 5+ (Information-Theoretic)"
      }
    }
  }
}
```

---

## 5. Path from Prototype to This Target

1. **Now (SIH26141 prototype):** in-app simulation of the protocol, digest-derived QBER/fidelity, Streamlit UI, Qiskit circuit visualization.
2. **Next:** extract verification logic from `app.py` into a standalone service; wrap it with the `/verify-signature` API above.
3. **Then:** replace simulated telemetry with real photon-counting hardware over dark fiber; move the decision gate onto FPGA for true line-rate latency.
4. **Then:** formal compliance work — ETSI GS QKD 014 conformance testing, CycloneDX CBOM generation, third-party security audit.

---

**Team QSentinel** — Smart India Hackathon 2026 · Problem ID SIH26141
