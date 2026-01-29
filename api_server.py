import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os
import time
from dotenv import load_dotenv

from agent.orchestrator import AgentOrchestrator
from agent.models import (
    AgentInput, WalletSignals, ProtocolHealthIndicators, MarketVolatilityFlags,
    RequestMetadata, CurrentBalance, PortfolioValue, TransactionVelocity,
    SuspiciousPatterns, LendingBorrowing, LiquidityDepth, GasPrice
)

# Load environment variables
load_dotenv()

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for dev, restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Orchestrator
api_key = os.getenv("OPENAI_API_KEY")
orchestrator = AgentOrchestrator(llm_api_key=api_key)

class AnalyzeRequest(BaseModel):
    walletAddress: str
    portfolio: Dict[str, Any]

@app.get("/")
def read_root():
    return {"status": "active", "service": "Wallet Risk Analysis AI"}

@app.post("/analyze")
async def analyze_wallet(request: AnalyzeRequest):
    try:
        # Construct WalletSignals from simplified frontend data
        # We use defaults for missing rich data since frontend only has basic Etherscan data
        
        wallet_signals = WalletSignals(
            wallet_address=request.walletAddress,
            first_seen_timestamp=int(time.time()) - (request.portfolio.get('walletAge', 0) * 86400),
            age_in_days=request.portfolio.get('walletAge', 0),
            total_transactions=request.portfolio.get('transactions', 0),
            average_transactions_per_day=0.5, # Placeholder
            last_activity_timestamp=int(time.time()), # Placeholder
            days_since_last_activity=0,
            current_balance=CurrentBalance(
                native=0.0, 
                stablecoins=0.0, 
                total_usd=request.portfolio.get('totalValue', 0)
            ),
            portfolio_value=PortfolioValue(
                tokens=0,
                nfts=0,
                defi=0,
                total_usd=request.portfolio.get('totalValue', 0)
            ),
            transaction_velocity=TransactionVelocity(last_24h=0, last_7d=0, last_30d=0), # Placeholder
            unique_contracts_interacted=0,
            unique_addresses_interacted=0,
            suspicious_patterns=SuspiciousPatterns(),
            ens_name=None,
            has_gitcoin_passport=False,
            on_chain_reputation=50.0
        )

        # Use intelligent defaults for Context (Simulation of Market Data)
        protocol_health = ProtocolHealthIndicators(
            total_value_locked=1_000_000_000,
            total_active_users=10000,
            system_utilization_rate=50.0,
            liquidity_depth=LiquidityDepth(tier1=1e6, tier2=1e7, tier3=1e8),
            default_rate=2.0,
            average_health_factor=2.0,
            liquidation_events_24h=0
        )

        market_volatility = MarketVolatilityFlags(
            volatility_index=30.0,
            market_sentiment='NEUTRAL',
            gas_price=GasPrice(current=20.0, average_7d=20.0, percentile=50.0),
            network_congestion='MEDIUM'
        )

        metadata = RequestMetadata(
            request_id=f"req_{int(time.time())}",
            timestamp=int(time.time()),
            request_type='MANUAL_REVIEW',
            requested_by="Frontend_User"
        )

        # Assemble Input
        agent_input = AgentInput(
            wallet_signals=wallet_signals,
            protocol_health=protocol_health,
            market_volatility=market_volatility,
            metadata=metadata
        )

        # Run Agent Analysis
        print(f"Analyzing wallet: {request.walletAddress}")
        result = orchestrator.analyze(agent_input)
        
        return result.to_dict()

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Render sets PORT dynamically
    print(f"Starting AI Agent API Server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
