# Andas API Client

A comprehensive Python client for interacting with the Andas API to fetch sales, stock, and business data from external systems.

## Features

- 🔐 **Authentication**: Secure token-based authentication
- 📊 **Sales Data**: Sales summaries and detailed transactions
- 📦 **Stock Management**: Stock adjustments and wastage tracking
- 🍽️ **Consumption**: Food consumption data
- 🛒 **Purchases**: Purchase order data
- 👤 **User Management**: User information and access control
- 🏪 **Outlet Management**: Branch/outlet information
- 🏭 **Production**: Final production items data
- 📈 **Comprehensive Reports**: Generate complete business reports

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Import the API client:
```python
from apipy import AndasAPI, AndasAPIConfig
```

## Quick Start

```python
from apipy import AndasAPI, AndasAPIConfig

# Create configuration
config = AndasAPIConfig(
    base_url="https://api.andas.com",  # Replace with actual base URL
    email="admin@admin.com",
    password="123456789"
)

# Create client and authenticate
client = AndasAPI(config)
auth_result = client.authenticate()

# Fetch sales summary
sales_summary = client.get_sales_summary(
    branch_id="10002",
    from_date="2025-05-04",
    to_date="2025-05-10"
)

# Clean up
client.close()
```

## API Endpoints

### 1. Authentication
```python
# Authenticate and get access token
auth_result = client.authenticate()
```

### 2. Sales Data
```python
# Get sales summary for a branch
sales_summary = client.get_sales_summary(
    branch_id="10002",
    from_date="2025-05-04",
    to_date="2025-05-10"
)

# Get detailed sales transactions
sales_transactions = client.get_sales_transactions(
    branch_id="10002",
    from_date="2025-05-04",
    to_date="2025-05-10"
)
```

### 3. Stock Management
```python
# Get stock adjustments
stock_adjustments = client.get_stock_adjustment(
    branch_id="10006",
    from_date="2025-05-04",
    to_date="2025-05-10"
)

# Get wastage data
wastages = client.get_wastages(
    branch_id="10006",
    from_date="2025-05-04",
    to_date="2025-05-10"
)
```

### 4. Consumption & Purchases
```python
# Get consumption data
consumption = client.get_consumption(
    branch_id="10002",
    from_date="2021-05-04",
    to_date="2025-06-10"
)

# Get purchases (no branch filter)
purchases = client.get_purchases(
    from_date="2021-05-04",
    to_date="2025-05-10"
)
```

### 5. User & System Data
```python
# Get user information
user_info = client.get_user_info()

# Get final production items
final_production = client.get_final_production()

# Get outlets/branches
outlets = client.get_outlets()
```

### 6. Comprehensive Data
```python
# Get all data for a specific branch
branch_data = client.get_all_branch_data(
    branch_id="10002",
    from_date="2025-05-04",
    to_date="2025-05-10"
)

# Generate comprehensive business report
report = client.get_comprehensive_report(
    from_date="2025-05-04",
    to_date="2025-05-10",
    branch_ids=["10002", "10006"]
)
```

## Configuration

### AndasAPIConfig
```python
@dataclass
class AndasAPIConfig:
    base_url: str      # Base URL for the Andas API
    email: str         # User email for authentication
    password: str      # User password for authentication
    timeout: int = 30  # Request timeout in seconds
```

## Utility Functions

### Create Client
```python
from apipy import create_andas_client

client = create_andas_client(
    base_url="https://api.andas.com",
    email="admin@admin.com",
    password="123456789"
)
```

### Date Formatting
```python
from apipy import format_date_range
from datetime import date

start_date = date(2025, 5, 4)
end_date = date(2025, 5, 10)
from_date_str, to_date_str = format_date_range(start_date, end_date)
# Returns: ("2025-05-04", "2025-05-10")
```

## Error Handling

The client includes comprehensive error handling:

```python
try:
    sales_data = client.get_sales_summary("10002", "2025-05-04", "2025-05-10")
except Exception as e:
    print(f"Error fetching sales data: {e}")
```

## Examples

Run the example file to see all endpoints in action:

```bash
python example_usage.py
```

The example file demonstrates:
- Authentication
- Sales data retrieval
- Stock management
- Consumption and purchases
- User and system data
- Comprehensive reporting
- Branch-specific data
- Utility functions

## API Endpoints Summary

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api-token` | POST | Authentication | email, password |
| `/sales-summary` | GET | Sales summary | branchId, from, to |
| `/sales-transaction` | GET | Sales transactions | branchId, from, to |
| `/stock-adjustment` | GET | Stock adjustments | branchId, from, to |
| `/wastages` | GET | Wastage data | branchId, from, to |
| `/consumption` | GET | Consumption data | branchId, from, to |
| `/purchases` | GET | Purchase data | from, to |
| `/user` | GET | User information | None |
| `/final-production` | GET | Production items | None |
| `/get-outlets` | POST | Outlets/branches | None |

## Data Structure

All API methods return dictionaries containing the response data. The structure depends on the specific endpoint and the data returned by the Andas API.

## Best Practices

1. **Always close the client**: Use `client.close()` when done
2. **Handle authentication**: The client automatically handles token refresh
3. **Use date formatting**: Use the utility functions for consistent date formatting
4. **Error handling**: Wrap API calls in try-catch blocks
5. **Configuration**: Store sensitive data in environment variables

## Environment Variables

For production use, consider using environment variables:

```python
import os

config = AndasAPIConfig(
    base_url=os.getenv("ANDAS_API_BASE_URL"),
    email=os.getenv("ANDAS_API_EMAIL"),
    password=os.getenv("ANDAS_API_PASSWORD")
)
```

## Contributing

1. Follow the existing code style
2. Add proper error handling
3. Include docstrings for all methods
4. Update the README for new features
5. Test with the example file

## License

This project is part of the Andas API integration system. 