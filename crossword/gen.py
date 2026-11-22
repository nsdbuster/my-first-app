import re,random,sys,json
C='[क-हक़-य़ॸ-ॿ]';V='[ऄ-औॠॡॲ-ॷ]'
CL=re.compile(f'(?:{C}़?(?:्{C}़?)*्?|{V})[ा-ौॢॣ]*[ऀ-ः]*')
D={}
for l in open('dict.txt'):
    w,q=l.strip().split('|');t=tuple(CL.findall(w))
    assert ''.join(t)==w,(w,t)
    if len(t)>=2: D.setdefault(t,q)
W=list(D);print(len(W),'words',file=sys.stderr)
N=11
def runs(g):
    out=[]
    for d,(dr,dc) in (('A',(0,1)),('D',(1,0))):
        for r in range(N):
            for c in range(N):
                if (r,c) in g and (r-dr,c-dc) not in g:
                    t=[];rr,cc=r,c
                    while (rr,cc) in g: t.append(g[(rr,cc)]);rr+=dr;cc+=dc
                    if len(t)>=2: out.append((r,c,d,tuple(t)))
    return out
def valid_after(g,cells):
    # check runs through new cells
    for (r,c) in cells:
        for dr,dc in ((0,1),(1,0)):
            rr,cc=r,c
            while (rr-dr,cc-dc) in g: rr-=dr;cc-=dc
            t=[]
            while (rr,cc) in g: t.append(g[(rr,cc)]);rr+=dr;cc+=dc
            if len(t)>=2 and tuple(t) not in D: return False
    return True
def attempt(rnd):
    g={}
    w=rnd.choice([x for x in W if len(x)>=4]);r=rnd.randrange(N);
    for i,a in enumerate(w): g[(0 if rnd.random()<.5 else r, i)]=a
    g={}; 
    for i,a in enumerate(w): g[(r,i)]=a
    fails=0
    while fails<600:
        w=rnd.choice(W);d=rnd.choice('AD');dr,dc=(0,1) if d=='A' else (1,0)
        L=len(w)
        if d=='A': r=rnd.randrange(N);c=rnd.randrange(N-L+1)
        else: r=rnd.randrange(N-L+1);c=rnd.randrange(N)
        cells=[(r+dr*i,c+dc*i) for i in range(L)]
        if any(k in g and g[k]!=a for k,a in zip(cells,w)) or all(k in g for k in cells): fails+=1;continue
        contact=any(k in g for k in cells) or any((a+x,b+y) in g for a,b in cells for x,y in((0,1),(1,0),(0,-1),(-1,0)))
        if not contact: fails+=1;continue
        if (r-dr,c-dc) in g or (r+dr*L,c+dc*L) in g: fails+=1;continue
        new=[k for k in cells if k not in g]
        for k,a in zip(cells,w): g[k]=a
        ws=[x[3] for x in runs(g)]
        if not valid_after(g,new) or len(ws)!=len(set(ws)):
            for k in new: del g[k]
            fails+=1;continue
        fails=0
    return g
best=(0,None)
seed=int(sys.argv[1]) if len(sys.argv)>1 else 0
rnd=random.Random(seed)
for it in range(int(sys.argv[2]) if len(sys.argv)>2 else 300):
    g=attempt(rnd)
    rs=runs(g)
    # every cell must be in some run
    sc=len(g)
    if sc>best[0]: best=(sc,g)
sc,g=best
print(sc,file=sys.stderr)
for r in range(N): print(' '.join((g.get((r,c)) or '■').ljust(4) for c in range(N)),file=sys.stderr)
json.dump({'g':{f'{r},{c}':v for (r,c),v in g.items()},'clues':{''.join(k):v for k,v in D.items()}},open(f'out{seed}.json','w'),ensure_ascii=False)
print(sc)
