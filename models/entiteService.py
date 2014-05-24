# coding: utf8
class entiteService(object):
    
    @staticmethod
    def getNameOfEntite(unid):
        if unid is None:
            name =""
        else:
            name = db.entite[unid].name
        return name
