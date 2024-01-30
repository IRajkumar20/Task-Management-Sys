from flask import Flask, request, send_from_directory
from flask_jwt_extended import JWTManager,verify_jwt_in_request,get_jwt
from models import db,ma,Role
from flask_mail import Mail
from flask_swagger_ui import get_swaggerui_blueprint
import os,jwt






# blueprints
from user_register import blue
from login import login
from add_role import role
from add_status import status
from task_assign import task



app=Flask(__name__)



basedir=os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['JWT_SECRET_KEY'] = "HELLO"



# mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ilangojayaraj07@gmail.com'
app.config['MAIL_PASSWORD'] = 'efsi mfyp jslu ionm'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

Mail(app)






db.init_app(app)
ma.init_app(app)
JWTManager(app)







with app.app_context():
    db.create_all()

# Flask Limiter


# swagger

SWAGGER_URL = '/openapi/docs' 
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  
    API_URL,
    config={ 
        'app_name': "Test application"
    },
)







app.register_blueprint(blue)
app.register_blueprint(login)
app.register_blueprint(role)
app.register_blueprint(status)
app.register_blueprint(swaggerui_blueprint)
app.register_blueprint(task)





@app.before_request
def authentication():

    path=request.endpoint
    
    secure=["task.task","task.delete_task","blue.Updateuser","blue.Deleteuser","blue.register"]
    
    if request.method != "OPTIONS":
        print(path)
        if path != "login.user_login" and path != "static" and path != "swagger_ui.show" and path != "login.refresh_token": 
            try:  
                verify_jwt_in_request()

            except jwt.InvalidTokenError:
                  return ({"message": "Token  is invalid"})   
            
            role = get_jwt()["role"] 
            if Role.query.filter_by(id=role).first().name !='admin':
                if path in secure:
                    return ("admin only access"),401
               

TIMEOUT_MESSAGE = "Request exceeded time limit."

@app.errorhandler(429)
def handle_timeout_error(error):
    return {'error': TIMEOUT_MESSAGE}, 429

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")




