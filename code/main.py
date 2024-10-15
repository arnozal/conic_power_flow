# Importing required libraries
import numpy as np
import lib

# Network configuration
#     0 ---- 1 ----- 2 
#             \     / \
#              \   /   \
#               \ /     \
#                3 ----- 4 

Sbase = 100e3
Ubase = 20e3
Zbase = (Ubase**2)/Sbase

# Buses 
Nodes = [{'id': 0, 'slack': True  },
         {'id': 1, 'slack': False },
         {'id': 2, 'slack': False },
         {'id': 3, 'slack': False },
         {'id': 4, 'slack': False }]

# Lines
Lines = [{'id': 0,  'From': 0,  'To': 1,  'R': 0.2/Zbase, 'X': 0.2/Zbase, 'Long': 1 }, 
         {'id': 1,  'From': 1,  'To': 2,  'R': 0.2/Zbase, 'X': 0.2/Zbase, 'Long': 1.1 },
         {'id': 2,  'From': 1,  'To': 3,  'R': 0.2/Zbase, 'X': 0.2/Zbase, 'Long': 1 },
         {'id': 3,  'From': 2,  'To': 3,  'R': 0.2/Zbase, 'X': 0.2/Zbase, 'Long': 1 },
         {'id': 4,  'From': 2,  'To': 4,  'R': 0.2/Zbase, 'X': 0.2/Zbase, 'Long': 1.1 },
         {'id': 5,  'From': 3,  'To': 4,  'R': 0.2/Zbase, 'X': 0.2/Zbase, 'Long': 1 }]

# Constructing network and solving power flow
net = lib.grid(Nodes, Lines)
