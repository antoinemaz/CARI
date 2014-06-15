# coding: utf8
class userService(object):

    @staticmethod
    def getPresidents():
        rows = db(db.auth_user.group_id==Constantes.PRESIDENT).select()
        return rows
    
    @staticmethod
    def getRepresentantsOfEntite(idEntite):
        
        query1 = db.auth_user.group_id==Constantes.REPRESENTANT
        query2 = db.auth_user.entite_id==idEntite
        
        rows = db(query1 & query2).select()
        return rows
    
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
  

    @staticmethod
    def random_password():
        import string
        import random
        password = ''
        specials=r'!#$*?'         
        for i in range(0,3):
            password += random.choice(string.lowercase)
            #password += random.choice(string.uppercase)
            password += random.choice(string.digits)
            #password += random.choice(specials)            
        return ''.join(random.sample(password,len(password)))

    @staticmethod
    def initPassword(id):
       mdp = userService.random_password()

       rowUser = userService.getInfosUser(id)
       rowUser.update_record(password= db.auth_user.password.validate(mdp)[0] )
       return mdp
