from flask import Blueprint, render_template, request, url_for, flash,redirect
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth',__name__)


@auth.route('/login',methods =["POST","GET"])
def Login():  
    if request.method == "POST":
        data = request.form
        email = data.get("email")
        password = data.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                login_user(user,remember=True)
                return redirect(url_for("views.Home"))
            else:
                flash("Incorrect username and password, try again",category="error")
        else:
            flash("No User Found",category="error")

    return render_template("login.html",username ="",password = "",authenticated= False)


@auth.route('/logout')
@login_required
def Logout():
    print("user logged out ")
    logout_user()
    return redirect(url_for("auth.Login"))



@auth.route('/sign-up',methods =["POST","GET"])
def Sign_out():
    if request.method == "POST":
        data = request.form
        email = data.get('email')
        name = data.get('name')
        password = data.get('password')
        password2 = data.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exist.",category="error")
        elif len(email) < 4:
            flash("Please enter valid email address.",category="error")
        elif len(name) < 2:
            flash("Please enter full name.",category="error")
        elif password!=password2:
            flash("Password mismatch, both passwords must be same.",category="error")
        elif len(password) < 2:
            flash("Enter a strong password.",category="error")
        else: 
            new_user = User(name = name, email = email, password = generate_password_hash(password2, method="scrypt"))
            db.session.add(new_user)
            db.session.commit() 
            return redirect(url_for("auth.Login"))

        return render_template("sign_up.html")    
    else:
        return render_template("sign_up.html")