from flask import Flask
from flask_sqlalchemy import SQLAlchemy      ## Setting a SQL based Database instance. 
from flask_bcrypt import Bcrypt              ## For password hashing and authentication.
from flask_login import LoginManager         ## Specifically for log in of User.
from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)                           # creating an instance for db: from now db will be mentioned wherever SQLAlchemy is required
bcrypt = Bcrypt(app)                           # creating an instance for bcrypt : ''
login_manager = LoginManager(app)              # creating an instance for login_manager: ''
login_manager.login_view = 'login'  
login_manager.login_message_category = 'info'  ## for messages to be presented in stylish blue highlight.



# class MyModelView(ModelView):
#     def is_authorized(self):
#         return False
            


ad = Admin(app)
# ad.add_view(MyModelView(User, db.session))



from flask_blog import routes   
## Importing here just in order to avoid Circular Imports
## Routes are importing modules from flask_blog and if __init__ will also import routes in the beginni
## This will go on forever and the code will not run.