"""
Export Handler
Handle data export functionality
"""

import pandas as pd
from datetime import datetime
import io
from typing import Optional


class ExportHandler:
    """
    Handle export of analysis results
    """
    
    def __init__(self):
        """Initialize export handler"""
        pass
    
    def export_to_csv(self, df: pd.DataFrame, include_timestamp: bool = True) -> bytes:
        """
        Export DataFrame to CSV bytes
        
        Args:
            df: DataFrame to export
            include_timestamp: Whether to add timestamp to filename
            
        Returns:
            CSV data as bytes
        """
        # Create buffer
        buffer = io.StringIO()
        
        # Write to CSV
        df.to_csv(buffer, index=False)
        
        # Get bytes
        csv_bytes = buffer.getvalue().encode()
        
        return csv_bytes
    
    def generate_filename(self, prefix: str = "sentiment_analysis", 
                         extension: str = "csv") -> str:
        """
        Generate filename with timestamp
        
        Args:
            prefix: Filename prefix
            extension: File extension
            
        Returns:
            Generated filename
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{extension}"
    
    def prepare_export_data(self, df: pd.DataFrame, 
                           include_original: bool = True) -> pd.DataFrame:
        """
        Prepare data for export
        
        Args:
            df: DataFrame with analysis results
            include_original: Whether to include original columns
            
        Returns:
            Prepared DataFrame
        """
        export_df = df.copy()
        
        # Add export timestamp
        export_df['export_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Reorder columns for better readability
        priority_cols = ['feedback_id', 'feedback_text', 'sentiment', 'confidence', 
                        'priority_score', 'priority_level']
        
        # Get columns that exist in the dataframe
        existing_priority_cols = [col for col in priority_cols if col in export_df.columns]
        other_cols = [col for col in export_df.columns if col not in existing_priority_cols]
        
        # Reorder
        export_df = export_df[existing_priority_cols + other_cols]
        
        return export_df


def create_export_handler() -> ExportHandler:
    """
    Factory function to create export handler
    
    Returns:
        ExportHandler instance
    """
    return ExportHandler()

# Made with Bob
