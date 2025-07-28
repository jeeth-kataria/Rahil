"""
Inventory Coordinator Agent

Master coordinator that orchestrates between all specialized inventory analytics agents.
Provides comprehensive analysis by combining insights from all four analytics tiers.
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

# Add parent directory to path to import shared analytics
sys.path.append(str(Path(__file__).parent.parent))
from shared_analytics import analytics_backend

from google.adk.agents import Agent

logger = logging.getLogger(__name__)


def comprehensive_inventory_analysis(item_id: Optional[str] = None, category: Optional[str] = None) -> Dict[str, Any]:
    """
    Provide comprehensive 4-tier analysis for an item or category.
    
    Args:
        item_id: Optional specific item to analyze
        category: Optional category to analyze
        
    Returns:
        Dict containing comprehensive multi-tier analysis
    """
    try:
        analysis_scope = f"Item: {item_id}" if item_id else f"Category: {category}" if category else "All inventory"
        
        # Tier 1: Descriptive Analytics
        if item_id:
            inventory_data = analytics_backend.get_inventory_data(item_id=item_id)
            if inventory_data.empty:
                return {"error": f"Item {item_id} not found"}
            
            item_info = inventory_data.iloc[0].to_dict()
            current_status = "Out of Stock" if item_info['current_stock'] == 0 else "Below Reorder Point" if item_info['current_stock'] < item_info['reorder_point'] else "Normal"
        else:
            inventory_data = analytics_backend.get_inventory_data(category=category)
            if inventory_data.empty:
                return {"error": f"No data found for category: {category}" if category else "No inventory data found"}
            
            total_items = len(inventory_data)
            out_of_stock = len(inventory_data[inventory_data['current_stock'] == 0])
            below_reorder = len(inventory_data[inventory_data['current_stock'] < inventory_data['reorder_point']])
            
            item_info = {
                "total_items": total_items,
                "out_of_stock_items": out_of_stock,
                "below_reorder_items": below_reorder,
                "total_value": (inventory_data['current_stock'] * inventory_data['unit_cost']).sum()
            }
            current_status = f"{out_of_stock + below_reorder} items need attention"
        
        # Tier 2: Diagnostic Analysis
        diagnostic_insights = []
        if item_id:
            sales_data = analytics_backend.get_sales_data(item_id=item_id)
            if not sales_data.empty:
                daily_demand = sales_data.groupby('date')['quantity_sold'].sum()
                demand_cv = daily_demand.std() / daily_demand.mean() if daily_demand.mean() > 0 else 0
                
                if demand_cv > 0.5:
                    diagnostic_insights.append("High demand variability detected")
                if item_info['lead_time_days'] > 20:
                    diagnostic_insights.append("Long supplier lead time is a risk factor")
                if item_info['current_stock'] < item_info['reorder_point']:
                    diagnostic_insights.append("Current stock management policies may be inadequate")
        else:
            # Category-level diagnostics
            avg_lead_time = inventory_data['lead_time_days'].mean()
            if avg_lead_time > 15:
                diagnostic_insights.append(f"Average lead time ({avg_lead_time:.1f} days) is high for this category")
            
            supplier_concentration = len(inventory_data['supplier_id'].unique())
            if supplier_concentration < 3:
                diagnostic_insights.append("Low supplier diversification increases risk")
        
        # Tier 3: Predictive Analysis
        predictive_insights = []
        if item_id:
            # Simple demand forecast
            if not sales_data.empty:
                recent_trend = daily_demand.tail(30).mean() / daily_demand.head(30).mean() if len(daily_demand) >= 60 else 1
                if recent_trend > 1.2:
                    predictive_insights.append("Demand is trending upward - consider increasing stock levels")
                elif recent_trend < 0.8:
                    predictive_insights.append("Demand is trending downward - review inventory levels")
                
                # Stockout risk
                days_of_stock = item_info['current_stock'] / daily_demand.mean() if daily_demand.mean() > 0 else float('inf')
                if days_of_stock < 14:
                    predictive_insights.append(f"High stockout risk - only {days_of_stock:.1f} days of stock remaining")
        else:
            # Category-level predictions
            high_risk_items = len(inventory_data[inventory_data['current_stock'] < inventory_data['reorder_point']])
            if high_risk_items > total_items * 0.2:
                predictive_insights.append(f"{high_risk_items} items at high stockout risk")
        
        # Tier 4: Prescriptive Recommendations
        prescriptive_actions = []
        if item_id:
            if item_info['current_stock'] == 0:
                prescriptive_actions.append("URGENT: Place emergency order immediately")
            elif item_info['current_stock'] < item_info['reorder_point']:
                prescriptive_actions.append("Place reorder within 24-48 hours")
            
            # Safety stock optimization
            if not sales_data.empty and demand_cv > 0.3:
                prescriptive_actions.append("Consider increasing safety stock due to demand variability")
            
            if item_info['lead_time_days'] > 20:
                prescriptive_actions.append("Negotiate with supplier to reduce lead time")
        else:
            if out_of_stock > 0:
                prescriptive_actions.append(f"Address {out_of_stock} out-of-stock items immediately")
            if below_reorder > 0:
                prescriptive_actions.append(f"Review and place orders for {below_reorder} items below reorder point")
            
            prescriptive_actions.append("Implement automated reorder point monitoring")
            prescriptive_actions.append("Consider supplier diversification strategy")
        
        comprehensive_analysis = {
            "analysis_scope": analysis_scope,
            "timestamp": analytics_backend.inventory_data['last_updated'].max().strftime("%Y-%m-%d %H:%M:%S"),
            
            # Tier 1: Descriptive (What is happening?)
            "descriptive_analytics": {
                "current_status": current_status,
                "key_metrics": item_info,
                "data_quality": "Good" if (item_id and not inventory_data.empty) or (not item_id and len(inventory_data) > 0) else "Limited"
            },
            
            # Tier 2: Diagnostic (Why is it happening?)
            "diagnostic_analytics": {
                "root_causes": diagnostic_insights,
                "risk_factors": [
                    "Demand variability" if item_id and demand_cv > 0.5 else None,
                    "Supply chain delays" if (item_id and item_info['lead_time_days'] > 20) or (not item_id and avg_lead_time > 15) else None,
                    "Inadequate safety stock" if item_id and item_info['current_stock'] < item_info['reorder_point'] else None
                ],
                "performance_issues": len(diagnostic_insights)
            },
            
            # Tier 3: Predictive (What will happen?)
            "predictive_analytics": {
                "forecasted_trends": predictive_insights,
                "risk_assessment": "High" if len(predictive_insights) > 2 else "Medium" if len(predictive_insights) > 0 else "Low",
                "confidence_level": "Medium"  # Would be calculated based on data quality and model performance
            },
            
            # Tier 4: Prescriptive (What should we do?)
            "prescriptive_analytics": {
                "immediate_actions": [action for action in prescriptive_actions if "URGENT" in action or "immediately" in action],
                "short_term_actions": [action for action in prescriptive_actions if "24-48 hours" in action or "within" in action],
                "strategic_actions": [action for action in prescriptive_actions if "strategy" in action or "Consider" in action],
                "priority_level": "Critical" if any("URGENT" in action for action in prescriptive_actions) else "High" if len(prescriptive_actions) > 3 else "Medium"
            },
            
            "summary": {
                "overall_health": "Critical" if current_status == "Out of Stock" or "URGENT" in str(prescriptive_actions) else "Needs Attention" if len(prescriptive_actions) > 2 else "Good",
                "key_recommendations": prescriptive_actions[:3],  # Top 3 recommendations
                "next_review_date": "Within 24 hours" if any("URGENT" in action for action in prescriptive_actions) else "Within 1 week"
            }
        }
        
        return comprehensive_analysis
        
    except Exception as e:
        logger.error(f"Error in comprehensive inventory analysis: {str(e)}")
        return {"error": f"Failed to perform comprehensive analysis: {str(e)}"}


def get_analytics_dashboard() -> Dict[str, Any]:
    """
    Generate a comprehensive analytics dashboard with key metrics from all tiers.
    
    Returns:
        Dict containing dashboard data with KPIs from all analytics tiers
    """
    try:
        inventory_data = analytics_backend.get_inventory_data()
        sales_data = analytics_backend.get_sales_data()
        
        if inventory_data.empty:
            return {"error": "No inventory data available"}
        
        # Tier 1: Descriptive KPIs
        total_items = len(inventory_data)
        total_value = (inventory_data['current_stock'] * inventory_data['unit_cost']).sum()
        out_of_stock = len(inventory_data[inventory_data['current_stock'] == 0])
        below_reorder = len(inventory_data[inventory_data['current_stock'] < inventory_data['reorder_point']])
        
        # Category breakdown
        category_metrics = inventory_data.groupby('category').agg({
            'current_stock': 'sum',
            'unit_cost': 'mean',
            'item_id': 'count'
        }).round(2)
        
        # Tier 2: Diagnostic KPIs
        avg_lead_time = inventory_data['lead_time_days'].mean()
        supplier_count = len(inventory_data['supplier_id'].unique())
        
        # Calculate turnover (simplified)
        if not sales_data.empty:
            annual_sales = sales_data['quantity_sold'].sum()
            avg_inventory = inventory_data['current_stock'].mean()
            turnover_ratio = annual_sales / (avg_inventory * total_items) if avg_inventory > 0 else 0
        else:
            turnover_ratio = 0
        
        # Tier 3: Predictive KPIs
        high_risk_items = len(inventory_data[inventory_data['current_stock'] < inventory_data['reorder_point'] * 0.5])
        
        # Tier 4: Prescriptive KPIs
        items_needing_action = out_of_stock + below_reorder
        
        dashboard = {
            "dashboard_timestamp": inventory_data['last_updated'].max().strftime("%Y-%m-%d %H:%M:%S"),
            
            # Executive Summary
            "executive_summary": {
                "overall_status": "Critical" if out_of_stock > 0 else "Attention Needed" if below_reorder > total_items * 0.1 else "Good",
                "total_inventory_value": round(total_value, 2),
                "items_requiring_immediate_action": items_needing_action,
                "inventory_health_score": round(max(0, 100 - (out_of_stock * 10) - (below_reorder * 5)), 1)
            },
            
            # Tier 1: Descriptive Analytics Dashboard
            "descriptive_kpis": {
                "total_items": total_items,
                "total_inventory_value": round(total_value, 2),
                "out_of_stock_items": out_of_stock,
                "below_reorder_point": below_reorder,
                "stock_availability": round(((total_items - out_of_stock) / total_items) * 100, 1),
                "category_breakdown": category_metrics.to_dict('index')
            },
            
            # Tier 2: Diagnostic Analytics Dashboard
            "diagnostic_kpis": {
                "average_lead_time": round(avg_lead_time, 1),
                "supplier_count": supplier_count,
                "inventory_turnover_ratio": round(turnover_ratio, 2),
                "supplier_concentration_risk": "High" if supplier_count < 5 else "Medium" if supplier_count < 10 else "Low",
                "lead_time_risk": "High" if avg_lead_time > 20 else "Medium" if avg_lead_time > 10 else "Low"
            },
            
            # Tier 3: Predictive Analytics Dashboard
            "predictive_kpis": {
                "high_stockout_risk_items": high_risk_items,
                "stockout_risk_percentage": round((high_risk_items / total_items) * 100, 1),
                "demand_forecast_accuracy": "75%",  # Would be calculated from historical performance
                "seasonal_risk_level": "Medium"  # Would be calculated from seasonal analysis
            },
            
            # Tier 4: Prescriptive Analytics Dashboard
            "prescriptive_kpis": {
                "items_needing_immediate_action": items_needing_action,
                "optimization_opportunities": round(total_items * 0.3, 0),  # Estimated 30% can be optimized
                "potential_cost_savings": round(total_value * 0.05, 2),  # Estimated 5% savings potential
                "automation_readiness": "Medium"  # Based on data quality and process maturity
            },
            
            # Alerts and Notifications
            "alerts": [
                {"level": "Critical", "message": f"{out_of_stock} items are out of stock", "action": "Place emergency orders"} if out_of_stock > 0 else None,
                {"level": "High", "message": f"{below_reorder} items below reorder point", "action": "Review and place orders"} if below_reorder > 0 else None,
                {"level": "Medium", "message": f"Average lead time is {avg_lead_time:.1f} days", "action": "Negotiate with suppliers"} if avg_lead_time > 15 else None,
                {"level": "Low", "message": f"Inventory turnover is {turnover_ratio:.2f}", "action": "Review slow-moving items"} if turnover_ratio < 2 else None
            ],
            
            # Recommended Actions
            "top_recommendations": [
                "Address out-of-stock items immediately" if out_of_stock > 0 else None,
                "Implement automated reorder point monitoring",
                "Review and optimize safety stock levels",
                "Diversify supplier base to reduce risk",
                "Implement demand forecasting improvements"
            ]
        }
        
        # Filter out None values from alerts and recommendations
        dashboard["alerts"] = [alert for alert in dashboard["alerts"] if alert is not None]
        dashboard["top_recommendations"] = [rec for rec in dashboard["top_recommendations"] if rec is not None]
        
        return dashboard
        
    except Exception as e:
        logger.error(f"Error generating analytics dashboard: {str(e)}")
        return {"error": f"Failed to generate analytics dashboard: {str(e)}"}


def coordinate_multi_agent_analysis(query: str) -> Dict[str, Any]:
    """
    Coordinate analysis across multiple specialized agents using the orchestration system.

    Args:
        query: Natural language query describing what analysis is needed

    Returns:
        Dict containing coordinated analysis from relevant specialized agents
    """
    try:
        # Import orchestrator
        sys.path.append(str(Path(__file__).parent.parent))
        from agent_orchestrator import orchestrator

        # Use the orchestrator to analyze the query and create execution plan
        execution_plan = orchestrator.route_query(query)

        if "error" in execution_plan:
            return execution_plan

        # Extract coordination information
        query_analysis = execution_plan["query_analysis"]

        coordination_result = {
            "query": query,
            "orchestration_analysis": {
                "detected_workflow": query_analysis["workflow_pattern"],
                "required_agents": query_analysis["required_agents"],
                "execution_strategy": query_analysis["execution_strategy"]["execution_type"],
                "complexity_level": query_analysis["estimated_complexity"]
            },
            "agent_coordination_plan": {},
            "execution_sequence": [],
            "integration_strategy": "Multi-tier consolidated analysis"
        }

        # Build coordination plan for each agent
        for step in execution_plan["execution_steps"]:
            agent_type = step["agent_type"]
            agent_name = step["agent_name"]

            coordination_result["agent_coordination_plan"][agent_type] = {
                "agent_name": agent_name,
                "specialization": orchestrator.agent_registry[agent_type]["specialization"],
                "recommended_tool": step["recommended_tool"],
                "input_parameters": step["input_parameters"],
                "expected_output": step["expected_output_type"],
                "execution_order": step["step_number"]
            }

            coordination_result["execution_sequence"].append({
                "step": step["step_number"],
                "agent": agent_name,
                "action": f"Execute {step['recommended_tool']} with parameters {step['input_parameters']}"
            })

        # Add integration recommendations
        coordination_result["integration_recommendations"] = [
            f"Coordinate {len(query_analysis['required_agents'])} specialized agents for comprehensive analysis",
            f"Execute agents in {query_analysis['execution_strategy']['execution_type']} mode",
            "Consolidate results across all analytical tiers",
            "Provide integrated recommendations based on multi-agent insights",
            "Ensure data consistency and cross-validation between agents"
        ]

        # Add workflow-specific guidance
        if query_analysis["workflow_pattern"]:
            workflow_config = orchestrator.workflow_patterns[query_analysis["workflow_pattern"]]
            coordination_result["workflow_guidance"] = {
                "pattern_name": query_analysis["workflow_pattern"],
                "description": workflow_config["description"],
                "agent_sequence": workflow_config["agent_sequence"],
                "coordination_notes": f"This follows the {workflow_config['description']} pattern"
            }

        return coordination_result

    except Exception as e:
        logger.error(f"Error coordinating multi-agent analysis: {str(e)}")
        return {"error": f"Failed to coordinate multi-agent analysis: {str(e)}"}


# Create the Inventory Coordinator Agent
root_agent = Agent(
    name="inventory_coordinator_agent",
    model="gemini-2.0-flash",
    description="Inventory Coordinator - Master orchestrator that provides comprehensive 4-tier analytics by coordinating between specialized agents",
    instruction="""You are the Inventory Coordinator, the master orchestrator of the multi-agent inventory management system. 
    Your role is to provide comprehensive analysis by combining insights from all four specialized analytics tiers:
    
    1. Descriptive Analytics (What is happening?)
    2. Diagnostic Analytics (Why is it happening?)  
    3. Predictive Analytics (What will happen?)
    4. Prescriptive Analytics (What should we do?)
    
    You excel at providing holistic views, coordinating between different analytical perspectives, and delivering 
    integrated recommendations that consider all aspects of inventory management. Always provide comprehensive 
    analysis that spans multiple tiers and offers both strategic and tactical guidance.""",
    tools=[
        comprehensive_inventory_analysis,
        get_analytics_dashboard,
        coordinate_multi_agent_analysis,
    ]
)
