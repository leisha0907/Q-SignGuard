# Q-SignGuard: System Architecture & API Specification (v1.0)
**Project Team:** Code VERDE  
**Classification:** Information-Theoretic Quantum Digital Signature (QDS) Engine  
**Compliance Target:** ETSI GS QKD 014 / CycloneDX CBOM v1.6  

---

## 1. Architectural System Overview

Q-SignGuard integrates physical-layer quantum state telemetry with FPGA line-rate decision gating to authenticate digital signatures and detect channel eavesdropping without classical computational trapdoors.

### System Pipeline & Boundaries
### Core Security Bounds
* **Detection Probability:** $P(\text{detection}) = 1 - \left(\frac{3}{4}\right)^n$ over $n$ conjugate measurement bases ($X$ and $Z$).
* **Deterministic Threshold:** Rejection boundary hardcoded at $\text{QBER} > 11.0\%$ ($p < 0.001$).
* **Fidelity Gate:** Minimum projection fidelity target $F = \langle \psi | \rho_{\text{rx}} | \psi \rangle \ge 0.99$.

---

## 2. API Specification

Base Endpoint: `https://q-signguard.streamlit.app/api/v1`  
Protocol: HTTPS / JSON (gRPC supported in FPGA runtime)

### Endpoint: `/verify-signature`
Submits teleportation classical bits and channel telemetry for line-rate physical gating.

* **Method:** `POST`
* **Headers:** `Content-Type: application/json`

#### Request Payload
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
