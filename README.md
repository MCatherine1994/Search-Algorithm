### **Request**:  
  Create a world map with 26 cities randomly distributed.  
  Calculate the distance between each city and select the four closest cities to connect with.  
  Store the city map and formulate this problem a as a search problem.  
  Run different search algorithm and compare them.  
  
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
