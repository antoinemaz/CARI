# coding: utf8
class entiteService(object):
    
    # get nom de l'entité par son id
    @staticmethod
    def getNameOfEntite(unid):
        if unid is None:
            name =""
        else:
            name = db.entite[unid].name
        return name
