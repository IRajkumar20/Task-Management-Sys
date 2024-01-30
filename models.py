from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db=SQLAlchemy()
ma=Marshmallow()

# User table
class User(db.Model):

    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(100),unique=True )
    email=db.Column(db.String(200),unique=True)
    password=db.Column(db.String(100),unique=True)
    roleID=db.Column(db.Integer, db.ForeignKey('role.id'))
    task=db.relationship("Task",backref='user')

    def __init__(self,username,email,password,roleID):
        self.username=username
        self.email=email
        self.password=password
        self.roleID=roleID

class UserSchema(ma.Schema):
    class Meta():
        fields=('id',"username","email","password","roleID")

user_schema=UserSchema()
users_schema=UserSchema(many=True)        

# role table

class Role(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    relation=db.relationship("User",backref='role')
    relation1=db.relationship("UserTrash",backref='role')

    def __init__ (self,name):
        self.name=name


class RoleSchema(ma.Schema):
    class Meta():
        fields=("id","name")  

role_schema=RoleSchema()
roles_schema=RoleSchema(many=True)  

# status table

class Status(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(10),unique=True)
    task=db.relationship('Task',backref='status')
    def __init__ (self,name):
        self.name=name

class StatusSchema(ma.Schema):
    class Meta():
        fields=("id","name")

status_schemas=StatusSchema(many=True)

# task table

class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    details=db.Column(db.String(200))
    statusID=db.Column(db.Integer,db.ForeignKey("status.id"),default=2)
    userID=db.Column(db.Integer,db.ForeignKey("user.id"))

    def __init__(self,name,details,userID):
        self.name=name
        self.details=details       
        self.userID=userID

class TaskSchema(ma.Schema):
    class Meta():
        fields=("id","name","details","status","username")

task_schema=TaskSchema()
tasks_schema=TaskSchema(many=True)
    

# deleted task db

class TaskTrash(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    details=db.Column(db.String(200))
    statusID=db.Column(db.Integer,db.ForeignKey("status.id"),default=1)
    userID=db.Column(db.Integer,db.ForeignKey("user.id"))
    
    def __init__(self,name,details,userID):
        self.name=name
        self.details=details       
        self.userID=userID

class deleteSchema(ma.Schema):
    class Meta():
        fields=("id","name","details","status","username")

# deleted user db

class UserTrash(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(100),unique=True )
    email=db.Column(db.String(200),unique=True)
    password=db.Column(db.String(100),unique=True)
    roleID=db.Column(db.Integer, db.ForeignKey('role.id'))
    # task=db.relationship("Task",backref='user')
    
    def __init__(self,username,email,password,roleID):
        self.username=username
        self.email=email
        self.password=password
        self.roleID=roleID

class UserSchema(ma.Schema):
    class Meta():
        fields=('id',"name","email","password","roleID")



