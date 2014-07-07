# PAGE DE GESTION DES UTILISATEURS : VISIBLE QUE PAR LE PRESIDENT
@auth.requires_membership('President')
def gestionUsers():
    
    # ROLE ET ENTITE DES UTILISATEURS MODIFIABLES
    userService.readonlyUser(True, True)
    
    # CREATION DU TABLEAU DES UTILISATEURS
    gridUser = SQLFORM.grid(db.auth_user, searchable=False, csv=False, ui="jquery-ui", links_in_grid=False, create=False, editable=True, onupdate=updateUser,user_signature=False, details=False )
    return dict(gridUsers=gridUser)

# méthode qui va s'executer apres chaque modification d'un user
def updateUser(form):
    # on met a jour le group_id du user dans la table auth_membership de web2py pour y renseigner l'id du role
    groupService.updateMembership(form.vars.id, form.vars.group_id)

# PAGE DE GESTION DES COMPOSANTES : VISIBLE QUE PAR LE PRESIDENT
@auth.requires_membership('President')
def gestionEntites():
    # CREATION DU TABLEAU DES COMPOSANTES
    gridEntites = SQLFORM.grid(db.entite, searchable=False, csv=False, ui="jquery-ui", links_in_grid=False, details=False, create=False, user_signature=False)
    return dict(gridEntites=gridEntites)

# PAGE D'AJOUT D'UN UTILISATEUR
@auth.requires_membership('President')
def addUser():

   # ROLE ET COMPOSANTE DES UTILISATEURS MODIFIABLE 
   userService.readonlyUser(True, True)

   # mot de passe non éditable car un mot de passe est envoyé aléatoirement par mail à l'utilisateur
   db.auth_user.password.readable = False
   db.auth_user.password.writable = False 
    
    # CREATION DU FORMULAIRE D'AJOUT D'UN UTILISATEUR
   form = SQLFORM(db.auth_user)
    
    # SI LE FORMULAIRE EST SOUMIS
   if form.process().accepted:

       # création d'un mot de passe aléatoire, mis a jour en base
       mdp = userService.initPassword(form.vars.id)

       response.flash = 'form accepted'

       # on ajoute une occurence dans la auth_membership de web2py : id du user + id du role
       groupService.inserMembership(form.vars.id, form.vars.group_id)
        
       #notification par mail
       mailService.sendMailNewUser(form.vars.first_name, form.vars.last_name, form.vars.email,mdp)
        
       # PUIS ON REDIRIGE VERS LA PAGE DE GESTION DES UTILISATEURS
       redirect(URL('gestionUsers'))
   # SI LE FORMULAIRE CONTIENT DES ERREURS
   elif form.errors:
       response.flash = 'form has errors'
   else:
       response.flash = 'please fill out the form'

   return locals()

# PAGE D'AJOUT D'UNE ENTITE
@auth.requires_membership('President')
def addEntite():

    # CREATION DU FORMULAIRE D'AJOUT D'UNE ENTITE
    form = SQLFORM(db.entite)

    # SI LE FORMULAIRE EST SOUMIS
    if form.process().accepted:
        # INSERTION EN BASE
       response.flash = 'form accepted'
        # PUIS ON REDIRIGE VERS LA PAGE DE GESTION DES ENTITES
       redirect(URL('gestionEntites'))
     # SI LE FORMULAIRE CONTIENT DES ERREURS
    elif form.errors:
       response.flash = 'form has errors'
    else:
       response.flash = 'please fill out the form'

    return locals()

# page de modification des informations du profile du user
@auth.requires_login()
def profile():

       # role et entité en lecture seule
       userService.readonlyUser(True,False)

       return dict(form=auth.profile())

# page de changement de mot de passe
@auth.requires_login()
def password():
       return dict(form=auth.change_password())
