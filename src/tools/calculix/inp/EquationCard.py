from tools.calculix.inp.Card import Card

class EquationCard(Card):
    def __init__(self, name, nset1, nset2, type_eq="point2point", dims=[1,2,3]):
        super().__init__(name, name)

        self.nset1 = nset1
        self.nset2 = nset2
        self.type_eq = type_eq
        self.type = '*EQUATION'
        self.dims = dims


    def print(self):
        if self.type_eq == "point2point":
            return self.print_point()
        elif self.type_eq == "mean":
            return self.print_mean()
        
    def print_point(self):
        # print the nodes but only in row of 10
        line_eq = ""
        id_1 = self.nset1.id_nodes
        id_2 = self.nset2.id_nodes
        # comprobar que tienen el mismo numero de nodos
        if len(id_1) != len(id_2):
            print("ERROR: EquationCard:print_point: nset1 and nset2 have different number of nodes")
            return None
        for j,k in zip(id_1,id_2):
            for dim in self.dims:
                line_eq = line_eq +\
                      "2\n{} , {} , 1 , {} , {} , -1\n".format(j,dim,k,dim)


        return self.type + '\n' + line_eq 


    def print_mean(self):
        # print the nodes but only in row of 10
        id_1 = self.nset1.id_nodes
        id_2 = self.nset2.id_nodes
        nterm = len(id_1) + len(id_2)
        
        line_eq_total = ""
        for dim in self.dims:
            line_eq = "*EQUATION\n"+str(nterm) + '\n'
            for i1 in id_1:
                line_eq = line_eq + "{} , {} ,  {},\n".format(i1,dim,1/len(id_1))    
            for i2 in id_2:
                line_eq = line_eq + "{} , {} , -{},\n".format(i2,dim,1/len(id_2))
        # remove last comma
            line_eq = line_eq[:-2] + '\n'
            line_eq_total = line_eq_total + line_eq
        line_eq_total = line_eq_total[:-1]
        return line_eq_total
    
    def restart_index_nodes(self, id_node_start):
        self.id_nodes = self.id_nodes + id_node_start

        return self
