"""
MongoDB Connector
Handle MongoDB and MongoDB Atlas connections
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import pandas as pd
from typing import Dict, Optional, List
import logging
from .base_connector import BaseConnector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MongoDBConnector(BaseConnector):
    """
    Connector for MongoDB databases
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize MongoDB connector
        
        Args:
            config: Configuration dictionary with:
                - connection_string: MongoDB connection URI
                - database: Database name
                - collection: Collection name
                - max_pool_size: Max connection pool size (default: 10)
                - timeout_ms: Connection timeout in milliseconds (default: 5000)
        """
        super().__init__(config)
        self.client = None
        self.database = None
        self.collection = None
        self.connection_string = None
        
    def connect(self) -> bool:
        """
        Establish MongoDB connection
        
        Returns:
            True if connection successful
        """
        # Validate required config
        validation = self.validate_config(['connection_string', 'database'])
        if not validation['valid']:
            logger.error(f"Configuration validation failed: {validation['errors']}")
            return False
        
        self.connection_string = self.config['connection_string']
        database_name = self.config['database']
        
        try:
            # Create MongoDB client
            max_pool_size = self.config.get('max_pool_size', 10)
            timeout_ms = self.config.get('timeout_ms', 5000)
            
            self.client = MongoClient(
                self.connection_string,
                maxPoolSize=max_pool_size,
                serverSelectionTimeoutMS=timeout_ms
            )
            
            # Test connection
            self.client.admin.command('ping')
            
            # Get database
            self.database = self.client[database_name]
            
            self.connected = True
            logger.info(f"MongoDB connection established to database: {database_name}")
            return True
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {e}")
            return False
    
    def disconnect(self) -> bool:
        """
        Close MongoDB connection
        
        Returns:
            True if disconnection successful
        """
        if self.client:
            self.client.close()
        self.connected = False
        self.client = None
        self.database = None
        self.collection = None
        return True
    
    def test_connection(self) -> Dict:
        """
        Test MongoDB connection
        
        Returns:
            Dictionary with test results
        """
        result = {
            'success': False,
            'message': '',
            'database': self.config.get('database')
        }
        
        if not self.connected:
            result['message'] = "Not connected. Call connect() first"
            return result
        
        try:
            # Ping server
            self.client.admin.command('ping')
            
            # Get server info
            server_info = self.client.server_info()
            
            result['success'] = True
            result['message'] = "Connection successful"
            result['mongodb_version'] = server_info.get('version')
            result['collections'] = self.database.list_collection_names()
            
        except Exception as e:
            result['message'] = f"Connection test failed: {str(e)}"
            logger.error(f"Test connection failed: {e}")
        
        return result
    
    def fetch_data(self, **kwargs) -> Optional[pd.DataFrame]:
        """
        Fetch data from MongoDB collection
        
        Args:
            **kwargs: Additional parameters
                - collection: Collection name (required if not in config)
                - filter: MongoDB query filter (default: {})
                - projection: Fields to include/exclude
                - limit: Maximum number of documents
                - sort: Sort specification
                
        Returns:
            DataFrame with data or None if failed
        """
        if not self.connected:
            logger.error("Not connected. Call connect() first")
            return None
        
        # Get collection
        collection_name = kwargs.get('collection', self.config.get('collection'))
        if not collection_name:
            logger.error("Collection name is required")
            return None
        
        collection = self.database[collection_name]
        
        try:
            # Build query
            query_filter = kwargs.get('filter', {})
            projection = kwargs.get('projection', None)
            limit = kwargs.get('limit', 0)
            sort = kwargs.get('sort', None)
            
            # Execute query
            cursor = collection.find(query_filter, projection)
            
            if sort:
                cursor = cursor.sort(sort)
            
            if limit > 0:
                cursor = cursor.limit(limit)
            
            # Convert to list
            documents = list(cursor)
            
            if not documents:
                logger.warning("No documents found matching the query")
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(documents)
            
            # Remove MongoDB _id if present and not needed
            if '_id' in df.columns and not kwargs.get('include_id', False):
                df = df.drop('_id', axis=1)
            
            logger.info(f"Successfully fetched {len(df)} documents from collection: {collection_name}")
            
            # Normalize column names
            column_mapping = kwargs.get('column_mapping', {})
            if column_mapping:
                df = self.normalize_dataframe(df, column_mapping)
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return None
    
    def insert_documents(self, collection_name: str, documents: List[Dict]) -> bool:
        """
        Insert documents into collection
        
        Args:
            collection_name: Name of collection
            documents: List of documents to insert
            
        Returns:
            True if insertion successful
        """
        if not self.connected:
            logger.error("Not connected. Call connect() first")
            return False
        
        try:
            collection = self.database[collection_name]
            result = collection.insert_many(documents)
            
            logger.info(f"Inserted {len(result.inserted_ids)} documents")
            return True
            
        except Exception as e:
            logger.error(f"Error inserting documents: {e}")
            return False
    
    def get_collection_info(self, collection_name: str) -> Dict:
        """
        Get information about a collection
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Dictionary with collection information
        """
        info = {
            'collection_name': collection_name,
            'exists': False
        }
        
        if not self.connected:
            info['error'] = "Not connected"
            return info
        
        try:
            # Check if collection exists
            if collection_name in self.database.list_collection_names():
                info['exists'] = True
                
                collection = self.database[collection_name]
                
                # Get document count
                info['document_count'] = collection.count_documents({})
                
                # Get sample document to show structure
                sample = collection.find_one()
                if sample:
                    # Remove _id for cleaner display
                    sample.pop('_id', None)
                    info['sample_fields'] = list(sample.keys())
                
                # Get collection stats
                stats = self.database.command('collStats', collection_name)
                info['size_bytes'] = stats.get('size', 0)
                info['avg_doc_size_bytes'] = stats.get('avgObjSize', 0)
            
        except Exception as e:
            info['error'] = str(e)
        
        return info
    
    def aggregate(self, collection_name: str, pipeline: List[Dict]) -> Optional[pd.DataFrame]:
        """
        Execute aggregation pipeline
        
        Args:
            collection_name: Name of collection
            pipeline: Aggregation pipeline stages
            
        Returns:
            DataFrame with aggregation results
        """
        if not self.connected:
            logger.error("Not connected. Call connect() first")
            return None
        
        try:
            collection = self.database[collection_name]
            results = list(collection.aggregate(pipeline))
            
            if not results:
                return pd.DataFrame()
            
            df = pd.DataFrame(results)
            
            # Remove _id if present
            if '_id' in df.columns:
                df = df.drop('_id', axis=1)
            
            logger.info(f"Aggregation returned {len(df)} results")
            return df
            
        except Exception as e:
            logger.error(f"Error executing aggregation: {e}")
            return None


def create_mongodb_connector(connection_string: str, database: str, **kwargs) -> MongoDBConnector:
    """
    Factory function to create MongoDB connector
    
    Args:
        connection_string: MongoDB connection URI
        database: Database name
        **kwargs: Additional configuration
        
    Returns:
        MongoDBConnector instance
    """
    config = {
        'connection_string': connection_string,
        'database': database,
        **kwargs
    }
    connector = MongoDBConnector(config=config)
    connector.connect()
    return connector

# Made with Bob
