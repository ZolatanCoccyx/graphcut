def growth(g,A):
    while A:
        p=A.pop()
        for q in neighbours(g,p):
            if g.flow(p,q)!=0:
                if g(q)[2]==0:
                    g(q)[2]=g(p)[2]
                    g(q)[3],g(q)[4]=p
                    A.append(q)
                elif g(q)[2]!=g(p)[2]:
                    P=path(g.root,g.term,g)
                    return P
        A.remove(p)
    return []

def path(a,b,g):
    P=[b]
    temp1,temp2=g(b)[3],g(b)[4]  
    temp=(temp1,temp2)  
    if temp and temp!=a:
        temp1=temp[3]
        temp2=temp[4]
        temp=(temp1,temp2)
        P.append(temp)
    if temp:
        return P.reverse()
    return False


def augmentation(g,P):
    n=len(P)
    K=[]
    O=[]
    delta=min([g.flow(P[j],P[j+1]) for j in range(n-1)])
    for j in range(n-1):
        i1=P[j]
        i2=P[j+1]
        print(i1,i2)
        # k=g.flow(i1,i2)
        # g.flow(i1,i2)=k-delta
        if g.flow(i1,i2)==0:
            K.append(j)
    for j in K:
        p=P[j]
        q=P[j+1]
        if p[2]==q[2]:
            if g(p)[2]==1:
                g(q)[3],g(q)[4]=False,False
                O.append(q)
            if p[2]==2:
                g(p)[3],g(p)[4]=False, False
                O.append(p)


def adoption(g,O):
    while O:
        p=O.pop()
        process(g,p)

def process(g,p):
    compt=0
    L=neighbours(p)
    L.remove(g.term)
    L.append(g.root)
    for j in L:
        if g(j)[2]==g(p)[2] and g.flow(j,p)>0:
            g(p)[3],g(p)[4]=j
            compt=1
            break
    if compt==0:
        for q in L:
            if g(p)[2]==g(q)[2]:
                if g.flow(q,p)>0:
                    A.append(q)
                if (g(q)[3],g(q)[4])==p:
                    O.append(q)
                    g(q)[3],g(q)[4]=False, False
        g(p)[2]=0
        A.remove(p)

def augmingpath(g):
    g.root[1]=1
    g.term[1]=1
    g.root[2]=1
    g.term[2]=2
    while True:
        grow(g,A)
        if P==[]:
            break
        augmentation(g,P)
        adoption(g,O)