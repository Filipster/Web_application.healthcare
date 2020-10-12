import os




# ----------------------------- Configurações de cache ---------------------
class FileReference:

    def __init__(self, filename):
        self.filename = filename


def hash_file_reference(file_reference):
    filename = file_reference.filename
    return (filename, os.path.getmtime(filename))