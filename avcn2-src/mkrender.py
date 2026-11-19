# trang vẽ slide để chụp ảnh / in (dùng font Inter có sẵn trên máy)
import json, os
D = os.path.dirname(os.path.abspath(__file__))
css = open(os.path.join(D, 'avs.css'), encoding='utf8').read()
js = open(os.path.join(D, 'avs.js'), encoding='utf8').read().replace('__AVS_DATA__', open(os.path.join(D, 'out', 'decks.json'), encoding='utf8').read())
html = f'''<!doctype html><html><head><meta charset="utf-8"><style>{css}
html,body{{margin:0;background:#fff}}
.frame{{width:1280px;height:720px;overflow:hidden;container-type:inline-size;background:#FCFEFD;position:relative}}
.avs{{min-height:720px}}
.avs,.avs *{{font-family:Carlito,"DejaVu Sans",sans-serif!important}}
.avs h2,.avs h3,.avs .big-u,.avs .mean,.avs .q .qn,.avs .ans b.n{{font-family:Carlito,sans-serif!important;font-weight:700}}
.avs .ipa{{font-family:"DejaVu Sans",sans-serif!important}}
.avs mark{{background:#FFE7A0;border-radius:2px;padding:0 2px}}
.avs .top,.avs .lbl,.avs .course,.avs .opt i,.avs .q .ql,.avs .map div::before,.avs .exs li .n{{font-family:Carlito,sans-serif!important;font-weight:700}}
</style></head><body><div class="frame" id="f"></div><script>{js}
function show(u,i){{document.getElementById('f').innerHTML=avsSlide(AVS_DECKS[u],i,true);const a=document.querySelector('.avs');let f=parseFloat(getComputedStyle(a).fontSize),k=0;while(a.scrollHeight>720&&k<30){{f-=.5;a.style.setProperty('--fs',f+'px');k++;}}return {{h:a.scrollHeight,n:AVS_DECKS[u].length,shrink:k}};}}
</script></body></html>'''
open(os.path.join(D, 'render', 'index.html'), 'w', encoding='utf8').write(html)
print('ok')
