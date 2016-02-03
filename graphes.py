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
    
    def __init__(self, g, booltab, w01 = 1, w11 = 6, w00 = 6, wn = 4):
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
    
    def __init__(self, booltab, nblabel = 1, w01 = 1, w11 = 6, w00 = 6, wn = 4):
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

# a = imread("lena.png")[150:160,50:60] > 0.2
# g = imgraph(a, 3)

##Poussage de flot

a=np.matrix([[0.6,0.4,0.4,0.9,0.9],[0.2,0.3,0.4,0.56,0.57],[0.1,0.4,0.9,0.8,0.9],[0.2,0.2,0.6,0.6,0.6],[0.1,0.1,0.6,0.6,0.6]])<0.5
g=imgraph(a,5)

def poussage(g):
    n,m=g.dim
    g.tab[:,:,1]=np.zeros((n,m))+1
    g.root[1]=n*m
    g.flow.root=np.zeros((n,m))
    A=[(i,j) for i in range(n) for j in range(m)]
    while len(A)>0:
        i=A[0]
        i1,i2=i
        L=neighbours(g,i)
        L.append(g.root)
        e=sum([g.w(j,i)-np.abs(g.flow(i,j)) for j in L])
        print(i,e)
        while len(A)>0 and A[0]==i:
            compt=0
            if g.tab[i1,i2,1]==g.term[1]+1 and g.flow(i,g.term)>0:
                k=g.flow(i,g.term)
                setflow(i,g.term,k-min(k,e))
                e=e-min(e,k)
                compt=1
                print([k,g.flow(i,g.term),e,g.term])
            else:
                L=neighbours(g,i)
                L.remove(g.term)
                for j in L:
                    j1,j2=j
                    if compt==0 and g.flow(i,j)>0 and g.tab[i1,i2,1]==g.tab[j1,j2,1]+1:
                        k=g.flow(i,j)
                        setflow(i,j,k-min(k,e))
                        e=e-min(e,k)
                        compt=1
                        print(k,g.flow(i,j),e,j)
            print([e,compt])
            if e==0:
                A.remove(i)
            if compt==0:
                L=neighbours(g,i)
                L.remove(g.term)
                k1=g.root[1]
                k2=g.term[1]
                for j in L:
                    if g.flow(i,j)<=0:
                        L.remove(j)
                if g.flow(i,g.root)<=0:
                    k1=float('infinity')
                if g.flow(i,g.term)<=0:
                    k2=float('infinity')
                k=min([g.tab[j1,j2,1]+1 for (j1,j2) in L])
                g.tab[i1,i2,1]=min(k,k1,k2)
                print(g.tab[:,:,1])
            # print(A)
    return([g.flow.lr,g.flow.tb])

t=time.time()
K=poussage(g)
print(time.time()-t)
# lr=K[0]
# tb=K[1]
# Llr=lr[1:,:]-lr[:-1,:]
# # Ltb=tb[1:,:]-tb[:-1,:]
# # Clr=lr[:,1:]-lr[:,:-1]
# Ctb=tb[:,1:]-tb[:,:-1]
# Nlr=np.sqrt(Llr[:,:-1]**2+Ctb[:-1,:]**2)
# print(time.time()-t)
# imshow(Nlr,cmap=cm.gray)        





## Augmenting path


def growth(g, A):
    '''Première coordonnée : étiquette, Seconde : actif si 1, Troisième : dans S si 1, Quatrième : première coordonnée parent, Cinquième : deuxième coordonnée parent '''
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
                P[k+1][3] = False
                orphans.append(P[k+1])
        
        # Adoption #
        
        while orphans :
            orphan = orphans.pop()
            neighlist = neighbour(orphan)
            for q in neighlist:
                if g.flow(orphan, q) != 0 and q[2] == 1:
                    if path(g.root, q, g):
                        orphan[3] = q
                    else:
                        A.append(q)
                        q[1] = 1
                if not orphan[3]:
                    orphan[2] = 0
                    for q in neighlist:
                        if q[3] = orphan:
                            q[3] = False
                            orphans.append(q)
        
    
                    


    
    