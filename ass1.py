import re
import sys
import random
import math
import collections
import Queue
import matplotlib.pyplot as plt
import networkx as nx
from datetime import datetime 
import timeit
import time

#randomly create the world map with 26 cities
def create_map():
     #global world_map 
     world_map = [[0 for x in range(100)] for y in range(100)] #range(100): 0-99
     city_list = collections.OrderedDict()
     for i in range(26):  #0-25
          x = random.randint (0,99)   #0-99
          y = random.randint (0,99) 
          #while world_map[x][y] != 0:

          while world_map[x][y] is not 0:
               x = random.randint (0,99)
               y = random.randint (0,99)

          if world_map[x][y] is 0:
               city_name = chr(ord('A') + i)
               world_map[x][y] = city_name
               city_list[city_name] = [x,y]
               #print(city_list)

     return city_list

#calculate the closest four neighbours for each city
def create_graph(city_location):
     graph = collections.OrderedDict()
     for i in range(26):
          city_name = chr(ord('A') + i)
          all_neighbor = {}
          for j in range(26):
               cmped_city_name = chr(ord('A') + j)
               dist = dist_cost(city_location[city_name], city_location[cmped_city_name])
               if dist!= 0:
                    all_neighbor[cmped_city_name] = dist
          # sort all neighbors based on distance
          sorted_neighbor = sorted(all_neighbor.items(), key = lambda x:x[1])    
          
          close_neighbor = []   # the four closest neighbors
          for i in range(4):
               close_neighbor.append(sorted_neighbor[i][0])  
          graph[city_name] = close_neighbor

     #add bi-direction neighbor, if A:[B,C,D,T], but B:[M,N,Q,E], need add A to B's neighbor list
     for i in range(26):
          city_name = chr(ord('A') + i)
          for j in range(26):
               cmped_city_name = chr(ord('A') + j)
               if city_name in graph[cmped_city_name]:
                    if cmped_city_name not in graph[city_name]:
                         graph[city_name].append(cmped_city_name) 

     return graph

def dist_cost(listone, listtwo):
     x_dist = listone[0]-listtwo[0]
     y_dist = listone[1]-listtwo[1]
     square_dist = math.pow(x_dist,2) + math.pow(y_dist,2)
     distance = math.sqrt(square_dist)
     new_distance = int(distance)

     return new_distance

#general method of getting the path
def get_path(parent, start, end):
     child = end 
     path = [end]
#    print 'parent:', parent
     if start in parent:
          del parent[start]
     if child in parent:
          while parent[child]:
               if parent[child] in path:
                    break
               path.append(parent[child])
               child = parent[child]
               if child not in parent: 
                    break
               # avoid the case 'K': 'I', 'I':'K', while loop will be infinite 
               child_parent = parent[child]
               if child_parent in parent:
                    if parent[child_parent] == child:
                         if child_parent not in path:
                              path.append(child_parent)
                         break
     if start != path[-1]:
          path.append(start)
     path.reverse()
     return path


#-----------------------BFS:Breadth First Search-----------------------------------------#
def bfs(start_state, goal_state, city_graph):
     frontier = collections.deque(city_graph[start_state])
     frontier_size = len(frontier)
     explored = []
     explored.append(start_state)
     path = []
     parent = {}
     for city in city_graph[start_state]:
          parent[city] = start_state
     while frontier:
          node = frontier.popleft()
          frontier_size = frontier_size - 1
          explored.append(node)
          if node == goal_state:
               path.append(start_state)
               path.append(node)                       
               return (path, len(explored), frontier_size)       
          child_list = city_graph[node]
          for child in child_list:
               if child not in explored and child not in frontier:
                    if child == goal_state:
                         parent[child] = node
                         path = get_path(parent, start_state, goal_state)
                         return (path, len(explored), frontier_size)
                    parent[child] = node
                    frontier.append(child)
                    frontier_size = frontier_size + 1
     return None

#------------------------------------DFS-------------------------------------#
def dfs(start_state, goal_state, city_graph):
     frontier = []
     for i in range(len(city_graph[start_state])-1,-1,-1):
          frontier.append(city_graph[start_state][i])
     frontier_size = len(city_graph[start_state])
     explored = []
     explored.append(start_state)
     parent = {}
     for city in city_graph[start_state]:
          parent[city] = start_state
     path = []
     while frontier:
          node = frontier.pop()
          frontier_size = frontier_size - 1
          explored.append(node)
          if node == goal_state:
               path = get_path(parent, start_state, goal_state)
          #    print 'dfs_explored:', explored
               return (path,len(explored), frontier_size)        
          child_list = city_graph[node]  #the neighbors of the current city          
          for child in child_list:
               if child not in explored and child not in frontier:
                    parent[child] = node
          frontier.extend(child for child in child_list if child not in explored and child not in frontier)
          frontier_size = frontier_size + 1
     return None

#------------------------------------IDS--------------------------------------#
def depth_limited_search(start_state, goal_state, city_graph, limit):
     parent = {}
     for city in city_graph[start_state]:
          parent[city] = start_state
     explored = []
     def recursive_dls(node, goal_state, city_graph, limit, parent, explored):  
          explored.append(node)    
          if node == goal_state:
          #    print 'parent1:', parent
               result = get_path(parent, start_state, goal_state)
               return (result, len(explored), len(parent)*limit)
          elif limit == 0:
               return 'cutoff'
          else:
               cutoff_occurred = False
               child_list = city_graph[node]
               for child in child_list:
                    parent[child] = node
                    result = recursive_dls(child, goal_state,city_graph, limit - 1, parent, explored)
                    if result == 'cutoff':
                         cutoff_occurred = True
                    elif result is not None:
                    #    print 'paren2:', parent
                    #     result = get_path(parent, start_state, goal_state)
                         return result
               return 'cutoff' if cutoff_occurred else None

     return recursive_dls(start_state, goal_state, city_graph, limit, parent, explored)


def ids(start_state, goal_state, city_graph):
     for depth in xrange(10):
          result = depth_limited_search(start_state, goal_state, city_graph, depth)
          if result != 'cutoff':
               return result
     return None


#----------------------------------Greedy Best first search---------------------------------#
def cost(goal_state, city_location):
     staright_line_distance = {}
     for i in city_location:
          dist = dist_cost(city_location[i], city_location[goal_state])
          staright_line_distance[i] = dist
     distance = sorted(staright_line_distance.items(), key = lambda x:x[1])
     dict_distance = collections.OrderedDict()
     for i in range(len(distance)):
          dict_distance[distance[i][0]] = distance[i][1]
#    print "staright_line_distance:", dict_distance
     return dict_distance

def best_first_search(start_state, goal_state, city_graph, f):  #have a list with all the distance of neighbor to the goal_state
     frontier = Queue.PriorityQueue()
     for city in city_graph[start_state]:
          frontier.put([f[city], city])   #  frontier  = [[1,'A'],[2, 'B'],[3, 'C']]
     frontier_size = frontier.qsize()
     parent = {}
     for city in city_graph[start_state]:
          parent[city] = start_state
     explored = []
     explored.append(start_state)
     while not frontier.empty():
          city = frontier.get()
          frontier_size = frontier_size - 1
          node = city[1]
          explored.append(node)  
          if node == goal_state:
               path = get_path(parent, start_state, goal_state)
               return (path, len(explored), frontier_size)       
          child_list = city_graph[node]
          for child in child_list:
               frontier_list = frontier.queue
               frontier_city = []
               for i in range(len(frontier_list)):
                    frontier_city.append(frontier_list[i][1])
               if child not in explored and child not in frontier_list:
                    parent[child] = node
                    frontier.put([f[child], child])
                    frontier_size = frontier_size + 1
     return None

#-----------------------------------A* Search-----------------------------------------#
def A_star_search(start_state, goal_state, city_graph, city_location, h):  ##have a list with all the distance of neighbor to the goal_state
     frontier = Queue.PriorityQueue()
     for city in city_graph[start_state]:
          frontier.put([h[city], city])   #  frontier  = [[1,'A'],[2, 'B'],[3, 'C']]
     frontier_size = frontier.qsize()
     parent = {}
     for city in city_graph[start_state]:
          parent[city] = start_state
     explored = []
     explored.append(start_state)
     # g is real cost from start to the current
     g = {}
     for city in city_graph[start_state]:
          dist = dist_cost(city_location[city], city_location[start_state])
          g[city] = dist

     while not frontier.empty():
          city = frontier.get()
          frontier_size = frontier_size - 1
          node = city[1]  
          explored.append(node)
          if node == goal_state:
               path = get_path(parent, start_state, goal_state)
               return (path, len(explored), frontier_size)       
          child_list = city_graph[node]
          for child in child_list:
               dist = dist_cost(city_location[child], city_location[node])
               ## get a city list 
               frontier_list = frontier.queue
               frontier_city = []
               for i in range(len(frontier_list)):
                    frontier_city.append(frontier_list[i][1])
               ##
               if child not in explored and child not in frontier_list:
                    parent[child] = node
                    g[child] = g[node]+ dist
                    frontier.put([h[child], child])
                    frontier_size = frontier_size + 1
               elif child in frontier_list:
                    if g[child] < g[node]+dist:
                         parent[child] = node
                         frontier.put([h[child], child])
                         frontier_size = frontier_size + 1

     return None

#----------------------------------Visualization----------------------------------#
def draw_graph(city_graph, city_location, path):
     g = nx.Graph()    #empty graph
     for node in city_graph:
          g.add_node(node)
     count = 0
     edge_list = []
     for node in city_graph:
          for neighbor in city_graph[node]:  
               if node in path and neighbor in path:
                    edge_list.append((node,neighbor))
               if (node,neighbor) not in g.edges():
                    g.add_edge(node, neighbor, weight = dist_cost(city_location[node], city_location[neighbor]))              
                    count = count + 1
               
     pos = nx.spring_layout(g)
     arc_weight = nx.get_edge_attributes(g,'weight')
#     nx.draw_networkx(g, pos, node_color = ['r' if not node in path else 'b' for node in g.nodes()], edge_color = ['black' if not edge in edge_list else 'b' for edge in g.edges()])
#     nx.draw_networkx_edge_labels(g, pos, edge_labels=arc_weight)
#     plt.axis('off')
#     plt.show()
     return count

count_branches = 0

bfs_time_complexity = 0
bfs_space_complexity = 0
bfs_running_time = 0
bfs_path_len = 0
bfs_solved = 0

dfs_time_complexity = 0
dfs_space_complexity = 0
dfs_running_time = 0
dfs_path_len = 0
dfs_solved = 0

ids_time_complexity = 0
ids_space_complexity = 0
ids_running_time = 0
ids_path_len = 0
ids_solved = 0

bestfs_time_complexity = 0
bestfs_space_complexity = 0
bestfs_running_time = 0
bestfs_path_len = 0
bestfs_solved = 0

Astar_time_complexity = 0
Astar_space_complexity = 0
Astar_running_time = 0
Astar_path_len = 0
Astar_solved = 0

for i in range(1):
     city_location = create_map() #create the map  
     start_state = chr(ord('A') + random.randint(0,25))
     #need to test if goal_state == start_state
     goal_state = chr(ord('A') + random.randint(0,25))
     while goal_state == start_state:
          goal_state = chr(ord('A') + random.randint(0,25))

     print 'start_state:', start_state
     print'goal_state:', goal_state
     
      
     #run bfs
     city_graph = create_graph(city_location)
     bfs_start_time = time.time()
     bfs_result = bfs(start_state, goal_state, city_graph)   #bfs_result = [[path], # of node explored]
     bfs_end_time = time.time()
     bfs_running_time = bfs_running_time + (bfs_end_time - bfs_start_time)
     bfs_path = None
     if bfs_result is not None:
          bfs_solved = bfs_solved + 1
          bfs_path = bfs_result[0]
          bfs_path_len = bfs_path_len + len(bfs_path)
          bfs_time_complexity = bfs_time_complexity + int(bfs_result[1])
          bfs_space_complexity = bfs_space_complexity + int(bfs_result[2])
     print 'bfs_path:', bfs_path
      

     
     #run dfs
     city_graph = create_graph(city_location)
     dfs_start_time = time.time()
     dfs_result = dfs(start_state, goal_state, city_graph)
     dfs_end_time = time.time()
     dfs_running_time = dfs_running_time + (dfs_end_time - dfs_start_time)
     dfs_path = None
     if dfs_result is not None:
          dfs_solved = dfs_solved + 1
          dfs_path = dfs_result[0]
          dfs_path_len = dfs_path_len + len(dfs_path)
          dfs_time_complexity = dfs_time_complexity + dfs_result[1]
          dfs_space_complexity = dfs_space_complexity + dfs_result[2]
     print 'dfs_path:', dfs_path
     

     
     #run ids
     city_graph = create_graph(city_location)
     ids_start_time = time.time()
     ids_result = ids(start_state, goal_state, city_graph)
     ids_end_time = time.time()
     ids_running_time = ids_running_time + (ids_end_time - ids_start_time)
     ids_path = None
     if ids_result is not None:
          ids_solved = ids_solved + 1
          ids_path = ids_result[0]
          ids_path_len = ids_path_len + len(ids_path)
          ids_time_complexity = ids_time_complexity + ids_result[1]
          ids_space_complexity = ids_space_complexity + ids_result[1]
     print 'ids_path:', ids_path
      

     '''  
     #run best_first_search
     city_graph = create_graph(city_location)
     bestfs_start_time = time.time()
     staright_distance_togoal = cost(goal_state, city_location)  
     bestfs_result = best_first_search(start_state, goal_state, city_graph, staright_distance_togoal)
     bestfs_end_time = time.time()
     bestfs_running_time = bestfs_running_time + (bestfs_end_time - bestfs_start_time)
     bestfs_path = None
     if bestfs_result is not None:
          bestfs_solved = bestfs_solved + 1
          bestfs_path = bestfs_result[0]
          bestfs_path_len = bestfs_path_len + len(bestfs_path)
          bestfs_time_complexity = bestfs_time_complexity + bestfs_result[1]
          bestfs_space_complexity = bestfs_space_complexity + bestfs_result[2]
     print 'bestfs_path', bestfs_path
      
      
     #run A*
     city_graph = create_graph(city_location)
     Astar_start_time = time.time()
     estimate_staright_distance_togoal = cost(goal_state, city_location)
     Astar_result = A_star_search(start_state, goal_state, city_graph, city_location, estimate_staright_distance_togoal)
     Astar_end_time = time.time()
     Astar_running_time = Astar_running_time + (Astar_end_time - Astar_start_time)
     Astar_path = None
     if Astar_result is not None:
          Astar_solved = Astar_solved + 1
          Astar_path = Astar_result[0]
          Astar_path_len = Astar_path_len + len(Astar_path)
          Astar_time_complexity = Astar_time_complexity + Astar_result[1]
          Astar_space_complexity = Astar_space_complexity + Astar_result[2]
     print 'Astar_path:', Astar_path
     
     '''
     city_graph = create_graph(city_location) 
     print city_graph

     if bfs_path is not None:
     	count_branches =  count_branches + draw_graph(city_graph, city_location, bfs_path)

#-----------------------Calculate the average and print the result------------------------------#
average_branches = count_branches/100
print average_branches


'''
average_bfs_time_complexity = bfs_time_complexity/100
average_bfs_space_complexity = bfs_space_complexity/100
average_bfs_running_time = bfs_running_time/100 
average_bfs_path_len = bfs_path_len/100
print 'average_bfs_time_complexity:', average_bfs_time_complexity    ## 9
print 'average_bfs_space_complexity:', average_bfs_space_complexity 
print 'average_bfs_running_time:', average_bfs_running_time    ## 0.0235ms
print 'average_bfs_path_len:', average_bfs_path_len   
print 'bfs_solved:', bfs_solved
 

  
average_dfs_time_complexity = dfs_time_complexity/100
average_dfs_space_complexity = dfs_space_complexity/100
average_dfs_running_time = dfs_running_time/100 
average_dfs_path_len = dfs_path_len/100
print 'average_dfs_time_complexity:', average_dfs_time_complexity    ## 14
print 'average_dfs_space_complexity:', average_dfs_space_complexity 
print 'average_dfs_running_time:', average_dfs_running_time    ## 5.89609146118e-05
print 'average_dfs_path_len:', average_dfs_path_len   ## 5
print 'dfs_solved:', dfs_solved     ## 96



##depth start from 10
average_ids_time_complexity = ids_time_complexity/100
average_ids_space_complexity = ids_space_complexity/100
average_ids_running_time = ids_running_time/100 
average_ids_path_len = ids_path_len/100
print 'average_ids_time_complexity:', average_ids_time_complexity    ## 2870
print 'average_ids_space_complexity:', average_ids_space_complexity 
print 'average_ids_running_time:', average_ids_running_time    ##  0.0222473692894
print 'average_ids_path_len:', average_ids_path_len   ## 3
print 'ids_solved:', ids_solved     ## 99



average_bestfs_time_complexity = bestfs_time_complexity/100
average_bestfs_space_complexity = bestfs_space_complexity/100
average_bestfs_running_time = bestfs_running_time/100 
average_bestfs_path_len = bestfs_path_len/100
print 'average_bestfs_time_complexity:', average_bestfs_time_complexity    ## 4
print 'average_bestfs_space_complexity:', average_bestfs_space_complexity 
print 'average_bestfs_running_time:', average_bestfs_running_time    ##  0.000818531513214
print 'average_bestfs_path_len:', average_bestfs_path_len   ## 4
print 'bestfs_solved:', bestfs_solved  ##97

 
average_Astar_time_complexity = Astar_time_complexity/100
average_Astar_space_complexity = Astar_space_complexity/100
average_Astar_running_time = Astar_running_time/100 
average_Astar_path_len = Astar_path_len/100
print 'average_Astar_time_complexity:', average_Astar_time_complexity    ## 5
print 'average_Astar_space_complexity:', average_Astar_space_complexity 
print 'average_Astar_running_time:', average_Astar_running_time    ##  0.000366499423981
print 'average_Astar_path_len:', average_Astar_path_len   ## 4
print 'Astar_solved:', Astar_solved  ##97
'''
'''
'''
