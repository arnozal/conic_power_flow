# Importing required libraries
import numpy as np
import lib

Sbase = 1e6
Ubase = 20e3
Zbase = (Ubase**2)/Sbase

# Nodes
Nodes = [{'id': 0, 'slack': True  , 'V': 20e3/Ubase},
         {'id': 1, 'slack': False , 'V': 20e3/Ubase},
         {'id': 2, 'slack': False , 'V': 20e3/Ubase},
         {'id': 3, 'slack': False , 'V': 20e3/Ubase}]

# Lines
Lines = [{'id': 0,  'From': 0,  'To': 1,  'R': 0.161*4/Zbase, 'X': 0.109*4/Zbase}, 
         {'id': 1,  'From': 1,  'To': 2,  'R': 0.161*2/Zbase, 'X': 0.109*2/Zbase}, 
         {'id': 2,  'From': 2,  'To': 3,  'R': 0.161*5/Zbase, 'X': 0.109*5/Zbase}]

# Prosumers
Pros = [{'id': 0, 'Node': 1, 'P': -2e6/Sbase, 'Q': -1.5e6/Sbase},
        {'id': 1, 'Node': 2, 'P': -1.6e6/Sbase, 'Q': -1.2e6/Sbase},
        {'id': 2, 'Node': 3, 'P': -6.4e6/Sbase, 'Q': -2.4e6/Sbase},]

# Constructing network and solving power flow
net = lib.grid(Nodes, Lines, Pros)

sol = net.solve_pf()

# for x in net.nodes:
#     for y in x.pros:
#         print(f'Nodo {x.ref} Prosumer {y.ref}\n')

# a, b = net.pf()
# #A = net.obtain_A()
# #B = net.obtain_B()
# #X = net.obtain_index()
# #f = net.obtain_f()

# net.obtain_index()
# net.obtain_A()
# net.obtain_B()
# A = net.A
# B = net.B
# X = net.X
# net.obtain_f(X)
# f = net.f



# lineas = net.lines
# for linea in lineas:
#     linea.ineq(X)


# Inecuacion = lib.line(ref= 0, From= 0, To= 1, R= 0.161*4/Zbase, X= 0.109*4/Zbase, nodes_list= Nodes )
# Inecuacion.ineq()
# Ineq = Inecuacion.ineq

# Algunos comandos interesantes
# net.__dict__
# net.nodes[0].__dict__
# net.nodes[0].lines[0].__dict__
# net.nodes[0].lines[0].nodes[0].__dict__

# for node in net.nodes:
#     print(node.__dict__)