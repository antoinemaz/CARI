# coding: utf8
class budgetService(object):
    
    @staticmethod
    def getBudgetById(unid):
        rows = db.budget[unid]
        return rows
    
    @staticmethod
    def getProduitsByBudgetId(unid):
        query = db(db.achat.budget_id==unid).select()
        return query
