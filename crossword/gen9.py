import json,random,sys,time
exec(open('gen3.py').read().split('specs=')[0])
easy=set(open('easy.txt').read().split())
banned|={t for t in D if ''.join(t) in easy}
out=[]
for pi in range(6):
    W=[w for w in D if w not in banned]
    att=mk(9,W);rnd=random.Random(900+pi);best=None;t0=time.time()
    for _ in range(2500):
        g,R=att(rnd)
        sc=len(g)+sum(len(t) for *_,t in R)*0.3
        if best is None or sc>best[2]: best=(g,R,sc)
    g,R,_=best
    for r,c,d,t in R: banned.add(t)
    print(pi,len(W),len(g),len(R),round(time.time()-t0),file=sys.stderr)
    for r in range(9): print(' '.join((g.get((r,c)) or '■').ljust(4) for c in range(9)),file=sys.stderr)
    out.append({'N':9,'runs':[[r,c,d,list(t),D[t]] for r,c,d,t in R]})
    json.dump(out,open('series9.json','w'),ensure_ascii=False)
