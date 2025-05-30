import os
import oracledb
from flask import Flask, jsonify, request


app = Flask(__name__)

dsn = os.getenv('DB_DSN', oracledb.makedsn("localhost", 1521, service_name="XE"))
db_user = os.getenv('DB_USER', 'system')
db_password = os.getenv('DB_PASSWORD', 'dazai')

def create_connection():
    try:
        connection = oracledb.connect(user=db_user, password=db_password, dsn=dsn)
        return connection
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        print(f"Error connecting to Oracle DB: {error_obj.message}")
        return None

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, username, email, status FROM users")
        
        users = [{'user_id': row[0], 'username': row[1], 'email': row[2], 'status': row[3]} for row in cursor.fetchall()]
        cursor.close()
        connection.close()

        return jsonify({"users": users})
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500

@app.route('/api/users', methods=['POST'])
def insert_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role_name = data.get('role_name')

    if not username or not password or not email or not role_name:
        return jsonify({"error": "All fields are required"}), 400

    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor()
        cursor.callproc("insert_user", [username, password, email, role_name])
        connection.commit()

        return jsonify({"message": f"User {username} inserted successfully"}), 201
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/api/employees', methods=['GET'])
def get_employees():
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = connection.cursor()
        cursor.execute("SELECT employee_id, employee_name, department FROM employees")

        employees = [{'employee_id': row[0], 'employee_name': row[1], 'department': row[2]} for row in cursor.fetchall()]
        cursor.close()
        connection.close()

        return jsonify({"employees": employees})
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500

@app.route('/api/employees', methods=['POST'])
def insert_employee():
    data = request.get_json()
    employee_name = data.get('employee_name')
    department = data.get('department')
    username = data.get('username')  # User performing the action

    if not employee_name or not department or not username:
        return jsonify({"error": "All fields are required"}), 400

    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = connection.cursor()

        cursor.execute("SELECT check_permission(:username, 'INSERT') FROM dual", [username])
        permission = cursor.fetchone()[0]

        if permission != 'Permission Granted':
            return jsonify({"error": "Permission Denied"}), 403

        cursor.execute("""
            INSERT INTO employees (employee_id, employee_name, department) 
            VALUES (employee_id_seq.NEXTVAL, :employee_name, :department)
        """, [employee_name, department])
        connection.commit()

        return jsonify({"message": f"Employee {employee_name} inserted successfully"}), 201
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/api/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.get_json()
    department = data.get('department')
    username = data.get('username')

    if not department or not username:
        return jsonify({"error": "All fields are required"}), 400

    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = connection.cursor()

        cursor.execute("SELECT check_permission(:username, 'UPDATE') FROM dual", [username])
        permission = cursor.fetchone()[0]

        if permission != 'Permission Granted':
            return jsonify({"error": "Permission Denied"}), 403

        cursor.execute("""
            UPDATE employees 
            SET department = :department
            WHERE employee_id = :employee_id
        """, [department, employee_id])
        connection.commit()

        return jsonify({"message": f"Employee {employee_id} updated successfully"}), 200
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    username = request.args.get('username')

    if not username:
        return jsonify({"error": "Username is required"}), 400

    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = connection.cursor()

        cursor.execute("SELECT check_permission(:username, 'DELETE') FROM dual", [username])
        permission = cursor.fetchone()[0]

        if permission != 'Permission Granted':
            return jsonify({"error": "Permission Denied"}), 403

        cursor.execute("DELETE FROM employees WHERE employee_id = :employee_id", [employee_id])
        connection.commit()

        return jsonify({"message": f"Employee {employee_id} deleted successfully"}), 200
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
