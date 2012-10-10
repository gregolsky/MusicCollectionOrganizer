import shutil


class FileMover(object):

    def __init__(self):
        pass

    @staticmethod
    def MoveFile(file=None, destination=None):
        if not file and not destination:
            return;
        else:
            shutil.move(file, destination)
