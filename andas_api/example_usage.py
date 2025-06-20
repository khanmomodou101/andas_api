#!/usr/bin/env python3
"""
Example usage of the Andas API client

This file demonstrates how to use all the endpoints in the Andas API collection
to fetch data from the external system.
"""

import sys
import os
from datetime import datetime, date, timedelta
from typing import Dict, Any

# Import the AndasAPI classes from the apipy module
from andas_api.api import AndasAPI, AndasAPIConfig, create_andas_client, format_date_range


def example_authentication():
    """Example of how to authenticate with the Andas API"""
    print("=== Authentication Example ===")
    
    # Create configuration
    config = AndasAPIConfig(
        base_url="https://api.andas.com",  # Replace with actual base URL
        email="admin@admin.com",
        password="123456789"
    )
    
    # Create client and authenticate
    client = AndasAPI(config)
    
    try:
        auth_result = client.authenticate()
        print(f"✅ Authentication successful!")
        print(f"Token: {auth_result.get('token', 'N/A')[:20]}...")
        return client
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return None


def example_sales_data(client: AndasAPI):
    """Example of fetching sales-related data"""
    print("\n=== Sales Data Examples ===")
    
    # Date range for the examples
    from_date = "2025-05-04"
    to_date = "2025-05-10"
    branch_id = "10002"
    
    try:
        # Get sales summary
        print("📊 Fetching sales summary...")
        sales_summary = client.get_sales_summary(branch_id, from_date, to_date)
        print(f"✅ Sales summary retrieved: {len(sales_summary) if isinstance(sales_summary, dict) else 'N/A'} fields")
        
        # Get detailed sales transactions
        print("📋 Fetching sales transactions...")
        sales_transactions = client.get_sales_transactions(branch_id, from_date, to_date)
        print(f"✅ Sales transactions retrieved: {len(sales_transactions) if isinstance(sales_transactions, dict) else 'N/A'} fields")
        
        return sales_summary, sales_transactions
        
    except Exception as e:
        print(f"❌ Failed to fetch sales data: {e}")
        return None, None


def example_stock_data(client: AndasAPI):
    """Example of fetching stock-related data"""
    print("\n=== Stock Data Examples ===")
    
    # Date range for the examples
    from_date = "2025-05-04"
    to_date = "2025-05-10"
    branch_id = "10006"  # Different branch for stock data
    
    try:
        # Get stock adjustments
        print("📦 Fetching stock adjustments...")
        stock_adjustments = client.get_stock_adjustment(branch_id, from_date, to_date)
        print(f"✅ Stock adjustments retrieved: {len(stock_adjustments) if isinstance(stock_adjustments, dict) else 'N/A'} fields")
        
        # Get wastages
        print("🗑️ Fetching wastages...")
        wastages = client.get_wastages(branch_id, from_date, to_date)
        print(f"✅ Wastages retrieved: {len(wastages) if isinstance(wastages, dict) else 'N/A'} fields")
        
        return stock_adjustments, wastages
        
    except Exception as e:
        print(f"❌ Failed to fetch stock data: {e}")
        return None, None


def example_consumption_and_purchases(client: AndasAPI):
    """Example of fetching consumption and purchase data"""
    print("\n=== Consumption & Purchases Examples ===")
    
    # Date range for the examples
    from_date = "2021-05-04"
    to_date = "2025-06-10"
    branch_id = "10002"
    
    try:
        # Get consumption data
        print("🍽️ Fetching consumption data...")
        consumption = client.get_consumption(branch_id, from_date, to_date)
        print(f"✅ Consumption data retrieved: {len(consumption) if isinstance(consumption, dict) else 'N/A'} fields")
        
        # Get purchases data (no branch filter)
        print("🛒 Fetching purchases data...")
        purchases = client.get_purchases(from_date, to_date)
        print(f"✅ Purchases data retrieved: {len(purchases) if isinstance(purchases, dict) else 'N/A'} fields")
        
        return consumption, purchases
        
    except Exception as e:
        print(f"❌ Failed to fetch consumption/purchases data: {e}")
        return None, None


def example_user_and_system_data(client: AndasAPI):
    """Example of fetching user and system data"""
    print("\n=== User & System Data Examples ===")
    
    try:
        # Get user information
        print("👤 Fetching user information...")
        user_info = client.get_user_info()
        print(f"✅ User info retrieved: {len(user_info) if isinstance(user_info, dict) else 'N/A'} fields")
        
        # Get final production items
        print("🏭 Fetching final production items...")
        final_production = client.get_final_production()
        print(f"✅ Final production items retrieved: {len(final_production) if isinstance(final_production, dict) else 'N/A'} fields")
        
        # Get outlets/branches
        print("🏪 Fetching outlets/branches...")
        outlets = client.get_outlets()
        print(f"✅ Outlets retrieved: {len(outlets) if isinstance(outlets, dict) else 'N/A'} fields")
        
        return user_info, final_production, outlets
        
    except Exception as e:
        print(f"❌ Failed to fetch user/system data: {e}")
        return None, None, None


def example_comprehensive_report(client: AndasAPI):
    """Example of generating a comprehensive business report"""
    print("\n=== Comprehensive Report Example ===")
    
    # Date range for the report
    from_date = "2025-05-04"
    to_date = "2025-05-10"
    branch_ids = ["10002", "10006"]
    
    try:
        print("📈 Generating comprehensive business report...")
        report = client.get_comprehensive_report(from_date, to_date, branch_ids)
        
        print("✅ Comprehensive report generated successfully!")
        print(f"📊 Report contains:")
        print(f"   - Purchases data: {'✅' if 'purchases' in report else '❌'}")
        print(f"   - Final production: {'✅' if 'final_production' in report else '❌'}")
        print(f"   - Outlets data: {'✅' if 'outlets' in report else '❌'}")
        print(f"   - User info: {'✅' if 'user_info' in report else '❌'}")
        print(f"   - Branch data: {'✅' if 'branch_data' in report else '❌'}")
        
        if 'branch_data' in report:
            for branch_id, branch_data in report['branch_data'].items():
                print(f"     - Branch {branch_id}: {len(branch_data)} data types")
        
        return report
        
    except Exception as e:
        print(f"❌ Failed to generate comprehensive report: {e}")
        return None


def example_branch_specific_data(client: AndasAPI):
    """Example of fetching all data for a specific branch"""
    print("\n=== Branch-Specific Data Example ===")
    
    branch_id = "10002"
    from_date = "2025-05-04"
    to_date = "2025-05-10"
    
    try:
        print(f"🏪 Fetching all data for branch {branch_id}...")
        branch_data = client.get_all_branch_data(branch_id, from_date, to_date)
        
        print(f"✅ All branch data retrieved for branch {branch_id}!")
        print(f"📊 Branch data contains:")
        for data_type in branch_data.keys():
            print(f"   - {data_type}: {'✅' if branch_data[data_type] else '❌'}")
        
        return branch_data
        
    except Exception as e:
        print(f"❌ Failed to fetch branch data: {e}")
        return None


def example_utility_functions():
    """Example of using utility functions"""
    print("\n=== Utility Functions Example ===")
    
    # Example of creating client using utility function
    print("🔧 Creating client using utility function...")
    client = create_andas_client(
        base_url="https://api.andas.com",
        email="admin@admin.com",
        password="123456789"
    )
    
    # Example of date formatting
    print("📅 Formatting date range...")
    start_date = date(2025, 5, 4)
    end_date = date(2025, 5, 10)
    from_date_str, to_date_str = format_date_range(start_date, end_date)
    print(f"   Start date: {start_date} -> {from_date_str}")
    print(f"   End date: {end_date} -> {to_date_str}")
    
    return client


def main():
    """Main function to run all examples"""
    print("🚀 Andas API Client Examples")
    print("=" * 50)
    
    # Example 1: Authentication
    client = example_authentication()
    if not client:
        print("❌ Cannot proceed without authentication")
        return
    
    # Example 2: Sales data
    example_sales_data(client)
    
    # Example 3: Stock data
    example_stock_data(client)
    
    # Example 4: Consumption and purchases
    example_consumption_and_purchases(client)
    
    # Example 5: User and system data
    example_user_and_system_data(client)
    
    # Example 6: Comprehensive report
    example_comprehensive_report(client)
    
    # Example 7: Branch-specific data
    example_branch_specific_data(client)
    
    # Example 8: Utility functions
    example_utility_functions()
    
    # Clean up
    client.close()
    print("\n✅ All examples completed successfully!")
    print("🔧 Remember to replace the base URL and credentials with actual values")


if __name__ == "__main__":
    main() 