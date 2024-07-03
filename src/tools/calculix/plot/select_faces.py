import numpy as np

def el2face(el,nface=None):
    face_1 = el[[0,1,2]]
    face_2 = el[[0,3,1]]
    face_3 = el[[1,3,2]]
    face_4 = el[[2,3,0]]

    faces = [face_1,face_2,face_3,face_4]
    if nface is not None:
        return [faces[nface]]
    return faces

def select_faces(inp_obj,surf,elem,
                 nodes=None): 
    """   
    Inputs:
    -------
    * inp_obj: object of class Inp
    * surf: object of class Surface
    * elem: object of class Element
    * nodes: object of dataframe nid,x,y,z
    """
    if nodes is None:
        nodes = inp_obj.nodes.df

    nodes = nodes.copy()
    nodes["real_index"] = np.arange(0,len(nodes))

    all_faces = []
    for k in range(4):

        ide     = surf.elsets[k].id_elements
        el_data = elem.df.loc[ide]
        
        el_data = el_data[[0,1,2,3]]

        el_data_real_index = [ nodes.loc[el_data.iloc[i].values].real_index.values 
                               for i in range(len(el_data))]

        for i in range(len(el_data_real_index)):
            faces = el2face(el_data_real_index[i],nface=k)
            all_faces.extend(faces)

    return all_faces