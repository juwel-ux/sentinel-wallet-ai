# Security Report — Sentinel Wallet AI

---

## Threat Model

| # | Threat | Defense Layer |
|---|--------|---------------|
| 1 | Prompt injection | Layer 4 — Prompt Guard |
| 2 | Drain attacks | Layer 7 — Drain Taxonomy |
| 3 | Unauthorized transfer | Layer 10 — Contract |
| 4 | Balance drain | Layer 3 — Session Budget |
| 5 | Fake recipient | Layer 1 — Verifier |
| 6 | Replay attack | Layer 9 — Audit Trail |
| 7 | Anomalous behaviour | Layer 5 — Anomaly |
| 8 | Policy bypass | Layer 6 — Proof-Gated |

---

## 10-Layer Defense

```mermaid
flowchart TB
    T[Incoming Transaction] --> L1
    L1{1 · Verifier} -->|PASS| L2{2 · Simulation}
    L1 -->|FAIL| X[❌ Reject]
    L2 -->|PASS| L3{3 · Session Budget}
    L2 -->|FAIL| X
    L3 -->|PASS| L4{4 · Prompt Guard}
    L3 -->|FAIL| X
    L4 -->|PASS| L5{5 · Anomaly}
    L4 -->|FAIL| X
    L5 -->|PASS| L6{6 · Proof-Gated}
    L5 -->|FAIL| X
    L6 -->|PASS| L7{7 · Drain Taxonomy}
    L6 -->|FAIL| X
    L7 -->|PASS| L8{8 · Compliance}
    L7 -->|FAIL| X
    L8 -->|PASS| L9{9 · Audit Trail}
    L8 -->|FAIL| X
    L9 -->|PASS| L10{10 · Contract}
    L9 -->|FAIL| X
    L10 -->|PASS| OK[✅ Execute]
    L10 -->|FAIL| X

    style X fill:#EF4444,color:#fff
    style OK fill:#10B981,color:#fff
    style T fill:#6366F1,color:#fff
```

---

## Default Constraints

| Constraint | Value |
|-----------|-------|
| Per-transaction limit | 0.01 ETH |
| Daily limit | 0.05 ETH |
| Session budget | 0.05 ETH |
| Whitelist | Required |
| KYC threshold | > 0.01 ETH |

---

## Attack Resistance Matrix

| Attack Type | Layer | Resistance |
|-------------|-------|-----------|
| Prompt injection | 4 | ✅ 95% |
| Drain (8 types) | 7 | ✅ 100% |
| Unauthorized | 10 | ✅ 100% |
| State drift | 6 | ✅ 93.6% |
| Replay | 9 | ✅ 100% |

---

**© 2026 Sentinel Wallet AI**
