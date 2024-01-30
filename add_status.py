from flask import Blueprint,request,jsonify
from models import Status,db,status_schemas
from flask_jwt_extended import jwt_required

status=Blueprint('status',__name__)

@status.route("/status",methods=["post"])
# @jwt_required()
def status_add():
  
    status_name=request.json['status_name']

    role=Status(status_name)

    db.session.add(role)
    db.session.commit()

    return jsonify({
        "message":"status added"
        }

    ),201

@status.route("/showstatus",methods=["get"])
def show_status():
    status=Status.query.all()
    return status_schemas.dump(status)