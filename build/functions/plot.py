import numpy as np
from tools.calculix.inp.inp import inp
from tools.calculix.plot.select_faces import select_faces
import plotly.graph_objects as go
def plot(frd,inp_path,plot=False):
    
    inpf  = inp(inp_path)
    # select nodes only is this nodes ids are in frd file
    # When the displacements is zero, the nodes are not in the frd file
    # In this model, we use the ghost nodes to calculate fix the bondary conditions
    # in INP files, this nodes exist but the displacements are zero, so we need to select only the nodes that are in the frd file
    nodes = inpf.setResults(frd,onlyfrd=True)
    # select faces of surfaces
    all_faces = []
    surfaces= inpf.select_regex(".*SURFACE.*","surface")
    surfaces = [ isurf for isurf in surfaces if not "REP" in isurf.name]
    for h in range(8):
        surf = surfaces[h] 
        elem = inpf.elements[h]

        all_faces_surf = select_faces(inpf,surf,elem,nodes=nodes)

        all_faces.extend(all_faces_surf)

    xD = nodes.values[:,0] + nodes["D1"].values
    yD = nodes.values[:,1] + nodes["D2"].values
    zD = nodes.values[:,2] + nodes["D3"].values

    xi = nodes.values[:,0]
    yi = nodes.values[:,1]
    zi = nodes.values[:,2]
    # 
    if np.sum(np.isnan(xD))>0:
        print("xD has nan")
        raise Exception("xD has nan")
    #
    ivalues = [ face[0] for face in all_faces]
    jvalues = [ face[1] for face in all_faces]
    kvalues = [ face[2] for face in all_faces]

    magnitud =nodes["P1"].values

    if plot:
        fig = go.Figure(data=[
        go.Mesh3d(
            x=xD, # x-coordinates of vertices
            y=yD, # y-coordinates of vertices
            z=zD, # z-coordinates of vertices
            # i, j and k give the vertices of triangles
            # here we represent the 4 triangles of the tetrahedron surface
            i=ivalues,
            j=jvalues,
            k=kvalues,
            intensity=magnitud, # the color is given by the z value
            name='y',
            showscale=True,
            colorscale='Jet'
        )
    ])

        # fig size 
        fig.update_layout(width=700, height=700)
        # aspect ratio
        fig.update_layout(scene_aspectmode='data')
        # zoom out 
        fig.show()

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
        "magnitud": magnitud.tolist()
    }
    return r