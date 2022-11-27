import math

class Node:

    def __init__(self,node_num,x,y,demand):
        self.node_num = node_num
        self.x = x
        self.y = y
        self.demand = demand
        self.previous = 0
    
    