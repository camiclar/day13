#!/usr/bin/env python3
"""
Test script for the Simple SQLite MCP Server
This script tests basic functionality of the MCP server without needing a full MCP client.
"""

import json
import subprocess
import sys
import os

def test_python_server():
    """Test the Python MCP server implementation."""
    print("🧪 Testing Python MCP Server...")
    
    # Test if the server can start
    server_path = "/workspace/simple_mcp_server.py"
    db_path = "/workspace/employees.db"
    
    if not os.path.exists(server_path):
        print("❌ Python server file not found")
        return False
    
    if not os.path.exists(db_path):
        print("❌ Database file not found")
        return False
    
    # Test basic functionality
    from simple_mcp_server import SimpleSQLiteMCPServer
    
    try:
        server = SimpleSQLiteMCPServer(db_path)
        
        # Test schema retrieval
        print("  📋 Testing schema retrieval...")
        schema = server.get_schema()
        if "error" in schema:
            print(f"    ❌ Schema error: {schema['error']}")
            return False
        else:
            print(f"    ✅ Found {len(schema)} tables: {list(schema.keys())}")
        
        # Test table listing
        print("  📋 Testing table listing...")
        tables = server.list_tables()
        if "error" in tables:
            print(f"    ❌ Tables error: {tables['error']}")
            return False
        else:
            print(f"    ✅ Tables: {tables['tables']}")
        
        # Test query execution
        print("  📋 Testing query execution...")
        result = server.execute_query("SELECT * FROM employees LIMIT 3")
        if "error" in result:
            print(f"    ❌ Query error: {result['error']}")
            return False
        else:
            print(f"    ✅ Query successful, returned {result['row_count']} rows")
            if result['data']:
                print(f"    📄 Sample data: {result['data'][0]}")
        
        print("✅ Python MCP Server test passed!")
        return True
    
    except Exception as e:
        print(f"❌ Python server test failed: {str(e)}")
        return False

def test_nodejs_server():
    """Test if Node.js MCP server is available."""
    print("🧪 Testing Node.js MCP Server availability...")
    
    try:
        # Check if the Node.js MCP server is available
        result = subprocess.run(
            ["npx", "@modelcontextprotocol/server-sqlite", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ Node.js MCP Server is available")
            return True
        else:
            print("❌ Node.js MCP Server not available")
            print("   Run: npm install -g @modelcontextprotocol/server-sqlite")
            return False
    
    except subprocess.TimeoutExpired:
        print("⏱️ Node.js MCP Server test timed out")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Node.js MCP Server test failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ npx not found. Please install Node.js first.")
        return False

def check_database():
    """Check if the database file exists and has data."""
    print("🗄️ Checking database...")
    
    db_path = "/workspace/employees.db"
    if not os.path.exists(db_path):
        print("❌ Database file not found at /workspace/employees.db")
        return False
    
    try:
        import sqlite3
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM employees")
            count = cursor.fetchone()[0]
            print(f"✅ Database has {count} employees")
            
            cursor.execute("SELECT COUNT(*) FROM departments")
            count = cursor.fetchone()[0]
            print(f"✅ Database has {count} departments")
            
            return True
    except Exception as e:
        print(f"❌ Database check failed: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Simple SQLite MCP Server Setup")
    print("=" * 50)
    
    success = True
    
    # Check database
    success &= check_database()
    print()
    
    # Test Python server
    success &= test_python_server()
    print()
    
    # Test Node.js server availability
    success &= test_nodejs_server()
    print()
    
    if success:
        print("🎉 All tests passed! Your MCP server setup is ready.")
        print()
        print("📋 Quick Start:")
        print("   For Node.js: npx @modelcontextprotocol/server-sqlite /workspace/employees.db")
        print("   For Python:  python3 simple_mcp_server.py /workspace/employees.db")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())