"""
Sentiment Analysis for User Feedback Triage
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import yaml
from datetime import datetime
import time

# Import modules
from modules.sentiment_analyzer import create_sentiment_analyzer
from modules.priority_scorer import create_priority_scorer
from modules.data_processor import create_data_processor
from modules.visualizations import create_visualizer
from connectors.csv_connector import create_csv_connector
from utils.export_handler import create_export_handler

# Page configuration
st.set_page_config(
    page_title="Sentiment Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load configuration
@st.cache_resource
def load_config():
    """Load configuration from YAML file"""
    try:
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        st.error(f"Error loading config: {e}")
        return {}

config = load_config()

# Initialize components
@st.cache_resource
def initialize_analyzer():
    """Initialize sentiment analyzer"""
    model_name = config.get('model', {}).get('name', 'distilbert-base-uncased-finetuned-sst-2-english')
    analyzer = create_sentiment_analyzer(model_name=model_name)
    return analyzer

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .sentiment-positive {
        color: #28a745;
        font-weight: bold;
    }
    .sentiment-negative {
        color: #dc3545;
        font-weight: bold;
    }
    .sentiment-neutral {
        color: #6c757d;
        font-weight: bold;
    }
    .priority-high {
        background-color: #ff4444;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-weight: bold;
    }
    .priority-medium {
        background-color: #ffaa00;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-weight: bold;
    }
    .priority-low {
        background-color: #44ff44;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<div class="main-header">📊 Sentiment Analysis for User Feedback Triage</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Data source selection
    data_source = st.selectbox(
        "Select Data Source",
        ["CSV/Excel Upload", "Use Sample Data", "REST API", "SQL Database", "MongoDB"],
        help="Choose how to load feedback data"
    )
    
    st.divider()
    
    # Analysis settings
    st.subheader("Analysis Settings")
    
    use_transformer = st.checkbox(
        "Use Transformer Model",
        value=True,
        help="Use BERT model (slower but more accurate) or VADER (faster)"
    )
    
    batch_size = st.slider(
        "Batch Size",
        min_value=10,
        max_value=100,
        value=32,
        help="Number of feedbacks to process at once"
    )
    
    st.divider()
    
    # About
    st.subheader("ℹ️ About")
    st.info("""
    This dashboard analyzes sentiment in user feedback and assigns priority scores for efficient triage.
    
    **Features:**
    - Multi-source data integration
    - BERT-based sentiment analysis
    - Intelligent priority scoring
    - Interactive visualizations
    """)

# Main content area
tab1, tab2, tab3 = st.tabs(["📥 Data & Analysis", "📊 Visualizations", "📋 Detailed Results"])

# Initialize session state
if 'analyzed_data' not in st.session_state:
    st.session_state.analyzed_data = None
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

# Tab 1: Data & Analysis
with tab1:
    st.header("Data Input & Analysis")
    
    df = None
    
    # Handle different data sources
    if data_source == "CSV/Excel Upload":
        uploaded_file = st.file_uploader(
            "Upload your feedback file",
            type=['csv', 'xlsx', 'xls'],
            help="File should contain a 'feedback_text' column"
        )
        
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                st.success(f"✅ Loaded {len(df)} feedback entries")
            except Exception as e:
                st.error(f"Error loading file: {e}")
    
    elif data_source == "Use Sample Data":
        try:
            df = pd.read_csv('data/sample_feedback.csv')
            st.success(f"✅ Loaded {len(df)} sample feedback entries")
        except Exception as e:
            st.error(f"Error loading sample data: {e}")
    
    elif data_source == "REST API":
        st.info("🚧 API connector - Configure your API endpoint")
        with st.expander("API Configuration"):
            api_endpoint = st.text_input("API Endpoint URL")
            auth_type = st.selectbox("Authentication", ["None", "API Key", "Bearer Token"])
            if auth_type != "None":
                api_key = st.text_input("API Key/Token", type="password")
            if st.button("Fetch Data"):
                st.warning("API integration requires configuration")
    
    elif data_source == "SQL Database":
        st.info("🚧 SQL connector - Configure your database connection")
        with st.expander("Database Configuration"):
            db_type = st.selectbox("Database Type", ["PostgreSQL", "MySQL", "SQLite"])
            connection_string = st.text_input("Connection String", type="password")
            query = st.text_area("SQL Query")
            if st.button("Execute Query"):
                st.warning("Database integration requires configuration")
    
    elif data_source == "MongoDB":
        st.info("🚧 MongoDB connector - Configure your MongoDB connection")
        with st.expander("MongoDB Configuration"):
            mongo_uri = st.text_input("MongoDB URI", type="password")
            database = st.text_input("Database Name")
            collection = st.text_input("Collection Name")
            if st.button("Fetch Data"):
                st.warning("MongoDB integration requires configuration")
    
    # Show data preview
    if df is not None:
        st.subheader("Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Validate data
        if 'feedback_text' not in df.columns:
            st.error("❌ Missing 'feedback_text' column. Please ensure your data has this column.")
        else:
            # Analyze button
            if st.button("🚀 Analyze Feedback", type="primary", use_container_width=True):
                with st.spinner("Analyzing feedback... This may take a moment."):
                    try:
                        # Initialize components
                        analyzer = initialize_analyzer()
                        scorer = create_priority_scorer(config.get('priority', {}))
                        processor = create_data_processor()
                        
                        # Process data
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        status_text.text("Step 1/4: Processing text...")
                        df_processed = processor.prepare_for_analysis(df, 'feedback_text')
                        progress_bar.progress(25)
                        
                        status_text.text("Step 2/4: Analyzing sentiment...")
                        texts = df_processed['feedback_text'].tolist()
                        sentiment_results = analyzer.batch_analyze(texts, batch_size=batch_size)
                        progress_bar.progress(50)
                        
                        status_text.text("Step 3/4: Calculating priority scores...")
                        priority_results = scorer.batch_analyze(sentiment_results, texts)
                        progress_bar.progress(75)
                        
                        status_text.text("Step 4/4: Preparing results...")
                        # Combine results
                        df_processed['sentiment'] = [r['sentiment'] for r in sentiment_results]
                        df_processed['confidence'] = [r['confidence'] for r in sentiment_results]
                        df_processed['model_used'] = [r['model'] for r in sentiment_results]
                        df_processed['priority_score'] = [r['priority_score'] for r in priority_results]
                        df_processed['priority_level'] = [r['priority_level'] for r in priority_results]
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Analysis complete!")
                        
                        # Store in session state
                        st.session_state.analyzed_data = df_processed
                        st.session_state.analysis_complete = True
                        
                        time.sleep(0.5)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error during analysis: {e}")
                        import traceback
                        st.code(traceback.format_exc())

# Tab 2: Visualizations
with tab2:
    if st.session_state.analysis_complete and st.session_state.analyzed_data is not None:
        df_results = st.session_state.analyzed_data
        
        st.header("📊 Analysis Visualizations")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Feedback", len(df_results))
        
        with col2:
            avg_confidence = df_results['confidence'].mean()
            st.metric("Avg Confidence", f"{avg_confidence:.2%}")
        
        with col3:
            avg_priority = df_results['priority_score'].mean()
            st.metric("Avg Priority Score", f"{avg_priority:.2f}")
        
        with col4:
            high_priority_count = len(df_results[df_results['priority_level'] == 'High'])
            st.metric("High Priority", high_priority_count)
        
        st.divider()
        
        # Create visualizations
        visualizer = create_visualizer(config.get('visualization', {}).get('color_scheme', {}))
        
        # Row 1: Sentiment and Priority distribution
        col1, col2 = st.columns(2)
        
        with col1:
            sentiment_counts = df_results['sentiment'].value_counts().to_dict()
            fig_sentiment = visualizer.create_sentiment_pie_chart(sentiment_counts)
            st.plotly_chart(fig_sentiment, use_container_width=True)
        
        with col2:
            priority_counts = df_results['priority_level'].value_counts().to_dict()
            fig_priority = visualizer.create_priority_bar_chart(priority_counts)
            st.plotly_chart(fig_priority, use_container_width=True)
        
        # Row 2: Confidence and Priority score distributions
        col1, col2 = st.columns(2)
        
        with col1:
            fig_confidence = visualizer.create_confidence_histogram(df_results['confidence'].tolist())
            st.plotly_chart(fig_confidence, use_container_width=True)
        
        with col2:
            fig_priority_score = visualizer.create_priority_score_histogram(df_results['priority_score'].tolist())
            st.plotly_chart(fig_priority_score, use_container_width=True)
        
        # Sentiment over time (if timestamp available)
        if 'timestamp' in df_results.columns:
            st.subheader("Sentiment Trends Over Time")
            fig_timeline = visualizer.create_sentiment_over_time(df_results)
            if fig_timeline:
                st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Category breakdown (if category available)
        if 'category' in df_results.columns:
            st.subheader("Sentiment by Category")
            fig_category = visualizer.create_category_breakdown(df_results)
            if fig_category:
                st.plotly_chart(fig_category, use_container_width=True)
    
    else:
        st.info("👆 Please load and analyze data first in the 'Data & Analysis' tab")

# Tab 3: Detailed Results
with tab3:
    if st.session_state.analysis_complete and st.session_state.analyzed_data is not None:
        df_results = st.session_state.analyzed_data
        
        st.header("📋 Detailed Analysis Results")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sentiment_filter = st.multiselect(
                "Filter by Sentiment",
                options=['positive', 'negative', 'neutral'],
                default=['positive', 'negative', 'neutral']
            )
        
        with col2:
            priority_filter = st.multiselect(
                "Filter by Priority",
                options=['High', 'Medium', 'Low'],
                default=['High', 'Medium', 'Low']
            )
        
        with col3:
            search_text = st.text_input("Search in feedback", "")
        
        # Apply filters
        filtered_df = df_results[
            (df_results['sentiment'].isin(sentiment_filter)) &
            (df_results['priority_level'].isin(priority_filter))
        ]
        
        if search_text:
            filtered_df = filtered_df[
                filtered_df['feedback_text'].str.contains(search_text, case=False, na=False)
            ]
        
        st.write(f"Showing {len(filtered_df)} of {len(df_results)} results")
        
        # Display results
        for idx, row in filtered_df.iterrows():
            with st.expander(f"Feedback #{row.get('feedback_id', idx)} - {row['sentiment'].upper()} - {row['priority_level']} Priority"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write("**Feedback:**")
                    st.write(row['feedback_text'])
                
                with col2:
                    st.metric("Sentiment", row['sentiment'].capitalize())
                    st.metric("Confidence", f"{row['confidence']:.2%}")
                    st.metric("Priority Score", f"{row['priority_score']:.2f}")
                    st.metric("Priority Level", row['priority_level'])
                    
                    if 'timestamp' in row:
                        st.write(f"**Date:** {row['timestamp']}")
                    if 'category' in row:
                        st.write(f"**Category:** {row['category']}")
        
        # Export functionality
        st.divider()
        st.subheader("📥 Export Results")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write("Download the analyzed results as CSV file")
        
        with col2:
            export_handler = create_export_handler()
            export_df = export_handler.prepare_export_data(filtered_df)
            csv_data = export_handler.export_to_csv(export_df)
            filename = export_handler.generate_filename()
            
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=filename,
                mime="text/csv",
                use_container_width=True
            )
    
    else:
        st.info("👆 Please load and analyze data first in the 'Data & Analysis' tab")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>Sentiment Analysis Dashboard | Built with Streamlit | Powered by BERT & VADER</p>
</div>
""", unsafe_allow_html=True)

# Made with Bob
