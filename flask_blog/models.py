from flask import url_for, redirect 
from flask_blog import db, login_manager, ad
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin


## login_manager is a instance similar to db present inside our flask_blog : __init__ package.
## UserMixin provides the functionality 


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Fuel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    address = db.Column(db.String(50))
    state = db.Column(db.String(10))
    
    def __repr__(self):
        return f"Fuel('{self.name}', '{self.address}', '{self.state}')"



# class FuelSchema(ma.Schema):
#     class Meta:
#         fields = ('id','name','address','state')


# fuel_schema = FuelSchema()  
# fuels_schema = FuelSchema(many=True)



class MyModelView(ModelView):
    def is_authorized(self):
        return False
            

ad.add_view(MyModelView(User, db.session))
ad.add_view(ModelView(Fuel,db.session))




### Class User here will create an sql table present inside site.db