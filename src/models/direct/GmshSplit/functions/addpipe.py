
import gmsh
def addpipe(trajs_gmsh,id,iter,final=False,disk=None,type_sweep="DiscreteTrihedron",rd=0.5):

    npts = len(trajs_gmsh)

    for i in range(npts):
        gmsh.model.occ.addPoint(trajs_gmsh[i][0], 
                                trajs_gmsh[i][1], 
                                trajs_gmsh[i][2], rd, i+1+id)


    list_points = [i+1+id for i in range(npts)]
    gmsh.model.occ.addSpline(list_points, 1 + id)
    gmsh.model.occ.addWire([1 + id], 1 + id)

    if final:
        vecz = final
    else:
        vecz = [trajs_gmsh[1][0] - trajs_gmsh[0][0], 
                trajs_gmsh[1][1] - trajs_gmsh[0][1], 
                trajs_gmsh[1][2] - trajs_gmsh[0][2]]
        # vecz = vecz/np.linalg.norm(vecz)
    

    vecz_final = [trajs_gmsh[-1][0] - trajs_gmsh[-2][0],
                trajs_gmsh[-1][1] - trajs_gmsh[-2][1],
                trajs_gmsh[-1][2] - trajs_gmsh[-2][2]]
    
    # vecz_final = trajs_gmsh[-1] - trajs_gmsh[-2]
    # vecz_final = vecz_final/np.linalg.norm(vecz_final)
    
    # points init 
    if final is None:

        disk = gmsh.model.occ.addDisk(trajs_gmsh[0][0],
                                        trajs_gmsh[0][1], 
                                        trajs_gmsh[0][2], 
                            rd, rd, 2+id,zAxis=vecz)

        gmsh.model.occ.synchronize()
        try:
            pipe= gmsh.model.occ.addPipe([(2, 2+id)], 
                                        1+id, type_sweep)
        except:
            print("Error in pipe creation")
            print("iter: ",iter)
            pipe = None
    else:
        try:
            pipe = gmsh.model.occ.addPipe([(2, 5+(iter-1)*3)], 
                                    1+id, type_sweep)
        except:
            print("Error in pipe creation")
            print("iter: ",iter)
            pipe = None
            raise ValueError("Error in pipe creation")


        gmsh.model.occ.remove([(2, 5+(iter-1)*3)])
    
        gmsh.model.occ.synchronize()

    return vecz_final,disk,pipe
