import os
import json
from flask import Flask, render_template, redirect, request, url_for, flash, session, g
from flask_mail import Mail
from forms import LoginForm, RegisterForm, VerificationForm, EditProfileForm, RunForm, RaceForm, EmptyForm, SponsorForm
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from mailService import send_verification_code,generate_verification_code
from datetime import date, datetime, timedelta
from dbHelper.services.UserService import UserService
from dbHelper.services.AddressService import AddressService
from dbHelper.services.PasswordService import PasswordService
from dbHelper.services.RunService import RunService
from dbHelper.services.UserRunService import UserRunService
from dbHelper.services.TeamService import TeamService
from dbHelper.services.PaymentService import PaymentService
from dbHelper.services.RaceService import RaceService
from dbHelper.services.UserRaceService import UserRaceService
from dbHelper.services.SponsorService import SponsorService

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
run_service = RunService()
user_run_service = UserRunService()
team_service = TeamService()
payment_service = PaymentService()
race_service = RaceService()
user_race_service = UserRaceService()
sponsor_service = SponsorService()

mail = Mail(app)

@app.before_request
def load_current_user():
    g.current_user = get_current_user()

@app.route("/")
def index():
    session["lang"] = "en"
    session["theme"] = "light"
    return redirect(url_for("content_section", section="index"))
    
@app.route("/set_language/<lang>")
def set_language(lang):
    session["lang"] = lang
    return redirect(url_for("content_section", section=session["section"]))

@app.route("/register_user/<userid>/<runid>")
def register_user(userid, runid):
    added = user_run_service.register_user_to_run(userId=userid, runId=runid)
    if added:
        flash("Registration successful", "success")
    else:
        flash("error", "danger")
    return redirect(url_for("content_section", section=session["section"]))

@app.route("/unregister_user/<userid>/<runid>")
def unregister_user(userid, runid):
    removed = user_run_service.unregister_user_from_run(userId=userid, runId=runid)
    if removed:
        flash("Unregistration successful", "success")
    else:
        flash("error", "danger")
    return redirect(url_for("content_section", section=session["section"]))

@app.route("/toggle-theme")
def toggle_theme():
    session["theme"] = "dark" if session.get("theme", "light") == "light" else "light"
    return redirect(url_for("content_section", section=session.get("section", "index")))

@app.route("/logout")
def logout():
    session.pop("user_token", None)
    return redirect(url_for("content_section", section = "login"))


@app.route("/content/<path:section>", methods=["GET", "POST"])
def content_section(section):
    templates = {
        "home": "home.html",
        "races": "races.html",
        "runs": "runs.html",
        "teams": "teams.html",
        "index": "index.html",
        "login": "login.html",
        "register": "register.html",
        "verify": "verify.html",
        "myProfile": "myProfile.html",
        "resend" : "verify.html",
        "run_detail" : "run_detail.html",
        "race_detail" : "race_detail.html",
        "sponsors" : "sponsors.html"
    }

    public_sections = {"login", "register", "verify", "index","resend"}

    if section not in public_sections and "user_token" not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for("content_section", section="login"))

    with open("textVars.json", "r", encoding="utf-8") as f:
        textVars = json.load(f)

    if section.startswith("runs/"):
        run_id = int(section.split("/")[1])  # Extract the run_id from the URL
        section = "run_detail"  # We map the 'runs/ID' to the 'run_detail' section
    elif section.startswith("races/"):
        race_id = int(section.split("/")[1])
        section = "race_detail"

    textVars = textVars["pages"][section][session["lang"]]

    
    if section in templates:
        session["section"] = section
        match section:
            case "login":
                return loginSection(textVars)
            case "register":
                return registerSection(textVars)
            case "verify":
                return verifySection(textVars)
            case "resend":
                return resendCode()
            case "home":
                return homeSection(textVars)
            case "myProfile":
                return myProfileSection(textVars)
            case "index":
                return indexSection(textVars)
            case "races":
                return racesSection(textVars)
            case "runs":
                return runsSection(textVars)
            case "teams":
                return teamsSection(textVars)
            case "run_detail":
                return runDetailSection(textVars, run_id)
            case "race_detail":
                return raceDetailSection(textVars, race_id)
            case "sponsors" :
                return sponsorsSection(textVars)
            case _:
                return "<h2>Section Not Found</h2>", 404
    else:
        return "<h2>Section Not Found</h2>", 404
    
    
# Root app methods
def loginSection(textVars):
    form = LoginForm(lang=session.get("lang", "en"))
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
            flash("Wrong email or password.", "danger")
            return redirect(url_for("content_section", section="login"))
        
    return render_template("login.html", section="login", textVars=textVars, form=form)

def registerSection(textVars):
    form = RegisterForm(lang=session.get("lang", "en"))
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

    return render_template("register.html", section="register", textVars=textVars, form=form)

def verifySection(textVars):
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
                # LOGGED IN
                flash("Login was successful.", "success")
                return redirect(url_for("content_section", section="home"))
        else:
            flash("Invalid code. Please try again.", "danger")

    return render_template("verify.html", section="verify", textVars=textVars, form=form)

def resendCode():
    if "email" not in session:
        flash("Session expired. Please log in again.", "warning")
        return redirect(url_for("content_section", section="login"))

    new_code = generate_verification_code()
    session["verification_code"] = new_code
    session["code_expiration"] = (datetime.now() + timedelta(minutes=2)).isoformat()

    if send_verification_code(session["email"], new_code):
        flash("A new verification code has been sent.", "info")
    else:
        flash("Error sending the verification email. Please try again.", "danger")

    return redirect(url_for("content_section", section="verify"))

def myProfileSection(textVars):
    form = EditProfileForm()  # Create form instance

    if form.validate_on_submit():  # Check if form is submitted
        name = form.name.data
        surname = form.surname.data
        telephone = form.telephone.data
        gender = form.gender.data
        country = form.country.data
        streetname = form.streetname.data
        postalcode = form.postalcode.data

        if not user_service.updateUser(session["user_token"], name, surname, telephone, gender, country, streetname, postalcode):
            flash("The update failed", "danger")
        else:
            flash("Profile updated successfully!", "success")

    user = user_service.getUserInfo(session["user_token"])  # Get updated user info
    return render_template("myProfile.html", section="myProfile", textVars=textVars, user=user, form=form)

def homeSection(textVars):
    user_id = g.current_user.id
    all_runs = run_service.get_all_runs()
    past_runs = run_service.get_past_runs()

    run_count = len(past_runs)
    
    user_upcoming_runs = []
    for run in all_runs:
        user_run = user_run_service.get_user_run_by_run_id_and_user_id(run.id, user_id)
        if user_run:
            user_upcoming_runs.append({
            "run": run,
            "is_creator": user_run.iscreator
                })
    print("RUNCOUNT", run_count)
   

    return render_template("home.html",section="home",textVars=textVars,upcoming_runs=user_upcoming_runs, run_count = run_count)


def indexSection(textVars):
    return render_template("index.html", section="index", textVars=textVars)

# TODO: 
def racesSection(textVars):
    form = RaceForm()

    if request.method == "POST":
        if "delete_race_id" in request.form:
            # Handle run deletion
            race_id = request.form.get("delete_race_id")
            deleted_race = race_service.get_race_by_id(race_id)  # Fetch race before deleting
            if deleted_race:
                success = race_service.delete_race(race_id)
                if success:
                    flash(f"Race '{deleted_race.name}' deleted successfully!", "success")
                else:
                    flash("Error deleting race.", "danger")
            else:
                flash("Race not found.", "danger")
        else:
            # Handle race creation or update
            race_id = request.form.get("race_id")
            streetname = request.form.get("streetname")
            postalcode = request.form.get("postalcode")
            country = request.form.get("country")
            date = request.form.get("date")
            time = request.form.get("time")
            name = request.form.get("name")
            description = request.form.get("description")

            if race_id:
                try:
                   # TODO 
                    updated_race = race_service.update_race(race_id, streetname, postalcode, country, date, time, name, description)
                    flash(f"Race '{updated_race.name}' updated successfully!", "success")
                except Exception as e:
                    flash(f"Error updating race: {str(e)}", "danger")
            else:
                try:
                    new_race = race_service.add_race(streetname, postalcode, country, date, time, name, description)
                    flash(f"Race '{new_race.name}' created successfully!", "success")
                    user_race_service.create_race_and_add_creator(g.current_user.id, new_race.id)
                except Exception as e:
                    flash(f"Error creating race: {str(e)}", "danger")

        return redirect(url_for("content_section", section="races"))
    
    # Get the sorting parameters from the request
    sort_by = request.args.get("sort_by", "date")  # Default sort by name
    order = request.args.get("order", "asc")  # Default order is ascending

    # Fetch all races
    races = race_service.get_all_races()

    # Sorting logic
    if sort_by == "name":
        races = sorted(races, key=lambda race: race.name.lower())  # Sort by name
    elif sort_by == "date":
        races = sorted(races, key=lambda race: race.date)  # Sort by date
    elif sort_by == "address":
        races = sorted(races, key=lambda race: race.address.streetname.lower())  # Sort by address

    # Apply the sorting order (ascending or descending)
    if order == "desc":
        races.reverse()  # Reverse the order for descending

    # Fetch all addresses for the "group by address" dropdown
    addresses = address_service.get_all_addresses()

    return render_template("races.html", section="races", textVars=textVars, races=races, form=form, user_race_service=user_race_service, addresses=addresses)

def teamsSection(textVars):
    teamScores = team_service.get_team_activity_counts()
    return render_template("teams.html", section="teams", textVars=textVars, teamScores=teamScores)

def runsSection(textVars):
    """Display all runs and handle creating, editing, and deleting a run."""
    form = RunForm()

    if request.method == "POST":
        if "delete_run_id" in request.form:
            # Handle run deletion
            run_id = request.form.get("delete_run_id")
            deleted_run = run_service.get_run_by_id(run_id)  # Fetch run before deleting
            if deleted_run:
                success = run_service.delete_run(run_id)
                if success:
                    flash(f"Run '{deleted_run.name}' deleted successfully!", "success")
                else:
                    flash("Error deleting run.", "danger")
            else:
                flash("Run not found.", "danger")
        else:
            # Handle run creation or update
            run_id = request.form.get("run_id")
            streetname = request.form.get("streetname")
            postalcode = request.form.get("postalcode")
            country = request.form.get("country")
            date = request.form.get("date")
            time = request.form.get("time")
            name = request.form.get("name")
            description = request.form.get("description")

            if run_id:
                try:
                    updated_run = run_service.update_run(run_id, streetname, postalcode, country, date, time, name, description)
                    flash(f"Run '{updated_run.name}' updated successfully!", "success")
                except Exception as e:
                    flash(f"Error updating run: {str(e)}", "danger")
            else:
                try:
                    new_run = run_service.create_run(streetname, postalcode, country, date, time, name, description)
                    flash(f"Run '{new_run.name}' created successfully!", "success")
                    user_run_service.create_run_and_add_creator(g.current_user.id, new_run.id)
                except Exception as e:
                    flash(f"Error creating run: {str(e)}", "danger")

        return redirect(url_for("content_section", section="runs"))

    

    # Get the sorting parameters from the request
    sort_by = request.args.get("sort_by", "date")  # Default sort by name
    order = request.args.get("order", "asc")  # Default order is ascending

    # Fetch all runs
    runs = run_service.get_all_runs()

    # Sorting logic
    if sort_by == "name":
        runs = sorted(runs, key=lambda run: run.name.lower())  # Sort by name
    elif sort_by == "date":
        runs = sorted(runs, key=lambda run: run.date)  # Sort by date
    elif sort_by == "address":
        runs = sorted(runs, key=lambda run: run.address.streetname.lower())  # Sort by address

    # Apply the sorting order (ascending or descending)
    if order == "desc":
        runs.reverse()  # Reverse the order for descending

    # Fetch all addresses for the "group by address" dropdown
    addresses = address_service.get_all_addresses()

    now = datetime.now()

    user_registered_run_ids = [ur.runid for ur in user_run_service.get_user_runs(g.current_user.id)]
    return render_template("runs.html", section="runs", textVars=textVars, runs=runs, form=form, user_run_service=user_run_service,run_service=run_service, addresses=addresses, user_registered_run_ids = user_registered_run_ids, now=now)

def runDetailSection(textVars, run_id):
    run = run_service.get_run_by_id(run_id)
    if not run:
        flash("Run not found.", "danger")
        return redirect(url_for("content_section", section="runs"))
    
    form = EmptyForm()
    
    if request.method == "POST" and form.validate_on_submit():
        if "sign_up" in request.form:
            if not g.current_user:
                flash("You need to log in first.", "warning")
                return redirect(url_for("content_section", section="login"))

            already_registered = user_run_service.get_user_run_by_run_id_and_user_id(run_id, g.current_user.id)
            if already_registered:
                flash("You're already signed up for this run.", "warning")
            else:
                user_run_service.register_user_to_run(g.current_user.id, run_id)
                flash("You've been signed up for the run!", "success")

        elif "sign_off" in request.form:
            user_run = user_run_service.get_user_run_by_run_id_and_user_id(run_id, g.current_user.id)
            if user_run and not user_run.iscreator:
                user_run_service.unregister_user_from_run(g.current_user.id, run_id)
                flash("You've been signed off from the run.", "info")
            else:
                flash("You can't sign off as the creator.", "danger")

        return redirect(url_for("content_section", section=f"runs/{run_id}"))

    user_runs = user_run_service.get_users_by_run_id(run_id)
    users = [user_service.get_user_by_id(user_run.userid) for user_run in user_runs]
    already_registered = any(u.id == g.current_user.id for u in users) if g.current_user else False

    return render_template("run_detail.html",section=f"runs/{run_id}",textVars=textVars,run=run,users=users,user_runs=user_runs,
        already_registered=already_registered,form=form)

def raceDetailSection(textVars, race_id):
    race = race_service.get_race_by_id(race_id)
    if not race:
        return "<h2>Race not found</h2>", 404
    
    user_races = user_race_service.get_users_by_race_id(race_id)
    users = [user_service.get_user_by_id(user_race.userid) for user_race in user_races]

    return render_template(
        "race_detail.html",
        section=f"races/{race_id}",
        textVars=textVars,
        race=race,
        users=users,
        user_races=user_races
    )

def sponsorsSection(textVars):
    form = SponsorForm()
    if form.validate_on_submit():
        try:
            password_service = PasswordService()
            password_id = password_service.add_password(form.password.data)
            sponsor_service.add_sponsor(
                name=form.name.data,
                email=form.email.data,
                passwordid=password_id
            )
            password_service.close()

            flash("Sponsor created successfully!", "success")
            return redirect(url_for("content_section", section="sponsors"))

        except Exception as e:

            flash(f"Chyba při vytváření sponzora: {str(e)}", "danger")

    sponsors = sponsor_service.get_all_sponsors()
    return render_template("sponsors.html", section="sponsors", textVars=textVars, form=form, sponsors=sponsors)



def get_current_user():
    user_token = session.get("user_token")
    if user_token:
        user = user_service.getUserInfo(user_token)
        if user is None:
            print("Invalid user ID in session, logging out.")
            session.pop("user_id", None)
        else:
            print(f"User {user.name} is admin: {user.isadmin}")  # Check if user info is being returned
            return user
    return None




if __name__ == "__main__":
    app.run(debug=True)