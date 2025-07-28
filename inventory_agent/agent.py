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

from google.adk.agents import Agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MockAnalyticsBackend:
    """Mock analytics backend to simulate a real analytics framework."""
    
    def __init__(self):
        """Initialize the mock analytics backend with sample data."""
        self.inventory_data = self._generate_sample_inventory_data()
        self.sales_data = self._generate_sample_sales_data()
        self.supplier_data = self._generate_sample_supplier_data()
    
    def _generate_sample_inventory_data(self) -> pd.DataFrame:
        """Generate sample inventory data for demonstration."""
        np.random.seed(42)
        items = [f"ITEM_{i:03d}" for i in range(1, 101)]
        categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books"]
        
        data = []
        for item in items:
            data.append({
                'item_id': item,
                'item_name': f"Product {item.split('_')[1]}",
                'category': np.random.choice(categories),
                'current_stock': np.random.randint(0, 500),
                'reorder_point': np.random.randint(20, 100),
                'max_stock': np.random.randint(200, 1000),
                'unit_cost': round(np.random.uniform(5.0, 200.0), 2),
                'supplier_id': f"SUP_{np.random.randint(1, 21):03d}",
                'lead_time_days': np.random.randint(1, 30),
                'last_updated': datetime.now() - timedelta(days=np.random.randint(0, 7))
            })
        
        return pd.DataFrame(data)
    
    def _generate_sample_sales_data(self) -> pd.DataFrame:
        """Generate sample sales data for demonstration."""
        np.random.seed(42)
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        items = [f"ITEM_{i:03d}" for i in range(1, 101)]
        
        data = []
        for date in dates:
            active_items = np.random.choice(items, size=np.random.randint(10, 50), replace=False)
            for item in active_items:
                quantity = np.random.randint(1, 20)
                unit_price = round(np.random.uniform(10.0, 300.0), 2)
                data.append({
                    'date': date,
                    'item_id': item,
                    'quantity_sold': quantity,
                    'unit_price': unit_price,
                    'total_revenue': quantity * unit_price
                })
        
        return pd.DataFrame(data)
    
    def _generate_sample_supplier_data(self) -> pd.DataFrame:
        """Generate sample supplier data for demonstration."""
        suppliers = []
        for i in range(1, 21):
            suppliers.append({
                'supplier_id': f"SUP_{i:03d}",
                'supplier_name': f"Supplier Company {i}",
                'reliability_score': round(np.random.uniform(0.7, 1.0), 2),
                'average_lead_time': np.random.randint(5, 25),
                'quality_rating': round(np.random.uniform(3.0, 5.0), 1)
            })
        
        return pd.DataFrame(suppliers)
    
    def get_sales_data(self, item_id: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Get sales data for a specific item within date range."""
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        
        filtered_data = self.sales_data[
            (self.sales_data['item_id'] == item_id) &
            (self.sales_data['date'] >= start) &
            (self.sales_data['date'] <= end)
        ].copy()
        
        return filtered_data


# Initialize the analytics backend
analytics = MockAnalyticsBackend()


def generate_inventory_summary(start_date: str, end_date: str) -> Dict[str, Any]:
    """
    Generate comprehensive inventory summary report for the specified date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        Dict containing inventory summary statistics and insights
    """
    try:
        inventory_data = analytics.inventory_data.copy()
        
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


def get_item_details(item_id: str) -> Dict[str, Any]:
    """
    Retrieve detailed information for a specific inventory item.
    
    Args:
        item_id: Unique identifier for the inventory item
        
    Returns:
        Dict containing detailed item information and current status
    """
    try:
        inventory_data = analytics.inventory_data.copy()
        item_data = inventory_data[inventory_data['item_id'] == item_id]
        
        if item_data.empty:
            return {"error": f"Item {item_id} not found in inventory"}
        
        item_info = item_data.iloc[0].to_dict()
        
        # Get recent sales data
        sales_data = analytics.get_sales_data(item_id, "2024-11-01", "2024-12-31")
        
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


def analyze_stockout_root_cause(item_id: str) -> Dict[str, Any]:
    """
    Perform root cause analysis for stockout situations.
    
    Args:
        item_id: Unique identifier for the inventory item
        
    Returns:
        Dict containing root cause analysis and contributing factors
    """
    try:
        inventory_data = analytics.inventory_data.copy()
        item_data = inventory_data[inventory_data['item_id'] == item_id]
        
        if item_data.empty:
            return {"error": f"Item {item_id} not found"}
        
        item_info = item_data.iloc[0]
        sales_data = analytics.sales_data[analytics.sales_data['item_id'] == item_id]
        
        daily_demand = sales_data.groupby('date')['quantity_sold'].sum()
        demand_std = daily_demand.std() if len(daily_demand) > 1 else 0
        avg_demand = daily_demand.mean() if len(daily_demand) > 0 else 0
        
        analysis = {
            "current_stock": int(item_info['current_stock']),
            "reorder_point": int(item_info['reorder_point']),
            "average_daily_demand": round(avg_demand, 2),
            "demand_variability": round(demand_std, 2),
            "lead_time_days": int(item_info['lead_time_days']),
            "potential_causes": [],
            "severity": "High" if item_info['current_stock'] == 0 else "Medium",
            "urgency": "Immediate" if item_info['current_stock'] < avg_demand * 3 else "Normal"
        }
        
        if item_info['current_stock'] < item_info['reorder_point']:
            analysis["potential_causes"].append("Current stock below reorder point")
        
        if demand_std > avg_demand * 0.5:
            analysis["potential_causes"].append("High demand variability")
        
        if item_info['lead_time_days'] > 14:
            analysis["potential_causes"].append("Long supplier lead time")
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error analyzing stockout root cause for {item_id}: {str(e)}")
        return {"error": f"Failed to analyze stockout root cause: {str(e)}"}


def forecast_demand(item_id: str, forecast_periods: int = 30) -> Dict[str, Any]:
    """
    Generate demand forecast for a specific item.
    
    Args:
        item_id: Unique identifier for the inventory item
        forecast_periods: Number of days to forecast
        
    Returns:
        Dict containing demand forecast and confidence intervals
    """
    try:
        sales_data = analytics.get_sales_data(item_id, "2024-01-01", "2024-12-31")
        
        if sales_data.empty:
            return {"error": f"No sales data found for item {item_id}"}
        
        daily_sales = sales_data.groupby('date')['quantity_sold'].sum()
        recent_avg = daily_sales.tail(30).mean() if len(daily_sales) >= 30 else daily_sales.mean()
        
        forecast_dates = pd.date_range(
            start=datetime.now().date() + timedelta(days=1),
            periods=forecast_periods,
            freq='D'
        )
        
        base_forecast = recent_avg
        forecasts = []
        
        for i, date in enumerate(forecast_dates):
            trend_factor = 1 + (i * 0.001)
            seasonal_factor = 1 + 0.1 * np.sin(2 * np.pi * i / 7)
            forecast_value = base_forecast * trend_factor * seasonal_factor
            
            forecasts.append({
                "date": date.strftime("%Y-%m-%d"),
                "forecasted_demand": round(max(0, forecast_value), 2),
                "confidence_interval_lower": round(max(0, forecast_value * 0.8), 2),
                "confidence_interval_upper": round(forecast_value * 1.2, 2)
            })
        
        # Add summary statistics
        total_forecasted_demand = sum([f["forecasted_demand"] for f in forecasts])
        avg_daily_forecast = total_forecasted_demand / len(forecasts)
        
        return {
            "item_id": item_id,
            "forecast_horizon_days": forecast_periods,
            "forecasts": forecasts,
            "model_type": "Moving Average with Trend/Seasonality",
            "summary": {
                "total_forecasted_demand": round(total_forecasted_demand, 2),
                "average_daily_forecast": round(avg_daily_forecast, 2),
                "peak_demand_day": max(forecasts, key=lambda x: x["forecasted_demand"])["date"],
                "lowest_demand_day": min(forecasts, key=lambda x: x["forecasted_demand"])["date"]
            }
        }
        
    except Exception as e:
        logger.error(f"Error forecasting demand for {item_id}: {str(e)}")
        return {"error": f"Failed to forecast demand: {str(e)}"}


def recommend_reorder_strategy(item_id: str, service_level: float = 0.95) -> Dict[str, Any]:
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
        
        inventory_data = analytics.inventory_data.copy()
        item_data = inventory_data[inventory_data['item_id'] == item_id]
        
        if item_data.empty:
            return {"error": f"Item {item_id} not found"}
        
        item_info = item_data.iloc[0]
        sales_data = analytics.sales_data[analytics.sales_data['item_id'] == item_id]
        
        daily_demand = sales_data.groupby('date')['quantity_sold'].sum()
        avg_demand = daily_demand.mean() if len(daily_demand) > 0 else 0
        demand_std = daily_demand.std() if len(daily_demand) > 1 else 0
        
        # Simple safety stock calculation
        from scipy import stats
        z_score = stats.norm.ppf(service_level)
        safety_stock = z_score * demand_std * np.sqrt(item_info['lead_time_days'])
        
        reorder_point = (avg_demand * item_info['lead_time_days']) + safety_stock
        
        # Economic Order Quantity (simplified)
        holding_cost_rate = 0.20
        ordering_cost = 50
        annual_demand = avg_demand * 365
        
        if annual_demand > 0 and item_info['unit_cost'] > 0:
            eoq = np.sqrt((2 * annual_demand * ordering_cost) / 
                         (item_info['unit_cost'] * holding_cost_rate))
        else:
            eoq = 100
        
        recommendations = {
            "item_id": item_id,
            "current_reorder_point": int(item_info['reorder_point']),
            "recommended_reorder_point": round(max(0, reorder_point), 0),
            "recommended_order_quantity": round(max(1, eoq), 0),
            "safety_stock": round(max(0, safety_stock), 0),
            "service_level": service_level,
            "average_daily_demand": round(avg_demand, 2),
            "lead_time_days": int(item_info['lead_time_days']),
            "recommendations": []
        }
        
        if reorder_point > item_info['reorder_point']:
            recommendations["recommendations"].append(
                f"Increase reorder point to {round(reorder_point, 0)} for {service_level*100}% service level"
            )
        
        if item_info['current_stock'] < reorder_point:
            recommendations["recommendations"].append(
                f"Immediate reorder needed - current stock below recommended point"
            )
        
        # Add priority level
        if recommendations["current_reorder_point"] < recommendations["recommended_reorder_point"]:
            recommendations["priority"] = "High - Reorder point adjustment needed"
        else:
            recommendations["priority"] = "Normal - Current settings adequate"
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error generating reorder strategy for {item_id}: {str(e)}")
        return {"error": f"Failed to generate reorder strategy: {str(e)}"}


# Create the ADK Agent following the official structure
root_agent = Agent(
    name="inventory_agent",
    model="gemini-2.0-flash",
    description="Expert inventory management agent providing comprehensive analytics and optimization recommendations",
    instruction="""You are an expert supply chain analyst and inventory management specialist. 
    Your goal is to provide deep, actionable insights into inventory management, demand forecasting, 
    and logistics optimization. You excel at analyzing complex inventory data, identifying root causes 
    of stockouts and overstock situations, and providing data-driven recommendations that improve 
    service levels while minimizing costs. Always provide specific, actionable recommendations 
    backed by quantitative analysis.""",
    tools=[
        generate_inventory_summary,
        get_item_details,
        analyze_stockout_root_cause,
        forecast_demand,
        recommend_reorder_strategy,
    ]
)
