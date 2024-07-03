import numpy as np
import gmsh
import pandas as pd


def readmesh(file):
    lines = open(file).readlines()
    # find VOLUMEN1

    index_ast = [i for i, line in enumerate(lines) if line.startswith('*')]
    for i, line in enumerate(lines):
        if line.startswith('*NODE'):
            break

    i_in_index_ast = np.where(np.array(index_ast) > i)[0][0]
    nodes = lines[i+1:index_ast[i_in_index_ast]]
    nodes = [line.replace("\n","").split(',') for line in nodes]
    # first is int, next columns are float
    nodes = [ [float(x) for x in line] for line in nodes]
    nodes = np.array(nodes)
    id_nodes = nodes[:,0]
    # int
    id_nodes = id_nodes.astype(int)
    df_nodes = pd.DataFrame(nodes[:,1:], columns=['x', 'y', 'z'], index=id_nodes)

    for i, line in enumerate(lines):
        if 'ELSET=Volume1' in line:
            break
    lines = lines[i+1:]
    lines = [line.replace("\n","").split(',') for line in lines]

    lines = [ [int(x) for x in line] for line in lines]
    lines = np.array(lines)
    lines = lines[:,1:]


    def faces(tetra):
        f1 = np.array([tetra[0], tetra[1], tetra[2]])
        f2 = np.array([tetra[0], tetra[1], tetra[3]])
        f3 = np.array([tetra[0], tetra[2], tetra[3]])
        f4 = np.array([tetra[1], tetra[2], tetra[3]])
        return np.array([f1, f2, f3, f4])

    all_faces = []
    for t in lines:
        all_faces.extend(faces(t))
    all_faces = np.array(all_faces) -1 

    return df_nodes, all_faces


def traj2mesh(traj,rhilo,file='t19.inp'):
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.model.add("t19")
    gmsh.option.setNumber("Mesh.Algorithm",2  )  # Frontal-Delaunay for 2D meshes

    npts = traj.shape[0]
    # h = h*nturns
    p = []

    for i in range(0, npts):
        gmsh.model.occ.addPoint(traj[i,0], 
                                traj[i,1], 
                                traj[i,2], 
                                1, 
                                1000 + i)
        p.append(1000 + i)

    dr = np.diff(traj,axis=0)
    vec0 = dr[0]
    vec0 = vec0 / np.linalg.norm(vec0)

    gmsh.model.occ.addSpline(p, 1000)

    # A wire is like a curve loop, but open:
    gmsh.model.occ.addWire([1000], 1000)

    # We define the shape we would like to extrude along the spline (a disk):
    gmsh.model.occ.addDisk(traj[0,0], 
                            traj[0,1], 
                            traj[0,2], 
                            rhilo, 
                            rhilo, 
                            1000,
                            zAxis=vec0)

    # We extrude the disk along the spline to create a pipe (other sweeping types
    # can be specified; try e.g. 'Frenet' instead of 'DiscreteTrihedron'):
    gmsh.model.occ.addPipe([(2, 1000)], 1000, 'DiscreteTrihedron')
    gmsh.model.occ.synchronize()
    gmsh.model.mesh.setSize(gmsh.model.getEntities(0), 0.5*rhilo)
    gmsh.model.mesh.generate(3)
    gmsh.model.mesh.set_order(1)
    gmsh.write(file)
    gmsh.finalize()

    df_nodes,all_faces = readmesh(file)

    return df_nodes,all_faces