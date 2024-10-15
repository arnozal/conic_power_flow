# Importing required libraries
import numpy as np



class grid:
    def __init__(self, nodes, lines):
        self.nodes = self.add_nodes(nodes)                                      
        self.lines = self.add_lines(lines, self.nodes)        
                
    def add_nodes(self, nodes):
        nodes_list = list()
        for item in nodes:
            nodes_list.append(node(item['id'], item['slack'], item['S'], item['fdp']))
        return nodes_list
        
    def add_lines(self, lines, nodes):
        lines_list = list()
        for item in lines:
            lines_list.append(line(item['id'], item['From'], item['To'], item['R'], item['X'], item['Long'], nodes))
        return lines_list

class node:
    def __init__(self, ref, slack, S, fdp):
        self.ref = ref   
        self.slack = slack        
        self.lines = list()
        
    def check(self, currents = 0):
        Ilines = 0
        for line in self.lines:
            if line.nodes[0] == self:
                Ilines += line.I
            else:
                Ilines -= line.I
        Iloads = - complex(self.P, - self.Q)/np.conjugate(self.U) + currents
        return Ilines + Iloads 
    
        
class line:
    def __init__(self, ref, From, To, R, X, long, nodes_list):
        self.ref = ref     
        self.Z = complex(R, X)*long  
        self.G, self.B = np.real(1/self.Z), -np.imag(1/self.Z)
        self.Y = 1/self.Z
        self.nodes = [next((item for item in nodes_list if item.ref == From), None), 
                      next((item for item in nodes_list if item.ref == To), None)]   
        self.nodes[0].lines.append(self)
        self.nodes[1].lines.append(self)
        
    def check(self):
        res = self.Z*self.I - (self.nodes[0].U - self.nodes[1].U)
        res = self.I - self.Y*(self.nodes[0].U - self.nodes[1].U) 
        return res
  
        
        
        
        
        
        
        
        
        
        
        
        
        
    