# coding: utf8
def projets():
    
    db.dossier.etat_dossier_id.readable=True
    db.dossier.entite_id.readable=True

    gridProjets = SQLFORM.grid(projetService.getQueryOfDossier(session), fields=[db.dossier.id, db.dossier.intitule, db.dossier.porteur_id, db.dossier.etat_dossier_id, db.dossier.entite_id, db.dossier.date_dossier], searchable=False, csv=False, ui="jquery-ui", links_in_grid=True, details=False, create=False, deletable=False, editable=False, links=[lambda row:A("Détail", _href=URL("projet", "addProjet", vars=dict(idDossier=row.id)))])
    
    return locals()
