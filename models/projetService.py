# coding: utf8
class projetService(object):

    @staticmethod
    def getDossierById(unid):
        rows = db.dossier[unid]
        return rows

    @staticmethod
    def insertDossier(vars):
        return db.dossier.insert(**db.dossier._filter_fields(vars))
    
    @staticmethod
    def updateDossier(vars, idDossier):
        rowDos = projetService.getDossierById(idDossier)
        rowDos.update_record(**db.dossier._filter_fields(vars))
        return rowDos.porteur_id
    
    @staticmethod
    def updateStatusDossier(comment, etat_id, idDossier):
        
        if idDossier is not None:
            rowDos = projetService.getDossierById(idDossier)
            rowDos.update_record(commentaire= comment)

        if etat_id is not None and etat_id != 0 and etat_id != '0':
              projetService.updateEtat(etat_id,idDossier)
              rowDos.update_record(etat_dossier_id= etat_id)

              if etat_id == Constantes.ACCEPTE:
                  achatService.updateBudgetOfProduitsDuDossier(idDossier)

    @staticmethod
    def updateEtat(etat_id, idDossier):
         if idDossier is not None:
              rowDos = projetService.getDossierById(idDossier)
              rowDos.update_record(etat_dossier_id=etat_id)
