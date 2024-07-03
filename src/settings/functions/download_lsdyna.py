import requests
import os
join = os.path.join
import tarfile
download_folder = join(os.getcwd(), "src", "settings", "downloads")
dependen_folder = join(os.getcwd(), "src", "dependences")

def download_lsdyna_linux():

    url = "https://ftp.lstc.com/anonymous/outgoing/lsprepost/4.10/linux64/lsprepost-4.10.8-common-06Nov2023.tgz"

    response = requests.get(url)

    if response.status_code == 200:
        with open("lsdyna.tgz", "wb") as file:
            file.write(response.content)

    
    # move the file to the downloads folder
    os.rename("lsdyna.tgz", join(download_folder, "lsdyna.tgz"))


    # Extract the file with python
    
    with tarfile.open(join(download_folder, "lsdyna.tgz"), "r:gz") as tar:
        tar.extractall(path=dependen_folder)

def download_lsdyna_windows():

    lsdyna_path = join(download_folder, "lsdyna.exe")

    if os.path.exists(lsdyna_path):
        print("File already exists")
        return
    
    url = "https://ftp.lstc.com/anonymous/outgoing/lsprepost/4.10/win64/LS-PrePost-4.10.11-x64-27Mar2024_setup.exe"

    response = requests.get(url)

    if response.status_code == 200:
        with open("lsdyna.exe", "wb") as file:
            file.write(response.content)

    
    # move the file to the downloads folder
    os.rename("lsdyna.exe", join(download_folder, "lsdyna.exe"))

    # Extract the file with python
    
def download_lsdyna():
    if os.name == "posix":
        download_lsdyna_linux()
    else:
        download_lsdyna_windows()