# Employee Management Rest API

This project is a simple CRUD-based Employee Management REST API built using Python and Flask.

# Featuers

1. Create Employee
2. Read All Employee
3. Update Employee
4. Delete Employee

# Technologies used

1. Python
2. Flask
3. Flask-SQLALCHEMY
4. SQLite Database

# API Endpoints

Method | Endpoint        | Description       |

POST   | /employees      | Add new employees |
GET    | /employees      | Get all employees |
PUT    | /employees/<id> | Update employee   |
Delete | /employees/<id> | Delete employee   |

# Sample Request (POST)
```json
{
    "name": "Diva",
    "email": "divakar@gmail.com",
    "phone": "9940025087",
    "designation": "Software Developer Trainee",
    "salary":15000
}
```
# Run the project
```

pip install-r requirements.txt
python app.py

```
