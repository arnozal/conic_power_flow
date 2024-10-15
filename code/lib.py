# Importing required libraries
import numpy as np



class grid:
    def __init__(self, nodes, lines, pros):
        self.nodes = self.add_nodes(nodes)                                      
        self.lines = self.add_lines(lines, self.nodes)  
        self.pros = self.add_pros(pros, self.nodes)  
                
    def add_nodes(self, nodes):
        nodes_list = list()
        for item in nodes:
            nodes_list.append(node(item['id'], item['slack']))
        return nodes_list
        
    def add_lines(self, lines, nodes):
        lines_list = list()
        for item in lines:
            lines_list.append(line(item['id'], item['From'], item['To'], item['R'], item['X'], nodes))
        return lines_list
        
    def add_pros(self, pros, nodes):
        pros_list = list()
        for item in pros:
            pros_list.append(prosumer(item['id'], item['Node'], item['P'], item['Q'], nodes))
        return pros_list

class node:
    def __init__(self, ref, slack):
        self.ref = ref   
        self.slack = slack        
        self.lines = list()
        self.pros = []
    
        
class line:
    def __init__(self, ref, From, To, R, X, nodes_list):
        self.ref = ref     
        self.Z = complex(R, X)
        self.G, self.B = np.real(1/self.Z), -np.imag(1/self.Z)
        self.Y = 1/self.Z
        self.nodes = [next((item for item in nodes_list if item.ref == From), None), 
                      next((item for item in nodes_list if item.ref == To), None)]   
        self.nodes[0].lines.append(self)
        self.nodes[1].lines.append(self)
  
class prosumer:
    def __init__(self, ref, node_id, P, Q, nodes_list):
        self.ref = ref
        self.P = P
        self.Q = Q        
        self.node = next((item for item in nodes_list if item.ref == node_id), None)
        self.node.pros.append(self)
        
        
        
        
        
        
        
        
        
        
    