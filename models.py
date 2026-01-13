from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 

class Employee(db.Model): # database table create
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    phone = db.Column(db.String(15),nullable=False)
    designation = db.Column(db.String(50),nullable=False)
    salary = db.Column(db.Integer,nullable=False)