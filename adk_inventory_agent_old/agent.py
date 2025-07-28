"""
ADK Inventory Management Agent

A comprehensive inventory management agent built with Google's Agent Development Kit (ADK).
This agent provides 4-tier analytics capabilities: Descriptive, Diagnostic, Predictive, and Prescriptive.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any
import json
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from google.adk.agents import Agent
from .analytics.backend import MockAnalyticsBackend

# Configure logging
log_level = os.getenv('AGENT_LOG_LEVEL', 'INFO')
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)


class ADKInventoryAgent:
    """
    Advanced Inventory Management Agent built with Google ADK.
    
    This agent provides comprehensive inventory analytics capabilities across four tiers:
    - Descriptive: Current and historical inventory state reporting
    - Diagnostic: Root cause analysis of inventory issues
    - Predictive: Demand forecasting and trend analysis
    - Prescriptive: Actionable recommendations for optimization
    """
    
    def __init__(self):
        """Initialize the ADK Inventory Agent with analytics backend."""
        self.analytics = MockAnalyticsBackend()
        self.agent_name = "ADKInventoryAgent"
        self.description = "Expert inventory management agent providing comprehensive analytics and optimization recommendations"
        
        # Get configuration from environment
        model = os.getenv('AGENT_MODEL', 'gemini-2.0-flash-exp')
        
        logger.info(f"Initializing {self.agent_name} with model: {model}")
    
    def _get_data(self, query_type: str, **kwargs) -> pd.DataFrame:
        """
        Placeholder method to simulate data fetching from various sources.
        In production, this would connect to actual databases, APIs, or data warehouses.
        
        Args:
            query_type: Type of data to fetch ('inventory', 'sales', 'suppliers', etc.)
            **kwargs: Additional parameters for the query
            
        Returns:
            pd.DataFrame: Sample data for demonstration
        """
        try:
            if query_type == "inventory":
                return self.analytics.inventory_data.copy()
            elif query_type == "sales":
                item_id = kwargs.get('item_id')
                start_date = kwargs.get('start_date', '2024-01-01')
                end_date = kwargs.get('end_date', '2024-12-31')
                return self.analytics.get_sales_data(item_id, start_date, end_date)
            elif query_type == "suppliers":
                return self.analytics.supplier_data.copy()
            else:
                return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error fetching {query_type} data: {str(e)}")
            return pd.DataFrame()
    
    # DESCRIPTIVE TOOLS - Tier 1 Analytics
    
    def generate_inventory_summary(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Generate comprehensive inventory summary report for the specified date range.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Dict containing inventory summary statistics and insights
        """
        try:
            inventory_data = self._get_data("inventory")
            
            if inventory_data.empty:
                return {"error": "No inventory data available for the specified period"}
            
            # Calculate summary statistics
            total_items = len(inventory_data)
            total_stock_value = (inventory_data['current_stock'] * inventory_data['unit_cost']).sum()
            items_below_reorder = len(inventory_data[inventory_data['current_stock'] < inventory_data['reorder_point']])
            out_of_stock_items = len(inventory_data[inventory_data['current_stock'] == 0])
            
            # Category breakdown
            category_summary = inventory_data.groupby('category').agg({
                'current_stock': 'sum',
                'unit_cost': 'mean',
                'item_id': 'count'
            }).round(2)
            
            summary = {
                "report_period": f"{start_date} to {end_date}",
                "total_items": total_items,
                "total_stock_value": round(total_stock_value, 2),
                "items_below_reorder_point": items_below_reorder,
                "out_of_stock_items": out_of_stock_items,
                "stock_turnover_alerts": items_below_reorder + out_of_stock_items,
                "category_breakdown": category_summary.to_dict('index'),
                "key_insights": [
                    f"{items_below_reorder} items need immediate attention (below reorder point)",
                    f"{out_of_stock_items} items are completely out of stock",
                    f"Total inventory value: ${total_stock_value:,.2f}",
                    f"Average stock value per item: ${total_stock_value/total_items:,.2f}"
                ]
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating inventory summary: {str(e)}")
            return {"error": f"Failed to generate inventory summary: {str(e)}"}
    
    def get_item_details(self, item_id: str) -> Dict[str, Any]:
        """
        Retrieve detailed information for a specific inventory item.
        
        Args:
            item_id: Unique identifier for the inventory item
            
        Returns:
            Dict containing detailed item information and current status
        """
        try:
            inventory_data = self._get_data("inventory")
            item_data = inventory_data[inventory_data['item_id'] == item_id]
            
            if item_data.empty:
                return {"error": f"Item {item_id} not found in inventory"}
            
            item_info = item_data.iloc[0].to_dict()
            
            # Get recent sales data
            sales_data = self._get_data("sales", item_id=item_id, 
                                      start_date="2024-11-01", end_date="2024-12-31")
            
            recent_sales_qty = sales_data['quantity_sold'].sum() if not sales_data.empty else 0
            avg_daily_demand = sales_data.groupby('date')['quantity_sold'].sum().mean() if not sales_data.empty else 0
            
            # Calculate status indicators
            status = "Normal"
            if item_info['current_stock'] == 0:
                status = "Out of Stock"
            elif item_info['current_stock'] < item_info['reorder_point']:
                status = "Below Reorder Point"
            elif item_info['current_stock'] > item_info['max_stock'] * 0.9:
                status = "Overstock Risk"
            
            item_details = {
                **item_info,
                "status": status,
                "recent_sales_quantity": recent_sales_qty,
                "average_daily_demand": round(avg_daily_demand, 2),
                "days_of_stock_remaining": round(item_info['current_stock'] / max(avg_daily_demand, 1), 1),
                "stock_value": round(item_info['current_stock'] * item_info['unit_cost'], 2),
                "reorder_needed": item_info['current_stock'] < item_info['reorder_point']
            }
            
            return item_details
            
        except Exception as e:
            logger.error(f"Error retrieving item details for {item_id}: {str(e)}")
            return {"error": f"Failed to retrieve item details: {str(e)}"}
    
    # DIAGNOSTIC TOOLS - Tier 2 Analytics
    
    def analyze_stockout_root_cause(self, item_id: str) -> Dict[str, Any]:
        """
        Perform root cause analysis for stockout situations.
        
        Args:
            item_id: Unique identifier for the inventory item
            
        Returns:
            Dict containing root cause analysis and contributing factors
        """
        try:
            analysis = self.analytics.analyze_stockout_causes(item_id)
            
            if "error" in analysis:
                return analysis
            
            # Enhanced analysis with recommendations
            analysis["severity"] = "High" if analysis["current_stock"] == 0 else "Medium"
            analysis["urgency"] = "Immediate" if analysis["current_stock"] < analysis["average_daily_demand"] * 3 else "Normal"
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing stockout root cause for {item_id}: {str(e)}")
            return {"error": f"Failed to analyze stockout root cause: {str(e)}"}
    
    # PREDICTIVE TOOLS - Tier 3 Analytics
    
    def forecast_demand(self, item_id: str, forecast_periods: int = 30) -> Dict[str, Any]:
        """
        Generate demand forecast for a specific item.
        
        Args:
            item_id: Unique identifier for the inventory item
            forecast_periods: Number of days to forecast
            
        Returns:
            Dict containing demand forecast and confidence intervals
        """
        try:
            forecast = self.analytics.forecast_demand(item_id, forecast_periods)
            
            if "error" in forecast:
                return forecast
            
            # Add summary statistics
            forecasts = forecast["forecasts"]
            total_forecasted_demand = sum([f["forecasted_demand"] for f in forecasts])
            avg_daily_forecast = total_forecasted_demand / len(forecasts)
            
            forecast["summary"] = {
                "total_forecasted_demand": round(total_forecasted_demand, 2),
                "average_daily_forecast": round(avg_daily_forecast, 2),
                "peak_demand_day": max(forecasts, key=lambda x: x["forecasted_demand"])["date"],
                "lowest_demand_day": min(forecasts, key=lambda x: x["forecasted_demand"])["date"]
            }
            
            return forecast
            
        except Exception as e:
            logger.error(f"Error forecasting demand for {item_id}: {str(e)}")
            return {"error": f"Failed to forecast demand: {str(e)}"}
    
    # PRESCRIPTIVE TOOLS - Tier 4 Analytics
    
    def recommend_reorder_strategy(self, item_id: str, service_level: float = 0.95) -> Dict[str, Any]:
        """
        Generate optimal reorder strategy recommendations.
        
        Args:
            item_id: Unique identifier for the inventory item
            service_level: Desired service level (0.0 to 1.0)
            
        Returns:
            Dict containing reorder strategy recommendations
        """
        try:
            if not 0.0 <= service_level <= 1.0:
                return {"error": "Service level must be between 0.0 and 1.0"}
            
            recommendations = self.analytics.recommend_reorder_strategy(item_id, service_level)
            
            if "error" in recommendations:
                return recommendations
            
            # Add priority level
            if recommendations["current_reorder_point"] < recommendations["recommended_reorder_point"]:
                recommendations["priority"] = "High - Reorder point adjustment needed"
            else:
                recommendations["priority"] = "Normal - Current settings adequate"
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating reorder strategy for {item_id}: {str(e)}")
            return {"error": f"Failed to generate reorder strategy: {str(e)}"}


# Create the main agent instance
def create_inventory_agent():
    """Create and return the inventory agent instance using proper ADK methods."""
    agent_instance = ADKInventoryAgent()

    try:
        # Try to load from JSON config if available
        config_path = os.path.join(os.path.dirname(__file__), '..', 'agent_config.json')
        if os.path.exists(config_path):
            logger.info(f"Loading agent configuration from {config_path}")
            # Use supported ADK method for loading configuration
            from google.adk.agents import Agent
            inventory_agent = Agent.load_from_json(config_path)

            # Bind the tools to the agent instance methods
            inventory_agent.tools = [
                agent_instance.generate_inventory_summary,
                agent_instance.get_item_details,
                agent_instance.analyze_stockout_root_cause,
                agent_instance.forecast_demand,
                agent_instance.recommend_reorder_strategy,
            ]
        else:
            # Fallback to programmatic creation
            logger.info("Creating agent programmatically")
            inventory_agent = Agent(
                name=agent_instance.agent_name,
                model=os.getenv('AGENT_MODEL', 'gemini-2.0-flash-exp'),
                description=agent_instance.description,
                instruction="""You are an expert supply chain analyst and inventory management specialist.
                Your goal is to provide deep, actionable insights into inventory management, demand forecasting,
                and logistics optimization. You excel at analyzing complex inventory data, identifying root causes
                of stockouts and overstock situations, and providing data-driven recommendations that improve
                service levels while minimizing costs. Always provide specific, actionable recommendations
                backed by quantitative analysis.""",
                tools=[
                    # Descriptive Tools
                    agent_instance.generate_inventory_summary,
                    agent_instance.get_item_details,

                    # Diagnostic Tools
                    agent_instance.analyze_stockout_root_cause,

                    # Predictive Tools
                    agent_instance.forecast_demand,

                    # Prescriptive Tools
                    agent_instance.recommend_reorder_strategy,
                ]
            )

    except Exception as e:
        logger.warning(f"Error loading from JSON config: {e}. Using programmatic creation.")
        # Fallback to programmatic creation
        inventory_agent = Agent(
            name=agent_instance.agent_name,
            model=os.getenv('AGENT_MODEL', 'gemini-2.0-flash-exp'),
            description=agent_instance.description,
            instruction="""You are an expert supply chain analyst and inventory management specialist.
            Your goal is to provide deep, actionable insights into inventory management, demand forecasting,
            and logistics optimization. You excel at analyzing complex inventory data, identifying root causes
            of stockouts and overstock situations, and providing data-driven recommendations that improve
            service levels while minimizing costs. Always provide specific, actionable recommendations
            backed by quantitative analysis.""",
            tools=[
                # Descriptive Tools
                agent_instance.generate_inventory_summary,
                agent_instance.get_item_details,

                # Diagnostic Tools
                agent_instance.analyze_stockout_root_cause,

                # Predictive Tools
                agent_instance.forecast_demand,

                # Prescriptive Tools
                agent_instance.recommend_reorder_strategy,
            ]
        )

    return inventory_agent

# Create the agent instance for export
inventory_agent = create_inventory_agent()
