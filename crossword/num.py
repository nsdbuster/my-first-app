import json,sys
exec(open('gen.py').read().split('def attempt')[0].replace("print(len(W),'words',file=sys.stderr)",""))
g={tuple(map(int,k.split(','))):v for k,v in json.load(open(sys.argv[1])).items()}
R=runs(g);starts=sorted({(r,c) for r,c,d,t in R});num={s:i+1 for i,s in enumerate(starts)}
ent=[dict(n=num[(r,c)],d=d,r=r,c=c,a=list(t),q=D[t]) for r,c,d,t in R]
ent.sort(key=lambda e:(e['d'],e['n']))
for e in ent: print(e['d'],e['n'],''.join(e['a']),'—',e['q'])
# cells not in any run?
inrun=set()
for r,c,d,t in R:
    for i in range(len(t)): inrun.add((r+(i if d=='D' else 0),c+(i if d=='A' else 0)))
print('orphans',[k for k in g if k not in inrun])
json.dump({'N':N,'grid':{f'{r},{c}':v for (r,c),v in g.items()},'num':{f'{r},{c}':n for (r,c),n in num.items()},'entries':ent},open('puzzle.json','w'),ensure_ascii=False,indent=0)
