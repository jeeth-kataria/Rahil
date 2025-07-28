"""
Project Synapse Business Data Backend

Shared data layer for all business management agents including financial data,
sales metrics, operational data, HR information, and strategic KPIs.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SynapseBusinessData:
    """Comprehensive business data backend for Project Synapse multi-agent system."""
    
    def __init__(self):
        """Initialize the business data backend with sample enterprise data."""
        self.financial_data = self._generate_financial_data()
        self.revenue_data = self._generate_revenue_data()
        self.operational_data = self._generate_operational_data()
        self.hr_data = self._generate_hr_data()
        self.market_data = self._generate_market_data()
        self.strategic_kpis = self._generate_strategic_kpis()
        logger.info("Synapse business data backend initialized")
    
    def _generate_financial_data(self) -> Dict[str, Any]:
        """Generate comprehensive financial data."""
        np.random.seed(42)
        
        # Generate monthly financial data for 24 months
        dates = pd.date_range(start='2023-01-01', periods=24, freq='M')
        
        financial_data = {
            "cash_flow": pd.DataFrame({
                'date': dates,
                'operating_cash_flow': np.random.normal(500000, 100000, 24),
                'investing_cash_flow': np.random.normal(-200000, 50000, 24),
                'financing_cash_flow': np.random.normal(-100000, 30000, 24),
                'net_cash_flow': np.random.normal(200000, 80000, 24)
            }),
            
            "pnl": pd.DataFrame({
                'date': dates,
                'revenue': np.random.normal(2000000, 300000, 24),
                'cogs': np.random.normal(1200000, 200000, 24),
                'gross_profit': np.random.normal(800000, 150000, 24),
                'operating_expenses': np.random.normal(600000, 100000, 24),
                'ebitda': np.random.normal(200000, 80000, 24),
                'net_income': np.random.normal(150000, 60000, 24)
            }),
            
            "balance_sheet": {
                'total_assets': 15000000,
                'current_assets': 8000000,
                'fixed_assets': 7000000,
                'total_liabilities': 9000000,
                'current_liabilities': 3000000,
                'long_term_debt': 6000000,
                'shareholders_equity': 6000000,
                'cash_and_equivalents': 2000000
            },
            
            "financial_ratios": {
                'current_ratio': 2.67,
                'debt_to_equity': 1.5,
                'roe': 0.15,
                'roa': 0.08,
                'gross_margin': 0.40,
                'operating_margin': 0.10,
                'net_margin': 0.075
            }
        }
        
        return financial_data
    
    def _generate_revenue_data(self) -> Dict[str, Any]:
        """Generate comprehensive revenue and sales data."""
        np.random.seed(42)
        
        # Product lines
        products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
        regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America']
        channels = ['Direct Sales', 'Online', 'Partners', 'Retail']
        
        # Generate sales data
        sales_data = []
        for month in pd.date_range(start='2023-01-01', periods=24, freq='M'):
            for product in products:
                for region in regions:
                    for channel in channels:
                        sales_data.append({
                            'date': month,
                            'product': product,
                            'region': region,
                            'channel': channel,
                            'revenue': np.random.normal(50000, 15000),
                            'units_sold': np.random.randint(100, 1000),
                            'avg_selling_price': np.random.normal(200, 50),
                            'customer_acquisition_cost': np.random.normal(50, 15),
                            'customer_lifetime_value': np.random.normal(800, 200)
                        })
        
        revenue_data = {
            "sales_data": pd.DataFrame(sales_data),
            "customer_metrics": {
                'total_customers': 25000,
                'new_customers_monthly': 1500,
                'churn_rate': 0.05,
                'avg_customer_lifetime_value': 850,
                'customer_acquisition_cost': 52,
                'net_promoter_score': 68
            },
            "pricing_data": {
                'price_elasticity': -1.2,
                'competitive_position': 'Premium',
                'pricing_power': 'Medium',
                'discount_frequency': 0.15
            }
        }
        
        return revenue_data
    
    def _generate_operational_data(self) -> Dict[str, Any]:
        """Generate operational and supply chain data."""
        np.random.seed(42)
        
        operational_data = {
            "production_metrics": {
                'monthly_production_capacity': 10000,
                'current_utilization': 0.85,
                'quality_score': 0.96,
                'on_time_delivery': 0.92,
                'inventory_turnover': 8.5,
                'lead_time_days': 14
            },
            
            "supply_chain": {
                'supplier_count': 45,
                'supplier_reliability_score': 0.88,
                'supply_chain_risk_score': 'Medium',
                'inventory_value': 3500000,
                'stockout_frequency': 0.03
            },
            
            "process_efficiency": {
                'automation_level': 0.65,
                'process_cycle_time': 2.3,
                'defect_rate': 0.02,
                'rework_percentage': 0.05,
                'overall_equipment_effectiveness': 0.78
            },
            
            "facilities": {
                'total_facilities': 8,
                'manufacturing_sites': 3,
                'distribution_centers': 2,
                'office_locations': 3,
                'facility_utilization': 0.82
            }
        }
        
        return operational_data
    
    def _generate_hr_data(self) -> Dict[str, Any]:
        """Generate human resources and talent data."""
        np.random.seed(42)
        
        departments = ['Engineering', 'Sales', 'Marketing', 'Operations', 'Finance', 'HR', 'Customer Success']
        
        hr_data = {
            "workforce_metrics": {
                'total_employees': 450,
                'employee_turnover_rate': 0.12,
                'time_to_fill_positions': 35,
                'employee_satisfaction_score': 7.8,
                'engagement_score': 8.2,
                'absenteeism_rate': 0.03
            },
            
            "talent_pipeline": {
                'open_positions': 25,
                'candidates_in_pipeline': 150,
                'offer_acceptance_rate': 0.85,
                'internal_promotion_rate': 0.30,
                'succession_planning_coverage': 0.75
            },
            
            "compensation": {
                'avg_salary_by_level': {
                    'Entry': 65000,
                    'Mid': 95000,
                    'Senior': 135000,
                    'Lead': 165000,
                    'Executive': 250000
                },
                'total_compensation_budget': 42000000,
                'merit_increase_budget': 0.04,
                'bonus_pool': 2500000
            },
            
            "department_data": pd.DataFrame([
                {'department': dept, 
                 'headcount': np.random.randint(30, 100),
                 'avg_tenure': np.random.uniform(2.5, 6.0),
                 'performance_rating': np.random.uniform(3.5, 4.5),
                 'budget_utilization': np.random.uniform(0.85, 0.98)}
                for dept in departments
            ]),
            
            "skills_data": {
                'critical_skills_gaps': ['Data Science', 'Cloud Architecture', 'AI/ML', 'Cybersecurity'],
                'training_completion_rate': 0.87,
                'certification_coverage': 0.65,
                'learning_hours_per_employee': 40
            }
        }
        
        return hr_data
    
    def _generate_market_data(self) -> Dict[str, Any]:
        """Generate market intelligence and competitive data."""
        np.random.seed(42)
        
        market_data = {
            "market_size": {
                'total_addressable_market': 50000000000,
                'serviceable_addressable_market': 8000000000,
                'serviceable_obtainable_market': 800000000,
                'market_growth_rate': 0.12,
                'market_share': 0.025
            },
            
            "competitive_landscape": {
                'direct_competitors': 8,
                'indirect_competitors': 15,
                'competitive_position': 'Strong',
                'differentiation_score': 7.5,
                'brand_recognition': 0.35
            },
            
            "customer_insights": {
                'customer_segments': 4,
                'primary_segment_size': 0.45,
                'customer_concentration_risk': 'Low',
                'geographic_diversification': 0.75,
                'customer_stickiness': 0.82
            },
            
            "trends": [
                'Digital Transformation',
                'Sustainability Focus',
                'Remote Work Adoption',
                'AI Integration',
                'Supply Chain Resilience'
            ]
        }
        
        return market_data
    
    def _generate_strategic_kpis(self) -> Dict[str, Any]:
        """Generate strategic KPIs and performance metrics."""
        strategic_kpis = {
            "financial_kpis": {
                'revenue_growth_rate': 0.18,
                'profit_margin_trend': 'Improving',
                'cash_conversion_cycle': 45,
                'return_on_invested_capital': 0.14,
                'debt_service_coverage': 2.8
            },
            
            "operational_kpis": {
                'operational_efficiency_score': 8.2,
                'customer_satisfaction_score': 8.7,
                'innovation_index': 7.5,
                'sustainability_score': 7.8,
                'digital_maturity_score': 7.2
            },
            
            "strategic_objectives": [
                {'objective': 'Market Expansion', 'progress': 0.75, 'target_date': '2024-12-31'},
                {'objective': 'Digital Transformation', 'progress': 0.60, 'target_date': '2025-06-30'},
                {'objective': 'Operational Excellence', 'progress': 0.85, 'target_date': '2024-09-30'},
                {'objective': 'Talent Development', 'progress': 0.70, 'target_date': '2024-12-31'}
            ]
        }
        
        return strategic_kpis
    
    def get_financial_summary(self, period: str = "current") -> Dict[str, Any]:
        """Get financial summary for specified period."""
        if period == "current":
            latest_pnl = self.financial_data["pnl"].iloc[-1]
            return {
                'revenue': latest_pnl['revenue'],
                'gross_profit': latest_pnl['gross_profit'],
                'ebitda': latest_pnl['ebitda'],
                'net_income': latest_pnl['net_income'],
                'cash_position': self.financial_data["balance_sheet"]['cash_and_equivalents'],
                'key_ratios': self.financial_data["financial_ratios"]
            }
        return self.financial_data
    
    def get_revenue_metrics(self, segment: Optional[str] = None) -> Dict[str, Any]:
        """Get revenue metrics, optionally filtered by segment."""
        if segment:
            filtered_data = self.revenue_data["sales_data"][
                self.revenue_data["sales_data"]['product'] == segment
            ]
            return {
                'segment_revenue': filtered_data['revenue'].sum(),
                'segment_units': filtered_data['units_sold'].sum(),
                'segment_data': filtered_data.to_dict('records')
            }
        return self.revenue_data
    
    def get_operational_status(self) -> Dict[str, Any]:
        """Get current operational status and metrics."""
        return self.operational_data
    
    def get_hr_insights(self) -> Dict[str, Any]:
        """Get HR and talent management insights."""
        return self.hr_data
    
    def get_market_intelligence(self) -> Dict[str, Any]:
        """Get market data and competitive intelligence."""
        return self.market_data
    
    def get_strategic_dashboard(self) -> Dict[str, Any]:
        """Get strategic KPIs and performance dashboard."""
        return self.strategic_kpis


# Global business data instance
business_data = SynapseBusinessData()
