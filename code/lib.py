<<<<<<< HEAD
# Importing required libraries
import numpy as np
from scipy.optimize import minimize, NonlinearConstraint, LinearConstraint

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
        matrizX = np.zeros((self.x_size,1), dtype=float)
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
    
        # matrizX1 = np.array([node.index for node in self.nodes]).reshape(self.n, 1)
        # matrizX2 = np.array([line.index[0] for line in self.lines]).reshape(self.m, 1)           
        # matrizX3 = np.array([line.index[1] for line in self.lines]).reshape(self.m, 1)     
        # matrizX = np.vstack((matrizX1, matrizX2, matrizX3)) 
        
        # self.X = matrizX
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

    def solve_pf(self):
        self.obtain_A()
        self.obtain_B()
        self.obtain_f()
        
        lc = LinearConstraint(self.A, self.B, self.B)
        nlc = NonlinearConstraint(self.ineq, -np.inf, 0)
        fo = lambda x: self.f.dot(x)
        sol = minimize(fo, self.X, constraints=(lc, nlc))
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
        # aux = self.n
        
        # while aux < (self.m + self.n):
        #     f[0, aux] = 1
        #     aux += 1
        
        f[0, self.n - 1:(self.n+self.m) - 1] = -1
        self.f = f
        # cuenta = np.dot(f, X)
        # self.cuenta = cuenta
           

        
    def pf(self):
        n = len(self.nodes)
        m = len(self.lines)
        x_size = n+(2*m)
        # columna_inicial = 1   #Para bucle con while

        matrizA = np.zeros((2*n, n+2*m), dtype=float)
        matrizB = np.zeros((2*n,1), dtype=float)
        matrizX = np.zeros((x_size,1), dtype=float)
        matrizX1 = np.zeros((n, 1), dtype=float)
        matrizX2 = np.zeros((m, 1), dtype=float)           
        matrizX3 = np.zeros((m, 1), dtype=float)
                            
        #MATRIZ B
        for i, node in enumerate(self.nodes):
            for x in node.pros:
                matrizB[2*i] += x.P
                matrizB[(2*i)+1] += x.Q
        
        
        #MATRIZ X
        #Listas Ckk, Ckt y Skt que formen la matriz X total
        n_aux = 0
        # while n_aux < n:
        #     matrizX1[n_aux] = self.nodes[n_aux].Ckk
        #     n_aux += 1
        
        # n_aux = 0    
        # while n_aux < m:
        #     matrizX2[n_aux] = self.lines[n_aux].Ckt
        #     n_aux += 1
        
        # n_aux = 0
        # while n_aux < m:
        #     matrizX3[n_aux] = self.lines[n_aux].Skt
        #     n_aux += 1
        
        while n_aux < n:
            self.nodes[n_aux].Ckk = n_aux
            n_aux += 1
        
        n_aux2 = 0    
        while n_aux2 < m:   
            self.lines[n_aux2].Ckt = n_aux
            n_aux += 1
            n_aux2 += 1
        
        n_aux3 = 0    
        while n_aux3 < m:   
            self.lines[n_aux3].Skt = n_aux
            n_aux += 1
            n_aux3 += 1        
       
        matrizX1 = np.array([node.Ckk for node in self.nodes]).reshape(n, 1)
        matrizX2 = np.array([line.Ckt for line in self.lines]).reshape(m, 1)           
        matrizX3 = np.array([line.Skt for line in self.lines]).reshape(m, 1)     
        matrizX = np.vstack((matrizX1, matrizX2, matrizX3))  #Concatena las 3 arrays en vertical.

        print("Los índices de la matriz X relacionados con la línea 0 son: \n", self.lines[0].Ckt,",", self.lines[0].Skt)        

    
        #MATRIZ A
        #El nudo 0 es slack, por lo que las 2 primeras filas son 0.
        for i in range(2, 2*n, 2):
            lineas = []
            for linea in self.lines:
                if linea.nodes[0].ref == i/2 or linea.nodes[1].ref == i/2:
                    lineas.append(linea)
            
            print("Las líneas pertenecientes al nodo", int(i/2) , "son:")
            print(lineas)
            print("")
            
            # j = columna_inicial
            # while j < x_size:
            #     SumaG, SumaB = self.cuenta_1(columna_inicial, lineas)
            #     G_ant, B_ant = self.cuenta_2(columna_inicial, lineas)
            #     G_post, B_post = self.cuenta_3(columna_inicial, lineas)
            #     print(f"Valor de la G de la línea que entra en el nodo: ", lineas[0].G)
            #     print("")
                
            #     if (columna_inicial) < matrizA.shape[1]:
            #         matrizA[i, columna_inicial] = SumaG  #Para la fila de P
            #         matrizA[(i+1), columna_inicial] = SumaB  #Para la fila de Q
               
            #     if (columna_inicial + 3) < matrizA.shape[1]:
            #         matrizA[i, (columna_inicial+3)] = -G_ant
            #         matrizA[(i+1), (columna_inicial+3)] = -B_ant
                
            #     if (columna_inicial + 4) < matrizA.shape[1]:
            #         matrizA[i, (columna_inicial+4)] = -G_post
            #         matrizA[(i+1), (columna_inicial+4)] = -B_post
                
            #     if (columna_inicial + 6) < matrizA.shape[1]:
            #         matrizA[i, (columna_inicial+6)] = -B_ant
            #         matrizA[(i+1), (columna_inicial+6)] = G_ant
                
            #     if (columna_inicial + 7) < matrizA.shape[1]:
            #         matrizA[i, (columna_inicial+7)] = -B_post
            #         matrizA[(i+1), (columna_inicial+7)] = G_post
                
            #     j += 1
                
            # columna_inicial += 1
            
            for j in range(i // 2, x_size):
                columna = j
                SumaG, SumaB = self.cuenta_1(lineas)
                G_ant, B_ant = self.cuenta_2(lineas)
                G_post, B_post = self.cuenta_3(lineas)
                
                if (columna) < matrizA.shape[1]:
                    matrizA[i, columna] = SumaG  #Para la fila de P
                    matrizA[(i+1), columna] = SumaB  #Para la fila de Q
               
                if (columna + 3) < matrizA.shape[1]:
                    matrizA[i, (columna+3)] = -G_ant
                    matrizA[(i+1), (columna+3)] = -B_ant
                
                if (columna + 4) < matrizA.shape[1]:
                    matrizA[i, (columna+4)] = -G_post
                    matrizA[(i+1), (columna+4)] = -B_post
                
                if (columna + 6) < matrizA.shape[1]:
                    matrizA[i, (columna+6)] = -B_ant
                    matrizA[(i+1), (columna+6)] = G_ant
                
                if (columna + 7) < matrizA.shape[1]:
                    matrizA[i, (columna+7)] = -B_post
                    matrizA[(i+1), (columna+7)] = G_post
                
                # print(f"Valor de la posición ({i}.{columna}) de la matriz A: ", matrizA[i, columna])
                # print("")                   
                break         
            
        print("La matriz B es:\n")
        print(matrizB)
        print("")
        print("La matriz X es:\n")
        print(matrizX)
        print("")
        print("La matriz A es:\n")
        print(matrizA)
        print("")
        
        return matrizA,matrizB
    
    def cuenta_1 (self, lineas):
        Suma1 = sum(linea.G  for linea in lineas)
        Suma2 = sum(linea.B  for linea in lineas)
        return Suma1, Suma2
    def cuenta_2 (self, lineas):
        G_anterior = lineas[0].G
        B_anterior = lineas[0].B
        return G_anterior, B_anterior
    def cuenta_3 (self, lineas):
        if len(lineas) > 1:
            G_posterior = lineas[1].G
            B_posterior = lineas[1].B
        else:
            G_posterior = 0
            B_posterior = 0
        return G_posterior, B_posterior


class node:
    def __init__(self, ref, slack):
        self.ref = ref   
        self.slack = slack        
        self.lines = list()
        self.pros = []
        self.Ckk = None
        self.Ctt = None
        self.index = None
        
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
        
class prosumer:
    def __init__(self, ref, node_id, P, Q, nodes_list):
        self.ref = ref
        self.P = P
        self.Q = Q        
        self.node = next((item for item in nodes_list if item.ref == node_id), None)
        self.node.pros.append(self)
        
        
        
        
        
       
        
        
        
        
=======
# Importing required libraries
import numpy as np
from scipy.optimize import minimize, NonlinearConstraint, LinearConstraint

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
        matrizX = np.zeros((self.x_size,1), dtype=float)
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
    
        # matrizX1 = np.array([node.index for node in self.nodes]).reshape(self.n, 1)
        # matrizX2 = np.array([line.index[0] for line in self.lines]).reshape(self.m, 1)           
        # matrizX3 = np.array([line.index[1] for line in self.lines]).reshape(self.m, 1)     
        # matrizX = np.vstack((matrizX1, matrizX2, matrizX3)) 
        
        # self.X = matrizX
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

    def solve_pf(self):
        self.obtain_A()
        self.obtain_B()
        self.obtain_f()
        
        lc = LinearConstraint(self.A, self.B, self.B)
        nlc = NonlinearConstraint(self.ineq, -np.inf, 0)
        fo = lambda x: self.f.dot(x)
        sol = minimize(fo, self.X, constraints=(lc, nlc))
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
        # aux = self.n
        
        # while aux < (self.m + self.n):
        #     f[0, aux] = 1
        #     aux += 1
        
        f[0, self.n - 1:(self.n+self.m) - 1] = -1
        self.f = f
        # cuenta = np.dot(f, X)
        # self.cuenta = cuenta
           

        
    def pf(self):
        n = len(self.nodes)
        m = len(self.lines)
        x_size = n+(2*m)
        # columna_inicial = 1   #Para bucle con while

        matrizA = np.zeros((2*n, n+2*m), dtype=float)
        matrizB = np.zeros((2*n,1), dtype=float)
        matrizX = np.zeros((x_size,1), dtype=float)
        matrizX1 = np.zeros((n, 1), dtype=float)
        matrizX2 = np.zeros((m, 1), dtype=float)           
        matrizX3 = np.zeros((m, 1), dtype=float)
                            
        #MATRIZ B
        for i, node in enumerate(self.nodes):
            for x in node.pros:
                matrizB[2*i] += x.P
                matrizB[(2*i)+1] += x.Q
        
        
        #MATRIZ X
        #Listas Ckk, Ckt y Skt que formen la matriz X total
        n_aux = 0
        # while n_aux < n:
        #     matrizX1[n_aux] = self.nodes[n_aux].Ckk
        #     n_aux += 1
        
        # n_aux = 0    
        # while n_aux < m:
        #     matrizX2[n_aux] = self.lines[n_aux].Ckt
        #     n_aux += 1
        
        # n_aux = 0
        # while n_aux < m:
        #     matrizX3[n_aux] = self.lines[n_aux].Skt
        #     n_aux += 1
        
        while n_aux < n:
            self.nodes[n_aux].Ckk = n_aux
            n_aux += 1
        
        n_aux2 = 0    
        while n_aux2 < m:   
            self.lines[n_aux2].Ckt = n_aux
            n_aux += 1
            n_aux2 += 1
        
        n_aux3 = 0    
        while n_aux3 < m:   
            self.lines[n_aux3].Skt = n_aux
            n_aux += 1
            n_aux3 += 1        
       
        matrizX1 = np.array([node.Ckk for node in self.nodes]).reshape(n, 1)
        matrizX2 = np.array([line.Ckt for line in self.lines]).reshape(m, 1)           
        matrizX3 = np.array([line.Skt for line in self.lines]).reshape(m, 1)     
        matrizX = np.vstack((matrizX1, matrizX2, matrizX3))  #Concatena las 3 arrays en vertical.

        print("Los índices de la matriz X relacionados con la línea 0 son: \n", self.lines[0].Ckt,",", self.lines[0].Skt)        

    
        #MATRIZ A
        #El nudo 0 es slack, por lo que las 2 primeras filas son 0.
        for i in range(2, 2*n, 2):
            lineas = []
            for linea in self.lines:
                if linea.nodes[0].ref == i/2 or linea.nodes[1].ref == i/2:
                    lineas.append(linea)
            
            print("Las líneas pertenecientes al nodo", int(i/2) , "son:")
            print(lineas)
            print("")
            
            # j = columna_inicial
            # while j < x_size:
            #     SumaG, SumaB = self.cuenta_1(columna_inicial, lineas)
            #     G_ant, B_ant = self.cuenta_2(columna_inicial, lineas)
            #     G_post, B_post = self.cuenta_3(columna_inicial, lineas)
            #     print(f"Valor de la G de la línea que entra en el nodo: ", lineas[0].G)
            #     print("")
                
            #     if (columna_inicial) < matrizA.shape[1]:
            #         matrizA[i, columna_inicial] = SumaG  #Para la fila de P
            #         matrizA[(i+1), columna_inicial] = SumaB  #Para la fila de Q
               
            #     if (columna_inicial + 3) < matrizA.shape[1]:
            #         matrizA[i, (columna_inicial+3)] = -G_ant
            #         matrizA[(i+1), (columna_inicial+3)] = -B_ant
                
            #     if (columna_inicial + 4) < matrizA.shape[1]:
            #         matrizA[i, (columna_inicial+4)] = -G_post
            #         matrizA[(i+1), (columna_inicial+4)] = -B_post
                
            #     if (columna_inicial + 6) < matrizA.shape[1]:
            #         matrizA[i, (columna_inicial+6)] = -B_ant
            #         matrizA[(i+1), (columna_inicial+6)] = G_ant
                
            #     if (columna_inicial + 7) < matrizA.shape[1]:
            #         matrizA[i, (columna_inicial+7)] = -B_post
            #         matrizA[(i+1), (columna_inicial+7)] = G_post
                
            #     j += 1
                
            # columna_inicial += 1
            
            for j in range(i // 2, x_size):
                columna = j
                SumaG, SumaB = self.cuenta_1(lineas)
                G_ant, B_ant = self.cuenta_2(lineas)
                G_post, B_post = self.cuenta_3(lineas)
                
                if (columna) < matrizA.shape[1]:
                    matrizA[i, columna] = SumaG  #Para la fila de P
                    matrizA[(i+1), columna] = SumaB  #Para la fila de Q
               
                if (columna + 3) < matrizA.shape[1]:
                    matrizA[i, (columna+3)] = -G_ant
                    matrizA[(i+1), (columna+3)] = -B_ant
                
                if (columna + 4) < matrizA.shape[1]:
                    matrizA[i, (columna+4)] = -G_post
                    matrizA[(i+1), (columna+4)] = -B_post
                
                if (columna + 6) < matrizA.shape[1]:
                    matrizA[i, (columna+6)] = -B_ant
                    matrizA[(i+1), (columna+6)] = G_ant
                
                if (columna + 7) < matrizA.shape[1]:
                    matrizA[i, (columna+7)] = -B_post
                    matrizA[(i+1), (columna+7)] = G_post
                
                # print(f"Valor de la posición ({i}.{columna}) de la matriz A: ", matrizA[i, columna])
                # print("")                   
                break         
            
        print("La matriz B es:\n")
        print(matrizB)
        print("")
        print("La matriz X es:\n")
        print(matrizX)
        print("")
        print("La matriz A es:\n")
        print(matrizA)
        print("")
        
        return matrizA,matrizB
    
    def cuenta_1 (self, lineas):
        Suma1 = sum(linea.G  for linea in lineas)
        Suma2 = sum(linea.B  for linea in lineas)
        return Suma1, Suma2
    def cuenta_2 (self, lineas):
        G_anterior = lineas[0].G
        B_anterior = lineas[0].B
        return G_anterior, B_anterior
    def cuenta_3 (self, lineas):
        if len(lineas) > 1:
            G_posterior = lineas[1].G
            B_posterior = lineas[1].B
        else:
            G_posterior = 0
            B_posterior = 0
        return G_posterior, B_posterior


class node:
    def __init__(self, ref, slack):
        self.ref = ref   
        self.slack = slack        
        self.lines = list()
        self.pros = []
        self.Ckk = None
        self.Ctt = None
        self.index = None
        
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
        
class prosumer:
    def __init__(self, ref, node_id, P, Q, nodes_list):
        self.ref = ref
        self.P = P
        self.Q = Q        
        self.node = next((item for item in nodes_list if item.ref == node_id), None)
        self.node.pros.append(self)
        
        
        
        
        
       
        
        
        
        
>>>>>>> c399fb9fcd346630496244393f270a7749c7a21f
    