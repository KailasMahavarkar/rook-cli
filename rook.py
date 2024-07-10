import subprocess
import typer
import os
from hashlib import md5
from utils.aes import Cacher as AES
from utils.util import getFiles

CACHE_PATH = "E:\\@cache"
TESTING_PATH = "E:\\@testing"


TYPER_OPTIONS = {
    "help": "help",
    "hide": "--hide",
}

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


@app.command('clean-extensions', help="Removes all files with given extensions")
def cleanExtensions(
    extensions: str = typer.Option("", help="Comma-separated list of extensions to remove"),
    inverse: bool = typer.Option(False, help="If true, removes all files except given extensions"),
    path: str = typer.Option(".", help="Path to the directory to clean")
):
    """
    extensions: comma separated extensions
    inverse: if true, removes all files except given extensions
    """
    extensions = [x.strip() for x in extensions.split(',')]
    extensions = tuple(extensions)

    def scandirs(path):
        for root, _, files in os.walk(path):
            for currentFile in files:
                file_path = os.path.join(root, currentFile)
                try:
                    # check mode
                    if inverse:
                        if not str(currentFile).lower().endswith(extensions):
                            os.remove(file_path)
                            typer.echo(f"Removed: {file_path}")
                    else:
                        if str(currentFile).lower().endswith(extensions):
                            os.remove(file_path)
                            typer.echo(f"Removed: {file_path}")
                except Exception as e:
                    typer.echo(f"Error removing {file_path}: {e}")

    scandirs(path)
    typer.echo("Operation completed successfully.")


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
def encrypt(folder: str, password: str):
    # check if argument is folder
    if os.path.isdir(folder):
        typer.echo(f"{folder} identifies as a folder")
        tool = AES(
            origin=folder,
            password=password
        )
        tool.encryptFiles()
    else:
        typer.echo(f"{folder} is not a folder")
        return


@app.command(help='decrypts the folder')
def decrypt(folder: str, password: str):

    if os.path.isdir(folder):
        typer.echo(f"{folder} identifies as a folder")
        tool = AES(
            origin=folder,
            password=password,
            allowedExtensions=['aes']
        )
        tool.decryptFiles()
    else:
        typer.echo(f"{folder} is not a folder")
        return


@app.command("cache", help="Encrypts/decrypts the cache folder")
def cache(
    encrypt_flag: bool = typer.Option(
        False, "--encrypt", help="Encrypt the cache folder"),
    decrypt_flag: bool = typer.Option(
        False, "--decrypt", help="Decrypt the cache folder"),
    password: str = typer.Option(
        "123", "--password", help="Password for encryption/decryption")
):
    if encrypt_flag and decrypt_flag:
        typer.echo(
            "Error: Cannot use both --encrypt and --decrypt flags together.")
        raise typer.Exit(code=1)
    elif encrypt_flag:
        encrypt(folder=CACHE_PATH, password=password)
        os.system(f'attrib +s +h {CACHE_PATH}')
        typer.echo("Cache folder encrypted and hidden.")
    elif decrypt_flag:
        decrypt(folder=CACHE_PATH, password=password)
        os.system(f'attrib -s -h {CACHE_PATH}')
        typer.echo("Cache folder decrypted and visible.")
    else:
        typer.echo("Error: Please use either --encrypt or --decrypt flag.")
        raise typer.Exit(code=1)


@app.command('peek', help='hide/unhide the vault (does not lock)')
def peek(hide: bool = typer.Option(False, "--hide", help="Hide the vault"),
         show: bool = typer.Option(False, "--show", help="Show the vault")):
    if hide and show:
        typer.echo("Error: Cannot use both --hide and --show flags together.")
        raise typer.Exit(code=1)
    elif hide:
        os.system(f'attrib +s +h {CACHE_PATH}')
        typer.echo("Vault is now hidden.")
    elif show:
        os.system(f'attrib -s -h {CACHE_PATH}')
        typer.echo("Vault is now visible.")
    else:
        typer.echo("Error: Please use either --hide or --show flag.")
        raise typer.Exit(code=1)


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


@app.command('shutdown', help='shutdown pc (minutes)')
def shutdown(timer: int = 0):
    typer.echo(f"pc will shutdown in {timer} mins")
    os.system(f'shutdown.exe /s /t {timer * 60}')


@app.command('adb-reverse', help='starts adb reverse port for android')
def adbReverse(port=8081):
    typer.echo(f"starting... adb reverse on port {port}")
    os.system(f'adb reverse tcp:{port} tcp:{port}')


@app.command('adb-kill', help='kills adb server')
def adbKill():
    typer.echo(f"killing... adb server")
    os.system(f'adb kill-server')


@app.command('story', help='start storybook')
def story(packageManager='npm'):
    final_command = f'yarn storybook'

    if packageManager == 'yarn':
        final_command = f'yarn storybook'
    elif packageManager == 'npm':
        final_command = f'npm run storybook'
    elif packageManager == 'pnpm':
        final_command = f'pnpm run storybook'
    else:
        typer.echo(f"package manager {packageManager} is not supported")
        return

    typer.echo(f"starting... storybook")
    os.system(final_command)


@app.command('story:native', help='start storybook for native')
def storyNative(packageManager='npm'):
    final_command = f'yarn storybook:native'

    if packageManager == 'yarn':
        final_command = f'yarn storybook:native'
    elif packageManager == 'npm':
        final_command = f'npm run storybook:native'
    elif packageManager == 'pnpm':
        final_command = f'pnpm run storybook:native'
    else:
        typer.echo(f"package manager {packageManager} is not supported")
        return

    typer.echo(f"starting... storybook for native")
    os.system(final_command)


@app.command('docs', help='start docs')
def storyNative(packageManager='npm'):
    final_command = f'yarn docs'

    if packageManager == 'yarn':
        final_command = f'yarn docs'
    elif packageManager == 'npm':
        final_command = f'npm run docs'
    elif packageManager == 'pnpm':
        final_command = f'pnpm run docs'
    else:
        typer.echo(f"package manager {packageManager} is not supported")
        return

    typer.echo(f"starting... docs")
    os.system(final_command)


@app.command('remove-audio-all', help='remove audio from video using CUDA')
def removeAudio(path: str = typer.Option(TESTING_PATH, "--path", help="Root path for videos")):
    files = getFiles(
        allowedExtensions=['mp4', 'mkv', 'webm'],
        rootPath=path,
    )

    NO_AUDIO_PATH = os.path.join(path, "no_audio")
    os.makedirs(NO_AUDIO_PATH, exist_ok=True)

    for file in files:
        input_file = file['fpath']
        input_directory = file['directory']

        common_path = os.path.relpath(input_directory, start=NO_AUDIO_PATH)
        common_path = common_path.replace(".", "")

        new_file = NO_AUDIO_PATH + common_path + '\\' + \
            file['filenameWithoutExtension'] + \
            '_no_audio' + '.' + file['extension']

        os.makedirs(os.path.dirname(new_file), exist_ok=True)

        # check if file['filenameWithoutExtension'] ends with _no_audio
        if file['filenameWithoutExtension'].endswith('_no_audio'):
            print(f"Skipping {file['filename']}")
            continue

        # remove audios
        ffmpeg_cmd = f'ffmpeg -y -hwaccel cuda -i "{input_file}" -c:v copy -an "{new_file}"'
        os.system(ffmpeg_cmd)
        print(f"Processed {file['filename']}")

    print("All files processed successfully")


@app.command('carwaleweb:test', help='start carwale test')
def carwalewebTest(platforms='carwale'):
    platforms = platforms.replace(" ", "").split(",")
    platformMap = {
        'carwale': r'carwale\\PWA',
        'bikewale': r'BikeWale.UI\\pwa',
        'editorial': r'editorial\\ui',
        'emicalci': r'EmiCalci\\ui',
        'finance': r'finance\\ui',
        'leadform': r'leadform\\ui',
        'leadform-shared': r'leadform\\ui-shared',
        'location': r'location\\ui',
        'mobility': r'mobilityoutlook\\ui',
        'retail': r'Retail\\ui',
        'testdrive': r'TestDrive\\ui',
        'used': r'used\\ui-shared',
    }

    for platform in platforms:
        if platform in platformMap:
            platformPath = os.path.join(
                r"C:\\Users\\Kailas.m\\Desktop\\carwale\\carwaleweb", 
                platformMap[platform]
            )

            if os.path.exists(platformPath):
                # Change the working directory to the specified directory
                os.chdir(platformPath)

                # Now, you can run a PowerShell function within this directory using subprocess
                powershell_command = f"npm run test"
                try:
                    subprocess.run(["powershell", powershell_command], shell=True, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error running PowerShell command: {e}")
            else:
                print(f"path {platformPath} does not exist.")
        else:
            print("Invalid platform provided.")

if __name__ == "__main__":
    app()
