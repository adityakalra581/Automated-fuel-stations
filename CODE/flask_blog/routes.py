import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flask_blog import app, db, bcrypt
from flask_blog.forms import RegistrationForm, LoginForm, UpdateProfileForm
from flask_blog.models import User
from flask_login import login_user,current_user, logout_user, login_required


## flask_blog is a directory inside which an __init__ file is present which will run every time whenever flask_blog is called
## It is used in order to avoid the error of Circular import.

## app,db,bcrypt all are instances created for initiating flask, SQL , Hashing the encrypted passwords respectively.

## current_user: here it is used for identifying whether the user is logged in or not.





@app.route('/')
def home():
    return render_template('home.html',title='HOME')


@app.route('/about')
def about():
	return render_template('about.html',title='about')



## methods essential for getting and posting of data.
## adding functionality requires it.

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')              ## decode('utf-8') will convert it into encrypted string.
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)        ## adding password to variable will make sure it does not change every time
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)





@app.route("/login", methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:                        
    ## is_authenticated:  
    ## This property should return True if the user is authenticated,
    ## i.e. they have provided valid credentials.
    ## (Only authenticated users will fulfill the criteria of login_required.)
    
        return redirect(url_for('home'))                     
    form = LoginForm()
    if form.validate_on_submit():                                              
        user = User.query.filter_by(email=form.email.data).first()        ## SQL query : will provide the email of the 
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


## After log in user should not see log in and register option again.
## Instead they should have logout option.

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    ## This will automatically reduce the size before saving.
    ## Neccessaery for saving space and making website faster.
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profile has been updated!','success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email 
    image_file = url_for('static', filename = 'profile_pics/'+ current_user.image_file)
    return render_template('profile.html',title='Profile',image_file=image_file,form = form )

## @login_required will make sure that "/account" page will prompt the user to log in
## if already not logged in.