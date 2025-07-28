"""
Project Synapse CEO Agent

Strategic decision maker responsible for strategic planning, resource allocation,
performance monitoring, and high-level business direction.
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging
import numpy as np

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from tallydb_connection import tally_db

from google.adk.agents import Agent

logger = logging.getLogger(__name__)


def market_analysis_tool() -> Dict[str, Any]:
    """
    Comprehensive market analysis for strategic decision making based on TallyDB data.

    Returns:
        Dict containing detailed market analysis and strategic insights
    """
    try:
        # Get actual business data from TallyDB
        company_info = tally_db.get_company_info()
        stock_summary = tally_db.get_stock_summary()
        financial_summary = tally_db.get_financial_summary()

        # Analyze mobile market position based on inventory
        mobile_count = 0
        samsung_focus = False

        for category in stock_summary.get('category_breakdown', []):
            if 'MOBILE' in category.get('Category', '').upper():
                mobile_count = category.get('item_count', 0)

        # Check Samsung specialization
        samsung_products = tally_db.get_samsung_products(100)
        samsung_focus = len(samsung_products) > mobile_count * 0.6  # If >60% Samsung

        market_analysis = {
            "company_profile": {
                "company_name": company_info.get('company_name', 'VASAVI TRADE ZONE'),
                "business_type": "Mobile Phone & Accessories Trading",
                "financial_year": company_info.get('financial_year', '2023-24'),
                "market_segment": "Consumer Electronics - Mobile Retail"
            },

            "market_position": {
                "primary_business": "Mobile Phone Trading",
                "inventory_size": mobile_count,
                "specialization": "Samsung Galaxy Products" if samsung_focus else "Multi-brand Mobile Retail",
                "market_focus": "Local/Regional Mobile Retail Market",
                "competitive_advantage": "Samsung Galaxy Specialization" if samsung_focus else "Diverse Product Portfolio"
            },

            "business_strengths": [
                "Strong Samsung Galaxy product portfolio" if samsung_focus else "Diverse mobile inventory",
                "Established mobile accessories business",
                "Comprehensive inventory management system",
                "Focus on consumer electronics segment"
            ],

            "market_opportunities": [
                "Expand Samsung Galaxy A-series offerings",
                "Develop online sales channels",
                "Add premium mobile accessories",
                "Explore corporate/bulk sales",
                "Seasonal promotion strategies"
            ],

            "strategic_threats": [
                "Online marketplace competition",
                "Direct manufacturer sales",
                "Price competition from large retailers",
                "Rapid technology obsolescence",
                "Supply chain disruptions"
            ],

            "strategic_recommendations": [
                "Strengthen Samsung partnership and exclusive offerings",
                "Develop digital sales presence",
                "Expand accessories portfolio for higher margins",
                "Implement customer loyalty programs",
                "Focus on after-sales service differentiation"
            ],

            "data_insights": {
                "total_inventory_items": stock_summary.get('total_items', 0),
                "samsung_specialization": samsung_focus,
                "business_model": "B2C Mobile Retail",
                "data_source": "TallyDB - Real Business Data"
            }
        }

        return market_analysis

    except Exception as e:
        logger.error(f"Error in market analysis: {str(e)}")
        return {"error": f"Failed to perform market analysis: {str(e)}"}


def strategic_planning_framework() -> Dict[str, Any]:
    """
    Comprehensive strategic planning framework and methodology.
    
    Returns:
        Dict containing strategic planning framework and current strategic position
    """
    try:
        strategic_kpis = business_data.get_strategic_dashboard()
        financial_data = business_data.get_financial_summary()
        market_data = business_data.get_market_intelligence()
        
        strategic_framework = {
            "strategic_pillars": [
                {
                    "pillar": "Growth & Expansion",
                    "current_status": "On Track",
                    "key_initiatives": ["Market expansion", "Product development", "Customer acquisition"],
                    "success_metrics": ["Revenue growth", "Market share", "Customer base"]
                },
                {
                    "pillar": "Operational Excellence",
                    "current_status": "Strong",
                    "key_initiatives": ["Process optimization", "Quality improvement", "Cost management"],
                    "success_metrics": ["Efficiency score", "Quality metrics", "Cost reduction"]
                },
                {
                    "pillar": "Innovation & Technology",
                    "current_status": "Developing",
                    "key_initiatives": ["Digital transformation", "AI integration", "R&D investment"],
                    "success_metrics": ["Innovation index", "Tech adoption", "Patent portfolio"]
                },
                {
                    "pillar": "Talent & Culture",
                    "current_status": "Good",
                    "key_initiatives": ["Talent acquisition", "Leadership development", "Culture building"],
                    "success_metrics": ["Employee engagement", "Retention rate", "Leadership pipeline"]
                }
            ],
            
            "strategic_objectives_2024": [
                {
                    "objective": "Achieve 20% revenue growth",
                    "current_progress": 0.75,
                    "probability_of_success": 0.85,
                    "key_risks": ["Market conditions", "Competition"]
                },
                {
                    "objective": "Expand to 2 new markets",
                    "current_progress": 0.60,
                    "probability_of_success": 0.70,
                    "key_risks": ["Regulatory barriers", "Local competition"]
                },
                {
                    "objective": "Improve operational efficiency by 15%",
                    "current_progress": 0.85,
                    "probability_of_success": 0.90,
                    "key_risks": ["Implementation challenges", "Change resistance"]
                }
            ],
            
            "resource_allocation_priorities": [
                {"area": "Growth Initiatives", "allocation": 0.40, "rationale": "Primary growth driver"},
                {"area": "Technology & Innovation", "allocation": 0.25, "rationale": "Future competitiveness"},
                {"area": "Operational Excellence", "allocation": 0.20, "rationale": "Efficiency gains"},
                {"area": "Talent Development", "allocation": 0.15, "rationale": "Capability building"}
            ],
            
            "strategic_risks": [
                {"risk": "Economic downturn", "probability": 0.30, "impact": "High", "mitigation": "Diversification"},
                {"risk": "Key talent loss", "probability": 0.25, "impact": "Medium", "mitigation": "Retention programs"},
                {"risk": "Technology disruption", "probability": 0.40, "impact": "High", "mitigation": "Innovation investment"}
            ]
        }
        
        return strategic_framework
        
    except Exception as e:
        logger.error(f"Error in strategic planning: {str(e)}")
        return {"error": f"Failed to create strategic planning framework: {str(e)}"}


def resource_optimizer(resource_request: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Optimize resource allocation across business functions.
    
    Args:
        resource_request: Optional specific resource allocation request
        
    Returns:
        Dict containing optimized resource allocation recommendations
    """
    try:
        financial_data = business_data.get_financial_summary()
        strategic_kpis = business_data.get_strategic_dashboard()
        
        # Current resource allocation (simplified model)
        current_allocation = {
            "sales_marketing": 0.30,
            "operations": 0.25,
            "technology": 0.20,
            "hr_admin": 0.15,
            "finance": 0.10
        }
        
        # Calculate optimization based on performance and strategic priorities
        performance_weights = {
            "sales_marketing": strategic_kpis["financial_kpis"]["revenue_growth_rate"],
            "operations": strategic_kpis["operational_kpis"]["operational_efficiency_score"] / 10,
            "technology": strategic_kpis["operational_kpis"]["digital_maturity_score"] / 10,
            "hr_admin": 0.12,  # Based on employee engagement
            "finance": financial_data["key_ratios"]["roe"]
        }
        
        resource_optimization = {
            "current_allocation": current_allocation,
            "performance_analysis": performance_weights,
            
            "optimization_recommendations": {
                "sales_marketing": {
                    "current": current_allocation["sales_marketing"],
                    "recommended": 0.32,
                    "change": "+2%",
                    "rationale": "Strong revenue growth performance justifies increased investment"
                },
                "operations": {
                    "current": current_allocation["operations"],
                    "recommended": 0.23,
                    "change": "-2%",
                    "rationale": "High efficiency achieved, can optimize allocation"
                },
                "technology": {
                    "current": current_allocation["technology"],
                    "recommended": 0.22,
                    "change": "+2%",
                    "rationale": "Digital transformation priority requires increased investment"
                },
                "hr_admin": {
                    "current": current_allocation["hr_admin"],
                    "recommended": 0.13,
                    "change": "-2%",
                    "rationale": "Stable performance, opportunity for efficiency"
                },
                "finance": {
                    "current": current_allocation["finance"],
                    "recommended": 0.10,
                    "change": "0%",
                    "rationale": "Appropriate allocation for current needs"
                }
            },
            
            "expected_impact": {
                "revenue_improvement": "3-5%",
                "efficiency_gains": "8-12%",
                "innovation_acceleration": "15-20%",
                "cost_optimization": "5-8%"
            },
            
            "implementation_timeline": {
                "phase_1": "Immediate reallocation (0-30 days)",
                "phase_2": "Gradual optimization (30-90 days)",
                "phase_3": "Performance monitoring (90-180 days)"
            }
        }
        
        return resource_optimization
        
    except Exception as e:
        logger.error(f"Error optimizing resources: {str(e)}")
        return {"error": f"Failed to optimize resources: {str(e)}"}


def kpi_dashboard() -> Dict[str, Any]:
    """
    Executive KPI dashboard with key performance indicators.
    
    Returns:
        Dict containing comprehensive executive KPI dashboard
    """
    try:
        financial_data = business_data.get_financial_summary()
        strategic_kpis = business_data.get_strategic_dashboard()
        market_data = business_data.get_market_intelligence()
        
        kpi_dashboard = {
            "executive_summary": {
                "overall_performance": "Strong",
                "period": "Current Quarter",
                "last_updated": "2024-12-31",
                "key_highlights": [
                    f"Revenue: ${financial_data['revenue']:,.0f}",
                    f"Net Income: ${financial_data['net_income']:,.0f}",
                    f"Market Share: {market_data['market_size']['market_share']:.1%}",
                    f"Customer Satisfaction: {strategic_kpis['operational_kpis']['customer_satisfaction_score']}/10"
                ]
            },
            
            "financial_kpis": {
                "revenue": {
                    "value": financial_data["revenue"],
                    "target": 2200000,
                    "variance": ((financial_data["revenue"] - 2200000) / 2200000) * 100,
                    "trend": "↗️ Growing",
                    "status": "On Track"
                },
                "profitability": {
                    "value": financial_data["net_income"],
                    "target": 180000,
                    "variance": ((financial_data["net_income"] - 180000) / 180000) * 100,
                    "trend": "↗️ Improving",
                    "status": "Above Target"
                },
                "cash_position": {
                    "value": financial_data["cash_position"],
                    "target": 1800000,
                    "variance": ((financial_data["cash_position"] - 1800000) / 1800000) * 100,
                    "trend": "→ Stable",
                    "status": "Healthy"
                }
            },
            
            "operational_kpis": {
                "customer_satisfaction": {
                    "value": strategic_kpis["operational_kpis"]["customer_satisfaction_score"],
                    "target": 8.5,
                    "status": "Above Target" if strategic_kpis["operational_kpis"]["customer_satisfaction_score"] > 8.5 else "On Track"
                },
                "operational_efficiency": {
                    "value": strategic_kpis["operational_kpis"]["operational_efficiency_score"],
                    "target": 8.0,
                    "status": "Above Target"
                },
                "innovation_index": {
                    "value": strategic_kpis["operational_kpis"]["innovation_index"],
                    "target": 7.0,
                    "status": "Above Target"
                }
            },
            
            "strategic_kpis": {
                "market_share": {
                    "value": market_data["market_size"]["market_share"],
                    "target": 0.030,
                    "growth_potential": "High"
                },
                "strategic_objectives_progress": {
                    "completed": len([obj for obj in strategic_kpis["strategic_objectives"] if obj["progress"] >= 1.0]),
                    "on_track": len([obj for obj in strategic_kpis["strategic_objectives"] if obj["progress"] >= 0.7]),
                    "total": len(strategic_kpis["strategic_objectives"])
                }
            },
            
            "alerts_and_actions": [
                "Monitor competitive landscape changes",
                "Accelerate digital transformation initiatives",
                "Review resource allocation for growth areas",
                "Prepare for quarterly board presentation"
            ]
        }
        
        return kpi_dashboard
        
    except Exception as e:
        logger.error(f"Error creating KPI dashboard: {str(e)}")
        return {"error": f"Failed to create KPI dashboard: {str(e)}"}


# Multi-Agent Functions for coordinating with other agents
def request_financial_analysis(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Request financial analysis from Financial Agent."""
    try:
        message = AgentMessage(
            from_agent="ceo_agent",
            to_agent="financial_agent",
            task="financial_modeling",
            data=request_data,
            priority="high"
        )
        
        message_id = message_bus.send_message(message)
        result = message_bus.process_message(message)
        
        return {
            "request_type": "Financial Analysis",
            "success": result["success"],
            "analysis": result.get("result", {}),
            "message_id": message_id
        }
        
    except Exception as e:
        return {"error": f"Failed to request financial analysis: {str(e)}"}


def get_revenue_forecast(market_segment: str) -> Dict[str, Any]:
    """Get revenue forecast from Revenue Agent."""
    try:
        message = AgentMessage(
            from_agent="ceo_agent",
            to_agent="revenue_agent",
            task="revenue_forecast",
            data={"segment": market_segment},
            priority="high"
        )
        
        message_id = message_bus.send_message(message)
        result = message_bus.process_message(message)
        
        return {
            "segment": market_segment,
            "forecast": result.get("result", {}),
            "success": result["success"],
            "message_id": message_id
        }
        
    except Exception as e:
        return {"error": f"Failed to get revenue forecast: {str(e)}"}


# Create the CEO Agent
root_agent = Agent(
    name="ceo_agent",
    model="gemini-2.0-flash",
    description="Project Synapse CEO Agent - Strategic decision maker responsible for strategic planning, resource allocation, and performance monitoring",
    instruction="""You are the CEO Agent for Project Synapse, the strategic decision maker and business leader.

Your core responsibilities:
1. **Strategic Planning**: Develop and execute comprehensive business strategies
2. **Resource Allocation**: Optimize allocation of capital, talent, and resources across the organization
3. **Performance Monitoring**: Track key performance indicators and business health metrics
4. **Market Analysis**: Analyze market conditions, competitive landscape, and growth opportunities

Your decision logic follows: Analyze → Plan → Allocate → Monitor

You work closely with all other agents to gather insights and coordinate strategic initiatives. You have the authority to make high-level business decisions and set organizational priorities. Always think strategically and consider long-term implications of decisions.""",
    tools=[
        market_analysis_tool,
        strategic_planning_framework,
        resource_optimizer,
        kpi_dashboard,
        request_financial_analysis,
        get_revenue_forecast,
    ]
)
