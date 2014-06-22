# coding: utf8
@auth.requires_login()
def projets():
    
    db.dossier.etat_dossier_id.readable=True
    db.dossier.entite_id.readable=True

    gridProjets = SQLFORM.grid(projetService.getQueryOfDossier(session), fields=[db.dossier.id, db.dossier.intitule, db.dossier.porteur_id, db.dossier.etat_dossier_id, db.dossier.entite_id, db.dossier.date_dossier], orderby=[~db.dossier.date_dossier], searchable=False, csv=False, ui="jquery-ui",user_signature=False, links_in_grid=True, details=False, create=False, deletable=False, editable=False, links=[lambda row:A("Détail", _href=URL("projet", "addProjet", vars=dict(idDossier=row.id)))])
    
    return locals()

@auth.requires_login()
def rechercheDossier():
    
        recherche = False
        idDossier = None
        rowTrouve = False
        intOk = True
            
        formRecherche = FORM(DIV('Numéro de dossier : ',_class="center"), INPUT(_name='numDossier',_class="text"), BR(),INPUT(_type='submit', _value="Rechercher"),_class="center", _id="formRecherche")
        
                # SI LE FORMULAIRE GESTION EST SOUMIS
        if formRecherche.accepts(request,session):
               
               recherche = True
               
               # INSERTION EN BASE
               response.flash = 'form accepted'

               try: 
                   idDossier = int(formRecherche.vars.numDossier)
               except ValueError:
                    intOk = False
                    
               if formRecherche.vars.numDossier != None and intOk ==True:
                  
                  row = projetService.getDossierById(formRecherche.vars.numDossier)
                  if row != None:
                     rowTrouve = True

               #redirect(URL('projets',vars=dict(idDossier=formRecherche.vars.numDossier)))
         # SI LE FORMULAIRE CONTIENT DES ERREURS
        elif formRecherche.errors:
            # ON VA LES AFFICHER
           response.flash = 'form has errors'
        else:
            # FORMULAIRE VIDE
           response.flash = 'please fill out the form'
    
        return locals()
