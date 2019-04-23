import math

#this is the map
tm = ['############################################################',
      '#..........................................................#',
      '#..........................................................#',
      '#...............................#..........................#',
      '#...............................#..........................#',
      '#...............................#..........................#',
      '#...............................#..........................#',
      '#...............................#..........................#',
      '#...............................#..........................#',
      '#...............................#..........................#',
      '#.....................S.........#..........................#',
      '#...............................#..........................#',
      '#...............................#..........................#',
      '####################..#################################.####',
      '#................#........#................................#',
      '#................#........#................................#',
      '#................##########................................#',
      '#..........................................................#',
      '#..........................................................#',
      '#..........................................................#',
      '#..........................................................#',
      '#..........................................................#',
      '#.........##############...................................#',
      '#.........#............#...................................#',
      '#.........#............#...................................#',
      '#.........#.......E....#...................................#',
      '#.........#............#...................................#',
      '#.........###..#########...................................#',
      '#..........................................................#',
      '############################################################']

test_map = []

class Node:
    def __init__(self,x,y,parent,distance):
        self.x = x
        self.y = y
        self.parent = parent
        self.distance = distance

class a_star:
    def __init__(self,sx,sy,ex,ey,width=60,height=30):
    #sx,sy,ex,ey are for x axis values and y axis values of start and end points
    # width and height define the size of map
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self.width = width
        self.height = height
        self.openlist = []
        self.closelist = []
        self.path = []

    def find_path(self):
        parent_node = Node(self.sx,self.sy,None,0)  #define the start node

        while True:
            self.extend_round(parent_node)  #extend the node around parent_node whose F value is smallest

            if not self.openlist:  #if the openlist is null,which means there exists no path,then return
                return

            idx,parent_node = self.get_smallest()  #get the node whose F value is smallest

            if self.is_target(parent_node):  #if already get the target node,then generate the path
                self.make_path(parent_node)
                return

            self.closelist.append(parent_node)  #put the node into closelist
            del self.openlist[idx]  #delete the node from openlist

    def make_path(self,parent_node):
        while parent_node:  #trace back from the end node to start node
            self.path.append((parent_node.x, parent_node.y))
            parent_node = parent_node.parent

    def is_target(self,i):
        return i.x == self.ex and i.y == self.ey

    def get_smallest(self):
        smallest = None
        before_value = 100000
        before_idx = -1

        for idx,i in enumerate(self.openlist):
            value = self.get_distance(i)  #get the F value of present node

            if value < before_value:
                smallest = i
                before_value = value
                before_idx = idx
            return before_idx,smallest

    def get_distance(self,i):
        #calculate the F value, F = G + H, G is the length of past path, H is how many length should go further
        G = i.distance
        H = math.sqrt((self.ex - i.x)**2 + (self.ey - i.y)**2) * 1.2
        F = G + H
        distance = F
        return distance

    def extend_round(self,parent_node):
        xs = (-1,0,1,-1,1,-1,0,1)
        ys = (-1,-1,-1,0,0,1,1,1)

        for x,y in zip(xs,ys):
            new_x,new_y = x + parent_node.x,y + parent_node.y

            if not self.is_valid_coordinates(new_x,new_y):  #ignore the invalid region
                continue

            node = Node(new_x,new_y,parent_node,parent_node.distance + self.get_cost(parent_node.x,parent_node.y,new_x,new_y))  #create the new node

            if self.node_in_closelist(node):
                continue

            i = self.node_in_openlist(node)

            if i != -1:
                if self.openlist[i].distance > node.distance:
                    self.openlist[i].parent = node.parent
                    self.openlist[i].distance = node.distance
                continue

            self.openlist.append(node)

    def get_cost(self,x1,y1,x2,y2):
        if x1 == x2 or y1 == y2:
            return 10
        return 14

    def node_in_closelist(self,node):
        for i in self.closelist:
            if node.x == i.x and node.y == i.y:
                return True
        return False

    def node_in_openlist(self,node):
        for i,n in enumerate(self.openlist):
            if node.x == n.x and node.y == n.y:
                return i
        return -1

    def is_valid_coordinates(self,x,y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return test_map[y][x] != '#'

    def get_searched(self):
        searchedlist = []

        for i in self.openlist:
            searchedlist.append((i.x,i.y))

        for i in self.closelist:
            searchedlist.append((i.x,i.y))

        return searchedlist


def print_test_map():
    for line in test_map:
        print(''.join(line))  #use ' ' to connect the line characters, generating a new string

def get_start_XY():
    return get_symbol_XY('S')

def get_end_XY():
    return get_symbol_XY('E')

def get_symbol_XY(s):
    for y, line in enumerate(test_map):
        try:
            x = line.index(s)
        except:
            continue
        else:
            break
    return x,y

def mark_path(searchedlist):
    mark_symbol(searchedlist,'*')

def mark_searched(searchedlist):
    mark_symbol(searchedlist,' ')

def mark_symbol(searchedlist,s):
    for x,y in searchedlist:
        test_map[y][x] = s

def mark_start_end_points(sx,sy,ex,ey):
    test_map[sy][sx] = 'S'
    test_map[ey][ex] = 'E'

def tm_to_test_map():
    for line in tm:
        test_map.append(list(line))

def find_path():
    sx,sy = get_start_XY()
    ex,ey = get_end_XY()
    Astar = a_star(sx,sy,ex,ey)
    Astar.find_path()
    searched = Astar.get_searched()
    path = Astar.path

    mark_searched(searched)  #mark searched area
    mark_path(path)

    print('\n',len(searched),'squares are searched\n')
    if len(path) == 0:
        print('There is no path from start point to end point')
    else:
        print('The path length is',len(path),'\n')

    mark_start_end_points(sx,sy,ex,ey)

if __name__ == "__main__":
    tm_to_test_map()
    find_path()
    print_test_map()



