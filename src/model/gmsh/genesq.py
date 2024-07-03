import numpy as np
from scipy.spatial.distance import cdist

def genesq(inp_files,df,radius=0.2):
    # ===============================================================
    for j in range(len(inp_files)):
        nodes = inp_files[j].nodes.df
        nodes = inp_files[j].elements[0].GetUniqueNodes(inp_files[j].nodes)
        id_nodes = nodes.index.values
        values   = nodes.values
        trajs = df[j][["xu","yu","zu"]].values
        # refine the trajs
        #
        old_span = np.arange(0,trajs.shape[0])
        new_span = np.linspace(0,trajs.shape[0]-1,500)
        #
        trajs = np.array([np.interp(new_span,old_span,trajs[:,i]) 
                          for i in range(trajs.shape[1])]).T
        # nos quedamos con los nodos que estan mas cerca de la trajetoria 
        # (th aprox 0.1*radius)
        # usando cdist
        distances = cdist(trajs,values)
        #
        dista_value = np.min(distances,axis=1)
        arg_value   = np.argmin(distances,axis=1)
        # aunque sea el minimo, este esta muy lejos
        arg_value = arg_value[dista_value<(radius*0.25)]
        id_nodes = id_nodes[arg_value]
        #
        id_nodes = np.unique(id_nodes)

        # remove id_nodes that are in bot and top
        id_nodes = id_nodes[1:-1]

        inp_files[j].FromId2Nset(id_nodes,"esqueleto_"+str(j+1))