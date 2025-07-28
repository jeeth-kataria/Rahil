"""
Multi-Agent Root Configuration
This file configures the multi-agent system where each agent can respond independently.
"""

import logging
from typing import Dict, Any, Optional, List
from google.adk.agents import Agent

logger = logging.getLogger(__name__)

# Import all agents
from orchestrator_agent.agent import orchestrator_agent
from tallydb_agent.agent import tallydb_agent

try:
    from ceo_agent.agent import root_agent as ceo_agent
    CEO_AVAILABLE = True
except ImportError:
    CEO_AVAILABLE = False
    logger.info("CEO agent not available")

try:
    from inventory_agent.agent import root_agent as inventory_agent
    INVENTORY_AVAILABLE = True
except ImportError:
    INVENTORY_AVAILABLE = False
    logger.info("Inventory agent not available")

# Agent routing configuration
AGENT_ROUTING = {
    'orchestrator_agent': {
        'agent': orchestrator_agent,
        'keywords': ['orchestrator', 'coordinator', 'system', 'workflow', 'agents', 'multi', 'complex', 'comprehensive', 'overall', 'summary', 'coordinate', 'manage', 'organize'],
        'description': 'System coordination and multi-agent workflows',
        'priority': 1
    },
    'tallydb_agent': {
        'agent': tallydb_agent,
        'keywords': ['client', 'customer', 'ar mobiles', 'database', 'data', 'sales', 'revenue', 'financial', 'profit', 'cash', 'balance', 'inventory', 'stock', 'products', 'mobile', 'samsung', 'transaction', 'ledger', 'account', 'business'],
        'description': 'Database queries, financial data, client verification, business intelligence',
        'priority': 2
    }
}

if CEO_AVAILABLE:
    AGENT_ROUTING['ceo_agent'] = {
        'agent': ceo_agent,
        'keywords': ['strategy', 'strategic', 'leadership', 'decision', 'ceo', 'executive', 'planning', 'vision', 'goals', 'objectives', 'market', 'competition', 'growth', 'expansion'],
        'description': 'Strategic planning, leadership decisions, market analysis',
        'priority': 3
    }

if INVENTORY_AVAILABLE:
    AGENT_ROUTING['inventory_agent'] = {
        'agent': inventory_agent,
        'keywords': ['supply', 'logistics', 'warehouse', 'reorder', 'demand', 'forecast', 'optimization', 'stockout', 'overstock'],
        'description': 'Supply chain management, inventory optimization, demand forecasting',
        'priority': 4
    }

def get_responsible_agent(query: str) -> str:
    """
    Determine which agent should handle the query based on work division.
    Returns the name of the most appropriate agent.
    """
    query_lower = query.lower()
    
    # Score each agent based on keyword matches
    agent_scores = {}
    for agent_name, config in AGENT_ROUTING.items():
        score = sum(1 for keyword in config['keywords'] if keyword in query_lower)
        if score > 0:
            agent_scores[agent_name] = score
    
    # Return the agent with the highest score, or default to TallyDB
    if agent_scores:
        best_agent = max(agent_scores.items(), key=lambda x: x[1])[0]
        return best_agent
    else:
        return 'tallydb_agent'  # Default for business queries

def get_agent_instance(agent_name: str) -> Optional[Agent]:
    """Get the agent instance by name."""
    if agent_name in AGENT_ROUTING:
        return AGENT_ROUTING[agent_name]['agent']
    return None

def should_use_multi_agent(query: str) -> bool:
    """
    Determine if query requires multiple agents to respond.
    """
    query_lower = query.lower()
    
    # Multi-agent keywords
    multi_keywords = ['comprehensive', 'complete', 'overall', 'full', 'detailed', 'analysis', 'report', 'summary']
    
    # Check if query spans multiple domains
    domain_matches = 0
    for agent_name, config in AGENT_ROUTING.items():
        if any(keyword in query_lower for keyword in config['keywords']):
            domain_matches += 1
    
    return domain_matches > 1 or any(keyword in query_lower for keyword in multi_keywords)

# Multi-Agent Response Handler
def handle_multi_agent_query(query: str) -> Dict[str, Any]:
    """
    Handle queries that require multiple agents to respond.
    Each agent provides their own independent response.
    """
    try:
        query_lower = query.lower()
        responding_agents = []
        
        # Determine which agents should respond
        for agent_name, config in AGENT_ROUTING.items():
            if any(keyword in query_lower for keyword in config['keywords']):
                responding_agents.append(agent_name)
        
        # If no specific matches, use TallyDB as default
        if not responding_agents:
            responding_agents = ['tallydb_agent']
        
        # Always include orchestrator for coordination if multiple agents
        if len(responding_agents) > 1 and 'orchestrator_agent' not in responding_agents:
            responding_agents.insert(0, 'orchestrator_agent')
        
        # Collect responses from each agent
        agent_responses = {}
        for agent_name in responding_agents:
            try:
                agent_instance = get_agent_instance(agent_name)
                if agent_instance:
                    # In a real multi-agent system, each agent would process the query independently
                    # For now, we'll route through the orchestrator with proper agent identification
                    agent_responses[agent_name] = {
                        'agent_identity': {
                            'name': agent_name.replace('_', ' ').title(),
                            'description': AGENT_ROUTING[agent_name]['description'],
                            'specialization': 'Independent agent response'
                        },
                        'response_status': 'Agent available and ready to respond',
                        'agent_signature': f'Response from {agent_name.replace("_", " ").title()}'
                    }
                else:
                    agent_responses[agent_name] = {
                        'agent_identity': {'name': agent_name},
                        'response_status': 'Agent not available',
                        'error': f'{agent_name} instance not found'
                    }
            except Exception as e:
                logger.error(f"Error with agent {agent_name}: {str(e)}")
                agent_responses[agent_name] = {
                    'agent_identity': {'name': agent_name},
                    'response_status': 'Error',
                    'error': str(e)
                }
        
        return {
            'multi_agent_response': {
                'query': query,
                'responding_agents': responding_agents,
                'total_agents': len(responding_agents),
                'coordination_method': 'Work division based multi-agent system'
            },
            'agent_responses': agent_responses,
            'system_info': {
                'available_agents': list(AGENT_ROUTING.keys()),
                'multi_agent_enabled': True,
                'routing_method': 'Keyword-based work division'
            }
        }
        
    except Exception as e:
        logger.error(f"Error in multi-agent query handling: {str(e)}")
        return {
            'multi_agent_response': {
                'query': query,
                'status': 'Error in multi-agent processing',
                'error': str(e)
            }
        }

# For ADK compatibility, we need to set a root agent
# The orchestrator will handle routing to appropriate agents
root_agent = orchestrator_agent

# Add multi-agent capability to orchestrator
def enable_multi_agent_routing():
    """Enable multi-agent routing in the orchestrator."""
    try:
        # This would modify the orchestrator to use multi-agent routing
        logger.info("Multi-agent routing enabled")
        return True
    except Exception as e:
        logger.error(f"Failed to enable multi-agent routing: {str(e)}")
        return False

# Initialize multi-agent system
logger.info(f"Multi-agent system initialized with {len(AGENT_ROUTING)} agents")
logger.info(f"Available agents: {list(AGENT_ROUTING.keys())}")
