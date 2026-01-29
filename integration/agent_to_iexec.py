"""
Agent to iExec Bridge

Handles escalation from local agent to iExec secure compute
"""

from typing import Optional
import asyncio

from agent import AgentOrchestrator, AgentInput, AgentOutput


class AgentIExecBridge:
    """
    Bridge between local agent and iExec integration
    """
    
    def __init__(self, iexec_config: Optional[dict] = None, contract_address: Optional[str] = None):
        self.local_agent = AgentOrchestrator()
        self.iexec_config = iexec_config or {}
        self.contract_address = contract_address
    
    async def analyze_wallet(self, agent_input: AgentInput) -> AgentOutput:
        """
        Analyze wallet with automatic iExec escalation if needed
        """
        # Try local first
        local_result = self.local_agent.analyze(agent_input)
        
        # Check if needs iExec
        if local_result.decision == 'REQUEST_SEVERITY_ANALYSIS':
            # Escalate to iExec (mock for now)
            return await self._mock_iexec_analysis(agent_input)
        
        return local_result
    
    async def _mock_iexec_analysis(self, agent_input: AgentInput) -> AgentOutput:
        """Mock iExec analysis"""
        await asyncio.sleep(2)  # Simulate delay
        
        # Return enhanced result
        local = self.local_agent.analyze(agent_input)
        return local
