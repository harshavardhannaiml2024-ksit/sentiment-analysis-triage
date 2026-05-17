"""
Sentiment Analysis Module
Supports BERT-based transformer models and VADER as fallback
"""

import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from typing import Dict, List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """
    Sentiment analyzer with BERT model and VADER fallback
    """
    
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english", 
                 use_vader_fallback: bool = True):
        """
        Initialize sentiment analyzer
        
        Args:
            model_name: Hugging Face model name
            use_vader_fallback: Whether to use VADER as fallback
        """
        self.model_name = model_name
        self.use_vader_fallback = use_vader_fallback
        self.model = None
        self.vader_analyzer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    @st.cache_resource
    def load_transformer_model(_self, model_name: str):
        """
        Load transformer model with caching
        
        Args:
            model_name: Model name to load
            
        Returns:
            Sentiment analysis pipeline
        """
        try:
            logger.info(f"Loading transformer model: {model_name}")
            sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model=model_name,
                device=0 if torch.cuda.is_available() else -1
            )
            logger.info("Transformer model loaded successfully")
            return sentiment_pipeline
        except Exception as e:
            logger.error(f"Error loading transformer model: {e}")
            return None
    
    def load_vader_model(self):
        """
        Load VADER sentiment analyzer
        
        Returns:
            VADER analyzer instance
        """
        try:
            # Download VADER lexicon if not present
            try:
                nltk.data.find('sentiment/vader_lexicon.zip')
            except LookupError:
                logger.info("Downloading VADER lexicon...")
                nltk.download('vader_lexicon', quiet=True)
            
            logger.info("Loading VADER analyzer")
            return SentimentIntensityAnalyzer()
        except Exception as e:
            logger.error(f"Error loading VADER: {e}")
            return None
    
    def initialize(self):
        """
        Initialize the sentiment analyzer models
        """
        # Try to load transformer model
        self.model = self.load_transformer_model(self.model_name)
        
        # Load VADER if enabled or if transformer failed
        if self.use_vader_fallback or self.model is None:
            self.vader_analyzer = self.load_vader_model()
    
    def analyze_with_transformer(self, text: str) -> Dict:
        """
        Analyze sentiment using transformer model
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with sentiment and confidence
        """
        try:
            # Truncate text if too long (BERT has 512 token limit)
            max_length = 512
            if len(text.split()) > max_length:
                text = ' '.join(text.split()[:max_length])
            
            result = self.model(text)[0]
            label = result['label'].upper()
            confidence = result['score']
            
            # Map labels to standard format
            sentiment_map = {
                'POSITIVE': 'positive',
                'NEGATIVE': 'negative',
                'NEUTRAL': 'neutral',
                'LABEL_0': 'negative',  # Some models use LABEL_0/1/2
                'LABEL_1': 'neutral',
                'LABEL_2': 'positive'
            }
            
            sentiment = sentiment_map.get(label, 'neutral')
            
            return {
                'sentiment': sentiment,
                'confidence': confidence,
                'model': 'transformer'
            }
        except Exception as e:
            logger.error(f"Error in transformer analysis: {e}")
            return None
    
    def analyze_with_vader(self, text: str) -> Dict:
        """
        Analyze sentiment using VADER
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with sentiment and confidence
        """
        try:
            scores = self.vader_analyzer.polarity_scores(text)
            compound = scores['compound']
            
            # Determine sentiment based on compound score
            if compound >= 0.05:
                sentiment = 'positive'
                confidence = scores['pos']
            elif compound <= -0.05:
                sentiment = 'negative'
                confidence = scores['neg']
            else:
                sentiment = 'neutral'
                confidence = scores['neu']
            
            return {
                'sentiment': sentiment,
                'confidence': confidence,
                'model': 'vader'
            }
        except Exception as e:
            logger.error(f"Error in VADER analysis: {e}")
            return None
    
    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of text using available models
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with sentiment, confidence, and model used
        """
        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            return {
                'sentiment': 'neutral',
                'confidence': 0.0,
                'model': 'default'
            }
        
        # Try transformer model first
        if self.model is not None:
            result = self.analyze_with_transformer(text)
            if result is not None:
                return result
        
        # Fall back to VADER
        if self.vader_analyzer is not None:
            result = self.analyze_with_vader(text)
            if result is not None:
                return result
        
        # Default fallback
        logger.warning("All models failed, returning neutral sentiment")
        return {
            'sentiment': 'neutral',
            'confidence': 0.0,
            'model': 'default'
        }
    
    def batch_analyze(self, texts: List[str], batch_size: int = 32) -> List[Dict]:
        """
        Analyze multiple texts in batches
        
        Args:
            texts: List of texts to analyze
            batch_size: Number of texts to process at once
            
        Returns:
            List of sentiment analysis results
        """
        results = []
        
        # Process in batches for efficiency
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            for text in batch:
                result = self.analyze_sentiment(text)
                results.append(result)
        
        return results
    
    def get_sentiment_distribution(self, results: List[Dict]) -> Dict[str, int]:
        """
        Calculate sentiment distribution from results
        
        Args:
            results: List of sentiment analysis results
            
        Returns:
            Dictionary with counts for each sentiment
        """
        distribution = {
            'positive': 0,
            'negative': 0,
            'neutral': 0
        }
        
        for result in results:
            sentiment = result.get('sentiment', 'neutral')
            distribution[sentiment] = distribution.get(sentiment, 0) + 1
        
        return distribution
    
    def get_average_confidence(self, results: List[Dict]) -> float:
        """
        Calculate average confidence score
        
        Args:
            results: List of sentiment analysis results
            
        Returns:
            Average confidence score
        """
        if not results:
            return 0.0
        
        total_confidence = sum(r.get('confidence', 0.0) for r in results)
        return total_confidence / len(results)


def create_sentiment_analyzer(model_name: str = None, use_vader: bool = True) -> SentimentAnalyzer:
    """
    Factory function to create and initialize sentiment analyzer
    
    Args:
        model_name: Optional model name override
        use_vader: Whether to enable VADER fallback
        
    Returns:
        Initialized SentimentAnalyzer instance
    """
    if model_name is None:
        model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    
    analyzer = SentimentAnalyzer(model_name=model_name, use_vader_fallback=use_vader)
    analyzer.initialize()
    
    return analyzer

# Made with Bob
