from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, ValidationError, URL
from app_functionnalities.music_management.models import Scene, Style


class AddMusicForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired(message="Ce champ est obligatoire.")])
    source = StringField('URL source', validators=[DataRequired(message="Ce champ est obligatoire."), URL(message="URL invalide.")])
    loop = BooleanField('Bouclable ?')
    genre = SelectField('Genre musical', coerce=int)
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
    genre = SelectField('Genre musical', coerce=int)
    style_tags = SelectMultipleField('Style(s)', coerce=int) #coerce=int permet de forcer les données (voir http://wtforms.simplecodes.com/docs/0.6/fields.html)
    scene_tags = SelectMultipleField('Scène(s)', coerce=int)
    submit = SubmitField('Rechercher')
