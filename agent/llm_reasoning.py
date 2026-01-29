"""
LLM-based reasoning layer

Provides contextual analysis for ambiguous cases using language models.
"""

import json
from typing import Dict, Optional
import openai
from .models import WalletSignals, ProtocolHealthIndicators, MarketVolatilityFlags, DecisionType


class LLMReasoning:
    """
    LLM-based contextual reasoning for complex cases
    
    Used when rule-based analysis is ambiguous or for edge cases requiring
    nuanced understanding.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize LLM reasoning module
        
        Args:
            api_key: Optional API key for LLM provider
            model: Model identifier (e.g., "gpt-4", "claude-3")
        """
        self.api_key = api_key
        self.model = model
        self._llm_available = api_key is not None
    
    def analyze(
        self,
        wallet_signals: WalletSignals,
        protocol_health: ProtocolHealthIndicators,
        market_volatility: MarketVolatilityFlags,
        base_risk_score: float
    ) -> Dict:
        """
        Perform LLM-based analysis for ambiguous cases
        
        Args:
            wallet_signals: Wallet behavior data
            protocol_health: Protocol metrics
            market_volatility: Market conditions
            base_risk_score: Risk score from rule-based engine
            
        Returns:
            Dictionary with LLM decision and reasoning
        """
        if not self._llm_available:
            # Fallback to rule-based decision
            return self._fallback_analysis(base_risk_score)
        
        # Build prompt
        prompt = self._build_prompt(
            wallet_signals,
            protocol_health,
            market_volatility,
            base_risk_score
        )
        
        # Call LLM (placeholder - would integrate with actual LLM API)
        llm_response = self._call_llm(prompt)
        
        # Parse and validate response
        return self._parse_llm_response(llm_response, base_risk_score)
    
    def _build_prompt(
        self,
        signals: WalletSignals,
        protocol: ProtocolHealthIndicators,
        market: MarketVolatilityFlags,
        base_score: float
    ) -> str:
        """Build comprehensive prompt for LLM analysis"""
        
        # Identify positive and negative signals
        positive_signals = []
        if signals.ens_name:
            positive_signals.append(f"ENS name: {signals.ens_name}")
        if signals.has_gitcoin_passport:
            positive_signals.append("Has Gitcoin Passport")
        if signals.age_in_days > 180:
            positive_signals.append(f"Wallet age: {signals.age_in_days} days (established)")
        if signals.on_chain_reputation and signals.on_chain_reputation > 70:
            positive_signals.append(f"On-chain reputation: {signals.on_chain_reputation}/100")
        
        negative_signals = []
        if signals.suspicious_patterns.mixer_interaction:
            negative_signals.append("Tornado Cash / mixer interaction detected")
        if signals.suspicious_patterns.rapid_draining:
            negative_signals.append("Rapid asset drainage pattern")
        if signals.suspicious_patterns.unusual_activity:
            negative_signals.append("Unusual transaction activity spike")
        if signals.suspicious_patterns.new_wallet_high_value:
            negative_signals.append("New wallet with unusually high value")
        
        # Build context
        context_description = self._build_context_description(signals, protocol, market)
        
        prompt = f"""You are an expert DeFi risk analyst. Analyze the following wallet situation and provide a nuanced assessment.

## Wallet Context
Address Hash: {signals.wallet_address[:10]}...
Age: {signals.age_in_days} days
Balance: ${signals.current_balance.total_usd:,.2f}
Transaction History: {signals.total_transactions} transactions

## Risk Signals
- Positive Indicators: {', '.join(positive_signals) if positive_signals else 'None'}
- Negative Indicators: {', '.join(negative_signals) if negative_signals else 'None'}

## Current Situation
{context_description}

## Market Context
Volatility Index: {market.volatility_index}/100
Market Sentiment: {market.market_sentiment}
Flash Crash: {'Yes' if market.flash_crash_detected else 'No'}

## Protocol Health
TVL: ${protocol.total_value_locked:,.2f}
Default Rate: {protocol.default_rate}%
Recent Liquidations (24h): {protocol.liquidation_events_24h}

## Rule-Based Risk Score
{base_score:.1f}/100

## Your Task
1. Assess the TRUE risk level (0-100)
2. Determine if this is:
   - Legitimate user exhibiting normal behavior
   - Privacy-focused user (not malicious)
   - High-risk borrower
   - Potential threat/Sybil attack
   - Victim of compromise

3. Recommend ONE of:
   - NO_ACTION (safe, continue normal operations)
   - MONITOR (elevated risk, watch closely)
   - REQUEST_SEVERITY_ANALYSIS (need more data)
   - ENFORCE_ACTION (immediate protective action)

4. Provide clear reasoning in 2-3 sentences

## Response Format (JSON only, no other text):
{{
  "risk_score": <number 0-100>,
  "classification": "<type>",
  "decision": "<NO_ACTION|MONITOR|REQUEST_SEVERITY_ANALYSIS|ENFORCE_ACTION>",
  "reasoning": "<explanation>",
  "confidence": <number 0-100>
}}"""
        
        return prompt
    
    def _build_context_description(
        self,
        signals: WalletSignals,
        protocol: ProtocolHealthIndicators,
        market: MarketVolatilityFlags
    ) -> str:
        """Build human-readable context description"""
        parts = []
        
        # Transaction velocity
        velocity = signals.transaction_velocity
        parts.append(f"Transaction velocity: {velocity.last_24h} (24h), {velocity.last_7d} (7d), {velocity.last_30d} (30d)")
        
        # DeFi positions
        if signals.lending_borrowing:
            lb = signals.lending_borrowing
            parts.append(f"DeFi Position: ${lb.total_borrowed:,.2f} borrowed, HF: {lb.health_factor:.2f}")
        
        # Recent activity
        if signals.days_since_last_activity > 0:
            parts.append(f"Last activity: {signals.days_since_last_activity} days ago")
        
        return "\n".join(parts)
    
    def _call_llm(self, prompt: str) -> Dict:
        """
        Call LLM API (placeholder implementation)
        
        In production, this would integrate with:
        - OpenAI GPT-4
        - Anthropic Claude
        - Open-source models via API
        """
        if self.api_key:
            client = openai.OpenAI(api_key=self.api_key)
            try:
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    response_format={"type": "json_object"}
                )
                return json.loads(response.choices[0].message.content)
            except Exception as e:
                print(f"LLM Error: {e}")
                # Fallback to mock if API fails
                return {
                    "risk_score": 65,
                    "classification": "Error fallback",
                    "decision": "MONITOR",
                    "reasoning": f"LLM analysis failed: {str(e)}. Defaulting to monitor.",
                    "confidence": 50
                }
        
        return {
            "risk_score": 65,
            "classification": "Privacy-focused user",
            "decision": "MONITOR",
            "reasoning": "Wallet shows mixer interaction but also has strong reputation signals (ENS, Gitcoin). Likely a privacy-conscious user rather than malicious actor. Recommend monitoring rather than immediate action.",
            "confidence": 75
        }
    
    def _parse_llm_response(self, llm_response: Dict, base_score: float) -> Dict:
        """
        Parse and validate LLM response
        
        Applies safety overrides to prevent dangerous decisions
        """
        # Extract fields
        llm_risk_score = float(llm_response.get('risk_score', base_score))
        decision = llm_response.get('decision', 'MONITOR')
        reasoning = llm_response.get('reasoning', '')
        confidence = float(llm_response.get('confidence', 50))
        
        # Safety override: Never downgrade ENFORCE_ACTION if base score is critical
        if base_score > 85 and decision != 'ENFORCE_ACTION':
            decision = 'ENFORCE_ACTION'
            reasoning += " [OVERRIDE: Critical risk detected by rule-based engine]"
            confidence = min(confidence, 70)  # Lower confidence due to override
        
        # Combine rule-based and LLM scores (weighted)
        final_risk_score = (base_score * 0.4) + (llm_risk_score * 0.6)
        
        return {
            'risk_score': final_risk_score,
            'decision': decision,
            'reasoning': reasoning,
            'confidence': confidence,
            'classification': llm_response.get('classification', 'Unknown')
        }
    
    def _fallback_analysis(self, base_risk_score: float) -> Dict:
        """
        Fallback analysis when LLM is unavailable
        
        Uses conservative decision-making based on risk score
        """
        if base_risk_score >= 75:
            decision = 'ENFORCE_ACTION'
            reasoning = "High risk score detected. LLM unavailable - using conservative approach."
        elif base_risk_score >= 50:
            decision = 'MONITOR'
            reasoning = "Elevated risk. LLM unavailable - defaulting to monitoring."
        else:
            decision = 'NO_ACTION'
            reasoning = "Risk within acceptable range."
        
        return {
            'risk_score': base_risk_score,
            'decision': decision,
            'reasoning': reasoning,
            'confidence': 60,  # Lower confidence without LLM
            'classification': 'Automated fallback'
        }
