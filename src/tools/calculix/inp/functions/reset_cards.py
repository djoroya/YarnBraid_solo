
def reset_cards(self):
    self.nodes = [
                card for card in self.cards 
                if card.type == '*NODE']
    # create a new nodecard with all nodes
    assert len(self.nodes) > 0, "At least one node card is required"
    #assert len(self.nodes) == 1, "There must be only one node card"
    self.nodes = self.nodes[0]

    self.elements = [card for card in self.cards 
                        if card.type == '*ELEMENT']
    
    self.nsets    = [card for card in self.cards 
                        if card.type == '*NSET']
    
    self.elsets   = [card for card in self.cards 
                        if card.type == '*ELSET']
    
    self.elsetsofelsets = [card for card in self.cards
                        if card.type == '*ELSETOFELSET']
    
    self.surfaces = [card for card in self.cards 
                        if card.type == '*SURFACE']
    
    self.ties     = [card for card in self.cards
                        if card.type == '*TIE']
    
    self.equations = [card for card in self.cards
                        if card.type == '*EQUATION']
    
    self.surface_interactions= [card for card in self.cards
                        if card.type == '*SURFACEINTERACTION']
    
    self.contacts = [card for card in self.cards
                        if card.type == '*CONTACTPAIR']
    
    self.materials = [card for card in self.cards
                        if card.type == '*MATERIAL']
    
    self.solid_sections = [card for card in self.cards
                        if card.type == '*SOLIDSECTION']
    
    return self