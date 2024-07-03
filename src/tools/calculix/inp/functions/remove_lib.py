from tools.calculix.inp.SurfaceCard import SurfaceCard
from tools.calculix.inp.SurfaceNode import SurfaceNodeCard
from tools.calculix.inp.NsetCard import NsetCard
from tools.calculix.inp.TieCard import TieCard
import re

# ===========================================
def remove_nset(self,name):
    def select(card):
        if isinstance(card,NsetCard):
            if card.name == name:
                return False
        return True
    self.cards = [card for card in self.cards 
                    if select(card)]
    self.reset_cards()
# ===========================================

def remove_surface(self,name):
    def select(card):
        if isinstance(card,SurfaceCard) or isinstance(card,SurfaceNodeCard):
            if card.name == name:
                return False
        return True
    self.cards = [card for card in self.cards 
                    if select(card)]
    self.reset_cards()
# ===========================================

def remove_surface_regex(self,regex):
    
    def select(card):
        if isinstance(card,SurfaceCard) or isinstance(card,SurfaceNodeCard):
            if re.fullmatch(regex,card.name):
                return False
        return True
    self.cards = [card for card in self.cards 
                    if select(card)]
    self.reset_cards()
# ===========================================

def remove_nset_regex(self,regex):
    self.cards = [card for card in self.cards 
                    if not re.fullmatch(regex,card.name)]
    self.reset_cards()
# ==========================================

def remove_tie(self,name):
    
    def select(card):
        if isinstance(card,TieCard):
            if card.name == name:
                return False
        return True
    self.cards = [card for card in self.cards 
                    if select(card)]
    self.reset_cards()

def remove_tie_regex(self,regex):
    def select(card):
        if isinstance(card,TieCard):
            if re.fullmatch(regex,card.name):
                return False
        return True
    self.cards = [card for card in self.cards 
                    if select(card)]
    self.reset_cards()