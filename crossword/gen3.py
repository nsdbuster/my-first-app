import re,random,sys,json,time
from collections import defaultdict
C='[क-हक़-य़ॸ-ॿ]';V='[ऄ-औॠॡॲ-ॷ]'
CL=re.compile(f'(?:{C}़?(?:्{C}़?)*्?|{V})[ा-ौॢॣ]*[ऀ-ः]*')
D={}
for f in ('dict.txt','dict2.txt'):
    for l in open(f):
        w,q=l.strip().split('|');t=tuple(CL.findall(w));assert ''.join(t)==w,(w,t)
        if len(t)>=2: D.setdefault(t,q)
cq=json.load(open('clues.json'))
for t in list(D):
    if ''.join(t) in cq: D[t]=cq[''.join(t)]
print(len(D),'words',file=sys.stderr)
banned=set()
p2=json.load(open('puzzle.json'))
for e in p2['entries']: banned.add(tuple(e['a']))
for w in "गोदावरी दिवाळी आरती कविता गणपती वारी रायगड नागपूर वेरूळ वसंत कणा शाहीर रांगोळी लावणी सरस्वती वारकरी सिंहगड सातारा पतंग वासुदेव गवळण नारळ नाशिक तमाशा".split():
    banned.add(tuple(CL.findall(w)))
def mk(N,W):
    idx=defaultdict(list)
    for w in W:
        for i,a in enumerate(w): idx[a].append((w,i))
    Wset=set(W)
    def run_at(g,r,c,dr,dc):
        while (r-dr,c-dc) in g: r-=dr;c-=dc
        t=[]
        while (r,c) in g: t.append(g[(r,c)]);r+=dr;c+=dc
        return tuple(t)
    def runs(g):
        out=[]
        for d,(dr,dc) in (('A',(0,1)),('D',(1,0))):
            for (r,c) in g:
                if (r-dr,c-dc) not in g and (r+dr,c+dc) in g:
                    out.append((r,c,d,run_at(g,r,c,dr,dc)))
        return out
    def attempt(rnd):
        w=rnd.choice([x for x in W if len(x)>=4]);r=rnd.randrange(N);c=rnd.randrange(N-len(w)+1)
        g={(r,c+i):a for i,a in enumerate(w)};used={w}
        while True:
            P=[]
            for (r0,c0),a in g.items():
                for w,i in idx[a]:
                    if w in used: continue
                    for d in 'AD':
                        dr,dc=(0,1) if d=='A' else (1,0);r,c=r0-dr*i,c0-dc*i;L=len(w)
                        if r<0 or c<0 or r+dr*(L-1)>=N or c+dc*(L-1)>=N: continue
                        if (r-dr,c-dc) in g or (r+dr*L,c+dc*L) in g: continue
                        cells=[(r+dr*k,c+dc*k) for k in range(L)]
                        if any(k in g and g[k]!=x for k,x in zip(cells,w)): continue
                        new=[k for k in cells if k not in g]
                        if new: P.append(((L-len(new))*2+len(new)*0.7+rnd.random()*3,w,cells,new))
            P.sort(key=lambda p:-p[0]);ok=False
            for _,w,cells,new in P[:300]:
                for k,a in zip(cells,w): g[k]=a
                good=True
                for (r,c) in new:
                    for dr,dc in ((0,1),(1,0)):
                        t=run_at(g,r,c,dr,dc)
                        if len(t)>=2 and (t not in Wset or (t in used and t!=w)): good=False;break
                    if not good: break
                if good:
                    ws=[x[3] for x in runs(g)]
                    if len(ws)!=len(set(ws)): good=False
                if good: used=set(x[3] for x in runs(g));ok=True;break
                for k in new: del g[k]
            if not ok: return g,runs(g)
    return attempt
specs=[(11,1500),(11,1500),(11,1500),(13,8000),(13,8000)]
out=[]
for pi,(N,K) in enumerate(specs):
    W=[w for w in D if w not in banned]
    att=mk(N,W);rnd=random.Random(100+pi);best=None;t0=time.time()
    for _ in range(K):
        g,R=att(rnd)
        if best is None or len(g)>len(best[0]): best=(g,R)
    g,R=best
    for r,c,d,t in R: banned.add(t)
    print(pi,N,len(g),len(R),round(time.time()-t0),file=sys.stderr)
    for r in range(N): print(' '.join((g.get((r,c)) or '■').ljust(4) for c in range(N)),file=sys.stderr)
    out.append({'N':N,'cells':{f'{r},{c}':v for (r,c),v in g.items()},'runs':[[r,c,d,list(t),D[t]] for r,c,d,t in R]})
    json.dump(out,open('series.json','w'),ensure_ascii=False)
