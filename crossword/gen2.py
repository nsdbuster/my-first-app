import re,random,sys,json
exec(open('gen.py').read().split('def attempt')[0].replace("print(len(W),'words',file=sys.stderr)",""))
from collections import defaultdict
idx=defaultdict(list)
for w in W:
    for i,a in enumerate(w): idx[a].append((w,i))
def placements(g,used):
    out=[]
    for (r0,c0),a in g.items():
        for w,i in idx[a]:
            if w in used: continue
            for d in 'AD':
                dr,dc=(0,1) if d=='A' else (1,0)
                r,c=r0-dr*i,c0-dc*i;L=len(w)
                if r<0 or c<0 or r+dr*(L-1)>=N or c+dc*(L-1)>=N: continue
                if (r-dr,c-dc) in g or (r+dr*L,c+dc*L) in g: continue
                cells=[(r+dr*k,c+dc*k) for k in range(L)]
                if any(k in g and g[k]!=x for k,x in zip(cells,w)): continue
                new=[k for k in cells if k not in g]
                if not new: continue
                out.append((w,cells,new,L-len(new)))
    return out
def attempt(rnd):
    w=rnd.choice([x for x in W if len(x)>=4]);r=rnd.randrange(N);c=rnd.randrange(N-len(w)+1)
    g={(r,c+i):a for i,a in enumerate(w)}
    used={w}
    while True:
        P=placements(g,used);rnd.shuffle(P)
        P.sort(key=lambda p:-(p[3]*2+len(p[2])*0.7+rnd.random()*3))
        ok=False
        for w,cells,new,x in P[:400]:
            for k,a in zip(cells,w): g[k]=a
            ws=[t[3] for t in runs(g)]
            if valid_after(g,new) and len(ws)==len(set(ws)):
                used=set(ws);ok=True;break
            for k in new: del g[k]
        if not ok: return g
seed=int(sys.argv[1]);rnd=random.Random(seed);best=(0,None)
for it in range(int(sys.argv[2])):
    g=attempt(rnd)
    if len(g)>best[0]: best=(len(g),g)
sc,g=best
for r in range(N): print(' '.join((g.get((r,c)) or '■').ljust(4) for c in range(N)),file=sys.stderr)
print(sc,len(runs(g)),file=sys.stderr)
json.dump({f'{r},{c}':v for (r,c),v in g.items()},open(f'g{seed}.json','w'),ensure_ascii=False)
