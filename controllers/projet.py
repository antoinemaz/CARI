# coding: utf8
@auth.requires_login()
def addProjet():
    
    detailsProjetView = True
    gestionProduitsView = False
    gestionPJsView = False
    finalDemandeView = False
    
    idDossier = request.vars.idDossier;
    editMode = request.vars.editMode;
    
    read = False
    nomEntite = None
    initDemande = True
    isPresident = False
    isRepresentant = False
    isDemandeur = False
    rowDossier = None
    
    user = None
    nameOfEntityUser = None
    nameOfGroupUser = None
    
    if idDossier is not None:
          
          rowDossier = projetService.getDossierById(idDossier)
           
          if rowDossier is None:
                redirect(URL('default','index'))
            
          rowPorteur = porteurService.getPorteurById(rowDossier.porteur_id)

          user = userService.getInfosUser(rowDossier.user_id)
          nameOfEntityUser = entiteService.getNameOfEntite(user.entite_id)
          nameOfGroupUser = groupService.getNameOfGroup(user.group_id)
            
          isRepresentant = groupService.isRepresentantOfDossier(session, rowDossier.entite_id)
          isPresident = session.auth.user.group_id == Constantes.PRESIDENT
          isDemandeur = rowDossier.user_id == session.auth.user.id
        
          if isDemandeur == False and  isRepresentant == False and isPresident == False:
            redirect(URL('default','index'))
        
          if (rowDossier.etat_dossier_id != Constantes.BROUILLON and editMode == None):
            read = True
    
    form=SQLFORM.factory(db.porteur, db.dossier,_class='formStyle',_name='formNormal',readonly=read)
    
    if idDossier is not None:
            options = {};
            if(rowDossier.etat_dossier_id == Constantes.SOUMIS):
                    options = {OPTION('', _value=0),
                               OPTION(Constantes.ACCEPTE_TXT, _value=Constantes.ACCEPTE),
                               OPTION(Constantes.REFUSE_TXT, _value=Constantes.REFUSE),
                               OPTION(Constantes.ATTENTE_TXT, _value=Constantes.ATTENTE)}
                    
            if(rowDossier.etat_dossier_id == Constantes.ATTENTE):
                    options = {OPTION('', _value=0),
                               OPTION(Constantes.ACCEPTE_TXT, _value=Constantes.ACCEPTE),
                               OPTION(Constantes.REFUSE_TXT, _value=Constantes.REFUSE)}
            
            if(rowDossier.etat_dossier_id == Constantes.ACCEPTE or rowDossier.etat_dossier_id == Constantes.REFUSE):
                options = {OPTION('', _value=0)}
            
            if not options:
                select = ''
                select_libelle = ''
            else:
                select = SELECT(*options, **dict(_name="idEtat", value=0, _id="boxEtats" ) )
                select_libelle = SPAN('Changer l\'état à : ')
            
            divSelectEtat = DIV(select, styles={'CODE':'display: none;'})
            if len(options) > 1:
                divSelectEtat = DIV(select_libelle, select, BR())
            
            formAdmin = FORM(DIV('Commentaire : ',_class="center"), TEXTAREA(_name='commentaire',_class="text"), divSelectEtat, INPUT(_type='submit', _value="Enregistrer"),_class="center" )
    
    if  idDossier is not None:
            
        form.vars.intitule = rowDossier.intitule
        form.vars.urgent = rowDossier.urgent
        form.vars.caractere_urgent = rowDossier.caractere_urgent
        form.vars.remplacement_materiel = rowDossier.remplacement_materiel
        form.vars.reference_materiel = rowDossier.reference_materiel
        form.vars.description = rowDossier.description
        form.vars.beneficiaires = rowDossier.beneficiaires
        form.vars.achat_courant = rowDossier.achat_courant
        form.vars.mailResponsable = rowDossier.mailResponsable
        form.vars.mailGestionnaire = rowDossier.mailGestionnaire
        form.vars.nom = rowPorteur.nom
        form.vars.prenom = rowPorteur.prenom
        form.vars.mail = rowPorteur.mail
        form.vars.entite_id = rowDossier.entite_id
        form.vars.id = rowDossier.id
        formAdmin.vars.commentaire = rowDossier.commentaire
        form.vars.commentaire = rowDossier.commentaire
        form.vars.etat_dossier_id = rowDossier.etat_dossier_id
        formAdmin.vars.idEtat = rowDossier.etat_dossier_id
        
        if form.vars.etat_dossier_id is None or form.vars.etat_dossier_id == Constantes.BROUILLON:
            initDemande = True
        else:
            initDemande = False
        
        nomEntite= entiteService.getNameOfEntite(form.vars.entite_id)
    else:
        form.vars.etat_dossier_id = Constantes.BROUILLON

        # SI LE FORMULAIRE EST SOUMIS
    if form.process(formname='formNormal').accepted:
        
       form.vars.user_id = session.auth.user.id
        
       if idDossier is None:
           idPorteur = porteurService.insertPorteur(form.vars)
           form.vars.date_dossier = request.now
           form.vars.porteur_id=idPorteur
           idDoss = projetService.insertDossier(form.vars)
            
       else:
           
           form.vars.commentaire = formAdmin.vars.commentaire

           idPort = projetService.updateDossier(form.vars, idDossier)
           porteurService.updatePorteur(form.vars, idPort)
                
           idDoss = idDossier

        # INSERTION EN BASE
       response.flash = 'form accepted'
        
       if idDossier is None:
           redirect(URL('achat', 'gestionProduits',vars=dict(idDossier=idDoss)))
       else:
           redirect(URL('addProjet',vars=dict(idDossier=idDoss)))
        
        
     # SI LE FORMULAIRE CONTIENT DES ERREURS
    elif form.errors:
        # ON VA LES AFFICHER
       response.flash = 'form has errors'
    else:
        # FORMULAIRE VIDE
       response.flash = 'please fill out the form'
    
    if  idDossier is not None:
            # SI LE FORMULAIRE GESTION EST SOUMIS
        if formAdmin.accepts(request,session):
               
               etatAvantUpdate = projetService.getDossierById(idDossier).etat_dossier_id
               
               projetService.updateStatusDossier(formAdmin.vars.commentaire, formAdmin.vars.idEtat, idDossier)
               idDoss = idDossier
                
               mailService.sendMail(idDoss,etatAvantUpdate,request)
                
                # INSERTION EN BASE
               response.flash = 'form accepted'
               redirect(URL('addProjet',vars=dict(idDossier=idDoss)))
         # SI LE FORMULAIRE CONTIENT DES ERREURS
        elif formAdmin.errors:
            # ON VA LES AFFICHER
           response.flash = 'form has errors'
        else:
            # FORMULAIRE VIDE
           response.flash = 'please fill out the form'
    else:
       formAdmin = None 
    
    return dict(form=form, formAdmin=formAdmin, entite=nomEntite, lecture=read, initDossier=initDemande, isPresident=isPresident, isRepresentant=isRepresentant, isDemandeur=isDemandeur,rowDossier=rowDossier,detailsProjetView=detailsProjetView, gestionProduitsView=gestionProduitsView, gestionPJsView=gestionPJsView, finalDemandeView=finalDemandeView, user=user, nameOfEntityUser=nameOfEntityUser, nameOfGroupUser=nameOfGroupUser)


@auth.requires_login()
def finalisationDemande():
    
    detailsProjetView = False
    gestionProduitsView = False
    gestionPJsView = False
    finalDemandeView = True
    
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
                
          if rowDossier.etat_dossier_id != Constantes.BROUILLON:
              redirect(URL('default','index'))
                                    
          if rowDossier.etat_dossier_id is None or rowDossier.etat_dossier_id == Constantes.BROUILLON:
                initDossier = True
          else:
                initDossier = False
     
    form = FORM(INPUT(_type='submit', _value="Soumettre"))
    
    changeState = False
    
    rowDos = projetService.getDossierById(idDossier)
    
    if(rowDos.etat_dossier_id == Constantes.SOUMIS):
        changeState = True;
    
    if form.accepts(request,session):
        projetService.updateEtat(Constantes.SOUMIS, idDossier)
        changeState = True;
        
        mailService.sendMail(idDossier,None,request)
        
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    
    return locals()
