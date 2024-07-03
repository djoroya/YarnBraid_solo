from tools.basic.loadsavejson     import loadjson
import os,gmsh
from tools.step.runstep          import runstep
from tqdm                   import tqdm
@runstep
def RunGmsh(params,output_folder):
    
    # full path
    output_folder = params["output_folder"]
    
    lsdyna_path = os.path.join(params["lsdyna_path"],"params.json")
    lsdyna_params = loadjson(lsdyna_path)

    folder = lsdyna_params["output_folder"]
    root   = lsdyna_params["root_folder"]
    folder = os.path.join(root,folder)
    #find step files
    files = os.listdir(folder)
    files = [f for f in files if f.endswith('.step')]

    if params["size_element"] is None:
        params["size_element"] = 1.2*lsdyna_params["radius"]
        if params["factor"] is not None:
            params["size_element"] = params["factor"]*params["size_element"]
        
    gmsh.initialize()
    #verbose off
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.option.setNumber("Mesh.Algorithm",params["Algorithm"]) 

    fcn = tqdm if params["verbose"] else lambda x: x

    for j,i in fcn(enumerate(range(1, len(files)+1))):

        gmsh.model.add("modelo_1")
        out_step = "out{}.step".format(i)
        out_step = os.path.join(folder,out_step)
        gmsh.merge(out_step)

        gmsh.model.occ.synchronize()

        dx = params["size_element"] 

        gmsh.model.mesh.setSize(gmsh.model.getEntities(), dx)
        gmsh.model.mesh.generate(3)
        gmsh.model.mesh.set_order(2)

        gmsh.model.mesh.setCompound(3, [1, 2, 3])
        gmsh.model.mesh.set_compound(3, [1, 2, 3])

        out_inp = "out{}.inp".format(j+1)
        file = os.path.join(output_folder,out_inp)
        gmsh.write(file)
        
        gmsh.fltk.finalize()
        

    return params