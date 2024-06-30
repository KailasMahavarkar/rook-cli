import os
from pprint import pprint


def getDirs(rootPath, cacheIgnoreNames=[]):
    crawlingDirs = []
    crawlingDirs.append(rootPath)

    for root, dirs, files in os.walk(rootPath, topdown=True):
        dirs[:] = [d for d in dirs if d not in cacheIgnoreNames]
        if (len(dirs) > 0):
            for dirr in dirs:
                crawlingDirs.append(os.path.join(root, dirr))

    return crawlingDirs


def getFiles(allowedExtensions=['*'], rootPath='', cacheIgnoreNames=[]):
    """
        `allowed_extensions:` list of allowed extensions (e.g., ['.txt', '.pdf'])
        `root_path:` root directory to start searching (default is current directory)
        `cache_ignore_names:` list of directory names to ignore

        `return:` list of files with specified extensions as dictionaries
    """
    files = []

    for i, item in enumerate(allowedExtensions):
        if len(item) >= 2 and item[0] == '.':
            allowedExtensions[i] = item[1:]

    for dirr in getDirs(
        rootPath=rootPath,
        cacheIgnoreNames=cacheIgnoreNames
    ):
        for f in os.listdir(dirr):
            fpath = os.path.join(dirr, f)
            if f not in files and not os.path.isdir(fpath):
                fileName = f.split('\\')[-1]
                if fileName is not None:
                    nameWithExt = fileName.split('.')
                    nameWithoutExt = '.'.join(nameWithExt[:-1])
                    if (len(nameWithExt) > 1):
                        extension = nameWithExt[-1]
                        if (extension in allowedExtensions) or ('*' in allowedExtensions):
                            files.append({
                                "fpath": fpath,
                                "directory": dirr,
                                "filename": f,
                                "extension": extension,
                                "filenameWithoutExtension": nameWithoutExt
                            })

    return files


if __name__ == '__main__':
    pprint(
        getFiles(
            allowedExtensions=['*'],
            rootPath="E:\\@cache",
            cacheIgnoreNames=['.git']
        ),
    )
