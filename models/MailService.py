# coding: utf8
class mailService(object):
    
    @staticmethod
    def sendMail(idDossier, etatAvantUpdate,request):
        from gluon.tools import Mail
        mail = Mail()
        mail.settings.server = 'gae'
        mail.settings.server = 'smtp.gmail.com:587'
        mail.settings.sender = 'antoine.mazelin@gmail.com'
        mail.settings.login = 'antoine.mazelin@gmail.com:monamour91'
        
        dossier = projetService.getDossierById(idDossier)
        demandeur = userService.getInfosUser(dossier.user_id)
        porteur = porteurService.getPorteurById(dossier.porteur_id)
        
        msgDemandeur = None
        msgResponsable = None
        msgPresident = None
                
        if(etatAvantUpdate != dossier.etat_dossier_id):
            
            if (dossier.etat_dossier_id == Constantes.SOUMIS):
                # Message aux demandeur et porteur
                msgDemandeur = 'Bonjour '+demandeur.first_name+' '+demandeur.last_name +'.\n\nVotre demande a bien été soumise. \n\nElle est actuellement en cours de traitement. Le numéro du dossier est le suivant : '+ str(dossier.id)+'.\nLe lien de la demande est la suivante : '+ str(request.env.http_host+"/"+request.application+"/projet/addProjet/")+''+'idDossier='+str(dossier.id)+'.'
                # Message aux représentant et au gestionnaire
                msgResponsable = 'Bonjour, \n\nUne demande a été soumise \n\nLe numéro du dossier est le suivant : '+ str(dossier.id)+'.'
                # Message au président
                msgPresident = 'Bonjour, \n\n Une demande a été soumise \n\nLe numéro du dossier est le suivant : '+ str(dossier.id)+'.'
            
            if (dossier.etat_dossier_id == Constantes.ACCEPTE):
                # Message aux demandeur et porteur
                msgDemandeur = 'Bonjour '+demandeur.first_name+' '+demandeur.last_name +'.\n\nLe dossier n°'+ str(dossier.id)+' a été acceptée.\n\n Voici le commentaire ajouté au dossier : \n\n'+dossier.commentaire
                # Message aux représentant et au gestionnaire
                msgResponsable = 'Bonjour, \n\Le dossier n°'+ str(dossier.id)+' a été acceptée.\n\n Voici le commentaire ajouté au dossier : \n\n'+dossier.commentaire
                # Message au président
                msgPresident = 'Bonjour, \n\Le dossier n°'+ str(dossier.id)+' a été acceptée.\n\nVoici le commentaire ajouté au dossier : \n\n'+dossier.commentaire
                
            if (dossier.etat_dossier_id == Constantes.REFUSE):
                # Message aux demandeur et porteur
                msgDemandeur = 'Bonjour '+demandeur.first_name+' '+demandeur.last_name +'.\n\nLe dossier n°'+ str(dossier.id)+' a été refusé.\n\n Voici le commentaire ajouté au dossier : \n\n'+dossier.commentaire
                # Message aux représentant et au gestionnaire
                msgResponsable = 'Bonjour, \n\Le dossier n°'+ str(dossier.id)+' a été refusé.\n\nVoici le commentaire ajouté au dossier : \n\n'+dossier.commentaire
                # Message au président
                msgPresident = 'Bonjour, \n\Le dossier n°'+ str(dossier.id)+' a été refusé.\n\nVoici le commentaire ajouté au dossier : \n\n'+dossier.commentaire
                
            if (dossier.etat_dossier_id == Constantes.ATTENTE):
                # Message aux demandeur et porteur
                msgDemandeur = 'Bonjour '+demandeur.first_name+' '+demandeur.last_name +'.\n\nLe dossier n°'+ str(dossier.id)+' a été mis en attente.\n\n Voici le commentaire ajouté au dossier : \n\n'+dossier.commentaire
                # Message aux représentant et au gestionnaire
                msgResponsable = 'Bonjour, \n\Le dossier n°'+ str(dossier.id)+' a été mis en attente.\n\nVoici le commentaire ajouté au dossier : \n\n'+dossier.commentaire
                # Message au président
                msgPresident = 'Bonjour, \n\Le dossier n°'+ str(dossier.id)+' a été mis en attente.\n\nVoici le commentaire ajouté au dossier : \n\n'+dossier.commentaire

        else:
                            # Message aux demandeur et porteur
            msgDemandeur = 'Bonjour '+demandeur.first_name+' '+demandeur.last_name +'.\n\nLe commentaire de votre dossier n°'+ str(dossier.id)+' a été mis modifié.\n\n Voici le commentaire du dossier : \n\n'+dossier.commentaire
            # Message aux représentant et au gestionnaire
            msgResponsable = 'Bonjour, \n\nLe commentaire du dossier n°'+ str(dossier.id)+' a été modifié.\n\nVoici le commentaire du dossier : \n\n'+dossier.commentaire
            # Message au président
            msgPresident = 'Bonjour, \n\nLe commentaire du dossier n°'+ str(dossier.id)+' a été modifié.\n\nVoici le commentaire du dossier : \n\n'+dossier.commentaire
                
         # Envoi des mails
        mail.send(to=[demandeur.email], cc=[porteur.mail], subject='Soumission de votre demande',message=msgDemandeur)
        mail.send(to=[dossier.mailResponsable], cc=[dossier.mailGestionnaire], subject='Soumission d\'une nouvelle demande',message=msgResponsable)
        for pres in userService.getPresidents():
              mail.send(to=[pres.email], subject='Soumission d\'une nouvelle demande',message=msgPresident)
