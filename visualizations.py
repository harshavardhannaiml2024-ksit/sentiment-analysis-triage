"""
Visualization Module
Create charts and graphs for sentiment analysis results
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64


class SentimentVisualizer:
    """
    Create visualizations for sentiment analysis results
    """
    
    def __init__(self, color_scheme: Dict = None):
        """
        Initialize visualizer
        
        Args:
            color_scheme: Dictionary with color mappings
        """
        self.color_scheme = color_scheme or self._get_default_colors()
    
    def _get_default_colors(self) -> Dict:
        """Get default color scheme"""
        return {
            'positive': '#28a745',
            'negative': '#dc3545',
            'neutral': '#6c757d',
            'high_priority': '#ff4444',
            'medium_priority': '#ffaa00',
            'low_priority': '#44ff44'
        }
    
    def create_sentiment_pie_chart(self, sentiment_counts: Dict) -> go.Figure:
        """
        Create pie chart for sentiment distribution
        
        Args:
            sentiment_counts: Dictionary with sentiment counts
            
        Returns:
            Plotly figure
        """
        labels = list(sentiment_counts.keys())
        values = list(sentiment_counts.values())
        
        colors = [self.color_scheme.get(label.lower(), '#999999') for label in labels]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            textinfo='label+percent+value',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title='Sentiment Distribution',
            showlegend=True,
            height=400
        )
        
        return fig
    
    def create_priority_bar_chart(self, priority_counts: Dict) -> go.Figure:
        """
        Create bar chart for priority distribution
        
        Args:
            priority_counts: Dictionary with priority level counts
            
        Returns:
            Plotly figure
        """
        labels = ['High', 'Medium', 'Low']
        values = [priority_counts.get(label, 0) for label in labels]
        
        colors = [
            self.color_scheme['high_priority'],
            self.color_scheme['medium_priority'],
            self.color_scheme['low_priority']
        ]
        
        fig = go.Figure(data=[go.Bar(
            x=labels,
            y=values,
            marker=dict(color=colors),
            text=values,
            textposition='auto',
            hovertemplate='<b>%{x} Priority</b><br>Count: %{y}<extra></extra>'
        )])
        
        fig.update_layout(
            title='Priority Level Distribution',
            xaxis_title='Priority Level',
            yaxis_title='Count',
            showlegend=False,
            height=400
        )
        
        return fig
    
    def create_confidence_histogram(self, confidence_scores: List[float]) -> go.Figure:
        """
        Create histogram for confidence score distribution
        
        Args:
            confidence_scores: List of confidence scores
            
        Returns:
            Plotly figure
        """
        fig = go.Figure(data=[go.Histogram(
            x=confidence_scores,
            nbinsx=20,
            marker=dict(color='#4CAF50', line=dict(color='white', width=1)),
            hovertemplate='Confidence: %{x:.2f}<br>Count: %{y}<extra></extra>'
        )])
        
        fig.update_layout(
            title='Confidence Score Distribution',
            xaxis_title='Confidence Score',
            yaxis_title='Frequency',
            showlegend=False,
            height=400
        )
        
        return fig
    
    def create_priority_score_histogram(self, priority_scores: List[float]) -> go.Figure:
        """
        Create histogram for priority score distribution
        
        Args:
            priority_scores: List of priority scores
            
        Returns:
            Plotly figure
        """
        fig = go.Figure(data=[go.Histogram(
            x=priority_scores,
            nbinsx=20,
            marker=dict(color='#FF9800', line=dict(color='white', width=1)),
            hovertemplate='Priority Score: %{x:.2f}<br>Count: %{y}<extra></extra>'
        )])
        
        fig.update_layout(
            title='Priority Score Distribution',
            xaxis_title='Priority Score (0-10)',
            yaxis_title='Frequency',
            showlegend=False,
            height=400
        )
        
        return fig
    
    def create_sentiment_over_time(self, df: pd.DataFrame, 
                                   timestamp_col: str = 'timestamp') -> go.Figure:
        """
        Create line chart showing sentiment trends over time
        
        Args:
            df: DataFrame with sentiment and timestamp data
            timestamp_col: Name of timestamp column
            
        Returns:
            Plotly figure
        """
        if timestamp_col not in df.columns:
            return None
        
        # Convert timestamp to datetime
        df[timestamp_col] = pd.to_datetime(df[timestamp_col])
        
        # Group by date and sentiment
        df['date'] = df[timestamp_col].dt.date
        sentiment_by_date = df.groupby(['date', 'sentiment']).size().reset_index(name='count')
        
        fig = go.Figure()
        
        for sentiment in ['positive', 'negative', 'neutral']:
            data = sentiment_by_date[sentiment_by_date['sentiment'] == sentiment]
            fig.add_trace(go.Scatter(
                x=data['date'],
                y=data['count'],
                mode='lines+markers',
                name=sentiment.capitalize(),
                line=dict(color=self.color_scheme[sentiment]),
                hovertemplate='<b>%{fullData.name}</b><br>Date: %{x}<br>Count: %{y}<extra></extra>'
            ))
        
        fig.update_layout(
            title='Sentiment Trends Over Time',
            xaxis_title='Date',
            yaxis_title='Count',
            hovermode='x unified',
            height=400
        )
        
        return fig
    
    def create_combined_dashboard(self, df: pd.DataFrame) -> go.Figure:
        """
        Create combined dashboard with multiple charts
        
        Args:
            df: DataFrame with analysis results
            
        Returns:
            Plotly figure with subplots
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Sentiment Distribution', 'Priority Levels',
                          'Confidence Scores', 'Priority Scores'),
            specs=[[{'type': 'pie'}, {'type': 'bar'}],
                   [{'type': 'histogram'}, {'type': 'histogram'}]]
        )
        
        # Sentiment pie chart
        sentiment_counts = df['sentiment'].value_counts().to_dict()
        labels = list(sentiment_counts.keys())
        values = list(sentiment_counts.values())
        colors = [self.color_scheme.get(label.lower(), '#999999') for label in labels]
        
        fig.add_trace(
            go.Pie(labels=labels, values=values, marker=dict(colors=colors)),
            row=1, col=1
        )
        
        # Priority bar chart
        priority_counts = df['priority_level'].value_counts().to_dict()
        priority_labels = ['High', 'Medium', 'Low']
        priority_values = [priority_counts.get(label, 0) for label in priority_labels]
        priority_colors = [
            self.color_scheme['high_priority'],
            self.color_scheme['medium_priority'],
            self.color_scheme['low_priority']
        ]
        
        fig.add_trace(
            go.Bar(x=priority_labels, y=priority_values, marker=dict(color=priority_colors)),
            row=1, col=2
        )
        
        # Confidence histogram
        fig.add_trace(
            go.Histogram(x=df['confidence'], nbinsx=20, marker=dict(color='#4CAF50')),
            row=2, col=1
        )
        
        # Priority score histogram
        fig.add_trace(
            go.Histogram(x=df['priority_score'], nbinsx=20, marker=dict(color='#FF9800')),
            row=2, col=2
        )
        
        fig.update_layout(
            height=800,
            showlegend=False,
            title_text="Sentiment Analysis Dashboard"
        )
        
        return fig
    
    def create_word_cloud(self, texts: List[str], sentiment: str = None) -> str:
        """
        Create word cloud from text data
        
        Args:
            texts: List of text strings
            sentiment: Optional sentiment filter
            
        Returns:
            Base64 encoded image string
        """
        # Combine all texts
        combined_text = ' '.join(texts)
        
        if not combined_text.strip():
            return None
        
        # Create word cloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='viridis' if not sentiment else self._get_colormap(sentiment),
            max_words=100
        ).generate(combined_text)
        
        # Convert to image
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        
        if sentiment:
            ax.set_title(f'Word Cloud - {sentiment.capitalize()} Feedback', 
                        fontsize=16, fontweight='bold')
        
        # Save to bytes
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        buf.seek(0)
        plt.close()
        
        # Encode to base64
        img_base64 = base64.b64encode(buf.read()).decode()
        return f"data:image/png;base64,{img_base64}"
    
    def _get_colormap(self, sentiment: str) -> str:
        """Get colormap for sentiment"""
        colormap_dict = {
            'positive': 'Greens',
            'negative': 'Reds',
            'neutral': 'Greys'
        }
        return colormap_dict.get(sentiment.lower(), 'viridis')
    
    def create_scatter_plot(self, df: pd.DataFrame) -> go.Figure:
        """
        Create scatter plot of confidence vs priority score
        
        Args:
            df: DataFrame with analysis results
            
        Returns:
            Plotly figure
        """
        fig = px.scatter(
            df,
            x='confidence',
            y='priority_score',
            color='sentiment',
            color_discrete_map={
                'positive': self.color_scheme['positive'],
                'negative': self.color_scheme['negative'],
                'neutral': self.color_scheme['neutral']
            },
            hover_data=['feedback_text'],
            title='Confidence vs Priority Score'
        )
        
        fig.update_layout(
            xaxis_title='Confidence Score',
            yaxis_title='Priority Score',
            height=500
        )
        
        return fig
    
    def create_category_breakdown(self, df: pd.DataFrame, 
                                 category_col: str = 'category') -> go.Figure:
        """
        Create stacked bar chart showing sentiment by category
        
        Args:
            df: DataFrame with analysis results
            category_col: Name of category column
            
        Returns:
            Plotly figure
        """
        if category_col not in df.columns:
            return None
        
        # Group by category and sentiment
        category_sentiment = df.groupby([category_col, 'sentiment']).size().reset_index(name='count')
        
        fig = go.Figure()
        
        for sentiment in ['positive', 'negative', 'neutral']:
            data = category_sentiment[category_sentiment['sentiment'] == sentiment]
            fig.add_trace(go.Bar(
                x=data[category_col],
                y=data['count'],
                name=sentiment.capitalize(),
                marker=dict(color=self.color_scheme[sentiment]),
                hovertemplate='<b>%{x}</b><br>%{fullData.name}: %{y}<extra></extra>'
            ))
        
        fig.update_layout(
            title='Sentiment Distribution by Category',
            xaxis_title='Category',
            yaxis_title='Count',
            barmode='stack',
            height=400
        )
        
        return fig


def create_visualizer(color_scheme: Dict = None) -> SentimentVisualizer:
    """
    Factory function to create visualizer
    
    Args:
        color_scheme: Optional custom color scheme
        
    Returns:
        SentimentVisualizer instance
    """
    return SentimentVisualizer(color_scheme=color_scheme)

# Made with Bob
