# coding: utf8
@auth.requires_login()
def gestionPjs():
    
    detailsProjetView = False
    gestionProduitsView = False
    gestionPJsView = True
    finalDemandeView = False
    
    idDossier = request.vars.idDossier;
    
    if idDossier is not None:
        
          gestionPJs = True
        
          rowDossier = projetService.getDossierById(idDossier)

          if rowDossier is None:
                redirect(URL('default','index'))
            
          rowPorteur = porteurService.getPorteurById(rowDossier.porteur_id)
    
          isRepresentant = groupService.isRepresentantOfDossier(session, rowDossier.entite_id)
          isPresident = session.auth.user.group_id == Constantes.PRESIDENT
          isDemandeur = rowDossier.user_id == session.auth.user.id
        
          if isDemandeur == False and  isRepresentant == False and isPresident == False:
              redirect(URL('default','index'))
                
          if isDemandeur and (not isPresident and not isRepresentant) and rowDossier.etat_dossier_id != Constantes.BROUILLON:
                  gestionPJs = False
            
          if rowDossier.etat_dossier_id is None or rowDossier.etat_dossier_id == Constantes.BROUILLON:
                initDossier = True
          else:
                initDossier = False
    
    userService.readonlyUser(True,False)
    
    gridPJ = SQLFORM.grid(documentService.getDocumentsByDossierId(idDossier), searchable=False, csv=False, ui="jquery-ui", details=False, create=False,editable=False, deletable=gestionPJs)

    return locals()


@auth.requires_login()
def addPJs():
    
    detailsProjetView = False
    gestionProduitsView = False
    gestionPJsView = True
    finalDemandeView = False
    
    idDossier = request.vars.idDossier;
    
    if idDossier is not None:
              
          rowDossier = projetService.getDossierById(idDossier)
            
          if rowDossier is None:
               redirect(URL('default','index'))
            
          rowPorteur = porteurService.getPorteurById(rowDossier.porteur_id)
    
          isRepresentant = groupService.isRepresentantOfDossier(session, rowDossier.entite_id)
          isPresident = session.auth.user.group_id == Constantes.PRESIDENT
          isDemandeur = rowDossier.user_id == session.auth.user.id
        
          if isDemandeur == False and  isRepresentant == False and isPresident == False:
              redirect(URL('default','index'))
                
          if isDemandeur and (not isPresident and not isRepresentant) and rowDossier.etat_dossier_id != Constantes.BROUILLON:
              redirect(URL('default','index'))
    
    documentService.displayFileName(False,False)
    
     # CREATION DU FORMULAIRE D'AJOUT D'UNE COMPOSANTE
    form = SQLFORM(db.piece_jointe)
   
    # ON SPECIFIE L'ID DU DOSSIER AU PROJET
    form.vars.id_dossier = request.vars.idDossier
    
    if request.vars.file_uid!=None and hasattr(request.vars.file_uid, 'filename'):
         form.vars.file_name = request.vars.file_uid.filename
    
    # SI LE FORMULAIRE EST SOUMIS
    if form.process().accepted:
        # INSERTION EN BASE        
       response.flash = 'form accepted'
        # PUIS ON REDIRIGE VERS LA PAGE DE GESTION DES COMPOSANTES
       redirect(URL('gestionPjs',vars=dict(idDossier=request.vars.idDossier)))
     # SI LE FORMULAIRE CONTIENT DES ERREURS
    elif form.errors:
        # ON VA LES AFFICHER
       response.flash = 'form has errors'
    else:
        # FORMULAIRE VIDE
       response.flash = 'please fill out the form'

    return locals()
