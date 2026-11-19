# Đọc w*.txt -> dict từ; kiểm tra khớp Glossary (glossary.json lấy lại từ bài 2.4 trong app)
import os, re, json, glob
D = os.path.dirname(os.path.abspath(__file__))
G = json.load(open(os.path.join(D, 'glossary.json'), encoding='utf8'))
GB = {o['term']: o for o in G}
norm = lambda s: re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()

def load():
    units, words = {}, {}
    for f in sorted(glob.glob(os.path.join(D, 'w*.txt'))):
        cur = None; u = None
        for ln in open(f, encoding='utf8').read().split('\n'):
            if not ln.strip(): continue
            if ln.startswith('# U'):
                m = re.match(r'# U(\d+) \| (.+)', ln); u = int(m.group(1)); units[u] = {'intro': m.group(2).strip(), 'order': []}; continue
            tag, rest = ln[0], ln[1:].strip()
            if tag == '@':
                p = [x.strip() for x in rest.split(' | ')]; assert len(p) == 4, ln
                cur = {'t': p[0], 'ipa': p[1], 'say': p[2], 'm': p[3], 'u': u}
                assert cur['t'] not in words, ('trùng', cur['t'])
                words[cur['t']] = cur; units[u]['order'].append(cur['t'])
            elif tag == '+': cur['hook'] = rest
            elif tag == '=':
                en, _, vi = rest.partition(' => '); assert vi, ln; cur['ex'] = en.strip(); cur['exv'] = vi.strip()
            elif tag == '~':
                cur['ch'] = [[y.strip() for y in x.split(' = ', 1)] for x in rest.split(' | ')]
                assert all(len(c) == 2 and c[0] and c[1] for c in cur['ch']), ln
            else: raise SystemExit('dòng lạ: ' + ln)
    for t, w in words.items():
        if t in GB: w.update(pos=GB[t]['pos'], en=GB[t]['en'], kw=GB[t]['kw'])
    return units, words

def check(units, words):
    errs = []
    for t, w in words.items():
        if t not in GB: errs.append(f'{t}: không có trong Glossary'); continue
        o = GB[t]
        if o['unit'] != w['u']: errs.append(f'{t}: sai unit {w["u"]} != {o["unit"]}')
        for k in ('hook', 'ex', 'ch'):
            if k not in w: errs.append(f'{t}: thiếu {k}')
        if 'ex' in w and not re.search(r'(?<![A-Za-z])' + re.escape(t) + r'(?![A-Za-z])', w['ex'], re.I):
            errs.append(f'{t}: ví dụ không chứa đúng từ: {w["ex"]}')
        if 'ch' in w:
            joined = norm(' '.join(c[0] for c in w['ch']))
            if not norm(o['en']).startswith(joined):
                errs.append(f'{t}: cụm không khớp\n   cụm: {joined}\n   gốc: {norm(o["en"])}')
    for u, d in units.items():
        miss = {o['term'] for o in G if o['unit'] == u} - set(d['order'])
        if miss: errs.append(f'U{u}: thiếu {sorted(miss)}')
    return errs

if __name__ == '__main__':
    units, words = load(); e = check(units, words)
    print(len(units), 'unit', len(words), 'từ'); print('\n'.join(e) if e else 'OK')
