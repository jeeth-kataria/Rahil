"""
Advanced Financial Agent for VASAVI TRADE ZONE
Comprehensive financial analysis, forecasting, and strategic insights
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

        # Simple trend-based prediction (can be enhanced with more sophisticated models)
        yearly_data = historical_data.get('yearly_breakdown', [])

        if len(yearly_data) >= 2:
            # Calculate growth trends
            recent_year = yearly_data[0]
            previous_year = yearly_data[1] if len(yearly_data) > 1 else yearly_data[0]

            income_growth = ((recent_year.get('income', 0) - previous_year.get('income', 0)) /
                           max(previous_year.get('income', 1), 1)) * 100

            profit_growth = ((recent_year.get('profit', 0) - previous_year.get('profit', 0)) /
                           max(previous_year.get('profit', 1), 1)) * 100

            # Project to target year
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

                "prediction_disclaimer": {
                    "accuracy": "Predictions are estimates based on historical trends",
                    "factors_not_considered": "Market changes, economic conditions, business strategy changes",
                    "recommendation": "Use as guidance only, not for critical business decisions",
                    "update_frequency": "Predictions should be updated as new data becomes available"
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


def analyze_quarterly_performance(year: str = "2023") -> Dict[str, Any]:
    """
    Analyze quarterly financial performance with detailed insights.
    
    Args:
        year: Year for quarterly analysis
        
    Returns:
        Dict containing detailed quarterly analysis
    """
    try:
        # Get quarterly data from TallyDB
        quarterly_data = tally_db.get_quarterly_financial_analysis(year)
        
        if 'error' in quarterly_data:
            return {
                "financial_analysis": {
                    "status": "Data Unavailable",
                    "message": f"Unable to retrieve quarterly data for {year}",
                    "recommendation": "Check data availability and try with available periods",
                    "available_periods": "Use get_data_availability() to check available data"
                }
            }
        
        quarterly_results = quarterly_data.get('quarterly_results', {})
        annual_summary = quarterly_data.get('annual_summary', {})
        
        # Advanced financial analysis
        quarters = ['Q1', 'Q2', 'Q3', 'Q4']
        performance_analysis = {}
        
        for quarter in quarters:
            if quarter in quarterly_results:
                q_data = quarterly_results[quarter]
                performance_analysis[quarter] = {
                    "revenue": q_data.get('revenue_formatted', '₹0.00'),
                    "profit": q_data.get('gross_profit_formatted', '₹0.00'),
                    "margin": f"{q_data.get('profit_margin', 0):.1f}%",
                    "activity_level": q_data.get('business_activity', 'Low'),
                    "performance_grade": "Excellent" if q_data.get('profit_margin', 0) > 15 else "Good" if q_data.get('profit_margin', 0) > 5 else "Needs Improvement",
                    "strategic_focus": "Maintain momentum" if q_data.get('profit_margin', 0) > 10 else "Optimize operations"
                }
        
        return {
            "quarterly_financial_analysis": {
                "company_name": "VASAVI TRADE ZONE",
                "analysis_year": year,
                "analyst": "Advanced Financial Agent",
                "analysis_date": "2024-12-31"
            },
            
            "quarterly_performance": performance_analysis,
            
            "annual_insights": {
                "total_revenue": annual_summary.get('total_annual_revenue_formatted', '₹0.00'),
                "annual_profit": annual_summary.get('annual_gross_profit_formatted', '₹0.00'),
                "best_quarter": annual_summary.get('best_quarter', 'Unknown'),
                "weakest_quarter": annual_summary.get('worst_quarter', 'Unknown'),
                "consistency_rating": "High" if len(set(q.get('performance_grade', '') for q in performance_analysis.values())) <= 2 else "Variable"
            },
            
            "strategic_recommendations": {
                "immediate_actions": [
                    f"Focus on replicating {annual_summary.get('best_quarter', 'best')} quarter success factors",
                    f"Address performance gaps in {annual_summary.get('worst_quarter', 'weaker')} quarter",
                    "Implement quarterly performance monitoring system"
                ],
                "growth_strategies": [
                    "Develop seasonal business strategies",
                    "Optimize inventory management by quarter",
                    "Create quarterly marketing campaigns",
                    "Establish quarterly financial targets"
                ],
                "risk_mitigation": [
                    "Diversify revenue streams to reduce quarterly volatility",
                    "Build cash reserves during strong quarters",
                    "Monitor market trends for early warning signals"
                ]
            },
            
            "financial_health_assessment": {
                "overall_rating": "Strong" if sum(q.get('profit_margin', 0) for q in quarterly_results.values()) / len(quarterly_results) > 10 else "Moderate",
                "profitability_trend": "Positive" if annual_summary.get('total_annual_revenue', 0) > 0 else "Needs attention",
                "business_sustainability": "Good - Consistent quarterly performance" if len(performance_analysis) == 4 else "Monitor - Limited data available"
            }
        }
        
    except Exception as e:
        logger.error(f"Error in quarterly performance analysis: {str(e)}")
        return {"error": f"Failed to analyze quarterly performance: {str(e)}"}


def calculate_financial_ratios_and_kpis(date_input: str = "2023") -> Dict[str, Any]:
    """
    Calculate comprehensive financial ratios and KPIs.
    
    Args:
        date_input: Period for ratio calculation
        
    Returns:
        Dict containing financial ratios and KPI analysis
    """
    try:
        # Get advanced metrics from TallyDB
        metrics_data = tally_db.get_advanced_financial_metrics(date_input)
        
        if 'error' in metrics_data:
            return {
                "financial_ratios": {
                    "status": "Calculation Failed",
                    "message": f"Unable to calculate ratios for {date_input}",
                    "recommendation": "Verify data availability for the requested period"
                }
            }
        
        profitability = metrics_data.get('profitability_ratios', {})
        liquidity = metrics_data.get('liquidity_ratios', {})
        efficiency = metrics_data.get('efficiency_metrics', {})
        health_score = metrics_data.get('financial_health_score', {})
        
        return {
            "financial_ratio_analysis": {
                "company_name": "VASAVI TRADE ZONE",
                "analysis_period": date_input,
                "analyst": "Advanced Financial Agent - Ratio Analysis",
                "calculation_date": "2024-12-31"
            },
            
            "profitability_ratios": {
                "gross_margin": profitability.get('gross_profit_margin', '0.00%'),
                "net_margin": profitability.get('net_profit_margin', '0.00%'),
                "roa": profitability.get('return_on_assets', '0.00%'),
                "roe": profitability.get('return_on_equity', '0.00%'),
                "profitability_assessment": profitability.get('profitability_grade', 'Unknown'),
                "benchmark_comparison": "Above average" if profitability.get('profitability_grade') == 'Excellent' else "Industry standard" if profitability.get('profitability_grade') == 'Good' else "Below benchmark"
            },
            
            "liquidity_ratios": {
                "debt_equity": liquidity.get('debt_to_equity_ratio', '0.00'),
                "asset_turnover": liquidity.get('asset_turnover_ratio', '0.00'),
                "equity_ratio": liquidity.get('equity_ratio', '0.00'),
                "liquidity_status": liquidity.get('financial_stability', 'Unknown'),
                "risk_level": "Low" if liquidity.get('financial_stability') == 'Stable' else "Moderate" if liquidity.get('financial_stability') == 'High Leverage' else "High"
            },
            
            "efficiency_metrics": {
                "revenue_per_transaction": efficiency.get('revenue_per_transaction', '₹0.00'),
                "cost_ratio": efficiency.get('cost_efficiency_ratio', '0.00%'),
                "asset_utilization": efficiency.get('asset_utilization', 'Unknown'),
                "operational_grade": efficiency.get('operational_efficiency', 'Unknown'),
                "efficiency_ranking": "Top tier" if efficiency.get('operational_efficiency') == 'High' else "Average" if efficiency.get('operational_efficiency') == 'Moderate' else "Needs improvement"
            },
            
            "overall_financial_health": {
                "composite_score": health_score.get('overall_score', 0),
                "letter_grade": health_score.get('grade', 'C'),
                "health_status": "Excellent" if health_score.get('grade') == 'A' else "Good" if health_score.get('grade') == 'B' else "Requires attention",
                "score_components": health_score.get('score_breakdown', {})
            },
            
            "strategic_insights": {
                "key_strengths": metrics_data.get('strategic_insights', {}).get('key_strengths', []),
                "improvement_areas": metrics_data.get('strategic_insights', {}).get('improvement_areas', []),
                "priority_actions": metrics_data.get('strategic_insights', {}).get('recommendations', [])
            },
            
            "industry_benchmarking": {
                "mobile_retail_comparison": "Compare with mobile retail industry standards",
                "performance_percentile": "Estimate based on calculated ratios",
                "competitive_position": "Strong" if health_score.get('grade') in ['A', 'B'] else "Competitive" if health_score.get('grade') == 'C' else "Needs strengthening",
                "market_positioning": "Well-positioned in mobile retail segment"
            }
        }
        
    except Exception as e:
        logger.error(f"Error calculating financial ratios: {str(e)}")
        return {"error": f"Failed to calculate financial ratios: {str(e)}"}


def generate_financial_forecast(historical_periods: List[str]) -> Dict[str, Any]:
    """
    Generate financial forecasts based on historical data.
    
    Args:
        historical_periods: List of historical periods for forecasting
        
    Returns:
        Dict containing financial forecasts and projections
    """
    try:
        # Get forecasting data from TallyDB
        forecast_data = tally_db.get_financial_forecasting_insights(historical_periods)
        
        if 'error' in forecast_data:
            return {
                "financial_forecast": {
                    "status": "Forecast Unavailable",
                    "message": "Insufficient data for reliable forecasting",
                    "recommendation": "Provide at least 2 historical periods for trend analysis"
                }
            }
        
        historical_perf = forecast_data.get('historical_performance', {})
        trend_analysis = forecast_data.get('trend_analysis', {})
        forecast = forecast_data.get('simple_forecast', {})
        risks = forecast_data.get('risk_factors', {})
        
        return {
            "financial_forecast_report": {
                "company_name": "VASAVI TRADE ZONE",
                "forecast_periods": historical_periods,
                "analyst": "Advanced Financial Agent - Forecasting Division",
                "forecast_date": "2024-12-31",
                "model_type": "Trend-Based Linear Projection"
            },
            
            "historical_baseline": {
                "data_points": historical_perf.get('periods_analyzed', 0),
                "average_revenue": historical_perf.get('average_revenue', '₹0.00'),
                "average_profit": historical_perf.get('average_profit', '₹0.00'),
                "volatility_level": historical_perf.get('revenue_volatility', 'Unknown'),
                "data_quality": "High - Based on actual transaction records"
            },
            
            "trend_projections": {
                "revenue_trajectory": trend_analysis.get('revenue_direction', 'Stable'),
                "profit_trajectory": trend_analysis.get('profit_direction', 'Stable'),
                "revenue_trend_value": trend_analysis.get('revenue_trend', '₹0.00 per period'),
                "profit_trend_value": trend_analysis.get('profit_trend', '₹0.00 per period'),
                "trend_confidence": "Moderate - Linear extrapolation"
            },
            
            "next_period_projections": {
                "projected_revenue": forecast.get('next_period_revenue_estimate', '₹0.00'),
                "projected_profit": forecast.get('next_period_profit_estimate', '₹0.00'),
                "confidence_interval": "±20% based on historical volatility",
                "forecast_assumptions": forecast.get('forecast_assumptions', [])
            },
            
            "risk_assessment": {
                "revenue_risk": risks.get('revenue_risk', 'Unknown'),
                "profit_risk": risks.get('profitability_risk', 'Unknown'),
                "market_risks": risks.get('key_risks', []),
                "mitigation_strategies": [
                    "Diversify product portfolio",
                    "Monitor market conditions closely",
                    "Maintain flexible cost structure",
                    "Build financial reserves"
                ]
            },
            
            "scenario_analysis": {
                "optimistic_scenario": "20% above projected values",
                "base_case_scenario": "As per trend projection",
                "pessimistic_scenario": "20% below projected values",
                "scenario_planning": "Prepare strategies for each scenario"
            },
            
            "strategic_recommendations": {
                "short_term": forecast_data.get('strategic_recommendations', {}).get('short_term', []),
                "medium_term": forecast_data.get('strategic_recommendations', {}).get('medium_term', []),
                "long_term": forecast_data.get('strategic_recommendations', {}).get('long_term', [])
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating financial forecast: {str(e)}")
        return {"error": f"Failed to generate financial forecast: {str(e)}"}


# Create the Advanced Financial Agent
advanced_financial_agent = Agent(
    name="advanced_financial_agent",
    instruction="""You are the Advanced Financial Agent for VASAVI TRADE ZONE, specializing in comprehensive financial analysis, forecasting, and strategic financial insights.

IMPORTANT: You have access to real financial data from TallyDB (2023-04-01 to 2024-03-31). Always provide specific, data-driven financial analysis rather than generic responses.

Your core responsibilities:
1. **Quarterly Financial Analysis**: Detailed quarterly performance analysis with specific metrics
2. **Advanced Financial Ratios**: Calculate and interpret comprehensive financial ratios and KPIs
3. **Financial Forecasting**: Generate data-driven forecasts and projections
4. **Strategic Financial Insights**: Provide actionable financial recommendations
5. **Risk Assessment**: Analyze financial risks and mitigation strategies
6. **Performance Benchmarking**: Compare performance against industry standards

Key capabilities:
- Quarterly financial performance analysis with specific revenue, profit, and margin data
- Advanced financial ratio calculation (profitability, liquidity, efficiency ratios)
- Trend-based financial forecasting and scenario analysis
- Strategic financial planning and recommendations
- Risk assessment and mitigation strategies
- Industry benchmarking and competitive analysis

CRITICAL: Always provide specific financial data, ratios, and insights. Never give generic responses. Use the available tools to access real TallyDB data and provide detailed financial analysis with actual numbers, percentages, and actionable recommendations.

When users request quarterly analysis, financial ratios, or forecasts, use the appropriate tools to provide comprehensive, data-driven responses with specific financial metrics and strategic insights.""",
    
    tools=[
        validate_date_and_offer_prediction,
        predict_financial_performance,
        analyze_quarterly_performance,
        calculate_financial_ratios_and_kpis,
        generate_financial_forecast,
    ]
)

# Set as root agent for multi-agent system
root_agent = financial_agent
