import numpy as np
import imageio
from matplotlib.pyplot import *

a = imread("lena.png")
w11 = 10
w10 = 1
w00 = 10
wn = 4

def isadj(node1, node2):
    a1, b1 = node1
    a2, b2 = node2
    return (abs(a1 - a2) == 1 and abs(b1 - b2) == 0) or (abs(a1 - a2) == 0 and abs(b1 - b2) == 1)
    
def axeadj(node1, node2):
    a1, b1 = node1
    a2, b2 = node2
    return "vert" if abs(a1 - a2) == 1 else "hori"
    
def ordadj(node1, node2):
    '''Renvoie 1 si node1 est plus proche du coins supérieur gauche que node2, -1 sinon'''
    a1, b1 = node1
    a2, b2 = node2
    return 1 if a1 - a2 + b1 - b2 == - 1 else - 1

class flot:
    
    def __init__(self, dimg, w10 = 1, w11 = 10, w00 = 10, wn = 4):
        if type(dimg) == tuple:
            self.root = np.zeros(dimg)
            self.term = np.zeros(dimg)
            self.lr = np.zeros(dimg)
            self.tb = np.zeros(dimg)
        else :
            self.root = dimg * w11 + (1 - dimg) * w10
            self.term = dimg * w10 + (1 - dimg) * w00
            self.lr = np.ones(dimg.shape) * wn
            self.tb = np.ones(dimg.shape) * wn
    
    def __call__(self, a, b):

        inf = float("infinity")
        
        if a == "root" and b == "term":
            return inf
        
        if b == "root" and a == "term":
            return inf
        
        if a == "root":
            return self.root[b]
        
        if b == "term":
            return self.term[a]
        
        if a == "term":
            return - self.term[b]
        
        if b == "root":
            return - self.root[a]
        
        if not isadj(a, b):
            return inf
        else:
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
    
def setflot(f, a, b, v):
    
        if a == "root" and b == "term":
            return
        
        if b == "root" and a == "term":
            return
        
        if a == "root":
            f.root[b] = v
            return
        
        if b == "term":
            f.term[a] = v
            return
        
        if a == "term":
            f.term[b] = - v
            return
        
        if b == "root":
            f.root[a] = - v
            return
        
        if not isadj(a, b):
            return
        else:
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

class picg:

    def __init__(self, img, lvl):
        nodes = (img <= lvl)
        antinodes = (img > lvl)
        self.nodes = nodes
        self.rac = "root"
        self.pui = "term"
        self.w = self.weight
        self.flot = flot(img)
        self.dim = img.shape
    
    def weight(self, a, b) :
        inf = float("infinity")
        if (a, b) == ("root", "term") or (a, b) == ("term", "root"):
            return inf
        
        if a == "root" :
            if self.nodes[b] :
                return w11
            else :
                return w10
        
        if b == "term" :
            if self.nodes[a] :
                return w10
            else :
                return w00
                
        if b == "root" or a == "term":
            return self.weight(b, a)   
            
        if isadj(a, b):
            return wn
        else:
            return inf

g = picg(a, 0.5)

f = flot((5, 5))
setflot(f, (0, 0), (0, 1), 5)

def path(start, target, parent):
    1
    
def neighbours(graph, node):
    m, n = graph.dim
    if node == graph.rac:
        return [(i, j) for i in range(m) for j in range(n)]
    if node == graph.pui:
        return []
    a, b = node
    m, n = m - 1, n - 1
    if a == 0 :
        if b == 0:
            return [(a + 1, b), (a, b + 1)]
        elif b == n:
            return [(a + 1, b), (a, b - 1)]
        else :
            return [(a + 1, b), (a, b - 1), (a, b + 1)]
    elif a == m :
        if b == 0:
            return [(a - 1, b), (a, b + 1)]
        elif b == n:
            return [(a - 1, b), (a, b - 1)]
        else :
            return [(a - 1, b), (a, b - 1), (a, b + 1)]
    elif b == 0 : 
        return [(a - 1, b), (a, b + 1), (a + 1, b)]
    elif b == m :
        return [(a - 1, b), (a, b - 1), (a + 1, b)]
    return [(a - 1, b), (a, b - 1), (a + 1, b), (a, b + 1)]

def growth(t,S,A,parent):
    if S[t]:
        return path("root", t, parent)
    while A:
        p = A.pop()
        