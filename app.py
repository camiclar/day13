#!/usr/bin/env python3
"""
Employee Management System - Web Interface
A Flask web application with Bootstrap for managing employee records.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

class EmployeeManager:
    def __init__(self, db_path: str = "employees.db"):
        """Initialize the Employee Manager with database path."""
        self.db_path = db_path
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found: {db_path}")
    
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
    
    def get_employees(self) -> List[Dict[str, Any]]:
        """Get all employees with department information."""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.id, e.name, d.name as department, e.salary, e.hire_date, e.department_id
                FROM employees e
                LEFT JOIN departments d ON e.department_id = d.id
                ORDER BY e.id
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_employee(self, employee_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific employee by ID."""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.id, e.name, d.name as department, e.salary, e.hire_date, e.department_id
                FROM employees e
                LEFT JOIN departments d ON e.department_id = d.id
                WHERE e.id = ?
            """, (employee_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
    
    def create_employee(self, name: str, department_id: int, salary: float, hire_date: str) -> bool:
        """Create a new employee record."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO employees (name, department_id, salary, hire_date) 
                    VALUES (?, ?, ?, ?)
                """, (name, department_id, salary, hire_date))
                conn.commit()
                return True
        except sqlite3.Error:
            return False
    
    def update_employee(self, employee_id: int, name: str, department_id: int, salary: float, hire_date: str) -> bool:
        """Update an existing employee record."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE employees 
                    SET name = ?, department_id = ?, salary = ?, hire_date = ?
                    WHERE id = ?
                """, (name, department_id, salary, hire_date, employee_id))
                conn.commit()
                return True
        except sqlite3.Error:
            return False
    
    def delete_employee(self, employee_id: int) -> bool:
        """Delete an employee record."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
                conn.commit()
                return True
        except sqlite3.Error:
            return False

# Initialize the employee manager
try:
    employee_manager = EmployeeManager()
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit(1)

@app.route('/')
def index():
    """Home page - display all employees."""
    employees = employee_manager.get_employees()
    departments = employee_manager.get_departments()
    
    # Calculate statistics
    avg_salary = 0
    new_this_year = 0
    department_counts = {}
    
    if employees:
        # Calculate average salary
        total_salary = sum(emp['salary'] for emp in employees)
        avg_salary = total_salary / len(employees)
        
        # Count employees hired this year
        current_year = datetime.now().year
        new_this_year = sum(1 for emp in employees if emp['hire_date'].startswith(str(current_year)))
        
        # Count employees per department
        for emp in employees:
            dept_id = emp['department_id']
            department_counts[dept_id] = department_counts.get(dept_id, 0) + 1
    
    return render_template('index.html', 
                         employees=employees, 
                         departments=departments,
                         avg_salary=avg_salary,
                         new_this_year=new_this_year,
                         department_counts=department_counts)

@app.route('/create', methods=['GET', 'POST'])
def create_employee():
    """Create a new employee."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        department_id = request.form.get('department_id')
        salary = request.form.get('salary')
        hire_date = request.form.get('hire_date', '').strip()
        
        # Validation
        if not name or not department_id or not salary or not hire_date:
            flash('All fields are required!', 'error')
            return redirect(url_for('create_employee'))
        
        try:
            department_id = int(department_id)
            salary = float(salary)
        except ValueError:
            flash('Invalid department ID or salary!', 'error')
            return redirect(url_for('create_employee'))
        
        if employee_manager.create_employee(name, department_id, salary, hire_date):
            flash(f'Employee "{name}" created successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Error creating employee. Please try again.', 'error')
    
    departments = employee_manager.get_departments()
    return render_template('create.html', departments=departments)

@app.route('/edit/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    """Edit an existing employee."""
    employee = employee_manager.get_employee(employee_id)
    if not employee:
        flash('Employee not found!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        department_id = request.form.get('department_id')
        salary = request.form.get('salary')
        hire_date = request.form.get('hire_date', '').strip()
        
        # Validation
        if not name or not department_id or not salary or not hire_date:
            flash('All fields are required!', 'error')
            return redirect(url_for('edit_employee', employee_id=employee_id))
        
        try:
            department_id = int(department_id)
            salary = float(salary)
        except ValueError:
            flash('Invalid department ID or salary!', 'error')
            return redirect(url_for('edit_employee', employee_id=employee_id))
        
        if employee_manager.update_employee(employee_id, name, department_id, salary, hire_date):
            flash(f'Employee "{name}" updated successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Error updating employee. Please try again.', 'error')
    
    departments = employee_manager.get_departments()
    return render_template('edit.html', employee=employee, departments=departments)

@app.route('/delete/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    """Delete an employee."""
    employee = employee_manager.get_employee(employee_id)
    if not employee:
        flash('Employee not found!', 'error')
        return redirect(url_for('index'))
    
    if employee_manager.delete_employee(employee_id):
        flash(f'Employee "{employee["name"]}" deleted successfully!', 'success')
    else:
        flash('Error deleting employee. Please try again.', 'error')
    
    return redirect(url_for('index'))

@app.route('/racing')
def racing_game():
    """Racing game page."""
    employees = employee_manager.get_employees()
    departments = employee_manager.get_departments()
    return render_template('racing.html', employees=employees, departments=departments)

@app.route('/api/employees')
def api_employees():
    """API endpoint to get all employees as JSON."""
    employees = employee_manager.get_employees()
    return jsonify(employees)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
