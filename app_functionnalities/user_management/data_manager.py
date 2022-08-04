# Gestionnaire de données (musiques, utilisateurs, etc.)
from app_functionnalities.user_management.models import User
from App import database
import pafy
from youtube_dl.utils import DownloadError

class DataManager:

    def add_new_user(self, login, password, email):
        user = User()
        user.login = login
        user.email = email
        user.set_passwpord(password)
        database.session.add(user)
        database.session.commit()
