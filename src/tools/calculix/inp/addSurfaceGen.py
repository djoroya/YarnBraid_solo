import numpy as np
from tools.calculix.inp.ElsetCard   import ElsetCard
from tools.calculix.inp.SurfaceCard import SurfaceCard

from tools.calculix.inp.tools.ComputeFaceOrder import ComputeFaceOrder, compute_faces

def addSurface(inp_f,element,nset,name):

    # En este caso tenemos 3 cartas *ELEMENT
    # debido a que el hilo se ha dividido en 3 partes
    # es necesario unirlas en una sola carta *ELEMENT
    # eliminamos las cartas *ELEMENT que ya no son necesarias
    # sus elementos se han unido en la primera carta *ELEMENT
    #
    select_elements = element.elements
    id_elements     = element.eid
    # Creamos una lista de caras para cada elemento
    element_faces = [compute_faces(select_elements[i])
                    for i in range(len(select_elements))]

    # Para cada elemento calculamos la cara que apunta hacia el exterior
    # si no tiene cara que apunte hacia el exterior, se devuelve None

    FaceOrder = [ ComputeFaceOrder(element_faces[i], 
                                   nset,
                                   select_elements[i]) 
                 for i in range(len(element_faces)) ]
    
    # Ordenamos los elementos por cara exterior
    index_Faces_4 = [  [  i for i, iFO in enumerate(FaceOrder) 
                          if iFO is not None
                          if j   in    iFO   ] 
                          for j in range(1, 5)]
    
    # Obtenemos los id de los elementos
    id_Faces_4 = [[id_elements[i] 
                   for i in index_Faces_4[j]] 
                   for j in range(4)]
    name = name.upper()
    # Creamos los elsets para cada cara
    elsets = [ElsetCard("ELSET_SURFACE_"+name+"_"+str(i+1), id_Faces_4[i])
            for i in range(4)]
    # Añadimos los elsets al archivo inp
    inp_f.cards = np.append(inp_f.cards, elsets)
    inp_f.reset_cards()

    # Creamos la superficie con los elsets  
    #  Es necesario que esten ordenados, 
    # Elset1 (Cara 1 hacia el exterior), 
    # Elset2 (Cara 2 hacia el exterior), etc
    isurface = SurfaceCard(name, elsets)
    inp_f.cards = np.append(inp_f.cards, isurface)
    inp_f.reset_cards()
    
