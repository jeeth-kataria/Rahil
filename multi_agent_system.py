"""
Multi-Agent System Dispatcher
Enables true multi-agent behavior where each agent responds independently based on work division.
"""

import logging
from typing import Dict, Any, Optional
from google.adk.agents import Agent

logger = logging.getLogger(__name__)

class MultiAgentDispatcher:
    """
    Dispatcher that routes queries to appropriate agents based on work division.
    Each agent responds independently in their area of expertise.
    """
    
    def __init__(self):
        self.agents = {}
        self.agent_specializations = {
            'orchestrator_agent': {
                'keywords': ['orchestrator', 'coordinator', 'system', 'workflow', 'agents', 'multi', 'complex', 'comprehensive', 'overall', 'summary'],
                'description': 'System coordination and multi-agent workflows'
            },
            'tallydb_agent': {
                'keywords': ['client', 'customer', 'ar mobiles', 'database', 'data', 'sales', 'revenue', 'financial', 'profit', 'cash', 'balance', 'inventory', 'stock', 'products', 'mobile', 'samsung', 'transaction', 'ledger', 'account', 'business'],
                'description': 'Database queries, financial data, client verification, business intelligence'
            },
            'ceo_agent': {
                'keywords': ['strategy', 'strategic', 'leadership', 'decision', 'ceo', 'executive', 'planning', 'vision', 'goals', 'objectives', 'market', 'competition', 'growth', 'expansion'],
                'description': 'Strategic planning, leadership decisions, market analysis'
            },
            'inventory_agent': {
                'keywords': ['supply', 'logistics', 'warehouse', 'reorder', 'demand', 'forecast', 'optimization', 'stockout', 'overstock'],
                'description': 'Supply chain management, inventory optimization, demand forecasting'
            }
        }
    
    def register_agent(self, agent_name: str, agent_instance: Agent):
        """Register an agent with the dispatcher."""
        self.agents[agent_name] = agent_instance
        logger.info(f"Registered agent: {agent_name}")
    
    def get_responsible_agents(self, query: str) -> list:
        """
        Determine which agents should respond to the query.
        Returns list of agent names that should handle the query.
        """
        query_lower = query.lower()
        responsible_agents = []
        
        # Check each agent's specialization
        for agent_name, spec in self.agent_specializations.items():
            if any(keyword in query_lower for keyword in spec['keywords']):
                responsible_agents.append(agent_name)
        
        # If no specific match, default to TallyDB for business queries
        if not responsible_agents:
            responsible_agents.append('tallydb_agent')
        
        # Always include orchestrator for coordination unless it's a simple single-domain query
        if len(responsible_agents) > 1 or any(term in query_lower for term in ['complex', 'comprehensive', 'overall']):
            if 'orchestrator_agent' not in responsible_agents:
                responsible_agents.insert(0, 'orchestrator_agent')
        
        return responsible_agents
    
    def dispatch_query(self, query: str) -> Dict[str, Any]:
        """
        Dispatch query to appropriate agents and collect their responses.
        """
        try:
            responsible_agents = self.get_responsible_agents(query)
            
            responses = {
                'multi_agent_dispatch': {
                    'query': query,
                    'responsible_agents': responsible_agents,
                    'dispatch_method': 'Work division based routing',
                    'total_agents_responding': len(responsible_agents)
                },
                'agent_responses': {}
            }
            
            # Get response from each responsible agent
            for agent_name in responsible_agents:
                try:
                    if agent_name in self.agents:
                        # This would be the actual agent call in a real multi-agent system
                        # For now, we'll simulate the agent response structure
                        agent_response = self._simulate_agent_response(agent_name, query)
                        responses['agent_responses'][agent_name] = agent_response
                    else:
                        responses['agent_responses'][agent_name] = {
                            'status': 'Agent not available',
                            'message': f'{agent_name} is not currently registered'
                        }
                except Exception as e:
                    logger.error(f"Error getting response from {agent_name}: {str(e)}")
                    responses['agent_responses'][agent_name] = {
                        'status': 'Error',
                        'error': str(e)
                    }
            
            return responses
            
        except Exception as e:
            logger.error(f"Error in multi-agent dispatch: {str(e)}")
            return {
                'multi_agent_dispatch': {
                    'query': query,
                    'status': 'Dispatch failed',
                    'error': str(e)
                }
            }
    
    def _simulate_agent_response(self, agent_name: str, query: str) -> Dict[str, Any]:
        """
        Simulate agent response structure.
        In a real system, this would call the actual agent.
        """
        return {
            'agent_identity': {
                'name': agent_name.replace('_', ' ').title(),
                'specialization': self.agent_specializations[agent_name]['description'],
                'response_method': 'Independent agent response'
            },
            'agent_response': {
                'query_received': query,
                'status': 'Processing with specialized expertise',
                'note': f'This would be the actual response from {agent_name}'
            },
            'agent_signature': f'Response from {agent_name.replace("_", " ").title()}'
        }

# Global dispatcher instance
multi_agent_dispatcher = MultiAgentDispatcher()

def enable_multi_agent_system():
    """
    Enable true multi-agent behavior where each agent responds independently.
    """
    try:
        # Import and register agents
        from orchestrator_agent.agent import orchestrator_agent
        from tallydb_agent.agent import tallydb_agent
        
        multi_agent_dispatcher.register_agent('orchestrator_agent', orchestrator_agent)
        multi_agent_dispatcher.register_agent('tallydb_agent', tallydb_agent)
        
        # Try to register other agents if available
        try:
            from ceo_agent.agent import root_agent as ceo_agent
            multi_agent_dispatcher.register_agent('ceo_agent', ceo_agent)
        except ImportError:
            logger.info("CEO agent not available")
        
        try:
            from inventory_agent.agent import root_agent as inventory_agent
            multi_agent_dispatcher.register_agent('inventory_agent', inventory_agent)
        except ImportError:
            logger.info("Inventory agent not available")
        
        logger.info("Multi-agent system enabled successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to enable multi-agent system: {str(e)}")
        return False

def get_multi_agent_response(query: str) -> Dict[str, Any]:
    """
    Get responses from multiple agents based on work division.
    """
    return multi_agent_dispatcher.dispatch_query(query)
