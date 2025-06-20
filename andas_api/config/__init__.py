import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, date
from dataclasses import dataclass


@dataclass
class AndasAPIConfig:
    """Configuration for Andas API client"""
    base_url: str
    email: str
    password: str
    timeout: int = 30


class AndasAPI:
    """
    Andas API Client for fetching sales, stock, and business data
    
    This client provides methods to interact with all Andas API endpoints:
    - Authentication
    - Sales Summary and Transactions
    - Stock Adjustments and Wastages
    - Consumption and Purchases
    - User Information and Outlets
    - Final Production Items
    """
    
    def __init__(self, config: AndasAPIConfig):
        self.config = config
        self.session = requests.Session()
        self.access_token = None
        self._authenticated = False
    
    def authenticate(self) -> Dict[str, Any]:
        """
        Authenticate with the Andas API using email and password
        
        Returns:
            Dict containing authentication response with token
        """
        url = f"{self.config.base_url}/api-token"
        payload = {
            "email": self.config.email,
            "password": self.config.password
        }
        
        try:
            response = self.session.post(
                url,
                json=payload,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            
            auth_data = response.json()
            self.access_token = auth_data.get('token')
            self._authenticated = True
            
            # Set authorization header for future requests
            self.session.headers.update({
                'Authorization': f'Bearer {self.access_token}'
            })
            
            return auth_data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Authentication failed: {str(e)}")
    
    def _ensure_authenticated(self):
        """Ensure the client is authenticated before making requests"""
        if not self._authenticated or not self.access_token:
            self.authenticate()
    
    def get_sales_summary(self, branch_id: str, from_date: str, to_date: str) -> Dict[str, Any]:
        """
        Get sales summary for a specific branch and date range
        
        Args:
            branch_id: Branch identifier
            from_date: Start date in YYYY-MM-DD format
            to_date: End date in YYYY-MM-DD format
            
        Returns:
            Dict containing sales summary data
        """
        self._ensure_authenticated()
        
        url = f"{self.config.base_url}/sales-summary"
        params = {
            "branchId": branch_id,
            "from": from_date,
            "to": to_date
        }
        
        try:
            response = self.session.get(url, params=params, timeout=self.config.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch sales summary: {str(e)}")
    
    def get_sales_transactions(self, branch_id: str, from_date: str, to_date: str) -> Dict[str, Any]:
        """
        Get detailed sales transactions for a specific branch and date range
        
        Args:
            branch_id: Branch identifier
            from_date: Start date in YYYY-MM-DD format
            to_date: End date in YYYY-MM-DD format
            
        Returns:
            Dict containing sales transactions data
        """
        self._ensure_authenticated()
        
        url = f"{self.config.base_url}/sales-transaction"
        params = {
            "branchId": branch_id,
            "from": from_date,
            "to": to_date
        }
        
        try:
            response = self.session.get(url, params=params, timeout=self.config.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch sales transactions: {str(e)}")
    
    def get_stock_adjustment(self, branch_id: str, from_date: str, to_date: str) -> Dict[str, Any]:
        """
        Get stock adjustment data for a specific branch and date range
        
        Args:
            branch_id: Branch identifier
            from_date: Start date in YYYY-MM-DD format
            to_date: End date in YYYY-MM-DD format
            
        Returns:
            Dict containing stock adjustment data
        """
        self._ensure_authenticated()
        
        url = f"{self.config.base_url}/stock-adjustment"
        params = {
            "branchId": branch_id,
            "from": from_date,
            "to": to_date
        }
        
        try:
            response = self.session.get(url, params=params, timeout=self.config.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch stock adjustment: {str(e)}")
    
    def get_wastages(self, branch_id: str, from_date: str, to_date: str) -> Dict[str, Any]:
        """
        Get wastage data for a specific branch and date range
        
        Args:
            branch_id: Branch identifier
            from_date: Start date in YYYY-MM-DD format
            to_date: End date in YYYY-MM-DD format
            
        Returns:
            Dict containing wastage data
        """
        self._ensure_authenticated()
        
        url = f"{self.config.base_url}/wastages"
        params = {
            "branchId": branch_id,
            "from": from_date,
            "to": to_date
        }
        
        try:
            response = self.session.get(url, params=params, timeout=self.config.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch wastages: {str(e)}")
    
    def get_consumption(self, branch_id: str, from_date: str, to_date: str) -> Dict[str, Any]:
        """
        Get consumption data for a specific branch and date range
        
        Args:
            branch_id: Branch identifier
            from_date: Start date in YYYY-MM-DD format
            to_date: End date in YYYY-MM-DD format
            
        Returns:
            Dict containing consumption data
        """
        self._ensure_authenticated()
        
        url = f"{self.config.base_url}/consumption"
        params = {
            "branchId": branch_id,
            "from": from_date,
            "to": to_date
        }
        
        try:
            response = self.session.get(url, params=params, timeout=self.config.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch consumption: {str(e)}")
    
    def get_purchases(self, from_date: str, to_date: str) -> Dict[str, Any]:
        """
        Get purchase data for a specific date range (no branch filter)
        
        Args:
            from_date: Start date in YYYY-MM-DD format
            to_date: End date in YYYY-MM-DD format
            
        Returns:
            Dict containing purchase data
        """
        self._ensure_authenticated()
        
        url = f"{self.config.base_url}/purchases"
        params = {
            "from": from_date,
            "to": to_date
        }
        
        try:
            response = self.session.get(url, params=params, timeout=self.config.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch purchases: {str(e)}")
    
    def get_user_info(self) -> Dict[str, Any]:
        """
        Get authenticated user information
        
        Returns:
            Dict containing user information
        """
        self._ensure_authenticated()
        
        url = f"{self.config.base_url}/user"
        
        try:
            response = self.session.get(url, timeout=self.config.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch user info: {str(e)}")
    
    def get_final_production(self) -> Dict[str, Any]:
        """
        Get final production items data
        
        Returns:
            Dict containing final production items data
        """
        self._ensure_authenticated()
        
        url = f"{self.config.base_url}/final-production"
        
        try:
            response = self.session.get(url, timeout=self.config.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch final production: {str(e)}")
    
    def get_outlets(self) -> Dict[str, Any]:
        """
        Get outlets/branches information
        
        Returns:
            Dict containing outlets/branches data
        """
        self._ensure_authenticated()
        
        url = f"{self.config.base_url}/get-outlets"
        
        try:
            response = self.session.post(url, timeout=self.config.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch outlets: {str(e)}")
    
    def get_all_branch_data(self, branch_id: str, from_date: str, to_date: str) -> Dict[str, Any]:
        """
        Get comprehensive data for a specific branch including sales, stock, and consumption
        
        Args:
            branch_id: Branch identifier
            from_date: Start date in YYYY-MM-DD format
            to_date: End date in YYYY-MM-DD format
            
        Returns:
            Dict containing all branch-related data
        """
        try:
            return {
                "sales_summary": self.get_sales_summary(branch_id, from_date, to_date),
                "sales_transactions": self.get_sales_transactions(branch_id, from_date, to_date),
                "stock_adjustment": self.get_stock_adjustment(branch_id, from_date, to_date),
                "wastages": self.get_wastages(branch_id, from_date, to_date),
                "consumption": self.get_consumption(branch_id, from_date, to_date)
            }
        except Exception as e:
            raise Exception(f"Failed to fetch all branch data: {str(e)}")
    
    def get_comprehensive_report(self, from_date: str, to_date: str, branch_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get comprehensive business report including all data types
        
        Args:
            from_date: Start date in YYYY-MM-DD format
            to_date: End date in YYYY-MM-DD format
            branch_ids: Optional list of branch IDs to filter by
            
        Returns:
            Dict containing comprehensive business report
        """
        try:
            report = {
                "purchases": self.get_purchases(from_date, to_date),
                "final_production": self.get_final_production(),
                "outlets": self.get_outlets(),
                "user_info": self.get_user_info()
            }
            
            # If branch IDs provided, get branch-specific data
            if branch_ids:
                report["branch_data"] = {}
                for branch_id in branch_ids:
                    report["branch_data"][branch_id] = self.get_all_branch_data(branch_id, from_date, to_date)
            
            return report
        except Exception as e:
            raise Exception(f"Failed to generate comprehensive report: {str(e)}")
    
    def close(self):
        """Close the session and clean up resources"""
        if self.session:
            self.session.close()


# Example usage and utility functions
def create_andas_client(base_url: str, email: str, password: str) -> AndasAPI:
    """
    Create and configure an Andas API client
    
    Args:
        base_url: Base URL for the Andas API
        email: User email for authentication
        password: User password for authentication
        
    Returns:
        Configured AndasAPI client instance
    """
    config = AndasAPIConfig(
        base_url=base_url,
        email=email,
        password=password
    )
    return AndasAPI(config)


def format_date_range(start_date: date, end_date: date) -> tuple:
    """
    Format date objects to string format expected by API
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        Tuple of (from_date_str, to_date_str)
    """
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


# Example usage
if __name__ == "__main__":
    # Example configuration
    config = AndasAPIConfig(
        base_url="https://api.andas.com",  # Replace with actual base URL
        email="admin@admin.com",
        password="123456789"
    )
    
    # Create client
    client = AndasAPI(config)
    
    try:
        # Authenticate
        auth_result = client.authenticate()
        print("Authentication successful:", auth_result)
        
        # Get sales summary for a specific branch
        sales_summary = client.get_sales_summary(
            branch_id="10002",
            from_date="2025-05-04",
            to_date="2025-05-10"
        )
        print("Sales Summary:", sales_summary)
        
        # Get comprehensive report
        report = client.get_comprehensive_report(
            from_date="2025-05-04",
            to_date="2025-05-10",
            branch_ids=["10002", "10006"]
        )
        print("Comprehensive Report:", report)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
