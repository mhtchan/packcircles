import math
from pyllist import dllist

class Node:
    __slots__ = ['x', 'y', 'radius', 'distance']
    def __init__(self, x, y, radius, distance):
        self.x = x
        self.y = y
        self.radius = radius
        self.distance = distance

## Euclidean distance between node1 and node2
def distance_nodes(node1,node2):
    return math.sqrt((node1.x-node2.x)**2+(node1.y-node2.y)**2)

## Euclidean distance from origin and node
def distance_from_origin(node):
    return math.sqrt(node.x**2+node.y**2)

## Creates a new node from cm, cn and a fixed radius for the new node. Both solutions are returned.
def new_node(cm,cn,radius):
    phi1 = math.atan2(cn.y-cm.y,cn.x-cm.x)
    phi2 = math.acos((distance_nodes(cm,cn)**2+(cm.radius+radius)**2-(cn.radius+radius)**2)/(2*(cm.radius+radius)*distance_nodes(cm,cn)))
    sol1 = Node(cm.x+(cm.radius+radius)*math.cos(phi1+phi2),cm.y+(cm.radius+radius)*math.sin(phi1+phi2),radius,None)
    sol2 = Node(cm.x+(cm.radius+radius)*math.cos(phi1-phi2),cm.y+(cm.radius+radius)*math.sin(phi1-phi2),radius,None)
    sol1.distance = distance_from_origin(sol1)
    sol2.distance = distance_from_origin(sol2)
    return sol1, sol2

## Calulcates the position of the first three nodes and recenters the configuration around the origin.
def initialise(r0,r1,r2):
    nodes = [Node(0,0,r0,None),Node(r0+r1,0,r1,None)]
    sol1, sol2 = new_node(nodes[0],nodes[1],r2)
    if sol1.y < 0:
        nodes.append(sol1)
    else:
        nodes.append(sol2)
    
    # Auxillary variables for equal detour point calculation
    a = r0+r1; b = r0+r2; c = r1+r2
    s = (a+b+c)/2;
    delta = math.sqrt(s*(s-a)*(s-b)*(s-c));
    L1 = a+delta/(s-a); L2 = b+delta/(s-b); L3 = c+delta/(s-c);
    LSum = L1+L2+L3;
    L1 = L1/LSum; L2 = L2/LSum; L3 = L3/LSum;
    
    # Calculate coords of equal detour point and recenter the nodes
    xEDP = L1*nodes[2].x+L2*nodes[1].x+L3*nodes[0].x;
    yEDP = L1*nodes[2].y+L2*nodes[1].y+L3*nodes[0].y;
    
    for node in nodes:
        node.x = node.x-xEDP
        node.y = node.y-yEDP
        node.distance = distance_from_origin(node)
    front_chain = dllist(nodes)
    cm = min(front_chain.iternodes(),key=lambda x:x.value.distance)
    return nodes, cm, front_chain

## Generates candidate nodes
## d is the signed perpendicular distance of the vector cm to cn
## Only the solution with d<0 (i.e. exterior to the front chain) is returned
def candidate_node(cm,radius,front_chain):
    cn = cm.next
    if cn is None:
        cn = front_chain.first
    sol1, sol2 = new_node(cm.value,cn.value,radius)
    d = (sol1.x-cm.value.x)*(cn.value.y-cm.value.y)-(sol1.y-cm.value.y)*(cn.value.x-cm.value.x)
    if d < 0:
        return sol1
    return sol2

## Returns the closest intersecting node, where distance here is defined to be the distance 
## traversed from cm/cn to the node
def check_intersect(candidate,cm,front_chain):
    cn = cm.next
    if cn is None:
        cn = front_chain.first
    intersecting_node = None
    direction = 0
    intersecting_nodes = [node for node in front_chain.iternodes() if distance_nodes(candidate,node.value)-(node.value.radius + candidate.radius) < -0.00000001]
    if len(intersecting_nodes) == 0:
        return intersecting_node, direction
    total_distance = sum(2*node.radius for node in front_chain)
    distances = [distance_to_node(node,cm,cn,front_chain,total_distance) for node in intersecting_nodes]
    min_index, min_distance = min(enumerate(distances), key=lambda x: min(x[1]))
    intersecting_node = intersecting_nodes[min_index]
    if min_distance[0] < min_distance[1]:
        direction = -1
    else:
        direction = 1
    return intersecting_node, direction

## Computes the distance traversed from to_node to cm/cn along the front chain
def distance_to_node(to_node,cm,cn,front_chain,total_distance):
    cm_backward_distance = 0
    current_node = cm
    while True:
        cm_backward_distance += 2*current_node.value.radius
        if current_node == front_chain.first:
            current_node = front_chain.last
        else:
            current_node = current_node.prev
        if current_node == to_node:
            break
    cn_forward_distance = total_distance-cm_backward_distance-2*to_node.value.radius 
    return (cm_backward_distance,cn_forward_distance)

def remove_nodes_ahead(to_node,cm,front_chain):
    while cm.next != to_node:
        if cm == front_chain.last:
            if front_chain.first == to_node:
                break
            front_chain.remove(front_chain.first)
            continue
        front_chain.remove(cm.next)

def remove_nodes_behind(to_node,cn,front_chain):
    while cn.prev != to_node:
        if cn == front_chain.first:
            if front_chain.last == to_node:
                break
            front_chain.remove(front_chain.last)
            continue
        front_chain.remove(cn.prev)

def modify_front_chain(intersecting_node,cm,front_chain,direction):
    if direction == 0:
        return cm, False
    if direction == -1:
        cn = cm.next
        if cn is None:
            cn = front_chain.first
        remove_nodes_behind(intersecting_node,cn,front_chain)
        cm = intersecting_node
    else:
        remove_nodes_ahead(intersecting_node,cm,front_chain)
    return cm, True

def resolve_intersections(cm,radius,front_chain):
    intersections = True
    while intersections:
        candidate = candidate_node(cm,radius,front_chain)
        intersecting_node,direction = check_intersect(candidate,cm,front_chain)
        cm, intersections = modify_front_chain(intersecting_node,cm,front_chain,direction)
    return cm, candidate

def pack(radii):
    if len(radii) < 3:
        raise ValueError("number of given radii must be greater than or equal to 3")
    nodes, cm, front_chain = initialise(radii[0],radii[1],radii[2])
    for idx, radius in enumerate(radii):
        if idx in range(3):
            yield (nodes[idx].x,nodes[idx].y,nodes[idx].radius)
            continue
        cm, new_node = resolve_intersections(cm,radius,front_chain)
        front_chain.insert(new_node,after=cm)
        yield (new_node.x,new_node.y,new_node.radius)
    
