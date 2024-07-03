import requests
import os
join = os.path.join
import shutil
download_folder = join(os.getcwd(), "src", "settings", "downloads")
dependen_folder = join(os.getcwd(), "src", "dependences")

def download_lammps():

    if os.name == "nt":
        print("This script is only for linux, please download LAMMPS manually")
        return


    lmp_zip = join(download_folder, "lammps.zip")

    if not os.path.exists(lmp_zip):

        url = "https://github.com/lammps/lammps/archive/refs/heads/stable.zip"

        response = requests.get(url)

        if response.status_code == 200:
            with open("lammps.zip", "wb") as file:
                file.write(response.content)

        
        # move the file to the downloads folder
        os.rename("lammps.zip", lmp_zip)


    # Extract the file with python
    
    shutil.unpack_archive(lmp_zip, dependen_folder, "zip")
