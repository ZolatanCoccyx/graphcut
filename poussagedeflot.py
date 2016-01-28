## Classes

import time
import numpy as np
import imageio
import scipy as sc
from matplotlib.pyplot import *

# a = imread("lena3.png")<0.5
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


## Poussage par flot

# a=a[:,:,1]
a=np.matrix([[0.4,0.4,0.8,0.9,0.9],[0.2,0.3,0.4,0.56,0.57],[0.1,0.4,0.9,0.8,0.9],[0.2,0.2,0.6,0.6,0.6],[0.1,0.1,0.6,0.6,0.6]])<0.5
g = picg(a,0.7)

def poussage(g):
    n=g.dim[0]
    La=np.zeros((n,n))+1
    lar=n**2
    lat=0
    g.flot.lr=np.zeros((n,n))
    g.flot.tb=np.zeros((n,n))
    g.flot.term=np.zeros((n,n))
    A=[(i,j) for i in range(n) for j in range(n)]
    while len(A)>0:
        i=A[0]
        i1,i2=i
        e=-g.weight(i,(i1+1,i2))+g.flot(i,(i1+1,i2))-g.weight(i,(i1,i2-1))+g.flot(i,(i1,i2-1))-g.weight(i,(i1-1,i2))+g.flot(i,(i1-1,i2))-g.weight(i,(i1,i2+1))+g.flot(i,(i1,i2+1))-g.weight(i,"term")+g.flot(i,"term")-g.weight(i,"root")+g.flot(i,"root")
        # print(e)
        while len(A) and A[0]==i:
            compt=0
            j1=(i1+1,i2)
            j2=(i1,i2+1)
            j3=(i1,i2-1)
            j4=(i1-1,i2)
            if La[i]==lat+1:
                r=g.flot(i,"term")
                if r>0:
                    k=g.flot(i,"term")
                    g.flot.bob(i,"term",k-min(r,e))
                    compt=1
            if compt==0 and i1!=n-1 and La[i]==La[j1]+1:
                r=g.flot(i,j1)
                if r>0:
                    k=g.flot(i,j1)
                    # print([k,e,r])
                    g.flot.bob(i,j1,k-min(r,e))
                    compt=1
                    # print(g.flot(i,j1))
            if compt==0 and i2!=n-1 and La[i]==La[j2]+1:
                r=g.flot(i,j2)
                if r>0:
                    k=g.flot(i,j2)
                    # print([k,e,r,j2])
                    g.flot.bob(i,j2,k-min(r,e))
                    compt=1
            if compt==0 and i2!=0 and La[i]==La[j3]+1:
                r=g.flot(i,j3)
                if r>0:
                    k=g.flot(i,j3)
                    # print([k,e,r,j3])
                    g.flot.bob(i,j3,k-min(r,e))
                    compt=1
            if compt==0 and i1!=0 and La[i]==La[j4]+1:
                r=g.flot(i,j4)
                # print([r,j4])
                if r>0:
                    k=g.flot(i,j4)
                    g.flot.bob(i,j4,k-min(r,e))
                    compt=1
            e=-g.weight(i,(i1+1,i2))+g.flot(i,(i1+1,i2))-g.weight(i,(i1,i2-1))+g.flot(i,(i1,i2-1))-g.weight(i,(i1-1,i2))+g.flot(i,(i1-1,i2))-g.weight(i,(i1,i2+1))+g.flot(i,(i1,i2+1))-g.weight(i,"term")+g.flot(i,"term")-g.weight(i,"root")+g.flot(i,"root")
            # print([e,compt])
            if e==0:
                A.remove(i)
            if compt==0:
                k1=float('infinity')
                k2=float('infinity')
                k3=float('infinity')
                k4=float('infinity')
                if i1!=n-1 and g.flot(i,j1)>0:
                    k1=La[j1]+1
                if i1!=0 and g.flot(i,j4)>0:
                    k4=La[j4]+1
                if i2!=0 and g.flot(i,j3)>0:
                    k3=La[j3]+1
                if i2!=n-1 and g.flot(i,j2)>0:
                    k2=La[j2]+1
                # print(k1,k2,k3,k4)
                La[i]=min(k1,k2,k3,k4)
                # print(La)
            # print(A)
    return([g.flot.lr,g.flot.tb])

t=time.time()
K=poussage(g)
lr=K[0]
tb=K[1]
Llr=lr[1:,:]-lr[:-1,:]
# Ltb=tb[1:,:]-tb[:-1,:]
# Clr=lr[:,1:]-lr[:,:-1]
Ctb=tb[:,1:]-tb[:,:-1]
Nlr=np.sqrt(Llr[:,:-1]**2+Ctb[:-1,:]**2)
print(time.time()-t)
imshow(Nlr,cmap=cm.gray)