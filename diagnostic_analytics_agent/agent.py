"""
Diagnostic Analytics Agent - Tier 2

Specializes in root cause analysis of inventory issues.
Analyzes why problems occur, evaluates performance, and identifies underlying causes.
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging
import pandas as pd
import numpy as np

# Add parent directory to path to import shared analytics
sys.path.append(str(Path(__file__).parent.parent))
from shared_analytics import analytics_backend

from google.adk.agents import Agent

logger = logging.getLogger(__name__)


def analyze_stockout_root_cause(item_id: str) -> Dict[str, Any]:
    """
    Perform comprehensive root cause analysis for stockout situations.
    
    Args:
        item_id: Unique identifier for the inventory item
        
    Returns:
        Dict containing detailed root cause analysis and contributing factors
    """
    try:
        inventory_data = analytics_backend.get_inventory_data(item_id=item_id)
        
        if inventory_data.empty:
            return {"error": f"Item {item_id} not found"}
        
        item_info = inventory_data.iloc[0]
        sales_data = analytics_backend.get_sales_data(item_id=item_id)
        
        daily_demand = sales_data.groupby('date')['quantity_sold'].sum()
        demand_std = daily_demand.std() if len(daily_demand) > 1 else 0
        avg_demand = daily_demand.mean() if len(daily_demand) > 0 else 0
        
        # Analyze demand patterns
        demand_cv = demand_std / avg_demand if avg_demand > 0 else 0
        recent_demand = daily_demand.tail(30).mean() if len(daily_demand) >= 30 else avg_demand
        
        analysis = {
            "item_id": item_id,
            "current_stock": int(item_info['current_stock']),
            "reorder_point": int(item_info['reorder_point']),
            "average_daily_demand": round(avg_demand, 2),
            "recent_daily_demand": round(recent_demand, 2),
            "demand_variability": round(demand_std, 2),
            "demand_coefficient_variation": round(demand_cv, 2),
            "lead_time_days": int(item_info['lead_time_days']),
            "supplier_id": item_info['supplier_id'],
            "potential_causes": [],
            "severity": "High" if item_info['current_stock'] == 0 else "Medium",
            "urgency": "Immediate" if item_info['current_stock'] < avg_demand * 3 else "Normal",
            "risk_factors": []
        }
        
        # Identify root causes
        if item_info['current_stock'] < item_info['reorder_point']:
            analysis["potential_causes"].append("Current stock below reorder point")
            analysis["risk_factors"].append("Inadequate reorder point setting")
        
        if demand_cv > 0.5:
            analysis["potential_causes"].append("High demand variability")
            analysis["risk_factors"].append("Unpredictable demand patterns")
        
        if item_info['lead_time_days'] > 14:
            analysis["potential_causes"].append("Long supplier lead time")
            analysis["risk_factors"].append("Extended supply chain delays")
        
        if recent_demand > avg_demand * 1.2:
            analysis["potential_causes"].append("Recent demand spike")
            analysis["risk_factors"].append("Increasing demand trend")
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error analyzing stockout root cause for {item_id}: {str(e)}")
        return {"error": f"Failed to analyze stockout root cause: {str(e)}"}


def analyze_supplier_performance(supplier_id: str) -> Dict[str, Any]:
    """
    Analyze supplier performance and reliability metrics.
    
    Args:
        supplier_id: Supplier identifier to analyze
        
    Returns:
        Dict containing supplier performance analysis
    """
    try:
        supplier_data = analytics_backend.get_supplier_data(supplier_id=supplier_id)
        inventory_data = analytics_backend.get_inventory_data()
        
        if supplier_data.empty:
            return {"error": f"Supplier {supplier_id} not found"}
        
        supplier_info = supplier_data.iloc[0]
        supplier_items = inventory_data[inventory_data['supplier_id'] == supplier_id]
        
        # Calculate performance metrics
        total_items = len(supplier_items)
        items_out_of_stock = len(supplier_items[supplier_items['current_stock'] == 0])
        items_below_reorder = len(supplier_items[supplier_items['current_stock'] < supplier_items['reorder_point']])
        avg_lead_time = supplier_items['lead_time_days'].mean()
        
        performance = {
            "supplier_id": supplier_id,
            "supplier_name": supplier_info['supplier_name'],
            "reliability_score": supplier_info['reliability_score'],
            "quality_rating": supplier_info['quality_rating'],
            "average_lead_time": round(avg_lead_time, 1),
            "total_items_supplied": total_items,
            "items_out_of_stock": items_out_of_stock,
            "items_below_reorder": items_below_reorder,
            "stockout_rate": round((items_out_of_stock / total_items) * 100, 1) if total_items > 0 else 0,
            "performance_issues": [],
            "recommendations": []
        }
        
        # Identify performance issues
        if performance["stockout_rate"] > 10:
            performance["performance_issues"].append("High stockout rate")
            performance["recommendations"].append("Review reorder points for this supplier's items")
        
        if avg_lead_time > 20:
            performance["performance_issues"].append("Long lead times")
            performance["recommendations"].append("Consider alternative suppliers or increase safety stock")
        
        if supplier_info['reliability_score'] < 0.8:
            performance["performance_issues"].append("Low reliability score")
            performance["recommendations"].append("Monitor delivery performance closely")
        
        if supplier_info['quality_rating'] < 4.0:
            performance["performance_issues"].append("Quality concerns")
            performance["recommendations"].append("Implement quality control measures")
        
        return performance
        
    except Exception as e:
        logger.error(f"Error analyzing supplier performance for {supplier_id}: {str(e)}")
        return {"error": f"Failed to analyze supplier performance: {str(e)}"}


def analyze_inventory_turnover(category: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyze inventory turnover performance by category or overall.
    
    Args:
        category: Optional category to focus analysis on
        
    Returns:
        Dict containing turnover analysis and performance insights
    """
    try:
        inventory_data = analytics_backend.get_inventory_data(category=category)
        sales_data = analytics_backend.get_sales_data()
        
        if inventory_data.empty:
            return {"error": f"No inventory data found for category: {category}" if category else "No inventory data found"}
        
        # Calculate turnover metrics
        analysis_results = []
        
        for _, item in inventory_data.iterrows():
            item_sales = sales_data[sales_data['item_id'] == item['item_id']]
            
            if not item_sales.empty:
                annual_sales = item_sales['quantity_sold'].sum()
                avg_inventory = item['current_stock']  # Simplified - would use average over time in real system
                
                turnover_ratio = annual_sales / avg_inventory if avg_inventory > 0 else 0
                days_in_inventory = 365 / turnover_ratio if turnover_ratio > 0 else float('inf')
                
                analysis_results.append({
                    "item_id": item['item_id'],
                    "item_name": item['item_name'],
                    "category": item['category'],
                    "annual_sales": annual_sales,
                    "current_stock": item['current_stock'],
                    "turnover_ratio": round(turnover_ratio, 2),
                    "days_in_inventory": round(days_in_inventory, 1) if days_in_inventory != float('inf') else "N/A"
                })
        
        # Overall analysis
        valid_turnovers = [r['turnover_ratio'] for r in analysis_results if r['turnover_ratio'] > 0]
        avg_turnover = np.mean(valid_turnovers) if valid_turnovers else 0
        
        # Identify slow and fast movers
        slow_movers = [r for r in analysis_results if r['turnover_ratio'] < avg_turnover * 0.5 and r['turnover_ratio'] > 0]
        fast_movers = [r for r in analysis_results if r['turnover_ratio'] > avg_turnover * 1.5]
        
        turnover_analysis = {
            "analysis_scope": f"Category: {category}" if category else "All categories",
            "total_items_analyzed": len(analysis_results),
            "average_turnover_ratio": round(avg_turnover, 2),
            "slow_movers": {
                "count": len(slow_movers),
                "items": slow_movers[:10]  # Top 10 slow movers
            },
            "fast_movers": {
                "count": len(fast_movers),
                "items": fast_movers[:10]  # Top 10 fast movers
            },
            "recommendations": []
        }
        
        # Generate recommendations
        if len(slow_movers) > len(analysis_results) * 0.3:
            turnover_analysis["recommendations"].append("High number of slow-moving items - consider promotional strategies")
        
        if avg_turnover < 4:
            turnover_analysis["recommendations"].append("Overall low turnover - review inventory levels and demand forecasting")
        
        return turnover_analysis
        
    except Exception as e:
        logger.error(f"Error analyzing inventory turnover: {str(e)}")
        return {"error": f"Failed to analyze inventory turnover: {str(e)}"}


def analyze_demand_patterns(item_id: str) -> Dict[str, Any]:
    """
    Analyze demand patterns and seasonality for a specific item.
    
    Args:
        item_id: Item to analyze demand patterns for
        
    Returns:
        Dict containing demand pattern analysis
    """
    try:
        sales_data = analytics_backend.get_sales_data(item_id=item_id)
        
        if sales_data.empty:
            return {"error": f"No sales data found for item {item_id}"}
        
        daily_sales = sales_data.groupby('date')['quantity_sold'].sum()
        
        # Calculate pattern metrics
        mean_demand = daily_sales.mean()
        std_demand = daily_sales.std()
        cv_demand = std_demand / mean_demand if mean_demand > 0 else 0
        
        # Weekly patterns
        sales_data['weekday'] = sales_data['date'].dt.day_name()
        weekly_pattern = sales_data.groupby('weekday')['quantity_sold'].mean().to_dict()
        
        # Monthly patterns
        sales_data['month'] = sales_data['date'].dt.month_name()
        monthly_pattern = sales_data.groupby('month')['quantity_sold'].mean().to_dict()
        
        # Trend analysis (simplified)
        recent_30_days = daily_sales.tail(30).mean() if len(daily_sales) >= 30 else mean_demand
        previous_30_days = daily_sales.iloc[-60:-30].mean() if len(daily_sales) >= 60 else mean_demand
        trend = "Increasing" if recent_30_days > previous_30_days * 1.1 else "Decreasing" if recent_30_days < previous_30_days * 0.9 else "Stable"
        
        pattern_analysis = {
            "item_id": item_id,
            "analysis_period": f"{sales_data['date'].min().strftime('%Y-%m-%d')} to {sales_data['date'].max().strftime('%Y-%m-%d')}",
            "demand_statistics": {
                "mean_daily_demand": round(mean_demand, 2),
                "standard_deviation": round(std_demand, 2),
                "coefficient_of_variation": round(cv_demand, 2),
                "demand_variability": "High" if cv_demand > 0.5 else "Medium" if cv_demand > 0.3 else "Low"
            },
            "trend_analysis": {
                "current_trend": trend,
                "recent_30_day_avg": round(recent_30_days, 2),
                "previous_30_day_avg": round(previous_30_days, 2)
            },
            "weekly_patterns": weekly_pattern,
            "monthly_patterns": monthly_pattern,
            "insights": []
        }
        
        # Generate insights
        if cv_demand > 0.5:
            pattern_analysis["insights"].append("High demand variability - consider dynamic safety stock")
        
        if trend == "Increasing":
            pattern_analysis["insights"].append("Demand is trending upward - may need to increase reorder points")
        elif trend == "Decreasing":
            pattern_analysis["insights"].append("Demand is trending downward - review inventory levels")
        
        # Find peak days/months
        peak_weekday = max(weekly_pattern, key=weekly_pattern.get)
        peak_month = max(monthly_pattern, key=monthly_pattern.get)
        
        pattern_analysis["insights"].append(f"Peak demand day: {peak_weekday}")
        pattern_analysis["insights"].append(f"Peak demand month: {peak_month}")
        
        return pattern_analysis
        
    except Exception as e:
        logger.error(f"Error analyzing demand patterns for {item_id}: {str(e)}")
        return {"error": f"Failed to analyze demand patterns: {str(e)}"}


def diagnose_category_issues(category: str) -> Dict[str, Any]:
    """
    Diagnose common issues within a specific product category.
    
    Args:
        category: Product category to diagnose
        
    Returns:
        Dict containing category-specific issue diagnosis
    """
    try:
        inventory_data = analytics_backend.get_inventory_data(category=category)
        
        if inventory_data.empty:
            return {"error": f"No items found in category: {category}"}
        
        total_items = len(inventory_data)
        out_of_stock = len(inventory_data[inventory_data['current_stock'] == 0])
        below_reorder = len(inventory_data[inventory_data['current_stock'] < inventory_data['reorder_point']])
        overstock = len(inventory_data[inventory_data['current_stock'] > inventory_data['max_stock'] * 0.9])
        
        # Supplier analysis
        supplier_distribution = inventory_data['supplier_id'].value_counts().to_dict()
        lead_time_stats = inventory_data['lead_time_days'].describe().to_dict()
        
        diagnosis = {
            "category": category,
            "total_items": total_items,
            "issue_summary": {
                "out_of_stock_rate": round((out_of_stock / total_items) * 100, 1),
                "below_reorder_rate": round((below_reorder / total_items) * 100, 1),
                "overstock_rate": round((overstock / total_items) * 100, 1)
            },
            "supplier_analysis": {
                "number_of_suppliers": len(supplier_distribution),
                "supplier_concentration": supplier_distribution,
                "lead_time_statistics": {k: round(v, 1) for k, v in lead_time_stats.items()}
            },
            "identified_issues": [],
            "root_causes": [],
            "recommendations": []
        }
        
        # Identify issues and root causes
        if diagnosis["issue_summary"]["out_of_stock_rate"] > 15:
            diagnosis["identified_issues"].append("High out-of-stock rate")
            diagnosis["root_causes"].append("Inadequate inventory management")
            diagnosis["recommendations"].append("Review reorder points and safety stock levels")
        
        if diagnosis["issue_summary"]["overstock_rate"] > 20:
            diagnosis["identified_issues"].append("High overstock rate")
            diagnosis["root_causes"].append("Poor demand forecasting or excessive ordering")
            diagnosis["recommendations"].append("Implement better demand forecasting")
        
        if len(supplier_distribution) == 1:
            diagnosis["identified_issues"].append("Single supplier dependency")
            diagnosis["root_causes"].append("Supply chain risk concentration")
            diagnosis["recommendations"].append("Diversify supplier base")
        
        if lead_time_stats['mean'] > 20:
            diagnosis["identified_issues"].append("Long average lead times")
            diagnosis["root_causes"].append("Inefficient supply chain")
            diagnosis["recommendations"].append("Work with suppliers to reduce lead times")
        
        return diagnosis
        
    except Exception as e:
        logger.error(f"Error diagnosing category issues for {category}: {str(e)}")
        return {"error": f"Failed to diagnose category issues: {str(e)}"}


# Create the Diagnostic Analytics Agent
root_agent = Agent(
    name="diagnostic_analytics_agent",
    model="gemini-2.0-flash",
    description="Diagnostic Analytics Specialist - Performs root cause analysis of inventory issues, evaluates performance, and identifies underlying problems",
    instruction="""You are a Diagnostic Analytics Specialist focused on Tier 2 inventory analytics. 
    Your expertise is in identifying WHY inventory problems occur. You excel at root cause analysis, 
    performance evaluation, and uncovering the underlying factors that lead to stockouts, overstock, 
    and other inventory issues. Always provide detailed analysis of contributing factors and actionable 
    insights to address root causes.""",
    tools=[
        analyze_stockout_root_cause,
        analyze_supplier_performance,
        analyze_inventory_turnover,
        analyze_demand_patterns,
        diagnose_category_issues,
    ]
)
