import typer
import os
from hashlib import md5
from utils.aes import Cacher as AES
from utils.env import getKey, setKey, deleteKey

# create typer instance
app = typer.Typer(
    help="Awesome CLI user manager.")


@app.command('ohio', help='welcome message')
def ohio():
    typer.echo(f">> Ohio Kai :)")
    typer.echo(f">> Type 'rook --help' to begin")


@app.command('ys', help='yarn start')
def yarnStart():
    os.system("yarn start")


@app.command('yd', help='yarn dev')
def yarnDev():
    os.system("yarn dev")


@app.command(help="runs the django server")
def runserver():
    os.system("python manage.py runserver")


@app.command(help="pings google 10000 times")
def pinger():
    os.system('ping -n 10000 -w 500 8.8.8.8')


@app.command(help="removes all files with given extension")
def cleanExtensions(extensions: str):
    extensions = [x.strip() for x in extensions.split(',')]
    extensions = tuple(extensions)

    def scandirs(path):
        for root, _, files in os.walk(path):
            for currentFile in files:
                if (str(currentFile).lower().endswith(tuple(extensions))):
                    os.remove(os.path.join(root, currentFile))

    typer.echo(scandirs('.'))


@app.command(help='create new file')
def touch(filename: str):
    # check if file exists
    if (os.path.isfile(filename)):
        typer.echo(f"file {filename} already exists")
        return

    # create file
    with open(filename, 'w') as file:
        file.write('')

    typer.echo(f"file {filename} created successfully")


@app.command(help='encrypts the folder')
def encrypt(argument: str, password: str):
    # check if argument is folder
    if os.path.isdir(argument):
        typer.echo(f"{argument} identifies as a folder")
    else:
        typer.echo(f"{argument} is not a folder")
        return

    folderHash = md5(argument.encode()).hexdigest()
    folder = argument

    if getKey(folderHash) is None:
        tool = AES(
            origin=folder,
            password=password
        )
        tool.encryptFiles()
        setKey(folderHash, True)
    else:
        typer.echo(f"folder {folder} is already encrypted")
        confirm = typer.prompt(
            "do you want to decrypt? (y/n)"
        )

        if confirm == 'y':
            tool = AES(
                origin=folder,
                password='299792458'
            )
            tool.decryptFiles()
            deleteKey(folderHash)

        else:
            typer.echo('>> stopping encryption process')


@app.command(help='decrypts the folder')
def decrypt(argument: str, password: str):

    if os.path.isdir(argument):
        typer.echo(f"{argument} identifies as a folder")
    else:
        typer.echo(f"{argument} is not a folder")
        return

    folderHash = md5(argument.encode()).hexdigest()

    if (getKey(folderHash) is not None):
        tool = AES(
            origin=argument,
            password=password
        )
        tool.decryptFiles()
        deleteKey(folderHash)
    else:
        typer.echo(f"folder {argument} is not encrypted")


@app.command('lock', help='hides the vault')
def encryptCache(password: str, hide: bool = True):
    CACHE = "E:/@cache"
    encrypt(
        argument=CACHE,
        password=password
    )

    if hide:
        os.system(f'attrib +s +h {CACHE}')


@app.command('unlock', help='unhides the vault')
def decryptCache(password: str, unhide: bool = True):
    CACHE = "E:/@cache"

    decrypt(
        argument=CACHE,
        password=password
    )

    if unhide:
        os.system(f'attrib -s -h {CACHE}')


@app.command('peeker', help='hide/unhide the vault (does not lock)')
def peeker(peek: bool = True):
    CACHE = "E:/@cache"
    if peek:
        os.system(f'attrib -s -h {CACHE}')
    else:
        os.system(f'attrib +s +h {CACHE}')


@app.command('git-switch', help='switches git user with specific name')
def gitSwitch(profile: str):
    profileMap = {
        "orkait": "orkaitsolutions@gmail.com",
        "kai": "kailashmahavarkar5@gmail.com",
        "cwk": "kailas.m@carwale.com"
    }

    if (profile in profileMap):
        os.system(f'git config --global user.name "{profile}"')
        os.system(f'git config --global user.email "{profileMap[profile]}"')
        print(f'echo "git switch user: {profile}"')
    else:
        print(f'echo "profile {profile} is does not exists"')
        print(f'echo possible values, {[x for x in profileMap.keys()]}')


@app.command('shutdown', help='shutdown pc (minutes)')
def shutdown(timer: int = 0):
    typer.echo(f"pc will shutdown in {timer} mins")
    os.system(f'shutdown.exe /s /t {timer * 60}')


if __name__ == "__main__":
    app()
