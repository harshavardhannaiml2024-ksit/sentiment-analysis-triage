"""
REST API Connector
Handle REST API connections with authentication
"""

import requests
import pandas as pd
from typing import Dict, Optional, List
import logging
import time
from .base_connector import BaseConnector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIConnector(BaseConnector):
    """
    Connector for REST APIs
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize API connector
        
        Args:
            config: Configuration dictionary with:
                - endpoint: API endpoint URL
                - auth_type: 'none', 'api_key', 'bearer', 'basic'
                - api_key: API key (if auth_type is 'api_key')
                - token: Bearer token (if auth_type is 'bearer')
                - username: Username (if auth_type is 'basic')
                - password: Password (if auth_type is 'basic')
                - headers: Additional headers
                - timeout: Request timeout in seconds
                - max_retries: Maximum number of retries
        """
        super().__init__(config)
        self.session = None
        self.endpoint = None
        self.auth_type = None
        
    def connect(self) -> bool:
        """
        Initialize API session
        
        Returns:
            True if session initialized successfully
        """
        # Validate required config
        validation = self.validate_config(['endpoint'])
        if not validation['valid']:
            logger.error(f"Configuration validation failed: {validation['errors']}")
            return False
        
        self.endpoint = self.config['endpoint']
        self.auth_type = self.config.get('auth_type', 'none')
        
        # Create session
        self.session = requests.Session()
        
        # Set up authentication
        if self.auth_type == 'api_key':
            api_key = self.config.get('api_key')
            if not api_key:
                logger.error("API key required but not provided")
                return False
            self.session.headers.update({'X-API-Key': api_key})
            
        elif self.auth_type == 'bearer':
            token = self.config.get('token')
            if not token:
                logger.error("Bearer token required but not provided")
                return False
            self.session.headers.update({'Authorization': f'Bearer {token}'})
            
        elif self.auth_type == 'basic':
            username = self.config.get('username')
            password = self.config.get('password')
            if not username or not password:
                logger.error("Username and password required for basic auth")
                return False
            self.session.auth = (username, password)
        
        # Add custom headers
        custom_headers = self.config.get('headers', {})
        self.session.headers.update(custom_headers)
        
        self.connected = True
        logger.info(f"API connector initialized for {self.endpoint}")
        return True
    
    def disconnect(self) -> bool:
        """
        Close API session
        
        Returns:
            True if disconnection successful
        """
        if self.session:
            self.session.close()
        self.connected = False
        self.session = None
        return True
    
    def test_connection(self) -> Dict:
        """
        Test API connection
        
        Returns:
            Dictionary with test results
        """
        result = {
            'success': False,
            'message': '',
            'endpoint': self.endpoint,
            'auth_type': self.auth_type
        }
        
        if not self.connected:
            result['message'] = "Not connected. Call connect() first"
            return result
        
        try:
            timeout = self.config.get('timeout', 30)
            response = self.session.get(self.endpoint, timeout=timeout)
            
            result['status_code'] = response.status_code
            result['response_time_ms'] = response.elapsed.total_seconds() * 1000
            
            if response.status_code == 200:
                result['success'] = True
                result['message'] = "Connection successful"
            else:
                result['message'] = f"Connection failed with status {response.status_code}"
                
        except requests.exceptions.Timeout:
            result['message'] = "Connection timeout"
        except requests.exceptions.ConnectionError:
            result['message'] = "Connection error - unable to reach endpoint"
        except Exception as e:
            result['message'] = f"Error: {str(e)}"
        
        return result
    
    def fetch_data(self, **kwargs) -> Optional[pd.DataFrame]:
        """
        Fetch data from API
        
        Args:
            **kwargs: Additional parameters
                - method: HTTP method (default: 'GET')
                - params: Query parameters
                - json_path: Path to data in JSON response
                - pagination: Enable pagination (default: False)
                - page_param: Parameter name for page number
                - limit_param: Parameter name for limit
                - max_pages: Maximum pages to fetch
                
        Returns:
            DataFrame with data or None if failed
        """
        if not self.connected:
            logger.error("Not connected. Call connect() first")
            return None
        
        try:
            method = kwargs.get('method', 'GET').upper()
            params = kwargs.get('params', {})
            json_path = kwargs.get('json_path', 'data')
            timeout = self.config.get('timeout', 30)
            max_retries = self.config.get('max_retries', 3)
            
            all_data = []
            
            # Handle pagination
            if kwargs.get('pagination', False):
                page_param = kwargs.get('page_param', 'page')
                limit_param = kwargs.get('limit_param', 'limit')
                max_pages = kwargs.get('max_pages', 10)
                
                for page in range(1, max_pages + 1):
                    params[page_param] = page
                    
                    data = self._make_request(method, params, timeout, max_retries)
                    if data is None:
                        break
                    
                    # Extract data from JSON path
                    page_data = self._extract_json_path(data, json_path)
                    if not page_data:
                        break
                    
                    all_data.extend(page_data if isinstance(page_data, list) else [page_data])
                    
                    # Check if there are more pages
                    if len(page_data) == 0:
                        break
            else:
                # Single request
                data = self._make_request(method, params, timeout, max_retries)
                if data is None:
                    return None
                
                # Extract data from JSON path
                extracted_data = self._extract_json_path(data, json_path)
                all_data = extracted_data if isinstance(extracted_data, list) else [extracted_data]
            
            # Convert to DataFrame
            if not all_data:
                logger.warning("No data received from API")
                return pd.DataFrame()
            
            df = pd.DataFrame(all_data)
            logger.info(f"Successfully fetched {len(df)} rows from API")
            
            # Normalize column names
            column_mapping = kwargs.get('column_mapping', {})
            if column_mapping:
                df = self.normalize_dataframe(df, column_mapping)
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return None
    
    def _make_request(self, method: str, params: Dict, 
                     timeout: int, max_retries: int) -> Optional[Dict]:
        """
        Make HTTP request with retry logic
        
        Args:
            method: HTTP method
            params: Query parameters
            timeout: Request timeout
            max_retries: Maximum retries
            
        Returns:
            JSON response or None
        """
        retry_delay = self.config.get('retry_delay', 2)
        
        for attempt in range(max_retries):
            try:
                if method == 'GET':
                    response = self.session.get(
                        self.endpoint,
                        params=params,
                        timeout=timeout
                    )
                elif method == 'POST':
                    response = self.session.post(
                        self.endpoint,
                        json=params,
                        timeout=timeout
                    )
                else:
                    logger.error(f"Unsupported HTTP method: {method}")
                    return None
                
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.HTTPError as e:
                logger.warning(f"HTTP error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    logger.error("Max retries reached")
                    return None
                    
            except Exception as e:
                logger.error(f"Request error: {e}")
                return None
        
        return None
    
    def _extract_json_path(self, data: Dict, path: str) -> any:
        """
        Extract data from nested JSON using dot notation
        
        Args:
            data: JSON data
            path: Dot-separated path (e.g., 'data.items')
            
        Returns:
            Extracted data
        """
        if not path:
            return data
        
        keys = path.split('.')
        result = data
        
        for key in keys:
            if isinstance(result, dict) and key in result:
                result = result[key]
            else:
                logger.warning(f"Path '{path}' not found in response")
                return None
        
        return result


def create_api_connector(endpoint: str, auth_type: str = 'none', **kwargs) -> APIConnector:
    """
    Factory function to create API connector
    
    Args:
        endpoint: API endpoint URL
        auth_type: Authentication type
        **kwargs: Additional configuration
        
    Returns:
        APIConnector instance
    """
    config = {
        'endpoint': endpoint,
        'auth_type': auth_type,
        **kwargs
    }
    connector = APIConnector(config=config)
    connector.connect()
    return connector

# Made with Bob
