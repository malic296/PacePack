import os
import json
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_mail import Mail
from forms import LoginForm, RegisterForm, VerificationForm
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from mailService import send_verification_code,generate_verification_code
from datetime import datetime, timedelta
from dbHelper.services.UserService import UserService
from dbHelper.services.AddressService import AddressService
from dbHelper.services.PasswordService import PasswordService
from dbHelper.DBModels import User

load_dotenv("environment.env")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
csrf = CSRFProtect(app)

app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS") == "True"
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")

user_service = UserService()
address_service = AddressService()
password_service = PasswordService()

mail = Mail(app)

@app.route("/")
def index():
    session["lang"] = "en"
    session["theme"] = "light"
    return redirect(url_for("content_section", section="index"))
    
@app.route("/set_language/<lang>")
def set_language(lang):
    session["lang"] = lang
    return redirect(url_for("content_section", section=session["section"]))

@app.route("/toggle-theme")
def toggle_theme():
    session["theme"] = "dark" if session.get("theme", "light") == "light" else "light"
    return redirect(url_for("content_section", section=session.get("section", "index")))

@app.route("/logout")
def logout():
    session.pop("user_token", None)
    return redirect(url_for("content_section", section = "login"))


@app.route("/content/<section>", methods=["GET", "POST"])
def content_section(section):
    templates = {
        "home": "home.html",
        "races": "races.html",
        "runs": "runs.html",
        "index": "index.html",
        "login": "login.html",
        "register": "register.html",
        "verify": "verify.html",
        "myProfile": "myProfile.html"
    }

    public_sections = {"login", "register", "verify", "index"}

    if section not in public_sections and "user_token" not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for("content_section", section="login"))

    with open("textVars.json", "r", encoding="utf-8") as f:
        textVars = json.load(f)

    textVars = textVars["pages"][section][session["lang"]]
    
    if section in templates:
        session["section"] = section
        if section == "login" :
            form = LoginForm()
            if form.validate_on_submit():
                email = form.email.data
                password = form.password.data

                verification_code = generate_verification_code()
                session["verification_code"] = verification_code
                session["code_expiration"] = (datetime.now() + timedelta(minutes=2)).isoformat()
                session["email"] = email

                if password_service.validate_user_login(email, password):
                    if send_verification_code(email, verification_code):
                        session["user_email"] = email
                        flash("A verification code has been sent to your email.", "info")
                        return redirect(url_for("content_section", section="verify"))
                    else:
                        flash("Error sending verification email. Please try again.", "danger")
                else:
                    flash("Wrong credentials.", "danger")
                    return redirect(url_for("content_section", section="login"))
                

            return render_template(templates[section], section=section, form=form)
        elif section == "register":
            form = RegisterForm()
            if form.validate_on_submit():
                name = form.name.data
                surname = form.surname.data
                email = form.email.data
                password = form.password.data
                confirmPassword = form.confirmPassword.data
                gender = form.gender.data
                telephone = form.telephone.data
                telephoneCode = form.telephoneCode.data
                postalCode = form.postalcode.data
                country = form.country.data
                streetName = form.streetname.data

                verification_code = generate_verification_code()
                session["verification_code"] = verification_code
                session["code_expiration"] = (datetime.now() + timedelta(minutes=2)).isoformat()
                session["email"] = email

                # test if email is in use 
                if user_service.isUserEmailInUse(email):
                    flash("Provided email is already in use", "danger")
                    return redirect(url_for("content_section", section="register"))
                
                # test if password was written correctly 
                if password != confirmPassword:
                    flash("Passwords do not match", "danger")
                    return redirect(url_for("content_section", section="register"))
            
                # user registration
                session["pending_registration"] = {
                    "name": name,
                    "surname": surname,
                    "email": email,
                    "password": password,
                    "gender": gender,
                    "telephone": telephone,
                    "telephoneCode": telephoneCode,
                    "postalCode": postalCode,
                    "country": country,
                    "streetName": streetName,
                }

                if send_verification_code(email, verification_code):
                    session["user_email"] = email
                    flash("A verification code has been sent to your email.", "info")
                    return redirect(url_for("content_section", section="verify"))
                else:
                    flash("Error sending verification email. Please try again.", "danger")
                
            return render_template(templates[section], section=section, form=form)

        elif section == "verify":
            form = VerificationForm()
            if request.method == "POST":
                expiration_time = datetime.fromisoformat(session.get("code_expiration", "1970-01-01T00:00:00"))
                if datetime.now() > expiration_time:
                    flash("The verification code has expired.", "danger")
                    return redirect(url_for("content_section", section="verify"))

                entered_code = form.code.data
                if entered_code == session.get("verification_code"):
                    flash("Verification successful!", "success")
                    session["user_token"] = session["user_email"]
                    session.pop("user_email", None)
                    pending_registration = session.pop("pending_registration", None)
                    if pending_registration:
                        password_id = password_service.add_password(pending_registration["password"])
                        address_id = address_service.add_address(
                            pending_registration["streetName"], 
                            pending_registration["postalCode"], 
                            pending_registration["country"]
                        )
                        user_service.add_user(
                            pending_registration["name"], 
                            pending_registration["surname"], 
                            pending_registration["email"], 
                            pending_registration["telephone"], 
                            pending_registration["telephoneCode"], 
                            False, True, 
                            pending_registration["gender"], 
                            password_id, 
                            address_id
                        )
                        # REGISTERED
                        flash("Your account has been created successfully!", "success")
                        return redirect(url_for("content_section", section="home"))

                    else:
                        # LOGGED ON
                        flash("Login was successful.", "success")
                        return redirect(url_for("content_section", section="home"))
                else:
                    flash("Invalid code. Please try again.", "danger")

            return render_template(templates[section], section=section, textVars=textVars, form=form)

        else:
            return render_template(templates[section], section=section, textVars=textVars)

    else:
        return "<h2>Section Not Found</h2>", 404
    

if __name__ == "__main__":
    app.run(debug=True)
