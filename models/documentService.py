# coding: utf8
class documentService(object):

    @staticmethod
    def displayFileName(read, write):
        db.piece_jointe.file_name.readable = read
        db.piece_jointe.file_name.writable = write
     
    @staticmethod
    def getDocumentsByDossierId(idDossier):
        query = db.piece_jointe.id_dossier==idDossier
        return query
