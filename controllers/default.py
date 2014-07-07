# entité et role du user en lecture seule
userService.readonlyUser(True,False)

# PAGE DE CONNEXION DES UTILISATEURS
def user():    
    return dict(form=auth())

# PAGE D'ACCUEIL LORSQUE L'UTILISATEUR S'EST IDENTIFIE
@auth.requires_login()
def index():
    # redirection vers la page listant les projets
    redirect(URL('listeProjets','projets'))
    return dict()
