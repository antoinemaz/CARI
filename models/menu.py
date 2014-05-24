#
# COMPOSITION DU MENU DE NAVIGATION
response.menu = []

if auth.is_logged_in() == False:
    response.menu += [('Se connecter', URL()==URL('default', 'user/login'), URL('default', 'user/login'),[])]
    response.menu += [('Mot de passe oublié ?', URL()==URL('default', 'user/reset_password'), URL('default', 'user/reset_password'),[])]

response.menu += [('Liste des projet', URL()==URL('default', 'index'), URL('default', 'index'),[])]
response.menu += [('Nouveau projet', URL()==URL('projet', 'addProjet'), URL('projet', 'addProjet'),[])]
response.menu += [('Gestion des utilisateurs', URL()==URL('compte', 'gestionUsers'), URL('compte', 'gestionUsers'),[])]
response.menu += [('Gestion des entités', URL()==URL('compte', 'gestionEntites'), URL('compte', 'gestionEntites'),[])]
response.menu += [('Gestion des budgets', URL()==URL('budget', 'gestionBudgets'), URL('budget', 'gestionBudgets'),[])]
response.menu += [('Profil', URL()==URL('default', 'user/profile'), URL('default', 'user/profile'),[])]
