"""
Priority Scoring Module
Calculates priority scores based on sentiment, confidence, and content analysis
"""

import re
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PriorityScorer:
    """
    Calculate priority scores for feedback based on multiple factors
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize priority scorer with configuration
        
        Args:
            config: Configuration dictionary with weights and keywords
        """
        self.config = config or self._get_default_config()
        
    def _get_default_config(self) -> Dict:
        """
        Get default configuration for priority scoring
        
        Returns:
            Default configuration dictionary
        """
        return {
            'weights': {
                'negative': 9,
                'neutral': 5,
                'positive': 2
            },
            'urgent_keywords': [
                'urgent', 'critical', 'broken', 'bug', 'issue',
                'problem', 'error', 'crash', 'down', 'not working',
                'failed', 'failure', 'emergency', 'asap', 'immediately',
                'severe', 'serious', 'major', 'blocker', 'stuck'
            ],
            'keyword_boost': 2,
            'length_threshold': 200,
            'length_boost': 1,
            'confidence_multiplier': 1.0
        }
    
    def detect_urgent_keywords(self, text: str) -> int:
        """
        Detect urgent keywords in text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Count of urgent keywords found
        """
        if not text:
            return 0
        
        text_lower = text.lower()
        count = 0
        
        for keyword in self.config['urgent_keywords']:
            # Use word boundaries to match whole words
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = re.findall(pattern, text_lower)
            count += len(matches)
        
        return count
    
    def calculate_length_factor(self, text: str) -> float:
        """
        Calculate length factor for priority
        Longer, detailed feedback may indicate higher priority
        
        Args:
            text: Input text
            
        Returns:
            Length factor score
        """
        if not text:
            return 0.0
        
        text_length = len(text)
        threshold = self.config['length_threshold']
        boost = self.config['length_boost']
        
        if text_length >= threshold:
            return boost
        
        return 0.0
    
    def calculate_priority_score(self, sentiment: str, confidence: float, text: str) -> float:
        """
        Calculate overall priority score
        
        Args:
            sentiment: Sentiment classification (positive/negative/neutral)
            confidence: Confidence score from sentiment analysis
            text: Original feedback text
            
        Returns:
            Priority score (0-10 scale)
        """
        # Get sentiment weight
        sentiment_weight = self.config['weights'].get(sentiment, 5)
        
        # Calculate base score with confidence
        base_score = sentiment_weight * confidence * self.config['confidence_multiplier']
        
        # Add keyword boost
        keyword_count = self.detect_urgent_keywords(text)
        keyword_score = min(keyword_count * self.config['keyword_boost'], 3)  # Cap at 3
        
        # Add length factor
        length_score = self.calculate_length_factor(text)
        
        # Calculate total score
        total_score = base_score + keyword_score + length_score
        
        # Normalize to 0-10 scale
        normalized_score = min(total_score, 10.0)
        
        return round(normalized_score, 2)
    
    def get_priority_level(self, score: float) -> str:
        """
        Convert numeric score to priority level
        
        Args:
            score: Priority score
            
        Returns:
            Priority level (High/Medium/Low)
        """
        if score >= 7.0:
            return 'High'
        elif score >= 4.0:
            return 'Medium'
        else:
            return 'Low'
    
    def analyze_feedback(self, sentiment_result: Dict, text: str) -> Dict:
        """
        Analyze feedback and calculate priority
        
        Args:
            sentiment_result: Result from sentiment analysis
            text: Original feedback text
            
        Returns:
            Dictionary with priority information
        """
        sentiment = sentiment_result.get('sentiment', 'neutral')
        confidence = sentiment_result.get('confidence', 0.0)
        
        score = self.calculate_priority_score(sentiment, confidence, text)
        level = self.get_priority_level(score)
        
        keyword_count = self.detect_urgent_keywords(text)
        
        return {
            'priority_score': score,
            'priority_level': level,
            'urgent_keywords_found': keyword_count,
            'text_length': len(text) if text else 0
        }
    
    def batch_analyze(self, sentiment_results: List[Dict], texts: List[str]) -> List[Dict]:
        """
        Analyze multiple feedback items
        
        Args:
            sentiment_results: List of sentiment analysis results
            texts: List of feedback texts
            
        Returns:
            List of priority analysis results
        """
        if len(sentiment_results) != len(texts):
            logger.error("Mismatch between sentiment results and texts length")
            return []
        
        results = []
        for sentiment_result, text in zip(sentiment_results, texts):
            priority_result = self.analyze_feedback(sentiment_result, text)
            results.append(priority_result)
        
        return results
    
    def get_priority_distribution(self, priority_results: List[Dict]) -> Dict[str, int]:
        """
        Calculate distribution of priority levels
        
        Args:
            priority_results: List of priority analysis results
            
        Returns:
            Dictionary with counts for each priority level
        """
        distribution = {
            'High': 0,
            'Medium': 0,
            'Low': 0
        }
        
        for result in priority_results:
            level = result.get('priority_level', 'Low')
            distribution[level] = distribution.get(level, 0) + 1
        
        return distribution
    
    def get_average_priority_score(self, priority_results: List[Dict]) -> float:
        """
        Calculate average priority score
        
        Args:
            priority_results: List of priority analysis results
            
        Returns:
            Average priority score
        """
        if not priority_results:
            return 0.0
        
        total_score = sum(r.get('priority_score', 0.0) for r in priority_results)
        return round(total_score / len(priority_results), 2)
    
    def get_high_priority_feedback(self, priority_results: List[Dict], 
                                   texts: List[str], 
                                   threshold: float = 7.0) -> List[Dict]:
        """
        Filter high priority feedback
        
        Args:
            priority_results: List of priority analysis results
            texts: List of feedback texts
            threshold: Minimum score for high priority
            
        Returns:
            List of high priority feedback with details
        """
        high_priority = []
        
        for i, (result, text) in enumerate(zip(priority_results, texts)):
            score = result.get('priority_score', 0.0)
            if score >= threshold:
                high_priority.append({
                    'index': i,
                    'text': text,
                    'priority_score': score,
                    'priority_level': result.get('priority_level'),
                    'urgent_keywords': result.get('urgent_keywords_found', 0)
                })
        
        # Sort by priority score descending
        high_priority.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return high_priority


def create_priority_scorer(config: Dict = None) -> PriorityScorer:
    """
    Factory function to create priority scorer
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        PriorityScorer instance
    """
    return PriorityScorer(config=config)

# Made with Bob
