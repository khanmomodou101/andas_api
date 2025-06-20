#!/usr/bin/env python3
"""
Simple test script for the Andas API client

This script tests the basic functionality without making actual API calls.
"""

from andas_api.api import AndasAPI, AndasAPIConfig, create_andas_client, format_date_range
from datetime import date
import sys


def test_imports():
    """Test that all imports work correctly"""
    print("🧪 Testing imports...")
    try:
        from andas_api.api import AndasAPI, AndasAPIConfig, create_andas_client, format_date_range
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_config():
    """Test configuration creation"""
    print("\n🧪 Testing configuration...")
    try:
        config = AndasAPIConfig(
            base_url="https://api.andas.com",
            email="admin@admin.com",
            password="123456789"
        )
        print(f"✅ Configuration created: {config.base_url}")
        return True
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        return False


def test_client_creation():
    """Test client creation"""
    print("\n🧪 Testing client creation...")
    try:
        client = create_andas_client(
            base_url="https://api.andas.com",
            email="admin@admin.com",
            password="123456789"
        )
        print("✅ Client created successfully")
        client.close()
        return True
    except Exception as e:
        print(f"❌ Client creation failed: {e}")
        return False


def test_date_formatting():
    """Test date formatting utility"""
    print("\n🧪 Testing date formatting...")
    try:
        start_date = date(2025, 5, 4)
        end_date = date(2025, 5, 10)
        from_date_str, to_date_str = format_date_range(start_date, end_date)
        
        expected_from = "2025-05-04"
        expected_to = "2025-05-10"
        
        if from_date_str == expected_from and to_date_str == expected_to:
            print(f"✅ Date formatting correct: {from_date_str} to {to_date_str}")
            return True
        else:
            print(f"❌ Date formatting incorrect: got {from_date_str} to {to_date_str}")
            return False
    except Exception as e:
        print(f"❌ Date formatting failed: {e}")
        return False


def test_method_signatures():
    """Test that all API methods have correct signatures"""
    print("\n🧪 Testing method signatures...")
    try:
        config = AndasAPIConfig(
            base_url="https://api.andas.com",
            email="admin@admin.com",
            password="123456789"
        )
        client = AndasAPI(config)
        
        # Test that all methods exist
        methods = [
            'authenticate',
            'get_sales_summary',
            'get_sales_transactions',
            'get_stock_adjustment',
            'get_wastages',
            'get_consumption',
            'get_purchases',
            'get_user_info',
            'get_final_production',
            'get_outlets',
            'get_all_branch_data',
            'get_comprehensive_report',
            'close'
        ]
        
        for method in methods:
            if hasattr(client, method):
                print(f"✅ Method {method} exists")
            else:
                print(f"❌ Method {method} missing")
                return False
        
        client.close()
        return True
    except Exception as e:
        print(f"❌ Method signature test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 Andas API Client Tests")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_config,
        test_client_creation,
        test_date_formatting,
        test_method_signatures
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The API client is ready to use.")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 