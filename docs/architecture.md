# Sentinel Wallet AI — System Architecture

> **Autonomous On-Chain Financial Agent with Hard Security Constraints**

---

## 1. High-Level System Architecture

```mermaid
flowchart TB
    subgraph USER["👤 User Layer"]
        U1[Voice Input<br/>Bengali · English · Chinese]
        U2[Text Input]
    end

    subgraph FRONTEND["📱 Frontend — Flutter Web"]
        F1[Chat Interface]
        F2[Dashboard]
        F3[Security Center]
        F4[Transaction History]
    end

    subgraph API["🌐 API Layer — FastAPI + Nginx"]
        A1[REST Endpoints]
        A2[Static File Server]
    end

    subgraph AI["🧠 AI Intelligence Layer"]
        AI1[NLP Parser<br/>BN / EN / ZH]
        AI2[LLM Agent<br/>Ollama llama3.2:3b]
        AI3[Conversation Engine]
        AI4[30+ Feature Modules]
    end

    subgraph SEC["🛡️ Security Layer — 10 Layers"]
        S1[Verifier Agent]
        S2[Simulation Engine]
        S3[Session Budget]
        S4[Prompt Guard]
        S5[Anomaly Detection]
    end

    subgraph CHAIN["⛓️ Blockchain Layer"]
        C1[AgentGuard Contract<br/>Solidity 0.8.19]
        C2[Ethereum<br/>Ganache · Sepolia]
    end

    U1 --> F1
    U2 --> F1
    F1 --> A1
    F2 --> A1
    F3 --> A1
    F4 --> A1
    A1 --> AI1
    AI1 --> AI2
    AI2 --> AI3
    AI3 --> AI4
    AI4 --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> C1
    C1 --> C2

    style USER fill:#6366F1,color:#fff
    style FRONTEND fill:#8B5CF6,color:#fff
    style API fill:#10B981,color:#fff
    style AI fill:#F59E0B,color:#fff
    style SEC fill:#EF4444,color:#fff
    style CHAIN fill:#1F2937,color:#fff
```

---

## 2. Security Pipeline — 10 Layers

Every transaction must pass **all 10 layers** before execution:

```mermaid
flowchart LR
    Start([User Command]) --> L1
    L1[1 · Verifier] --> L2[2 · Simulation]
    L2 --> L3[3 · Session Budget]
    L3 --> L4[4 · Prompt Guard]
    L4 --> L5[5 · Anomaly]
    L5 --> L6[6 · Proof-Gated]
    L6 --> L7[7 · Drain Taxonomy]
    L7 --> L8[8 · Compliance]
    L8 --> L9[9 · Audit Trail]
    L9 --> L10[10 · Smart Contract]
    L10 --> End([✅ Transaction Executed])

    style Start fill:#6366F1,color:#fff
    style End fill:#10B981,color:#fff
    style L1 fill:#EF4444,color:#fff
    style L2 fill:#F59E0B,color:#fff
    style L3 fill:#F59E0B,color:#fff
    style L4 fill:#F59E0B,color:#fff
    style L5 fill:#F59E0B,color:#fff
    style L6 fill:#EF4444,color:#fff
    style L7 fill:#EF4444,color:#fff
    style L8 fill:#EF4444,color:#fff
    style L9 fill:#EF4444,color:#fff
    style L10 fill:#8B5CF6,color:#fff
```

---

## 3. Transaction Sequence — End-to-End

```mermaid
sequenceDiagram
    autonumber
    participant U as 👤 User
    participant F as 📱 Flutter App
    participant A as 🌐 FastAPI
    participant N as 🧠 NLP Parser
    participant S as 🛡️ Security
    participant C as 📜 Contract
    participant B as ⛓️ Blockchain

    U->>F: "send 0.009 ETH to rahim"
    F->>A: POST /command
    A->>N: parse(text)
    N-->>A: {action: transfer, amount: 0.009}
    A->>S: verify(transaction)
    S->>S: Run 10 security checks
    S-->>A: ✅ Approved
    A->>C: checkAndExecute(to, amount)
    C->>B: broadcast transaction
    B-->>C: mined
    C-->>A: TX hash 0xabc...
    A-->>F: {success: true, tx: "0xabc..."}
    F-->>U: 🔊 Voice + Text response
```

---

## 4. Component Architecture

```mermaid
flowchart TB
    subgraph FE["Frontend Components"]
        FE1[Chat Widget]
        FE2[Voice Button]
        FE3[Balance Card]
        FE4[Notification Bar]
    end

    subgraph BE["Backend Components"]
        BE1[FastAPI Router]
        BE2[NLP Parser]
        BE3[LLM Agent]
        BE4[Conversation Engine]
    end

    subgraph FM["Feature Modules"]
        FM1[Accounting]
        FM2[Budget]
        FM3[Forecasting]
        FM4[Advice]
        FM5[Bill Payment]
        FM6[Swap]
        FM7[Portfolio]
    end

    subgraph SL["Security Modules"]
        SL1[Verifier]
        SL2[Simulation]
        SL3[Session Budget]
        SL4[Prompt Guard]
        SL5[Anomaly Detection]
    end

    subgraph BC["Blockchain"]
        BC1[AgentGuard.sol]
        BC2[Ganache / Sepolia]
    end

    FE1 --> BE1
    FE2 --> BE1
    FE3 --> BE1
    FE4 --> BE1
    BE1 --> BE2
    BE1 --> BE3
    BE1 --> BE4
    BE2 --> FM1
    BE2 --> FM2
    BE3 --> FM3
    BE4 --> FM4
    FM1 --> SL1
    FM2 --> SL2
    SL1 --> BC1
    BC1 --> BC2
```

---

## 5. Technology Stack

```mermaid
flowchart LR
    subgraph FE["Frontend"]
        FE1[Flutter 3.47]
        FE2[Dart]
        FE3[Material 3]
    end

    subgraph BE["Backend"]
        BE1[Python 3.11]
        BE2[FastAPI]
        BE3[Web3.py]
        BE4[solcx]
    end

    subgraph AI["AI / ML"]
        AI1[Ollama]
        AI2[llama3.2:3b]
        AI3[SpeechRecognition]
        AI4[gTTS]
    end

    subgraph BC["Blockchain"]
        BC1[Solidity 0.8.19]
        BC2[Ganache]
        BC3[Ethereum]
    end

    subgraph DO["DevOps"]
        DO1[Docker]
        DO2[Docker Compose]
        DO3[Nginx]
    end

    FE1 --> BE1
    BE1 --> AI1
    BE1 --> BC1
    BE1 --> DO1

    style FE fill:#8B5CF6,color:#fff
    style BE fill:#10B981,color:#fff
    style AI fill:#F59E0B,color:#fff
    style BC fill:#1F2937,color:#fff
    style DO fill:#6366F1,color:#fff
```

---

## 6. Layer Summary

| # | Layer | Technology | Purpose |
|---|-------|-----------|---------|
| 1 | **User** | Voice + Text | Input in 3 languages |
| 2 | **Frontend** | Flutter Web | Cross-platform UI |
| 3 | **API** | FastAPI + Nginx | REST + static |
| 4 | **AI** | Ollama + NLP | Language understanding |
| 5 | **Features** | Python | 30+ modules |
| 6 | **Security** | Python + Solidity | 10-layer protection |
| 7 | **Blockchain** | Ethereum | On-chain execution |
| 8 | **DevOps** | Docker | One-command deploy |

---

## 7. Deployment Architecture

```mermaid
flowchart TB
    subgraph LOCAL["💻 Developer Machine"]
        D1[docker-compose up]
    end

    subgraph DOCKER["🐳 Docker Compose"]
        DC1[ganache<br/>:7545]
        DC2[ollama<br/>:11434]
        DC3[app<br/>:8000 · :8080]
    end

    subgraph ACCESS["🌐 Access Points"]
        AC1[http://localhost:8080<br/>Flutter Web]
        AC2[http://localhost:8000<br/>REST API]
    end

    D1 --> DC1
    D1 --> DC2
    D1 --> DC3
    DC1 --> DC3
    DC2 --> DC3
    DC3 --> AC1
    DC3 --> AC2

    style LOCAL fill:#6366F1,color:#fff
    style DOCKER fill:#10B981,color:#fff
    style ACCESS fill:#F59E0B,color:#fff
```

---

**© 2026 Sentinel Wallet AI — FinTechathon Submission**
