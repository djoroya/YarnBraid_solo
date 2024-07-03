from tools.calculix.inp.MaterialCard import *
def parse_material(name,content,cards,index):
    opts = name.split('=')
    name = opts[1]

    posible_cards = ['*ELASTIC','*EXPANSION',
                     '*CONDUCTIVITY',"*SPECIFICHEAT",
                     "*DENSITY"]

    for i in range(index+1,len(cards)):
        
        pc = False
        for iposi in posible_cards:
            if cards[i][0].startswith(iposi):
                pc = True
                break
        if not pc:
            break

    select_cards = cards[(index+1):(i+1)]
    select_cards = cards[(index+1):(i)]
    
    for i in range(len(select_cards)):
        select_cards[i][0] = select_cards[i][0].replace("\n","")
        select_cards[i][1] = select_cards[i][1].replace("\n","")

    implemented_cards = ["*ELASTIC","*DENSITY"]

    select_cards = [card for card in select_cards
                        if card[0].split(',')[0] in implemented_cards]
    
    new_cards = []
    for icard in select_cards:
        if icard[0].startswith('*ELASTIC'):
            E,nu = icard[1].split(',')
            E  = float(E)
            nu = float(nu)
            new_card = ElasticCard("ELASTIC",E,nu)
        elif icard[0].startswith('*DENSITY'):
            rho = float(icard[1])
            new_card = DensityCard("DENSITY",rho)
        new_cards.append(new_card)

    material_card = MaterialCard(name,new_cards)
    return material_card