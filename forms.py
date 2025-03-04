from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    """Login Form"""
    email = StringField("Email", validators=[DataRequired(), Length(max=60)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    """Registration Form"""
    name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=50)])
    surname = StringField("Surname", validators=[DataRequired(), Length(min=2, max=50)])
    streetname = StringField("Street Name", validators=[DataRequired(), Length(min=3, max=100)])
    postalcode = IntegerField("Postal Code", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    telephoneCode = IntegerField("Telephone Code", validators=[DataRequired()])
    telephone = StringField("Telephone", validators=[DataRequired(), Length(min=7, max=15)])
    
    gender = RadioField("Gender", choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[DataRequired()])
    
    submit = SubmitField("Register")

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
