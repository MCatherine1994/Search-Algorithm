### **Request**:  
  * Create a world map with 26 cities randomly distributed.  
  * Calculate the distance between each city and select the four closest cities to connect with.  
  * Store the city map and formulate this problem a as a search problem.  
  * Run breadth first search, depth first search, interactive deepening search, greedy best first search and A* search.   
  * Compare the average time complexity, average space complexity, average running time, average path length, and the number of problem solved.  

### **Notes**:  
#####  Create a 100*100 two-dimension list:  
```
world_map = [[0 for x in range(100)] for y in range(100)]
```
#### Generate a random number in a range:  
```
import random
x = random.randint (0,99)
```
#### Assign city name through A to Z in a loop:  
```
for i in range(26):
    city_name = chr(ord('A') + i)
```
#### Ordered Dictionary  
```
import collections
city_list = collections.OrderedDict()
```
  
#### Visualization a graph  
```
import matplotlib.pyplot as plt
import networkx as nx
def draw_graph(city_graph, city_location, path):
     g = nx.Graph()    #empty graph
     for node in city_graph:
          g.add_node(node)  #add node
     edge_list = []
     for node in city_graph:
          for neighbor in city_graph[node]:  
               if node in path and neighbor in path:
                    edge_list.append((node,neighbor))
               if (node,neighbor) not in g.edges():
                    g.add_edge(node, neighbor, weight = dist_cost(city_location[node], city_location[neighbor]))              
               
     pos = nx.spring_layout(g)
     arc_weight = nx.get_edge_attributes(g,'weight')  #assign the path cost as the edge weight
     nx.draw_networkx(g, pos, node_color = ['r' if not node in path else 'b' for node in g.nodes()], edge_color = ['black' if not edge in edge_list else 'b' for edge in g.edges()])
     nx.draw_networkx_edge_labels(g, pos, edge_labels=arc_weight)
     plt.axis('off')  #don't display the axis
     plt.show()   #show the plot

```
