# coding: utf8
def gestionBudgets():
    return locals()

def addBudget():

    # CREATION DU FORMULAIRE D'AJOUT D'UNE COMPOSANTE
    form = SQLFORM(db.budget)

    # SI LE FORMULAIRE EST SOUMIS
    if form.process().accepted:
        # INSERTION EN BASE
       response.flash = 'form accepted'
        # PUIS ON REDIRIGE VERS LA PAGE DE GESTION DES COMPOSANTES
       redirect(URL('gestionBudgets'))
     # SI LE FORMULAIRE CONTIENT DES ERREURS
    elif form.errors:
        # ON VA LES AFFICHER
       response.flash = 'form has errors'
    else:
        # FORMULAIRE VIDE
       response.flash = 'please fill out the form'
    return locals()
