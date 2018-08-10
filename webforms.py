from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    login = StringField('Pseudo', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Connexion')


class RegisterForm(FlaskForm):
    login = StringField('Pseudo', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), EqualTo('password_confirmation')])
    password_confirmation = PasswordField('Confirmation du mot de passe', validators=[DataRequired()])
    email = StringField('Adresse mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Connexion')
