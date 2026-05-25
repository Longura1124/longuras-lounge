from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, RadioField, SubmitField
from wtforms.validators import DataRequired, equal_to, length


class RegisterForm(FlaskForm):
    username = StringField("Enter Username", validators=[
        DataRequired()
    ])
    password = PasswordField("Enter Password", validators=[
        DataRequired(),
        length(min=6, max=24),
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(),
        equal_to("password", message="პაროლები არ ემთხვევა")
    ])
    gender = RadioField(choices=["Male", "Female", "I'm a Mekanik"], validators=[
        DataRequired()
    ])

    register = SubmitField("Register")