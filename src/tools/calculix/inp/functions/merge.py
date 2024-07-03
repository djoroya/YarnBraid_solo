import numpy as np
import pandas as pd
def merge(inp1,inp2,prefix=""):
    # merge two inps
    # get the last node id of inp1
    last_node_id = inp1.last_node_id()
    # add the last node id to inp2
    last_ele_id = inp1.last_element_id()
    inp2.nodes.df.index += last_node_id

    # reset elements id
    inp2 = inp2.reset_index(last_node_id,last_ele_id)
    # all name of elements  in inp2 must be changed to prefix
    for element in inp2.elements:
        element.name = element.name.replace("ELSET=", "ELSET="+prefix)
        element.options["ELSET"] = prefix+element.options["ELSET"]
        # nset
    for elset in inp2.elsets:
        elset.name = prefix + elset.name 
        elset.name_up = prefix.upper() + elset.name_up

    for elsetofelset in inp2.elsetsofelsets:
        elsetofelset.name = prefix + elsetofelset.name 
        elsetofelset.name_up = prefix.upper() + elsetofelset.name_up
        for ide in range(len(elsetofelset.id_elements)):
            elsetofelset.id_elements[ide] = prefix + elsetofelset.id_elements[ide]

    for nset in inp2.nsets:
        nset.name = prefix + nset.name 
        nset.name_up =  prefix.upper() + nset.name_up 

    for surf in inp2.surfaces:
        surf.name = prefix + surf.name 
        surf.name_up =  prefix.upper() + surf.name_up 
        
    for interaction in inp2.surface_interactions:
        interaction.name = prefix +interaction.name 
        interaction.name_up = prefix.upper() + interaction.name_up 

    for tie in inp2.ties:
        tie.name = prefix + tie.name 
        tie.name_up = prefix.upper() + tie.name_up

    for material in inp2.materials:
        material.name = prefix + material.name 
        material.name_up = prefix.upper() + material.name_up
    # add the nodes of inp2 to inp1
    inp1.nodes.df = pd.concat([inp1.nodes.df,inp2.nodes.df])

    # add the elements of inp2 to inp1
    #inp1.elements = np.append(inp1.elements,inp2.elements)
    # add the cards of inp2 to inp1
    # remove nodeCard of inp2
    inp2.cards = [card for card in inp2.cards 
                    if card.type != '*NODE']
    inp2.cards = [card for card in inp2.cards 
                    if card.type != 'None']

    inp1.cards = np.append(inp1.cards,inp2.cards)
    inp1 = inp1.reset_cards()
    return inp1