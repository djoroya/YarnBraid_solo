from tools.calculix.inp.Card import Card

class ContactCard (Card):
    def __init__(self, name, SurfaceInteraction, slave,master):
        super().__init__(name, name)

        self.master = master
        self.slave  = slave
        self.SurfaceInteraction = SurfaceInteraction
        self.type = '*CONTACTPAIR'

    def print(self):
        # print the nodes but only in row of 10
        return  '*CONTACT PAIR, INTERACTION=' +\
               self.SurfaceInteraction.name_up + \
                ',TYPE=SURFACE TO SURFACE\n' +\
               self.slave.name_up + ', ' + self.master.name_up + '\n' 


