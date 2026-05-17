"""
CSV/Excel File Connector
Handle CSV and Excel file uploads
"""

import pandas as pd
from typing import Dict, Optional
import logging
from .base_connector import BaseConnector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CSVConnector(BaseConnector):
    """
    Connector for CSV and Excel files
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize CSV connector
        
        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.file_path = None
        self.file_type = None
        
    def connect(self) -> bool:
        """
        Validate file path exists
        
        Returns:
            True if file path is valid
        """
        if 'file_path' not in self.config:
            logger.error("file_path not provided in configuration")
            return False
        
        self.file_path = self.config['file_path']
        
        # Determine file type
        if self.file_path.endswith('.csv'):
            self.file_type = 'csv'
        elif self.file_path.endswith(('.xlsx', '.xls')):
            self.file_type = 'excel'
        else:
            logger.error(f"Unsupported file type: {self.file_path}")
            return False
        
        self.connected = True
        logger.info(f"CSV connector initialized for {self.file_type} file")
        return True
    
    def disconnect(self) -> bool:
        """
        Disconnect (no-op for file connector)
        
        Returns:
            True
        """
        self.connected = False
        self.file_path = None
        self.file_type = None
        return True
    
    def test_connection(self) -> Dict:
        """
        Test if file can be read
        
        Returns:
            Dictionary with test results
        """
        result = {
            'success': False,
            'message': '',
            'file_type': self.file_type,
            'file_path': self.file_path
        }
        
        try:
            if self.file_type == 'csv':
                # Try reading first few rows
                df = pd.read_csv(self.file_path, nrows=5)
            elif self.file_type == 'excel':
                df = pd.read_excel(self.file_path, nrows=5)
            else:
                result['message'] = "Unknown file type"
                return result
            
            result['success'] = True
            result['message'] = f"Successfully read {self.file_type} file"
            result['columns'] = list(df.columns)
            result['sample_rows'] = len(df)
            
        except Exception as e:
            result['message'] = f"Error reading file: {str(e)}"
            logger.error(f"Test connection failed: {e}")
        
        return result
    
    def fetch_data(self, **kwargs) -> Optional[pd.DataFrame]:
        """
        Read data from CSV/Excel file
        
        Args:
            **kwargs: Additional parameters
                - sheet_name: For Excel files (default: 0)
                - encoding: For CSV files (default: 'utf-8')
                - nrows: Number of rows to read (default: None - all rows)
                
        Returns:
            DataFrame with data or None if failed
        """
        if not self.connected:
            logger.error("Not connected. Call connect() first")
            return None
        
        try:
            if self.file_type == 'csv':
                encoding = kwargs.get('encoding', 'utf-8')
                nrows = kwargs.get('nrows', None)
                df = pd.read_csv(
                    self.file_path,
                    encoding=encoding,
                    nrows=nrows
                )
            elif self.file_type == 'excel':
                sheet_name = kwargs.get('sheet_name', 0)
                nrows = kwargs.get('nrows', None)
                df = pd.read_excel(
                    self.file_path,
                    sheet_name=sheet_name,
                    nrows=nrows
                )
            else:
                logger.error(f"Unsupported file type: {self.file_type}")
                return None
            
            logger.info(f"Successfully loaded {len(df)} rows from {self.file_type} file")
            
            # Normalize column names
            column_mapping = kwargs.get('column_mapping', {})
            if column_mapping:
                df = self.normalize_dataframe(df, column_mapping)
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return None
    
    def validate_file(self, required_columns: list = None) -> Dict:
        """
        Validate file structure
        
        Args:
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
            'file_info': {}
        }
        
        try:
            # Read file to check structure
            if self.file_type == 'csv':
                df = pd.read_csv(self.file_path, nrows=10)
            elif self.file_type == 'excel':
                df = pd.read_excel(self.file_path, nrows=10)
            else:
                validation_result['valid'] = False
                validation_result['errors'].append("Unknown file type")
                return validation_result
            
            # Store file info
            validation_result['file_info'] = {
                'columns': list(df.columns),
                'column_count': len(df.columns),
                'sample_row_count': len(df)
            }
            
            # Check for required columns
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                validation_result['valid'] = False
                validation_result['errors'].append(
                    f"Missing required columns: {missing_columns}"
                )
            
            # Check for empty dataframe
            if df.empty:
                validation_result['valid'] = False
                validation_result['errors'].append("File is empty")
            
        except Exception as e:
            validation_result['valid'] = False
            validation_result['errors'].append(f"Error validating file: {str(e)}")
        
        return validation_result
    
    def get_file_info(self) -> Dict:
        """
        Get information about the file
        
        Returns:
            Dictionary with file information
        """
        info = {
            'file_path': self.file_path,
            'file_type': self.file_type,
            'connected': self.connected
        }
        
        if self.connected:
            try:
                if self.file_type == 'csv':
                    df = pd.read_csv(self.file_path)
                elif self.file_type == 'excel':
                    df = pd.read_excel(self.file_path)
                else:
                    return info
                
                info['total_rows'] = len(df)
                info['columns'] = list(df.columns)
                info['column_count'] = len(df.columns)
                info['memory_usage_mb'] = df.memory_usage(deep=True).sum() / (1024 * 1024)
                
            except Exception as e:
                info['error'] = str(e)
        
        return info


def create_csv_connector(file_path: str, **kwargs) -> CSVConnector:
    """
    Factory function to create CSV connector
    
    Args:
        file_path: Path to CSV/Excel file
        **kwargs: Additional configuration
        
    Returns:
        CSVConnector instance
    """
    config = {'file_path': file_path, **kwargs}
    connector = CSVConnector(config=config)
    connector.connect()
    return connector

# Made with Bob
