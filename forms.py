from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo
import json
from flask import session

with open("textVars.json", "r", encoding="utf-8") as file:
    translations = json.load(file)

def get_translation(page, key, lang):
    """Fetch translation from JSON file."""
    return translations.get("pages", {}).get(page, {}).get(lang, {}).get(key, key)

class LoginForm(FlaskForm):
    """Login Form with dynamic language support"""

    def __init__(self, lang="en", *args, **kwargs):
        super().__init__(*args, **kwargs)  # Initialize the FlaskForm first

        # Dynamically set labels based on selected language
        self.email.label.text = get_translation("login", "email", lang)
        self.password.label.text = get_translation("login", "password", lang)
        self.submit.label.text = get_translation("login", "submit", lang)

    email = StringField("Email", validators=[DataRequired(), Length(max=60)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    """Registration Form"""
    def __init__(self, lang="en", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name.label.text = get_translation("register", "name", lang)
        self.surname.label.text = get_translation("register", "surname", lang)
        self.email.label.text = get_translation("register", "email", lang)
        self.password.label.text = get_translation("register", "password", lang)
        self.confirmPassword.label.text = get_translation("register", "confirmPassword", lang)
        self.gender.label.text = get_translation("register", "gender", lang)
        self.telephone.label.text = get_translation("register", "telephone", lang)
        self.telephoneCode.label.text = get_translation("register", "telephoneCode", lang)
        self.postalcode.label.text = get_translation("register", "postalcode", lang)
        self.country.label.text = get_translation("register", "country", lang)
        self.streetname.label.text = get_translation("register", "streetname", lang)
        self.submit.label.text = get_translation("register", "submit", lang)
        male_label = get_translation("myProfile", "male", lang)
        female_label = get_translation("myProfile", "female", lang)
        other_label = get_translation("myProfile", "other", lang)
        self.gender.choices = [('M', male_label), ('F', female_label), ('O', other_label)]

    
    name = StringField(validators=[DataRequired()])
    surname = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    confirmPassword = PasswordField(validators=[DataRequired(), EqualTo('password')])
    gender = RadioField(validators=[DataRequired()])
    telephone = StringField(validators=[DataRequired()])
    telephoneCode = StringField(validators=[DataRequired()])
    postalcode = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    streetname = StringField(validators=[DataRequired()])

    submit = SubmitField()


class VerificationForm(FlaskForm):
    """Verification Form (6-digit code)"""
    code = StringField(
        "Verification Code",
        validators=[
            DataRequired(message="This field is required."),
            Length(min=6, max=6, message="The code must be 6 digits.")
        ]
    )
    submit = SubmitField("Verify")


class EditProfileForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    telephone = StringField("Telephone", validators=[DataRequired()])
    gender = StringField("Gender", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    streetname = StringField("Street Name", validators=[DataRequired()])
    postalcode = StringField("Postal Code", validators=[DataRequired()])
    submit = SubmitField("Save Changes")

class RunForm(FlaskForm):
    """Form for creating and editing runs."""
    name = StringField("Run Name", validators=[DataRequired()])
    date = DateField("Date", format='%Y-%m-%d', validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    address_id = StringField("Address ID", validators=[DataRequired()])
    submit = SubmitField("Save")