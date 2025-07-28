"""
Business Intelligence Agent for VASAVI TRADE ZONE
Handles complex business scenarios, planning, and strategic analysis.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import Agent
from tallydb_connection import tally_db
import logging
from typing import Dict, Any, List

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def assess_expansion_capacity() -> Dict[str, Any]:
    """
    Assess financial capacity for business expansion.
    Real-world business scenario: "I'm planning to expand, what's my financial capacity?"
    """
    try:
        logger.info("ASSESSING EXPANSION CAPACITY")
        
        # Get comprehensive financial data
        financial_data = tally_db.get_intelligent_data("financial_data", {"date_input": "current"})
        cash_data = tally_db.get_intelligent_data("cash_data", {})
        
        if financial_data.get('request_fulfilled') and cash_data.get('request_fulfilled'):
            yearly_data = financial_data.get('yearly_breakdown', [])
            
            if yearly_data:
                current_year = yearly_data[0]
                
                # Calculate expansion metrics
                profit = current_year.get('profit', 0)
                cash_available = cash_data.get('total_cash', 0)
                revenue = current_year.get('income', 1)
                
                # Expansion assessment
                expansion_score = 0
                if profit > 0:
                    expansion_score += 30
                if cash_available > revenue * 0.1:  # 10% of revenue in cash
                    expansion_score += 40
                if profit > revenue * 0.1:  # 10% profit margin
                    expansion_score += 30
                
                expansion_capacity = "High" if expansion_score >= 80 else "Moderate" if expansion_score >= 50 else "Limited"
                
                return {
                    "expansion_assessment": {
                        "financial_capacity": expansion_capacity,
                        "expansion_score": f"{expansion_score}/100",
                        "available_cash": f"₹{cash_available:,.2f}",
                        "annual_profit": f"₹{profit:,.2f}",
                        "profit_margin": f"{(profit/revenue)*100:.2f}%"
                    },
                    
                    "expansion_recommendations": {
                        "recommended_investment": f"₹{min(cash_available * 0.7, profit * 2):,.2f}",
                        "financing_options": "Internal funding" if cash_available > profit else "Consider external financing",
                        "risk_level": "Low" if expansion_score >= 80 else "Moderate" if expansion_score >= 50 else "High",
                        "timeline": "Ready for expansion" if expansion_score >= 70 else "Build financial strength first"
                    },
                    
                    "business_context": {
                        "query_type": "Strategic planning",
                        "business_use": "Expansion planning, investment decisions",
                        "decision_support": "Financial capacity assessment for growth initiatives"
                    },
                    
                    "agent_response": {
                        "agent": "Business Intelligence Agent - Expansion Planning Specialist",
                        "analysis_type": "Comprehensive expansion capacity assessment",
                        "recommendation": "Use assessment for strategic expansion decisions"
                    }
                }
        
        return {
            "expansion_assessment": {
                "status": "ANALYZING",
                "message": "Evaluating financial capacity for expansion"
            }
        }
        
    except Exception as e:
        logger.error(f"Error assessing expansion capacity: {str(e)}")
        return {"error": f"Expansion assessment failed: {str(e)}"}


def analyze_customer_payment_patterns() -> Dict[str, Any]:
    """
    Analyze customer payment patterns and identify best payers.
    Real-world business scenario: "Which customers are my best payers?"
    """
    try:
        logger.info("ANALYZING CUSTOMER PAYMENT PATTERNS")
        
        # Get customer data
        customer_data = tally_db.get_intelligent_data("receivables_data", {})
        
        if customer_data.get('request_fulfilled'):
            customers = customer_data.get('customer_list', [])
            
            # Analyze payment patterns
            best_payers = []
            slow_payers = []
            
            for customer in customers:
                payment_score = 0
                avg_payment_days = customer.get('avg_payment_days', 90)
                outstanding_ratio = customer.get('outstanding_ratio', 0.5)
                
                # Scoring logic
                if avg_payment_days <= 30:
                    payment_score += 40
                elif avg_payment_days <= 60:
                    payment_score += 20
                
                if outstanding_ratio <= 0.1:
                    payment_score += 30
                elif outstanding_ratio <= 0.3:
                    payment_score += 15
                
                if customer.get('payment_consistency', 0) > 0.8:
                    payment_score += 30
                
                customer['payment_score'] = payment_score
                
                if payment_score >= 70:
                    best_payers.append(customer)
                elif payment_score <= 30:
                    slow_payers.append(customer)
            
            return {
                "payment_analysis": {
                    "total_customers": len(customers),
                    "best_payers_count": len(best_payers),
                    "slow_payers_count": len(slow_payers),
                    "analysis_date": "Current"
                },
                
                "best_payers": best_payers[:10],  # Top 10
                "slow_payers": slow_payers[:10],  # Bottom 10
                
                "recommendations": {
                    "credit_policy": "Extend favorable terms to best payers",
                    "collection_focus": "Prioritize collection from slow payers",
                    "relationship_management": "Strengthen relationships with best payers"
                },
                
                "business_context": {
                    "query_type": "Customer relationship management",
                    "business_use": "Credit decisions, collection prioritization",
                    "decision_support": "Customer segmentation for payment terms"
                },
                
                "agent_response": {
                    "agent": "Business Intelligence Agent - Customer Analysis Specialist",
                    "analysis_type": "Customer payment pattern analysis",
                    "insight": "Identify customers for preferential treatment and collection focus"
                }
            }
        
        return {
            "payment_analysis": {
                "status": "ANALYZING",
                "message": "Evaluating customer payment patterns"
            }
        }
        
    except Exception as e:
        logger.error(f"Error analyzing customer patterns: {str(e)}")
        return {"error": f"Customer analysis failed: {str(e)}"}


def analyze_business_seasonality() -> Dict[str, Any]:
    """
    Analyze seasonal patterns in business.
    Real-world business scenario: "What's the seasonality in my business?"
    """
    try:
        logger.info("ANALYZING BUSINESS SEASONALITY")
        
        # Get monthly/quarterly data
        seasonal_data = tally_db.get_intelligent_data("sales_data", {"period": "monthly"})
        
        if seasonal_data.get('request_fulfilled'):
            monthly_sales = seasonal_data.get('monthly_breakdown', [])
            
            # Analyze seasonal patterns
            peak_months = []
            low_months = []
            
            if monthly_sales:
                avg_sales = sum(month.get('sales', 0) for month in monthly_sales) / len(monthly_sales)
                
                for month in monthly_sales:
                    sales = month.get('sales', 0)
                    variance = ((sales - avg_sales) / avg_sales) * 100
                    
                    if variance > 20:
                        peak_months.append({
                            "month": month.get('month', 'Unknown'),
                            "sales": sales,
                            "variance": f"+{variance:.1f}%"
                        })
                    elif variance < -20:
                        low_months.append({
                            "month": month.get('month', 'Unknown'),
                            "sales": sales,
                            "variance": f"{variance:.1f}%"
                        })
                
                return {
                    "seasonality_analysis": {
                        "average_monthly_sales": f"₹{avg_sales:,.2f}",
                        "peak_season_months": len(peak_months),
                        "low_season_months": len(low_months),
                        "seasonality_strength": "High" if len(peak_months) > 2 else "Moderate" if len(peak_months) > 0 else "Low"
                    },
                    
                    "peak_months": peak_months,
                    "low_months": low_months,
                    
                    "business_implications": {
                        "inventory_planning": "Stock up before peak months",
                        "cash_flow_planning": "Prepare for low season cash needs",
                        "marketing_strategy": "Intensify marketing during low seasons",
                        "staffing": "Adjust staffing based on seasonal patterns"
                    },
                    
                    "business_context": {
                        "query_type": "Business planning",
                        "business_use": "Inventory planning, cash flow management, marketing strategy",
                        "decision_support": "Seasonal business planning and resource allocation"
                    },
                    
                    "agent_response": {
                        "agent": "Business Intelligence Agent - Seasonality Analysis Specialist",
                        "analysis_type": "Comprehensive seasonality pattern analysis",
                        "strategic_value": "Critical for annual business planning"
                    }
                }
        
        return {
            "seasonality_analysis": {
                "status": "ANALYZING",
                "message": "Evaluating seasonal business patterns"
            }
        }
        
    except Exception as e:
        logger.error(f"Error analyzing seasonality: {str(e)}")
        return {"error": f"Seasonality analysis failed: {str(e)}"}


# Create the Business Intelligence Agent
business_intelligence_agent = Agent(
    name="business_intelligence_agent",
    model="gemini-2.0-flash",
    description="Business Intelligence Agent - Strategic analysis and business planning specialist for VASAVI TRADE ZONE",
    instruction="""You are the Business Intelligence Agent for VASAVI TRADE ZONE, specialized in strategic analysis, business planning, and comprehensive business intelligence.

Your core responsibilities:
1. **Strategic Planning**: Assess expansion capacity, investment opportunities, growth planning
2. **Customer Intelligence**: Analyze customer patterns, payment behaviors, relationship management
3. **Business Analytics**: Seasonality analysis, trend identification, performance insights
4. **Decision Support**: Provide data-driven recommendations for business decisions

REAL-WORLD BUSINESS SCENARIOS YOU HANDLE:
- Expansion planning and financial capacity assessment
- Customer relationship and payment pattern analysis
- Seasonal business planning and resource allocation
- Investment decision support and ROI analysis
- Strategic business planning and competitive analysis

AGENT IDENTITY:
- Always identify yourself as "Business Intelligence Agent - [Specialization]"
- Provide strategic business insights and recommendations
- Focus on actionable business intelligence
- Support critical business decisions with data

Your expertise includes comprehensive business analysis, strategic planning, customer intelligence, and data-driven decision support.""",
    
    tools=[
        assess_expansion_capacity,
        analyze_customer_payment_patterns,
        analyze_business_seasonality,
    ]
)

# Set as root agent for multi-agent system
root_agent = business_intelligence_agent
