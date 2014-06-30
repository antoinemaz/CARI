# coding: utf8
from gluon.tools import Auth
# INSTANCE D'UNE CONNEXION BDD
db = DAL('mysql://root@localhost/cari')

# TABLE COMPOSANTE
db.define_table('entite', Field('name'), format='%(name)s')

db.entite.name.label="Nom"
db.entite.name.requires=IS_NOT_EMPTY()

# ID DES ENTITES INVISIBLES DANS LES FORMULAIRES
db.entite.id.readable = False

# TABLE BUDGET LIE A UNE ENTITE
db.define_table('budget', Field('date_budget','date'), Field('budget_initial','double'), Field('entite_id','reference entite'),
                 Field.Virtual('Date', lambda row: budgetService.formatDate(row.budget.date_budget) ))


db.budget.budget_initial.represent = lambda name,row: str(name) +' €'

db.budget.entite_id.label="Entité"
db.budget.budget_initial.label='Budget initial'
db.budget.date_budget.label='Date'
db.budget.date_budget.readable=False

# GESTION DE LA TABLE DES UTILISATEURS : MODIFICATION DES TABLES DES USERS DE WEB2PY
auth = Auth(db)
# UN UTILISATEUR EST LIE A UNE COMPOSANTE ET UN GROUPE (ROLE)
# NO ACTION : REND LA SUPPRESSION EN CASCADE IMPOSSIBLE
auth.settings.extra_fields['auth_user'] = [
Field('entite_id', 'reference entite',ondelete='NO ACTION' ),
Field('group_id', 'reference auth_group',ondelete='NO ACTION')]

# ON REDEFINIT LA TABLE GROUPE DE WEB2PY
db.define_table(auth.settings.table_group_name,
                Field('role', length=512, default=''),Field('description', 'text', default=''),format='%(role)s' )

custom_auth_table = db[auth.settings.table_group_name] # ON RECUPERE LA CUSTOM TABLE DEFINIE AU DESSUS
# AJOUT DES CHAMPS OBLIGATOIRES
custom_auth_table.role.requires =   IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.description.requires =   IS_NOT_EMPTY(error_message=auth.messages.is_empty)
auth.settings.table_group = custom_auth_table # ON LIE LA CUSTOM TABLE A LA VRAIE TABLE GROUP

# CREATION DES TABLES D'AUTHENTIFICATION EN BASE
auth.define_tables()

# CONTROLLEUR PAR DEFAUT DES VUES CONCERNANT LES UTILISATEURS (GERE PAR WEB2PY)
auth.settings.controller = 'default'
# ON DEFINIT LA PAGE DE CONNEXION DES UTILISATEURS : PAGE user
auth.settings.login_url = URL('user', args='login');

# MODIFICATION DES LABELS DES CHAMPS DANS LES FORMULAIRES
db.auth_user.entite_id.label='Entité'
db.auth_user.group_id.label='Role'
# POSSIBILITE DE NE PAS RENSEIGNER DE COMPOSANTE POUR UN UTILISATEUR
db.auth_user.entite_id.requires=IS_IN_DB(db,'entite.id','%(name)s')

# ID DE LA TABLE UTILISATEUR INVISIBLE DES LES FORMULAIRES
db.auth_user.id.readable = False

auth.settings.actions_disabled.append('register')

default_application = "CARI"
default_controller = "listeProjets"
default_function = "projets"

auth.settings.login_next = URL('listeProjets','projet')
auth.settings.profile_next = URL('profile')
auth.settings.change_password_next = URL('profile')

auth.settings.password_min_length = 1

mailService.settingMail()
auth.messages.reset_password_subject = 'Choisir un autre mot de passe'
auth.messages.reset_password = 'Bonjour, \n\n veuillez cliquer sur le lien suivant pour choisir un autre mot de passe :  http://' +     request.env.http_host +     URL(r=request,c='default',f='user',args=['reset_password']) +     '/%(key)s'

# TABLE PORTEUR
db.define_table('porteur', Field('nom'), Field('prenom'), Field('mail'))

db.porteur.nom.requires=IS_NOT_EMPTY()
db.porteur.mail.requires=IS_EMPTY_OR(IS_EMAIL())

# TABLE ETAT DOSSIER
db.define_table('etat_dossier',Field('nom'), format='%(nom)s')

# TABLE DOSSIER : UN DOSSIER LIE A UN UTILISATEUR
db.define_table('dossier',
Field('intitule'), Field('urgent', 'boolean'), Field('caractere_urgent'), Field('remplacement_materiel','boolean'), Field('reference_materiel'),
Field('description','text'), Field('beneficiaires'), Field('mailResponsable'), Field('mailGestionnaire'), Field('achat_courant','boolean'), Field('user_id','reference auth_user'),Field('porteur_id','reference porteur',writable=False,readable=False), Field('etat_dossier_id','reference etat_dossier',writable=False,readable=False), Field('commentaire','text'),Field('date_dossier','datetime',writable=False, requires = IS_DATETIME(format=('%d/%m/%Y à %H:%M:%S'))), Field('entite_id','reference entite'))

db.dossier.entite_id.label="Entité"

db.dossier.user_id.requires=IS_EMPTY_OR(IS_IN_DB(db,'auth_user.id',))
db.dossier.intitule.requires=IS_NOT_EMPTY()
db.dossier.beneficiaires.requires=IS_NOT_EMPTY()
db.dossier.intitule.requires=IS_NOT_EMPTY()
db.dossier.description.requires=IS_NOT_EMPTY()
db.dossier.beneficiaires.requires=IS_NOT_EMPTY()
db.dossier.mailResponsable.requires=IS_EMAIL()
db.dossier.mailGestionnaire.requires=IS_EMPTY_OR(IS_EMAIL())

db.dossier.etat_dossier_id.label="Etat"
db.dossier.mailResponsable.label='Email du responsable'
db.dossier.mailGestionnaire.label='Email du gestionnaire'
db.dossier.date_dossier.label='Date de création du dossier'

# TABLE PRODUIT : UN PRODUIT EST LIE A UN DOSSIER
db.define_table('achat',
Field('libelle'), Field('prix_unitaire','double',default=0.0), Field('date_achat','date'), Field('qte', 'integer',default=1), Field('dossier_id','reference dossier'), Field('budget_id','reference budget', readable=False, writable=False), Field('entite_id','reference entite'), Field.Virtual('Total', lambda row: row.achat.prix_unitaire*row.achat.qte))

db.achat.qte.label='Quantité'
db.achat.date_achat.label='Date d\'achat'

db.achat.date_achat.represent = lambda name, row: name.strftime("%d/%m/%Y")
db.achat.prix_unitaire.represent = lambda name,row: str(name) +' €'
db.achat.prix_unitaire.represent = lambda name,row: str(name) +' €'
db.achat.Total.represent = lambda name,row: str(name) +' €'

db.achat.prix_unitaire.requires=IS_NOT_EMPTY()
db.achat.qte.requires=IS_INT_IN_RANGE()
db.achat.qte.prix_unitaire=IS_DECIMAL_IN_RANGE(dot=",")
db.achat.date_achat.requires=IS_NOT_EMPTY()
db.achat.libelle.requires=IS_NOT_EMPTY()

db.achat.id.readable = False
db.achat.id.writable = False

db.achat.dossier_id.writable = False
db.achat.dossier_id.readable = False

db.achat.entite_id.label = "Budget"

db.define_table('piece_jointe',
    Field('file_uid', 'upload',autodelete=True), Field('file_name', 'text'),Field('id_dossier','integer'))

db.piece_jointe.file_uid.requires = IS_UPLOAD_FILENAME()

db.piece_jointe.id_dossier.readable = False
db.piece_jointe.id_dossier.writable = False
db.piece_jointe.file_name.readable = True
db.piece_jointe.file_uid.label='Choisir un fichier'
db.piece_jointe.file_name.label='Nom du fichier'
db.piece_jointe.file_uid.label='Fichier'
db.piece_jointe.id.writable = False
db.piece_jointe.id.readable = False

#readonlyUser(True, False)

# METHODE QUI VA PEUPLER LA BASE DE DONNEES, A APPLIQUER A CHAQUE INITIALISATION DE LA BASE
# A EXECUTER AVEC LE SHELL
def scriptInsert():

    # ON AJOUTE LES 3 ROLES
    auth.add_group('President', 'Président de l\'association CARI')
    auth.add_group('Utilisateur', 'Personne soumettant les demandes')
    auth.add_group('Représentant', 'Représentant de l\'entité')

    # INSERTION DU PREMIER UTILISATEUR
    db.auth_user.insert(
            password = db.auth_user.password.validate('admin')[0],
            email = 'admin@admin.com',
            first_name = 'System',
            last_name = 'Administrator',
            group_id=1
    )

    # ON AFFECTE LE ROLE PRESIDENT AU PREMIER UTILISATEUR
    auth.add_membership(user_id=1, group_id=1)

    # LISTE DES ENTITES
    db.entite.insert(name="UFR LAM");

    # INSERTION DES ETATS
    db.etat_dossier.insert(nom="Brouillon")
    db.etat_dossier.insert(nom="Soumis")
    db.etat_dossier.insert(nom="Suspendu")
    db.etat_dossier.insert(nom="Accepté")
    db.etat_dossier.insert(nom="Refusé")
    
    #UN BUDGET POUR TESTER
    db.budget.insert(entite_id=1, date_budget='2014-06-30', budget_initial="10000")
