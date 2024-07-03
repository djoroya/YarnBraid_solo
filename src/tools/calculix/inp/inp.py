from tools.calculix.inp.Card import *
import numpy  as np

from tools.calculix.inp.functions.init                   import init
from tools.calculix.inp.functions.merge                  import merge
from tools.calculix.inp.functions.reset_cards            import reset_cards
from tools.calculix.inp.functions.print                  import print
from tools.calculix.inp.functions.SetUniqueNodes         import SetUniqueNodes
from tools.calculix.inp.functions.CopyNset               import CopyNset
from tools.calculix.inp.functions.CreateTie              import CreateTie
from tools.calculix.inp.functions.select                 import *
from tools.calculix.inp.functions.CreatePBC_with_tie     import CreatePBC_with_tie
from tools.calculix.inp.functions.reset_index            import reset_index
from tools.calculix.inp.functions.addDisplFRD            import addDisplFRD
from tools.calculix.inp.functions.AddEquation            import AddEquation
from tools.calculix.inp.functions.FromElement2Nset       import FromElement2Nset
from tools.calculix.inp.functions.remove_by_type         import remove_by_type
from tools.calculix.inp.functions.addDisplacement        import addDisplacement
from tools.calculix.inp.functions.GetNodesElement        import GetNodesElement
from tools.calculix.inp.functions.FromElement2NsetClass  import FromElement2NsetClass
from tools.calculix.inp.functions.filter_by_type         import filter_by_type
from tools.calculix.inp.functions.remove_lib             import *
from tools.calculix.inp.functions.Nset2SurfNode          import Nset2SurfNode
from tools.calculix.inp.functions.FromId2Nset            import FromId2Nset
from tools.calculix.inp.functions.plots                  import *
from model.inflation.plane_svd import plane_svd
import pandas as pd

class inp:
    """ 
    This class is used to read and write inp files from calculix
    Also, it is used to manipulate the inp file and create new inp files
    """
    def __init__(self, 
                 file_name:str      ,
                 warning  :bool=True):
        """ 
        ***JSON***
        {"input":{
                    "file_name": " Name of the file to read. It must be a .inp file",
                    "warning"  : " If True, it will print warnings"
                 },
        "output":{
                    "self"     : " Object of the class inp"
                 }
        }
        ***JSON***
        """
        init(self,file_name,warning)
    # ===========================================
    def reset_cards(self):
        return reset_cards(self)
    # ===========================================
    def GetNodesElement(self,element):
        """  
        ***JSON***
        {"input":{
                    "element": " Element to get the nodes"
                 },
        "output":{
                    "nodes"  : " Nodes of the element"
                 }
        """
        return GetNodesElement(self,element)
    # ===========================================
    def plot(self,*args,**kwargs):
        plot(self,*args,**kwargs)
    # ===========================================
    def plot3D(self,ax,*args,**kwargs):
        plot3D(self,ax,*args,**kwargs)
    # ===========================================
    def filter_by_type(self,
                       dim,
                       replace:bool=False) -> list:
        return filter_by_type(self,dim,replace=replace)
    # ===========================================   
    def remove_by_type(self,dim):
        return remove_by_type(self,dim)
    # ===========================================        
    def last_node_id(self):
        return max(self.nodes.df.index)
    # ===========================================
    def last_element_id(self):
        all_el = [element.eid for element in self.elements]
        all_el = np.concatenate(all_el)
        return np.max(all_el)
    # ===========================================
    def reset_index(self,last_node_id,last_ele_id):
        return reset_index(self,last_node_id,last_ele_id)
    # ===========================================
    def merge(self,inp2,prefix=""):
        return merge(self,inp2,prefix)
    # ===========================================
    def print(self, file):
        print(self,file)
    # ===========================================
    def FromId2Nset(self,id_values_list,name=None):
        return FromId2Nset(self,id_values_list,name=name)
    # ===========================================
    def Nset2SurfNode(self,id_values_list,name=None):
        return Nset2SurfNode(self,id_values_list,name=name)
    # ===========================================
    def AddEquation(self,nset1,nset2,type_eq="point2point",dims=[1,2,3]):
        return AddEquation(self,nset1,nset2,type_eq=type_eq,dims=dims)
    # ===========================================
    def FromElement2Nset(self,index_el,name=None):
        return FromElement2Nset(self,index_el,name=name)
    # ===========================================
    def FromElement2NsetClass(self,element,name):
        return FromElement2NsetClass(self,element,name)
    # ===========================================
    def CreateTie(self,name,slave,master,type="surface"):
        return CreateTie(self,name,slave,master,type=type)
    # ===========================================    
    def SetUniqueNodes(inp_f):
        SetUniqueNodes(inp_f)
    # ===========================================
    def remove_nset(self,name):
        remove_nset(self,name)
    # ===========================================
    def remove_surface(self,name):
        remove_surface(self,name)
    # ===========================================
    def remove_surface_regex(self,regex):
        remove_surface_regex(self,regex)
    # ===========================================
    def remove_nset_regex(self,regex):
        remove_nset_regex(self,regex)
    # ===========================================
    def remove_tie(self,name):
        remove_tie(self,name)
    def remove_tie_regex(self,regex):
        remove_tie_regex(self,regex)
    # ===========================================
    def select(self,name,type):
        return select(self,name,type)
    # ===========================================
    def select_regex(self,regex,type):
        return select_regex(self,regex,type)
    # ===========================================
    def addDisplacement(self,vec):
        addDisplacement(self,vec)
    # ===========================================  
    def addDisplFRD(self,frd):
        return addDisplFRD(self,frd)
    # ===========================================    
    def CopyNset(self,nameset,nameset_copy,vec):
        return CopyNset(self,nameset,nameset_copy,vec)
    # ===========================================
    def CreatePBC_with_tie(self,tie_name,nset,surface,vec):
        CreatePBC_with_tie(self,tie_name,nset,surface,vec)
    # ===========================================
    # def AddSolidSection(self,name,material):
    #     AddSolidSection(self,name,material)
    def setResults(self,frd,onlyfrd=False):

        # ms = ['D1', 'D2', 'D3', 'SXX', 'SYY', 'SZZ', 'SXY', ...]
        ms = frd["data"].keys().values[4:]
        
        # nodes is a dataframe with the nodes and the results
        nodes = self.nodes.df.copy()
        if onlyfrd:
            indx_frd = frd["data"]["node"].values
            nodes = nodes.loc[indx_frd]
        # nodes has a [x, y, z] with index = nid
        # Add new columns to the nodes dataframe
        # ms = ['D1', 'D2', 'D3', 'SXX', 'SYY', 'SZZ', 'SXY', ...]
        for im in ms:
            nodes[im] = frd["data"][im]
            
        self.frd = nodes

        return nodes
    
    def scale(self,factor):
        self.nodes.df[["x","y","z"]] = self.nodes.df[["x","y","z"]]*factor
        return self
    
    def NsetProjection(self,bot_1_str,clone_top_4_str):

        bot_1       = self.select(bot_1_str      , "nset")
        clone_top_4 = self.select(clone_top_4_str, "nset")

        id_nodes = []
        id_nodes.extend(bot_1.id_nodes)
        id_nodes.extend(clone_top_4.id_nodes)

        df = self.nodes.df
        select_df = df.loc[id_nodes].copy()

        puntos_proyectados, _ = plane_svd(select_df.values)

        new_points_bot_1       = puntos_proyectados[:len(bot_1.id_nodes)]
        new_points_clone_top_4 = puntos_proyectados[len(bot_1.id_nodes):]

        # update nodes
        df.loc[bot_1.id_nodes] = new_points_bot_1
        df.loc[clone_top_4.id_nodes] = new_points_clone_top_4

    def CreateNsetCopy(inp_file,rep_nset,label,vec):
        nodes_df    = inp_file.nodes.df.loc[rep_nset.id_nodes]
        nodes_rep   = nodes_df.values.copy() + vec
        id_rep_old  = nodes_df.index.values.copy()
        last_id     = np.max(inp_file.nodes.df.index.values)
        id_rep      = id_rep_old + last_id
        # add type col 
        # create a df with the new nodes
        df_rep = pd.DataFrame(nodes_rep,columns=["x","y","z"])
        df_rep["nid"] = id_rep
        # set nid as index
        df_rep = df_rep.set_index("nid")

        inp_file.nodes.df = pd.concat([inp_file.nodes.df,df_rep])

        # create a nset with the new nodes
        inset_rep = inp_file.FromId2Nset(id_rep,label)
        
        return inset_rep
    
    def SetPrefix(inp2,prefix):
        for element in inp2.elements:
            element.name = element.name.replace("ELSET=", "ELSET="+prefix)
            element.options["ELSET"] = prefix+element.options["ELSET"]
            # nset

        for elsetofelset in inp2.elsetsofelsets:
            elsetofelset.name = prefix + elsetofelset.name 
            elsetofelset.name_up = prefix.upper() + elsetofelset.name_up
            for ide in range(len(elsetofelset.id_elements)):
                elsetofelset.id_elements[ide] = prefix + elsetofelset.id_elements[ide]

        cards_sets = [ inp2.elsets, 
                       inp2.nsets, 
                       inp2.surfaces, 
                       inp2.surface_interactions, 
                       inp2.ties, 
                       inp2.materials]
        
        for cards in cards_sets:
            for card in cards:
                card.name = prefix + card.name 
                card.name_up = prefix.upper() + card.name_up

