"""
Rule-based decision engine

Implements fast, deterministic risk scoring and decision logic.
"""

from typing import Tuple
from .models import (
    AgentInput, WalletSignals, ProtocolHealthIndicators, 
    MarketVolatilityFlags, DecisionType, TransactionVelocity
)


class RuleBasedEngine:
    """
    Fast rule-based risk assessment engine
    
    Provides deterministic decisions based on predefined rules and thresholds.
    """
    
    def calculate_risk_score(self, agent_input: AgentInput) -> float:
        """
        Calculate comprehensive risk score (0-100)
        
        Args:
            agent_input: Complete agent input data
            
        Returns:
            Risk score from 0 (low risk) to 100 (high risk)
        """
        score = 0.0
        
        # Wallet Age & History (up to +/-20 points)
        score += self._score_wallet_age(agent_input.wallet_signals)
        
        # Balance & Portfolio (up to +15 points)
        score += self._score_balance(agent_input.wallet_signals)
        
        # Transaction Patterns (up to +25 points)
        score += self._score_transaction_patterns(agent_input.wallet_signals)
        
        # Suspicious Patterns (up to +60 points)
        score += self._score_suspicious_patterns(agent_input.wallet_signals)
        
        # Reputation (up to -40 points - reduces risk)
        score += self._score_reputation(agent_input.wallet_signals)
        
        # DeFi Health (up to +50 points)
        score += self._score_defi_health(agent_input.wallet_signals)
        
        # Protocol Health (up to +35 points)
        score += self._score_protocol_health(agent_input.protocol_health)
        
        # Market Volatility (up to +55 points)
        score += self._score_market_volatility(agent_input.market_volatility)
        
        # Clamp to 0-100
        return max(0.0, min(100.0, score))
    
    def _score_wallet_age(self, signals: WalletSignals) -> float:
        """Score based on wallet age"""
        age = signals.age_in_days
        
        if age < 7:
            return 20.0  # Very new - high risk
        elif age < 30:
            return 10.0  # New
        elif age < 90:
            return 5.0   # Moderately new
        elif age > 365:
            return -10.0  # Mature - low risk
        else:
            return 0.0
    
    def _score_balance(self, signals: WalletSignals) -> float:
        """Score based on balance and portfolio value"""
        score = 0.0
        total_balance = signals.current_balance.total_usd
        
        # Very low balance is risky
        if total_balance < 100:
            score += 15.0
        elif total_balance < 1000:
            score += 5.0
        
        # New wallet with high value is suspicious
        if signals.age_in_days < 30 and total_balance > 50000:
            score += 10.0
        
        # Established wallet with high value is good
        if signals.age_in_days > 365 and signals.portfolio_value.total_usd > 100000:
            score -= 5.0
        
        return score
    
    def _score_transaction_patterns(self, signals: WalletSignals) -> float:
        """Score based on transaction patterns"""
        score = 0.0
        velocity = signals.transaction_velocity
        
        # Calculate velocity ratio (recent vs average)
        velocity_ratio = self._calculate_velocity_ratio(velocity, signals.age_in_days)
        
        # Abnormal velocity spike
        if velocity_ratio > 5.0:
            score += 25.0
        elif velocity_ratio > 3.0:
            score += 15.0
        elif velocity_ratio > 2.0:
            score += 10.0
        
        # Very low activity is also suspicious for active protocols
        if signals.days_since_last_activity > 90:
            score += 10.0
        
        return score
    
    def _score_suspicious_patterns(self, signals: WalletSignals) -> float:
        """Score based on detected suspicious patterns"""
        score = 0.0
        patterns = signals.suspicious_patterns
        
        if patterns.rapid_draining:
            score += 30.0
        
        if patterns.mixer_interaction:
            score += 25.0
        
        if patterns.new_wallet_high_value:
            score += 20.0
        
        if patterns.unusual_activity:
            score += 15.0
        
        if patterns.sanctioned_address_interaction:
            score += 50.0  # Critical red flag
        
        return score
    
    def _score_reputation(self, signals: WalletSignals) -> float:
        """Score based on reputation signals (negative values = lower risk)"""
        score = 0.0
        
        # Positive reputation signals reduce risk
        if signals.ens_name:
            score -= 10.0
        
        if signals.has_gitcoin_passport:
            score -= 15.0
        
        if signals.has_poap:
            score -= 5.0
        
        if signals.on_chain_reputation and signals.on_chain_reputation > 70:
            score -= 10.0
        
        if signals.credit_score and signals.credit_score > 700:
            score -= 15.0
        
        return score
    
    def _score_defi_health(self, signals: WalletSignals) -> float:
        """Score based on DeFi position health"""
        if not signals.lending_borrowing:
            return 0.0
        
        score = 0.0
        health_factor = signals.lending_borrowing.health_factor
        
        # Critical liquidation risk
        if health_factor < 1.05:
            score += 50.0
        elif health_factor < 1.1:
            score += 40.0
        elif health_factor < 1.2:
            score += 30.0
        elif health_factor < 1.5:
            score += 20.0
        elif health_factor < 2.0:
            score += 10.0
        
        return score
    
    def _score_protocol_health(self, protocol: ProtocolHealthIndicators) -> float:
        """Score based on overall protocol health"""
        score = 0.0
        
        # High default rate
        if protocol.default_rate > 10.0:
            score += 25.0
        elif protocol.default_rate > 5.0:
            score += 15.0
        
        # Many recent liquidations
        if protocol.liquidation_events_24h > 20:
            score += 20.0
        elif protocol.liquidation_events_24h > 10:
            score += 10.0
        
        # Paused contracts (emergency)
        if protocol.paused_contracts:
            score += 30.0
        
        # Oracle issues
        if not protocol.oracle_freshness:
            score += 25.0
        
        if protocol.oracle_deviation > 5.0:
            score += 15.0
        
        return score
    
    def _score_market_volatility(self, market: MarketVolatilityFlags) -> float:
        """Score based on market conditions"""
        score = 0.0
        
        # High volatility
        if market.volatility_index > 80:
            score += 30.0
        elif market.volatility_index > 70:
            score += 25.0
        elif market.volatility_index > 50:
            score += 15.0
        
        # Market events
        if market.flash_crash_detected:
            score += 30.0
        
        if market.black_swan_event:
            score += 40.0
        
        # Liquidation cascade risk
        if market.large_liquidations_in_progress:
            score += 20.0
        
        # Extreme network congestion
        if market.network_congestion == 'EXTREME':
            score += 10.0
        
        return score
    
    def _calculate_velocity_ratio(self, velocity: TransactionVelocity, age_days: int) -> float:
        """Calculate recent transaction velocity vs normal rate"""
        if age_days == 0 or velocity.last_30d == 0:
            return 1.0
        
        # Average daily transactions over 30 days
        avg_daily = velocity.last_30d / 30.0
        
        if avg_daily == 0:
            return 1.0
        
        # Recent 24h activity compared to average
        recent_rate = velocity.last_24h
        ratio = recent_rate / avg_daily
        
        return ratio
    
    def map_score_to_decision(
        self,
        risk_score: float,
        signals: WalletSignals,
        protocol: ProtocolHealthIndicators,
        market: MarketVolatilityFlags
    ) -> Tuple[DecisionType, bool]:
        """
        Map risk score to decision type
        
        Args:
            risk_score: Calculated risk score
            signals: Wallet signals
            protocol: Protocol health
            market: Market conditions
            
        Returns:
            Tuple of (decision_type, needs_llm_analysis)
        """
        # Critical blockers - immediate action
        if self._check_critical_blockers(signals, protocol, market):
            return ('ENFORCE_ACTION', False)
        
        # Very high risk
        if risk_score >= 80:
            return ('ENFORCE_ACTION', False)
        
        # High risk with ambiguity
        if risk_score >= 60:
            # Check for conflicting signals
            has_positive = self._has_positive_signals(signals)
            has_negative = self._has_negative_signals(signals)
            
            if has_positive and has_negative:
                # Ambiguous - needs LLM analysis
                return ('REQUEST_SEVERITY_ANALYSIS', True)
            else:
                # Clear high risk
                return ('ENFORCE_ACTION', False)
        
        # Medium risk
        if risk_score >= 30:
            return ('MONITOR', False)
        
        # Low risk
        return ('NO_ACTION', False)
    
    def _check_critical_blockers(
        self,
        signals: WalletSignals,
        protocol: ProtocolHealthIndicators,
        market: MarketVolatilityFlags
    ) -> bool:
        """Check for critical conditions requiring immediate action"""
        # Sanctioned address
        if signals.suspicious_patterns.sanctioned_address_interaction:
            return True
        
        # Critical health factor during high volatility
        if signals.lending_borrowing:
            if signals.lending_borrowing.health_factor < 1.05 and market.volatility_index > 70:
                return True
        
        # Protocol emergency
        if protocol.paused_contracts:
            return True
        
        return False
    
    def _has_positive_signals(self, signals: WalletSignals) -> bool:
        """Check if wallet has positive reputation signals"""
        return (
            signals.ens_name is not None or
            signals.has_gitcoin_passport or
            signals.age_in_days > 365 or
            (signals.on_chain_reputation and signals.on_chain_reputation > 70)
        )
    
    def _has_negative_signals(self, signals: WalletSignals) -> bool:
        """Check if wallet has negative risk signals"""
        patterns = signals.suspicious_patterns
        return (
            patterns.mixer_interaction or
            patterns.rapid_draining or
            patterns.unusual_activity or
            patterns.new_wallet_high_value
        )
