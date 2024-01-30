from flask import Blueprint,request,jsonify
from models import Role,db,roles_schema
from flask_jwt_extended import jwt_required


role=Blueprint('role',__name__)

@role.route("/role",methods=["post"])
def role_add():  
    role_name=request.json['role_name']
    role=Role(role_name)
    db.session.add(role)
    db.session.commit()

    return jsonify({
        "message":"role added"
        }

    ),201

@role.route("/showrole", methods=["GET"])
def show_role():
    role=Role.query.all()
    return roles_schema.dump(role)