from flask import Blueprint, current_app,request,jsonify
from flask_mail import Message,Mail

import validators
from werkzeug.security import generate_password_hash
from models import db,User,user_schema,users_schema,UserTrash,Role




blue=Blueprint('blue', __name__)




@blue.route("/register",methods=["post"])

def register():

    username=request.json['username']
    email=request.json['email']
    password=request.json['password']
    roleID=request.json['roleID']
    
    
    if len(username)<5:
        return jsonify({"error":"username must be have above 6 character"})
    
    if len(password)<8:
        return jsonify({"error":"passwor must be in 8 character"})
    
    if not username.isalnum() or " " in username:
        return jsonify({"error":"should be in alpha numeric without space"})
    
    if not validators.email(email):
        return jsonify({"error":"email is invalid"}) 
    
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error":"email is taken"})
    
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error":"username is taken"})
    
    pwd_hash=generate_password_hash(password)
       
    user=User(username,email,pwd_hash,roleID)
    
    msg = Message('Hello ' + username +",", sender='ilangojayaraj07@gmail.com', recipients=[email])
    msg.body = 'register completed.'  +"\n" + "email: " + email + "\n"+ "password: "+password
                
    mail = Mail(current_app)  # Initialize the mail object 
    Mail.send(message=msg,self=mail)
    

    
    
    db.session.add(user)
    db.session.commit()

    
    return jsonify({
        "message":"user created",
        "user":{
            "username":username,
            "email":email
        }

    }),201

@blue.route(('/show/<id>'), methods=['GET'])
def getproductbyid(id):

    if User.query.filter_by(id=id).first() is not None :
        query=User.query.with_entities(User.id,User.username,User.email,Role.name.label("roleID")).join(Role)
        user=query.filter(User.id==id).first()
        return {"user":user_schema.dump(user)}
    else:
        return "id not prsent in User table"

@blue.route('/upd/<id>', methods=['PUT'])
def Updateuser(id):
    if User.query.filter_by(id=id).first() is not None:
        user=User.query.get(id)
        username=request.json['username']
        email=request.json['email']
        password=request.json['password']
        roleID=request.json['roleID'] 
        
        pwd_hash=generate_password_hash(password)
        user.username=username
        user.email=email
        user.password=pwd_hash
        user.roleID=roleID
        
        db.session.commit()
        return "details updated successfully"
    else:
        return "id not prsent in User table"
    

@blue.route("/del/<id>" , methods=["DELETE"])
def Deleteuser(id):
    if User.query.filter_by(id=id).first() is not None :
        user=User.query.get(id)
        deldata=UserTrash(user.username,user.password,user.email,user.roleID)
        db.session.add(deldata)
        db.session.delete(user)
        db.session.commit()
        return "successfully deleted"
    else:
        return "id not prsent in User table"

@blue.route("/showall" , methods=["GET"])
def show_all():
    query=User.query.with_entities(User.id,User.username,User.email,Role.name.label("roleID")).join(Role)
    user=query.all()
    return {"user":users_schema.dump(user)}


