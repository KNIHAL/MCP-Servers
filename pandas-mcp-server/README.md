# Pandas MCP Server

A powerful Model Context Protocol (MCP) server for data analysis and manipulation using pandas. This server provides tools for reading, processing, and visualizing data from various sources including CSV, Excel, JSON, and SQL databases.

## Features

- 📊 **Data Reading & Metadata Analysis**: Read and analyze CSV, Excel, JSON files with detailed metadata
- 🔧 **Pandas Code Execution**: Execute pandas code with security checks and smart suggestions
- 📈 **Data Visualization**: Generate interactive Chart.js visualizations
- 💾 **JSON Support**: Read from and write to JSON files with multiple orient options
- 🗄️ **SQL Integration**: Query SQL databases and save DataFrames to database tables
- 🔒 **Security**: Built-in security checks to prevent dangerous operations

### Setup

1. Clone the repository:
```bash
git clone https://github.com/KNIHAL/MCP-Servers.git
cd MCP-Servers/pandas-mcp-server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python server.py
```

## Tools

### 1. `read_metadata_tool`

Read and analyze metadata from Excel or CSV files.

**Parameters:**
- `file_path` (str): Absolute path to the data file

**Returns:**
- File information (type, sheet names for Excel, encoding for CSV)
- Data structure (rows, columns)
- Column details (name, type, examples, statistics)
- Warnings and suggested operations

**Example:**
```python
{
    "file_path": "/path/to/data.csv"
}
```

### 2. `run_pandas_code_tool`

Execute pandas code with security checks and automatic result handling.

**Parameters:**
- `code` (str): Python code string containing pandas operations

**Security:** Blocks dangerous operations like `os.`, `sys.`, `exec()`, `eval()`, file operations, and subprocess calls.

**Requirements:**
- Code must assign the final result to a `result` variable
- Pandas is available as `pd`

**Example:**
```python
{
    "code": "import pandas as pd\ndf = pd.read_csv('data.csv')\nresult = df.head()"
}
```

### 3. `generate_chartjs_tool`

Generate interactive Chart.js visualizations from structured data.

**Parameters:**
- `data` (dict): Structured data with columns array
- `chart_types` (list, optional): Chart types to generate
- `title` (str, optional): Chart title (default: "Data Visualization")
- `request_params` (dict, optional): Additional visualization parameters

**Example:**
```python
{
    "data": {
        "columns": [
            {"name": "Category", "type": "string", "examples": ["A", "B", "C"]},
            {"name": "Value", "type": "number", "examples": [10, 20, 30]}
        ]
    },
    "title": "Sales by Category"
}
```

### 4. `read_json_tool`

Read JSON file and convert to pandas DataFrame.

**Parameters:**
- `file_path` (str): Path to JSON file
- `orient` (str, optional): JSON structure - 'records', 'columns', 'index', 'values' (default: 'records')

**Returns:**
- Status, data (as records), shape, and column names

**Example:**
```python
{
    "file_path": "/path/to/data.json",
    "orient": "records"
}
```

### 5. `dataframe_to_json_tool`

Convert DataFrame to JSON file with proper serialization.

**Parameters:**
- `code` (str): Pandas code that creates a 'result' DataFrame
- `output_path` (str): Where to save the JSON file
- `orient` (str, optional): Output format (default: 'records')

**Features:**
- Handles numpy types, datetime objects, Decimal, pandas NaT/NA
- Pretty-printed JSON output with 2-space indentation
- UTF-8 encoding support

**Example:**
```python
{
    "code": "import pandas as pd\nresult = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})",
    "output_path": "/path/to/output.json",
    "orient": "records"
}
```

### 6. `read_sql_tool`

Read data from SQL database using a query.

**Parameters:**
- `query` (str): SQL query to execute
- `connection_string` (str): Database connection URL

**Connection String Examples:**
- SQLite: `sqlite:///database.db`
- PostgreSQL: `postgresql://user:password@localhost/dbname`
- MySQL: `mysql+pymysql://user:password@localhost/dbname`

**Example:**
```python
{
    "query": "SELECT * FROM users WHERE age > 25",
    "connection_string": "sqlite:///mydata.db"
}
```

### 7. `dataframe_to_sql_tool`

Save DataFrame to SQL database table.

**Parameters:**
- `code` (str): Pandas code creating a 'result' DataFrame
- `table_name` (str): Name of the SQL table
- `connection_string` (str): Database connection URL
- `if_exists` (str, optional): Action if table exists - 'replace', 'append', 'fail' (default: 'replace')

**Example:**
```python
{
    "code": "import pandas as pd\nresult = pd.DataFrame({'name': ['John', 'Jane'], 'age': [30, 25]})",
    "table_name": "users",
    "connection_string": "sqlite:///mydata.db",
    "if_exists": "append"
}
```

## Security Features

The server includes built-in security checks to prevent dangerous operations:

### Blocked Operations
- System access: `os.`, `sys.`, `subprocess.`
- Code execution: `exec()`, `eval()`, `open()`
- Dangerous imports: `import os`, `import sys`
- Browser/DOM access: `document.`, `window.`, `XMLHttpRequest`
- Remote operations: `fetch()`, `Function()`
- Script injection: `<script>`, `javascript:`

## Data Type Support

The server intelligently detects and handles various data types:

- **Numbers**: int, float, numpy numeric types
- **Strings**: text, categorical data
- **Dates**: datetime, timestamps, pandas Timestamp
- **Booleans**: True/False values
- **Mixed types**: Automatically detected and categorized
- **Special values**: NaN, NaT, None properly handled

## Error Handling

All tools return structured error responses:

```json
{
    "status": "ERROR",
    "message": "Error description",
    "traceback": "Detailed traceback (when available)"
}
```

## Examples

### Complete Workflow Example

```python
# 1. Read metadata from CSV
metadata = read_metadata_tool("/data/sales.csv")

# 2. Process data with pandas
result = run_pandas_code_tool("""
import pandas as pd
df = pd.read_csv('/data/sales.csv')
df['total'] = df['quantity'] * df['price']
result = df.groupby('category')['total'].sum()
""")

# 3. Save to JSON
json_result = dataframe_to_json_tool(
    code="result = df",
    output_path="/output/processed.json",
    orient="records"
)

# 4. Save to SQL database
sql_result = dataframe_to_sql_tool(
    code="result = df",
    table_name="sales_summary",
    connection_string="sqlite:///analytics.db",
    if_exists="replace"
)

# 5. Visualize results
chart = generate_chartjs_tool(
    data=metadata['data'],
    title="Sales Analysis",
    chart_types=["bar"]
)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

License
MIT License - see LICENSE file for details

## Author

Original repo: [marlonluo2018/pandas-mcp-server](https://github.com/marlonluo2018/pandas-mcp-server)

## Changelog

### Latest Updates
- ✅ Added JSON read/write tools with advanced serialization
- ✅ Added SQL database integration (read/write)
- ✅ Improved error handling and traceback reporting
- ✅ Enhanced data type conversion for JSON export
- ✅ Removed logging complexity for cleaner codebase

## Support

For issues and questions, please open an issue on GitHub.

