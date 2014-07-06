#
# COMPOSITION DU MENU DE NAVIGATION
response.menu = []

# menu d'un visiteur
if auth.is_logged_in() == False:
    response.menu += [('Se connecter', URL()==URL('default', 'user/login'), URL('default', 'user/login'),[])]
    response.menu += [('Mot de passe oublié ?', URL()==URL('default', 'user/request_reset_password'), URL('default', 'user/request_reset_password'),[])]
    
# menu d'un user connecté
else:
    response.menu += [('Liste des projets', URL()==URL('listeProjets', 'projets'), URL('listeProjets', 'projets'),[])]
    response.menu += [('Nouveau projet', URL()==URL('projet', 'addProjet'), URL('projet', 'addProjet'),[])]
    response.menu += [('Liste des budgets', URL()==URL('budget', 'gestionBudgets'), URL('budget', 'gestionBudgets'),[])]
    
    # liens dans le menu en plus si c'est le président qui est connecté
    isPresident = session.auth.user.group_id == Constantes.PRESIDENT
    if isPresident == True:
        response.menu += [('Gestion des utilisateurs', URL()==URL('compte', 'gestionUsers'), URL('compte', 'gestionUsers'),[])]
        response.menu += [('Gestion des entités', URL()==URL('compte', 'gestionEntites'), URL('compte', 'gestionEntites'),[])]
   
    # commun a tout le monde
    response.menu += [('Profil', URL()==URL('compte', 'profile'), URL('compte', 'profile'),[])]
    response.menu += [('Se déconnecter', URL()==URL('default', 'user/logout'), URL('default', 'user/logout'),[])]
