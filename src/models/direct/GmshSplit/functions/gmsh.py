
import numpy as np
import sys
import gmsh
from tools.calculix.inp.inp import inp
from models.direct.GmshSplit.functions.addpipe import addpipe
import pandas as pd
import os

join = os.path.join

# ===============================================================

def gmsh_mesh(trajs_gmsh,r0,params,debug=False):

    outfolder = params["output_folder"]
    
    dtraj = trajs_gmsh[1:] - trajs_gmsh[:-1]

    long = np.linalg.norm(dtraj, axis=1)
    long = np.insert(long, 0, 0)
    long = np.cumsum(long)

    gmsh.initialize(sys.argv)
    # algoriathm
    gmsh.option.setNumber("Mesh.Algorithm", 2)

    rd = r0




    nlen = len(trajs_gmsh)
    final =None
    disk = None

    list_index = np.arange(0,nlen-1,5)

    # list_index = list_index[:-1]
    
    list_index = list_index[:-1]
    # add nlen-1
    list_index = np.append(list_index,nlen-1)

    long = list_index[-1] - list_index[-2]
    if long < 7:
        # remove -2 element
        list_index = list_index[:-2]
        # add nlen-1
        list_index = np.append(list_index,nlen-1)
        long = list_index[-1] - list_index[-2]

    print("Size of last segment: ",long)
    iter = 0
    pipe_list = []
    for i in  list_index[:-1]:

        vec_z,disk,pipe = addpipe(trajs_gmsh[i:i+6],i*1000,iter,
                                            final=final,disk=disk,rd=rd)
       
        if debug:
            gmsh.fltk.run()
        if pipe is None:
            print("Error in pipe creation")
            if params["debug"]:
               gmsh.fltk.run()
            gmsh.finalize()

            raise ValueError("Error in pipe creation")
        
        # open gui 
            
        final = vec_z
        iter += 1
        pipe_list.append(pipe)


    last_circle_id = i*1000+4
    # 20004 curve to wire
    #creamos un circulo al final de la trajectoria alineado con el ultimo segmento

    point_center_last = i*1000+8
    point_xaxis_last  = i*1000+6
    #get positions 

    pos_center = gmsh.model.getValue(0,point_center_last,parametricCoord=[0])
    pos_xaxis = gmsh.model.getValue(0,point_xaxis_last,parametricCoord=[0])

    vec_x = -pos_xaxis +  pos_center

    last_points = trajs_gmsh[-1]
    last_vec = trajs_gmsh[-1] - trajs_gmsh[-2]
    diskid = gmsh.model.occ.addCircle(last_points[0],
                                    last_points[1],
                                    last_points[2],
                                    rd,
                                   2+last_circle_id,
                                   zAxis=last_vec,
                                   xAxis=vec_x)

    wiredistid = gmsh.model.occ.addCurveLoop([diskid],3+last_circle_id)

    gmsh.model.occ.addThruSections([last_circle_id,wiredistid],
                                -1,makeRuled=False,
                                makeSolid=True,
                                maxDegree=-1)


    gmsh.model.occ.synchronize()
    # gmsh.fltk.run()
    vols = gmsh.model.getEntities(3)
    iter = 0

    nvols = len(vols)
    # print("vols:",vols)
    # gmsh.fltk.run()
    for i in range(nvols):

        if len(vols) == 1:
            break
        gmsh.model.occ.fuse([vols[-1]],[vols[-2]], 
                            removeTool=True, 
                            removeObject=True)
        gmsh.model.occ.synchronize()
        vols = gmsh.model.getEntities(3)

        # if i % 5 == 0:
        #     print("iter: ",i," | vols:",vols)

    #open gui
    gmsh.model.occ.synchronize()

    # remesh

    # open gmsh GUI
    # gmsh.fltk.run()

    # nodes = gmsh.model.getEntities(0)
    # nodes = [i[1] for i in nodes]

    if debug:
        gmsh.fltk.run()
    
    # distance = np.array(distance)
    # inside = distance < 10
    # nodes = np.array(nodes)[inside].tolist()
    # nodes = [1,2,3,4,5,6,7]
    # print("=========")
    # print(nodes)
    #open gui 
    gmsh.model.geo.synchronize()

    params["MeshSizeMin"] = round(params["MeshSizeMin"],4)
    params["MeshSizeMax"] = round(params["MeshSizeMax"],4)
    # gmsh.fltk.run()
    # print("MinMesh : ",params["MeshSizeMin"])
    # print("MaxMesh : ",params["MeshSizeMax"])
    gmsh.option.setNumber('Mesh.MeshSizeMin', params["MeshSizeMin"])
    gmsh.option.setNumber('Mesh.MeshSizeMax', params["MeshSizeMax"])
    gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 100)
    gmsh.option.setNumber("Mesh.Optimize", 1)  # Optimizar la malla
    gmsh.option.setNumber("Mesh.OptimizeNetgen", 1)  # Utilizar Netgen para optimización

    #open gmsh GUI
    try:
        gmsh.model.mesh.generate(3)
    except:
        print("Error in mesh generation")
        if params["debug"]:
            gmsh.fltk.run()
        gmsh.finalize()
        raise ValueError("Error in mesh generation")

    gmsh.model.mesh.setOrder(2)

    vols = gmsh.model.getEntities(3)
    vols = [vol[1] for vol in vols]
    gmsh.model.mesh.setCompound(3,vols)

    gmsh.write(join(outfolder,"model.inp"))

    # gmsh.fltk.run()
    gmsh.finalize()
    print("Done")

    inp_file = join(outfolder,"model.inp")

    inp_obj = inp(inp_file)

    # remove 1d elements
    eid = inp_obj.elements[0].eid


    
    # Volumes
    # ===============================================================
    volumes = [ i for i in inp_obj.elements 
                  if i.options["TYPE"] == "C3D10"]


    df = pd.concat([i.df for i in volumes])
    eid = np.concatenate( [i.eid for i in volumes])
    elements = np.concatenate([i.elements for i in volumes])

    volumes[0].eid = eid
    volumes[0].df = df
    volumes[0].elements = elements
    volumes = volumes[0]
    # ===============================================================
    surfaces = [ i for i in inp_obj.elements 
                    if i.options["TYPE"] == "CPS6"]
    
    surfaces_len = [len(i.elements) for i in surfaces]

    max_len = max(surfaces_len)
    min_len = min(surfaces_len)
    mid_len = (max_len + min_len) // 2

    small = [i for i in surfaces if len(i.elements) < mid_len]

    start_point = trajs_gmsh[0]
    # 
    sm_points = [ ism.GetMassCenter(inp_obj.nodes) for ism in small]
    #search nearest point
    dist = [np.linalg.norm(start_point - i) for i in sm_points]

    idx = np.argmin(dist)

    bot = small[idx]
    bot.options["ELSET"] = "BOT"

    end_point = trajs_gmsh[-1]
    #
    sm_points = [ ism.GetMassCenter(inp_obj.nodes) for ism in small]
    #search nearest point
    dist = [np.linalg.norm(end_point - i) for i in sm_points]

    idx = np.argmin(dist)

    top = small[idx]
    top.options["ELSET"] = "TOP"

    diameters = [ isurf.GetDiameter(inp_obj.nodes) for isurf in surfaces]
    diameters = np.array(diameters)

    errors = 100*(diameters -  r0)/r0
    errors = np.abs(errors)

    bigs = [i for i,j in zip(surfaces,errors) if j >= 5]


    df = pd.concat([i.df for i in bigs])
    eid = np.concatenate( [i.eid for i in bigs])
    elements = np.concatenate([i.elements for i in bigs])

    bigs[0].eid = eid
    bigs[0].df = df
    bigs[0].elements = elements
    bigs[0].options["ELSET"] = "SURFACE"

    bigs = bigs[0]


    # =========
    # 
    eid_final = np.concatenate([bigs.eid,top.eid,bot.eid])
    df_final = pd.concat([bigs.df,top.df,bot.df])
    elements_final = np.concatenate([bigs.elements,top.elements,bot.elements])

    final_surfaces = bigs
    final_surfaces.eid = eid_final
    final_surfaces.df = df_final
    final_surfaces.elements = elements_final
    # 
    #     
    inp_obj.cards = inp_obj.cards[0:2].tolist() +  [volumes] + [final_surfaces]

    inp_obj.reset_cards()

    return inp_obj,list_index

