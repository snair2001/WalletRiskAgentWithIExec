"""
Main Agent Orchestrator

Coordinates rule-based and LLM reasoning to produce final decisions.
"""

import time
from typing import Optional
from .models import AgentInput, AgentOutput, OutputMetadata, DecisionType
from .rules import RuleBasedEngine
from .llm_reasoning import LLMReasoning


class AgentOrchestrator:
    """
    Main decision engine orchestrator
    
    Coordinates between rule-based engine and LLM reasoning layer
    to produce final risk assessments and decisions.
    """
    
    def __init__(self, llm_api_key: Optional[str] = None):
        """
        Initialize the agent orchestrator
        
        Args:
            llm_api_key: Optional API key for LLM provider
        """
        self.rule_engine = RuleBasedEngine()
        self.llm_reasoning = LLMReasoning(api_key=llm_api_key)
    
    def analyze(self, agent_input: AgentInput) -> AgentOutput:
        """
        Perform complete wallet risk analysis
        
        Args:
            agent_input: Complete input data
            
        Returns:
            AgentOutput with decision and reasoning
        """
        start_time = time.time()
        
        # Phase 1: Rule-based analysis
        risk_score = self.rule_engine.calculate_risk_score(agent_input)
        
        decision, needs_llm = self.rule_engine.map_score_to_decision(
            risk_score,
            agent_input.wallet_signals,
            agent_input.protocol_health,
            agent_input.market_volatility
        )
        
        # Phase 2: LLM analysis (if needed)
        llm_used = False
        llm_score = None
        reasoning = ""
        confidence = 0.0
        
        if needs_llm or decision == 'REQUEST_SEVERITY_ANALYSIS':
            llm_result = self.llm_reasoning.analyze(
                agent_input.wallet_signals,
                agent_input.protocol_health,
                agent_input.market_volatility,
                risk_score
            )
            
            # Override with LLM analysis
            decision = llm_result['decision']
            risk_score = llm_result['risk_score']
            reasoning = llm_result['reasoning']
            confidence = llm_result['confidence']
            llm_score = llm_result['risk_score']
            llm_used = True
        else:
            # Use rule-based reasoning
            reasoning = self._generate_rule_based_reasoning(
                decision,
                risk_score,
                agent_input
            )
            confidence = self._calculate_rule_based_confidence(risk_score)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            decision,
            risk_score,
            agent_input
        )
        
        # Extract flags
        flags = self._extract_flags(agent_input, risk_score)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000  # ms
        
        # Build metadata
        metadata = OutputMetadata(
            processing_time_ms=processing_time,
            llm_used=llm_used,
            rule_based_score=risk_score if not llm_used else self.rule_engine.calculate_risk_score(agent_input),
            llm_score=llm_score
        )
        
        return AgentOutput(
            decision=decision,
            confidence=confidence,
            reasoning=reasoning,
            risk_score=risk_score,
            recommendations=recommendations,
            flags=flags,
            timestamp=int(time.time()),
            metadata=metadata
        )
    
    def _generate_rule_based_reasoning(
        self,
        decision: DecisionType,
        risk_score: float,
        agent_input: AgentInput
    ) -> str:
        """Generate human-readable reasoning for rule-based decisions"""
        signals = agent_input.wallet_signals
        protocol = agent_input.protocol_health
        market = agent_input.market_volatility
        
        parts = []
        
        # Decision header
        parts.append(f"Risk Score: {risk_score:.1f}/100. ")
        
        # Key risk factors
        if signals.age_in_days < 30:
            parts.append(f"New wallet ({signals.age_in_days} days old). ")
        
        if signals.lending_borrowing and signals.lending_borrowing.health_factor < 1.5:
            parts.append(f"Health factor {signals.lending_borrowing.health_factor:.2f} - liquidation risk. ")
        
        if signals.suspicious_patterns.rapid_draining:
            parts.append("Rapid asset drainage detected. ")
        
        if signals.suspicious_patterns.mixer_interaction:
            parts.append("Privacy mixer interaction found. ")
        
        # Market context
        if market.volatility_index > 70:
            parts.append(f"High market volatility ({market.volatility_index}/100). ")
        
        # Protocol context
        if protocol.default_rate > 5.0:
            parts.append(f"Elevated protocol default rate ({protocol.default_rate}%). ")
        
        # Positive factors
        if signals.has_gitcoin_passport:
            parts.append("Gitcoin Passport verified. ")
        
        if signals.ens_name:
            parts.append(f"ENS: {signals.ens_name}. ")
        
        return "".join(parts).strip()
    
    def _calculate_rule_based_confidence(self, risk_score: float) -> float:
        """Calculate confidence for rule-based decisions"""
        # Scores near decision boundaries have lower confidence
        boundaries = [30, 60, 80]
        min_distance = min(abs(risk_score - b) for b in boundaries)
        
        # Distance of 10+ points gives high confidence
        if min_distance >= 10:
            return 90.0
        elif min_distance >= 5:
            return 75.0
        else:
            return 60.0
    
    def _generate_recommendations(
        self,
        decision: DecisionType,
        risk_score: float,
        agent_input: AgentInput
    ) -> list:
        """Generate actionable recommendations based on decision"""
        recommendations = []
        signals = agent_input.wallet_signals
        
        if decision == 'NO_ACTION':
            recommendations.append("Continue normal monitoring")
            if signals.lending_borrowing and signals.lending_borrowing.health_factor < 2.0:
                recommendations.append("Monitor health factor - currently safe but could improve")
        
        elif decision == 'MONITOR':
            recommendations.append("Increase monitoring frequency to hourly")
            
            if signals.lending_borrowing and signals.lending_borrowing.health_factor < 1.5:
                recommendations.append(f"Set alert for health factor < 1.2")
            
            if signals.suspicious_patterns.unusual_activity:
                recommendations.append("Watch for continued unusual transaction patterns")
            
            recommendations.append("Review again in 24 hours")
        
        elif decision == 'REQUEST_SEVERITY_ANALYSIS':
            recommendations.append("Escalate to human review or advanced LLM analysis")
            recommendations.append("Gather additional context on flagged behaviors")
            
            if signals.suspicious_patterns.mixer_interaction:
                recommendations.append("Investigate mixer usage - potentially legitimate privacy concern")
        
        elif decision == 'ENFORCE_ACTION':
            recommendations.append("IMMEDIATE: Notify wallet owner")
            
            if signals.lending_borrowing and signals.lending_borrowing.health_factor < 1.2:
                recommendations.append("IMMEDIATE: Suggest collateral top-up")
                recommendations.append("IMMEDIATE: Prepare liquidation if health factor < 1.0")
            
            if signals.suspicious_patterns.sanctioned_address_interaction:
                recommendations.append("IMMEDIATE: Freeze position pending compliance review")
            
            if signals.suspicious_patterns.rapid_draining:
                recommendations.append("URGENT: Investigate potential compromise")
                recommendations.append("Consider temporary position freeze")
        
        return recommendations
    
    def _extract_flags(self, agent_input: AgentInput, risk_score: float) -> list:
        """Extract relevant flags for the decision"""
        flags = []
        signals = agent_input.wallet_signals
        market = agent_input.market_volatility
        
        # Wallet age flags
        if signals.age_in_days < 7:
            flags.append("VERY_NEW_WALLET")
        elif signals.age_in_days < 30:
            flags.append("NEW_WALLET")
        
        # Suspicious pattern flags
        if signals.suspicious_patterns.rapid_draining:
            flags.append("RAPID_DRAINAGE")
        
        if signals.suspicious_patterns.mixer_interaction:
            flags.append("MIXER_INTERACTION")
        
        if signals.suspicious_patterns.unusual_activity:
            flags.append("UNUSUAL_ACTIVITY")
        
        if signals.suspicious_patterns.sanctioned_address_interaction:
            flags.append("SANCTIONED_ADDRESS")
        
        # DeFi health flags
        if signals.lending_borrowing:
            hf = signals.lending_borrowing.health_factor
            if hf < 1.1:
                flags.append("CRITICAL_HEALTH_FACTOR")
            elif hf < 1.3:
                flags.append("LOW_HEALTH_FACTOR")
            elif hf < 1.5:
                flags.append("DECLINING_HEALTH_FACTOR")
        
        # Market flags
        if market.volatility_index > 70:
            flags.append("HIGH_MARKET_VOLATILITY")
        
        if market.flash_crash_detected:
            flags.append("FLASH_CRASH_ACTIVE")
        
        # Reputation flags
        if signals.has_gitcoin_passport:
            flags.append("GITCOIN_VERIFIED")
        
        if signals.ens_name:
            flags.append("HAS_ENS")
        
        return flags


# Convenience function for quick analysis
def analyze_wallet(
    wallet_signals,
    protocol_health,
    market_volatility,
    metadata,
    llm_api_key: Optional[str] = None
) -> AgentOutput:
    """
    Convenience function for wallet analysis
    
    Args:
        wallet_signals: WalletSignals object
        protocol_health: ProtocolHealthIndicators object
        market_volatility: MarketVolatilityFlags object
        metadata: RequestMetadata object
        llm_api_key: Optional LLM API key
        
    Returns:
        AgentOutput with decision
    """
    agent_input = AgentInput(
        wallet_signals=wallet_signals,
        protocol_health=protocol_health,
        market_volatility=market_volatility,
        metadata=metadata
    )
    
    orchestrator = AgentOrchestrator(llm_api_key=llm_api_key)
    return orchestrator.analyze(agent_input)
