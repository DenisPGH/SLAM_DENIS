""""
#TODO
ALL INTO CLASS
1. table edges
2. table graph
2.1 graph[name]={'edg1': reference to table edges,'edg2':,'coord of detected points'}
3. store the graph into sqlite db
4. visualisation of points in matplot
"""
import sqlite3


class MapInDataBase:
    def __init__(self):
        self.con=sqlite3.connect('map.db')
        self.cur=self.con.cursor()

    def drop_table(self,name):
        """
        :param name: name of the table in db for delete
        :return:
        """
        self.cur.execute(f''' DROP TABLE {name}''')
        self.con.commit()
        #self.con.close()

    def create_db_table_edges(self,name='edges'):
        """
        :param name: name of table in DB which store each edge between nodes
        :return:
        """
        self.cur.execute(f'''CREATE TABLE {name}
         (id text primary key, parent_node integer , source_node text, destination_node text, distance real, direction_angle integer, FOREIGN KEY(parent_node) REFERENCES node(id_node))''')
        self.con.commit()
        #self.con.close()

    def add_edge(self,name,node,source_node,destination_node,distance,direction_angle):
        """

        :param name: nodeCur-nodePRev
        :param node: int
        :param source_node: nodeCur
        :param destination_node: nodePrev
        :param distance: between,int
        :param direction_angle: angle between them 0-360,int
        :return:
        """

        self.cur.execute('''INSERT INTO edges (id,parent_node,source_node,destination_node,distance,direction_angle)
                        VALUES (?,?, ?, ?, ?, ?);''', (name, node, source_node, destination_node, distance, direction_angle))
        self.con.commit()
        #self.con.close()

    def create_db_table_graph_node(self,name='node'):
        """
        :param name: name of table, where to store all nodes
        :return:
        """
        self.cur.execute(f'''CREATE TABLE {name}
                 (id integer primary key, id_node integer, x integer , y integer )''')
        self.con.commit()
        #self.con.close()

    def add_node_into_graph_node_table(self,id,x,y):
        """

        :param id: unique ID num from 1, to n-nodes
        :param x: x coord in the word frame
        :param y: y coord in the word frame
        :return:
        """
        self.cur.execute('''INSERT INTO node (id_node,x,y)
                               VALUES (?,?,?);''',
                         (id,x,y))
        self.con.commit()
        #self.con.close()

    def return_kinder_edges_for_node(self, node_id):
        """

        :param node_id: return all edges for node with name 'node_id'
        :return: list
        """
        res=''
        self.cur.execute(f"select * from edges where parent_node={node_id}")
        res=self.cur.fetchall()
        #self.con.close()
        return res

    def all_nodes_names(self):
        """
        :return: the list with all nodes names
        """
        self.cur.execute(f"select id_node from node")
        res = self.cur.fetchall()
        res=[x[0] for x in res]
        return res

    def create_coordinates_table_in_db(self,name='coordinates'):
        """
        :param name: name of table in DB for store all coordinates and from which node are generated
        :return:
        """
        self.cur.execute(f'''CREATE TABLE {name}
                        (id integer, x integer , y integer, FOREIGN KEY(id) REFERENCES node(id_node) )''')

        self.con.commit()

    def add_new_coordinate(self,id_node,coord:list):
        """
        add the all cordiantes corelate to one node
        :param coord: list with tuple [(x,y),(x,y)]
        :return: nothing
        """
        #self.cur.execute(f'''INSERT INTO coordinates (id) VALUES ({id_node});''')
        self.cur.executemany(f"INSERT INTO coordinates (id,x,y) values ({id_node}, ?, ?)", (coord))

        self.con.commit()


    def create_new_unique_into_DB(self,nodes:dict):
        """
        test creating graph into db
        dict=nodes={ 1: {'x':0,'y':10,'coord':[(1,1),(1,2)],dist:0,dir:0} }
        :param nodes:
        :return:
        """
        x, y, coord, dist, dir = 'x', 'y', 'coord', 'dist', 'dir'
        for node, info in nodes.items():
            if node in self.all_nodes_names():
                continue
            if node not in self.all_nodes_names():
                self.add_node_into_graph_node_table(node, info[x], info[y])
                self.add_new_coordinate(node, info[coord]) # if I want to store at same time coordinates and new node
            if node != 1:
                if info[dir]+180 >=360:
                    self.add_edge(f'{node}-{node - 1}', node, f'{node}', f"{node - 1}", info[dist], info[dir]-180)
                else:
                    self.add_edge(f'{node}-{node - 1}', node, f'{node}', f"{node - 1}", info[dist], info[dir]+180)

                self.add_edge(f'{node - 1}-{node}', node - 1, f'{node - 1}', f"{node}", info[dist], info[dir])

        # m.con.close()


    def return_all_coord_for_a_node(self,node_id):
        """
        :param node_id: node_id
        :return: list with tuple(x,y), all coordinates for this node
        """
        result = ''
        self.cur.execute(f"select x,y from coordinates where id={node_id}")
        result = self.cur.fetchall()
        # self.con.close()
        return result

    def close(self):
        """
        close connection to the DB IMPORTANT
        """
        self.con.close()

    def return_own_coord_of_node(self,node_id):
        """
        :param node_id: name node
        :return: tuple(x,y) of the node
        """
        result=(0,0)
        self.cur.execute(f"select x,y from node where id_node={node_id}")
        self.con.commit()
        result = self.cur.fetchall()
        return result

    def clear_graph_in_DB(self):
        """
        clear all tables in DB
        """
        self.cur.execute("""DELETE FROM node""")
        self.cur.execute("""DELETE FROM edges""")
        self.cur.execute("""DELETE FROM coordinates""")
        self.con.commit()


    def return_edge_by_name(self,id_edge):
        """
        :param id_edge: name of edge
        :return: the info for this edge [('1-2', 1, '1', '2', 10.0, 0)]
        """
        edge = ''
        self.cur.execute(f"select * from edges where id='{id_edge}'")
        edge = self.cur.fetchall()
        return edge[0]


    def delete_node(self,node_id):
        """
        delete all info for a node from all tables
        :param node_id: id of the node for deleting
        """

        self.cur.execute(f"""DELETE FROM edges WHERE parent_node='{node_id}'""")
        self.cur.execute(f"""DELETE FROM coordinates WHERE id='{node_id}'""")
        self.cur.execute(f"""DELETE FROM node WHERE id_node='{node_id}'""")
        self.con.commit()




    def print_all_info_from_table_nodes(self):
        """
        return all nodes from the db-node table
        :return: nothing
        """
        self.cur.execute(f"select * from node")
        result = self.cur.fetchall()
        print('Nodes:')
        for node in result:
            print(f"id: {node[0]} | name:{node[1]} | x:{node[2]} | y:{node[3]}")
        return

    def print_all_info_from_table_edges(self):
        """
        return all edges from the db-edges table
        :return: nothing
        """
        self.cur.execute(f"select * from edges")
        result = self.cur.fetchall()
        print('Edges:')
        for edge in result:
            print(f"name: {edge[0]} | parent_node: {edge[1]} | from: {edge[2]} | to: {edge[3]} | distance_between= {edge[4]} cm | world_direction: {edge[5]} deg.")

    def print_all_coord_for_node(self,node):
        result = ''
        self.cur.execute(f"select * from coordinates where id={node}")
        result = self.cur.fetchall()
        for a in result:
            print(f"node: {a[0]} | x: {a[1]:.2f} | y: {a[2]:.2f}")

    def clear_coord_for_node(self,node):
        self.cur.execute(f"""DELETE FROM coordinates WHERE id={node}""")
        self.con.commit()

    # Position table
    def create_db_table_position(self,name='position'):
        """
        :param name: name of table, where to store current position, orientation, and node name
        :return:
        """
        self.cur.execute(f'''CREATE TABLE {name}
                 (id integer, node_name text, theta float , x float , y float )''')
        self.con.commit()


    def update_position_in__DB(self,node_name,theta,x,y):
        """
        update the new coordiantes, orientation and name of the node in the DataBase
        :param node_name: name of current node
        :param theta: 0-360 degrees
        :param x: x coord in the word frame
        :param y: y coord in the word frame
        :return:
        """
        #self.cur.execute("""DELETE FROM position """)
        #self.cur.execute('''INSERT INTO position (node_name,theta,x,y) VALUES (?,?,?,?);''', node_name,theta,x,y))

        self.cur.execute('''UPDATE position SET node_name=?,theta=?,x=?,y=? WHERE id=0  ;''',
                         (node_name, theta, x, y))


        self.con.commit()



    def print_current_location_of_the_robot(self):
        """
        return the info for location, orientation and node name
        :return: nothing
        """
        self.cur.execute(f"select * from position ")
        result = self.cur.fetchall()
        print(f'{result}')

    def add_the_first_coordinates(self,node_=0,theta_=0.0,x_=0.0,y_=0.0):
        
        self.cur.execute(f"INSERT INTO position(id,node_name,theta,x,y) VALUES (?,?,?,?,?)", (0,node_,theta_,x_,y_))
        self.con.commit()

    def return_current_location_of_the_robot(self):
        """
        return the info for location, orientation and node name
        :return: [id,node_name,theta,x,y]
        """
        self.cur.execute(f"select * from position ")
        self.con.commit()
        result = self.cur.fetchall()[0]
        return result[1],float(result[2]),float(result[3]),float(result[4])

    def del_table_position(self):
        self.cur.execute(f''' DROP TABLE position''')
        self.con.commit()











