# coding: utf8
def gestionProduits():
    
    detailsProjetView = False
    gestionProduitsView = True
    gestionPJsView = False
    finalDemandeView = False
    
    idDossier = request.vars.idDossier;
    
    if idDossier is not None:
        
          gestionProduits = True
        
          rowDossier = projetService.getDossierById(idDossier)
          rowPorteur = porteurService.getPorteurById(rowDossier.porteur_id)
    
          isRepresentant = groupService.isRepresentantOfDossier(session, rowPorteur.entite_id)
          isPresident = session.auth.user.group_id == Constantes.PRESIDENT
          isDemandeur = rowDossier.user_id == session.auth.user.id
        
          if isDemandeur == False and  isRepresentant == False and isPresident == False:
              redirect(URL('default','index'))
                
          if isDemandeur and (not isPresident and not isRepresentant) and rowDossier.etat_dossier_id != Constantes.BROUILLON:
                  gestionProduits = False
            
          if rowDossier.etat_dossier_id is None or rowDossier.etat_dossier_id == Constantes.BROUILLON:
                initDossier = True
          else:
                initDossier = False
        
    prixTot = achatService.calculerPrixTotal(idDossier)
    
    gridProduits = SQLFORM.grid(achatService.getAchatsByDossierId(idDossier), searchable=False, csv=False, ui="jquery-ui", links_in_grid=False, details=False, create=False, editable=gestionProduits, deletable=gestionProduits)
    
    return locals()

@auth.requires_login()
def addProduits():

    detailsProjetView = False
    gestionProduitsView = True
    gestionPJsView = False
    finalDemandeView = False
    
    idDossier = request.vars.idDossier;
    
    if idDossier is not None:
              
          rowDossier = projetService.getDossierById(idDossier)
          rowPorteur = porteurService.getPorteurById(rowDossier.porteur_id)
    
          isRepresentant = groupService.isRepresentantOfDossier(session, rowPorteur.entite_id)
          isPresident = session.auth.user.group_id == Constantes.PRESIDENT
          isDemandeur = rowDossier.user_id == session.auth.user.id
        
          if isDemandeur == False and  isRepresentant == False and isPresident == False:
              redirect(URL('default','index'))
                
          if isDemandeur and (not isPresident and not isRepresentant) and rowDossier.etat_dossier_id != Constantes.BROUILLON:
              redirect(URL('default','index'))
    
     # CREATION DU FORMULAIRE D'AJOUT D'UNE COMPOSANTE
    form = SQLFORM(db.achat)
    
    # ON SPECIFIE L'ID DU DOSSIER AU PROJET
    form.vars.dossier_id = request.vars.idDossier
       
    # SI LE FORMULAIRE EST SOUMIS
    if form.process().accepted:
     
        if rowDossier.etat_dossier_id == Constantes.ACCEPTE:
            achatService.updateBudgetOfProduitsDuDossier(rowDossier.id)
        
        # INSERTION EN BASE
        response.flash = 'form accepted'
        # PUIS ON REDIRIGE VERS LA PAGE DE GESTION DES COMPOSANTES
        redirect(URL('gestionProduits',vars=dict(idDossier=request.vars.idDossier)))
     # SI LE FORMULAIRE CONTIENT DES ERREURS
    elif form.errors:
        # ON VA LES AFFICHER
       response.flash = 'form has errors'
    else:
        # FORMULAIRE VIDE
       response.flash = 'please fill out the form'

    return locals()
