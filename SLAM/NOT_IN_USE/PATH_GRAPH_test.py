from collections import deque
from queue import PriorityQueue




class Edge:
    def __init__(self,source,destination,weight,direction=None):
        self.source = source
        self.destination = destination
        self.weight = weight
        self.direction=direction
        # self.edge_name=''
        # self.edge_row=0
        # self.edge_col=0

def prove_if_coordinates_are_in_range(row,col,rows,cols):
    if 0<= row < rows and 0<= col < cols:
        return True
    else:
        return False

def print_matrix(mat):
    for row in mat:
        print("".join([str(x) for x in row]))

def number_nodes_in_matrix(mat):
    """

    :param mat: matrix
    :return: put name on every non wall cells
    """

    counter=0
    for row in range(len(mat)):
        for col in range(len(mat[row])):
            if mat[row][col]=="-":
                counter+=1
                mat[row][col]=counter
    return mat

def create_graph_from_matrix(mat):
    """

    :param mat: matrix with each sell unique name
    :return: graph {name:{'name': Edge,}} , connected each cell with its all connected nodes in all directions(8 nodes)
    """

    graph={}
    rows=len(mat)
    for row in range(rows):
        cols=len(mat[row])
        for col in range(cols):
            if mat[row][col]!="*":
                current_node_name=mat[row][col]
                if current_node_name not in graph:
                    graph[current_node_name]={}
                if prove_if_coordinates_are_in_range(row - 1, col, rows, cols) and mat[row-1][col]!="*":
                    above_node_name = mat[row - 1][col]
                    graph[current_node_name][f"{current_node_name}-{above_node_name}"]=(Edge(current_node_name, above_node_name, 10,'up'))
                if prove_if_coordinates_are_in_range(row + 1, col, rows, cols) and mat[row+1][col]!="*":
                    down_node_name = mat[row + 1][col]
                    graph[current_node_name][f"{current_node_name}-{down_node_name}"]=(Edge(current_node_name, down_node_name, 10,'down'))
                if prove_if_coordinates_are_in_range(row, col-1, rows, cols) and mat[row][col-1]!="*":
                    left_node_name = mat[row][col-1]
                    graph[current_node_name][f"{current_node_name}-{left_node_name}"]=(Edge(current_node_name, left_node_name, 10,'left'))
                if prove_if_coordinates_are_in_range(row, col+1, rows, cols) and mat[row][col+1]!="*":
                    right_node_name = mat[row][col+1]
                    graph[current_node_name][f"{current_node_name}-{right_node_name}"]=(Edge(current_node_name, right_node_name, 10,'right'))


                if prove_if_coordinates_are_in_range(row - 1, col-1, rows, cols) and mat[row-1][col-1]!="*":
                    up_left_node_name = mat[row - 1][col-1]
                    graph[current_node_name][f"{current_node_name}-{up_left_node_name}"]=(Edge(current_node_name, up_left_node_name, 14,'up-left'))
                if prove_if_coordinates_are_in_range(row + 1, col+1, rows, cols) and mat[row+1][col+1]!="*":
                    down_right_node_name = mat[row + 1][col+1]
                    graph[current_node_name][f"{current_node_name}-{down_right_node_name}"]=(Edge(current_node_name, down_right_node_name, 14,'down-right'))
                if prove_if_coordinates_are_in_range(row+1, col-1, rows, cols) and mat[row+1][col-1]!="*":
                    down_left_node_name = mat[row+1][col-1]
                    graph[current_node_name][f"{current_node_name}-{down_left_node_name}"]=(Edge(current_node_name, down_left_node_name, 14,'down-left'))
                if prove_if_coordinates_are_in_range(row-1, col+1, rows, cols) and mat[row-1][col+1]!="*":
                    up_right_node_name = mat[row-1][col+1]
                    graph[current_node_name][f"{current_node_name}-{up_right_node_name}"]=(Edge(current_node_name, up_right_node_name, 14,'up-right'))


    return graph

def find_shortest_way_between_two_nodes(start,target,graph):
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
    distances[start]=0 # declare the start node with distance 0
    pq=PriorityQueue()
    pq.put((0,start))
    while not pq.empty():
        min_distance_to_the_node,node=pq.get() # get the min value in the queue
        if node ==target:
            break
        for node_name,edge in graph[node].items():
            new_distance= min_distance_to_the_node+edge.weight
            if new_distance < distances[edge.destination]:
                distances[edge.destination]=new_distance
                parents[edge.destination]=node
                pq.put((new_distance,edge.destination))
    return distances,parents


def generate_path_from_source_to_target(target_,parents,mat):
    """
    1.this function got the target and parents lists
    2.return the path-list with name nodes from the start to the target, and exact location of the nodes
     """
    path = deque()
    end_path={}
    node = target_
    while node is not None:
        path.appendleft(node)
        node = parents[node]

    for row in range(len(mat)):
        for col in range(len(mat[row])):
            if mat[row][col] in path:
                before=mat[row][col]
                # mat[row][col]='P'
                end_path[before]={}
                end_path[before]['row']=row
                end_path[before]['col']=col


    return path,end_path


def mark_path_on_the_map(path:dict,mat):
    """

    :param path:
    :param mat:
    :return: new matrix with marked road from start node to the target node
    """
    matrix_=mat.copy()
    for node,coor in path.items():
        matrix_[coor['row']][coor['col']]='.'

    for row in range(len(matrix_)):
        for col in range(len(matrix_[row])):
            if isinstance(matrix_[row][col], int):
                matrix_[row][col]=' '
            elif matrix_[row][col]=='*':
                matrix_[row][col] = '#'


    return matrix_


def commands_to_the_target(path:list,graph):
    """

    :param path: list with names from the nodes
    :param graph:
    :return: the command where shoud go, and the distance in cm
    """

    dir='dir'
    dist='dist'
    commands={}
    cur_dir=''
    prev_dir=''
    weight=0
    step=1
    same_step_dist=0
    for each_step_idx in range(len(path)):
        if each_step_idx<len(path)-1:
            commands[step] = {}
            cur_dir=graph[path[each_step_idx]][f"{path[each_step_idx]}-{path[each_step_idx+1]}"].direction
            weight = graph[path[each_step_idx]][f"{path[each_step_idx]}-{path[each_step_idx + 1]}"].weight
            same_step_dist += weight
            if cur_dir ==prev_dir:
                commands[step-1][dist]=same_step_dist
            else:
                commands[step][dir] = cur_dir
                same_step_dist=weight
                commands[step][dist] = same_step_dist
                step += 1
            prev_dir=cur_dir
        else:
            commands[step] = []
            commands[step].append("END")
    return commands





matrix=[["*************************************************************************************"],
        ["*---------------------------------*------------------------*------------------------*"],
        ["*---------------------------------*------------------------*------------------------*"],
        ["*---------------------------------*------------------------*------------------------*"],
        ["*---------------------------------*-------------------------------------------------*"],
        ["*---------------------------------*-------------------------------------------------*"],
        ["*----------------------------------------------------------*------------------------*"],
        ["*----------------------------------------------------------*------------------------*"],
        ["*-----*******************************************************************************"],
        ["*-----------------------------------------------------------------------------------*"],
        ["*-----------------------------------------------------------------------------------*"],
        ["*--------------------------------**-------------------------------------------------*"],
        ["*--------------------------------**-------------------------------------------------*"],
        ["*--------------------------------**-------------------------------------------------*"],
        ["*--------------------------------**-------------------------------------------------*"],
        ["*--------------------------------**-------------------------*************************"],
        ["*--------------------------------**-------------------------**----------------------*"],
        ["*--------------------------------**-------------------------**----------------------*"],
        ["*--------------------------------**----------------------------------------e--------*"],
        ["*--------------------------------**-------------------------------------------------*"],
        ["*--------------------------------**-------------------------**----------------------*"],
        ["*************************************************************************************"],
        ]

matrix_2=[["*******************************************"],
          ["*-----------------------------------------*"],
          ["*----------------------**-----------------*"],
          ["*----------------------**-----------------*"],
          ["*----------------------**-----------------*"],
          ["*************************-----*************"],
          ["**----------------------------------------*"],
          ["**-----------------------------**---------*"],
          ["**-----------------------------**---------*"],
          ["************************************----***"],
          ["**------------**--------------------------*"],
          ["**------------**--------------------------*"],
          ["**----------------------------------------*"],
          ["*******************************************"],


        ]

matrix=[list(x[0]) for x in matrix_2]
new_matrix=number_nodes_in_matrix(matrix)
test_matrix=[[1,2,3],
             [4,5,6],
             [7,8,9]]

graph=create_graph_from_matrix(new_matrix)
start_node=364 #3
target_node=230 # 364
distances,parents=find_shortest_way_between_two_nodes(start_node,target_node,graph)
path,dict_path=list(generate_path_from_source_to_target(target_node,parents,new_matrix))
final_matrix=mark_path_on_the_map(dict_path,new_matrix)
print_matrix(final_matrix)
comand=commands_to_the_target(list(path),graph)
print(comand)

text='Go  '
measure=0
for step,info in comand.items():
    if isinstance(info,dict):
        measure+=info['dist']
        text+=f"'{info['dir']}' => {info['dist']} cm , then "
    else:
        text+=' done!'


print(f'{text}. Distance= {measure} cm')




