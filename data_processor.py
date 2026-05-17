"""
Data Processing Pipeline
Clean and prepare feedback text for sentiment analysis
"""

import re
import pandas as pd
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Process and clean feedback text data
    """
    
    def __init__(self):
        """Initialize data processor"""
        pass
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Convert to string if not already
        text = str(text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def remove_special_characters(self, text: str, keep_punctuation: bool = True) -> str:
        """
        Remove special characters from text
        
        Args:
            text: Input text
            keep_punctuation: Whether to keep basic punctuation
            
        Returns:
            Text with special characters removed
        """
        if not text:
            return ""
        
        if keep_punctuation:
            # Keep letters, numbers, and basic punctuation
            text = re.sub(r'[^a-zA-Z0-9\s.,!?;:\'-]', '', text)
        else:
            # Keep only letters, numbers, and spaces
            text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        
        return text
    
    def normalize_whitespace(self, text: str) -> str:
        """
        Normalize whitespace in text
        
        Args:
            text: Input text
            
        Returns:
            Text with normalized whitespace
        """
        if not text:
            return ""
        
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def process_text(self, text: str, 
                    remove_urls: bool = True,
                    remove_emails: bool = True,
                    remove_special_chars: bool = False,
                    keep_punctuation: bool = True) -> str:
        """
        Process text with multiple cleaning steps
        
        Args:
            text: Input text
            remove_urls: Whether to remove URLs
            remove_emails: Whether to remove email addresses
            remove_special_chars: Whether to remove special characters
            keep_punctuation: Whether to keep punctuation (if removing special chars)
            
        Returns:
            Processed text
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Clean text
        processed = self.clean_text(text)
        
        # Remove special characters if requested
        if remove_special_chars:
            processed = self.remove_special_characters(processed, keep_punctuation)
        
        # Normalize whitespace
        processed = self.normalize_whitespace(processed)
        
        return processed
    
    def process_dataframe(self, df: pd.DataFrame, 
                         text_column: str = 'feedback_text',
                         **kwargs) -> pd.DataFrame:
        """
        Process all text in a dataframe
        
        Args:
            df: Input dataframe
            text_column: Name of column containing text
            **kwargs: Additional arguments for process_text
            
        Returns:
            Dataframe with processed text
        """
        if text_column not in df.columns:
            logger.error(f"Column '{text_column}' not found in dataframe")
            return df
        
        # Create a copy to avoid modifying original
        df_processed = df.copy()
        
        # Process each text entry
        df_processed[text_column] = df_processed[text_column].apply(
            lambda x: self.process_text(x, **kwargs)
        )
        
        # Remove empty entries
        df_processed = df_processed[df_processed[text_column].str.len() > 0]
        
        return df_processed
    
    def validate_dataframe(self, df: pd.DataFrame, 
                          required_columns: List[str] = None) -> Dict:
        """
        Validate dataframe structure and content
        
        Args:
            df: Input dataframe
            required_columns: List of required column names
            
        Returns:
            Dictionary with validation results
        """
        if required_columns is None:
            required_columns = ['feedback_text']
        
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'row_count': len(df),
            'column_count': len(df.columns)
        }
        
        # Check if dataframe is empty
        if df.empty:
            validation_result['valid'] = False
            validation_result['errors'].append("Dataframe is empty")
            return validation_result
        
        # Check for required columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            validation_result['valid'] = False
            validation_result['errors'].append(f"Missing required columns: {missing_columns}")
        
        # Check for empty text entries
        if 'feedback_text' in df.columns:
            empty_count = df['feedback_text'].isna().sum() + (df['feedback_text'] == '').sum()
            if empty_count > 0:
                validation_result['warnings'].append(
                    f"{empty_count} rows have empty feedback text"
                )
        
        # Check for duplicate entries
        if 'feedback_id' in df.columns:
            duplicate_count = df['feedback_id'].duplicated().sum()
            if duplicate_count > 0:
                validation_result['warnings'].append(
                    f"{duplicate_count} duplicate feedback IDs found"
                )
        
        return validation_result
    
    def deduplicate_dataframe(self, df: pd.DataFrame, 
                             id_column: str = 'feedback_id',
                             keep: str = 'first') -> pd.DataFrame:
        """
        Remove duplicate entries from dataframe
        
        Args:
            df: Input dataframe
            id_column: Column to use for deduplication
            keep: Which duplicate to keep ('first', 'last', False)
            
        Returns:
            Deduplicated dataframe
        """
        if id_column not in df.columns:
            logger.warning(f"Column '{id_column}' not found, skipping deduplication")
            return df
        
        initial_count = len(df)
        df_dedup = df.drop_duplicates(subset=[id_column], keep=keep)
        removed_count = initial_count - len(df_dedup)
        
        if removed_count > 0:
            logger.info(f"Removed {removed_count} duplicate entries")
        
        return df_dedup
    
    def handle_missing_values(self, df: pd.DataFrame, 
                             text_column: str = 'feedback_text',
                             strategy: str = 'drop') -> pd.DataFrame:
        """
        Handle missing values in dataframe
        
        Args:
            df: Input dataframe
            text_column: Column to check for missing values
            strategy: How to handle missing values ('drop', 'fill')
            
        Returns:
            Dataframe with missing values handled
        """
        if text_column not in df.columns:
            return df
        
        if strategy == 'drop':
            # Drop rows with missing text
            df_clean = df.dropna(subset=[text_column])
            df_clean = df_clean[df_clean[text_column].str.len() > 0]
        elif strategy == 'fill':
            # Fill missing values with empty string
            df_clean = df.copy()
            df_clean[text_column] = df_clean[text_column].fillna('')
        else:
            logger.warning(f"Unknown strategy '{strategy}', returning original dataframe")
            df_clean = df
        
        return df_clean
    
    def add_text_features(self, df: pd.DataFrame, 
                         text_column: str = 'feedback_text') -> pd.DataFrame:
        """
        Add text-based features to dataframe
        
        Args:
            df: Input dataframe
            text_column: Column containing text
            
        Returns:
            Dataframe with additional features
        """
        if text_column not in df.columns:
            return df
        
        df_features = df.copy()
        
        # Add text length
        df_features['text_length'] = df_features[text_column].str.len()
        
        # Add word count
        df_features['word_count'] = df_features[text_column].str.split().str.len()
        
        # Add character count (excluding spaces)
        df_features['char_count'] = df_features[text_column].str.replace(' ', '').str.len()
        
        return df_features
    
    def prepare_for_analysis(self, df: pd.DataFrame,
                            text_column: str = 'feedback_text',
                            clean: bool = True,
                            deduplicate: bool = True,
                            handle_missing: bool = True,
                            add_features: bool = True) -> pd.DataFrame:
        """
        Complete preparation pipeline for analysis
        
        Args:
            df: Input dataframe
            text_column: Column containing text
            clean: Whether to clean text
            deduplicate: Whether to remove duplicates
            handle_missing: Whether to handle missing values
            add_features: Whether to add text features
            
        Returns:
            Prepared dataframe
        """
        df_prepared = df.copy()
        
        # Validate dataframe
        validation = self.validate_dataframe(df_prepared, [text_column])
        if not validation['valid']:
            logger.error(f"Validation failed: {validation['errors']}")
            return df_prepared
        
        # Handle missing values
        if handle_missing:
            df_prepared = self.handle_missing_values(df_prepared, text_column)
        
        # Deduplicate
        if deduplicate and 'feedback_id' in df_prepared.columns:
            df_prepared = self.deduplicate_dataframe(df_prepared)
        
        # Clean text
        if clean:
            df_prepared = self.process_dataframe(df_prepared, text_column)
        
        # Add features
        if add_features:
            df_prepared = self.add_text_features(df_prepared, text_column)
        
        logger.info(f"Prepared {len(df_prepared)} feedback entries for analysis")
        
        return df_prepared


def create_data_processor() -> DataProcessor:
    """
    Factory function to create data processor
    
    Returns:
        DataProcessor instance
    """
    return DataProcessor()

# Made with Bob
