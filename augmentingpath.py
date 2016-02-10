a=np.matrix([[0.1,0.1,0.6],[0.1,0.6,0.6],[0.6,0.6,0.6]])<0.5

def neighbours2(g,node):
    m, n = g.dim
    
    if node == (-1,0):
        return [(i, j) for i in range(m) for j in range(n)]
        
    if node == (0,-1):
        return [(i, j) for i in range(m) for j in range(n)]
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
        
    elif b == m-1 :
        return [(a - 1, b), (a, b - 1), (a + 1, b), (0,-1)]
    return [(a - 1, b), (a, b - 1), (a + 1, b), (a, b + 1), (0,-1)]

def treeflow(g,a,b):
    
    if g(a)[2]==1:
        return(g.flow(a,b))
    elif g(a)[2]==2:
        return(g.flow(b,a))
    else:
        return False

def growth(g,A):
    while A:
        p=A.pop()
        A.append(p)
        # print(p)
        for q in neighbours2(g,p):
            if treeflow(g,p,q)>0:
                if g(q)[2]==0:
                    g(q)[2]=g(p)[2]
                    g(q)[3],g(q)[4]=p
                    if not (q in A):
                        A.append(q)
                        g(q)[1]=1
                elif g(q)[2]!=0 and g(q)[2]!=g(p)[2]:
                    P=path2(p,q,g)
                    return P
        A.remove(p)
        g(p)[1]=0
    return []

g=imgraph(a,5)
    
##
def path(a,b,g):
    P=[b]
    if a==b:
        return P
    temp1,temp2=b
    temp=(temp1,temp2)
    while temp!=a:
        temp1=g((temp1,temp2))[3]
        temp2=g(temp)[4]
        temp=(temp1,temp2)
        P.append(temp)
    P.reverse()
    return P

def path2(a,b,g):
    R=[]
    P=[]
    Q=[]
    if g(a)[2]==1:
        P=path((-1,0),a,g)
        Q=path((0,-1),b,g)
        Q.reverse()
        R=P+Q
    else:
        P=path((-1,0),b,g)
        Q=path((0,-1),a,g)
        Q.reverse()
        R=P+Q
    return R
    


##

def augmentation(g,P):
    O=[]
    n=len(P)
    K=[]
    delta=min([np.abs(g.flow(P[j],P[j+1])) for j in range(n-1)])
    for j in range(n-1):
        i1=P[j]
        i2=P[j+1]
        k=g.flow(i1,i2)
        if k<0:
            setflow(i1,i2,k+delta)
        elif k>=0:
            setflow(i1,i2,k-delta)
        if g.flow(i1,i2)==0:
            K.append(j)
    for j in K:
        p=P[j]
        q=P[j+1]
        if g(p)[2]==g(q)[2]:
            if g(p)[2]==1:
                g(q)[3],g(q)[4]=0.5,0.5
                O.append(q)
            elif g(p)[2]==2:
                g(p)[3],g(p)[4]=0.5,0.5
                O.append(p)
    return(O)

def adoption(g,O,A):
    while O:
        p=O.pop()
        process(g,p,A,O)

def process(g,p,A,O):
    compt=0
    L=neighbours2(g,p)
    L.append((-1,0))
    for j in L:
        if g(j)[2]==g(p)[2] and treeflow(g,j,p)>0:
            g(p)[3],g(p)[4]=j
            compt=1
            break
    if compt==0:
        for q in L:
            if g(p)[2]==g(q)[2]:
                if treeflow(g,q,p)>0:
                    A.append(q)
                    g(q)[1]=1
                if (g(q)[3],g(q)[4])==p:
                    O.append(q)
                    g(q)[3],g(q)[4]=0.5,0.5
        g(p)[2]=0
        g(p)[1]=0
        if p in A:
            A.remove(p)

g=imgraph(a,5)

def augmingpath(g):
    m,n=g.dim
    g.root[1]=1
    g.term[1]=1
    g.root[2]=1
    g.term[2]=2
    g.root[3:5]=[0.5,0.5]
    g.term[3:5]=[0.5,0.5]
    A=[(-1,0),(0,-1)]
    g.tab[:,:,3]=np.zeros((m,n))+0.5
    g.tab[:,:,4]=np.zeros((m,n))+0.5
    O=[]
    while True:
        P=growth(g,A)
        # print(['fin augmentation'])
        # input()
        if P==[]:
            break
        # print('debut augmentation')
        O=augmentation(g,P)
        # print([g.flow.root])
        # print([g.flow.term])
        # print([g.flow.lr])
        # print([g.flow.tb])
        # print([O,'orphan'])
        # input()
        adoption(g,O,A)
        # print(['fin cycle'])
    # print('resultats')
    # print([g.flow.root])
    # print([g.flow.term])
    # print([g.flow.lr])
    # print([g.flow.tb])
    # print([g.tab[:,:,2]])
    return(g.tab[:,:,2])

# augmingpath(g)

## test
import pylab as plt
import time
import matplotlib.pyplot

a=imread('lena.png')
a=a[0:51,0:51,0]
b=np.random.normal(0,1,a.shape)
a=a+b*0.1
a=a<0.5

a[10,10]=1
g=imgraph(a,5)

t=time.time()
T=augmingpath(g)
print(time.time()-t)

## test 2

a=imread('a2.png')
