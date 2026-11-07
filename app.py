
"""Simple Employee Management System (Python + Flask + SQLite).

Features: add an employee, list employees, delete an employee.
Run:  python app.py   then open  http://SERVER-IP:5000
"""
import os
import sqlite3

from flask import Flask, jsonify, redirect, render_template_string, request

app = Flask(__name__)
DB_FILE = os.environ.get("DB_FILE", "employees.db")

PAGE = """
<!doctype html>
<title>Employee Management System</title>
<body style="font-family:Arial;margin:30px">
  <h1>Employee Management System</h1>

  <h3>Add new employee</h3>
  <form method="post" action="/add">
    <input name="emp_id" placeholder="Employee ID" required>
    <input name="name" placeholder="Name" required>
    <input name="role" placeholder="Role" required>
    <button type="submit">Add</button>
  </form>

  <h3>All employees</h3>
  <table border="1" cellpadding="8" cellspacing="0">
    <tr><th>ID</th><th>Name</th><th>Role</th><th>Action</th></tr>
    {% for e in employees %}
    <tr>
      <td>{{ e["emp_id"] }}</td><td>{{ e["name"] }}</td><td>{{ e["role"] }}</td>
      <td><form method="post" action="/delete/{{ e['emp_id'] }}">
            <button type="submit">Delete</button></form></td>
    </tr>
    {% else %}
    <tr><td colspan="4">No employees yet</td></tr>
    {% endfor %}
  </table>
</body>
"""


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS employees ("
            "emp_id TEXT PRIMARY KEY, name TEXT NOT NULL, role TEXT NOT NULL)"
        )


@app.route("/")
def home():
    with get_db() as conn:
        employees = conn.execute("SELECT * FROM employees ORDER BY emp_id").fetchall()
    return render_template_string(PAGE, employees=employees)


@app.route("/add", methods=["POST"])
def add():
    emp_id = request.form["emp_id"].strip()
    name = request.form["name"].strip()
    role = request.form["role"].strip()
    with get_db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO employees (emp_id, name, role) VALUES (?, ?, ?)",
            (emp_id, name, role),
        )
    return redirect("/")


@app.route("/delete/<emp_id>", methods=["POST"])
def delete(emp_id):
    with get_db() as conn:
        conn.execute("DELETE FROM employees WHERE emp_id = ?", (emp_id,))
    return redirect("/")


@app.route("/api/employees")
def api_employees():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM employees ORDER BY emp_id").fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/health")
def health():
    return "OK"


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

