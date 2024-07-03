import json
import numpy as np
import pandas as pd
def savejson(diccionario, ruta_archivo):
    diccionario = diccionario.copy()
    # 
    # diccionario: diccionario a guardar
    assert isinstance(diccionario, dict), "El diccionario debe ser un diccionario de Python"
    # ruta_archivo: ruta del archivo JSON
    assert isinstance(ruta_archivo, str), "La ruta del archivo debe ser un string"
    
    # Convertir matrices de NumPy en listas
    # copy dictionary
    diccionario = numpytolist(diccionario)
    diccionario = pandastodict(diccionario)

    
    #comprobar que los valores son de tipo nativo no numpy
    for clave, valor in diccionario.items():
        if type(valor) == np.int64:
            diccionario[clave] = int(valor)


    # Guardar el diccionario en un archivo JSON
    with open(ruta_archivo, 'w') as archivo:
        # pretty print
        json.dump(diccionario, archivo, indent=4)

def loadjson_plain(ruta_archivo):
    # Cargar el diccionario desde el archivo JSON
    with open(ruta_archivo, 'r') as archivo:
        diccionario = json.load(archivo)
    return diccionario

def loadjson(ruta_archivo):
    # Cargar el diccionario desde el archivo JSON
    with open(ruta_archivo, 'r') as archivo:
        diccionario = json.load(archivo)
    
    # Convertir listas en matrices de NumPy
    diccionario = listtonumpy(diccionario)
    diccionario = dicttopandas(diccionario)
    return diccionario

def numpytolist(diccionario):
    diccionario = diccionario.copy()

    for clave, valor in diccionario.items():
        if isinstance(valor, np.ndarray):
            diccionario[clave] = valor.tolist()
        if isinstance(valor, dict): # if value is a dictionary
            diccionario[clave] = numpytolist(diccionario[clave])
        if isinstance(valor, list):
            # comprobar si es una lista de diccionarios
            bol = [isinstance(i,dict) for i in valor]
            bol = all(bol)
            if bol:
                for i in range(len(valor)):
                    valor[i] = numpytolist(valor[i])
            diccionario[clave] = valor
                    
    return diccionario

def pandastodict(diccionario):
    diccionario = diccionario.copy()

    for clave, valor in diccionario.items():
        if isinstance(valor, pd.DataFrame):
            keys   = valor.keys().tolist()
            values = valor.values.T.tolist()
            
            values = dict(zip(keys,values))
            values["pandas"] = None
            diccionario[clave] = values
        if isinstance(valor, dict): # if value is a dictionary
            diccionario[clave] = pandastodict(diccionario[clave])
    return diccionario

def dicttopandas(diccionario):
    diccionario = diccionario.copy()

    for clave, valor in diccionario.items():
        if isinstance(valor, dict):
            if "pandas" in valor.keys():
                valor.pop("pandas")
                valor = pd.DataFrame(valor)
                diccionario[clave] = valor
        if isinstance(valor, dict): # if value is a dictionary
            diccionario[clave] = dicttopandas(diccionario[clave])
    return diccionario

def listtonumpy(diccionario):
    diccionario = diccionario.copy()
    for clave, valor in diccionario.items():
        if isinstance(valor, list):
            try:
                diccionario[clave] = np.array(valor)
            except:
                # comprobar si es una lista de diccionarios
                bol = [isinstance(i,dict) for i in valor]
                bol = all(bol)
                if bol:
                    for i in range(len(valor)):
                        valor[i] = listtonumpy(valor[i])
                    diccionario[clave] = valor
                else:
                    print("Error en la clave: ", clave)
                    diccionario[clave] = valor
        if isinstance(valor, dict): # if value is a dictionary
            diccionario[clave] = listtonumpy(diccionario[clave])
            
    return diccionario