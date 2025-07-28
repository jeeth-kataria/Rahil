"""
Descriptive Analytics Agent - Tier 1

Specializes in current and historical inventory state reporting.
Provides comprehensive overviews of inventory status, item details, and stock monitoring.
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any
import logging

# Add parent directory to path to import shared analytics
sys.path.append(str(Path(__file__).parent.parent))
from shared_analytics import analytics_backend

from google.adk.agents import Agent

logger = logging.getLogger(__name__)


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
        inventory_data = analytics_backend.get_inventory_data()
        
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
        inventory_data = analytics_backend.get_inventory_data(item_id=item_id)
        
        if inventory_data.empty:
            return {"error": f"Item {item_id} not found in inventory"}
        
        item_info = inventory_data.iloc[0].to_dict()
        
        # Get recent sales data
        sales_data = analytics_backend.get_sales_data(item_id=item_id, start_date="2024-11-01", end_date="2024-12-31")
        
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


def get_category_overview(category: str) -> Dict[str, Any]:
    """
    Get overview of inventory for a specific category.
    
    Args:
        category: Product category to analyze
        
    Returns:
        Dict containing category-specific inventory insights
    """
    try:
        inventory_data = analytics_backend.get_inventory_data(category=category)
        
        if inventory_data.empty:
            return {"error": f"No items found in category: {category}"}
        
        total_items = len(inventory_data)
        total_value = (inventory_data['current_stock'] * inventory_data['unit_cost']).sum()
        avg_stock_level = inventory_data['current_stock'].mean()
        items_below_reorder = len(inventory_data[inventory_data['current_stock'] < inventory_data['reorder_point']])
        
        overview = {
            "category": category,
            "total_items": total_items,
            "total_category_value": round(total_value, 2),
            "average_stock_level": round(avg_stock_level, 2),
            "items_below_reorder": items_below_reorder,
            "reorder_percentage": round((items_below_reorder / total_items) * 100, 1),
            "top_value_items": inventory_data.nlargest(5, 'current_stock')[['item_id', 'item_name', 'current_stock', 'unit_cost']].to_dict('records')
        }
        
        return overview
        
    except Exception as e:
        logger.error(f"Error getting category overview for {category}: {str(e)}")
        return {"error": f"Failed to get category overview: {str(e)}"}


def get_stock_alerts() -> Dict[str, Any]:
    """
    Get current stock alerts for items requiring attention.
    
    Returns:
        Dict containing various stock alert categories
    """
    try:
        inventory_data = analytics_backend.get_inventory_data()
        
        # Out of stock items
        out_of_stock = inventory_data[inventory_data['current_stock'] == 0]
        
        # Below reorder point
        below_reorder = inventory_data[
            (inventory_data['current_stock'] < inventory_data['reorder_point']) & 
            (inventory_data['current_stock'] > 0)
        ]
        
        # Overstock items
        overstock = inventory_data[inventory_data['current_stock'] > inventory_data['max_stock'] * 0.9]
        
        alerts = {
            "out_of_stock": {
                "count": len(out_of_stock),
                "items": out_of_stock[['item_id', 'item_name', 'category', 'supplier_id']].to_dict('records')
            },
            "below_reorder_point": {
                "count": len(below_reorder),
                "items": below_reorder[['item_id', 'item_name', 'current_stock', 'reorder_point', 'category']].to_dict('records')
            },
            "overstock_risk": {
                "count": len(overstock),
                "items": overstock[['item_id', 'item_name', 'current_stock', 'max_stock', 'category']].to_dict('records')
            },
            "total_alerts": len(out_of_stock) + len(below_reorder) + len(overstock)
        }
        
        return alerts
        
    except Exception as e:
        logger.error(f"Error getting stock alerts: {str(e)}")
        return {"error": f"Failed to get stock alerts: {str(e)}"}


def get_supplier_inventory_summary(supplier_id: str) -> Dict[str, Any]:
    """
    Get inventory summary for items from a specific supplier.
    
    Args:
        supplier_id: Supplier identifier
        
    Returns:
        Dict containing supplier-specific inventory summary
    """
    try:
        inventory_data = analytics_backend.get_inventory_data()
        supplier_items = inventory_data[inventory_data['supplier_id'] == supplier_id]
        
        if supplier_items.empty:
            return {"error": f"No items found for supplier: {supplier_id}"}
        
        supplier_info = analytics_backend.get_supplier_data(supplier_id=supplier_id)
        
        summary = {
            "supplier_id": supplier_id,
            "supplier_name": supplier_info.iloc[0]['supplier_name'] if not supplier_info.empty else "Unknown",
            "total_items": len(supplier_items),
            "total_inventory_value": round((supplier_items['current_stock'] * supplier_items['unit_cost']).sum(), 2),
            "items_below_reorder": len(supplier_items[supplier_items['current_stock'] < supplier_items['reorder_point']]),
            "average_lead_time": round(supplier_items['lead_time_days'].mean(), 1),
            "categories_supplied": supplier_items['category'].unique().tolist(),
            "item_breakdown": supplier_items[['item_id', 'item_name', 'current_stock', 'reorder_point', 'category']].to_dict('records')
        }
        
        return summary
        
    except Exception as e:
        logger.error(f"Error getting supplier inventory summary for {supplier_id}: {str(e)}")
        return {"error": f"Failed to get supplier inventory summary: {str(e)}"}


# Create the Descriptive Analytics Agent
root_agent = Agent(
    name="descriptive_analytics_agent",
    model="gemini-2.0-flash",
    description="Descriptive Analytics Specialist - Provides comprehensive current and historical inventory state reporting, item details, and stock monitoring",
    instruction="""You are a Descriptive Analytics Specialist focused on Tier 1 inventory analytics. 
    Your expertise is in providing comprehensive overviews of current inventory status, detailed item information, 
    and real-time stock monitoring. You excel at generating clear, actionable reports about what is currently 
    happening in the inventory system. Always provide detailed summaries with key insights and actionable alerts.""",
    tools=[
        generate_inventory_summary,
        get_item_details,
        get_category_overview,
        get_stock_alerts,
        get_supplier_inventory_summary,
    ]
)
