#!/usr/bin/env python3
"""
Simple MCP Server for SQLite Database Interaction
This is a minimal implementation of an MCP server that provides safe read-only access to SQLite databases.
"""

import json
import sqlite3
import sys
import os
from typing import Dict, Any, List

class SimpleSQLiteMCPServer:
    def __init__(self, db_path: str):
        """Initialize the MCP server with a SQLite database path."""
        self.db_path = db_path
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found: {db_path}")
    
    def get_schema(self) -> Dict[str, Any]:
        """Get the database schema information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # Get all tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                schema = {}
                for table in tables:
                    table_name = table['name']
                    if table_name != 'sqlite_sequence':  # Skip system table
                        cursor.execute(f"PRAGMA table_info({table_name})")
                        columns = cursor.fetchall()
                        schema[table_name] = [
                            {
                                'name': col['name'],
                                'type': col['type'],
                                'notnull': bool(col['notnull']),
                                'pk': bool(col['pk'])
                            }
                            for col in columns
                        ]
                
                return schema
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}
    
    def execute_query(self, query: str, limit: int = 100) -> Dict[str, Any]:
        """Execute a read-only SQL query with safety checks."""
        # Simple safety check - only allow SELECT statements
        query_upper = query.strip().upper()
        if not query_upper.startswith('SELECT'):
            return {"error": "Only SELECT queries are allowed"}
        
        # Prevent dangerous operations
        dangerous_keywords = ['DELETE', 'UPDATE', 'INSERT', 'DROP', 'CREATE', 'ALTER']
        if any(keyword in query_upper for keyword in dangerous_keywords):
            return {"error": "Only SELECT queries are allowed"}
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # Add LIMIT if not present and limit is specified
                if 'LIMIT' not in query_upper and limit > 0:
                    query = f"{query.rstrip(';')} LIMIT {limit}"
                
                cursor.execute(query)
                results = cursor.fetchall()
                
                # Convert to list of dictionaries
                data = [dict(row) for row in results]
                
                return {
                    "success": True,
                    "data": data,
                    "row_count": len(data),
                    "query": query
                }
        
        except sqlite3.Error as e:
            return {"error": f"SQL error: {str(e)}"}
    
    def list_tables(self) -> Dict[str, Any]:
        """List all tables in the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
                tables = [row[0] for row in cursor.fetchall()]
                return {"success": True, "tables": tables}
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}

def handle_mcp_request(server: SimpleSQLiteMCPServer, request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle MCP protocol requests."""
    method = request.get('method', '')
    params = request.get('params', {})
    
    if method == 'initialize':
        return {
            "jsonrpc": "2.0",
            "id": request.get('id'),
            "result": {
                "protocolVersion": "0.1.0",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "simple-sqlite-mcp-server",
                    "version": "1.0.0"
                }
            }
        }
    
    elif method == 'tools/list':
        return {
            "jsonrpc": "2.0",
            "id": request.get('id'),
            "result": {
                "tools": [
                    {
                        "name": "query_database",
                        "description": "Execute a SELECT query on the SQLite database",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "SQL SELECT query to execute"},
                                "limit": {"type": "integer", "description": "Maximum number of rows to return", "default": 100}
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "get_schema",
                        "description": "Get the database schema information",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    },
                    {
                        "name": "list_tables",
                        "description": "List all tables in the database",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }
                ]
            }
        }
    
    elif method == 'tools/call':
        tool_name = params.get('name')
        arguments = params.get('arguments', {})
        
        if tool_name == 'query_database':
            query = arguments.get('query', '')
            limit = arguments.get('limit', 100)
            result = server.execute_query(query, limit)
            
            return {
                "jsonrpc": "2.0",
                "id": request.get('id'),
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            }
        
        elif tool_name == 'get_schema':
            result = server.get_schema()
            return {
                "jsonrpc": "2.0",
                "id": request.get('id'),
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            }
        
        elif tool_name == 'list_tables':
            result = server.list_tables()
            return {
                "jsonrpc": "2.0",
                "id": request.get('id'),
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            }
    
    # Default error response
    return {
        "jsonrpc": "2.0",
        "id": request.get('id'),
        "error": {
            "code": -32601,
            "message": f"Method not found: {method}"
        }
    }

def main():
    """Main server loop for MCP communication via stdio."""
    if len(sys.argv) != 2:
        print("Usage: python simple_mcp_server.py <database_path>", file=sys.stderr)
        sys.exit(1)
    
    db_path = sys.argv[1]
    
    try:
        server = SimpleSQLiteMCPServer(db_path)
        
        # MCP communication via stdin/stdout
        for line in sys.stdin:
            try:
                request = json.loads(line.strip())
                response = handle_mcp_request(server, request)
                print(json.dumps(response))
                sys.stdout.flush()
            except json.JSONDecodeError:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    }
                }
                print(json.dumps(error_response))
                sys.stdout.flush()
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": request.get('id') if 'request' in locals() else None,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                print(json.dumps(error_response))
                sys.stdout.flush()
    
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()