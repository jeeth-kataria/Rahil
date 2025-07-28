# Rahil - Multi-Agent Business Intelligence System

A sophisticated multi-agent system built with Google's Agent Development Kit (ADK) for comprehensive business intelligence and financial analysis.

## 🎯 Overview

Rahil is an advanced business intelligence platform that uses multiple specialized AI agents to provide comprehensive insights into business operations, financial performance, and strategic planning. The system integrates with TallyDB for real-time business data access and provides intelligent analysis across multiple domains.

## 🏗️ Architecture

### Multi-Agent System
- **Orchestrator Agent**: Central coordinator that routes queries and manages multi-agent workflows
- **Financial Agent**: Specialized in financial analysis, P&L statements, cash flow, and forecasting
- **TallyDB Agent**: Direct interface to TallyDB for real-time business data access
- **Business Intelligence Agent**: Strategic analysis, expansion planning, and customer insights
- **CEO Agent**: Executive-level strategic planning and leadership decisions
- **Inventory Agent**: Supply chain management and inventory optimization

### Key Components
- **TallyDB Integration**: Direct connection to TallyDB SQLite database for real business data
- **Intelligent Data System**: Advanced query processing with fallback mechanisms
- **Multi-Agent Workflows**: Coordinated analysis across multiple specialized agents
- **Real-World Business Scenarios**: Handles complex business queries and decision-making

## 🚀 Features

### Financial Analysis
- **P&L Statement Generation**: Comprehensive profit and loss analysis
- **Cash Flow Analysis**: Real-time cash position and flow projections
- **Financial Ratios**: Key performance indicators and financial health metrics
- **Date Validation**: Smart handling of historical and future date queries
- **Predictive Analytics**: Financial forecasting based on historical trends

### Business Intelligence
- **Client Verification**: Definitive customer relationship verification
- **Expansion Assessment**: Financial capacity analysis for business growth
- **Customer Analysis**: Payment patterns and relationship insights
- **Seasonality Analysis**: Business trend identification and planning
- **Strategic Planning**: Executive-level business strategy recommendations

### Real-World Scenarios
- Supplier payment planning and cash flow management
- Customer credit term negotiations
- Bank loan applications and financial statement preparation
- Investment decision support
- Tax filing and compliance reporting

## 🛠️ Technology Stack

- **Framework**: Google Agent Development Kit (ADK)
- **Language**: Python 3.12+
- **Database**: TallyDB (SQLite)
- **AI Model**: Google Gemini 2.0 Flash
- **Architecture**: Multi-agent system with specialized domains

## 📁 Project Structure

```
rahil/
├── orchestrator_agent/          # Central coordination agent
├── financial_agent/             # Financial analysis specialist
├── tallydb_agent/              # Database interface agent
├── business_intelligence_agent/ # Strategic analysis agent
├── ceo_agent/                  # Executive decision agent
├── inventory_agent/            # Supply chain specialist
├── tallydb_connection.py       # Database connection utilities
├── tallydb.db                  # Business database (SQLite)
└── README.md                   # This file
```

## 🔧 Setup and Installation

### Prerequisites
- Python 3.12 or higher
- Google ADK installed
- TallyDB database file
- Google API key for Gemini

### Installation
1. Clone the repository:
   ```bash
   git clone git@github.com:jeeth-kataria/Rahil.git
   cd Rahil
   ```

2. Set up environment variables:
   ```bash
   # Add to each agent's .env file
   GOOGLE_GENAI_USE_VERTEXAI=FALSE
   GOOGLE_API_KEY=your_api_key_here
   ```

3. Start the system:
   ```bash
   adk web
   ```

4. Access the system at `http://localhost:8000`

## 💡 Usage Examples

### Financial Queries
- "Generate P&L statement for 2023"
- "Do I have enough cash to pay suppliers next week?"
- "Show me financial data for 2030" (triggers prediction offer)
- "Calculate financial ratios for loan application"

### Business Intelligence
- "Is AR MOBILES a client?"
- "What's my expansion capacity?"
- "Analyze customer payment patterns"
- "Show business seasonality trends"

### Strategic Planning
- "Should I take a loan? What's my debt-to-equity ratio?"
- "Customer is asking for extended payment terms, what's my cash situation?"
- "Bank is asking for financial statements, show me P&L"

## 🎯 Key Capabilities

### Intelligent Data Processing
- **Fallback Mechanisms**: Multiple layers of data access and processing
- **Error Resilience**: Graceful handling of API limitations and data issues
- **Real-Time Analysis**: Direct database queries for immediate insights
- **Context Awareness**: Multi-turn conversation support with context retention

### Business Decision Support
- **Definitive Answers**: Clear YES/NO responses for business decisions
- **Evidence-Based**: All responses backed by real transaction data
- **Strategic Insights**: Executive-level analysis and recommendations
- **Actionable Intelligence**: Specific next steps and recommendations

## 🔒 Security and Reliability

- **Direct Database Access**: Bypasses API limitations for critical queries
- **Data Validation**: Comprehensive input validation and sanitization
- **Error Handling**: Robust error management with meaningful fallbacks
- **Audit Trail**: Complete logging of all agent interactions and decisions

## 🤝 Contributing

This is a specialized business intelligence system. For contributions or modifications, please ensure:
- Maintain agent architecture principles
- Preserve data integrity and security
- Test with real business scenarios
- Document any new capabilities or changes

## 📄 License

Private business intelligence system. All rights reserved.

## 📞 Support

For technical support or business inquiries, please contact the development team.

---

**Rahil - Intelligent Business Decision Support System**
*Powered by Multi-Agent AI Architecture*
