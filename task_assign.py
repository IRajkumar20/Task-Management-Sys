from flask import Blueprint,request
from models import Role,User,Task,TaskTrash,db,task_schema,tasks_schema,Status
from flask_jwt_extended import get_jwt_identity,get_jwt,jwt_required

task=Blueprint("task", __name__)

@task.route("/task",methods=["post"])    
def task_assign():
    token_id=get_jwt_identity()
    role_id=get_jwt()['role']

    name=request.json['name']
    details=request.json['details']
    staffID=request.json['staffID']


    if Role.query.filter_by(id=role_id).first().name=='admin':
        
        staff=User.query.filter_by(id = staffID).first()
        if staff:
    
            create_task = Task(name,details,staffID)
            db.session.add(create_task)
            db.session.commit()                    
            return "successfully task assigned"               
           
        else:
             return {"message":"given staff id is not present"}
    else:
        return {"warning":"only admin can assign task"}



@task.route("/deltask/<id>",methods=["delete"])
def delete_task(id):
    if Task.query.filter_by(id=id).first() is not None :
        task=Task.query.get(id)
        deldata=TaskTrash(task.name,task.details,task.userID)
        db.session.add(deldata)
        db.session.delete(task)
        db.session.commit()
        return "Successfully task deleted"
    else :
        return "id not present in task table"

@task.route("/taskupdate/<id>",methods=['put'])
def update_task(id):

    role_id=get_jwt()['role']    
    
    if Role.query.filter_by(id=role_id).first().name=='admin':
        if Task.query.filter_by(id=id).first() is not None :
            name=request.json['name']
            details=request.json['details']
            staffID=request.json['staffID']

            task=Task.query.get(id)
            task.name=name
            task.details=details
            task.staffID=staffID
            db.session.commit()
            return "Successfully updated"
        else:
            return "id not prsent in task table"
    else:
        req_id=get_jwt_identity()
        StatusID=request.json['statusID']        
        if Task.query.get(id).userID == int(req_id): 
            task=Task.query.get(id)
            task.statusID=StatusID
            db.session.commit()
        else:
            return "task status only access"
    return "Successfull status update"


@task.route("/showtask")
def show_task():
    role_id=get_jwt()['role']
    if Role.query.get(role_id).name =='admin':
        query=Task.query.with_entities(Task.id,Task.name,Task.details,Status.name.label("status"),User.username.label("username")).join(Status).join(User)
        task=query.all()
        return {"tasks":tasks_schema.dump(task)}
    else:
        req_id=get_jwt_identity()               
        if Task.query.filter_by(userID=req_id).first() is not None :
            query=Task.query.with_entities(Task.id,Task.name,Task.details,Status.name.label("status"),User.username.label("username")).join(Status).join(User)

            task = query.filter(Task.userID==req_id).all()
            return {"task":tasks_schema.dump(task)}
        else:
            return "Zero Task"
        
    
@task.route("/showtask/<id>")
def showtask(id):
    role_id=get_jwt()['role']    
    
    if Role.query.filter_by(id=role_id).first().name=='admin':
        if Task.query.filter_by(id=id).first() is not None :
            query=Task.query.with_entities(Task.id,Task.details,Task.name,Status.name.label("status"),User.username.label("username")).join(Status).join(User)
            
            task=query.filter(Task.id==id).first()
            return {"task":task_schema.dump(task)}
        else:
            return "id not prsent in task table"
    else:
        return "only admin can to see specified task"





    
