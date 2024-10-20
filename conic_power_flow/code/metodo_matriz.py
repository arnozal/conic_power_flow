import numpy as np
import lib


numero_nodos = n
numero_lineas = m



matrizA = (2*n, n+2*m)
matrizB = (2*n,1)

for i, node in enumerate(self.nodes):
    for x in node.pros:
        matrizB(2*i) = x.P
        matrizB((2*i)+1) = x.Q