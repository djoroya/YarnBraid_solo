import io
import sys

# La función lambda que has proporcionado
methods = lambda cls: [func for func in cls.__dict__ 
                       if callable(getattr(cls, func)) 
                       and not func.startswith("__")]

init    = lambda cls: [func for func in cls.__dict__
                          if  callable(getattr(cls, func)) 
                          and func.startswith("__init__")][0]

def helpstr(x):
    buffer = io.StringIO()
    # Guardar la referencia actual de stdout para restaurarla más tarde
    stdout_actual = sys.stdout
    # Redireccionar stdout al buffer
    sys.stdout = buffer

    # Llamar a help, que escribirá en el buffer
    help(x)

    # Restaurar la salida estándar original
    sys.stdout = stdout_actual
    r = buffer.getvalue()
    buffer.close()

    # Agregar el contenido del buffer a la lista
    return r
def classdoc(MiClase):

    docs = dict()
    docs["main"] = helpstr(MiClase)
    # split main by "Methods defined here:"
    docs["main"] = docs["main"].split("Methods defined here:")[0].replace("|", "")
    # split by \n
    docs["main"] = docs["main"].split("\n")[5:-2]
    # remove 5 first lines
    docs["main"] = "\n".join(docs["main"])

    # 
    docs["init"]  = helpstr(getattr(MiClase,init(MiClase)))
    #
    # from "***JSON***" to "***JSON***" cut
    docs["init"] = docs["init"].split("***JSON***")
    if len(docs["init"])>1:
        docs["init"] = docs["init"][1]
    methods_content = [ "\n".join(helpstr(getattr(MiClase, metodo)).split("\n")[2:])
                       for metodo in methods(MiClase)]
    
    ime_list = []
    for content in methods_content:
        ime = dict()

        ime["header"] = content.split("\n")[0]
        ime["name"] = ime["header"].split("(")[0]
        ime["body"] = "\n".join(content.split("\n")[1:])

        inputs = ime["header"].replace(")","").split("(")[1].split(",")
        inputs = [inp.strip() for inp in inputs]

        input_list = []
        for i in inputs[1:]:
            id = dict()
            mandatory = "=" in i
            name = i.split("=")[0]
            type = name.split(":")
            if len(type)>1:
                name = type[0]
                type = type[1]
            else:
                type = "Unknown"
            id["name"]  = name
            id["optional"] = mandatory
            id["type"] = type
            input_list.append(id)
        ime["inputs"] = input_list

        # outputs
        outputs = ime["header"].split("->")
        if len(outputs)>1:
            outputs = outputs[1].split(",")
            outputs = [out.strip() for out in outputs]
            output_list = []
            for o in outputs:
                od = dict()
                od["type"] = o
                output_list.append(od)
            ime["outputs"] = output_list
        else:
            ime["outputs"] = []
        ime_list.append(ime)
    docs["methods"] = ime_list
    # Devolver la lista de documentaciones
    return docs

