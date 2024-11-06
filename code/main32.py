import numpy as np
import lib

Sbase = 0.1e6
Ubase = 12.66e3
Zbase = (Ubase**2)/Sbase

Nodes = []
Lines = []
Pros = []
Nodes.append({'id': 0, 'S': 0, 'fdp': 0, 'slack': True})

flag = False
data = 'something'
with open('red32nudos/datos_32.m') as fp:
    data = fp.readline()
    while(data):
        if flag:
            data = data.split(' ')
            data = list(filter(lambda x: x != '' and x != '\n' and x != ']', data))            
            if len(data) == 0:
                break
            Lines.append({
                          'id': int(data[0])-1, 
                          'From': int(data[1]),
                          'To': int(data[2]),
                          'R': float(data[3])/Zbase,
                          'X': float(data[4])/Zbase,
                          'Long':1.0
                          })     
            if int(data[2]) not in [node['id'] for node in Nodes]:
                Nodes.append({
                              'id': int(data[2]),
                              'S': np.sqrt((float(data[5])*1e3)**2 + (float(data[6])*1e3)**2)/Sbase,
                              'fdp': float(data[5])/(np.sqrt(float(data[5])**2 + float(data[6])**2)) if float(data[5]) != 0 else 0,
                              'slack': False
                              })
            if float(data[5]) != 0 and float(data[6]) != 0:
                Pros.append({
                              'id': int(data[2])-1, 
                              'Node': int(data[2]), 
                              'P': float(data[5])*1000/Sbase, 
                              'Q': float(data[6])*1000/Sbase
                              })
    
        if 'datsis' in data:
            flag = True
            data = data.split('datsis = [')[1]
            data = data.split(' ')
            data = list(filter(lambda x: x != '' and x != '\n' and x != ']', data))            
            Lines.append({
                          'id': int(data[0])-1, 
                          'From': 0, 
                          'To': int(data[2]),
                          'R': float(data[3])/Zbase,
                          'X': float(data[4])/Zbase,
                          'Long':1.0,
                          })    
            Nodes.append({
                          'id': int(data[2]),
                          'S': np.sqrt((float(data[5])*1e3)**2 + (float(data[6])*1e3)**2)/Sbase,
                          'fdp': float(data[5])/(np.sqrt(float(data[5])**2 + float(data[6])**2)),
                          'slack': False
                          })
            Pros.append({
                             'id': int(data[2])-1, 
                             'Node': int(data[2]), 
                             'P': float(data[5])*1000/Sbase, 
                             'Q': float(data[6])*1000/Sbase
                             })
        data = fp.readline()

net = lib.grid(Nodes, Lines, Pros)

sol = net.solve_pf()
Volt = net.obtain_volt()
I = net.intensity()
Check = net.comprobacion_Kirchoff() 
I_pros = net.intensity_pros()