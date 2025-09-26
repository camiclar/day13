# Simple SQLite MCP Server

A very simple Model Context Protocol (MCP) server for interacting with SQLite databases. This allows Cursor AI to interact with your `employees.db` database safely through an MCP server instead of direct database access.

## 🚀 Quick Start

1. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Test the setup:**
   ```bash
   python3 test_mcp_server.py
   ```

3. **Start your preferred MCP server:**
   
   **Option 1 (Recommended): Node.js MCP Server**
   ```bash
   npx @modelcontextprotocol/server-sqlite /workspace/employees.db
   ```
   
   **Option 2: Python MCP Server**
   ```bash
   python3 simple_mcp_server.py /workspace/employees.db
   ```

## 📋 Files Overview

- `employees.db` - Your SQLite database with employee and department data
- `simple_mcp_server.py` - Custom Python MCP server implementation
- `mcp-config.json` - Configuration file for Cursor AI
- `setup.sh` - Automated setup script
- `test_mcp_server.py` - Test script to verify functionality
- `package.json` - Node.js dependencies

## 🛠️ Configuration

### For Cursor AI Integration

Copy the `mcp-config.json` to your Cursor settings directory or configure Cursor to use the MCP server with these settings:

```json
{
  "mcpServers": {
    "sqlite-server": {
      "command": "npx",
      "args": [
        "-y", 
        "@modelcontextprotocol/server-sqlite", 
        "/workspace/employees.db"
      ]
    }
  }
}
```

## 🔧 Available Operations

The MCP server provides these safe, read-only operations:

1. **List Tables** - Get all table names in the database
2. **Get Schema** - View the structure of all tables
3. **Execute Queries** - Run SELECT queries (read-only)

### Sample Queries You Can Run

```sql
-- List all employees
SELECT * FROM employees;

-- Get employees by department
SELECT e.name, d.name as department, e.salary 
FROM employees e 
JOIN departments d ON e.department_id = d.id;

-- Count employees per department
SELECT d.name, COUNT(*) as employee_count 
FROM departments d 
LEFT JOIN employees e ON d.id = e.department_id 
GROUP BY d.name;
```

## 🔒 Security Features

- **Read-only access** - Only SELECT queries are allowed
- **Query validation** - Prevents dangerous SQL operations
- **Row limits** - Prevents excessive data retrieval
- **Safe parameter binding** - Protection against SQL injection

## 🐛 Troubleshooting

### Common Issues

1. **"Database file not found"**
   - Ensure `/workspace/employees.db` exists
   - Check file permissions

2. **"Node.js not found"**
   - Install Node.js from https://nodejs.org/
   - Restart your terminal

3. **"MCP server not responding"**
   - Check if the server process is running
   - Verify the configuration file path
   - Review server logs for errors

### Testing Your Setup

Run the test script to verify everything is working:
```bash
python3 test_mcp_server.py
```

This will check:
- Database accessibility
- Python MCP server functionality  
- Node.js MCP server availability

## 📊 Database Schema

Your `employees.db` contains:

**employees table:**
- id (PRIMARY KEY)
- name (TEXT)
- department_id (INTEGER, FOREIGN KEY)
- salary (REAL)
- hire_date (TEXT)

**departments table:**
- id (PRIMARY KEY) 
- name (TEXT)

## 🆘 Support

If you encounter issues:

1. Run the test script: `python3 test_mcp_server.py`
2. Check that Node.js and Python are properly installed
3. Verify the database file exists and is readable
4. Ensure MCP server configuration matches your setup

## 📝 License

MIT License - feel free to modify and use as needed.