# Chuẩn bị danh sách câu cần đọc: chữ để đọc (số → chữ, đơn vị, ký hiệu) + giọng của từng nhân vật
# python3 -I voice-src/prep.py  → voice-src/lines.json
import json, os, re
D = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open(os.path.join(D, 'raw-lines.json'), encoding='utf8'))
CAST = json.load(open(os.path.join(D, 'cast.json'), encoding='utf8'))

DG = ['không', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín']


def num(n):
    if n < 10: return DG[n]
    if n < 20: return 'mười' + ('' if n == 10 else ' ' + ('lăm' if n % 10 == 5 else DG[n % 10]))
    if n < 100:
        t, u = divmod(n, 10); s = DG[t] + ' mươi'
        return s if u == 0 else s + ' ' + {1: 'mốt', 4: 'tư', 5: 'lăm'}.get(u, DG[u])
    if n < 1000:
        h, r = divmod(n, 100); s = DG[h] + ' trăm'
        return s if r == 0 else s + ' linh ' + DG[r] if r < 10 else s + ' ' + num(r)
    raise ValueError(n)


# Cách đọc riêng (đọc trước khi đổi số chung)
SPECIAL = [
    (r'răng 38\b', 'răng ba tám'), (r'răng 45\b', 'răng bốn lăm'),
    (r'(\d+)–(\d+)', lambda m: num(int(m[1])) + ' ' + num(int(m[2]))),
    (r'(\d+),(\d+)', lambda m: num(int(m[1])) + ' phẩy ' + ' '.join(DG[int(c)] for c in m[2])),
    (r'(\d+) ?mg\b', lambda m: num(int(m[1])) + ' mi li gam'),
    (r'\bINR\b', 'I N R'),
]


def speak(t):
    s = t
    for a, b in SPECIAL: s = re.sub(a, b, s)
    s = re.sub(r'\d+', lambda m: num(int(m[0])), s)
    s = s.replace('…', '...').replace('–', ', ').replace('“', '').replace('”', '')
    assert not re.search(r'\d', s), s
    return s[:1].upper() + s[1:]


cases = {c['id']: c for c in raw['cases']}
out = []
for l in raw['lines']:
    c = cases[l['case']]
    cast = CAST['cases'][c['id']]
    who = {'pt': cast['pt'], 'fam': cast.get('fam'), 'rec': CAST['rec']}[l['w']]
    assert who, (c['id'], l['w'])
    out.append({**l, 'say': speak(l['text']), 'voice': who['voice'], 'fx': who.get('fx', '')})
json.dump({'lines': out, 'sample': CAST['sample']}, open(os.path.join(D, 'lines.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(len(out), 'câu;', len({(o['voice'], o['fx']) for o in out}), 'giọng khác nhau')
for o in out:
    if o['say'] != o['text']: print(' ', o['case'], '|', o['say'])
