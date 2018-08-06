import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' # TODO: A changer quand lancement en prod'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://username:password@server/db'  # TODO
    SQLALCHEMY_TRACK_MODIFICATIONS = False