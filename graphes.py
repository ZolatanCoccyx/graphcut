import numpy as np
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

class flow:
    
    def __init__(self, g, booltab, w01 = 1, w11 = 10, w00 = 10, wn = 4):
            self.root = booltab * w11 + (1 - booltab) * w01
            self.term = booltab * w01 + (1 - booltab) * w00
            self.lr = np.ones(booltab.shape) * wn
            self.tb = np.ones(booltab.shape) * wn
    
    def __call__(self, a, b):
        
        if a == g.root:
            return self.root[b]
        
        if b == g.term:
            return self.term[a]
        
        if a == g.term:
            return - self.term[b]
        
        if b == g.root:
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
    
    def __init__(self, booltab, nblabel = 1, w01 = 1, w11 = 8, w00 = 8, wn = 4):
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
        self.flow = flow(g, booltab, w01, w11, w00, wn)
            
        def w(a, b):
            
            inf = float("infinity")
            
            if self.isadj(a, b):
                if a == self.root:
                    return w11 if self.im[b] else w10
                if b == self.root:
                    return w11 if self.im[a] else w10
                if a == self.term:
                    return w10 if self.im[b] else w00
                if b == self.term:
                    return w10 if self.im[a] else w00
                else:
                    return wn
            else:
                return inf
        
        self.w = w
        
        def setflow(a, b, v):
                
            f = g.flow
            
            if a == g.root:
                f.root[b] = v
                return
            
            if b == g.term:
                f.term[a] = v
                return
            
            if a == g.term:
                f.term[b] = - v
                return
            
            if b == g.root:
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

a=np.matrix([[0.4,0.4,0.8,0.9,0.9],[0.2,0.3,0.4,0.56,0.57],[0.1,0.4,0.9,0.8,0.9],[0.2,0.2,0.6,0.6,0.6],[0.1,0.1,0.6,0.6,0.6]])<0.5
g = imgraph(a,1)

## Neighbours

def neighbours(graph, node):
    
    m, n = graph.dim
    
    if node == graph.root:
        return [(i, j) for i in range(m) for j in range(n)]
        
    if node == graph.term:
        return []
    
    a, b = node
    m, n = m - 2, n - 2
    
    if a == 0 :
        if b == 0:
            return [(a + 1, b), (a, b + 1), graph.term]
        elif b == n:
            return [(a + 1, b), (a, b - 1), graph.term]
        else :
            return [(a + 1, b), (a, b - 1), (a, b + 1), graph.term]
            
    elif a == m :
        if b == 0:
            return [(a - 1, b), (a, b + 1), graph.term]
        elif b == n:
            return [(a - 1, b), (a, b - 1), graph.term]
        else :
            return [(a - 1, b), (a, b - 1), (a, b + 1), graph.term]
            
    elif b == 0 : 
        return [(a - 1, b), (a, b + 1), (a + 1, b), graph.term]
        
    elif b == m :
        return [(a - 1, b), (a, b - 1), (a + 1, b), graph.term]
    return [(a - 1, b), (a, b - 1), (a + 1, b), (a, b + 1), graph.term]

a = imread("lena.png")[150:160,50:60] > 0.2
g = imgraph(a, 3)

def growth(g, A):
    '''Première coordonnée : étiquette, Seconde : actif si 1, Troisième : dans S si 1, Quatrième : parent'''
    if g.term[2] == 1:
        P = path(g.root, g.term, g.tab[:,:,3])
    while A:
        p = A.pop()
        for q in neighbours(g, p):
            if g.flow(p, q) != 0 and :
                q[2] = 1
                if q[1] = 0:
                    q[1] = 1
                    A.append(q)
                    q[3] = p
                if q = g.term:
                    P = path(g.root, g.term, g.tab[:,:,3])
        p[1] = 0
        
        # Augmentation #
        
        n = len(P)
        argmin = 0
        min = g.flow(P[0], P[1])
        for k in range(n-1):
            temp = g.flow(P[k], P[k+1])
            if temp < min :
                argmin = k
                min = temp
        for k in range(n-1):
            g.setflow(P[k], P[k+1], g.flow(P[k], P[k+1]) - min)
        orphans = []
        for k in range(n-1):
            if g.flow(P[k], P[k+1]) == 0:
                orphans.append(P[k+1])
        
        # Adoption #
        
        while 

def augmentation(P, g):
    
    