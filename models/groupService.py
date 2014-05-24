# coding: utf8
class groupService(object):

    @staticmethod
    def isRepresentantOfDossier(mySession, entitePorteurId):
        query = db(db.auth_user.group_id==Constantes.REPRESENTANT).select(db.auth_user.id)
    
        find = False;
    
        for row in query:
            if row.id==mySession.auth.user.id and entitePorteurId == mySession.auth.user.entite_id:
                find=True
                break
    
        return find;
    
    @staticmethod
    def getNameOfGroup(unid):
        return db.auth_group[unid].role

    @staticmethod
    def updateMembership(userId, groupId):
           # LORSQUE L'ON DEFINIT UN ROLE A UN UTILISATEUR, ON FAIT UN MODIFICATION DANS LA TABLE JOINTURE DES GROUPES(ROLES) DEFINIT
           # PAR WEB2PY >> NECESSAIRE POUR LA GESTION DES HABILITATIONS DES DECORATEURS DE WEB2PY
           db(db.auth_membership.user_id == userId).update(group_id=groupId)
            
    @staticmethod
    def inserMembership(userId, groupId):
       # LORSQUE L'ON DEFINIT UN ROLE A UN UTILISATEUR, ON FAIT UNE INSERTION DANS LA TABLE JOINTURE DES GROUPES(ROLES) DEFINIT
       # PAR WEB2PY >> NECESSAIRE POUR LA GESTION DES HABILITATIONS DES DECORATEURS DE WEB2PY
       db.auth_membership.insert(user_id = userId, group_id = groupId)
