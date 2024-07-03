import os

def createFolder(out_folder):
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    # remove all files .step
    #for file in os.listdir(out_folder):
    #    os.remove(os.path.join(out_folder, file))
