from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectMultipleField
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


class AddMusicForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired(message="Ce champ est obligatoire.")])
    source = StringField('URL source', validators=[DataRequired(message="Ce champ est obligatoire."), URL(message="URL invalide.")])
    duration = IntegerField('Durée (en secondes)', validators=[DataRequired(message="Ce champ est obligatoire."), NumberRange(min=1, message="Durée invalide.")])
    loop = BooleanField('Bouclable ?')
    style_tags = SelectMultipleField('Style(s)', coerce=int) #coerce=int permet de forcer les données (voir http://wtforms.simplecodes.com/docs/0.6/fields.html)
    scene_tags = SelectMultipleField('Scène(s)', coerce=int)
    submit = SubmitField('Ajouter')


class AddStyleForm(FlaskForm):
    existing_list = []
    for style in Style.query.order_by(Style.name).all():
        existing_list.append((style.id, style.name))

    name = StringField('Nom du style', validators=[DataRequired(message="Ce champ est obligatoire.")])
    submit = SubmitField('Ajouter')

    def validate_name(self, scene):
        scene = Style.query.filter_by(name=scene.data).first()
        if scene is not None:
            raise ValidationError('Ce style existe déjà.')


class AddSceneForm(FlaskForm):
    existing_list = []
    for scene in Scene.query.order_by(Scene.name).all():
        existing_list.append((scene.id, scene.name))

    name = StringField('Nom de la scene', validators=[DataRequired(message="Ce champ est obligatoire.")])
    submit = SubmitField('Ajouter')

    def validate_name(self, scene):
        scene = Scene.query.filter_by(name=scene.data).first()
        if scene is not None:
            raise ValidationError('Ce type de scène existe déjà.')


class SearchMusicForm(FlaskForm):
    title = StringField('Titre')
    loop = BooleanField('Bouclable ?')
    style_tags = SelectMultipleField('Style(s)', coerce=int) #coerce=int permet de forcer les données (voir http://wtforms.simplecodes.com/docs/0.6/fields.html)
    scene_tags = SelectMultipleField('Scène(s)', coerce=int)
    submit = SubmitField('Rechercher')
