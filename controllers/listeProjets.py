# coding: utf8

# page listant les projets
@auth.requires_login()
def projets():
    
    # tableau contenant tous les projets
    # attention : la requete (premier argument de la méthode grid, contient la requete qui va lister tous les projets, EN FONCTION DU ROLE
    # DU USER CONNECTE : demandeur --> tous les dossiers qu'il a créé, représentant --> tous les dossiers de son entité, président --> tous
    # les dossiers
    gridProjets = SQLFORM.grid(projetService.getQueryOfDossier(session), fields=[db.dossier.id, db.dossier.intitule, db.dossier.porteur_id, db.dossier.etat_dossier_id, db.dossier.entite_id, db.dossier.date_dossier], orderby=[~db.dossier.date_dossier], searchable=False, csv=False, ui="jquery-ui",user_signature=False, links_in_grid=True, details=False, create=False, deletable=False, editable=False, links=[lambda row:A("Détail", _href=URL("projet", "addProjet", vars=dict(idDossier=row.id)))])
    
    return locals()

# page intégrée à la page listant les projets : recherche de dossier par son id
@auth.requires_login()
def rechercheDossier():
    
        recherche = False
        idDossier = None
        rowTrouve = False
        intOk = True
         
        # création d'un forumulaire de recherche d'un dossier par son id
        formRecherche = FORM(DIV('Numéro de dossier : ',_class="center"), INPUT(_name='numDossier',_class="text"), BR(),INPUT(_type='submit', _value="Rechercher"),_class="center", _id="formRecherche")
        
         # si une rechercher a été faite
        if formRecherche.accepts(request,session):
               
               recherche = True
               
               response.flash = 'form accepted'
                
               # récupération de l'id du dossier tapé dans le champ de recherche
               try: 
                   idDossier = int(formRecherche.vars.numDossier)
               except ValueError:
                    # parsing impossible en int : le user n'a pas tapé de chiffre dans le champ !
                    intOk = False
                
               # l'id du dossier n'est pas null et c'est un integer
               if formRecherche.vars.numDossier != None and intOk ==True:
                  
                  # on récupère le dossier par son id
                  row = projetService.getDossierById(formRecherche.vars.numDossier)
                    
                  # s'il a été trouvé (il existe bien), rowTrouve va fait apparaitre un message dans la vue pour dire qu'un dossier
                  #a bien été trouvé, accompagné de l'url de détail vers ce dossier
                  if row != None:
                     rowTrouve = True

        elif formRecherche.errors:
           response.flash = 'form has errors'
        else:
           response.flash = 'please fill out the form'
    
        return locals()
