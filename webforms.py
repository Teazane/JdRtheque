from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    login = StringField('Pseudo', validators=[DataRequired(message="Ce champ est obligatoire.")])
    password = PasswordField('Mot de passe', validators=[DataRequired(message="Ce champ est obligatoire.")])
    submit = SubmitField('Connexion')


class RegisterForm(FlaskForm):
    login = StringField('Pseudo', validators=[DataRequired(message="Ce champ est obligatoire.")])
    password = PasswordField('Mot de passe', validators=[DataRequired(message="Ce champ est obligatoire.")])
    password_confirmation = PasswordField('Confirmation du mot de passe', validators=[DataRequired(message="Ce champ est obligatoire."), EqualTo('password', message="Les deux mots de passe ne sont pas identiques.")])
    email = StringField('Adresse mail', validators=[DataRequired(message="Ce champ est obligatoire."), Email(message="Format de l'adresse mail incorrect.")])
    submit = SubmitField('Connexion')
