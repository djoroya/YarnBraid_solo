from tools.calculix.inp.Card import Card
import numpy  as np
class NsetCard (Card):
    def __init__(self, name, id_nodes):
        super().__init__(name, id_nodes)

        self.id_nodes = id_nodes
        self.type = '*NSET'

    def radius(self,nodes):
        # * Input:
        #   - nodes: NodeCard
        # Se calcula el radio de un circulo que contenga 
        # todos los nodos
        nodes_df = nodes.df.loc[self.id_nodes]
        center   = nodes_df.mean(axis=0)
        d2center = np.linalg.norm(nodes_df.values -\
                                        center.values,
                                        axis=1)
        radius = np.max(d2center)
        return radius
    def print(self):
        # print the nodes but only in row of 10
        line = ''
        for i, node in enumerate(self.id_nodes):
            line += str(node) + ','
            if i % 10 == 0 and i != 0:
                line += '\n'
        line = line[:-1]
        name_up = self.name_up.replace("\n", "")
        return self.type + ', NSET=' + name_up + '\n' + line 

    def GetNodes(self,nodes):
        return nodes.df.loc[self.id_nodes]

    def restart_index_nodes(self, id_node_start):
        self.id_nodes = self.id_nodes + id_node_start

        return self
