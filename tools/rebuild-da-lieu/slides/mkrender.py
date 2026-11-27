# trang vẽ slide Da Liễu để chụp/in: python3 mkrender.py
import json, os
D = os.path.dirname(os.path.abspath(__file__)); A = '/home/claude/on-luyen-nha-khoa/avcn2-src'
css = open(A + '/avs.css', encoding='utf8').read() + open(D + '/dls.css', encoding='utf8').read()
decks = json.load(open(D + '/out/decks.json', encoding='utf8'))
# bản in: thêm slide đáp án sau mỗi slide trắc nghiệm
pr = {}
for k, S in decks.items():
    out = []
    for s in S:
        out.append(s)
        if s['k'] == 'quiz': out.append({**s, 'k': 'ans', 'title': 'Đáp án · ' + s['title'].split(': ', 1)[-1]})
    pr[k] = out
js = open(A + '/avs.js', encoding='utf8').read().replace('__AVS_DATA__', '{}').replace('__AVS_META__', '{}')
js += open(D + '/dls.js', encoding='utf8').read().replace('__DLS_DATA__', json.dumps(decks, ensure_ascii=False))
js += '\nvar DLS_PRINT = ' + json.dumps(pr, ensure_ascii=False) + ';\nDLS_BASE = "../fig/";\n'
html = f'''<!doctype html><html><head><meta charset="utf-8"><style>{css}
html,body{{margin:0;background:#fff}}
.frame{{width:1280px;height:720px;overflow:hidden;container-type:inline-size;background:#FFFCFD;position:relative}}
.avs{{min-height:720px}}
.avs,.avs *{{font-family:Carlito,"DejaVu Sans",sans-serif!important}}
.avs h2,.avs h3,.avs .big-u,.avs .q .qn,.avs .ans b.n{{font-family:Carlito,sans-serif!important;font-weight:700}}
.avs .top,.avs .lbl,.avs .course,.avs .opt i,.avs .q .ql{{font-family:Carlito,sans-serif!important;font-weight:700}}
</style></head><body><div class="frame" id="f"></div><script>{js}
function show(u,i,pr){{const S=(pr?DLS_PRINT:DLS_DECKS)[u];document.getElementById('f').innerHTML=dlsSlide(S,i,true);const a=document.querySelector('.avs');let f=parseFloat(getComputedStyle(a).fontSize),k=0;while(a.scrollHeight>720&&k<30){{f-=.5;a.style.setProperty('--fs',f+'px');k++;}}return {{h:a.scrollHeight,n:S.length,shrink:k}};}}
</script></body></html>'''
open(D + '/render/index.html', 'w', encoding='utf8').write(html); print('ok')
