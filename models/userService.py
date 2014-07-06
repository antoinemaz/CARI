# coding: utf8
class userService(object):

    # get tous les présidents
    @staticmethod
    def getPresidents():
        rows = db(db.auth_user.group_id==Constantes.PRESIDENT).select()
        return rows
    
    # get representants de l'entité passé en paramètre
    @staticmethod
    def getRepresentantsOfEntite(idEntite):
        
        # representant + entité passé en paramètre
        query1 = db.auth_user.group_id==Constantes.REPRESENTANT
        query2 = db.auth_user.entite_id==idEntite
        
        rows = db(query1 & query2).select()
        return rows
    
    # get informations du user
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
  
    # construction d'une chaine aléatoire pour le mot de passe lors de l'ajout d'un user
    @staticmethod
    def random_password():
        import string
        import random
        password = ''
        specials=r'!#$*?'         
        for i in range(0,3):
            password += random.choice(string.lowercase)
            password += random.choice(string.digits)
        return ''.join(random.sample(password,len(password)))

    # mis a jour du mot passe d'un user avec un mot de passe créé aléatoirement
    @staticmethod
    def initPassword(id):
       # création d'un mdp aléatoire
       mdp = userService.random_password()

       rowUser = userService.getInfosUser(id)
        
       # update du mot de passe du user (retrouvé avec son id passé en paramètre)
       rowUser.update_record(password= db.auth_user.password.validate(mdp)[0] )
       return mdp
