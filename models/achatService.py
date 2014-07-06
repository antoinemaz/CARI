# coding: utf8
class achatService(object):
    
    # mis à jour du budget_id pour chaque produit lorsque le dossier est accepté
    @staticmethod
    def updateBudgetOfProduitsDuDossier(dossier):
    
        # récupération de tous les budgets de l'entité du dossier
        rowBudgets = db(db.budget.entite_id == dossier.entite_id).select()
        
        dateBudget = None
        rowBudget = None
        
        # on va retrouver le dernier budget en date
        for row in rowBudgets:
            if dateBudget == None or dateBudget <= row.budget_initial:
                rowBudget = row
        
        # récupération de tous les achats du dossier
        rowAchats = db(db.achat.dossier_id == dossier.id).select()
    
        # mis à jour du budget_id de chaque achat du dossier
        if rowBudget != None:
           for row in rowAchats:
                row.update_record(budget_id=rowBudget.id)
    
    # récupération des achats par l'id du dossier
    @staticmethod
    def getAchatsByDossierId(idDossier):
        query = db.achat.dossier_id==idDossier
        return query
        
    # calcul le prix total du dossier : somme de tous les achats
    @staticmethod
    def calculerPrixTotal(idDossier):             
        query = achatService.getAchatsByDossierId(idDossier)
    
        prixTot = 0.0
    
        for row in db(query).select():
            prixTot = prixTot+row.Total
        return prixTot
