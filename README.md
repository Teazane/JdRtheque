# JdRtheque
La JdRthèque est un site web de partage de ressources consacrées au jeu de rôles (musiques, scénarii, etc.).
Il est codé en Python, optimisé pour la version 3.9 et utilise le framework Django.
Le projet a été codé sous Windows, la plupart des commandes conseillées sont donc adaptées à PowerShell ou Cmd mais sont largement adaptables à un environnement Linux.

## Sommaire
1. [Objectifs du projet](#objectifs-du-projet)
1. [Prérequis](#prérequis)
1. [Initialiser le projet](#initialiser-le-projet)
1. [Problèmes connus](#problèmes-connus)

## Objectifs du projet
L'objectif de ce projet est de proposer une plate-forme moderne et accessible sur le web, mettant à disposition des ressources utiles à la pratique du jeu de rôle.
Il s'agira dans un premier temps d'une plate-forme de recherche de musiques en fonction de l'ambiance souhaitée.
Par la suite, d'autres ressources pourront être partagées (scénarii, fiches personnages, ...).

### Recherche de musiques
La recherche de musique pourra se faire via différents critères (ambiance recherchée, musique bouclable ou non, durée, ...).
L'utilisateur pourra constituer des playlists dans lesquelles il pourra sauvegarder une liste de musiques de son choix.
Il sera possible d'ajouter des styles de jeux de rôles et des styles de scènes. 

### Gestion utilisateur
L'utilisateur pourra modifier les informations de son profil ou supprimer son profil.

### Partage de scénarii
[TODO]

### Partage d'autres ressources
[TODO]

## Prérequis
- Une version de [Python 3](https://www.python.org/downloads/) installée (préférentiellement 3.9).
- Une version de [Git](https://git-scm.com/downloads) installée.

Les autres dépendances sont listées dans "pyproject.toml", le fichier utilisé par Poetry pour gérer les bibliothèques.

## Initialiser le projet
1. Télécharger les fichiers sources avec `git clone https://github.com/Teazane/JdRtheque.git`
1. Installer Poetry avec la commande : `pip install poetry`
1. Créer l'environnement virtuel et installer les dépendences : `poetry install`

Il ne reste plus qu'à lancer le projet avec `poetry run python jdrtheque/manage.py runserver localhost:<chosen-port>`.

## Problèmes connus

### Mysqlclient
[TODO - Revoir cette partie avec Poetry]

Sous Windows 7, il est courant que la dépendance "mysqlclient" ne s'installe pas correctement. 
Windows réclame un fichier Microsoft Visual C++ que vous possédez sans doute déjà.
L'installer ne changera rien, c'est un bug connu qui peut se résoudre en allant installer directement la bibliothèque Python manquante.
Allez sur https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient télécharger la version appropriée de "mysqlclient" et le monter avec la commande `pip install mysqlclient‑1.3.13‑cp36‑cp36m‑win_amd64.whl` (en imaginant que vous possédez un Windows en 64 bits et que vous utilisez la version 3.6 de Python).
Solution trouvée via StackOverflow sur cette question : https://stackoverflow.com/questions/29846087/microsoft-visual-c-14-0-is-required-unable-to-find-vcvarsall-bat/47935574#47935574

### Pafy (dislike count)
Quand on ajoute une musique :
```
[2022-08-04 11:36:20,855] ERROR in app: Exception on /ajouter_musique [POST]
Traceback (most recent call last):
  [...]
  File "D:\Programs\Python39\lib\site-packages\pafy\pafy.py", line 124, in new
    return Pafy(url, basic, gdata, size, callback, ydl_opts=ydl_opts)
  File "D:\Programs\Python39\lib\site-packages\pafy\backend_youtube_dl.py", line 31, in __init__
    super(YtdlPafy, self).__init__(*args, **kwargs)
  File "D:\Programs\Python39\lib\site-packages\pafy\backend_shared.py", line 97, in __init__
    self._fetch_basic()
  File "D:\Programs\Python39\lib\site-packages\pafy\backend_youtube_dl.py", line 54, in _fetch_basic
    self._dislikes = self._ydl_info['dislike_count']
KeyError: 'dislike_count'
```
L'erreur vient du fait que Youtube a retiré la fonction consistant à compter les "je n'aime pas" et que la bibliothèque Pafy n'a pour l'instant pas suivi cette évolution.
Pour résoudre le problème, j'ai donc changé la ligne 54 du fichier de la bibliothèque à la main :
```
- self._dislikes = self._ydl_info['dislike_count']
+ self._dislikes = 0 # self._ydl_info['dislike_count']
```

### Youtube-dl (argument 5: <class 'TypeError'>: expected LP_OVERLAPPED2 instance instead of pointer to OVERLAPPED3)
```
[23/Aug/2022 17:37:19] "POST /admin/resources/scenario/add/ HTTP/1.1" 500 205738
Traceback (most recent call last):
  [...]
  File "D:\Programs\Python39\lib\site-packages\django\db\models\fields\files.py", line 316, in pre_save
    file.save(file.name, file.file, save=False)
  File "D:\Programs\Python39\lib\site-packages\django\db\models\fields\files.py", line 92, in save
    self.name = self.storage.save(name, content, max_length=self.field.max_length)
  File "D:\Programs\Python39\lib\site-packages\django\core\files\storage.py", line 56, in save
    name = self._save(name, content)
  File "D:\Programs\Python39\lib\site-packages\django\core\files\storage.py", line 309, in _save
    file_move_safe(content.temporary_file_path(), full_path)
  File "D:\Programs\Python39\lib\site-packages\django\core\files\move.py", line 80, in file_move_safe
    locks.unlock(fd)
  File "D:\Programs\Python39\lib\site-packages\django\core\files\locks.py", line 92, in unlock
    ret = UnlockFileEx(hfile, 0, 0, 0xFFFF0000, byref(overlapped))
ctypes.ArgumentError: argument 5: <class 'TypeError'>: expected LP_OVERLAPPED instance instead of pointer to OVERLAPPED
```
Causée par Youtube-dl qui s'entrechoque avec des méthodes Django (Oo') : https://stackoverflow.com/questions/50337960/django-1-11-7-django-compressor-argument-5-class-typeerror-expected-lp
Pour le résoudre, on vire Youtube-dl mais cela cause l'erreur suivante : 
```
ImportError: pafy: youtube-dl not found; you can use the internal backend by setting the environmental variable PAFY_BACKEND to "internal". It is not enabled by default because it is not as well maintained as the youtube-dl backend.
```
Pour la surmonter, suivre l'instruction :
```
D:\Code\JdRtheque\jdrtheque>set PAFY_BACKEND=internal
```
