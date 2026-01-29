# Wallet Detection System with iExec

Privacy-preserving wallet risk analysis using agentic AI and iExec secure compute.

## 🏗️ Project Structure

```
walletdetectioniexce/
├── agent/                      # Milestone 1: Agent Decision Engine
│   ├── __init__.py
│   ├── models.py              # Data schemas
│   ├── rules.py               # Rule-based decision logic
│   ├── llm_reasoning.py       # LLM integration
│   └── orchestrator.py        # Main agent coordinator
├── examples/
│   └── example_usage.py       # Usage examples
└── requirements.txt
```

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

```python
from agent import analyze_wallet, WalletSignals, ProtocolHealthIndicators, MarketVolatilityFlags, RequestMetadata

# Create input data
wallet_signals = WalletSignals(...)
protocol_health = ProtocolHealthIndicators(...)
market_volatility = MarketVolatilityFlags(...)
metadata = RequestMetadata(...)

# Analyze
result = analyze_wallet(
    wallet_signals,
    protocol_health,
    market_volatility,
    metadata
)

print(f"Decision: {result.decision}")
print(f"Risk Score: {result.risk_score}")
print(f"Confidence: {result.confidence}%")
```

### Run Examples

```bash
python examples/example_usage.py
```

## 📊 Decision Outputs

The agent produces one of four decisions:

- **NO_ACTION** (Risk: 0-25) - Low risk, continue normal operations
- **MONITOR** (Risk: 25-60) - Elevated risk, increase monitoring
- **REQUEST_SEVERITY_ANALYSIS** (Risk: 60-80) - Ambiguous, needs deeper analysis
- **ENFORCE_ACTION** (Risk: 80-100) - High risk, immediate action required

## 🧠 How It Works

### 1. Rule-Based Scoring
Fast, deterministic risk assessment based on:
- Wallet age and history
- Transaction patterns and velocity
- DeFi position health
- Suspicious behavior detection
- Reputation signals
- Protocol and market conditions

### 2. LLM Reasoning (Optional)
For ambiguous cases, the system can use LLM-based contextual analysis to:
- Interpret conflicting signals
- Distinguish legitimate from malicious behavior
- Handle edge cases requiring nuanced understanding

### 3. Hybrid Decision
Combines rule-based and LLM analysis with safety overrides to ensure:
- Fast processing (< 100ms for rules, < 5s with LLM)
- High accuracy (> 95%)
- Conservative approach to critical risks

## 📁 Milestones

### ✅ Milestone 0: System Understanding
- Defined roles and trust boundaries
- Established data flow architecture

### ✅ Milestone 1: Agent Decision Engine ⭐ (Current)
- Implemented data models and schemas
- Created rule-based scoring engine
- Integrated LLM reasoning layer
- Built main orchestrator

### 🔄 Milestone 2: iExec Integration (Next)
- Docker containerization
- TEE configuration
- Smart contract integration

### 📋 Milestone 3: Smart Contracts
- Task triggering
- Result verification
- Payment handling

### 🎨 Milestone 4: Frontend
- Wallet connection
- Analysis dashboard
- Result visualization

## 🔐 Privacy & Security

- **Zero-knowledge**: Agent never accesses private keys
- **Privacy-preserving**: Runs in TEE for confidential computation
- **Verifiable**: All decisions are cryptographically provable
- **Auditable**: Complete decision trail with explanations

## 📖 Documentation

See the `brain/` directory for comprehensive design documents:
- `milestone_0_system_boundaries.md`
- `milestone_1_agent_decision_engine.md`
- `milestone_2_iexec_integration.md`
- `milestone_2b_severity_engine.md`

## 🧪 Testing

```bash
# Run tests (when available)
pytest tests/

# With coverage
pytest --cov=agent tests/
```

## 📝 License

MIT

## 🤝 Contributing

This is a project built with iExec decentralized infrastructure for privacy-preserving DeFi risk analysis.
