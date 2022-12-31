"""
here I test the storage of new graph into db
"""

import math


from SLAM.mapping_DB_functionality import MapInDataBase
from SLAM.graph_functionality import DeniGraphMatrixWorld
from SLAM.visualisation_functionality import Visualisation

vis=Visualisation()
m=MapInDataBase()
sp=DeniGraphMatrixWorld()
#b=BODY()

x,y,coord,dist,dir='x','y','coord','dist','dir'
nodes={1:{'x':0,'y':0,'coord':[(1,1),(1,2)],dist:0,dir:0},
       2:{'x':0,'y':50,'coord':[(2,2),(2,3)],dist:50,dir:0},
       3:{'x':50,'y':50,'coord':[(3,3),(3,4)],dist:50,dir:90},
       4:{'x':50,'y':0,'coord':[(4,4),(4,5)],dist:50,dir:90},
       # 5:{'x':10,'y':40,'coord':[(30,4),(40,5)],dist:10,dir:90},
       # 6:{'x':10,'y':30,'coord':[(30,40),(40,50)],dist:10,dir:180},
       # 7:{'x':20,'y':30,'coord':[(33,40),(44,50)],dist:10,dir:90},
       }

m.create_new_unique_into_DB(nodes)

vis.show_all_points_in_db()
#m.clear_graph_in_DB()
#m.delete_node(7)

#comands=sp.final_function(5,6)
#print(comands)
m.con.close()








