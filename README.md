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


