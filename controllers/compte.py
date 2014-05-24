# PAGE DE GESTION DES UTILISATEURS : VISIBLE QUE PAR LE PRESIDENT
@auth.requires_membership('President')
def gestionUsers():
    # ROLE ET COMPOSANTE DES UTILISATEURS MODIFIABLE : METHODE DEFINIT dans db.py
    userService.readonlyUser(True, True)
    # CREATION DU TABLEAU DES UTILISATEURS
    gridUser = SQLFORM.grid(db.auth_user, searchable=False, csv=False, ui="jquery-ui", links_in_grid=False, create=False, editable=True, onupdate=updateUser )
    return dict(gridUsers=gridUser)


def updateUser(form):
    groupService.updateMembership(form.vars.id, form.vars.group_id)

# PAGE DE GESTION DES COMPOSANTES : VISIBLE QUE PAR LE PRESIDENT
@auth.requires_membership('President')
def gestionEntites():
    # CREATION DU TABLEAU DES COMPOSANTES
    gridEntites = SQLFORM.grid(db.entite, searchable=False, csv=False, ui="jquery-ui", links_in_grid=False, details=False, create=False)
    return dict(gridEntites=gridEntites)

# PAGE D'AJOUT D'UN UTILISATEUR
@auth.requires_membership('President')
def addUser():

   # ROLE ET COMPOSANTE DES UTILISATEURS MODIFIABLE : METHODE DEFINIT dans db.py
   userService.readonlyUser(True, True)

    # CREATION DU FORMULAIRE D'AJOUT D'UN UTILISATEUR
   form = SQLFORM(db.auth_user)

    # SI LE FORMULAIRE EST SOUMIS
   if form.process().accepted:
        # INSERTION EN BASE
       response.flash = 'form accepted'

       groupService.inserMembership(form.vars.id, form.vars.group_id)
        
       # PUIS ON REDIRIGE VERS LA PAGE DE GESTION DES UTILISATEURS
       redirect(URL('gestionUsers'))
   # SI LE FORMULAIRE CONTIENT DES ERREURS
   elif form.errors:
       # ON VA LES AFFICHER
       response.flash = 'form has errors'
   else:
       # FORMULAIRE VIDE
       response.flash = 'please fill out the form'

   return locals()

# PAGE D'AJOUT D'UNE COMPOSANTE
@auth.requires_membership('President')
def addEntite():

    # CREATION DU FORMULAIRE D'AJOUT D'UNE COMPOSANTE
    form = SQLFORM(db.entite)

    # SI LE FORMULAIRE EST SOUMIS
    if form.process().accepted:
        # INSERTION EN BASE
       response.flash = 'form accepted'
        # PUIS ON REDIRIGE VERS LA PAGE DE GESTION DES COMPOSANTES
       redirect(URL('gestionEntites'))
     # SI LE FORMULAIRE CONTIENT DES ERREURS
    elif form.errors:
        # ON VA LES AFFICHER
       response.flash = 'form has errors'
    else:
        # FORMULAIRE VIDE
       response.flash = 'please fill out the form'

    return locals()
