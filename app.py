import os
from flask import Flask, render_template, redirect, url_for, flash
from forms import LoginForm, RegisterForm
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

load_dotenv("environment.env")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
csrf = CSRFProtect(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if(email == "test@gmail.com" and password == "test"):
             flash("Login successful!", "success")
             return redirect(url_for("content"))
   
        flash("Invalid username or password", "danger")
    return render_template("login.html", form=form)
    

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        gender = form.gender.data
        telephone = form.telephone.data
        telephoneCode = form.telephone.data
        postalCode = form.postalcode.data
        country = form.country.data
        streetName = form.streetname.data
        if name == "admin":
            flash("Login successful!", "success")
            return redirect(url_for("content"))
        flash("Invalid username or password", "danger") 

    return render_template("register.html", form=form)

@app.route("/content")
def content():
    return redirect(url_for("content_section", section = "home"))

@app.route("/content/<section>")
def content_section(section):
    templates = {
        "home": "home.html",
        "races": "races.html",
        "runs": "runs.html"
    }
    
    if section in templates:
        return render_template(templates[section], section=section)
    else:
        return "<h2>Section Not Found</h2>", 404

if __name__ == "__main__":
    app.run(debug=True)
