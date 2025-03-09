from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    """Login Form"""
    email = StringField("Email", validators=[DataRequired(), Length(max=60)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    """Registration Form"""
    name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=50)])
    surname = StringField("Surname", validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=5, max=30)])
    confirmPassword = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    streetname = StringField("Street Name", validators=[DataRequired(), Length(min=3, max=100)])
    postalcode = IntegerField("Postal Code", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()],render_kw={"placeholder": "example@gmail.com"})
    telephoneCode = IntegerField("Telephone Code", validators=[DataRequired()], render_kw={"placeholder": "+123"})
    telephone = StringField("Telephone", validators=[DataRequired(), Length(min=7, max=15)], render_kw={"placeholder": "123456789"})
    gender = RadioField("Gender", choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], validators=[DataRequired()])
    
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
