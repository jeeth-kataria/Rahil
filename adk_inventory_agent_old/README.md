# ADK Inventory Management Agent

A comprehensive inventory management agent built with Google's Agent Development Kit (ADK). This agent provides 4-tier analytics capabilities: Descriptive, Diagnostic, Predictive, and Prescriptive analytics for inventory optimization.

## Features

### 🔍 Descriptive Analytics (Tier 1)
- **Inventory Summary Reports**: Comprehensive overview of current inventory status
- **Item Details**: Detailed information for specific inventory items
- **Stock Status Monitoring**: Real-time tracking of stock levels and alerts

### 🔧 Diagnostic Analytics (Tier 2)
- **Stockout Root Cause Analysis**: Identify why items go out of stock
- **Performance Analysis**: Analyze inventory turnover and efficiency
- **Supplier Performance**: Evaluate supplier reliability and lead times

### 📈 Predictive Analytics (Tier 3)
- **Demand Forecasting**: Predict future demand patterns with confidence intervals
- **Stockout Risk Prediction**: Anticipate potential stockout situations
- **Inventory Level Forecasting**: Project future inventory needs

### 💡 Prescriptive Analytics (Tier 4)
- **Reorder Strategy Optimization**: Generate optimal reorder points and quantities
- **Safety Stock Optimization**: Calculate optimal safety stock levels
- **Action Recommendations**: Provide specific, actionable recommendations

## Quick Start

### Prerequisites

1. **Python 3.10+** installed on your system
2. **Google Cloud Project** with Vertex AI API enabled
3. **Google Cloud CLI** installed and authenticated

### Installation

1. **Clone/Download** this agent directory
2. **Navigate** to the agent directory:
   ```bash
   cd adk_inventory_agent
   ```

3. **Create and activate** a virtual environment:
   ```bash
   python -m venv .venv
   
   # Activate (choose your platform)
   # macOS/Linux:
   source .venv/bin/activate
   
   # Windows CMD:
   .venv\Scripts\activate.bat
   
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment**:
   - Edit `.env` file with your Google Cloud project details:
   ```env
   GOOGLE_CLOUD_PROJECT="your-actual-project-id"
   GOOGLE_CLOUD_LOCATION="us-central1"
   GOOGLE_GENAI_USE_VERTEXAI="True"
   ```

6. **Set up Google Cloud authentication**:
   ```bash
   gcloud auth application-default login
   ```

### Running the Agent

1. **Start the ADK Web UI**:
   ```bash
   adk web
   ```

2. **Open your browser** to `http://localhost:8000` or `http://127.0.0.1:8000`

3. **Select** `adk_inventory_agent` from the available agents

4. **Start chatting** with your inventory agent!

## Example Prompts

Try these prompts to explore the agent's capabilities:

### Descriptive Analytics
- "Generate an inventory summary for the last 30 days"
- "Show me details for item ITEM_001"
- "What items are currently below their reorder point?"

### Diagnostic Analytics
- "Analyze the root cause of stockouts for ITEM_042"
- "Why did ITEM_015 go out of stock?"
- "What are the main causes of inventory issues in Electronics category?"

### Predictive Analytics
- "Forecast demand for ITEM_023 for the next 30 days"
- "Which items are at risk of stockout in the next 2 weeks?"
- "Predict inventory levels for top-selling items"

### Prescriptive Analytics
- "Recommend an optimal reorder strategy for ITEM_056"
- "What should be the safety stock level for ITEM_078 with 95% service level?"
- "Provide action recommendations for improving inventory turnover"

## Architecture

```
adk_inventory_agent/
├── __init__.py              # Package initialization
├── agent.py                 # Main ADK agent implementation
├── .env                     # Environment configuration
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── analytics/              # Analytics backend
│   ├── __init__.py
│   └── backend.py          # Mock analytics backend
├── config/                 # Configuration management
│   ├── __init__.py
│   └── settings.py         # Agent settings
└── utils/                  # Utility functions
    ├── __init__.py
    └── data_helpers.py     # Data processing utilities
```

## Customization

### Adding Real Data Sources

The agent currently uses mock data for demonstration. To connect to real data sources:

1. **Modify `analytics/backend.py`**:
   - Replace `MockAnalyticsBackend` with real database connections
   - Update data fetching methods to query actual systems
   - Add authentication and connection management

2. **Update data models**:
   - Modify the sample data structures to match your schema
   - Add additional fields as needed for your business

3. **Configure connections**:
   - Add database credentials to `.env`
   - Update `config/settings.py` with connection parameters

### Extending Analytics Capabilities

To add new analytics functions:

1. **Add new tools** to the agent in `agent.py`
2. **Implement backend logic** in `analytics/backend.py`
3. **Add utility functions** in `utils/data_helpers.py` if needed
4. **Update documentation** and example prompts

### Advanced Configuration

Edit `config/settings.py` to modify:
- Default forecast periods
- Service level targets
- Alert thresholds
- Model parameters

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   ```bash
   gcloud auth application-default login
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Module Import Errors**:
   - Ensure virtual environment is activated
   - Reinstall requirements: `pip install -r requirements.txt`

3. **Agent Not Loading**:
   - Check `.env` configuration
   - Verify Google Cloud project settings
   - Check logs for specific error messages

4. **Data Issues**:
   - Mock data is generated randomly - restart if needed
   - Check date formats (YYYY-MM-DD required)
   - Verify item IDs exist (ITEM_001 to ITEM_100)

### Getting Help

- Check the [ADK Documentation](https://google.github.io/adk-docs/)
- Review [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- Examine agent logs for detailed error information

## Development

### Running Tests

```bash
# Install development dependencies
pip install pytest pytest-cov

# Run tests (when implemented)
pytest tests/
```

### Code Structure

The agent follows these principles:
- **Separation of Concerns**: Analytics logic separate from agent interface
- **Modular Design**: Each analytics tier in separate methods
- **Error Handling**: Comprehensive try-catch blocks with logging
- **Type Safety**: Full type hints for better development experience
- **Documentation**: Detailed docstrings for all methods

### Contributing

1. Follow the existing code style and patterns
2. Add comprehensive error handling
3. Include detailed docstrings
4. Test with various data scenarios
5. Update documentation as needed

## License

This project is provided as-is for educational and development purposes. Modify and adapt as needed for your specific use case.

## Acknowledgments

Built with Google's Agent Development Kit (ADK) - a powerful framework for creating intelligent agents with advanced AI capabilities.
