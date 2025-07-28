"""
Prescriptive Analytics Agent - Tier 4

Specializes in actionable recommendations and optimization strategies.
Provides specific actions to optimize inventory performance and solve problems.
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add parent directory to path to import shared analytics
sys.path.append(str(Path(__file__).parent.parent))
from shared_analytics import analytics_backend

from google.adk.agents import Agent

logger = logging.getLogger(__name__)


def recommend_reorder_strategy(item_id: str, service_level: float = 0.95) -> Dict[str, Any]:
    """
    Generate optimal reorder strategy recommendations with detailed calculations.
    
    Args:
        item_id: Unique identifier for the inventory item
        service_level: Desired service level (0.0 to 1.0)
        
    Returns:
        Dict containing comprehensive reorder strategy recommendations
    """
    try:
        if not 0.0 <= service_level <= 1.0:
            return {"error": "Service level must be between 0.0 and 1.0"}
        
        inventory_data = analytics_backend.get_inventory_data(item_id=item_id)
        
        if inventory_data.empty:
            return {"error": f"Item {item_id} not found"}
        
        item_info = inventory_data.iloc[0]
        sales_data = analytics_backend.get_sales_data(item_id=item_id)
        
        daily_demand = sales_data.groupby('date')['quantity_sold'].sum()
        avg_demand = daily_demand.mean() if len(daily_demand) > 0 else 0
        demand_std = daily_demand.std() if len(daily_demand) > 1 else 0
        
        # Advanced safety stock calculation
        from scipy import stats
        z_score = stats.norm.ppf(service_level)
        safety_stock = z_score * demand_std * np.sqrt(item_info['lead_time_days'])
        
        reorder_point = (avg_demand * item_info['lead_time_days']) + safety_stock
        
        # Economic Order Quantity (EOQ) calculation
        holding_cost_rate = 0.20  # 20% annual holding cost
        ordering_cost = 50  # Fixed ordering cost
        annual_demand = avg_demand * 365
        
        if annual_demand > 0 and item_info['unit_cost'] > 0:
            eoq = np.sqrt((2 * annual_demand * ordering_cost) / 
                         (item_info['unit_cost'] * holding_cost_rate))
        else:
            eoq = 100
        
        # Calculate total costs
        annual_holding_cost = (eoq / 2) * item_info['unit_cost'] * holding_cost_rate
        annual_ordering_cost = (annual_demand / eoq) * ordering_cost if eoq > 0 else 0
        total_annual_cost = annual_holding_cost + annual_ordering_cost
        
        recommendations = {
            "item_id": item_id,
            "item_name": item_info['item_name'],
            "current_settings": {
                "current_reorder_point": int(item_info['reorder_point']),
                "current_stock": int(item_info['current_stock']),
                "max_stock": int(item_info['max_stock'])
            },
            "recommended_settings": {
                "recommended_reorder_point": round(max(0, reorder_point), 0),
                "recommended_order_quantity": round(max(1, eoq), 0),
                "safety_stock": round(max(0, safety_stock), 0),
                "service_level": service_level
            },
            "demand_analysis": {
                "average_daily_demand": round(avg_demand, 2),
                "demand_variability": round(demand_std, 2),
                "lead_time_days": int(item_info['lead_time_days']),
                "annual_demand": round(annual_demand, 2)
            },
            "cost_analysis": {
                "unit_cost": item_info['unit_cost'],
                "annual_holding_cost": round(annual_holding_cost, 2),
                "annual_ordering_cost": round(annual_ordering_cost, 2),
                "total_annual_cost": round(total_annual_cost, 2),
                "cost_per_unit": round(total_annual_cost / annual_demand, 4) if annual_demand > 0 else 0
            },
            "specific_actions": [],
            "priority": "Normal",
            "implementation_timeline": "Immediate"
        }
        
        # Generate specific actionable recommendations
        if reorder_point > item_info['reorder_point']:
            recommendations["specific_actions"].append(
                f"Increase reorder point from {item_info['reorder_point']} to {round(reorder_point, 0)} units"
            )
            recommendations["priority"] = "High"
        
        if item_info['current_stock'] < reorder_point:
            urgent_order_qty = round(reorder_point - item_info['current_stock'] + eoq, 0)
            recommendations["specific_actions"].append(
                f"URGENT: Place immediate order for {urgent_order_qty} units"
            )
            recommendations["priority"] = "Critical"
            recommendations["implementation_timeline"] = "Within 24 hours"
        
        if eoq != item_info.get('standard_order_qty', eoq):
            recommendations["specific_actions"].append(
                f"Optimize order quantity to {round(eoq, 0)} units for cost efficiency"
            )
        
        # Additional optimization recommendations
        if demand_std / avg_demand > 0.5:  # High variability
            recommendations["specific_actions"].append(
                "Consider dynamic safety stock due to high demand variability"
            )
        
        if item_info['lead_time_days'] > 20:
            recommendations["specific_actions"].append(
                "Work with supplier to reduce lead time for better inventory efficiency"
            )
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error generating reorder strategy for {item_id}: {str(e)}")
        return {"error": f"Failed to generate reorder strategy: {str(e)}"}


def optimize_safety_stock(item_id: str, target_service_level: float = 0.95) -> Dict[str, Any]:
    """
    Optimize safety stock levels for specific service level targets.
    
    Args:
        item_id: Item to optimize safety stock for
        target_service_level: Target service level (0.0 to 1.0)
        
    Returns:
        Dict containing safety stock optimization recommendations
    """
    try:
        inventory_data = analytics_backend.get_inventory_data(item_id=item_id)
        
        if inventory_data.empty:
            return {"error": f"Item {item_id} not found"}
        
        item_info = inventory_data.iloc[0]
        sales_data = analytics_backend.get_sales_data(item_id=item_id)
        
        daily_demand = sales_data.groupby('date')['quantity_sold'].sum()
        avg_demand = daily_demand.mean() if len(daily_demand) > 0 else 0
        demand_std = daily_demand.std() if len(daily_demand) > 1 else avg_demand * 0.3
        
        # Calculate safety stock for different service levels
        from scipy import stats
        service_levels = [0.90, 0.95, 0.98, 0.99]
        safety_stock_options = []
        
        for sl in service_levels:
            z_score = stats.norm.ppf(sl)
            safety_stock = z_score * demand_std * np.sqrt(item_info['lead_time_days'])
            
            # Calculate associated costs
            holding_cost = safety_stock * item_info['unit_cost'] * 0.20  # 20% annual holding cost
            stockout_cost = (1 - sl) * avg_demand * 365 * item_info['unit_cost'] * 0.1  # 10% stockout penalty
            
            safety_stock_options.append({
                "service_level": sl,
                "safety_stock": round(max(0, safety_stock), 2),
                "annual_holding_cost": round(holding_cost, 2),
                "expected_stockout_cost": round(stockout_cost, 2),
                "total_cost": round(holding_cost + stockout_cost, 2)
            })
        
        # Find optimal safety stock for target service level
        target_z = stats.norm.ppf(target_service_level)
        optimal_safety_stock = target_z * demand_std * np.sqrt(item_info['lead_time_days'])
        
        # Current safety stock (estimated)
        current_safety_stock = max(0, item_info['reorder_point'] - (avg_demand * item_info['lead_time_days']))
        
        optimization = {
            "item_id": item_id,
            "item_name": item_info['item_name'],
            "target_service_level": target_service_level,
            "current_analysis": {
                "estimated_current_safety_stock": round(current_safety_stock, 2),
                "current_reorder_point": int(item_info['reorder_point']),
                "average_daily_demand": round(avg_demand, 2),
                "demand_standard_deviation": round(demand_std, 2),
                "lead_time_days": int(item_info['lead_time_days'])
            },
            "optimization_results": {
                "optimal_safety_stock": round(max(0, optimal_safety_stock), 2),
                "recommended_reorder_point": round(avg_demand * item_info['lead_time_days'] + optimal_safety_stock, 2),
                "safety_stock_change": round(optimal_safety_stock - current_safety_stock, 2)
            },
            "service_level_analysis": safety_stock_options,
            "recommendations": [],
            "cost_impact": {
                "current_holding_cost": round(current_safety_stock * item_info['unit_cost'] * 0.20, 2),
                "optimized_holding_cost": round(optimal_safety_stock * item_info['unit_cost'] * 0.20, 2),
                "annual_cost_change": round((optimal_safety_stock - current_safety_stock) * item_info['unit_cost'] * 0.20, 2)
            }
        }
        
        # Generate specific recommendations
        if optimal_safety_stock > current_safety_stock * 1.1:
            optimization["recommendations"].append(
                f"Increase safety stock by {round(optimal_safety_stock - current_safety_stock, 0)} units"
            )
            optimization["recommendations"].append(
                f"This will improve service level to {target_service_level*100}% but increase holding costs"
            )
        elif optimal_safety_stock < current_safety_stock * 0.9:
            optimization["recommendations"].append(
                f"Reduce safety stock by {round(current_safety_stock - optimal_safety_stock, 0)} units"
            )
            optimization["recommendations"].append(
                f"This will reduce holding costs while maintaining {target_service_level*100}% service level"
            )
        else:
            optimization["recommendations"].append(
                "Current safety stock levels are approximately optimal"
            )
        
        # Find the most cost-effective service level
        min_cost_option = min(safety_stock_options, key=lambda x: x["total_cost"])
        if min_cost_option["service_level"] != target_service_level:
            optimization["recommendations"].append(
                f"Consider {min_cost_option['service_level']*100}% service level for lowest total cost"
            )
        
        return optimization
        
    except Exception as e:
        logger.error(f"Error optimizing safety stock for {item_id}: {str(e)}")
        return {"error": f"Failed to optimize safety stock: {str(e)}"}


def generate_action_plan(priority: str = "high", category: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate comprehensive action plan for inventory optimization.
    
    Args:
        priority: Priority level ("high", "medium", "all")
        category: Optional category filter
        
    Returns:
        Dict containing prioritized action plan
    """
    try:
        inventory_data = analytics_backend.get_inventory_data(category=category)
        
        if inventory_data.empty:
            return {"error": f"No inventory data found for category: {category}" if category else "No inventory data found"}
        
        # Analyze all items and categorize actions needed
        action_items = []
        
        for _, item in inventory_data.iterrows():
            item_actions = []
            urgency_score = 0
            
            # Check for immediate stockout risk
            if item['current_stock'] == 0:
                item_actions.append({
                    "action": "EMERGENCY_REORDER",
                    "description": "Item is out of stock - immediate reorder required",
                    "urgency": "Critical",
                    "timeline": "Within 24 hours"
                })
                urgency_score += 10
            
            # Check for below reorder point
            elif item['current_stock'] < item['reorder_point']:
                item_actions.append({
                    "action": "REORDER_NEEDED",
                    "description": f"Stock below reorder point ({item['current_stock']} < {item['reorder_point']})",
                    "urgency": "High",
                    "timeline": "Within 3 days"
                })
                urgency_score += 7
            
            # Check for overstock
            elif item['current_stock'] > item['max_stock'] * 0.9:
                item_actions.append({
                    "action": "REDUCE_INVENTORY",
                    "description": f"Overstock situation - consider promotions or reduced ordering",
                    "urgency": "Medium",
                    "timeline": "Within 2 weeks"
                })
                urgency_score += 3
            
            # Check for long lead times
            if item['lead_time_days'] > 20:
                item_actions.append({
                    "action": "SUPPLIER_NEGOTIATION",
                    "description": f"Long lead time ({item['lead_time_days']} days) - negotiate with supplier",
                    "urgency": "Medium",
                    "timeline": "Within 1 month"
                })
                urgency_score += 2
            
            # Get sales data for demand analysis
            sales_data = analytics_backend.get_sales_data(item_id=item['item_id'])
            if not sales_data.empty:
                daily_demand = sales_data.groupby('date')['quantity_sold'].sum()
                if len(daily_demand) > 1:
                    cv = daily_demand.std() / daily_demand.mean()
                    if cv > 0.5:
                        item_actions.append({
                            "action": "REVIEW_FORECASTING",
                            "description": "High demand variability - review forecasting methods",
                            "urgency": "Medium",
                            "timeline": "Within 2 weeks"
                        })
                        urgency_score += 2
            
            if item_actions:
                action_items.append({
                    "item_id": item['item_id'],
                    "item_name": item['item_name'],
                    "category": item['category'],
                    "supplier_id": item['supplier_id'],
                    "urgency_score": urgency_score,
                    "actions": item_actions,
                    "overall_priority": "Critical" if urgency_score >= 10 else "High" if urgency_score >= 7 else "Medium" if urgency_score >= 3 else "Low"
                })
        
        # Filter by priority if specified
        if priority.lower() == "high":
            action_items = [item for item in action_items if item["overall_priority"] in ["Critical", "High"]]
        elif priority.lower() == "medium":
            action_items = [item for item in action_items if item["overall_priority"] == "Medium"]
        
        # Sort by urgency score
        action_items.sort(key=lambda x: x["urgency_score"], reverse=True)
        
        # Group actions by type for summary
        action_summary = {}
        for item in action_items:
            for action in item["actions"]:
                action_type = action["action"]
                if action_type not in action_summary:
                    action_summary[action_type] = 0
                action_summary[action_type] += 1
        
        # Generate implementation timeline
        immediate_actions = [item for item in action_items if item["overall_priority"] == "Critical"]
        short_term_actions = [item for item in action_items if item["overall_priority"] == "High"]
        medium_term_actions = [item for item in action_items if item["overall_priority"] == "Medium"]
        
        action_plan = {
            "plan_scope": f"Category: {category}" if category else "All categories",
            "priority_filter": priority,
            "total_items_requiring_action": len(action_items),
            "action_summary": action_summary,
            "implementation_timeline": {
                "immediate_24h": {
                    "count": len(immediate_actions),
                    "items": immediate_actions[:5]  # Top 5 most urgent
                },
                "short_term_1week": {
                    "count": len(short_term_actions),
                    "items": short_term_actions[:10]  # Top 10 high priority
                },
                "medium_term_1month": {
                    "count": len(medium_term_actions),
                    "items": medium_term_actions[:10]  # Top 10 medium priority
                }
            },
            "resource_requirements": {
                "procurement_team": len([item for item in action_items if any(a["action"] in ["EMERGENCY_REORDER", "REORDER_NEEDED"] for a in item["actions"])]),
                "supplier_management": len([item for item in action_items if any(a["action"] == "SUPPLIER_NEGOTIATION" for a in item["actions"])]),
                "demand_planning": len([item for item in action_items if any(a["action"] == "REVIEW_FORECASTING" for a in item["actions"])])
            },
            "success_metrics": [
                "Reduce out-of-stock items to zero within 1 week",
                "Achieve 95% service level across all categories",
                "Reduce average lead times by 20%",
                "Optimize inventory turnover ratio"
            ]
        }
        
        return action_plan
        
    except Exception as e:
        logger.error(f"Error generating action plan: {str(e)}")
        return {"error": f"Failed to generate action plan: {str(e)}"}


def optimize_inventory_investment(budget: float, category: Optional[str] = None) -> Dict[str, Any]:
    """
    Optimize inventory investment allocation within a given budget.
    
    Args:
        budget: Available budget for inventory investment
        category: Optional category to focus optimization on
        
    Returns:
        Dict containing investment optimization recommendations
    """
    try:
        inventory_data = analytics_backend.get_inventory_data(category=category)
        
        if inventory_data.empty:
            return {"error": f"No inventory data found for category: {category}" if category else "No inventory data found"}
        
        # Calculate investment priorities for each item
        investment_opportunities = []
        
        for _, item in inventory_data.iterrows():
            # Get sales data for ROI calculation
            sales_data = analytics_backend.get_sales_data(item_id=item['item_id'])
            
            if not sales_data.empty:
                annual_sales = sales_data['quantity_sold'].sum()
                annual_revenue = sales_data['total_revenue'].sum()
                
                # Calculate potential investment and return
                current_investment = item['current_stock'] * item['unit_cost']
                
                # Estimate optimal stock level (simplified)
                daily_demand = sales_data.groupby('date')['quantity_sold'].sum().mean()
                optimal_stock = daily_demand * (item['lead_time_days'] + 30)  # Lead time + 30 days safety
                optimal_investment = optimal_stock * item['unit_cost']
                
                investment_gap = max(0, optimal_investment - current_investment)
                
                # Calculate ROI potential
                if investment_gap > 0:
                    # Estimate additional revenue from better stock availability
                    stockout_risk = max(0, 1 - (item['current_stock'] / optimal_stock))
                    potential_additional_revenue = annual_revenue * stockout_risk * 0.5  # 50% of lost sales recoverable
                    roi = (potential_additional_revenue / investment_gap) if investment_gap > 0 else 0
                    
                    investment_opportunities.append({
                        "item_id": item['item_id'],
                        "item_name": item['item_name'],
                        "category": item['category'],
                        "current_investment": round(current_investment, 2),
                        "optimal_investment": round(optimal_investment, 2),
                        "investment_gap": round(investment_gap, 2),
                        "potential_roi": round(roi, 2),
                        "annual_revenue": round(annual_revenue, 2),
                        "priority_score": roi * investment_gap  # ROI weighted by investment size
                    })
        
        # Sort by priority score (ROI * investment size)
        investment_opportunities.sort(key=lambda x: x["priority_score"], reverse=True)
        
        # Allocate budget optimally
        allocated_investments = []
        remaining_budget = budget
        total_expected_roi = 0
        
        for opportunity in investment_opportunities:
            if remaining_budget >= opportunity["investment_gap"]:
                allocated_investments.append({
                    **opportunity,
                    "allocated_amount": opportunity["investment_gap"],
                    "expected_return": opportunity["investment_gap"] * opportunity["potential_roi"]
                })
                remaining_budget -= opportunity["investment_gap"]
                total_expected_roi += opportunity["investment_gap"] * opportunity["potential_roi"]
            elif remaining_budget > 0:
                # Partial allocation
                partial_roi = opportunity["potential_roi"] * (remaining_budget / opportunity["investment_gap"])
                allocated_investments.append({
                    **opportunity,
                    "allocated_amount": remaining_budget,
                    "expected_return": remaining_budget * partial_roi
                })
                remaining_budget = 0
                total_expected_roi += remaining_budget * partial_roi
                break
        
        # Calculate portfolio metrics
        total_allocated = budget - remaining_budget
        portfolio_roi = (total_expected_roi / total_allocated) if total_allocated > 0 else 0
        
        optimization_result = {
            "optimization_scope": f"Category: {category}" if category else "All categories",
            "budget_analysis": {
                "total_budget": budget,
                "total_allocated": round(total_allocated, 2),
                "remaining_budget": round(remaining_budget, 2),
                "allocation_efficiency": round((total_allocated / budget) * 100, 1)
            },
            "portfolio_metrics": {
                "expected_total_return": round(total_expected_roi, 2),
                "portfolio_roi": round(portfolio_roi, 2),
                "number_of_investments": len(allocated_investments),
                "average_investment_size": round(total_allocated / len(allocated_investments), 2) if allocated_investments else 0
            },
            "recommended_investments": allocated_investments[:20],  # Top 20 recommendations
            "investment_categories": {},
            "implementation_strategy": [
                "Prioritize high-ROI, low-investment items first",
                "Monitor performance of allocated investments",
                "Reassess allocation quarterly based on performance",
                "Consider supplier negotiations for bulk purchases"
            ]
        }
        
        # Categorize investments
        if category is None:
            category_allocation = {}
            for inv in allocated_investments:
                cat = inv["category"]
                if cat not in category_allocation:
                    category_allocation[cat] = {"count": 0, "amount": 0}
                category_allocation[cat]["count"] += 1
                category_allocation[cat]["amount"] += inv["allocated_amount"]
            
            optimization_result["investment_categories"] = category_allocation
        
        return optimization_result
        
    except Exception as e:
        logger.error(f"Error optimizing inventory investment: {str(e)}")
        return {"error": f"Failed to optimize inventory investment: {str(e)}"}


# Create the Prescriptive Analytics Agent
root_agent = Agent(
    name="prescriptive_analytics_agent",
    model="gemini-2.0-flash",
    description="Prescriptive Analytics Specialist - Provides actionable recommendations, optimization strategies, and specific solutions for inventory management",
    instruction="""You are a Prescriptive Analytics Specialist focused on Tier 4 inventory analytics. 
    Your expertise is in providing ACTIONABLE RECOMMENDATIONS and optimization strategies. You excel at 
    translating analysis into specific, implementable actions that solve inventory problems and optimize 
    performance. You provide detailed action plans, cost-benefit analysis, and step-by-step implementation 
    guidance. Always include specific timelines, resource requirements, and success metrics in your recommendations.""",
    tools=[
        recommend_reorder_strategy,
        optimize_safety_stock,
        generate_action_plan,
        optimize_inventory_investment,
    ]
)
