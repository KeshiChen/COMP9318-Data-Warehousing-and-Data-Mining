## import modules here 
import math
################# Question 0 #################

def add(a, b): # do not change the heading of the function
    return a + b


################# Question 1 #################

def nsqrt(x): # do not change the heading of the function
    if x < 2:
        return x
    if x == 2:
        return 1
    tmp = int(x/2)
    while tmp**2 > x:
        tmp = int(tmp/2)
    a = tmp * 2
    b = tmp
    while a > b + 1:
        avg = (a + b)/2
        if avg ** 2 <= x:
            b = math.floor(avg)
        else:
            a = math.ceil(avg)
    if a ** 2 <= x:
        return a
    return b


################# Question 2 #################


# x_0: initial guess
# EPSILON: stop when abs(x - x_new) < EPSILON
# MAX_ITER: maximum number of iterations

## NOTE: you must use the default values of the above parameters, do not change them

def find_root(f, fprime, x_0=1.0, EPSILON = 1E-7, MAX_ITER = 1000): # do not change the heading of the function
    x = x_0
    for i in range(MAX_ITER):
        x_1 = x
        x = x - f(x)/fprime(x)
        if abs(x_1 - x) < EPSILON:
            return x
    return x


################# Question 3 #################

class Tree(object):
    def __init__(self, name='ROOT', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

def make_tree(tokens): # do not change the heading of the function
    tree = Tree(tokens[0])
    parent = tree
    child = tree
    grandparents = []
    for i in range(1, len(tokens)):
        if tokens[i] == '[':
            grandparents.append(parent)
            parent = child
            continue
        if tokens[i] == ']':
            parent = grandparents.pop()
            continue
        child = Tree(tokens[i])
        parent.add_child(child)
    return tree  

def max_depth(root): # do not change the heading of the function
    if len(root.children) == 0:
        return 1
    maxDepth = max([1+max_depth(child) for child in root.children])
    return maxDepth