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
