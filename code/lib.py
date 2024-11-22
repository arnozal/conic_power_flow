# Importing required libraries
import numpy as np
from scipy.optimize import minimize, NonlinearConstraint, LinearConstraint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata


class grid:
    def __init__(self, nodes, lines, pros):
        self.nodes = self.add_nodes(nodes)                                      
        self.lines = self.add_lines(lines, self.nodes)  
        self.pros = self.add_pros(pros, self.nodes)  
        self.n = len(self.nodes)
        self.m = len(self.lines)
        self.x_size = self.n+(2*self.m)-1
        self.obtain_index()
        
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
    
    def obtain_index(self):
        
        n_aux = 0
        while n_aux < self.n:
            self.nodes[n_aux].index = n_aux -1
            n_aux += 1
        
        n_aux2 = 0    
        while n_aux2 < self.m:   
            self.lines[n_aux2].index.append(n_aux - 1)
            n_aux += 1
            n_aux2 += 1
        
        n_aux3 = 0    
        while n_aux3 < self.m:   
            self.lines[n_aux3].index.append(n_aux - 1)
            n_aux += 1
            n_aux3 += 1   
    
        self.X = np.zeros(self.x_size)
        self.X[:self.n - 1] = 1
        
    def obtain_A(self):
        
        matrizA = np.zeros(((2*self.n)-2, (self.n+2*self.m)-1), dtype=float)
        
        n_aux = 0
        for i, node in enumerate(self.nodes[1:]):
            matrizA[2*i, n_aux] = np.sum([line.G for line in node.lines])
            matrizA[2*i+1, n_aux] = np.sum([line.B for line in node.lines])
            n_aux += 1
            
            for j, line in enumerate(node.lines):
                if node == line.nodes[0]:
                    matrizA[2*i, line.index[0]] = -line.G
                    matrizA[2*i, line.index[1]] = -line.B
                    matrizA[2*i+1, line.index[0]] = -line.B
                    matrizA[2*i+1, line.index[1]] = line.G
                else:
                    matrizA[2*i, line.index[0]] = -line.G
                    matrizA[2*i, line.index[1]] = line.B
                    matrizA[2*i+1, line.index[0]] = -line.B
                    matrizA[2*i+1, line.index[1]] = -line.G            
        self.A = matrizA
        
    def ineq(self, X):
        
        rest = []
        for line in self.lines:
            rest.append(line.ineq(X))
          
        return rest
    
    def intensity(self):
        intens = []
        for line in self.lines:
            intens.append(line.intensity())
        return intens    
    
    def intensity_pros(self):
        intens_pros = []
        for pros in self.pros:
            intens_pros.append(pros.intensity()) 
        return intens_pros    
    
    def comprobacion_Kirchhoff(self, tolerancia = 1e-2):
        Check = []
        for node in self.nodes[1:]:
            total_intens = 0 + 0j
            for line in node.lines:
                if line.nodes[0] == node:
                    total_intens -= line.intensity()  #Sale intensidad del nodo
                elif line.nodes[1] == node:
                    total_intens += line.intensity()  #Entra intensidad al nodo   
            for pros in node.pros:
                total_intens += pros.intensity() 
            if abs(total_intens) < tolerancia:
                Check.append(True)
            else: 
                Check.append(total_intens) 
        return Check       
                
        
    
    def solve_pf(self):
        
        self.obtain_A()
        self.obtain_B()
        self.obtain_f()
        
        
        lc = LinearConstraint(self.A, self.B, self.B)
        nlc = NonlinearConstraint(self.ineq, -np.inf, 0)
        fo = lambda x: self.f.dot(x)
        sol = minimize(fo, self.X, constraints=(lc, nlc))
        
       
        for index, node in enumerate(self.nodes[1:]):
            node.Ckk = sol.x[index]      
        
        return sol
        
    
    def obtain_B(self):
        
        matrizB = np.zeros(2*self.n-2, dtype=float)
        
        for i, node in enumerate(self.nodes[1:]):
           
            for x in node.pros:
                matrizB[2*i] += x.P
                matrizB[2*i+1] += x.Q             
        self.B = matrizB
        
    
    def obtain_f(self):
        
        f = np.zeros((1, self.x_size))       
        f[0, self.n - 1:(self.n+self.m) - 1] = -1
        self.f = f
    
    def obtain_volt(self):
                  
        self.nodes[0].U = complex(1, 0)
        for line in self.lines:
            A = np.array([[np.real(line.nodes[0].U), np.imag(line.nodes[0].U)], 
                          [-np.imag(line.nodes[0].U), np.real(line.nodes[0].U)]], dtype = np.float64)
            b = np.array([line.Ckt, line.Skt], dtype = np.float64)
            x = np.linalg.solve(A, b)
            line.nodes[1].U = complex(x[0], x[1])
           
        return [node.U for node in self.nodes]  
        
    def plot_voltages(self):
        # Extraer las magnitudes y ángulos de las tensiones de cada nodo
        magnitudes = [abs(node.U) for node in self.nodes]
        
        node_ids = [node.ref for node in self.nodes]
        
        # Crear un gráfico de barras para la magnitud de la tensión
        plt.figure(figsize=(16, 6))
        
        plt.bar(node_ids, magnitudes, color='skyblue', edgecolor='black')
        plt.xlabel('Nodo', fontsize=16, fontname='Arial')
        plt.ylabel('Magnitud Tensión (pu)', fontsize=16, fontname='Arial')
        # plt.title('Voltage Magnitudes of Nodes')
        plt.xticks(node_ids, fontsize=12, fontname='Arial', rotation=0)# Mostrar solo números enteros
        plt.yticks(fontsize=16, fontname='Arial')
        plt.ylim(0.91, 1.02)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
        
    def plot_line_currents(self):
        # Crear listas para las intensidades y las referencias de las líneas
        line_ids = [line.ref for line in self.lines]
        line_currents = [abs(line.I) for line in self.lines]  # Tomamos el valor absoluto de la corriente
        
        # Crear el gráfico
        plt.figure(figsize=(16, 6))
        plt.bar(line_ids, line_currents, color='yellow', edgecolor='black')
        plt.xlabel('Línea', fontsize=16, fontname='Arial')
        plt.ylabel('Intensidad (pu)', fontsize=16, fontname='Arial')
        # plt.title('Current Intensities of Each Line')
        plt.xticks(line_ids, fontsize=12, fontname='Arial', rotation=0)
        plt.yticks(fontsize=16, fontname='Arial')
        plt.grid(True)
        
        # Mostrar los valores exactos en cada punto desplazados a la derecha
        # for i, current in enumerate(line_currents):
        #     if i % 3 == 0:
        #         plt.text(line_ids[i] + 0.1, current + 0.02, f'{current:.2f}', ha='left', va='bottom', fontsize=9, rotation=45)
        
        plt.tight_layout()
        plt.show()  
        
    def plot_prosumers_currents(self):
        # Obtener los IDs de los prosumer
        prosumer_ids = [prosumer.ref for prosumer in self.pros]
        
        # Obtener las corrientes de cada prosumer
        currents = [prosumer.intensity() for prosumer in self.pros]
        
        # Obtener las magnitudes de las corrientes
        currents_magnitude = [abs(I) for I in currents]
        
        # Crear el gráfico de la corriente
        plt.figure(figsize=(16, 6))
        
        # Graficar la corriente de cada prosumer
        plt.bar(prosumer_ids, currents_magnitude, color='red', edgecolor='black')
        plt.xlabel('Consumidor/Generador', fontsize=16, fontname='Arial')
        plt.ylabel('Intensidad (pu)', fontsize=16, fontname='Arial')
        # plt.title('Current for Each Prosumer')
        plt.xticks(prosumer_ids, fontsize=12, fontname='Arial', rotation=0)
        plt.yticks(fontsize=16, fontname='Arial')
        # plt.xlim(5,)
        plt.tick_params(axis='x', pad=5)  # Separar los números del eje X del eje
        plt.grid(True)
        plt.legend()        
        plt.tight_layout()
        plt.show()       
        
        
   
    
class node:
    def __init__(self, ref, slack):
        self.ref = ref   
        self.slack = slack        
        self.lines = list()
        self.pros = []
        self.Ckk = None
        self.Ctt = None
        self.index = None
        self.U = None
        
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
        self.Ckt = None
        self.Skt = None
        self.index = []  
        
    def ineq(self, X):
        if self.nodes[0].slack == True:
            Ckk = 1
        else:
            Ckk = X[self.nodes[0].index]
        
        Ctt = X[self.nodes[1].index]
        self.Ckt = X[self.index[0]]
        self.Skt = X[self.index[1]]
        ineq = self.Ckt**2 + self.Skt**2 - Ckk * Ctt
        return ineq
     
    def intensity(self):
        self.I = (self.nodes[0].U - self.nodes[1].U) / self.Z   
        return self.I
            
class prosumer:
    def __init__(self, ref, node_id, P, Q, nodes_list):
        self.ref = ref
        self.P = P
        self.Q = Q    
        self.S = complex(self.P, self.Q)
        self.node = next((item for item in nodes_list if item.ref == node_id), None)
        self.node.pros.append(self)
        
    def intensity(self):
        self.I = np.conj(self.S/(self.node.U))
        return self.I