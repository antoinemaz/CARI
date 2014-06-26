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
    
    @staticmethod
    def formatDate(date):
          strDate = str(date)
          from datetime import datetime
          d = datetime.strptime(strDate, '%Y-%m-%d')
          day_string = d.strftime('%d/%m/%Y')
          return day_string

    @staticmethod
    def getTotalProduitsByBudgetId(unid):
        query = db(db.achat.budget_id==unid).select()
        prixTot = 0.0
    
        for row in query:
            prixTot = prixTot+row.Total
        return prixTot

    @staticmethod
    def getPercentValue(value, chiffres):
         return round(value, chiffres)

    @staticmethod
    def getLastBudgets():
        newBudgets = db.executesql('SELECT * FROM budget b1 WHERE date_budget = (SELECT max(date_budget) FROM budget b2 WHERE b1.entite_id = b2.entite_id);', as_dict=True)
        return newBudgets
