import math

class Node:

    def __init__(self,node_num,x,y,demand):
        self.node_num = node_num
        self.x = x
        self.y = y
        self.demand = demand
    
    def distance(self,to_node):
        return math.sqrt((self.x - to_node.x)**2 + (self.y - to_node.y)**2)