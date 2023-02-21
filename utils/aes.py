from collections import defaultdict
import utils.base62 as base
import pyAesCrypt as fileaes
import json
import os
from utils.textaes import AESCipher

def join(path, child):
    return os.path.join(path, child)

class Cacher:
    @staticmethod
    def cacheIgnoreCheck(cacheIgnoreNames, cachePath):
        # check if .cacheignore exists
        if (os.path.isfile(cachePath)):
            # loop through cache file
            with open(cachePath, 'r') as file:
                for line in file:
                    if (len(line) > 1):
                        cacheIgnoreNames.append(line.strip())
        return cacheIgnoreNames

    def __init__(self, 
            origin='',
            ignorePaths=[],
            password='123',
            allowedExtensions=[
                'webm', 'mpg', 'mp2', 'mpeg', 'mpe',
                'mpv', 'ogg', 'mp4', 'm4p', 'm4v', 'avi',
                'wmv.mov', 'qt', 'flv', 'swf', 'avchd', 'txt'
            ],


        ) -> None:
        # get all subdirectories
        self.origin = origin
        self.password = password
        self.root = os.path.abspath(os.path.dirname(__file__))
        self.textAes = AESCipher(self.password)
        self.uuidMap = {}
        self.allowedExtensions = allowedExtensions

        self.errorPath = join(self.origin, "error.enc")
        self.errorRawPath = join(self.origin, 'cache.err')

        self.lockfile = join(self.root, '.lockfile')
        self.cacheIgnorePath = join(self.root, '.cacheignore')
        self.cacheIgnoreNames = self.cacheIgnoreCheck(ignorePaths, self.cacheIgnorePath)

    def crawlDirs(self):
        crawlingDirs = []

        crawlingDirs.append(self.origin)
        for root, dirs, files in os.walk(self.origin, topdown=True):
            dirs[:] = [d for d in dirs if d not in self.cacheIgnoreNames]

            if (len(dirs) > 0):
                for dirr in dirs:
                    crawlingDirs.append(os.path.join(root, dirr))

        return crawlingDirs

    def crawlFiles(self, mode='encrypt'):
        files = []
        dirs = []
        if mode == 'decrypt':
            self.allowedExtensions = ['aes']

        for dirr in self.crawlDirs():
            for f in os.listdir(dirr):
                fpath = os.path.join(dirr, f)
                if f not in files and not os.path.isdir(fpath):
                    fileName = f.split('\\')[-1]
                    if fileName is not None:
                        nameWithExt = fileName.split('.')
                        if (len(nameWithExt) > 1):
                            extension = nameWithExt[-1]
                            if (extension in self.allowedExtensions):
                                files.append({
                                    "fpath": fpath,
                                    "directory": dirr,
                                    "filename": f,
                                    "extension": extension
                                })

        return files

    def encryptFiles(self):
        errorMap = {}
        errorJSON = {}
        visited = defaultdict(list)

        """
            file = {
                filename: "dummy",
                extension: ".mp4",
                fpath: "E:/test/dummy.mp4",
                directory: "E:/test"
            }
        """
        for file in self.crawlFiles():
            filename = file['filename']
            fpath = file['fpath']
            dirr = file['directory']

            newName = base.encode62(filename)
            newNameWithExt = newName + '.aes'
            encPath = fpath.replace(filename, newNameWithExt)

            if dirr not in visited:
                visited[dirr] = 1
                print("encrypting directory: ", dirr)

            try:
                fileaes.encryptFile(
                    fpath,
                    encPath,
                    self.password
                )
                os.remove(fpath)
            except Exception as e:
                errorMap[filename] = str(e)

        if errorMap != {}:
            errorJSON = str(json.dumps(errorMap))
            with open(file=self.errorPath, mode='w+') as file:
                file.write(errorJSON)

    def decryptFiles(self):
        errorMap = {}
        errorJSON = {}
        visited = defaultdict(list)

        for file in self.crawlFiles(mode='decrypt'):
            filename = file['filename']
            fpath = file['fpath']
            dirr = file['directory']

            if dirr not in visited:
                visited[dirr] = 1
                print("decrypting directory: ", dirr)

            if filename.endswith('.aes'):
                newName = base.decode62(filename.split('.aes')[0])
                newPath = fpath.replace(filename, newName)

                try:
                    fileaes.decryptFile(fpath, newPath, self.password)
                    os.remove(fpath)
                except Exception as e:
                    errorMap[filename] = str(e)


        if errorMap != {}:
            errorJSON = json.dumps(errorMap)
            with open(file=self.errorPath, mode='w+') as file:
                file.write(str(errorJSON, encoding='utf-8'))


if __name__ == "__main__":
    instance = Cacher(origin='E:\@cache')
    instance.encryptFiles()

    # instance.decryptFiles()
