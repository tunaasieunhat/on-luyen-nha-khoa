# Gom out/bN.json -> out/videos.json (dữ liệu nhúng vào app)
import json, os, glob, re
D = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(D, 'slides.json'), encoding='utf8'))
V = {}
for f in sorted(glob.glob(os.path.join(D, 'out', 'b*.json'))):
    b = int(re.search(r'b(\d+)\.json', f).group(1)); d = json.load(open(f, encoding='utf8'))
    titles = []
    for k, s in enumerate(S[str(b)]):
        t = s['text'][1] if k == 0 else s['text'][0]
        titles.append(re.sub(r'^\d+(–\d+)?\.\s*', '', t))
    assert len(titles) == len(d['slides'])
    V[f'vlnk-bai-{b}'] = {'src': f'video/vlnk/b{b}.mp4', 'dur': d['dur'], 'mb': round(os.path.getsize(f[:-5] + '.mp4') / 1e6, 1),
                          'ch': [[t, ti] for t, ti in zip(d['slides'], titles)], 'cues': d['cues']}
def split(c, lim=84):
    a, b, t = c
    if len(t) <= lim: return [c]
    cuts = [m.end() for m in __import__('re').finditer(r'[,:;.?] ', t)] or [m.end() for m in __import__('re').finditer(r' ', t)]
    k = min(cuts, key=lambda x: abs(x - len(t) / 2))
    x, y = t[:k].strip(), t[k:].strip(); m = round(a + (b - a) * len(x) / (len(x) + len(y)), 2)
    return split([a, m, x], lim) + split([m, b, y], lim)
for v in V.values(): v['cues'] = [z for c in v['cues'] for z in split(c)]
json.dump(V, open(os.path.join(D, 'out', 'videos.json'), 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
print({k: (round(v['dur'] / 60, 1), v['mb'], len(v['cues'])) for k, v in V.items()})
