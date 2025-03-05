import os
import json
from flask import Flask, render_template, redirect, url_for, flash, session
from forms import LoginForm, RegisterForm
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

load_dotenv("environment.env")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
csrf = CSRFProtect(app)

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

@app.route("/content/<section>", methods=["GET", "POST"])
def content_section(section):
    templates = {
        "home": "home.html",
        "races": "races.html",
        "runs": "runs.html",
        "index": "index.html",
        "login": "login.html",
        "register": "register.html"
    }

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

                if(email == "test" and password == "test"):
                    return redirect(url_for("content_section", section = "home"))

            return render_template(templates[section], section=section, form=form)
        elif section == "register":
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
                    return redirect(url_for("content_section", section = "home"))
            return render_template(templates[section], section=section, form=form) 
        else:
            return render_template(templates[section], section=section, textVars=textVars)
        
    else:
        return "<h2>Section Not Found</h2>", 404

if __name__ == "__main__":
    app.run(debug=True)
