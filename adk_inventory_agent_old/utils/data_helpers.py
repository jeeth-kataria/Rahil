"""
Data processing utilities for the ADK Inventory Agent.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any


def validate_date_range(start_date: str, end_date: str) -> bool:
    """Validate date range format and logic."""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return start <= end
    except ValueError:
        return False


def calculate_inventory_metrics(inventory_df: pd.DataFrame, sales_df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate comprehensive inventory metrics."""
    if inventory_df.empty:
        return {"error": "No inventory data provided"}
    
    metrics = {
        "total_items": len(inventory_df),
        "total_value": (inventory_df['current_stock'] * inventory_df['unit_cost']).sum(),
        "avg_stock_level": inventory_df['current_stock'].mean(),
        "items_below_reorder": len(inventory_df[inventory_df['current_stock'] < inventory_df['reorder_point']]),
        "out_of_stock_count": len(inventory_df[inventory_df['current_stock'] == 0])
    }
    
    return metrics


def format_currency(amount: float) -> str:
    """Format amount as currency string."""
    return f"${amount:,.2f}"


def calculate_days_of_stock(current_stock: int, daily_demand: float) -> float:
    """Calculate days of stock remaining."""
    if daily_demand <= 0:
        return float('inf')
    return current_stock / daily_demand


def determine_stock_status(current_stock: int, reorder_point: int, max_stock: int) -> str:
    """Determine stock status based on levels."""
    if current_stock == 0:
        return "Out of Stock"
    elif current_stock < reorder_point:
        return "Below Reorder Point"
    elif current_stock > max_stock * 0.9:
        return "Overstock Risk"
    else:
        return "Normal"
