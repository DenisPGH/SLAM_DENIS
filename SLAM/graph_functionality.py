from collections import deque
from queue import PriorityQueue

from mapping_DB_functionality import MapInDataBase
from rotation_graph import Rotation


class Edge:
    def __init__(self,source,destination,weight,direction=None):
        self.source = source
        self.destination = destination
        self.weight = weight
        self.direction=direction
        # self.edge_name=''
        # self.edge_row=0
        # self.edge_col=0


class DeniGraphMatrixWorld:
    def __init__(self):
        self.graph_rotation=Rotation()
        self.graph = MapInDataBase()
        self.data_base=MapInDataBase()

    def prove_if_coordinates_are_in_range(self,row, col, rows, cols):
        """

        :param row: current row
        :param col: current col
        :param rows: max row value
        :param cols: max col value
        :return: true if its ok, False if not
        """

        if 0 <= row < rows and 0 <= col < cols:
            return True
        else:
            return False

    def print_matrix(self,mat):
        for row in mat:
            print("".join([str(x) for x in row]))

    def number_nodes_in_matrix(self,mat,free_cell):
        """

        :param mat: matrix
        :free_cell > cell-NAME(sign), equal to free and cen be numbered, all others not
        :return: put name on every non wall cells
        """

        counter = 0
        for row in range(len(mat)):
            for col in range(len(mat[row])):
                if mat[row][col] == free_cell:
                    counter += 1
                    mat[row][col] = counter
        return mat

    def create_graph_from_matrix(self,mat):
        """
        create new graph from given matrix

        :param mat: matrix with each sell unique name
        :return: graph {name:{'name': Edge,}} , connected each cell with its all connected nodes in all directions(8 nodes)
        """

        graph = {}
        rows = len(mat)
        for row in range(rows):
            cols = len(mat[row])
            for col in range(cols):
                if mat[row][col] != "*":
                    current_node_name = mat[row][col]
                    if current_node_name not in graph:
                        graph[current_node_name] = {}
                    if self.prove_if_coordinates_are_in_range(row - 1, col, rows, cols) and mat[row - 1][col] != "*":
                        above_node_name = mat[row - 1][col]
                        graph[current_node_name][f"{current_node_name}-{above_node_name}"] = (
                            Edge(current_node_name, above_node_name, 10, 'up'))
                    if self.prove_if_coordinates_are_in_range(row + 1, col, rows, cols) and mat[row + 1][col] != "*":
                        down_node_name = mat[row + 1][col]
                        graph[current_node_name][f"{current_node_name}-{down_node_name}"] = (
                            Edge(current_node_name, down_node_name, 10, 'down'))
                    if self.prove_if_coordinates_are_in_range(row, col - 1, rows, cols) and mat[row][col - 1] != "*":
                        left_node_name = mat[row][col - 1]
                        graph[current_node_name][f"{current_node_name}-{left_node_name}"] = (
                            Edge(current_node_name, left_node_name, 10, 'left'))
                    if self.prove_if_coordinates_are_in_range(row, col + 1, rows, cols) and mat[row][col + 1] != "*":
                        right_node_name = mat[row][col + 1]
                        graph[current_node_name][f"{current_node_name}-{right_node_name}"] = (
                            Edge(current_node_name, right_node_name, 10, 'right'))

                    if self.prove_if_coordinates_are_in_range(row - 1, col - 1, rows, cols) and mat[row - 1][col - 1] != "*":
                        up_left_node_name = mat[row - 1][col - 1]
                        graph[current_node_name][f"{current_node_name}-{up_left_node_name}"] = (
                            Edge(current_node_name, up_left_node_name, 14, 'up-left'))
                    if self.prove_if_coordinates_are_in_range(row + 1, col + 1, rows, cols) and mat[row + 1][col + 1] != "*":
                        down_right_node_name = mat[row + 1][col + 1]
                        graph[current_node_name][f"{current_node_name}-{down_right_node_name}"] = (
                            Edge(current_node_name, down_right_node_name, 14, 'down-right'))
                    if self.prove_if_coordinates_are_in_range(row + 1, col - 1, rows, cols) and mat[row + 1][col - 1] != "*":
                        down_left_node_name = mat[row + 1][col - 1]
                        graph[current_node_name][f"{current_node_name}-{down_left_node_name}"] = (
                            Edge(current_node_name, down_left_node_name, 14, 'down-left'))
                    if self.prove_if_coordinates_are_in_range(row - 1, col + 1, rows, cols) and mat[row - 1][col + 1] != "*":
                        up_right_node_name = mat[row - 1][col + 1]
                        graph[current_node_name][f"{current_node_name}-{up_right_node_name}"] = (
                            Edge(current_node_name, up_right_node_name, 14, 'up-right'))

        return graph

    def check_if_no_close_walls(self,matrix,row,col,dist,wall_sign):
        """

        :param matrix: world matrix with 0-free, 1-walls
        :param row: current row
        :param col: current col
        :param to_wall: how far shoud be the wall
        :param wall_sign: what charackter is wall
        :return: return True if no wall in given range, False if wall

        """
        wall=False
        to_wall=0
        for _ in range(dist):
            to_wall+=1
            if self.prove_if_coordinates_are_in_range(row,col+to_wall,len(matrix),len(matrix[row]))\
                    and matrix[row][col+to_wall] ==wall_sign:
                wall=True
                break
            if self.prove_if_coordinates_are_in_range(row,col-to_wall,len(matrix),len(matrix[row])) \
                 and matrix[row][col-to_wall] ==wall_sign:
                    wall=True
                    break
            if self.prove_if_coordinates_are_in_range(row+to_wall,col,len(matrix),len(matrix[row])) \
                and matrix[row+to_wall][col] ==wall_sign:
                    wall=True
                    break

            if self.prove_if_coordinates_are_in_range(row-to_wall,col,len(matrix),len(matrix[row]))\
                and matrix[row-to_wall][col] ==wall_sign:
                    wall=True
                    break

            if self.prove_if_coordinates_are_in_range(row+to_wall,col+to_wall,len(matrix),len(matrix[row]))\
                and matrix[row+to_wall][col+to_wall] ==wall_sign:
                    wall=True
                    break
            if self.prove_if_coordinates_are_in_range(row-to_wall,col-to_wall,len(matrix),len(matrix[row]))\
                and matrix[row-to_wall][col-to_wall] ==wall_sign:
                    wall=True
                    break
            if self.prove_if_coordinates_are_in_range(row-to_wall,col+to_wall,len(matrix),len(matrix[row]))\
                and matrix[row-to_wall][col+to_wall] ==wall_sign:
                    wall=True
                    break

            if self.prove_if_coordinates_are_in_range(row+to_wall,col-to_wall,len(matrix),len(matrix[row]))\
                and matrix[row+to_wall][col-to_wall] ==wall_sign:
                    wall=True
                    break
        if wall==True:
            return False
        else:
            return True


    def create_graph_from_LIDAR_coordinates_already_stored_into_world_matrix(self,mat,dist,wall):
        """
        when build the graph, connect only nodes +15 cm far from the walls, and not outside
        store the graph into DB
        :param mat: actual world matrix, generate with helper class
        :param dist :  min distance to the wall
        :param wall : what shoud not be(free cells from world matrix)
        :return:nothing, all points stored into DB
        """
        rows = len(mat)
        for row in range(rows):
            cols = len(mat[row])
            for col in range(cols):
                if mat[row][col] != wall and self.check_if_no_close_walls(mat,row,col,dist,wall): # tuk da e + 15 cm navytre
                    current_node_name = mat[row][col]
                    if current_node_name in self.data_base.all_nodes_names():
                        continue
                    if current_node_name not in self.data_base.all_nodes_names():
                        self.data_base.add_node_into_graph_node_table(current_node_name, col, row)

                    if self.prove_if_coordinates_are_in_range(row - 1, col, rows, cols) \
                            and self.check_if_no_close_walls(mat,row-1,col,dist,wall) \
                            and mat[row - 1][col] !=wall:
                        above_node_name = mat[row - 1][col]
                        self.data_base.add_edge(f'{current_node_name}-{above_node_name}', current_node_name, f'{current_node_name}', f"{above_node_name}", 1, 0)
                        #self.data_base.add_edge(f'{above_node_name}-{current_node_name}', above_node_name, f'{above_node_name}', f"{current_node_name}", 1, 180)




                    if self.prove_if_coordinates_are_in_range(row + 1, col, rows, cols) and\
                            self.check_if_no_close_walls(mat,row+1,col,dist,wall) and\
                        mat[row + 1][col] !=wall:
                        down_node_name = mat[row + 1][col]
                        self.data_base.add_edge(f'{current_node_name}-{down_node_name}', current_node_name,
                                                f'{current_node_name}', f"{down_node_name}", 1, 180)
                        # self.data_base.add_edge(f'{down_node_name}-{current_node_name}', down_node_name,
                        #                         f'{down_node_name}', f"{current_node_name}", 1, 0)

                    if self.prove_if_coordinates_are_in_range(row, col - 1, rows, cols) and\
                        self.check_if_no_close_walls(mat,row,col-1,dist,wall) and\
                            mat[row][col - 1] !=wall:
                        left_node_name = mat[row][col - 1]
                        self.data_base.add_edge(f'{current_node_name}-{left_node_name}', current_node_name,
                                                f'{current_node_name}', f"{left_node_name}", 1, 270)
                        # self.data_base.add_edge(f'{left_node_name}-{current_node_name}', left_node_name,
                        #                         f'{left_node_name}', f"{current_node_name}", 1, 90)
                    if self.prove_if_coordinates_are_in_range(row, col + 1, rows, cols) and\
                            self.check_if_no_close_walls(mat,row,col+1,dist,wall) and \
                            mat[row][col + 1] !=wall:
                        right_node_name = mat[row][col + 1]
                        self.data_base.add_edge(f'{current_node_name}-{right_node_name}', current_node_name,
                                                f'{current_node_name}', f"{right_node_name}", 1, 90)
                        # self.data_base.add_edge(f'{right_node_name}-{current_node_name}', right_node_name,
                        #                         f'{right_node_name}', f"{current_node_name}", 1, 270)

                    if self.prove_if_coordinates_are_in_range(row - 1, col - 1, rows, cols) and \
                        self.check_if_no_close_walls(mat,row-1,col-1,dist,wall) and\
                        mat[row - 1][col - 1] !=wall:
                        up_left_node_name = mat[row - 1][col - 1]
                        self.data_base.add_edge(f'{current_node_name}-{up_left_node_name}', current_node_name,
                                                f'{current_node_name}', f"{up_left_node_name}", 1, 315)
                        # self.data_base.add_edge(f'{up_left_node_name}-{current_node_name}', up_left_node_name,
                        #                         f'{up_left_node_name}', f"{current_node_name}", 1, 135)
                    if self.prove_if_coordinates_are_in_range(row + 1, col + 1, rows, cols) and\
                        self.check_if_no_close_walls(mat,row+1,col+1,dist,wall) and\
                            mat[row + 1][col + 1] !=wall:
                        down_right_node_name = mat[row + 1][col + 1]
                        self.data_base.add_edge(f'{current_node_name}-{down_right_node_name}', current_node_name,
                                                f'{current_node_name}', f"{down_right_node_name}", 1, 135)
                        # self.data_base.add_edge(f'{down_right_node_name}-{current_node_name}', down_right_node_name,
                        #                         f'{down_right_node_name}', f"{current_node_name}", 1, 315)
                    if self.prove_if_coordinates_are_in_range(row + 1, col - 1, rows, cols) and\
                        self.check_if_no_close_walls(mat,row+1,col-1,dist,wall) and \
                            mat[row + 1][col - 1] !=wall:
                        down_left_node_name = mat[row + 1][col - 1]
                        self.data_base.add_edge(f'{current_node_name}-{down_left_node_name}', current_node_name,
                                                f'{current_node_name}', f"{down_left_node_name}", 1, 225)
                        # self.data_base.add_edge(f'{down_left_node_name}-{current_node_name}', down_left_node_name,
                        #                         f'{down_left_node_name}', f"{current_node_name}", 1, 45)
                    if self.prove_if_coordinates_are_in_range(row - 1, col + 1, rows, cols) and \
                        self.check_if_no_close_walls(mat,row-1,col+1,dist,wall) and \
                            mat[row - 1][col + 1] !=wall:
                        up_right_node_name = mat[row - 1][col + 1]
                        self.data_base.add_edge(f'{current_node_name}-{up_right_node_name}', current_node_name,
                                                f'{current_node_name}', f"{up_right_node_name}", 1, 45)
                        # self.data_base.add_edge(f'{up_right_node_name}-{current_node_name}', up_right_node_name,
                        #                         f'{up_right_node_name}', f"{current_node_name}", 1, 225)

        return

    def find_shortest_way_between_two_nodes(self,start, target, graph):
        """
        1. got graph dict with all nodes, weighs, start node, and target node name
        2. return 2 collections:
        - distance(all short distance between start and custom node)
        - parents( each node and its parents node, from it came from)
        """
        distances = {}
        parents = {}
        for nod in graph:
            distances[nod] = float('inf')
            parents[nod] = None
        distances[start] = 0  # declare the start node with distance 0
        pq = PriorityQueue()
        pq.put((0, start))
        while not pq.empty():
            min_distance_to_the_node, node = pq.get()  # get the min value in the queue
            if node == target:
                break
            for node_name, edge in graph[node].items():
                new_distance = min_distance_to_the_node + edge.weight
                if new_distance < distances[edge.destination]:
                    distances[edge.destination] = new_distance
                    parents[edge.destination] = node
                    pq.put((new_distance, edge.destination))
        return distances, parents

    def generate_path_from_source_to_target(self,target_, parents):
        """
        1.this function got the target and parents lists
        2.return the path-list with name nodes from the start to the target, and exact location of the nodes
         """
        path = deque()
        end_path = {}
        node = target_
        while node is not None:
            path.appendleft(node)
            node = parents[node]

        # for row in range(len(mat)):
        #     for col in range(len(mat[row])):
        #         if mat[row][col] in path:
        #             before = mat[row][col]
        #             # mat[row][col]='P'
        #             end_path[before] = {}
        #             end_path[before]['row'] = row
        #             end_path[before]['col'] = col
        #
        return path, end_path

    def mark_path_on_the_map(self,path: dict, mat):
        """

        :param path:
        :param mat:
        :return: new matrix with marked road from start node to the target node
        """
        matrix_ = mat.copy()
        for node, coor in path.items():
            matrix_[coor['row']][coor['col']] = '.'

        for row in range(len(matrix_)):
            for col in range(len(matrix_[row])):
                if isinstance(matrix_[row][col], int):
                    matrix_[row][col] = ' '
                elif matrix_[row][col] == '*':
                    matrix_[row][col] = '#'

        return matrix_

    def commands_to_the_target(self,path: list, graph):
        """

        :param path: list with names from the nodes
        :param graph:
        :return: the command where shoud go, and the distance in cm
        """

        dir = 'dir'
        dist = 'dist'
        commands = {}
        cur_dir = ''
        prev_dir = ''
        weight = 0
        step = 1
        same_step_dist = 0
        for each_step_idx in range(len(path)):
            if each_step_idx < len(path) - 1:
                commands[step] = {}
                cur_dir = graph[path[each_step_idx]][f"{path[each_step_idx]}-{path[each_step_idx + 1]}"].direction
                weight = graph[path[each_step_idx]][f"{path[each_step_idx]}-{path[each_step_idx + 1]}"].weight
                same_step_dist += weight
                if cur_dir == prev_dir:
                    commands[step - 1][dist] = same_step_dist
                else:
                    commands[step][dir] = cur_dir
                    same_step_dist = weight
                    commands[step][dist] = same_step_dist
                    step += 1
                prev_dir = cur_dir
            else:
                commands[step] = []
                commands[step].append("END")
        return commands


    def commands_to_the_target_DB(self,path: list, graph):
        """

        :param path: list with names from the nodes
        :param graph:
        :return: the command where shoud go, and the distance in cm
        """

        dir = 'dir'
        dist = 'dist'
        commands = {}
        cur_dir = ''
        prev_dir = ''
        weight = 0
        step = 1
        same_step_dist = 0
        for each_step_idx in range(len(path)):
            if each_step_idx < len(path) - 1:
                commands[step] = {}
                searched_name=f"{path[each_step_idx]}-{path[each_step_idx+1]}"
                cur_dir = self.graph.return_edge_by_name(searched_name)[5]
                weight = float(self.graph.return_edge_by_name(searched_name)[4])
                same_step_dist += weight
                if cur_dir == prev_dir:
                    commands[step - 1][dist] = same_step_dist
                else:
                    commands[step][dir] = cur_dir
                    same_step_dist = weight
                    commands[step][dist] = same_step_dist
                    step += 1
                prev_dir = cur_dir
            else:
                commands[step] = []
                commands[step].append("END")
        return commands



    def shortest_path_DB(self,start, target):
        graph = self.graph.all_nodes_names()
        distances = {}
        parents = {}
        for nod in graph:
            distances[nod] = float('inf')
            parents[nod] = None
        distances[start] = 0  # declare the start node with distance 0
        pq = PriorityQueue()
        pq.put((0, start))
        while not pq.empty():
            min_distance_to_the_node, node = pq.get()  # get the min value in the queue
            if node == target:
                break
            for  edge,node,source,dest,dist,dir in self.graph.return_kinder_edges_for_node(node):
                dest=int(dest)
                new_distance = min_distance_to_the_node + dist
                if new_distance < distances[dest]:
                    distances[dest] = new_distance
                    parents[dest] = node
                    pq.put((new_distance, dest))
        return distances,parents


    def final_function(self, start:int,target:int):
        """
        !!!!! real world function, with DB
        find the path from db nodes and return the command to reach from point A to point B
        dir= 0-360
        dist= 00.00 cm
        commands= {1: {'dir': 180, 'dist': 30.0}, 2: ['END']}

        """
        # nodes=self.graph.all_nodes_names()  # make errors and stoped it
        # if start not in nodes or target not in nodes:
        #     return 'The node does not exist!!! final function'

        graph ={}
        start_node = start # 3
        target_node =target  # 364
        _, parents = self.shortest_path_DB(start_node, target_node)
        path, _ = list(self.generate_path_from_source_to_target(target_node, parents))
        commands = self.commands_to_the_target_DB(list(path), graph)
        return commands


    def commands_for_rotation_from_direction_to_target_dir(self, cur_dir:int, target_dir:int):
        """
        this function return the exactly value of rotation angle and which dir= L or R

        :param cur_dir: orientation at moment, degree
        :param target_dir: target orientation shoud be, degree
        :return: dict with directions and degree (L >left, R >right)
        """
        start_node = cur_dir  # 3
        target_node = target_dir  # 364
        distances, parents = self.find_shortest_way_between_two_nodes(start_node, target_node, self.graph_rotation.rot_graph())
        path, dict_path = list(self.generate_path_from_source_to_target(target_node, parents))
        commands = self.commands_to_the_target(list(path), self.graph_rotation.rot_graph())
        #print(commands)
        if isinstance(commands[1],dict):
            return commands[1]['dir'],commands[1]['dist']
        else:
            return 'R', 0








# if __name__=='__main__':
#     sp=ShortestPath()
#     path=sp.commands_for_rotation_from_direction_to_target_dir(270, 181)
#     print(f'path==> {path}')







