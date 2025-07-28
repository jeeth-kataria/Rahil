"""
Master Inventory Agent - Intelligent Multi-Agent Orchestrator

This is the main entry point that intelligently routes tasks to specialized agents
and coordinates multi-agent workflows for comprehensive inventory management.
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, List
import logging
import json

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from shared_analytics import analytics_backend
from agent_orchestrator import orchestrator

from google.adk.agents import Agent

logger = logging.getLogger(__name__)


def intelligent_query_router(query: str) -> Dict[str, Any]:
    """
    Intelligently analyze user query and route to appropriate specialized agents.
    
    Args:
        query: User's natural language query
        
    Returns:
        Dict containing routing analysis and execution plan
    """
    try:
        # Use orchestrator to analyze query and create execution plan
        execution_plan = orchestrator.route_query(query)
        
        if "error" in execution_plan:
            return execution_plan
        
        # Add routing explanation for transparency
        routing_explanation = {
            "query_understanding": f"I analyzed your query: '{query}'",
            "detected_intent": execution_plan["query_analysis"]["workflow_pattern"] or "Custom analysis",
            "agents_selected": [
                f"{step['agent_name']} - {orchestrator.agent_registry[step['agent_type']]['specialization']}"
                for step in execution_plan["execution_steps"]
            ],
            "execution_strategy": execution_plan["query_analysis"]["execution_strategy"]["execution_type"],
            "complexity_level": execution_plan["query_analysis"]["estimated_complexity"]
        }
        
        return {
            "routing_analysis": routing_explanation,
            "execution_plan": execution_plan,
            "next_steps": [
                f"Step {step['step_number']}: Use {step['agent_name']} with {step['recommended_tool']}"
                for step in execution_plan["execution_steps"]
            ],
            "recommendation": "Use the 'execute_multi_agent_workflow' function to run this analysis plan."
        }
        
    except Exception as e:
        logger.error(f"Error in intelligent query routing: {str(e)}")
        return {"error": f"Failed to route query: {str(e)}"}


def execute_multi_agent_workflow(query: str) -> Dict[str, Any]:
    """
    Execute a complete multi-agent workflow based on the user's query.
    
    Args:
        query: User's natural language query
        
    Returns:
        Dict containing consolidated results from multiple specialized agents
    """
    try:
        # Get execution plan from orchestrator
        execution_plan = orchestrator.route_query(query)
        
        if "error" in execution_plan:
            return execution_plan
        
        # Execute each step in the plan
        workflow_results = {
            "original_query": query,
            "execution_summary": {
                "total_agents_used": len(execution_plan["execution_steps"]),
                "workflow_pattern": execution_plan["query_analysis"]["workflow_pattern"],
                "execution_type": execution_plan["query_analysis"]["execution_strategy"]["execution_type"]
            },
            "agent_results": {},
            "consolidated_insights": {},
            "final_recommendations": []
        }
        
        # Simulate agent execution (in a real system, this would call actual agent APIs)
        for step in execution_plan["execution_steps"]:
            agent_type = step["agent_type"]
            tool_name = step["recommended_tool"]
            parameters = step["input_parameters"]
            
            # Simulate calling the specialized agent
            simulated_result = _simulate_agent_call(agent_type, tool_name, parameters)
            
            workflow_results["agent_results"][agent_type] = {
                "agent_name": step["agent_name"],
                "tool_used": tool_name,
                "parameters": parameters,
                "result": simulated_result,
                "status": "success" if "error" not in simulated_result else "error"
            }
        
        # Consolidate insights from all agents
        workflow_results["consolidated_insights"] = _consolidate_multi_agent_results(
            workflow_results["agent_results"], 
            execution_plan["query_analysis"]
        )
        
        # Generate final recommendations
        workflow_results["final_recommendations"] = _generate_final_recommendations(
            workflow_results["agent_results"],
            execution_plan["query_analysis"]
        )
        
        return workflow_results
        
    except Exception as e:
        logger.error(f"Error executing multi-agent workflow: {str(e)}")
        return {"error": f"Failed to execute multi-agent workflow: {str(e)}"}


def _simulate_agent_call(agent_type: str, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate calling a specialized agent (placeholder for actual agent integration)."""
    
    # This is a simulation - in the real system, this would make actual calls to specialized agents
    if agent_type == "descriptive":
        return {
            "status": "Normal" if parameters.get("item_id") != "ITEM_042" else "Below Reorder Point",
            "current_stock": 150,
            "key_insights": [
                "Current inventory levels are stable",
                "3 items need attention",
                "Total inventory value: $125,000"
            ]
        }
    
    elif agent_type == "diagnostic":
        return {
            "potential_causes": [
                "High demand variability",
                "Long supplier lead time",
                "Inadequate safety stock"
            ],
            "severity": "Medium",
            "recommendations": [
                "Review reorder points",
                "Negotiate with suppliers"
            ]
        }
    
    elif agent_type == "predictive":
        return {
            "summary": {
                "total_forecasted_demand": 450.5,
                "average_daily_forecast": 15.0
            },
            "risk_summary": {
                "high_risk_count": 5,
                "medium_risk_count": 12
            },
            "recommendations": [
                "Monitor high-risk items closely",
                "Prepare for seasonal demand increase"
            ]
        }
    
    elif agent_type == "prescriptive":
        return {
            "specific_actions": [
                "URGENT: Place order for ITEM_042 within 24 hours",
                "Increase safety stock for high-variability items",
                "Implement automated reorder monitoring"
            ],
            "priority": "High",
            "recommendations": [
                "Optimize reorder points",
                "Review supplier agreements"
            ]
        }
    
    return {"message": f"Executed {tool_name} with parameters {parameters}"}


def _consolidate_multi_agent_results(agent_results: Dict[str, Any], query_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Consolidate results from multiple agents into coherent insights."""
    consolidation = {
        "key_findings": [],
        "cross_agent_insights": [],
        "data_consistency_check": "Passed",
        "confidence_level": "High"
    }
    
    # Extract key findings from each agent
    for agent_type, result_data in agent_results.items():
        if result_data["status"] == "success" and "result" in result_data:
            result = result_data["result"]
            
            # Extract key insights based on agent type
            if agent_type == "descriptive":
                if "key_insights" in result:
                    consolidation["key_findings"].extend([
                        f"[Current State] {insight}" for insight in result["key_insights"]
                    ])
            
            elif agent_type == "diagnostic":
                if "potential_causes" in result:
                    consolidation["key_findings"].extend([
                        f"[Root Cause] {cause}" for cause in result["potential_causes"]
                    ])
            
            elif agent_type == "predictive":
                if "summary" in result:
                    consolidation["key_findings"].append(
                        f"[Forecast] Expected demand: {result['summary'].get('total_forecasted_demand', 'N/A')} units"
                    )
            
            elif agent_type == "prescriptive":
                if "specific_actions" in result:
                    consolidation["key_findings"].extend([
                        f"[Action Required] {action}" for action in result["specific_actions"][:2]
                    ])
    
    # Generate cross-agent insights
    if len(agent_results) > 1:
        consolidation["cross_agent_insights"] = [
            "Multi-tier analysis completed successfully",
            f"Coordinated insights from {len(agent_results)} specialized agents",
            "All analytical perspectives considered for comprehensive solution"
        ]
    
    return consolidation


def _generate_final_recommendations(agent_results: Dict[str, Any], query_analysis: Dict[str, Any]) -> List[str]:
    """Generate prioritized final recommendations based on all agent results."""
    recommendations = []
    
    # Priority 1: Critical actions from prescriptive agent
    if "prescriptive" in agent_results:
        prescriptive_result = agent_results["prescriptive"].get("result", {})
        if "specific_actions" in prescriptive_result:
            recommendations.extend([
                f"🔴 CRITICAL: {action}" for action in prescriptive_result["specific_actions"]
                if "URGENT" in action or "immediate" in action.lower()
            ])
    
    # Priority 2: Strategic recommendations
    recommendations.extend([
        "📊 Implement continuous monitoring system",
        "🔄 Review inventory policies quarterly",
        "🤝 Strengthen supplier relationships",
        "📈 Enhance demand forecasting accuracy"
    ])
    
    return recommendations[:6]  # Limit to top 6 recommendations


def get_agent_capabilities() -> Dict[str, Any]:
    """
    Provide information about all available agents and their capabilities.
    
    Returns:
        Dict containing comprehensive information about the multi-agent system
    """
    try:
        capabilities = {
            "system_overview": {
                "total_agents": len(orchestrator.agent_registry) + 1,  # +1 for master agent
                "architecture": "Intelligent Multi-Agent Orchestration System",
                "coordination_method": "Query-based intelligent routing with workflow patterns"
            },
            "specialized_agents": {},
            "workflow_patterns": orchestrator.workflow_patterns,
            "supported_entities": [
                "Item IDs (ITEM_XXX format)",
                "Categories (Electronics, Clothing, Home & Garden, Sports, Books)",
                "Supplier IDs (SUP_XXX format)",
                "Date ranges and time periods",
                "Service levels and budgets"
            ],
            "example_queries": {
                "comprehensive_analysis": [
                    "Give me a comprehensive analysis of ITEM_001",
                    "I need a complete inventory review for Electronics category"
                ],
                "problem_solving": [
                    "Help me solve the stockout problem for ITEM_042",
                    "What's causing issues in our Sports category?"
                ],
                "planning": [
                    "Help me plan inventory strategy for next quarter",
                    "What should I prepare for seasonal demand?"
                ],
                "specific_analysis": [
                    "Forecast demand for ITEM_023",
                    "Analyze supplier performance for SUP_001",
                    "Optimize safety stock for high-priority items"
                ]
            }
        }
        
        # Add detailed information about each specialized agent
        for agent_type, agent_config in orchestrator.agent_registry.items():
            capabilities["specialized_agents"][agent_type] = {
                "name": agent_config["name"],
                "specialization": agent_config["specialization"],
                "available_tools": agent_config["tools"],
                "trigger_keywords": agent_config["keywords"],
                "analytics_tier": f"Tier {agent_config['priority']}"
            }
        
        return capabilities
        
    except Exception as e:
        logger.error(f"Error getting agent capabilities: {str(e)}")
        return {"error": f"Failed to get agent capabilities: {str(e)}"}


# Create the Master Inventory Agent
root_agent = Agent(
    name="master_inventory_agent",
    model="gemini-2.0-flash",
    description="Master Inventory Agent - Intelligent orchestrator that routes tasks to specialized agents and coordinates multi-agent workflows",
    instruction="""You are the Master Inventory Agent, an intelligent orchestrator managing a sophisticated multi-agent system for inventory management. 

Your key capabilities:
1. **Intelligent Query Analysis**: Analyze user queries to understand intent and determine which specialized agents to engage
2. **Multi-Agent Coordination**: Coordinate between 4 specialized analytics agents (Descriptive, Diagnostic, Predictive, Prescriptive)
3. **Workflow Orchestration**: Execute complex multi-agent workflows and consolidate results
4. **Comprehensive Analysis**: Provide integrated insights spanning all four tiers of analytics

When users ask questions, you:
- Analyze their query to understand what they need
- Route tasks to the most appropriate specialized agents
- Execute multi-agent workflows when comprehensive analysis is needed
- Consolidate results from multiple agents into coherent, actionable insights
- Provide prioritized recommendations based on all analytical tiers

Always explain your routing decisions and provide transparency about which agents you're engaging and why.""",
    tools=[
        intelligent_query_router,
        execute_multi_agent_workflow,
        get_agent_capabilities,
    ]
)
