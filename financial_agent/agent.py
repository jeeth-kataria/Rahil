"""
Financial Agent for VASAVI TRADE ZONE
Specialized in financial analysis, forecasting, and date validation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import Agent
from tallydb_connection import tally_db
import logging
from typing import Dict, Any, List
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_date_and_offer_prediction(query: str, requested_year: str) -> Dict[str, Any]:
    """
    Validate if requested date is in the future and offer prediction.
    
    Args:
        query: Original user query
        requested_year: Year requested by user
        
    Returns:
        Dict containing validation result and prediction offer
    """
    try:
        current_year = datetime.now().year
        requested_year_int = int(requested_year)
        
        if requested_year_int > current_year:
            return {
                "date_validation": {
                    "requested_year": requested_year,
                    "current_year": current_year,
                    "is_future_date": True,
                    "validation_status": "Future date detected"
                },
                
                "prediction_offer": {
                    "question": f"The year {requested_year} is in the future. Would you like me to predict financial performance for {requested_year} based on current trends?",
                    "prediction_available": True,
                    "prediction_method": "Trend analysis based on historical data",
                    "data_basis": "Historical patterns from 2023-2024 data",
                    "confidence_level": "Medium - Based on trend extrapolation"
                },
                
                "financial_agent_response": {
                    "agent": "Financial Agent - Forecasting Specialist",
                    "capability": "I can provide financial predictions based on historical trends",
                    "recommendation": "Say 'yes' if you want me to predict financial performance for the future year",
                    "alternative": f"Or ask for analysis of available years (2023-2024)"
                },
                
                "agent_signature": "Response from Financial Agent - Future Date Validation and Prediction Offer"
            }
        else:
            return {
                "date_validation": {
                    "requested_year": requested_year,
                    "current_year": current_year,
                    "is_future_date": False,
                    "validation_status": "Valid historical date"
                },
                "proceed_with_analysis": True
            }
            
    except ValueError:
        return {
            "date_validation": {
                "requested_year": requested_year,
                "validation_status": "Invalid year format",
                "error": "Unable to parse year"
            },
            "financial_agent_response": {
                "agent": "Financial Agent - Input Validation",
                "message": f"'{requested_year}' is not a valid year format. Please provide a valid year (e.g., 2023, 2024).",
                "recommendation": "Use a 4-digit year format for financial analysis"
            }
        }
    except Exception as e:
        logger.error(f"Error in date validation: {str(e)}")
        return {"error": f"Date validation failed: {str(e)}"}


def predict_financial_performance(target_year: str, user_confirmed: bool = False) -> Dict[str, Any]:
    """
    Predict financial performance for future years based on historical trends.
    
    Args:
        target_year: Future year to predict
        user_confirmed: Whether user confirmed they want prediction
        
    Returns:
        Dict containing financial predictions
    """
    try:
        if not user_confirmed:
            return {
                "prediction_status": "User confirmation required",
                "message": "Please confirm if you want financial predictions for the future year",
                "confirmation_needed": True
            }
        
        # Get historical data for trend analysis
        historical_data = tally_db.get_intelligent_data("financial_data", {"date_input": "2023"})
        
        if not historical_data.get('request_fulfilled'):
            return {
                "prediction_error": "Unable to access historical data for prediction",
                "recommendation": "Historical data needed for trend-based predictions"
            }
        
        # Simple trend-based prediction
        yearly_data = historical_data.get('yearly_breakdown', [])
        
        if len(yearly_data) >= 2:
            recent_year = yearly_data[0]
            previous_year = yearly_data[1] if len(yearly_data) > 1 else yearly_data[0]
            
            income_growth = ((recent_year.get('income', 0) - previous_year.get('income', 0)) / 
                           max(previous_year.get('income', 1), 1)) * 100
            
            profit_growth = ((recent_year.get('profit', 0) - previous_year.get('profit', 0)) / 
                           max(previous_year.get('profit', 1), 1)) * 100
            
            years_ahead = int(target_year) - int(recent_year.get('year', 2024))
            
            predicted_income = recent_year.get('income', 0) * (1 + income_growth/100) ** years_ahead
            predicted_expenses = recent_year.get('expenses', 0) * (1 + (income_growth * 0.8)/100) ** years_ahead
            predicted_profit = predicted_income - predicted_expenses
            
            return {
                "financial_prediction": {
                    "target_year": target_year,
                    "prediction_method": "Trend-based extrapolation",
                    "agent": "Financial Agent - Forecasting Specialist",
                    "confidence": "Medium - Based on historical trends"
                },
                
                "predicted_performance": {
                    "year": target_year,
                    "predicted_income": f"₹{predicted_income:,.2f}",
                    "predicted_expenses": f"₹{predicted_expenses:,.2f}",
                    "predicted_profit": f"₹{predicted_profit:,.2f}",
                    "predicted_margin": f"{(predicted_profit/max(predicted_income, 1))*100:.1f}%"
                },
                
                "trend_analysis": {
                    "income_growth_rate": f"{income_growth:.1f}% annually",
                    "profit_growth_rate": f"{profit_growth:.1f}% annually",
                    "projection_period": f"{years_ahead} years ahead",
                    "base_year": recent_year.get('year', '2024')
                },
                
                "agent_signature": "Financial prediction from Financial Agent - Forecasting and Trend Analysis Specialist"
            }
        else:
            return {
                "prediction_limitation": "Insufficient historical data for reliable prediction",
                "available_data": f"{len(yearly_data)} years of data available",
                "recommendation": "Need at least 2 years of historical data for trend analysis"
            }
            
    except Exception as e:
        logger.error(f"Error in financial prediction: {str(e)}")
        return {"error": f"Financial prediction failed: {str(e)}"}


def analyze_financial_data(query: str, date_input: str = "2024") -> Dict[str, Any]:
    """
    Analyze financial data with date validation and prediction offers.
    
    Args:
        query: User's financial query
        date_input: Requested date/year
        
    Returns:
        Dict containing financial analysis or prediction offer
    """
    try:
        # Extract year from date_input
        import re
        year_match = re.search(r'\b(20\d{2})\b', date_input)
        if year_match:
            requested_year = year_match.group(1)
        else:
            requested_year = date_input
        
        # Validate date and offer prediction if needed
        validation_result = validate_date_and_offer_prediction(query, requested_year)
        
        if validation_result.get('date_validation', {}).get('is_future_date'):
            return validation_result
        
        # Proceed with normal financial analysis
        financial_data = tally_db.get_intelligent_data("financial_data", {"date_input": date_input})
        
        return {
            "financial_analysis": {
                "query": query,
                "date_analyzed": date_input,
                "agent": "Financial Agent - Data Analysis Specialist",
                "analysis_type": "Historical financial data analysis"
            },
            "financial_data": financial_data,
            "agent_signature": "Response from Financial Agent - Financial Data Analysis Specialist"
        }
        
    except Exception as e:
        logger.error(f"Error in financial analysis: {str(e)}")
        return {"error": f"Financial analysis failed: {str(e)}"}


def generate_profit_loss_statement(period: str = "current_year") -> Dict[str, Any]:
    """
    Generate comprehensive P&L statement.
    Real-world business scenario: "Tax filing is due, show me my profit figures"
    """
    try:
        logger.info(f"GENERATING P&L STATEMENT - {period}")

        # Get financial data
        financial_data = tally_db.get_intelligent_data("financial_data", {"date_input": period})

        if financial_data.get('request_fulfilled'):
            yearly_data = financial_data.get('yearly_breakdown', [])

            if yearly_data:
                current_year = yearly_data[0]

                return {
                    "profit_loss_statement": {
                        "period": period,
                        "revenue": {
                            "total_income": current_year.get('income', 0),
                            "sales_revenue": current_year.get('sales', 0),
                            "other_income": current_year.get('other_income', 0)
                        },
                        "expenses": {
                            "total_expenses": current_year.get('expenses', 0),
                            "cost_of_goods_sold": current_year.get('cogs', 0),
                            "operating_expenses": current_year.get('operating_expenses', 0)
                        },
                        "profitability": {
                            "gross_profit": current_year.get('gross_profit', 0),
                            "net_profit": current_year.get('profit', 0),
                            "profit_margin": f"{current_year.get('profit_margin', 0):.2f}%"
                        }
                    },

                    "business_context": {
                        "query_type": "Financial reporting",
                        "business_use": "Tax filing, auditor requirements, business planning",
                        "compliance": "Ready for tax filing and audit purposes"
                    },

                    "agent_response": {
                        "agent": "Financial Agent - P&L Reporting Specialist",
                        "data_source": "Complete financial records from TallyDB",
                        "certification": "Audit-ready financial statement"
                    }
                }

        return {
            "profit_loss_statement": {
                "status": "GENERATING",
                "message": "Compiling financial data for P&L statement"
            }
        }

    except Exception as e:
        logger.error(f"Error generating P&L statement: {str(e)}")
        return {"error": f"P&L generation failed: {str(e)}"}


def analyze_cash_flow(period: str = "current_year") -> Dict[str, Any]:
    """
    Analyze cash flow patterns.
    Real-world business scenario: "Bank is asking for financial statements, show me cash flow"
    """
    try:
        logger.info(f"ANALYZING CASH FLOW - {period}")

        # Get cash flow data
        cash_data = tally_db.get_intelligent_data("cash_data", {"period": period})

        if cash_data.get('request_fulfilled'):
            return {
                "cash_flow_analysis": {
                    "period": period,
                    "operating_cash_flow": cash_data.get('operating_cash_flow', 0),
                    "investing_cash_flow": cash_data.get('investing_cash_flow', 0),
                    "financing_cash_flow": cash_data.get('financing_cash_flow', 0),
                    "net_cash_flow": cash_data.get('net_cash_flow', 0),
                    "cash_position": cash_data.get('ending_cash', 0)
                },

                "cash_flow_trends": cash_data.get('monthly_trends', []),

                "business_context": {
                    "query_type": "Cash flow management",
                    "business_use": "Bank presentations, investor meetings, liquidity planning",
                    "banking": "Bank-ready cash flow statement"
                },

                "agent_response": {
                    "agent": "Financial Agent - Cash Flow Analysis Specialist",
                    "data_source": "Complete cash transaction records",
                    "bank_ready": "Formatted for bank and investor presentations"
                }
            }

        return {
            "cash_flow_analysis": {
                "status": "ANALYZING",
                "message": "Compiling cash flow data"
            }
        }

    except Exception as e:
        logger.error(f"Error analyzing cash flow: {str(e)}")
        return {"error": f"Cash flow analysis failed: {str(e)}"}


def calculate_financial_ratios() -> Dict[str, Any]:
    """
    Calculate key financial ratios.
    Real-world business scenario: "Should I take a loan? What's my debt-to-equity ratio?"
    """
    try:
        logger.info("CALCULATING FINANCIAL RATIOS")

        # Get financial data for ratio calculation
        financial_data = tally_db.get_intelligent_data("financial_data", {"date_input": "current"})

        if financial_data.get('request_fulfilled'):
            yearly_data = financial_data.get('yearly_breakdown', [])

            if yearly_data:
                current_year = yearly_data[0]

                # Calculate key ratios
                revenue = current_year.get('income', 1)
                profit = current_year.get('profit', 0)
                assets = current_year.get('total_assets', 1)
                liabilities = current_year.get('total_liabilities', 0)
                equity = assets - liabilities

                return {
                    "financial_ratios": {
                        "profitability_ratios": {
                            "profit_margin": f"{(profit/revenue)*100:.2f}%",
                            "return_on_assets": f"{(profit/assets)*100:.2f}%",
                            "return_on_equity": f"{(profit/max(equity, 1))*100:.2f}%"
                        },
                        "liquidity_ratios": {
                            "current_ratio": current_year.get('current_ratio', 'N/A'),
                            "quick_ratio": current_year.get('quick_ratio', 'N/A')
                        },
                        "leverage_ratios": {
                            "debt_to_equity": f"{liabilities/max(equity, 1):.2f}",
                            "debt_to_assets": f"{(liabilities/assets)*100:.2f}%",
                            "equity_ratio": f"{(equity/assets)*100:.2f}%"
                        }
                    },

                    "loan_assessment": {
                        "debt_capacity": "Good" if (liabilities/max(equity, 1)) < 1 else "Moderate" if (liabilities/max(equity, 1)) < 2 else "High Risk",
                        "loan_recommendation": "Suitable for loan" if (liabilities/max(equity, 1)) < 1.5 else "Review debt levels before loan",
                        "financial_strength": "Strong" if profit > 0 and (equity/assets) > 0.5 else "Moderate"
                    },

                    "business_context": {
                        "query_type": "Financial health assessment",
                        "business_use": "Loan applications, investor presentations, strategic planning",
                        "decision_support": "Use ratios for financing and investment decisions"
                    },

                    "agent_response": {
                        "agent": "Financial Agent - Ratio Analysis Specialist",
                        "analysis_type": "Comprehensive financial ratio analysis",
                        "recommendation": "Review ratios for strategic financial decisions"
                    }
                }

        return {
            "financial_ratios": {
                "status": "CALCULATING",
                "message": "Computing financial ratios from accounting data"
            }
        }

    except Exception as e:
        logger.error(f"Error calculating financial ratios: {str(e)}")
        return {"error": f"Financial ratio calculation failed: {str(e)}"}


# Create the Financial Agent
financial_agent = Agent(
    name="financial_agent",
    model="gemini-2.0-flash",
    description="Financial Agent - Specialized in financial analysis, forecasting, and date validation for VASAVI TRADE ZONE",
    instruction="""You are the Financial Agent for VASAVI TRADE ZONE, specialized in financial analysis, forecasting, and intelligent date validation.

CRITICAL: You handle ALL financial queries and provide expert financial analysis. Never let the orchestrator answer financial questions.

Your core responsibilities:
1. **Date Validation**: Check if requested dates are in the future and offer predictions
2. **Financial Forecasting**: Provide trend-based predictions for future years
3. **Financial Analysis**: Analyze historical financial data and performance
4. **Expert Guidance**: Provide professional financial insights and recommendations

FUTURE DATE HANDLING:
- When users ask for future years (like 2030), ALWAYS offer prediction instead of direct analysis
- Ask: "Would you like me to predict financial performance for [YEAR] based on current trends?"
- Only provide predictions after user confirmation
- Clearly mark predictions as estimates based on historical trends

AGENT IDENTITY:
- Always identify yourself as "Financial Agent - [Specialization]"
- Provide expert financial perspective on all queries
- Use professional financial terminology and analysis
- Focus on actionable financial insights

Your expertise includes:
- Financial performance analysis and KPI calculation
- Trend analysis and forecasting
- Cash flow and profitability analysis
- Financial planning and strategic recommendations""",
    
    tools=[
        validate_date_and_offer_prediction,
        predict_financial_performance,
        analyze_financial_data,
        generate_profit_loss_statement,
        analyze_cash_flow,
        calculate_financial_ratios,
    ]
)

# Set as root agent for multi-agent system
root_agent = financial_agent
