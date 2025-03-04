from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/content")
def content():
    #return render_template("content.html", section="home")
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
