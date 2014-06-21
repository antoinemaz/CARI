userService.readonlyUser(True,False)

# PAGE D'ACCUEIL LORSQUE L'UTILISATEUR S'EST IDENTIFIE
@auth.requires_login()
def index():
    return dict()

# PAGE DE CONNEXION DES UTILISATEURS
def user():    
    return dict(form=auth())
