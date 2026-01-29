"""
Data models for the Agent Decision Engine

This module defines all input and output schemas for the wallet analysis system.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal
from datetime import datetime


# ============================================================================
# INPUT SCHEMAS
# ============================================================================

@dataclass
class TransactionVelocity:
    """Transaction activity over different time windows"""
    last_24h: int
    last_7d: int
    last_30d: int


@dataclass
class CurrentBalance:
    """Current wallet balances"""
    native: float  # ETH, MATIC, etc.
    stablecoins: float  # USDC, USDT, DAI
    total_usd: float


@dataclass
class PortfolioValue:
    """Total portfolio breakdown"""
    tokens: float
    nfts: float
    defi: float
    total_usd: float


@dataclass
class SuspiciousPatterns:
    """Detected suspicious behavior flags"""
    rapid_draining: bool = False
    unusual_activity: bool = False
    new_wallet_high_value: bool = False
    mixer_interaction: bool = False
    sanctioned_address_interaction: bool = False


@dataclass
class DeFiProtocol:
    """DeFi protocol interaction data"""
    protocol_name: str
    interaction_count: int
    total_value_locked: float
    last_interaction: int


@dataclass
class LendingBorrowing:
    """Lending/borrowing position data"""
    total_borrowed: float
    total_collateral: float
    health_factor: float  # <1.0 = liquidation risk


@dataclass
class WalletSignals:
    """Comprehensive wallet behavior signals"""
    # Identity & Age
    wallet_address: str
    first_seen_timestamp: int
    age_in_days: int
    
    # Transaction Patterns
    total_transactions: int
    average_transactions_per_day: float
    last_activity_timestamp: int
    days_since_last_activity: int
    
    # Financial Metrics
    current_balance: CurrentBalance
    portfolio_value: PortfolioValue
    
    # Behavior Indicators
    transaction_velocity: TransactionVelocity
    unique_contracts_interacted: int
    unique_addresses_interacted: int
    
    # Risk Signals
    suspicious_patterns: SuspiciousPatterns
    
    # DeFi Activity
    defi_protocols: List[DeFiProtocol] = field(default_factory=list)
    lending_borrowing: Optional[LendingBorrowing] = None
    
    # Reputation Scores
    credit_score: Optional[float] = None  # 0-1000
    on_chain_reputation: Optional[float] = None  # 0-100
    ens_name: Optional[str] = None
    has_poap: bool = False
    has_gitcoin_passport: bool = False


@dataclass
class LiquidityDepth:
    """Protocol liquidity tiers"""
    tier1: float  # Immediate liquidity
    tier2: float  # 1-hour liquidity
    tier3: float  # 24-hour liquidity


@dataclass
class PegStability:
    """Stablecoin peg stability"""
    asset: str
    target_price: float
    current_price: float
    deviation: float  # %


@dataclass
class RecentUpgrade:
    """Smart contract upgrade info"""
    contract: str
    timestamp: int
    audited: bool


@dataclass
class ProtocolHealthIndicators:
    """System-wide protocol health metrics"""
    # System-wide Metrics
    total_value_locked: float
    total_active_users: int
    system_utilization_rate: float  # 0-100%
    
    # Liquidity Health
    liquidity_depth: LiquidityDepth
    
    # Risk Metrics
    default_rate: float  # % of loans in default
    average_health_factor: float
    liquidation_events_24h: int
    
    # Stability Indicators
    pegs_stability: List[PegStability] = field(default_factory=list)
    
    # Oracle Health
    oracle_freshness: bool = True
    oracle_deviation: float = 0.0
    
    # Smart Contract Status
    paused_contracts: List[str] = field(default_factory=list)
    recent_upgrades: List[RecentUpgrade] = field(default_factory=list)


@dataclass
class AssetVolatility:
    """Asset-specific volatility metrics"""
    asset: str
    price_24h_change: float  # %
    price_7d_change: float  # %
    volatility_30d: float  # Standard deviation
    volume_24h: float
    volume_change: float  # % vs avg


@dataclass
class GasPrice:
    """Network gas price metrics"""
    current: float
    average_7d: float
    percentile: float  # 0-100


MarketSentiment = Literal['EXTREME_FEAR', 'FEAR', 'NEUTRAL', 'GREED', 'EXTREME_GREED']
NetworkCongestion = Literal['LOW', 'MEDIUM', 'HIGH', 'EXTREME']


@dataclass
class MarketVolatilityFlags:
    """Market conditions and volatility indicators"""
    # Global Market Conditions
    volatility_index: float  # 0-100
    market_sentiment: MarketSentiment
    
    # Asset-Specific Volatility
    asset_volatility: List[AssetVolatility] = field(default_factory=list)
    
    # Event Flags
    flash_crash_detected: bool = False
    black_swan_event: bool = False
    regulatory_news: bool = False
    
    # On-chain Activity
    gas_price: GasPrice = None
    network_congestion: NetworkCongestion = 'MEDIUM'
    
    # Liquidation Risk
    large_liquidations_in_progress: bool = False
    estimated_liquidation_cascade: float = 0.0  # USD value


RequestType = Literal['NEW_LOAN', 'POSITION_REVIEW', 'SCHEDULED_CHECK', 'MANUAL_REVIEW']
Urgency = Literal['LOW', 'MEDIUM', 'HIGH']


@dataclass
class RequestMetadata:
    """Request context metadata"""
    request_id: str
    timestamp: int
    request_type: RequestType
    requested_by: str
    urgency: Urgency = 'MEDIUM'


@dataclass
class AgentInput:
    """Complete input to the agent decision engine"""
    wallet_signals: WalletSignals
    protocol_health: ProtocolHealthIndicators
    market_volatility: MarketVolatilityFlags
    metadata: RequestMetadata


# ============================================================================
# OUTPUT SCHEMAS
# ============================================================================

DecisionType = Literal['NO_ACTION', 'MONITOR', 'REQUEST_SEVERITY_ANALYSIS', 'ENFORCE_ACTION']


@dataclass
class OutputMetadata:
    """Metadata about the decision process"""
    processing_time_ms: float
    llm_used: bool
    rule_based_score: float
    llm_score: Optional[float] = None


@dataclass
class AgentOutput:
    """Output from the agent decision engine"""
    decision: DecisionType
    confidence: float  # 0-100
    reasoning: str
    risk_score: float  # 0-100
    recommendations: List[str]
    flags: List[str]
    timestamp: int
    metadata: OutputMetadata
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'decision': self.decision,
            'confidence': round(self.confidence, 2),
            'reasoning': self.reasoning,
            'risk_score': round(self.risk_score, 2),
            'recommendations': self.recommendations,
            'flags': self.flags,
            'timestamp': self.timestamp,
            'metadata': {
                'processing_time_ms': round(self.metadata.processing_time_ms, 2),
                'llm_used': self.metadata.llm_used,
                'rule_based_score': round(self.metadata.rule_based_score, 2),
                'llm_score': round(self.metadata.llm_score, 2) if self.metadata.llm_score else None
            }
        }
