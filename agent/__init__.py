"""
Agent Decision Engine Package

Privacy-preserving wallet risk analysis with hybrid rule-based and LLM reasoning.
"""

from .models import (
    AgentInput,
    AgentOutput,
    WalletSignals,
    ProtocolHealthIndicators,
    MarketVolatilityFlags,
    RequestMetadata,
    DecisionType,
    # Nested models
    CurrentBalance,
    PortfolioValue,
    TransactionVelocity,
    SuspiciousPatterns,
    DeFiProtocol,
    LendingBorrowing,
    LiquidityDepth,
    PegStability,
    AssetVolatility,
    GasPrice,
)

from .orchestrator import AgentOrchestrator, analyze_wallet
from .rules import RuleBasedEngine
from .llm_reasoning import LLMReasoning

__version__ = "0.1.0"

__all__ = [
    # Main components
    "AgentOrchestrator",
    "analyze_wallet",
    "RuleBasedEngine",
    "LLMReasoning",
    
    # Input/Output models
    "AgentInput",
    "AgentOutput",
    "WalletSignals",
    "ProtocolHealthIndicators",
    "MarketVolatilityFlags",
    "RequestMetadata",
    
    # Nested models
    "CurrentBalance",
    "PortfolioValue",
    "TransactionVelocity",
    "SuspiciousPatterns",
    "DeFiProtocol",
    "LendingBorrowing",
    "LiquidityDepth",
    "PegStability",
    "AssetVolatility",
    "GasPrice",
    
    # Types
    "DecisionType",
]
