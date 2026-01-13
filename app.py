from flask import Flask,request,jsonify
from models import db,Employee
import re

app = Flask(__name__)

# ================================================== Database Config ==================================================

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///employees.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ================================================== Error Handling Function ==================================================

def bad_request(message):
    return jsonify({"error":message}),400

def not_found(message):
    return jsonify({"error":message}),404

def server_error(message='Internal Server Error'):
    return jsonify({"error":message}),500

# ================================================== Validation Function ==================================================

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def is_valid_phone(phone):
    return phone.isdigit() and 10 <= len(phone) <= 15

# ================================================== Routes ==================================================

# Add Employee

@app.route('/employees',methods=['POST'])
def add_employee():
    try:
        data = request.json
        if not data:
            return bad_request("JSON data is required")
        required_fields = ['name','email','phone','designation','salary']
        for field in required_fields:
            if field not in data:
                return bad_request(f"{field} is required")
        if not is_valid_email(data['email']):
            return bad_request("Invalid email format")   # mail validate

        existing = Employee.query.filter_by(email=data["email"]).first()
        if existing:
            return bad_request("Email already exists") # unique mail validate
        
        if not is_valid_phone(data['phone']):
            return bad_request("Invalid phone number") # phone validate
        
        if not isinstance(data['salary'], int) or data['salary'] < 0:
            return bad_request("Salary must be a positive integer") 
        
        emp =Employee(
            name = data['name'],
            email = data['email'],
            phone = data['phone'],
            designation = data['designation'],
            salary = data['salary']
        )
        db.session.add(emp)
        db.session.commit()
        return jsonify({"message":'Employee added successfully'}),201
    except Exception as e:
        return server_error(str(e))

# Get All Employees

@app.route('/employees',methods=['GET'])
def get_employees():
    try:    
        employees = Employee.query.all()
        result = []
        for emp in employees:
            result.append({
                "id":emp.id,
                "name":emp.name,
                "email":emp.email,
                "phone":emp.phone,
                "designation":emp.designation,
                "salary":emp.salary
            })
        return jsonify(result)
    except Exception as e:
        return server_error(str(e))


# Update Employee

@app.route('/employees/<int:id>',methods=['PUT'])
def update_employee(id):
    try:
        emp = Employee.query.get(id)
        if not emp:
            return not_found("Employee not found")
        data = request.json
        if not data:
            return bad_request("JSON data is required")
        
        if 'email' in data and not is_valid_email(data['email']):  # mail validate
            return bad_request("Invalid email format")
        
        if 'phone' in data and not is_valid_phone(data['phone']):  # phone validate
            return bad_request("Invalid phone number")
        
        if 'salary' in data:
            if not isinstance(data['salary'], int) or data['salary'] < 0:  # salary validate without negative
                return bad_request("Salary must be a positive integer")
        
        if "email" in data:
            if not is_valid_email(data["email"]):
                return bad_request("Invalid email format")

            email_owner = Employee.query.filter_by(email=data["email"]).first()
            if email_owner and email_owner.id != id:
                return bad_request("Email already exists")  # unique mail validate

        
        emp.name = data.get('name',emp.name)
        emp.email = data.get('email',emp.email)
        emp.phone = data.get('phone',emp.phone)
        emp.designation = data.get('designation',emp.designation)
        emp.salary = data.get('salary',emp.salary)

        db.session.commit()
        return jsonify({"message":'Employee updated successfully'})
    except Exception as e:
        return server_error(str(e))
    

# Delete Employee

@app.route('/employees/<int:id>',methods=['DELETE'])
def delete_employee(id):
    try:
        emp = Employee.query.get(id)
        if not emp:
            return not_found("Employee not found")
        db.session.delete(emp)
        db.session.commit()
        return jsonify({"message":'Employee deleted successfully'})
    
    except Exception as e:
        return server_error(str(e))
    


# ================================================== App Run ==================================================
with app.app_context():
    db.create_all()
app.run(debug=True)