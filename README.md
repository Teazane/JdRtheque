# JdRtheque
La JdRthèque est un site web de partage de ressources consacrées au jeu de rôles (musiques, images, etc.).
Il est codé en Python, optimisé pour la version 3.6 et utilise le framework Flask.
Le projet a été codé sous Windows, la plupart des commandes conseillées sont donc adaptées à PowerShell ou Cmd mais sont largement adaptables à un environnement Linux.

## Initialiser le projet
1. Installer Python (préférentiellement la version 3.6)
1. (optionnel) Installer virtualenv avec la commande : `pip install virtualenv`
1. (optionnel) Créer l'environnement virtuel : `virtualenv ENV`
1. (optionnel) Activer l'environnement virtuel : `.\ENV\Scripts\activate`
1. Installer les dépendances du projet : `pip install -r requirements.txt`
1. Initialiser la variable FLASK_APP (sous Cmd : `set FLASK_APP=App.py`, sous PS : `$env:FLASK_APP="App.py"`, sous Linux : `export FLASK_APP=App.py`)

Il ne reste plus qu'à lancer le projet avec `flask run`.

### Problèmes connus

#### Mysqlclient
Sous Windows 7, il est courant que la dépendance "mysqlclient" ne s'installe pas correctement. 
Windows réclame un fichier Microsoft Visual C++ que vous possédez sans doute déjà.
L'installer ne changera rien, c'est un bug connu qui peut se résoudre en allant installer directement la bibliothèque Python manquante.
Allez sur https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient télécharger la version appropriée de "mysqlclient" et le monter avec la commande `pip install mysqlclient‑1.3.13‑cp36‑cp36m‑win_amd64.whl` (en imaginant que vous possédez un Windows en 64 bits et que vous utilisez la version 3.6 de Python).
Solution trouvée via StackOverflow sur cette question : https://stackoverflow.com/questions/29846087/microsoft-visual-c-14-0-is-required-unable-to-find-vcvarsall-bat/47935574#47935574

