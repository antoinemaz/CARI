# coding: utf8
class groupService(object):

    # méthode qui permet de savoir si le user connecté est un représentant de l'entité passé en paramètre
    @staticmethod
    def isRepresentantOfDossier(mySession, entiteId):
        # get users ayant le role representant
        query = db(db.auth_user.group_id==Constantes.REPRESENTANT).select(db.auth_user.id)
    
        find = False;

        # parcours des representants
        for row in query:
            # s'il est representant et qu'il est dans la meme entité, on retourne vrai, c'est un representant de l'entite
            if row.id==mySession.auth.user.id and entiteId == mySession.auth.user.entite_id:
                find=True
                break
    
        return find;
    
    # get nom du role
    @staticmethod
    def getNameOfGroup(unid):
        return db.auth_group[unid].role

    #mise a jour de la table membership de web2py lorsque l'on change le role d'un user
    @staticmethod
    def updateMembership(userId, groupId):
           # LORSQUE L'ON DEFINIT UN ROLE A UN UTILISATEUR, ON FAIT UN MODIFICATION DANS LA TABLE JOINTURE DES GROUPES(ROLES) DEFINIT
           # PAR WEB2PY >> NECESSAIRE POUR LA GESTION DES HABILITATIONS DES DECORATEURS DE WEB2PY
           db(db.auth_membership.user_id == userId).update(group_id=groupId)
          
    #ajout dans la table membership de web2py d'une occurence userId pour un roleId
    @staticmethod
    def inserMembership(userId, groupId):
       # LORSQUE L'ON DEFINIT UN ROLE A UN UTILISATEUR, ON FAIT UNE INSERTION DANS LA TABLE JOINTURE DES GROUPES(ROLES) DEFINIT
       # PAR WEB2PY >> NECESSAIRE POUR LA GESTION DES HABILITATIONS DES DECORATEURS DE WEB2PY
       db.auth_membership.insert(user_id = userId, group_id = groupId)
