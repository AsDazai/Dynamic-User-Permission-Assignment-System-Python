#  Title:
Dynamic User Permission Management System

##  Description:
The Dynamic User Permission Management System is a robust solution designed to efficiently manage user roles and permissions in an organization. It provides administrators with the ability to create and manage users, assign them specific roles, and dynamically configure permissions based on roles. The system integrates with Oracle SQL Developer XE to handle the backend database operations and leverages Python for backend processing. The system allows administrators to manage user data, control access, and track permissions via role-based access control. Through API endpoints built using Flask and tested via Postman, the system supports operations like user creation, role assignment, permission checking, and more, ensuring secure and efficient access management.

##  Key Features:
1.User Management: Allows for the creation, updating, and deletion of users, ensuring flexibility and control.
2.Role Assignment: Admin users can assign roles (such as Admin, User, Employee) to users, each with distinct permissions.
3.Permission Control: Defines and assigns permissions such as SELECT, INSERT, UPDATE, DELETE based on user roles, offering fine-grained control over access rights.
4.API-based Interaction: Utilizes APIs for communication with the backend and Postman for API testing and validation.
5.Database Integration: Uses Oracle SQL Developer XE to store and manage user, role, and permission data in relational tables.
6.Role-Based Access Control: Ensures that users can only perform actions allowed by their assigned roles and permissions, providing a secure and efficient access management system.

##  Tech Used:
1.Backend Development: Python
2.Database Management: Oracle SQL Developer XE
3.API Testing: Postman
4.Web Framework: Flask (used for building and managing APIs)
5.Database Connectivity: oracledb (Python library for connecting and interacting with Oracle databases)
6.Response Formatting: jsonify (for returning JSON responses from Flask APIs)

## Tools and Libraries Needed:
1.Tools:
Oracle SQL Developer XE: Used for database management and executing SQL queries for operations such as creating tables, managing roles and users, and running stored procedures.
Postman: A powerful tool for testing RESTful APIs and simulating HTTP requests (e.g., GET, POST) to ensure proper functionality of the backend system.
2.Libraries:
oracledb: Python library for connecting to Oracle databases, facilitating operations like data retrieval, insertion, and calling stored procedures.
Flask: A Python-based micro-framework used to create web APIs, which allow communication with the frontend or Postman.
jsonify: Flask utility for formatting the responses in JSON, making it easy to communicate with frontend applications or API clients like Postman.
