from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, URL, NumberRange
from models import User, Scene, Style


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

    # Validators de la forme "validate_<champ>" pour être pris en compte
    def validate_login(self, username):
        user = User.query.filter_by(login=username.data).first()
        if user is not None:
            raise ValidationError('Cet identifiant est déjà utilisé par un autre compte.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Cette adresse mail est déjà utilisée par un autre compte.')


class AddMusicForm(FlaskForm):
    style_list = []
    scene_list = []
    for style in Style.query.order_by(Style.name).all():
        style_list.append((style.id, style.name))
    for scene in Scene.query.order_by(Scene.name).all():
        scene_list.append((scene.id, scene.name))

    title = StringField('Titre', validators=[DataRequired(message="Ce champ est obligatoire.")])
    source = StringField('URL source', validators=[DataRequired(message="Ce champ est obligatoire."), URL(message="URL invalide.")])
    duration = IntegerField('Durée (en secondes)', validators=[DataRequired(message="Ce champ est obligatoire."), NumberRange(min=1, message="Durée invalide.")])
    loop = BooleanField('Bouclable ?', validators=[DataRequired(message="Ce champ est obligatoire.")])
    style_tags = SelectField('Style(s)', choices=style_list)
    scene_tags = SelectField('Scene(s)', choices=scene_list)
    submit = SubmitField('Connexion')
