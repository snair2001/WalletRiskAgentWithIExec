"""
Complete end-to-end integration orchestrator

Coordinates: Agent → iExec → Smart Contract
"""

import asyncio
import json
import time
import hashlib
from typing import Dict, Optional

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import (
    AgentOrchestrator, AgentInput, AgentOutput,
    WalletSignals, ProtocolHealthIndicators,
    MarketVolatilityFlags, RequestMetadata
)


class MockIExecIntegration:
    """
    Mock iExec integration for demonstration
    In production, this would use the real iExec SDK
    """
    
    async def analyze_with_iexec(self, agent_input: AgentInput, timeout: int = 300):
        """Simulate iExec analysis"""
        print("   📤 Sending to iExec TEE...")
        await asyncio.sleep(2)  # Simulate network delay
        
        print("   🔐 Encrypting data...")
        await asyncio.sleep(1)
        
        print("   ⚙️  TEE processing...")
        await asyncio.sleep(3)  # Simulate TEE execution
        
        print("   🔓 Decrypting result...")
        await asyncio.sleep(1)
        
        # Simulate iExec result (enhanced analysis)
        base_orchestrator = AgentOrchestrator()
        local_result = base_orchestrator.analyze(agent_input)
        
        # Simulate LLM enhancement - create new output with updated values
        enhanced_score = min(local_result.risk_score * 1.1, 100)
        
        return AgentOutput(
            decision=local_result.decision,
            confidence=min(local_result.confidence + 10, 100),
            reasoning=f"{local_result.reasoning} [Enhanced by iExec TEE analysis]",
            risk_score=enhanced_score,
            recommendations=local_result.recommendations + ["iExec verification completed"],
            flags=local_result.flags + ["IEXEC_VERIFIED"],
            timestamp=int(time.time()),
            metadata=local_result.metadata
        )


class MockContractBridge:
    """
    Mock smart contract bridge for demonstration
    In production, this would interact with real deployed contract
    """
    
    def __init__(self, contract_address: str):
        self.contract_address = contract_address
        self.submitted_results = []
    
    def submit_result(self, result_dict: Dict, task_id: str, task_proof: bytes):
        """Simulate contract submission"""
        print(f"   📝 Submitting to contract: {self.contract_address[:10]}...")
        
        # Simulate transaction
        tx_hash_bytes = hashlib.sha256(json.dumps(result_dict).encode()).digest()
        tx_hash = tx_hash_bytes.hex()
        
        receipt = {
            'transactionHash': tx_hash,
            'blockNumber': 12345678,
            'status': 1,
            'gasUsed': 250000,
            'logs': []
        }
        
        # Store result
        self.submitted_results.append({
            'result': result_dict,
            'task_id': task_id,
            'receipt': receipt
        })
        
        print(f"   ✅ Transaction confirmed: {tx_hash[:16]}...")
        
        # Simulate event emission
        if result_dict['risk_score'] >= 80:
            print(f"   🚨 Event: CriticalRiskDetected")
        elif result_dict['risk_score'] >= 60:
            print(f"   ⚠️  Event: HighRiskDetected")
        else:
            print(f"   ℹ️  Event: RiskAssessmentRecorded")
        
        return receipt


class EndToEndOrchestrator:
    """
    Orchestrates complete workflow:
    Agent → iExec → Smart Contract
    """
    
    def __init__(
        self,
        iexec_config: Optional[Dict] = None,
        contract_address: str = "0x0000000000000000000000000000000000000000"
    ):
        self.iexec_integration = MockIExecIntegration()
        self.contract_bridge = MockContractBridge(contract_address)
        self.local_agent = AgentOrchestrator()
    
    async def process_wallet_analysis(
        self,
        wallet_address: str,
        wallet_signals: WalletSignals,
        protocol_health: ProtocolHealthIndicators,
        market_volatility: MarketVolatilityFlags,
        metadata: RequestMetadata
    ) -> Dict:
        """
        Complete end-to-end processing
        
        Returns:
            Dictionary with analysis result and transaction receipt
        """
        print(f"\n{'='*60}")
        print(f"🔍 WALLET ANALYSIS: {wallet_address[:16]}...")
        print(f"{'='*60}\n")
        
        # Build agent input
        agent_input = AgentInput(
            wallet_signals=wallet_signals,
            protocol_health=protocol_health,
            market_volatility=market_volatility,
            metadata=metadata
        )
        
        # Step 1: Local Agent Analysis
        print("📊 Phase 1: Local Agent Analysis")
        local_result = self.local_agent.analyze(agent_input)
        
        print(f"   Decision: {local_result.decision}")
        print(f"   Risk Score: {local_result.risk_score:.1f}/100")
        print(f"   Confidence: {local_result.confidence:.1f}%")
        
        # Step 2: Check if iExec needed
        needs_iexec = (
            local_result.decision == 'REQUEST_SEVERITY_ANALYSIS' or
            local_result.risk_score >= 60
        )
        
        if needs_iexec:
            print(f"\n📤 Phase 2: iExec Severity Analysis")
            
            # Send to iExec
            iexec_result = await self.iexec_integration.analyze_with_iexec(
                agent_input,
                timeout=300
            )
            
            final_result = iexec_result
            print(f"   Enhanced Risk Score: {final_result.risk_score:.1f}/100")
            print(f"   Enhanced Confidence: {final_result.confidence:.1f}%")
        else:
            final_result = local_result
            print(f"\n✅ Local analysis sufficient - no iExec needed")
        
        # Step 3: Submit to Smart Contract (if significant risk)
        if final_result.risk_score >= 25:  # MEDIUM or higher
            print(f"\n📝 Phase 3: Smart Contract Submission")
            
            receipt = self.contract_bridge.submit_result(
                final_result.to_dict(),
                task_id=metadata.request_id,
                task_proof=b"mock_proof"
            )
            
            return {
                'analysis': final_result.to_dict(),
                'transaction': receipt,
                'contract_address': self.contract_bridge.contract_address
            }
        else:
            print(f"\n✅ Risk too low - no contract submission needed")
            return {
                'analysis': final_result.to_dict(),
                'transaction': None,
                'contract_address': None
            }
