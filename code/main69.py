import numpy as np
import pandas as pd
import lib

Sbase = 0.1e6
Ubase = 12.66e3
Zbase = (Ubase**2)/Sbase

Nodes = []
Lines = []
Pros = []
Nodes.append({
              'id': 0,
              'S': 0,
              'fdp': 0,
              'slack': True
              })

# df = pd.read_csv(os.path.join('red69nudos','69nudos.csv'), decimal=',')
df = pd.read_csv('red69nudos/69nudos.csv', decimal=',')
df.head()
df.fillna(0.0, inplace=True)
df['node_from'].replace(69, 0, inplace=True)
# df['node_from'] = df['node_from'].replace(69, 0)
df['node_to'].replace(69, 0, inplace=True)
# df['node_to'] = df['node_to'].replace(69, 0)


for i, row in df.iterrows():
    Lines.append({
                'id': i, 
                'From': int(row['node_from']), 
                'To': int(row['node_to']),
                'R': row['r_pu'],
                'X': row['x_pu'],
                'Long':1.0,
                })
    if int(row['node_to']) not in [69] + [node['id'] for node in Nodes]:
        Nodes.append({
                    'id': int(row['node_to']),
                    'S': np.sqrt((float(row['p_to_MW'])*1e6)**2 + (float(row['q_to_Mvar'])*1e6)**2)/Sbase,
                    'fdp': float(row['p_to_MW'])/(np.sqrt(float(row['p_to_MW'])**2 + float(row['q_to_Mvar'])**2)) if float(row['p_to_MW']) != 0 else 0,
                    'slack': False
                    })
    
    if float(row['p_to_MW']) != 0 and float(row['q_to_Mvar']) != 0:
        
       Pros.append({
                   'id': int(row['node_to'])-1,
                   'Node': int(row['node_to']),
                   'P': -float(row['p_to_MW']*1000000/Sbase),
                   'Q': -float(row['q_to_Mvar']*1000000/Sbase),
                   })
      
        
        
Lines = Lines[:68] #Las redes radiales.
net = lib.grid(Nodes, Lines, Pros)

sol = net.solve_pf()
Volt = net.obtain_volt()    
I = net.intensity()
Check = net.comprobacion_Kirchhoff() 
I_pros = net.intensity_pros()        
        
net.plot_voltages()
net.plot_line_currents()
net.plot_prosumers_currents()