from simanneal import Annealer
import random
from model.multicopter import Multi
from model.vtol import Vtol

class VRP(Annealer):
    
    def __init__(self, state):
        self.possible_state = None
        super(VRP,self).__init__(state)
    
    def move(self):
        self.state.change()
        #return super().move()
    
    def energy(self):
        sum_BC = self.state.calcScore()
        
        return sum_BC