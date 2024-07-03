from tools.doc.classdoc import classdoc
import os



def class2blog(var_class,content_folder):

    template = """Title: VAR_NAME
Date: 2010-12-03 10:20
Category: Class
Header: VAR_HEADER
Class: VAR_CLASS

VAR_CONTENT
"""
    doc = classdoc(var_class)


    #if content does not exist, create it
    # remove the file if it exists
    if os.path.exists(content_folder):
        os.system("rm -rf "+content_folder)
        
    os.makedirs(content_folder, exist_ok=True)
    template = template.replace("VAR_CLASS",var_class.__name__)
    for imethod in doc["methods"]:

        file = os.path.join(content_folder,imethod["name"]+".md")

        itemplate = template.replace("VAR_NAME",imethod["name"])
        itemplate = itemplate.replace("VAR_HEADER",imethod["header"])
        content = imethod["body"]
        # strip left 
        content = content.lstrip()
        # 
        inout_str = "<h5>Input</h5>\n\n"
        for input in imethod["inputs"]:
            inout_str += "* "+input["name"]+\
                        " | `type`: "+input["type"]+" \n"
        inout_str += "\n"

        inout_str += "<h5>Output</h5>\n"
        for output in imethod["outputs"]:
            inout_str += "* "+output["type"]+"\n"
        inout_str += "\n"

        content = inout_str + content
        itemplate = itemplate.replace("VAR_CONTENT",content)
        try:
            f = open(file,"w")
            f.write(itemplate)
            f.close()
        except:
            print("Error writing file: "+file)
            raise