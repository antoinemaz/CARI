# coding: utf8
class userService(object):

    @staticmethod
    def getInfosUser(unid):
         rows = db.auth_user[unid]
         return rows

    # METHODE QUI VA AUTORISER OU REFUSER LA MODIFICATION/LECTURE DU ROLE ET COMPOSANTE D'UN UTILISATEUR
    # @param read : booléan. True : les champs entite  et role vont être visibles
    # @param write : booléan. True : les champs entite et role vont être modifiables
    @staticmethod
    def readonlyUser(read, write):
         db.auth_user.group_id.readable = read
         db.auth_user.group_id.writable = write
         db.auth_user.entite_id.readable = read
         db.auth_user.entite_id.writable = write
