from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,login_required,logout_user,current_user

auth=Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        mail=request.form.get('email')
        password=request.form.get('password')
        user= User.query.filter_by(email=mail).first()
        if user:
            if check_password_hash(user.password,password):
                flash(f'''Welcome home! {mail[:-10]}''',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, Try again', category='error')
        else:
            flash('Email does not exist',category='error')
            #return redirect('/signup')
    return render_template("login.html", user=current_user)
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
    
@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        mail=request.form.get('email')
        firstname=request.form.get('firstname')
        lastname=request.form.get('lastname')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        user= User.query.filter_by(email=mail).first()
        #authentication checks
        if user:
            flash('Email already exists,Please try logging in',category='error')
            return redirect('/login')
        elif mail.count('@')!=1 or mail.count('.')<1 or mail.count('.')>2:
            flash('Invalid email address',category='error')
        elif len(firstname)<2:
            flash('First name is too short',category='error')
        elif len(lastname)<2:
            flash('First name is too short',category='error')
        elif len(password1)<7:
            flash('Password must be atleast 8 characters',category='error')
        elif password1!=password2 or password1=='' or password2=='':
            flash('Passwords do not match',category='error')
        else:
            new_user=User(email=mail,first_name=firstname,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user=new_user,remember=True)
            flash('Account Created successfully!',category='success')
            return redirect(url_for('views.home'))
    return render_template("signup.html",user=current_user)
@auth.route('/home')
@login_required
def home():
    return render_template("home.html",user=current_user)
