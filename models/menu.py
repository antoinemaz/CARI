#
# COMPOSITION DU MENU DE NAVIGATION
response.menu = []

if auth.is_logged_in() == False:
    response.menu += [('Se connecter', URL()==URL('default', 'user/login'), URL('default', 'user/login'),[])]
    response.menu += [('Mot de passe oublié ?', URL()==URL('default', 'user/request_reset_password'), URL('default', 'user/request_reset_password'),[])]
else:
    response.menu += [('Liste des projets', URL()==URL('listeProjets', 'projets'), URL('listeProjets', 'projets'),[])]
    response.menu += [('Nouveau projet', URL()==URL('projet', 'addProjet'), URL('projet', 'addProjet'),[])]
    response.menu += [('Liste des budgets', URL()==URL('budget', 'gestionBudgets'), URL('budget', 'gestionBudgets'),[])]
    
    isPresident = session.auth.user.group_id == Constantes.PRESIDENT
    if isPresident == True:
        response.menu += [('Gestion des utilisateurs', URL()==URL('compte', 'gestionUsers'), URL('compte', 'gestionUsers'),[])]
        response.menu += [('Gestion des entités', URL()==URL('compte', 'gestionEntites'), URL('compte', 'gestionEntites'),[])]
   
    response.menu += [('Profil', URL()==URL('compte', 'profile'), URL('compte', 'profile'),[])]
    response.menu += [('Se déconnecter', URL()==URL('default', 'user/logout'), URL('default', 'user/logout'),[])]
