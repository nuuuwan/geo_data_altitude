import os

from utils import JSONFile


class Places:
    @staticmethod
    def mountains():
        return JSONFile(os.path.join('data', 'mountains.json')).read()

    @staticmethod
    def buildings():
        return JSONFile(os.path.join('data', 'buildings.json')).read()
