# 🚀 Quick Start Guide

Get your Sentiment Analysis Dashboard up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

### 1. Navigate to Project Directory

```bash
cd sentiment-analysis-triage
```

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** This will download ~2GB of dependencies including the BERT model. First-time installation may take 5-10 minutes.

### 4. Download NLTK Data (Required for VADER)

```bash
python -c "import nltk; nltk.download('vader_lexicon')"
```

## Running the Application

### Start the Dashboard

```bash
streamlit run app.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

## Quick Test with Sample Data

1. **Launch the app** using the command above
2. In the sidebar, select **"Use Sample Data"** from the data source dropdown
3. Click the **"🚀 Analyze Feedback"** button
4. Wait 10-30 seconds for analysis to complete
5. Explore the results in the three tabs:
   - **Data & Analysis**: View raw data and analysis controls
   - **Visualizations**: Interactive charts and graphs
   - **Detailed Results**: Filter and export analyzed feedback

## What You'll See

### Summary Metrics
- Total feedback count
- Average confidence score
- Average priority score
- High priority feedback count

### Visualizations
- **Sentiment Distribution**: Pie chart showing positive/negative/neutral breakdown
- **Priority Levels**: Bar chart of high/medium/low priority feedback
- **Confidence Distribution**: Histogram of model confidence scores
- **Priority Score Distribution**: Histogram of calculated priority scores

### Detailed Results
- Expandable feedback cards with full analysis
- Filters for sentiment and priority
- Search functionality
- CSV export capability

## Testing with Your Own Data

### CSV/Excel Upload

1. Prepare a CSV or Excel file with a column named `feedback_text`
2. Optional columns: `feedback_id`, `timestamp`, `category`
3. Select **"CSV/Excel Upload"** in the sidebar
4. Upload your file
5. Click **"🚀 Analyze Feedback"**

### Example CSV Format

```csv
feedback_id,feedback_text,timestamp,category
1,"Great product! Very satisfied with the quality.",2024-01-15,Product
2,"Terrible customer service. Very disappointed.",2024-01-16,Service
3,"Average experience. Nothing special.",2024-01-17,General
```

## Configuration

### Adjust Analysis Settings

In the sidebar, you can customize:

- **Use Transformer Model**: Toggle between BERT (accurate) and VADER (fast)
- **Batch Size**: Adjust processing speed (10-100)

### Modify Priority Weights

Edit `config.yaml` to customize:

```yaml
priority:
  sentiment_weights:
    negative: 9
    neutral: 5
    positive: 2
  confidence_weight: 0.3
  urgent_keyword_weight: 20
  text_length_weight: 0.1
```

## Troubleshooting

### Issue: "Module not found" errors

**Solution:** Ensure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

### Issue: NLTK data not found

**Solution:** Download VADER lexicon:
```bash
python -c "import nltk; nltk.download('vader_lexicon')"
```

### Issue: Out of memory during analysis

**Solution:** Reduce batch size in sidebar settings (try 10-20)

### Issue: Slow first-time analysis

**Solution:** First run downloads the BERT model (~500MB). Subsequent runs are faster.

## Performance Tips

1. **Use VADER for large datasets** (1000+ feedbacks) - Toggle off "Use Transformer Model"
2. **Adjust batch size** based on your system RAM:
   - 4GB RAM: batch_size = 10
   - 8GB RAM: batch_size = 32
   - 16GB+ RAM: batch_size = 64
3. **Filter data before analysis** to focus on specific time periods or categories

## Next Steps

### Connect to Live Data Sources

Once you've tested with sample data, explore connecting to:

- **REST APIs**: Configure in sidebar under "REST API" option
- **SQL Databases**: PostgreSQL, MySQL, or SQLite
- **MongoDB**: NoSQL document database

See the full [README.md](README.md) for detailed configuration instructions.

### Customize the Dashboard

- Modify `config.yaml` for priority scoring rules
- Edit `app.py` to add custom visualizations
- Extend connectors for additional data sources

## Sample Data Details

The included `data/sample_feedback.csv` contains:
- **50 feedback entries** across various sentiments
- **Mix of positive, negative, and neutral** feedback
- **Different text lengths** and complexity levels
- **Urgent keywords** for priority testing

## Support

For issues or questions:
1. Check the [README.md](README.md) for detailed documentation
2. Review error messages in the Streamlit interface
3. Verify all dependencies are correctly installed

## Quick Reference Commands

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('vader_lexicon')"

# Run application
streamlit run app.py

# Deactivate virtual environment
deactivate
```

---

**Ready to analyze feedback!** 🎉

Start with the sample data, then upload your own CSV files or connect to your data sources.