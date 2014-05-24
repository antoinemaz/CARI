# coding: utf8
class porteurService(object):

    @staticmethod
    def getPorteurById(unid):
         rows = db.porteur[unid]
         return rows

    @staticmethod
    def insertPorteur(vars):
        return db.porteur.insert(**db.porteur._filter_fields(vars))
    
    @staticmethod
    def updatePorteur(vars, idPorteur):
         rowPor = porteurService.getPorteurById(idPorteur)
         rowPor.update_record(**db.porteur._filter_fields(vars))