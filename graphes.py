import numpy as np
import time
from matplotlib.pyplot import imread
    
def axeadj(node1, node2):
    a1, b1 = node1
    a2, b2 = node2
    return "vert" if abs(a1 - a2) == 1 else "hori"
    
def ordadj(node1, node2):
    '''Renvoie 1 si node1 est plus proche du coin supérieur gauche que node2, -1 sinon'''
    a1, b1 = node1
    a2, b2 = node2
    return 1 if a1 - a2 + b1 - b2 == - 1 else - 1

## Flow


w01=1
w11=8
w00=8
wn=4

class flow:
    
    def __init__(self, g, booltab, w01 = 1, w11 = 8, w00 = 8, wn = 4):
            self.root = booltab * w11 + (1 - booltab) * w01
            self.term = booltab * w01 + (1 - booltab) * w00
            self.lr = np.ones(booltab.shape) * wn
            self.tb = np.ones(booltab.shape) * wn
    
    def __call__(self, a, b):
        
        if a == (-1,0):
            return self.root[b]
        
        if b == (0,-1):
            return self.term[a]
        
        if a == (0,-1):
            return - self.term[b]
        
        if b == (-1,0):
            return - self.root[a]
        
        if axeadj(a, b) == "vert":
            if ordadj(a, b) == 1 :
                return self.tb[a]
            else :
                return - self.tb[b]
        else :
            if ordadj(a, b) == 1 :
                return self.lr[a]
            else :
                return - self.lr[b]
                
## Graphe

class imgraph:
    
    def __init__(self, booltab, nblabel = 1, w01 = 4, w11 = 8, w00 = 8, wn = 6):
        a, b, = booltab.shape
        self.dim = (a, b)
        self.tab = np.zeros((a, b, nblabel))
        self.tab[:,:,0] = booltab
        self.im = self.tab[:,:,0]
        r = [0] * nblabel
        r[0] = "root"
        self.root = r
        t = [0] * nblabel
        t[0] = "term"
        self.term = t
        self.flow = flow(self, booltab, w01, w11, w00, wn)
            
        def w(a, b):
            
            inf = float("infinity")
            
            if self.isadj(a, b):
                if a == self.root:
                    return w11 if self.im[b] else w01
                if b == self.root:
                    return w11 if self.im[a] else w01
                if a == self.term:
                    return w01 if self.im[b] else w00
                if b == self.term:
                    return w01 if self.im[a] else w00
                else:
                    return wn
            else:
                return inf
        self.w = w
        self.setflow = setflow

        def isadj(node1, node2):
            if node1 == node2:
                return False
            elif node1 == self.root and node2 == self.term or node1 == self.term and node2 == self.root:
                return False
            elif node1 == self.root or node2 == self.term or node1 == self.term or node2 == self.root:
                return True
            a1, b1 = node1
            a2, b2 = node2
            return (abs(a1 - a2) == 1 and abs(b1 - b2) == 0) or (abs(a1 - a2) == 0 and abs(b1 - b2) == 1)
        
        self.isadj = isadj
    
    def __call__(self,coor):
        a,b=coor
        if a==-1:
            return g.root
        if b==-1:
            return g.term
        else:
            return g.tab[a,b,:]
    

def setflow(a, b, v):
                
    f = g.flow
            
    if a == (-1,0):
        f.root[b] = v
        return
            
    if b == (0,-1):
        f.term[a] = v
        return
    if a == (0,-1):
        f.term[b] = - v
        return
            
    if b == (-1,0):
        f.root[a] = - v
        return
            
    if axeadj(a, b) == "vert":
        if ordadj(a, b) == 1 :
            f.tb[a] = v
        else :
            f.tb[b] = - v
    else :
        if ordadj(a, b) == 1 :
            f.lr[a] = v
        else :
            f.lr[b] = - v
    return


## Neighbours

def neighbours(graph, node):
    
    m, n = graph.dim
    
    if node == (-1,0):
        return [(i, j) for i in range(m) for j in range(n)]
        
    if node == (0,-1):
        return []
    a, b = node
    
    if a == 0 :
        if b == 0:
            return [(a + 1, b), (a, b + 1), (0,-1)]
        elif b == n-1:
            return [(a + 1, b), (a, b - 1), (0,-1)]
        else :
            return [(a + 1, b), (a, b - 1), (a, b + 1), (0,-1)]
            
    elif a == m-1 :
        if b == 0:
            return [(a - 1, b), (a, b + 1), (0,-1)]
        elif b == n-1:
            return [(a - 1, b), (a, b - 1), (0,-1)]
        else :
            return [(a - 1, b), (a, b - 1), (a, b + 1), (0,-1)]
            
    elif b == 0 : 
        return [(a - 1, b), (a, b + 1), (a + 1, b), (0,-1)]
        
    elif b == m :
        return [(a - 1, b), (a, b - 1), (a + 1, b), (0,-1)]
    return [(a - 1, b), (a, b - 1), (a + 1, b), (a, b + 1), (0,-1)]

# a = imread("lena.png")[150:160,50:60] > 0.2
# g = imgraph(a, 3)