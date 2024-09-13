import numpy as np
from tools.calculix.inp.inp import inp
from tools.calculix.plot.select_faces import select_faces
from tools.calculix.frd.readfrd import readfrd

def frd2json(frd_path,inp_path):
    
    frd = readfrd(frd_path)
    inpf  = inp(inp_path)
    # select nodes only is this nodes ids are in frd file
    # When the displacements is zero, the nodes are not in the frd file
    # In this model, we use the ghost nodes to calculate fix the bondary conditions
    # in INP files, this nodes exist but the displacements are zero, so we need to select only the nodes that are in the frd file
    nodes = inpf.setResults(frd,onlyfrd=True)
    # select faces of surfaces
    all_faces = []
    all_faces_list = []
    surfaces= inpf.select_regex(".*SURFACE.*","surface")
    surfaces = [ isurf for isurf in surfaces if not "REP" in isurf.name]
    for h in range(64):
        surf = surfaces[h] 
        elem = inpf.elements[h]

        all_faces_surf = select_faces(inpf,surf,elem,nodes=nodes)

        all_faces.extend(all_faces_surf)
        all_faces_list.append(all_faces_surf)

    xD = nodes.values[:,0] + nodes["D1"].values
    yD = nodes.values[:,1] + nodes["D2"].values
    zD = nodes.values[:,2] + nodes["D3"].values

    xi = nodes.values[:,0]
    yi = nodes.values[:,1]
    zi = nodes.values[:,2]
    #
    ivalues = [ face[0] for face in all_faces]
    jvalues = [ face[1] for face in all_faces]
    kvalues = [ face[2] for face in all_faces]

    ivalues_list = []
    jvalues_list = []
    kvalues_list = []

    for all_faces_surf in all_faces_list:
        all_faces_surf = np.array(all_faces_surf).tolist()
        ivalues_list.append([ face[0] for face in all_faces_surf])
        jvalues_list.append([ face[1] for face in all_faces_surf])
        kvalues_list.append([ face[2] for face in all_faces_surf])

    magnitud =nodes["P1"].values


    # round values
    xD = np.round(xD,4)
    yD = np.round(yD,4)
    zD = np.round(zD,4)
    magnitud = np.round(magnitud,4)


    r = {
        "x": xD.tolist(),
        "y": yD.tolist(),
        "z": zD.tolist(),
        "xi": xi.tolist(),
        "yi": yi.tolist(),
        "zi": zi.tolist(),
        "i": np.array(ivalues).tolist(),
        "j": np.array(jvalues).tolist(),
        "k": np.array(kvalues).tolist(),
        "magnitud": magnitud.tolist(),
        "i_list": ivalues_list,
        "j_list": jvalues_list,
        "k_list": kvalues_list
    }
    return r