# Sentiment Analysis for User Feedback Triage

A comprehensive Python-based Streamlit dashboard for analyzing sentiment in survey responses and feedback forms. The system supports multiple data sources (CSV/Excel, REST API, SQL databases, MongoDB), classifies feedback as positive/negative/neutral, assigns priority scores, and provides visual analytics for efficient triage.

## Features

- **Multi-Source Data Integration**: Support for CSV/Excel files, REST APIs, SQL databases (PostgreSQL, MySQL, SQLite), and MongoDB
- **Advanced Sentiment Analysis**: Uses BERT-based transformer models with VADER fallback
- **Intelligent Priority Scoring**: Multi-factor algorithm considering sentiment, confidence, keywords, and text length
- **Interactive Dashboard**: Real-time analysis with visual analytics and filtering
- **Export Capabilities**: Download analyzed results in CSV format
- **Secure Credential Management**: Environment variable support for sensitive data

## Project Structure

```
sentiment-analysis-triage/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── config.yaml                     # Configuration settings
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore file
├── README.md                       # This file
├── modules/
│   ├── __init__.py
│   ├── sentiment_analyzer.py      # Sentiment analysis logic
│   ├── priority_scorer.py         # Priority calculation
│   └── data_processor.py          # Data cleaning & preprocessing
├── connectors/
│   ├── __init__.py
│   ├── base_connector.py          # Abstract base class
│   ├── csv_connector.py           # CSV/Excel handler
│   ├── api_connector.py           # REST API integration
│   ├── sql_connector.py           # SQL database integration
│   └── mongodb_connector.py       # MongoDB integration
├── utils/
│   ├── __init__.py
│   ├── data_validator.py          # Data validation utilities
│   ├── credential_manager.py      # Secure credential handling
│   └── export_handler.py          # Export functionality
├── data/
│   └── sample_feedback.csv        # Sample data for testing
└── assets/
    └── styles.css                 # Custom CSS styling
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) Virtual environment tool (venv, conda, etc.)

### Step 1: Clone or Download the Project

```bash
cd sentiment-analysis-triage
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Using venv
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- streamlit
- pandas
- transformers
- torch
- nltk
- plotly
- requests
- sqlalchemy
- pymongo
- and more...

### Step 4: Download NLTK Data

The first time you run the application, NLTK will automatically download the required VADER lexicon. Alternatively, you can download it manually:

```python
import nltk
nltk.download('vader_lexicon')
```

### Step 5: Configure Environment Variables (Optional)

If you plan to use API or database connections:

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your actual credentials
# NEVER commit .env to version control!
```

## Configuration

Edit `config.yaml` to customize:

- **Model Settings**: Choose sentiment analysis model
- **Priority Weights**: Adjust scoring algorithm
- **Urgent Keywords**: Define keywords that boost priority
- **Data Source Settings**: Configure timeouts, pool sizes, etc.
- **Dashboard Appearance**: Customize colors, layout, etc.

## Usage

### Running the Application

```bash
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

### Data Source Options

#### 1. CSV/Excel File Upload

**Supported Formats**: `.csv`, `.xlsx`, `.xls`

**Expected Columns**:
- `feedback_text` (required): The feedback content
- `feedback_id` (optional): Unique identifier
- `timestamp` (optional): When feedback was submitted
- `user_id` (optional): User identifier
- `category` (optional): Feedback category

**Example CSV**:
```csv
feedback_id,feedback_text,timestamp,user_id,category
1,"Great product!",2024-01-15 10:30:00,user_001,product
2,"Terrible experience",2024-01-15 11:45:00,user_002,support
```

**Steps**:
1. Select "CSV/Excel Upload" from data source dropdown
2. Click "Browse files" and select your file
3. Click "Analyze Feedback"

#### 2. REST API Connection

**Configuration**:
```python
{
    "endpoint": "https://api.example.com/feedback",
    "auth_type": "bearer",  # none, api_key, bearer, basic
    "token": "your_token_here",
    "params": {
        "limit": 100,
        "status": "pending"
    }
}
```

**Authentication Types**:
- **None**: No authentication required
- **API Key**: Add `X-API-Key` header
- **Bearer Token**: Add `Authorization: Bearer {token}` header
- **Basic Auth**: Username and password

**Steps**:
1. Select "REST API" from data source dropdown
2. Enter API endpoint URL
3. Select authentication type
4. Provide credentials
5. (Optional) Add query parameters
6. Click "Test Connection" to verify
7. Click "Fetch Data"

#### 3. SQL Database Connection

**Supported Databases**:
- PostgreSQL
- MySQL
- SQLite

**Connection String Format**:
```
postgresql://username:password@host:port/database
mysql://username:password@host:port/database
sqlite:///path/to/database.db
```

**Example Query**:
```sql
SELECT 
    feedback_id,
    feedback_text,
    created_at as timestamp,
    user_id,
    category
FROM feedback
WHERE status = 'pending'
ORDER BY created_at DESC
LIMIT 1000
```

**Steps**:
1. Select "SQL Database" from data source dropdown
2. Enter connection string
3. Write or paste your SQL query
4. Click "Test Connection"
5. Click "Execute Query"

#### 4. MongoDB Connection

**Connection String Format**:
```
mongodb://username:password@host:port/database
mongodb+srv://username:password@cluster.mongodb.net/database
```

**Query Example**:
```json
{
    "collection": "feedback",
    "filter": {"status": "pending"},
    "projection": {
        "feedback_id": 1,
        "text": 1,
        "timestamp": 1,
        "user_id": 1
    },
    "limit": 1000
}
```

**Steps**:
1. Select "MongoDB" from data source dropdown
2. Enter connection string
3. Enter database name
4. Enter collection name
5. (Optional) Add filter query
6. Click "Test Connection"
7. Click "Fetch Data"

## Understanding the Results

### Sentiment Classification

- **Positive**: Feedback expressing satisfaction, praise, or positive emotions
- **Negative**: Feedback expressing dissatisfaction, complaints, or negative emotions
- **Neutral**: Feedback that is neither clearly positive nor negative

### Priority Scoring

Priority scores range from 0-10 and are calculated based on:

1. **Sentiment Weight**:
   - Negative: 9 (high priority)
   - Neutral: 5 (medium priority)
   - Positive: 2 (low priority)

2. **Confidence Score**: Model's confidence in sentiment classification

3. **Urgent Keywords**: Presence of words like "urgent", "critical", "broken", etc.

4. **Text Length**: Longer, detailed feedback may indicate higher priority

**Priority Levels**:
- **High**: Score ≥ 7.0 (Requires immediate attention)
- **Medium**: Score 4.0-6.9 (Should be addressed soon)
- **Low**: Score < 4.0 (Can be handled routinely)

### Dashboard Sections

1. **Summary Statistics**:
   - Total feedback count
   - Sentiment distribution
   - Average priority score
   - Processing time

2. **Results Table**:
   - Sortable and filterable
   - Color-coded sentiment badges
   - Priority indicators
   - Full feedback text

3. **Visual Analytics**:
   - Sentiment distribution pie chart
   - Priority breakdown bar chart
   - Confidence score histogram
   - Word clouds per sentiment

4. **Filters**:
   - Filter by sentiment type
   - Filter by priority level
   - Search feedback text

## Exporting Results

1. Click "Export Results" button
2. Choose export format (CSV)
3. File will include:
   - Original feedback data
   - Sentiment classification
   - Confidence scores
   - Priority scores and levels
   - Analysis timestamp

## Troubleshooting

### Model Loading Issues

**Problem**: Transformer model fails to load

**Solutions**:
- Check internet connection (first-time download)
- Ensure sufficient disk space (models are ~250MB)
- Try using VADER fallback: Set `model.fallback: "vader"` in config.yaml

### Memory Issues

**Problem**: Out of memory errors with large datasets

**Solutions**:
- Process data in smaller batches
- Reduce `sentiment.batch_size` in config.yaml
- Use VADER instead of transformer model
- Increase system RAM or use cloud deployment

### Connection Errors

**Problem**: Cannot connect to API/Database

**Solutions**:
- Verify credentials are correct
- Check network connectivity
- Ensure firewall allows connections
- Test connection string separately
- Check if service is running

### Import Errors

**Problem**: Module not found errors

**Solutions**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# If specific package fails
pip install package_name --force-reinstall
```

## Performance Optimization

### For Large Datasets (10,000+ records)

1. **Use Batch Processing**:
   - Adjust `sentiment.batch_size` in config.yaml
   - Process in chunks of 100-500 records

2. **Enable Caching**:
   - Streamlit automatically caches model loading
   - Set appropriate `cache_ttl_minutes` in config

3. **Use GPU Acceleration** (if available):
   - Set `model.device: "cuda"` in config.yaml
   - Ensure PyTorch with CUDA support is installed

4. **Database Optimization**:
   - Add indexes on frequently queried columns
   - Use LIMIT clauses in SQL queries
   - Optimize MongoDB queries with proper indexes

## Security Best Practices

1. **Never commit credentials**:
   - Use `.env` file for sensitive data
   - Add `.env` to `.gitignore`

2. **Use environment variables**:
   ```python
   import os
   api_key = os.getenv('API_KEY')
   ```

3. **Secure database connections**:
   - Use SSL/TLS for database connections
   - Implement connection pooling
   - Use parameterized queries to prevent SQL injection

4. **API security**:
   - Rotate API keys regularly
   - Use token-based authentication
   - Implement rate limiting

## Advanced Usage

### Custom Model Training

To use a custom sentiment analysis model:

1. Train your model using Hugging Face transformers
2. Upload to Hugging Face Hub or save locally
3. Update `model.name` in config.yaml with your model path

### Extending Functionality

The modular architecture allows easy extension:

- **Add new data sources**: Create new connector class inheriting from `BaseConnector`
- **Custom priority algorithms**: Modify `priority_scorer.py`
- **Additional visualizations**: Add to dashboard using Plotly
- **New sentiment categories**: Extend sentiment analyzer

### API Integration Example

```python
from connectors.api_connector import create_api_connector

# Create connector
connector = create_api_connector(
    endpoint="https://api.example.com/feedback",
    auth_type="bearer",
    token="your_token"
)

# Fetch data
df = connector.fetch_data(
    params={"limit": 100},
    json_path="data.items"
)
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is provided as-is for educational and commercial use.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

## Changelog

### Version 1.0.0 (2024-01-18)
- Initial release
- Multi-source data integration
- BERT-based sentiment analysis
- Priority scoring system
- Interactive Streamlit dashboard
- Export functionality

## Acknowledgments

- Hugging Face for transformer models
- NLTK for VADER sentiment analyzer
- Streamlit for dashboard framework
- Plotly for visualizations

---

**Built with ❤️ for efficient feedback triage**