# coding: utf8
class documentService(object):

    # droit de visu et de modification du nom du fichier
    @staticmethod
    def displayFileName(read, write):
        db.piece_jointe.file_name.readable = read
        db.piece_jointe.file_name.writable = write

    # récupération des documents à partir de l'id du dossier
    @staticmethod
    def getDocumentsByDossierId(idDossier):
        query = db.piece_jointe.id_dossier==idDossier
        return query
