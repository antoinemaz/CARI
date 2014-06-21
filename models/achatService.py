# coding: utf8
class achatService(object):
    
    @staticmethod
    def updateBudgetOfProduitsDuDossier(dossier):
    
        rowBudgets = db(db.budget.entite_id == dossier.entite_id).select()
        
        dateBudget = None
        rowBudget = None
        for row in rowBudgets:
            if dateBudget == None or dateBudget <= row.budget_initial:
                rowBudget = row
        
        rowAchats = db(db.achat.dossier_id == dossier.id).select()
    
        if rowBudget != None:
           for row in rowAchats:
                row.update_record(budget_id=rowBudget.id)
    
    @staticmethod
    def getAchatsByDossierId(idDossier):
        query = db.achat.dossier_id==idDossier
        return query
        
    @staticmethod
    def calculerPrixTotal(idDossier):             
        query = achatService.getAchatsByDossierId(idDossier)
    
        prixTot = 0.0
    
        for row in db(query).select():
            prixTot = prixTot+row.Total
        return prixTot
