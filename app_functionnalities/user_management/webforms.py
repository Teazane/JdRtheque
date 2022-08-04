from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app_functionnalities.user_management.models import User


class LoginForm(FlaskForm):
    login = StringField('Pseudo', validators=[DataRequired(message="Ce champ est obligatoire.")])
    password = PasswordField('Mot de passe', validators=[DataRequired(message="Ce champ est obligatoire.")])
    submit = SubmitField('Connexion')


class RegisterForm(FlaskForm):
    login = StringField('Pseudo', validators=[DataRequired(message="Ce champ est obligatoire.")])
    password = PasswordField('Mot de passe', validators=[DataRequired(message="Ce champ est obligatoire.")])
    password_confirmation = PasswordField('Confirmation du mot de passe', validators=[DataRequired(message="Ce champ est obligatoire."), EqualTo('password', message="Les deux mots de passe ne sont pas identiques.")])
    email = StringField('Adresse mail', validators=[DataRequired(message="Ce champ est obligatoire."), Email(message="Format de l'adresse mail incorrect.")])
    submit = SubmitField('Inscription')

    # Validators de la forme "validate_<champ>" pour être pris en compte
    def validate_login(self, username):
        user = User.query.filter_by(login=username.data).first()
        if user is not None:
            raise ValidationError('Cet identifiant est déjà utilisé par un autre compte.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Cette adresse mail est déjà utilisée par un autre compte.')