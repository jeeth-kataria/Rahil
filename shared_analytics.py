"""
Shared Analytics Backend for Multi-Agent Inventory Management System

This module provides the common data and analytics functions used by all specialized agents.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SharedAnalyticsBackend:
    """Shared analytics backend used by all inventory management agents."""
    
    def __init__(self):
        """Initialize the shared analytics backend with sample data."""
        self.inventory_data = self._generate_sample_inventory_data()
        self.sales_data = self._generate_sample_sales_data()
        self.supplier_data = self._generate_sample_supplier_data()
        logger.info("Shared analytics backend initialized with sample data")
    
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
    
    def get_sales_data(self, item_id: Optional[str] = None, start_date: str = "2024-01-01", end_date: str = "2024-12-31") -> pd.DataFrame:
        """Get sales data for a specific item within date range."""
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        
        filtered_data = self.sales_data[
            (self.sales_data['date'] >= start) &
            (self.sales_data['date'] <= end)
        ].copy()
        
        if item_id:
            filtered_data = filtered_data[filtered_data['item_id'] == item_id]
        
        return filtered_data
    
    def get_inventory_data(self, item_id: Optional[str] = None, category: Optional[str] = None) -> pd.DataFrame:
        """Get inventory data with optional filtering."""
        data = self.inventory_data.copy()
        
        if item_id:
            data = data[data['item_id'] == item_id]
        
        if category:
            data = data[data['category'] == category]
        
        return data
    
    def get_supplier_data(self, supplier_id: Optional[str] = None) -> pd.DataFrame:
        """Get supplier data with optional filtering."""
        data = self.supplier_data.copy()
        
        if supplier_id:
            data = data[data['supplier_id'] == supplier_id]
        
        return data


# Global shared instance
analytics_backend = SharedAnalyticsBackend()
