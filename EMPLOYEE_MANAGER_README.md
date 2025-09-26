# Employee Management System

A simple terminal-based CRUD application for managing employee records in a SQLite database.

## 🚀 Features

- **Create Employee** - Add new employee records
- **View Employees** - Display all employees with department information
- **Update Employee** - Modify existing employee records
- **Delete Employee** - Remove employee records with confirmation
- **Department Integration** - Shows available departments for selection

## 📋 Requirements

- Python 3.6+
- SQLite database (`employees.db`)
- Required tables: `employees` and `departments`

## 🛠️ Usage

### Basic Usage
```bash
python employee_manager.py
```

### With Custom Database
```bash
python employee_manager.py your_database.db
```

## 📊 Database Schema

### employees table
- `id` (INTEGER PRIMARY KEY)
- `name` (TEXT)
- `department_id` (INTEGER, FOREIGN KEY)
- `salary` (REAL)
- `hire_date` (TEXT)

### departments table
- `id` (INTEGER PRIMARY KEY)
- `name` (TEXT)

## 🎯 Menu Options

1. **Create Employee** - Add a new employee with name, department, salary, and hire date
2. **View Employees** - Display all employees in a formatted table
3. **Update Employee** - Modify existing employee information
4. **Delete Employee** - Remove an employee with confirmation prompt
5. **Exit** - Close the application

## 🔧 Features

- **Input Validation** - Validates all user inputs
- **Error Handling** - Graceful error handling with user-friendly messages
- **Confirmation Prompts** - Safety confirmations for destructive operations
- **Formatted Output** - Clean, readable table formatting
- **Department Integration** - Shows available departments when creating/updating

## 📝 Example Usage

```
🏢 EMPLOYEE MANAGEMENT SYSTEM
==================================================
1. Create Employee
2. View Employees
3. Update Employee
4. Delete Employee
5. Exit
==================================================
Enter your choice (1-5): 1

➕ CREATE NEW EMPLOYEE
==============================
Enter employee name: John Smith
📋 Available Departments:
------------------------------
  1. HR
  2. Engineering
  3. Sales

Enter department ID: 2
Enter salary: $75000
Enter hire date (YYYY-MM-DD): 2024-01-15
✅ Employee 'John Smith' created successfully!
   💰 Salary: $75,000.00
   📅 Hire Date: 2024-01-15
   🏢 Department ID: 2
```

## 🛡️ Safety Features

- **Confirmation for Deletion** - Prevents accidental data loss
- **Input Validation** - Ensures data integrity
- **Error Handling** - Graceful handling of database errors
- **Transaction Safety** - Uses proper database transactions

## 📁 Files

- `employee_manager.py` - Main application file
- `test_employee_manager.py` - Test script
- `employees.db` - SQLite database file
- `EMPLOYEE_MANAGER_README.md` - This documentation

## 🚀 Quick Start

1. Ensure you have Python 3.6+ installed
2. Make sure `employees.db` exists with proper schema
3. Run: `python employee_manager.py`
4. Follow the menu prompts to manage employees

## 🔧 Troubleshooting

- **Database not found**: Ensure `employees.db` exists in the current directory
- **Permission errors**: Check file permissions for the database
- **Invalid input**: Follow the prompts carefully and use proper formats
- **Department ID errors**: Use valid department IDs (1, 2, 3, etc.)
