"""
Agent Orchestration System for Multi-Agent Inventory Management

This module provides intelligent routing and coordination between specialized agents.
The orchestrator analyzes user queries and determines which agents to call and in what order.
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import logging
import re
from datetime import datetime

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))
from shared_analytics import analytics_backend

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Intelligent orchestrator that routes tasks to appropriate specialized agents
    and coordinates multi-agent workflows.
    """
    
    def __init__(self):
        """Initialize the agent orchestrator with agent registry and routing rules."""
        self.agent_registry = {
            "descriptive": {
                "name": "Descriptive Analytics Agent",
                "specialization": "Current state analysis and reporting",
                "tools": [
                    "generate_inventory_summary",
                    "get_item_details", 
                    "get_category_overview",
                    "get_stock_alerts",
                    "get_supplier_inventory_summary"
                ],
                "keywords": ["summary", "current", "status", "overview", "details", "what is", "show me", "list", "report"],
                "priority": 1  # First tier - foundation for other analyses
            },
            "diagnostic": {
                "name": "Diagnostic Analytics Agent",
                "specialization": "Root cause analysis and problem diagnosis",
                "tools": [
                    "analyze_stockout_root_cause",
                    "analyze_supplier_performance",
                    "analyze_inventory_turnover",
                    "analyze_demand_patterns",
                    "diagnose_category_issues"
                ],
                "keywords": ["why", "cause", "reason", "problem", "issue", "analyze", "root cause", "performance", "diagnosis"],
                "priority": 2  # Second tier - builds on descriptive
            },
            "predictive": {
                "name": "Predictive Analytics Agent", 
                "specialization": "Forecasting and trend analysis",
                "tools": [
                    "forecast_demand",
                    "predict_stockout_risk",
                    "forecast_inventory_levels",
                    "predict_seasonal_trends"
                ],
                "keywords": ["forecast", "predict", "future", "trend", "will", "expect", "risk", "projection", "ahead"],
                "priority": 3  # Third tier - uses diagnostic insights
            },
            "prescriptive": {
                "name": "Prescriptive Analytics Agent",
                "specialization": "Actionable recommendations and optimization",
                "tools": [
                    "recommend_reorder_strategy",
                    "optimize_safety_stock", 
                    "generate_action_plan",
                    "optimize_inventory_investment"
                ],
                "keywords": ["recommend", "optimize", "should", "action", "strategy", "improve", "solution", "plan"],
                "priority": 4  # Fourth tier - provides actionable solutions
            }
        }
        
        # Define multi-agent workflows for complex queries
        self.workflow_patterns = {
            "comprehensive_analysis": {
                "triggers": ["comprehensive", "complete", "full analysis", "everything", "all aspects"],
                "agent_sequence": ["descriptive", "diagnostic", "predictive", "prescriptive"],
                "description": "Complete 4-tier analysis workflow"
            },
            "problem_solving": {
                "triggers": ["problem", "issue", "fix", "solve", "help with"],
                "agent_sequence": ["descriptive", "diagnostic", "prescriptive"],
                "description": "Problem identification and solution workflow"
            },
            "planning_workflow": {
                "triggers": ["plan", "planning", "strategy", "prepare", "future"],
                "agent_sequence": ["descriptive", "predictive", "prescriptive"],
                "description": "Strategic planning workflow"
            },
            "performance_review": {
                "triggers": ["performance", "review", "evaluation", "assessment"],
                "agent_sequence": ["descriptive", "diagnostic"],
                "description": "Performance evaluation workflow"
            }
        }
    
    def analyze_query(self, query: str) -> Dict[str, Any]:
        """
        Analyze user query to determine intent, entities, and required agents.
        
        Args:
            query: User's natural language query
            
        Returns:
            Dict containing query analysis results
        """
        query_lower = query.lower()
        
        # Extract entities (item IDs, categories, etc.)
        entities = self._extract_entities(query)
        
        # Determine query intent and required agents
        required_agents = []
        confidence_scores = {}
        
        # Check for workflow patterns first
        workflow_match = None
        for workflow_name, workflow_config in self.workflow_patterns.items():
            if any(trigger in query_lower for trigger in workflow_config["triggers"]):
                workflow_match = workflow_name
                required_agents = workflow_config["agent_sequence"]
                break
        
        # If no workflow pattern matched, analyze individual agent requirements
        if not workflow_match:
            for agent_type, agent_config in self.agent_registry.items():
                score = 0
                keyword_matches = []
                
                for keyword in agent_config["keywords"]:
                    if keyword in query_lower:
                        score += 1
                        keyword_matches.append(keyword)
                
                if score > 0:
                    confidence_scores[agent_type] = {
                        "score": score,
                        "matches": keyword_matches,
                        "confidence": min(score / len(agent_config["keywords"]), 1.0)
                    }
                    required_agents.append(agent_type)
        
        # Sort agents by priority if multiple are needed
        if len(required_agents) > 1:
            required_agents.sort(key=lambda x: self.agent_registry[x]["priority"])
        
        analysis = {
            "original_query": query,
            "entities": entities,
            "workflow_pattern": workflow_match,
            "required_agents": required_agents,
            "confidence_scores": confidence_scores,
            "execution_strategy": self._determine_execution_strategy(required_agents, entities),
            "estimated_complexity": "High" if len(required_agents) > 2 else "Medium" if len(required_agents) > 1 else "Low"
        }
        
        return analysis
    
    def _extract_entities(self, query: str) -> Dict[str, Any]:
        """Extract relevant entities from the query (item IDs, categories, dates, etc.)."""
        entities = {
            "item_ids": [],
            "categories": [],
            "suppliers": [],
            "date_ranges": [],
            "metrics": []
        }
        
        # Extract item IDs (ITEM_XXX pattern)
        item_pattern = r'ITEM_(\d{3})'
        item_matches = re.findall(item_pattern, query.upper())
        entities["item_ids"] = [f"ITEM_{match}" for match in item_matches]
        
        # Extract supplier IDs (SUP_XXX pattern)
        supplier_pattern = r'SUP_(\d{3})'
        supplier_matches = re.findall(supplier_pattern, query.upper())
        entities["suppliers"] = [f"SUP_{match}" for match in supplier_matches]
        
        # Extract categories
        categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books"]
        for category in categories:
            if category.lower() in query.lower():
                entities["categories"].append(category)
        
        # Extract date patterns (simplified)
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'last \d+ days?',
            r'next \d+ days?',
            r'past \d+ months?'
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, query.lower())
            entities["date_ranges"].extend(matches)
        
        # Extract common metrics
        metrics = ["service level", "budget", "forecast period", "lead time"]
        for metric in metrics:
            if metric in query.lower():
                entities["metrics"].append(metric)
        
        return entities
    
    def _determine_execution_strategy(self, required_agents: List[str], entities: Dict[str, Any]) -> Dict[str, Any]:
        """Determine how to execute the multi-agent workflow."""
        strategy = {
            "execution_type": "sequential",  # or "parallel" for independent analyses
            "data_sharing": True,  # Whether agents should share intermediate results
            "consolidation_required": len(required_agents) > 1,
            "priority_order": required_agents.copy()
        }
        
        # Determine if parallel execution is possible
        if len(required_agents) > 1:
            # Check if agents have dependencies
            has_dependencies = any(
                self.agent_registry[agent]["priority"] > 1 
                for agent in required_agents
            )
            
            if not has_dependencies:
                strategy["execution_type"] = "parallel"
        
        return strategy
    
    def route_query(self, query: str) -> Dict[str, Any]:
        """
        Main routing function that analyzes query and returns execution plan.
        
        Args:
            query: User's natural language query
            
        Returns:
            Dict containing complete execution plan for the query
        """
        try:
            # Analyze the query
            analysis = self.analyze_query(query)
            
            # Generate execution plan
            execution_plan = {
                "query_analysis": analysis,
                "execution_steps": [],
                "expected_outputs": [],
                "consolidation_strategy": None
            }
            
            # Create execution steps for each required agent
            for i, agent_type in enumerate(analysis["required_agents"]):
                agent_config = self.agent_registry[agent_type]
                
                # Determine which tool to use based on entities and query
                recommended_tool = self._select_tool_for_agent(agent_type, analysis["entities"], query)
                
                step = {
                    "step_number": i + 1,
                    "agent_type": agent_type,
                    "agent_name": agent_config["name"],
                    "recommended_tool": recommended_tool,
                    "input_parameters": self._generate_tool_parameters(recommended_tool, analysis["entities"]),
                    "depends_on": list(range(1, i + 1)) if analysis["execution_strategy"]["execution_type"] == "sequential" else [],
                    "expected_output_type": self._get_expected_output_type(agent_type, recommended_tool)
                }
                
                execution_plan["execution_steps"].append(step)
                execution_plan["expected_outputs"].append(step["expected_output_type"])
            
            # Define consolidation strategy if multiple agents are involved
            if len(analysis["required_agents"]) > 1:
                execution_plan["consolidation_strategy"] = {
                    "method": "integrated_summary",
                    "focus_areas": [
                        "Key findings from each tier",
                        "Conflicting recommendations resolution",
                        "Prioritized action items",
                        "Implementation timeline"
                    ]
                }
            
            return execution_plan
            
        except Exception as e:
            logger.error(f"Error in query routing: {str(e)}")
            return {"error": f"Failed to route query: {str(e)}"}
    
    def _select_tool_for_agent(self, agent_type: str, entities: Dict[str, Any], query: str) -> str:
        """Select the most appropriate tool for an agent based on query context."""
        agent_config = self.agent_registry[agent_type]
        available_tools = agent_config["tools"]
        
        # Simple tool selection logic based on entities and keywords
        query_lower = query.lower()
        
        if agent_type == "descriptive":
            if entities["item_ids"]:
                return "get_item_details"
            elif entities["categories"]:
                return "get_category_overview"
            elif entities["suppliers"]:
                return "get_supplier_inventory_summary"
            elif "alert" in query_lower or "urgent" in query_lower:
                return "get_stock_alerts"
            else:
                return "generate_inventory_summary"
        
        elif agent_type == "diagnostic":
            if "stockout" in query_lower or "out of stock" in query_lower:
                return "analyze_stockout_root_cause"
            elif "supplier" in query_lower and "performance" in query_lower:
                return "analyze_supplier_performance"
            elif "turnover" in query_lower:
                return "analyze_inventory_turnover"
            elif "demand" in query_lower and "pattern" in query_lower:
                return "analyze_demand_patterns"
            elif entities["categories"]:
                return "diagnose_category_issues"
            else:
                return "analyze_stockout_root_cause"
        
        elif agent_type == "predictive":
            if "risk" in query_lower:
                return "predict_stockout_risk"
            elif "seasonal" in query_lower:
                return "predict_seasonal_trends"
            elif "inventory level" in query_lower:
                return "forecast_inventory_levels"
            else:
                return "forecast_demand"
        
        elif agent_type == "prescriptive":
            if "reorder" in query_lower:
                return "recommend_reorder_strategy"
            elif "safety stock" in query_lower:
                return "optimize_safety_stock"
            elif "budget" in query_lower or "investment" in query_lower:
                return "optimize_inventory_investment"
            else:
                return "generate_action_plan"
        
        # Default to first available tool
        return available_tools[0]
    
    def _generate_tool_parameters(self, tool_name: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Generate appropriate parameters for a tool based on extracted entities."""
        params = {}
        
        # Common parameter mappings
        if entities["item_ids"]:
            params["item_id"] = entities["item_ids"][0]  # Use first item if multiple
        
        if entities["categories"]:
            params["category"] = entities["categories"][0]  # Use first category if multiple
        
        if entities["suppliers"]:
            params["supplier_id"] = entities["suppliers"][0]  # Use first supplier if multiple
        
        # Tool-specific parameter defaults
        if "forecast" in tool_name:
            params["forecast_periods"] = 30  # Default forecast period
        
        if "service_level" in str(entities["metrics"]):
            params["service_level"] = 0.95  # Default service level
        
        if "summary" in tool_name:
            params["start_date"] = "2024-01-01"
            params["end_date"] = "2024-12-31"
        
        return params
    
    def _get_expected_output_type(self, agent_type: str, tool_name: str) -> str:
        """Determine the expected output type for a tool."""
        output_types = {
            "descriptive": "Current state report",
            "diagnostic": "Root cause analysis",
            "predictive": "Forecast and predictions", 
            "prescriptive": "Actionable recommendations"
        }
        
        return output_types.get(agent_type, "Analysis results")


# Global orchestrator instance
orchestrator = AgentOrchestrator()
