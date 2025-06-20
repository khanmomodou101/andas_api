import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, date
from dataclasses import dataclass
import frappe


    

@frappe.whitelist(allow_guest=True)
def authenticate() -> Dict[str, Any]:
    """
    Authenticate with the Andas API using email and password
    
    Returns:
        Dict containing authentication response with token
    """
    url = "https://andaserp.com/api/v1/api-token"
    
    payload = {
        "email": "support@powersoftsystem.com",
        "password": "]q36&2y1VPrz"
    }
    
    try:
        response = requests.post(
            url,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        # Debug: Log the response content to see what we're getting
        frappe.logger().info(f"Andas API Response Status: {response.status_code}")
        frappe.logger().info(f"Andas API Response Headers: {dict(response.headers)}")
        frappe.logger().info(f"Andas API Response Content: {response.text}")
        
        # Handle the specific response format: "user_id|token"
        response_text = response.text.strip()
        
        if '|' in response_text:
            # Parse the pipe-separated format: "user_id|token"
            parts = response_text.split('|')
            if len(parts) == 2:
                user_id, token = parts
                return {
                    "user_id": user_id,
                    "token": token,
                    "success": True
                }
            else:
                return {
                    "error": "Invalid response format - expected 'user_id|token'",
                    "response_text": response_text
                }
        else:
            # Try to parse as JSON first
            try:
                auth_data = response.json()
                return auth_data
            except requests.exceptions.JSONDecodeError:
                # If it's not JSON and doesn't have pipe, return the raw response
                return {
                    "error": "Unexpected response format",
                    "response_text": response_text,
                    "status_code": response.status_code
                }
        
    except requests.exceptions.RequestException as e:
        frappe.log_error(frappe.get_traceback(), "Andas API Authentication Error")
        return {
            "error": "Request failed",
            "exception": str(e),
            "url": url
        }


@frappe.whitelist(allow_guest=True)
def get_sales_summary() -> Dict[str, Any]:
    """
    Get sales summary for a specific branch and date range
    
    Args:
        branch_id: Branch identifier
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
        access_token: Authentication token
        
    Returns:
        Dict containing sales summary data
    """

    auth_result = authenticate()
    if "error" in auth_result:
        return auth_result
    access_token = auth_result.get('token')
    
    url = "https://andaserp.com/api/v1/sales-summary"
    params = {
        "branchId": "10002",
        "from": "2025-05-04",
        "to": "2025-05-10"
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Handle both JSON and non-JSON responses
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            # If not JSON, return the raw response for debugging
            return {
                "error": "Non-JSON response received",
                "response_text": response.text[:500],
                "status_code": response.status_code
            }
            
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Andas API Sales Summary Error")
        return str(e)

def get_sales_transactions(branch_id: str, from_date: str, to_date: str, access_token: str = None) -> Dict[str, Any]:
    """
    Get detailed sales transactions for a specific branch and date range
    
    Args:
        branch_id: Branch identifier
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
        access_token: Authentication token
        
    Returns:
        Dict containing sales transactions data
    """
    if not access_token:
        auth_result = authenticate()
        if "error" in auth_result:
            return auth_result
        access_token = auth_result.get('token')
    
    url = "https://andaserp.com/api/v1/sales-transaction"
    params = {
        "branchId": branch_id,
        "from": from_date,
        "to": to_date
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {
                "error": "Non-JSON response received",
                "response_text": response.text[:500],
                "status_code": response.status_code
            }
            
    except requests.exceptions.RequestException as e:
        frappe.log_error(frappe.get_traceback(), "Andas API Sales Transactions Error")
        return {
            "error": f"Failed to fetch sales transactions: {str(e)}"
        }

def get_stock_adjustment(branch_id: str, from_date: str, to_date: str, access_token: str = None) -> Dict[str, Any]:
    """
    Get stock adjustment data for a specific branch and date range
    
    Args:
        branch_id: Branch identifier
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
        access_token: Authentication token
        
    Returns:
        Dict containing stock adjustment data
    """
    if not access_token:
        auth_result = authenticate()
        if "error" in auth_result:
            return auth_result
        access_token = auth_result.get('token')
    
    url = "https://andaserp.com/api/v1/stock-adjustment"
    params = {
        "branchId": branch_id,
        "from": from_date,
        "to": to_date
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {
                "error": "Non-JSON response received",
                "response_text": response.text[:500],
                "status_code": response.status_code
            }
            
    except requests.exceptions.RequestException as e:
        frappe.log_error(frappe.get_traceback(), "Andas API Stock Adjustment Error")
        return {
            "error": f"Failed to fetch stock adjustment: {str(e)}"
        }

def get_wastages(branch_id: str, from_date: str, to_date: str, access_token: str = None) -> Dict[str, Any]:
    """
    Get wastage data for a specific branch and date range
    
    Args:
        branch_id: Branch identifier
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
        access_token: Authentication token
        
    Returns:
        Dict containing wastage data
    """
    if not access_token:
        auth_result = authenticate()
        if "error" in auth_result:
            return auth_result
        access_token = auth_result.get('token')
    
    url = "https://andaserp.com/api/v1/wastages"
    params = {
        "branchId": branch_id,
        "from": from_date,
        "to": to_date
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {
                "error": "Non-JSON response received",
                "response_text": response.text[:500],
                "status_code": response.status_code
            }
            
    except requests.exceptions.RequestException as e:
        frappe.log_error(frappe.get_traceback(), "Andas API Wastages Error")
        return {
            "error": f"Failed to fetch wastages: {str(e)}"
        }

def get_consumption(branch_id: str, from_date: str, to_date: str, access_token: str = None) -> Dict[str, Any]:
    """
    Get consumption data for a specific branch and date range
    
    Args:
        branch_id: Branch identifier
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
        access_token: Authentication token
        
    Returns:
        Dict containing consumption data
    """
    if not access_token:
        auth_result = authenticate()
        if "error" in auth_result:
            return auth_result
        access_token = auth_result.get('token')
    
    url = "https://andaserp.com/api/v1/consumption"
    params = {
        "branchId": branch_id,
        "from": from_date,
        "to": to_date
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {
                "error": "Non-JSON response received",
                "response_text": response.text[:500],
                "status_code": response.status_code
            }
            
    except requests.exceptions.RequestException as e:
        frappe.log_error(frappe.get_traceback(), "Andas API Consumption Error")
        return {
            "error": f"Failed to fetch consumption: {str(e)}"
        }

def get_purchases(from_date: str, to_date: str, access_token: str = None) -> Dict[str, Any]:
    """
    Get purchase data for a specific date range (no branch filter)
    
    Args:
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
        access_token: Authentication token
        
    Returns:
        Dict containing purchase data
    """
    if not access_token:
        auth_result = authenticate()
        if "error" in auth_result:
            return auth_result
        access_token = auth_result.get('token')
    
    url = "https://andaserp.com/api/v1/purchases"
    params = {
        "from": from_date,
        "to": to_date
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {
                "error": "Non-JSON response received",
                "response_text": response.text[:500],
                "status_code": response.status_code
            }
            
    except requests.exceptions.RequestException as e:
        frappe.log_error(frappe.get_traceback(), "Andas API Purchases Error")
        return {
            "error": f"Failed to fetch purchases: {str(e)}"
        }

def get_user_info(access_token: str = None) -> Dict[str, Any]:
    """
    Get authenticated user information
    
    Args:
        access_token: Authentication token
        
    Returns:
        Dict containing user information
    """
    if not access_token:
        auth_result = authenticate()
        if "error" in auth_result:
            return auth_result
        access_token = auth_result.get('token')
    
    url = "https://andaserp.com/api/v1/user"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {
                "error": "Non-JSON response received",
                "response_text": response.text[:500],
                "status_code": response.status_code
            }
            
    except requests.exceptions.RequestException as e:
        frappe.log_error(frappe.get_traceback(), "Andas API User Info Error")
        return {
            "error": f"Failed to fetch user info: {str(e)}"
        }

def get_final_production(access_token: str = None) -> Dict[str, Any]:
    """
    Get final production items data
    
    Args:
        access_token: Authentication token
        
    Returns:
        Dict containing final production items data
    """
    if not access_token:
        auth_result = authenticate()
        if "error" in auth_result:
            return auth_result
        access_token = auth_result.get('token')
    
    url = "https://andaserp.com/api/v1/final-production"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {
                "error": "Non-JSON response received",
                "response_text": response.text[:500],
                "status_code": response.status_code
            }
            
    except requests.exceptions.RequestException as e:
        frappe.log_error(frappe.get_traceback(), "Andas API Final Production Error")
        return {
            "error": f"Failed to fetch final production: {str(e)}"
        }

def get_outlets(access_token: str = None) -> Dict[str, Any]:
    """
    Get outlets/branches information
    
    Args:
        access_token: Authentication token
        
    Returns:
        Dict containing outlets/branches data
    """
    if not access_token:
        auth_result = authenticate()
        if "error" in auth_result:
            return auth_result
        access_token = auth_result.get('token')
    
    url = "https://andaserp.com/api/v1/get-outlets"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {
                "error": "Non-JSON response received",
                "response_text": response.text[:500],
                "status_code": response.status_code
            }
            
    except requests.exceptions.RequestException as e:
        frappe.log_error(frappe.get_traceback(), "Andas API Outlets Error")
        return {
            "error": f"Failed to fetch outlets: {str(e)}"
        }

def get_all_branch_data(branch_id: str, from_date: str, to_date: str, access_token: str = None) -> Dict[str, Any]:
    """
    Get comprehensive data for a specific branch including sales, stock, and consumption
    
    Args:
        branch_id: Branch identifier
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
        access_token: Authentication token
        
    Returns:
        Dict containing all branch-related data
    """
    try:
        return {
            "sales_summary": get_sales_summary(branch_id, from_date, to_date, access_token),
            "sales_transactions": get_sales_transactions(branch_id, from_date, to_date, access_token),
            "stock_adjustment": get_stock_adjustment(branch_id, from_date, to_date, access_token),
            "wastages": get_wastages(branch_id, from_date, to_date, access_token),
            "consumption": get_consumption(branch_id, from_date, to_date, access_token)
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Andas API All Branch Data Error")
        return {
            "error": f"Failed to fetch all branch data: {str(e)}"
        }

def get_comprehensive_report(from_date: str, to_date: str, branch_ids: Optional[List[str]] = None, access_token: str = None) -> Dict[str, Any]:
    """
    Get comprehensive business report including all data types
    
    Args:
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
        branch_ids: Optional list of branch IDs to filter by
        access_token: Authentication token
        
    Returns:
        Dict containing comprehensive business report
    """
    try:
        report = {
            "purchases": get_purchases(from_date, to_date, access_token),
            "final_production": get_final_production(access_token),
            "outlets": get_outlets(access_token),
            "user_info": get_user_info(access_token)
        }
        
        # If branch IDs provided, get branch-specific data
        if branch_ids:
            report["branch_data"] = {}
            for branch_id in branch_ids:
                report["branch_data"][branch_id] = get_all_branch_data(branch_id, from_date, to_date, access_token)
        
        return report
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Andas API Comprehensive Report Error")
        return {
            "error": f"Failed to generate comprehensive report: {str(e)}"
        }

@frappe.whitelist(allow_guest=True)
def test_authentication_and_sales():
    """
    Test function to verify authentication works and test sales summary endpoint
    """
    try:
        # Step 1: Test authentication
        print("🔐 Testing authentication...")
        auth_result = authenticate()
        
        if "error" in auth_result:
            return {
                "success": False,
                "step": "authentication",
                "error": auth_result
            }
        
        print(f"✅ Authentication successful!")
        print(f"   User ID: {auth_result.get('user_id')}")
        print(f"   Token: {auth_result.get('token')[:20]}...")
        
        # Step 2: Test sales summary with the token
        print("📊 Testing sales summary...")
        sales_result = get_sales_summary(
            branch_id="10002",
            from_date="2025-05-04",
            to_date="2025-05-10",
            access_token=auth_result.get('token')
        )
        
        if "error" in sales_result:
            return {
                "success": False,
                "step": "sales_summary",
                "auth_result": auth_result,
                "error": sales_result
            }
        
        return {
            "success": True,
            "auth_result": auth_result,
            "sales_result": sales_result
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": frappe.get_traceback()
        }


#