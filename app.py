import os
import json
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_mail import Mail
from forms import LoginForm, RegisterForm, VerificationForm
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from mailService import send_verification_code,generate_verification_code
from datetime import datetime, timedelta

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

                if send_verification_code(email, verification_code):
                    flash("A verification code has been sent to your email.", "info")
                    return redirect(url_for("content_section", section="verify"))
                else:
                    flash("Error sending verification email. Please try again.", "danger")

                if(email == "miroslav.pavlik1@seznam.cz" and password == "test"):
                    session["user_token"] = "usertokenforverification"
                    return redirect(url_for("content_section", section = "verify"))

            return render_template(templates[section], section=section, form=form)
        elif section == "register":
            form = RegisterForm()
            if form.validate_on_submit():
                name = form.name.data
                surname = form.surname.data
                email = form.email.data
                gender = form.gender.data
                telephone = form.telephone.data
                postalCode = form.postalcode.data
                country = form.country.data
                streetName = form.streetname.data

                verification_code = generate_verification_code()
                session["verification_code"] = verification_code
                session["code_expiration"] = (datetime.now() + timedelta(minutes=2)).isoformat()
                session["email"] = email

                if send_verification_code(email, verification_code):
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
                    session["user_token"] = "usertokenforverification"
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
