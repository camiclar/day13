#!/bin/bash

echo "🚀 Setting up Simple SQLite MCP Server..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

echo "✅ Node.js version: $(node --version)"
echo "✅ Python3 version: $(python3 --version)"

# Check Python dependencies
echo "📦 Checking Python dependencies..."
python3 -c "import sqlite3, json, sys" && echo "✅ Python dependencies are available"

# Make Python server executable
chmod +x simple_mcp_server.py

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Test your setup:"
echo "   python3 test_mcp_server.py"
echo ""
echo "2. Start the MCP Server:"
echo "   🟢 RECOMMENDED: Use the Python MCP Server"
echo "   Run: python3 simple_mcp_server.py /workspace/employees.db"
echo ""
echo "2. Configure Cursor AI to use the MCP server by adding mcp-config.json"
echo "   to your Cursor settings directory."
echo ""
echo "📁 Database file: /workspace/employees.db"
echo "📄 Config file: /workspace/mcp-config.json"
echo ""
