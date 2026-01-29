"""
Example usage of the Agent Decision Engine

This demonstrates how to use the wallet risk analysis system.
"""

import sys
import os
import time

# Add parent directory to path so agent module can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import (
    analyze_wallet,
    WalletSignals,
    ProtocolHealthIndicators,
    MarketVolatilityFlags,
    RequestMetadata,
    CurrentBalance,
    PortfolioValue,
    TransactionVelocity,
    SuspiciousPatterns,
    LendingBorrowing,
    LiquidityDepth,
    GasPrice,
)


def example_low_risk_wallet():
    """Example: Established wallet with low risk"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Low Risk Wallet")
    print("="*60)
    
    wallet_signals = WalletSignals(
        wallet_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
        first_seen_timestamp=int(time.time()) - (500 * 86400),  # 500 days ago
        age_in_days=500,
        total_transactions=1250,
        average_transactions_per_day=2.5,
        last_activity_timestamp=int(time.time()) - 3600,  # 1 hour ago
        days_since_last_activity=0,
        current_balance=CurrentBalance(
            native=2.5,
            stablecoins=5000,
            total_usd=12500
        ),
        portfolio_value=PortfolioValue(
            tokens=12500,
            nfts=0,
            defi=8000,
            total_usd=20500
        ),
        transaction_velocity=TransactionVelocity(
            last_24h=3,
            last_7d=18,
            last_30d=75
        ),
        unique_contracts_interacted=25,
        unique_addresses_interacted=150,
        suspicious_patterns=SuspiciousPatterns(),  # No suspicious patterns
        defi_protocols=[],
        lending_borrowing=LendingBorrowing(
            total_borrowed=5000,
            total_collateral=8000,
            health_factor=2.8
        ),
        ens_name="alice.eth",
        has_gitcoin_passport=True,
        has_poap=True,
        on_chain_reputation=85.0
    )
    
    protocol_health = ProtocolHealthIndicators(
        total_value_locked=500_000_000,
        total_active_users=50000,
        system_utilization_rate=65.0,
        liquidity_depth=LiquidityDepth(
            tier1=50_000_000,
            tier2=100_000_000,
            tier3=150_000_000
        ),
        default_rate=1.2,
        average_health_factor=2.5,
        liquidation_events_24h=3
    )
    
    market_volatility = MarketVolatilityFlags(
        volatility_index=35.0,
        market_sentiment='NEUTRAL',
        gas_price=GasPrice(
            current=25.0,
            average_7d=30.0,
            percentile=40.0
        ),
        network_congestion='MEDIUM'
    )
    
    metadata = RequestMetadata(
        request_id="req_001",
        timestamp=int(time.time()),
        request_type='POSITION_REVIEW',
        requested_by="0xProtocol",
        urgency='LOW'
    )
    
    # Analyze
    result = analyze_wallet(
        wallet_signals,
        protocol_health,
        market_volatility,
        metadata
    )
    
    print_result(result)


def example_high_risk_wallet():
    """Example: New wallet with high risk patterns"""
    print("\n" + "="*60)
    print("EXAMPLE 2: High Risk Wallet")
    print("="*60)
    
    wallet_signals = WalletSignals(
        wallet_address="0xSuspicious123456789abcdef",
        first_seen_timestamp=int(time.time()) - (5 * 86400),  # 5 days ago
        age_in_days=5,
        total_transactions=450,  # High velocity for new wallet
        average_transactions_per_day=90,
        last_activity_timestamp=int(time.time()) - 300,
        days_since_last_activity=0,
        current_balance=CurrentBalance(
            native=0.1,
            stablecoins=100,
            total_usd=500
        ),
        portfolio_value=PortfolioValue(
            tokens=500,
            nfts=0,
            defi=0,
            total_usd=500
        ),
        transaction_velocity=TransactionVelocity(
            last_24h=150,  # Extreme spike
            last_7d=450,
            last_30d=450
        ),
        unique_contracts_interacted=5,
        unique_addresses_interacted=200,
        suspicious_patterns=SuspiciousPatterns(
            rapid_draining=True,
            unusual_activity=True,
            new_wallet_high_value=False,
            mixer_interaction=False
        ),
        defi_protocols=[],
        lending_borrowing=None
    )
    
    protocol_health = ProtocolHealthIndicators(
        total_value_locked=500_000_000,
        total_active_users=50000,
        system_utilization_rate=65.0,
        liquidity_depth=LiquidityDepth(
            tier1=50_000_000,
            tier2=100_000_000,
            tier3=150_000_000
        ),
        default_rate=1.2,
        average_health_factor=2.5,
        liquidation_events_24h=3
    )
    
    market_volatility = MarketVolatilityFlags(
        volatility_index=45.0,
        market_sentiment='NEUTRAL',
        gas_price=GasPrice(current=30.0, average_7d=30.0, percentile=50.0),
        network_congestion='MEDIUM'
    )
    
    metadata = RequestMetadata(
        request_id="req_002",
        timestamp=int(time.time()),
        request_type='NEW_LOAN',
        requested_by="0xProtocol",
        urgency='HIGH'
    )
    
    result = analyze_wallet(
        wallet_signals,
        protocol_health,
        market_volatility,
        metadata
    )
    
    print_result(result)


def example_critical_liquidation_risk():
    """Example: Critical liquidation risk during market crash"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Critical Liquidation Risk")
    print("="*60)
    
    wallet_signals = WalletSignals(
        wallet_address="0xAtRisk987654321",
        first_seen_timestamp=int(time.time()) - (120 * 86400),
        age_in_days=120,
        total_transactions=500,
        average_transactions_per_day=4.2,
        last_activity_timestamp=int(time.time()) - 86400,
        days_since_last_activity=1,
        current_balance=CurrentBalance(
            native=1.0,
            stablecoins=500,
            total_usd=2500
        ),
        portfolio_value=PortfolioValue(
            tokens=2500,
            nfts=0,
            defi=200000,
            total_usd=202500
        ),
        transaction_velocity=TransactionVelocity(
            last_24h=2,
            last_7d=15,
            last_30d=125
        ),
        unique_contracts_interacted=15,
        unique_addresses_interacted=80,
        suspicious_patterns=SuspiciousPatterns(),
        defi_protocols=[],
        lending_borrowing=LendingBorrowing(
            total_borrowed=150000,
            total_collateral=200000,
            health_factor=1.08  # CRITICAL!
        )
    )
    
    protocol_health = ProtocolHealthIndicators(
        total_value_locked=500_000_000,
        total_active_users=50000,
        system_utilization_rate=85.0,  # High utilization
        liquidity_depth=LiquidityDepth(
            tier1=20_000_000,  # Lower liquidity
            tier2=40_000_000,
            tier3=60_000_000
        ),
        default_rate=3.5,
        average_health_factor=1.8,
        liquidation_events_24h=25  # Many liquidations
    )
    
    market_volatility = MarketVolatilityFlags(
        volatility_index=85.0,  # HIGH VOLATILITY
        market_sentiment='EXTREME_FEAR',
        flash_crash_detected=True,
        large_liquidations_in_progress=True,
        estimated_liquidation_cascade=50_000_000,
        gas_price=GasPrice(current=150.0, average_7d=30.0, percentile=95.0),
        network_congestion='EXTREME'
    )
    
    metadata = RequestMetadata(
        request_id="req_003",
        timestamp=int(time.time()),
        request_type='SCHEDULED_CHECK',
        requested_by="0xProtocol",
        urgency='HIGH'
    )
    
    result = analyze_wallet(
        wallet_signals,
        protocol_health,
        market_volatility,
        metadata
    )
    
    print_result(result)


def print_result(result):
    """Pretty print the analysis result"""
    print(f"\n🔍 DECISION: {result.decision}")
    print(f"📊 Risk Score: {result.risk_score:.1f}/100")
    print(f"💯 Confidence: {result.confidence:.1f}%")
    print(f"\n📝 Reasoning:")
    print(f"   {result.reasoning}")
    
    if result.flags:
        print(f"\n🚩 Flags: {', '.join(result.flags)}")
    
    if result.recommendations:
        print(f"\n💡 Recommendations:")
        for i, rec in enumerate(result.recommendations, 1):
            print(f"   {i}. {rec}")
    
    print(f"\n⚙️  Processing: {result.metadata.processing_time_ms:.2f}ms")
    print(f"🤖 LLM Used: {result.metadata.llm_used}")
    
    # JSON output
    print(f"\n📄 JSON Output:")
    import json
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    print("🤖 Agent Decision Engine - Example Usage")
    print("="*60)
    
    # Run examples
    example_low_risk_wallet()
    example_high_risk_wallet()
    example_critical_liquidation_risk()
    
    print("\n" + "="*60)
    print("✅ All examples completed!")
    print("="*60)
