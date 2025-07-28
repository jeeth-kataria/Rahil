"""
Example usage of the ADK Inventory Agent

This script demonstrates how to interact with the agent programmatically.
"""

import sys
import os
from pathlib import Path

# Add the agent directory to Python path
agent_dir = Path(__file__).parent
sys.path.insert(0, str(agent_dir))

# Import the agent
try:
    from agent import inventory_agent
    print("✅ Successfully imported inventory_agent")
except ImportError as e:
    print(f"❌ Failed to import agent: {e}")
    print("Make sure you're in the agent directory and have installed requirements")
    sys.exit(1)

def demonstrate_agent_capabilities():
    """Demonstrate various agent capabilities."""
    
    print("\n🤖 ADK Inventory Agent - Example Usage")
    print("=" * 50)
    
    # Note: In the actual ADK web interface, you would interact with the agent
    # through natural language. This is just to show the agent structure.
    
    print("\n📊 Available Agent Tools:")
    for i, tool in enumerate(inventory_agent.tools, 1):
        tool_name = getattr(tool, '__name__', str(tool))
        print(f"   {i}. {tool_name}")
    
    print(f"\n🎯 Agent Name: {inventory_agent.name}")
    print(f"📝 Description: {inventory_agent.description}")
    print(f"🤖 Model: {inventory_agent.model}")
    
    print("\n💡 Example Prompts to try in the ADK Web UI:")
    example_prompts = [
        "Generate an inventory summary for the last 30 days",
        "Show me details for item ITEM_001", 
        "Analyze the root cause of stockouts for ITEM_042",
        "Forecast demand for ITEM_023 for the next 30 days",
        "Recommend an optimal reorder strategy for ITEM_056 with 95% service level"
    ]
    
    for i, prompt in enumerate(example_prompts, 1):
        print(f"   {i}. {prompt}")
    
    print("\n🚀 To interact with the agent:")
    print("   1. Run: python run_agent.py")
    print("   2. Open: http://localhost:8000")
    print("   3. Select: adk_inventory_agent")
    print("   4. Start chatting!")

def show_sample_data():
    """Show sample data structure."""
    print("\n📁 Sample Data Structure:")
    print("-" * 30)
    
    # This would show the structure of the mock data
    print("Items: ITEM_001 to ITEM_100")
    print("Categories: Electronics, Clothing, Home & Garden, Sports, Books")
    print("Suppliers: SUP_001 to SUP_020")
    print("Date Range: 2024-01-01 to 2024-12-31")

if __name__ == "__main__":
    demonstrate_agent_capabilities()
    show_sample_data()
