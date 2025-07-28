"""
Mock Analytics Backend for ADK Inventory Agent

This module provides sample data and analytics functions.
In production, replace with actual database connections and analytics services.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any
import logging

logger = logging.getLogger(__name__)


class MockAnalyticsBackend:
    """
    Mock analytics backend to simulate a real analytics framework.
    In production, this would be replaced with actual database connections.
    """
    
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
    
    def get_inventory_summary(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Get inventory summary for the specified date range."""
        return self.inventory_data.copy()
    
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
    
    def analyze_stockout_causes(self, item_id: str) -> Dict[str, Any]:
        """Analyze potential causes of stockouts for an item."""
        item_data = self.inventory_data[self.inventory_data['item_id'] == item_id]
        if item_data.empty:
            return {"error": f"Item {item_id} not found"}
        
        item_info = item_data.iloc[0]
        sales_data = self.sales_data[self.sales_data['item_id'] == item_id]
        
        daily_demand = sales_data.groupby('date')['quantity_sold'].sum()
        demand_std = daily_demand.std() if len(daily_demand) > 1 else 0
        avg_demand = daily_demand.mean() if len(daily_demand) > 0 else 0
        
        analysis = {
            "current_stock": int(item_info['current_stock']),
            "reorder_point": int(item_info['reorder_point']),
            "average_daily_demand": round(avg_demand, 2),
            "demand_variability": round(demand_std, 2),
            "lead_time_days": int(item_info['lead_time_days']),
            "potential_causes": []
        }
        
        if item_info['current_stock'] < item_info['reorder_point']:
            analysis["potential_causes"].append("Current stock below reorder point")
        
        if demand_std > avg_demand * 0.5:
            analysis["potential_causes"].append("High demand variability")
        
        if item_info['lead_time_days'] > 14:
            analysis["potential_causes"].append("Long supplier lead time")
        
        return analysis
    
    def forecast_demand(self, item_id: str, periods: int) -> Dict[str, Any]:
        """Generate demand forecast for an item."""
        sales_data = self.get_sales_data(item_id, "2024-01-01", "2024-12-31")
        
        if sales_data.empty:
            return {"error": f"No sales data found for item {item_id}"}
        
        daily_sales = sales_data.groupby('date')['quantity_sold'].sum()
        recent_avg = daily_sales.tail(30).mean() if len(daily_sales) >= 30 else daily_sales.mean()
        
        forecast_dates = pd.date_range(
            start=datetime.now().date() + timedelta(days=1),
            periods=periods,
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
        
        return {
            "item_id": item_id,
            "forecast_horizon_days": periods,
            "forecasts": forecasts,
            "model_type": "Moving Average with Trend/Seasonality"
        }
    
    def recommend_reorder_strategy(self, item_id: str, service_level: float) -> Dict[str, Any]:
        """Generate reorder strategy recommendations."""
        item_data = self.inventory_data[self.inventory_data['item_id'] == item_id]
        if item_data.empty:
            return {"error": f"Item {item_id} not found"}
        
        item_info = item_data.iloc[0]
        sales_data = self.sales_data[self.sales_data['item_id'] == item_id]
        
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
        
        return recommendations
