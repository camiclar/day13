#!/usr/bin/env python3
"""
Employee Management System
A simple terminal-based CRUD application for managing employee records.
"""

import sqlite3
import sys
import os
from typing import Dict, Any, List, Optional

class EmployeeManager:
    def __init__(self, db_path: str = "employees.db"):
        """Initialize the Employee Manager with database path."""
        self.db_path = db_path
        if not os.path.exists(db_path):
            print(f"❌ Database file not found: {db_path}")
            sys.exit(1)
    
    def get_connection(self):
        """Get a database connection."""
        return sqlite3.connect(self.db_path)
    
    def get_departments(self) -> List[Dict[str, Any]]:
        """Get all departments for display."""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM departments ORDER BY id")
            return [dict(row) for row in cursor.fetchall()]
    
    def display_departments(self):
        """Display available departments."""
        departments = self.get_departments()
        print("\n📋 Available Departments:")
        print("-" * 30)
        for dept in departments:
            print(f"  {dept['id']}. {dept['name']}")
        print()
    
    def create_employee(self):
        """Create a new employee record."""
        print("\n➕ CREATE NEW EMPLOYEE")
        print("=" * 30)
        
        # Get employee details
        name = input("Enter employee name: ").strip()
        if not name:
            print("❌ Name cannot be empty!")
            return
        
        self.display_departments()
        try:
            department_id = int(input("Enter department ID: "))
        except ValueError:
            print("❌ Invalid department ID!")
            return
        
        try:
            salary = float(input("Enter salary: $"))
        except ValueError:
            print("❌ Invalid salary amount!")
            return
        
        hire_date = input("Enter hire date (YYYY-MM-DD): ").strip()
        if not hire_date:
            print("❌ Hire date cannot be empty!")
            return
        
        # Insert the employee
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO employees (name, department_id, salary, hire_date) 
                    VALUES (?, ?, ?, ?)
                """, (name, department_id, salary, hire_date))
                conn.commit()
                
                print(f"✅ Employee '{name}' created successfully!")
                print(f"   💰 Salary: ${salary:,.2f}")
                print(f"   📅 Hire Date: {hire_date}")
                print(f"   🏢 Department ID: {department_id}")
                
        except sqlite3.Error as e:
            print(f"❌ Error creating employee: {e}")
    
    def view_employees(self):
        """View all employee records."""
        print("\n👥 EMPLOYEE RECORDS")
        print("=" * 50)
        
        try:
            with self.get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT e.id, e.name, d.name as department, e.salary, e.hire_date
                    FROM employees e
                    LEFT JOIN departments d ON e.department_id = d.id
                    ORDER BY e.id
                """)
                employees = cursor.fetchall()
                
                if not employees:
                    print("📭 No employees found in the database.")
                    return
                
                print(f"{'ID':<3} {'Name':<20} {'Department':<15} {'Salary':<12} {'Hire Date':<12}")
                print("-" * 70)
                
                for emp in employees:
                    print(f"{emp['id']:<3} {emp['name']:<20} {emp['department']:<15} ${emp['salary']:<11,.2f} {emp['hire_date']:<12}")
                
                print(f"\n📊 Total employees: {len(employees)}")
                
        except sqlite3.Error as e:
            print(f"❌ Error viewing employees: {e}")
    
    def update_employee(self):
        """Update an existing employee record."""
        print("\n✏️  UPDATE EMPLOYEE")
        print("=" * 30)
        
        # First, show current employees
        self.view_employees()
        
        try:
            employee_id = int(input("\nEnter employee ID to update: "))
        except ValueError:
            print("❌ Invalid employee ID!")
            return
        
        # Check if employee exists
        try:
            with self.get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
                employee = cursor.fetchone()
                
                if not employee:
                    print(f"❌ Employee with ID {employee_id} not found!")
                    return
                
                print(f"\n📋 Current details for {employee['name']}:")
                print(f"   Name: {employee['name']}")
                print(f"   Department ID: {employee['department_id']}")
                print(f"   Salary: ${employee['salary']:,.2f}")
                print(f"   Hire Date: {employee['hire_date']}")
                
                # Get updated information
                print("\nEnter new details (press Enter to keep current value):")
                
                new_name = input(f"Name [{employee['name']}]: ").strip()
                if not new_name:
                    new_name = employee['name']
                
                dept_input = input(f"Department ID [{employee['department_id']}]: ").strip()
                if not dept_input:
                    new_department_id = employee['department_id']
                else:
                    try:
                        new_department_id = int(dept_input)
                    except ValueError:
                        print("❌ Invalid department ID!")
                        return
                
                salary_input = input(f"Salary [${employee['salary']:,.2f}]: ").strip()
                if not salary_input:
                    new_salary = employee['salary']
                else:
                    try:
                        new_salary = float(salary_input)
                    except ValueError:
                        print("❌ Invalid salary amount!")
                        return
                
                hire_input = input(f"Hire Date [{employee['hire_date']}]: ").strip()
                if not hire_input:
                    new_hire_date = employee['hire_date']
                else:
                    new_hire_date = hire_input
                
                # Update the employee
                cursor.execute("""
                    UPDATE employees 
                    SET name = ?, department_id = ?, salary = ?, hire_date = ?
                    WHERE id = ?
                """, (new_name, new_department_id, new_salary, new_hire_date, employee_id))
                conn.commit()
                
                print(f"✅ Employee updated successfully!")
                print(f"   👤 Name: {new_name}")
                print(f"   💰 Salary: ${new_salary:,.2f}")
                print(f"   📅 Hire Date: {new_hire_date}")
                print(f"   🏢 Department ID: {new_department_id}")
                
        except sqlite3.Error as e:
            print(f"❌ Error updating employee: {e}")
    
    def delete_employee(self):
        """Delete an employee record."""
        print("\n🗑️  DELETE EMPLOYEE")
        print("=" * 30)
        
        # First, show current employees
        self.view_employees()
        
        try:
            employee_id = int(input("\nEnter employee ID to delete: "))
        except ValueError:
            print("❌ Invalid employee ID!")
            return
        
        # Check if employee exists
        try:
            with self.get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
                employee = cursor.fetchone()
                
                if not employee:
                    print(f"❌ Employee with ID {employee_id} not found!")
                    return
                
                print(f"\n⚠️  WARNING: You are about to delete:")
                print(f"   👤 Name: {employee['name']}")
                print(f"   💰 Salary: ${employee['salary']:,.2f}")
                print(f"   📅 Hire Date: {employee['hire_date']}")
                print(f"   🏢 Department ID: {employee['department_id']}")
                
                confirm = input("\nAre you sure you want to delete this employee? (yes/no): ").strip().lower()
                
                if confirm in ['yes', 'y']:
                    cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
                    conn.commit()
                    print(f"✅ Employee '{employee['name']}' deleted successfully!")
                else:
                    print("❌ Deletion cancelled.")
                
        except sqlite3.Error as e:
            print(f"❌ Error deleting employee: {e}")
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*50)
        print("🏢 EMPLOYEE MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Create Employee")
        print("2. View Employees")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Exit")
        print("="*50)
    
    def run(self):
        """Run the main application loop."""
        print("🚀 Welcome to the Employee Management System!")
        
        while True:
            self.display_menu()
            
            try:
                choice = input("Enter your choice (1-5): ").strip()
                
                if choice == '1':
                    self.create_employee()
                elif choice == '2':
                    self.view_employees()
                elif choice == '3':
                    self.update_employee()
                elif choice == '4':
                    self.delete_employee()
                elif choice == '5':
                    print("\n👋 Thank you for using the Employee Management System!")
                    break
                else:
                    print("❌ Invalid choice! Please enter 1-5.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                input("Press Enter to continue...")

def main():
    """Main function to start the application."""
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        db_path = "employees.db"
    
    app = EmployeeManager(db_path)
    app.run()

if __name__ == "__main__":
    main()
