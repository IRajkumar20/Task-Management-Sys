from flask import Blueprint,request
from werkzeug.security import check_password_hash
from models import User,user_schema
from flask_jwt_extended import create_refresh_token,create_access_token,get_jwt_identity,jwt_required



login=Blueprint("login",__name__)

@login.post("/login")
def user_login():
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username).first()

    if user:
        is_correct_pwd=check_password_hash(user.password,password)
        
        if is_correct_pwd:
            refresh=create_refresh_token(identity=user.id,additional_claims={"role":user.roleID})
            access=create_access_token(identity=user.id,additional_claims={"role":user.roleID})

            return {
                'user':{
                    'refresh':refresh,
                    'access':access,
                    'username':user.username,
                    'id':user.id
                }
            }
        return{'message':'wrong credentials'}
    else:
        return{'message':'wrong name entered credentials'}


@login.get("/token")

def token():
    user_id=get_jwt_identity()
    user=User.query.filter_by(id=user_id).first()
    
    return {
        "username":user.username,
        "email":user.email
    }

@login.get("/token/refresh")
@jwt_required(refresh=True)

def refresh_token():
    identity=get_jwt_identity()
    access=create_access_token(identity=identity)

    return {
        "access":access
    }