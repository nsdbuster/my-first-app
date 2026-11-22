import json
P=json.load(open('puzzle.json'));CQ=json.load(open('clues.json'))
dev=lambda n:''.join('०१२३४५६७८९'[int(d)] for d in str(n))
N=P['N'];g=P['grid'];num=P['num']
def grid(ans):
    h=''
    for r in range(N):
        for c in range(N):
            k=f'{r},{c}'
            if k not in g: h+='<div class="b"></div>';continue
            n=f'<span class="n">{dev(num[k])}</span>' if k in num else ''
            h+=f'<div class="w">{n}<span class="l">{g[k] if ans else ""}</span></div>'
    return f'<div class="grid">{h}</div>'
def clues(d):
    return '; '.join(f'<b>{dev(e["n"])}.</b> {CQ["".join(e["a"])]}' for e in P['entries'] if e['d']==d)
CSS='''<link href="https://fonts.googleapis.com/css2?family=Tiro+Devanagari+Marathi&family=Mukta:wght@400;600;800&display=swap" rel="stylesheet">
<style>*{box-sizing:border-box}body{margin:0;background:#fff;color:#111;font-family:Mukta,sans-serif}
.page{width:1080px;padding:44px 48px 40px;border:0}
.frame{border:3px solid #111;padding:26px 28px 22px}
.hd{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:3px double #111;padding-bottom:10px;margin-bottom:22px}
h1{font-family:"Tiro Devanagari Marathi",serif;font-weight:400;font-size:64px;margin:0;line-height:1}
.sub{font-size:24px;font-weight:600;text-align:right;line-height:1.3}
.grid{display:grid;grid-template-columns:repeat(11,1fr);border:3px solid #111;width:100%;aspect-ratio:1;background:#111;gap:2px}
.w{background:#fff;position:relative;display:flex;align-items:center;justify-content:center}
.b{background:#111}
.n{position:absolute;top:2px;left:5px;font-size:20px;font-weight:600;line-height:1}
.l{font-family:"Tiro Devanagari Marathi",serif;font-size:46px;padding-top:12px;color:#123d8a}
.cl{font-size:27px;line-height:1.55;margin-top:22px;text-align:justify}
.cl h2{display:inline;font-size:29px;font-weight:800;margin:0}
.cl b{font-weight:800}
.ft{margin-top:18px;border-top:1px dotted #111;padding-top:10px;font-size:23px;display:flex;justify-content:space-between;font-weight:600}
</style>'''
def page(ans):
    body=f'<div class="page"><div class="frame"><div class="hd"><h1>शब्दखेळ</h1><div class="sub">मराठी शब्दकोडे क्र. १<br>{"उत्तर" if ans else "११ × ११ · ४० शब्द"}</div></div>{grid(ans)}'
    if ans:
        body+='<div class="cl"><h2>आडवे :</h2> '+'; '.join(f'<b>{dev(e["n"])}.</b> {"".join(e["a"])}' for e in P['entries'] if e['d']=='A')+'</div>'
        body+='<div class="cl"><h2>उभे :</h2> '+'; '.join(f'<b>{dev(e["n"])}.</b> {"".join(e["a"])}' for e in P['entries'] if e['d']=='D')+'</div>'
    else:
        body+=f'<div class="cl"><h2>आडवे शब्द :</h2> {clues("A")}</div><div class="cl"><h2>उभे शब्द :</h2> {clues("D")}</div>'
        body+='<div class="ft"><span>प्रत्येक घरात एक अक्षर (जोडाक्षरासह)</span><span>(उत्तर नंतर पाठवले जाईल)</span></div>'
    body+='</div></div>'
    return '<html><head><meta charset="utf-8">'+CSS+'</head><body>'+body+'</body></html>'
open('puzzle.html','w').write(page(False));open('answer.html','w').write(page(True))
