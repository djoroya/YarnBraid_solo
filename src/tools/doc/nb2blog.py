import os
import nbformat
from nbconvert import MarkdownExporter
import shutil
import glob
header = """Title: VAR_NAME
Date: 2010-12-03 10:20
Category: notebook
Header: VAR_HEADER
Type: notebook
Path: VAR_PATH

"""

def nb2blog(notebook_path, content_folder):

    output_dir = "temp_nb2blog"
    # remove if exists
    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(output_dir, exist_ok=True)

    error = False
    try:
        # Cargar el cuaderno de Jupyter
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        # Crear un exportador de Markdown y exportar el cuaderno
        exporter = MarkdownExporter()
        body, resources = exporter.from_notebook_node(nb)

        name_blog = "__".join(notebook_path.split("/")[2:]).replace(".ipynb","")
        header_loop = header.replace("VAR_NAME",name_blog)
        header_loop = header_loop.replace("VAR_HEADER",name_blog)
        path_list = notebook_path.split(os.sep)[2:]
        header_loop = header_loop.replace("VAR_PATH","["+",".join(path_list)+"]")
        body = header_loop + body

        # Crear el directorio de salida para las imágenes
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Guardar las imágenes en el directorio de salida
        for key, img_data in resources['outputs'].items():
            # El nombre del archivo de la imagen
            filename = os.path.join(output_dir, key)

            # Escribir los datos de la imagen en un archivo
            with open(filename, 'wb') as img_file:
                img_file.write(img_data)

        # Guardar el cuerpo del Markdown en un archivo
        md_filename = os.path.join(output_dir, 'notebook.md')

        # find al lines with "image/png"
        lines = body.split("\n")
        #"![png](output_10_1.png)" -> https://localhost:8000/output_10_1.png

        newfolder = "/".join(path_list[:-1])

        for i in range(len(lines)):
            if "![png]" in lines[i]:
                lines[i] = lines[i].replace("![png](", "![png](/images/"+newfolder+"/")

        body = "\n".join(lines)
        with open(md_filename, 'w', encoding='utf-8') as md_file:
            md_file.write(body)

        # copy img to content/images
        newfolder = "/".join(path_list[:-1])
        newfolder = content_folder+"/images/"+newfolder
        # create folder recursively
        os.makedirs(newfolder, exist_ok=True)

        # if exists .png files, copy them
        png_files = glob.glob(output_dir+"/*.png")
        if len(png_files)>0:
            os.system("cp "+output_dir+"/*.png "+newfolder+"/.")
        # copy md to content
        name = notebook_path.split("/")[-1].replace(".ipynb","")
        folder = "/".join(notebook_path.split("/")[2:-1])
        newfolder = content_folder+"/notebook/"+folder
        os.makedirs(newfolder, exist_ok=True)
        os.system("cp "+md_filename+" "+newfolder+"/"+name+".md")

        # remove temp folder
    except:
        # remove 
        print("Error processing: "+notebook_path)
        error = True

    shutil.rmtree(output_dir, ignore_errors=True)

    return error
