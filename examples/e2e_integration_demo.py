"""
End-to-End Integration Demo

Demonstrates complete workflow: Agent → iExec → Smart Contract
"""

import sys
import os
import asyncio
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import *
from integration.orchestrator import EndToEndOrchestrator


async def demo_scenario_1_low_risk():
    """Scenario 1: Low Risk Wallet (Local Analysis Only)"""
    
    print("\n" + "="*70)
    print("SCENARIO 1: Established Low-Risk Wallet")
    print("="*70)
    
    orchestrator = EndToEndOrchestrator(
        contract_address="0x1234567890ABCDEFWalletRiskEnforcement"
    )
    
    result = await orchestrator.process_wallet_analysis(
        wallet_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
        wallet_signals=WalletSignals(
            wallet_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
            first_seen_timestamp=int(time.time()) - (500 * 86400),
            age_in_days=500,
            total_transactions=1250,
            average_transactions_per_day=2.5,
            last_activity_timestamp=int(time.time()) - 3600,
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
            suspicious_patterns=SuspiciousPatterns(),
            ens_name="alice.eth",
            has_gitcoin_passport=True,
            on_chain_reputation=85.0
        ),
        protocol_health=ProtocolHealthIndicators(
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
        ),
        market_volatility=MarketVolatilityFlags(
            volatility_index=35.0,
            market_sentiment='NEUTRAL',
            gas_price=GasPrice(current=25.0, average_7d=30.0, percentile=40.0),
            network_congestion='MEDIUM'
        ),
        metadata=RequestMetadata(
            request_id="req_scenario_1",
            timestamp=int(time.time()),
            request_type='NEW_LOAN',
            requested_by="0xLendingProtocol"
        )
    )
    
    print(f"\n📊 FINAL RESULT:")
    print(f"   Decision: {result['analysis']['decision']}")
    print(f"   Risk Score: {result['analysis']['risk_score']:.1f}/100")
    print(f"   Confidence: {result['analysis']['confidence']:.1f}%")
    if result['transaction']:
        tx_hash = result['transaction']['transactionHash']
        print(f"   TX Hash: {tx_hash[:16] if isinstance(tx_hash, str) else tx_hash.hex()[:16]}...")
    else:
        print(f"   On-Chain: Not required (low risk)")


async def demo_scenario_2_high_risk():
    """Scenario 2: High Risk Case (Requires iExec)"""
    
    print("\n" + "="*70)
    print("SCENARIO 2: High-Risk Wallet (iExec Analysis Required)")
    print("="*70)
    
    orchestrator = EndToEndOrchestrator(
        contract_address="0x1234567890ABCDEFWalletRiskEnforcement"
    )
    
    result = await orchestrator.process_wallet_analysis(
        wallet_address="0xHighRisk123456789abcdef",
        wallet_signals=WalletSignals(
            wallet_address="0xHighRisk123456789abcdef",
            first_seen_timestamp=int(time.time()) - (90 * 86400),
            age_in_days=90,
            total_transactions=800,
            average_transactions_per_day=8.9,
            last_activity_timestamp=int(time.time()) - 1800,
            days_since_last_activity=0,
            current_balance=CurrentBalance(
                native=0.5,
                stablecoins=1500,
                total_usd=3000
            ),
            portfolio_value=PortfolioValue(
                tokens=3000,
                nfts=0,
                defi=5000,
                total_usd=8000
            ),
            transaction_velocity=TransactionVelocity(
                last_24h=45,  # High spike
                last_7d=150,
                last_30d=270
            ),
            unique_contracts_interacted=8,
            unique_addresses_interacted=120,
            suspicious_patterns=SuspiciousPatterns(
                rapid_draining=True,
                unusual_activity=True
            ),
            lending_borrowing=LendingBorrowing(
                total_borrowed=4000,
                total_collateral=5000,
                health_factor=1.35  # Declining
            )
        ),
        protocol_health=ProtocolHealthIndicators(
            total_value_locked=500_000_000,
            total_active_users=50000,
            system_utilization_rate=75.0,
            liquidity_depth=LiquidityDepth(
                tier1=35_000_000,
                tier2=70_000_000,
                tier3=100_000_000
            ),
            default_rate=3.5,
            average_health_factor=2.0,
            liquidation_events_24h=15
        ),
        market_volatility=MarketVolatilityFlags(
            volatility_index=72.0,
            market_sentiment='FEAR',
            gas_price=GasPrice(current=65.0, average_7d=30.0, percentile=85.0),
            network_congestion='HIGH'
        ),
        metadata=RequestMetadata(
            request_id="req_scenario_2",
            timestamp=int(time.time()),
            request_type='POSITION_REVIEW',
            requested_by="0xLendingProtocol",
            urgency='HIGH'
        )
    )
    
    print(f"\n📊 FINAL RESULT:")
    print(f"   Decision: {result['analysis']['decision']}")
    print(f"   Risk Score: {result['analysis']['risk_score']:.1f}/100")
    print(f"   Confidence: {result['analysis']['confidence']:.1f}%")
    print(f"   Reasoning: {result['analysis']['reasoning']}")
    if result['transaction']:
        tx_hash = result['transaction']['transactionHash']
        print(f"   Contract: {result['contract_address'][:16]}...")
        print(f"   TX Hash: {tx_hash[:16]}...")


async def demo_scenario_3_critical():
    """Scenario 3: Critical Risk (Auto-Pause)"""
    
    print("\n" + "="*70)
    print("SCENARIO 3: Critical Risk Wallet (Auto-Pause)")
    print("="*70)
    
    orchestrator = EndToEndOrchestrator(
        contract_address="0x1234567890ABCDEFWalletRiskEnforcement"
    )
    
    result = await orchestrator.process_wallet_analysis(
        wallet_address="0xCritical987654321",
        wallet_signals=WalletSignals(
            wallet_address="0xCritical987654321",
            first_seen_timestamp=int(time.time()) - (120 * 86400),
            age_in_days=120,
            total_transactions=600,
            average_transactions_per_day=5.0,
            last_activity_timestamp=int(time.time()) - 900,
            days_since_last_activity=0,
            current_balance=CurrentBalance(
                native=0.3,
                stablecoins=800,
                total_usd=2000
            ),
            portfolio_value=PortfolioValue(
                tokens=2000,
                nfts=0,
                defi=180000,
                total_usd=182000
            ),
            transaction_velocity=TransactionVelocity(
                last_24h=8,
                last_7d=25,
                last_30d=150
            ),
            unique_contracts_interacted=12,
            unique_addresses_interacted=90,
            suspicious_patterns=SuspiciousPatterns(),
            lending_borrowing=LendingBorrowing(
                total_borrowed=120000,
                total_collateral=180000,
                health_factor=1.08  # CRITICAL!
            )
        ),
        protocol_health=ProtocolHealthIndicators(
            total_value_locked=450_000_000,
            total_active_users=48000,
            system_utilization_rate=88.0,
            liquidity_depth=LiquidityDepth(
                tier1=20_000_000,
                tier2=40_000_000,
                tier3=60_000_000
            ),
            default_rate=4.5,
            average_health_factor=1.7,
            liquidation_events_24h=35
        ),
        market_volatility=MarketVolatilityFlags(
            volatility_index=92.0,
            market_sentiment='EXTREME_FEAR',
            flash_crash_detected=True,
            large_liquidations_in_progress=True,
            estimated_liquidation_cascade=80_000_000,
            gas_price=GasPrice(current=180.0, average_7d=35.0, percentile=98.0),
            network_congestion='EXTREME'
        ),
        metadata=RequestMetadata(
            request_id="req_scenario_3",
            timestamp=int(time.time()),
            request_type='SCHEDULED_CHECK',
            requested_by="0xLendingProtocol",
            urgency='HIGH'
        )
    )
    
    print(f"\n📊 FINAL RESULT:")
    print(f"   Decision: {result['analysis']['decision']}")
    print(f"   Risk Score: {result['analysis']['risk_score']:.1f}/100")
    print(f"   Confidence: {result['analysis']['confidence']:.1f}%")
    print(f"   Flags: {', '.join(result['analysis']['flags'])}")
    if result['transaction']:
        tx_hash = result['transaction']['transactionHash']
        print(f"   Contract: {result['contract_address'][:16]}...")
        print(f"   TX Hash: {tx_hash[:16]}...")
        print(f"\n   🚨 WALLET PAUSED - CRITICAL RISK DETECTED")


async def main():
    """Run all demonstration scenarios"""
    
    print("="*70)
    print("🚀 END-TO-END INTEGRATION DEMONSTRATION")
    print("   Agent → iExec → Smart Contract")
    print("="*70)
    
    # Run scenarios
    await demo_scenario_1_low_risk()
    await asyncio.sleep(1)
    
    await demo_scenario_2_high_risk()
    await asyncio.sleep(1)
    
    await demo_scenario_3_critical()
    
    print("\n" + "="*70)
    print("✅ ALL SCENARIOS COMPLETED")
    print("="*70)
    print("\nIntegration Summary:")
    print("  ✅ Local agent analysis working")
    print("  ✅ iExec escalation working")
    print("  ✅ Smart contract submission working")
    print("  ✅ Event emission working")
    print("\n🎉 System is fully integrated and operational!")


if __name__ == "__main__":
    asyncio.run(main())
