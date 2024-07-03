import requests
import os
join = os.path.join
import shutil
download_folder = join(os.getcwd(), "src", "settings", "downloads")
dependen_folder = join(os.getcwd(), "src", "dependences")

def download_prepomax():

    lmp_zip = join(download_folder, "prepomax.zip")

    if not os.path.exists(lmp_zip):

        url = "https://prepomax.fs.um.si/Files/Downloads/PrePoMax%20v2.0.0.zip"

        response = requests.get(url)

        if response.status_code == 200:
            with open("prepomax.zip", "wb") as file:
                file.write(response.content)

        
        # move the file to the downloads folder
        os.rename("prepomax.zip", lmp_zip)


    # Extract the file with python
    
        shutil.unpack_archive(lmp_zip, dependen_folder, "zip")

        # remove blank spaces of folder name
        os.rename(join(dependen_folder, "PrePoMax v2.0.0"), join(dependen_folder, "PrePoMax"))
    else:
        print("File already exists")
