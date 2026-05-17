"""
SQL Database Connector
Handle PostgreSQL, MySQL, and SQLite connections
"""

from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
import pandas as pd
from typing import Dict, Optional
import logging
from .base_connector import BaseConnector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SQLConnector(BaseConnector):
    """
    Connector for SQL databases (PostgreSQL, MySQL, SQLite)
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize SQL connector
        
        Args:
            config: Configuration dictionary with:
                - connection_string: SQLAlchemy connection string
                - pool_size: Connection pool size (default: 5)
                - max_overflow: Max overflow connections (default: 10)
                - pool_timeout: Pool timeout in seconds (default: 30)
        """
        super().__init__(config)
        self.engine = None
        self.connection_string = None
        
    def connect(self) -> bool:
        """
        Establish database connection
        
        Returns:
            True if connection successful
        """
        # Validate required config
        validation = self.validate_config(['connection_string'])
        if not validation['valid']:
            logger.error(f"Configuration validation failed: {validation['errors']}")
            return False
        
        self.connection_string = self.config['connection_string']
        
        try:
            # Create engine with connection pooling
            pool_size = self.config.get('pool_size', 5)
            max_overflow = self.config.get('max_overflow', 10)
            pool_timeout = self.config.get('pool_timeout', 30)
            
            self.engine = create_engine(
                self.connection_string,
                poolclass=QueuePool,
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_timeout=pool_timeout,
                pool_pre_ping=True  # Verify connections before using
            )
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            self.connected = True
            logger.info("SQL database connection established")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False
    
    def disconnect(self) -> bool:
        """
        Close database connection
        
        Returns:
            True if disconnection successful
        """
        if self.engine:
            self.engine.dispose()
        self.connected = False
        self.engine = None
        return True
    
    def test_connection(self) -> Dict:
        """
        Test database connection
        
        Returns:
            Dictionary with test results
        """
        result = {
            'success': False,
            'message': '',
            'database_type': self._get_database_type()
        }
        
        if not self.connected:
            result['message'] = "Not connected. Call connect() first"
            return result
        
        try:
            with self.engine.connect() as conn:
                test_result = conn.execute(text("SELECT 1")).fetchone()
                
            result['success'] = True
            result['message'] = "Connection successful"
            result['pool_size'] = self.engine.pool.size()
            
        except Exception as e:
            result['message'] = f"Connection test failed: {str(e)}"
            logger.error(f"Test connection failed: {e}")
        
        return result
    
    def fetch_data(self, **kwargs) -> Optional[pd.DataFrame]:
        """
        Fetch data from database
        
        Args:
            **kwargs: Additional parameters
                - query: SQL query string (required)
                - params: Query parameters for parameterized queries
                - chunksize: Read data in chunks
                
        Returns:
            DataFrame with data or None if failed
        """
        if not self.connected:
            logger.error("Not connected. Call connect() first")
            return None
        
        query = kwargs.get('query')
        if not query:
            logger.error("SQL query is required")
            return None
        
        try:
            params = kwargs.get('params', {})
            chunksize = kwargs.get('chunksize', None)
            
            # Execute query and load into DataFrame
            df = pd.read_sql_query(
                query,
                self.engine,
                params=params,
                chunksize=chunksize
            )
            
            # If chunksize is used, concatenate chunks
            if chunksize:
                df = pd.concat(df, ignore_index=True)
            
            logger.info(f"Successfully fetched {len(df)} rows from database")
            
            # Normalize column names
            column_mapping = kwargs.get('column_mapping', {})
            if column_mapping:
                df = self.normalize_dataframe(df, column_mapping)
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return None
    
    def execute_query(self, query: str, params: Dict = None) -> bool:
        """
        Execute a SQL query (INSERT, UPDATE, DELETE)
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            True if execution successful
        """
        if not self.connected:
            logger.error("Not connected. Call connect() first")
            return False
        
        try:
            with self.engine.connect() as conn:
                conn.execute(text(query), params or {})
                conn.commit()
            
            logger.info("Query executed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return False
    
    def get_table_info(self, table_name: str) -> Dict:
        """
        Get information about a table
        
        Args:
            table_name: Name of the table
            
        Returns:
            Dictionary with table information
        """
        info = {
            'table_name': table_name,
            'exists': False
        }
        
        if not self.connected:
            info['error'] = "Not connected"
            return info
        
        try:
            # Check if table exists and get row count
            query = f"SELECT COUNT(*) as count FROM {table_name}"
            with self.engine.connect() as conn:
                result = conn.execute(text(query)).fetchone()
                info['exists'] = True
                info['row_count'] = result[0]
            
            # Get column information
            query = f"SELECT * FROM {table_name} LIMIT 1"
            df = pd.read_sql_query(query, self.engine)
            info['columns'] = list(df.columns)
            info['column_count'] = len(df.columns)
            
        except Exception as e:
            info['error'] = str(e)
        
        return info
    
    def _get_database_type(self) -> str:
        """
        Get database type from connection string
        
        Returns:
            Database type (postgresql, mysql, sqlite, etc.)
        """
        if not self.connection_string:
            return "unknown"
        
        if self.connection_string.startswith('postgresql'):
            return "PostgreSQL"
        elif self.connection_string.startswith('mysql'):
            return "MySQL"
        elif self.connection_string.startswith('sqlite'):
            return "SQLite"
        else:
            return "Unknown"


def create_sql_connector(connection_string: str, **kwargs) -> SQLConnector:
    """
    Factory function to create SQL connector
    
    Args:
        connection_string: SQLAlchemy connection string
        **kwargs: Additional configuration
        
    Returns:
        SQLConnector instance
    """
    config = {
        'connection_string': connection_string,
        **kwargs
    }
    connector = SQLConnector(config=config)
    connector.connect()
    return connector

# Made with Bob
