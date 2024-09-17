import numpy as np
from scipy.interpolate import NearestNDInterpolator
from models.direct.postDirect.is_fcn.mesh import mesh
from models.direct.postDirect.is_fcn.remesh_step import remesh_step
from tqdm import tqdm

def interp_section(ifrd_data,nsets,ndisk=10):
    
    # =====================================
    # Construir lista de nodos de cada hilo
    yarns_nodes = []
    nyarns = len([ inset for inset in nsets.keys() if "YARN_" in inset ])

    for i in range(nyarns):
        id_nodes = nsets["YARN_"+str(i+1)]
        id_nodes = np.unique(id_nodes)
        yarns_nodes.append(id_nodes)
    # =====================================
    yarns = []

    print("Interpolating section")
    for id_yarn in tqdm(range(nyarns)):

        id_nodes = yarns_nodes[id_yarn]

        fvalues = ifrd_data.loc[id_nodes]["P1"].values # Von Mises stress or P1
        xvalues = ifrd_data.loc[id_nodes]["x"].values
        yvalues = ifrd_data.loc[id_nodes]["y"].values
        zvalues = ifrd_data.loc[id_nodes]["z"].values
        # sort by z 

        interp = NearestNDInterpolator(list(zip(xvalues, yvalues, zvalues)),
                                        fvalues)
        if id_yarn == 0:
            prefix = ""
        else:
            prefix = "P"+str(id_yarn+1)+"_"
        id_n = nsets[prefix+"ESQUELETO_"+str(id_yarn+1)]
        r = ifrd_data.loc[id_n][["x","y","z"]]
        # sort by z
        r = r.sort_values(by=["z"])
        r = remesh_step(r.values,0.2)
        dr = r[1:] - r[:-1]

        dr_list = np.linspace(0,len(dr)-1,ndisk).astype(int)
        # if last element is not in dr_list

        disks = []
        for idr in dr_list:
            # norm
            vector_direccion =  dr[idr]
            translate        =  r[idr]
            X_trans, Y_trans, Z_trans,nan_mt = mesh(vector_direccion,translate,size=0.5)
            
            f = interp(X_trans,Y_trans,Z_trans)
            f = f*nan_mt

            disk = dict()
            disk["values"] = f
            disk["X"] = X_trans
            disk["Y"] = Y_trans
            disk["Z"] = Z_trans

            disk["f"] = f
            disk["center"] = translate
            f_no_nan = f[~np.isnan(f)]
            disk["mean"] = np.mean(f_no_nan)
            disks.append(disk)

        yarn = dict()
        yarn["disks"] = disks
        yarn["esq"] = r
        yarn["x"] = xvalues
        yarn["y"] = yvalues
        yarn["z"] = zvalues
        yarn["f"]  = fvalues 
        yarn["dr"] = dr
        yarns.append(yarn)
        
    
    return yarns