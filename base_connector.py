"""
Base Connector Class
Abstract base class for all data source connectors
"""

from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseConnector(ABC):
    """
    Abstract base class for data source connectors
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize connector
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.connected = False
        self.connection = None
        
    @abstractmethod
    def connect(self) -> bool:
        """
        Establish connection to data source
        
        Returns:
            True if connection successful, False otherwise
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """
        Close connection to data source
        
        Returns:
            True if disconnection successful, False otherwise
        """
        pass
    
    @abstractmethod
    def test_connection(self) -> Dict:
        """
        Test connection to data source
        
        Returns:
            Dictionary with test results
        """
        pass
    
    @abstractmethod
    def fetch_data(self, **kwargs) -> Optional[pd.DataFrame]:
        """
        Fetch data from source
        
        Args:
            **kwargs: Additional parameters for fetching data
            
        Returns:
            DataFrame with fetched data or None if failed
        """
        pass
    
    def validate_config(self, required_keys: list) -> Dict:
        """
        Validate configuration has required keys
        
        Args:
            required_keys: List of required configuration keys
            
        Returns:
            Dictionary with validation results
        """
        validation_result = {
            'valid': True,
            'missing_keys': [],
            'errors': []
        }
        
        for key in required_keys:
            if key not in self.config:
                validation_result['valid'] = False
                validation_result['missing_keys'].append(key)
        
        if not validation_result['valid']:
            validation_result['errors'].append(
                f"Missing required configuration keys: {validation_result['missing_keys']}"
            )
        
        return validation_result
    
    def normalize_dataframe(self, df: pd.DataFrame, 
                           column_mapping: Dict = None) -> pd.DataFrame:
        """
        Normalize dataframe to standard format
        
        Args:
            df: Input dataframe
            column_mapping: Dictionary mapping source columns to standard columns
            
        Returns:
            Normalized dataframe
        """
        if column_mapping is None:
            column_mapping = {}
        
        # Rename columns according to mapping
        df_normalized = df.rename(columns=column_mapping)
        
        # Ensure required columns exist
        required_columns = ['feedback_id', 'feedback_text', 'timestamp']
        for col in required_columns:
            if col not in df_normalized.columns:
                if col == 'feedback_id':
                    # Generate IDs if not present
                    df_normalized['feedback_id'] = range(1, len(df_normalized) + 1)
                elif col == 'timestamp':
                    # Use current timestamp if not present
                    df_normalized['timestamp'] = pd.Timestamp.now()
                elif col == 'feedback_text':
                    logger.error("feedback_text column is required but not found")
                    return pd.DataFrame()
        
        return df_normalized
    
    def get_connection_status(self) -> Dict:
        """
        Get current connection status
        
        Returns:
            Dictionary with connection status information
        """
        return {
            'connected': self.connected,
            'connector_type': self.__class__.__name__,
            'config_keys': list(self.config.keys())
        }

# Made with Bob
