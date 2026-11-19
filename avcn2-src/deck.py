# Slide Anh văn chuyên ngành 2 (Version 2.6.3): dựng dữ liệu bộ slide từng Unit từ w*.txt (2.6.1) + ex*.txt (ví dụ thêm)
# python3 deck.py -> out/decks.json (đủ, có slide đáp án cho PowerPoint/bản in) + out/decks-app.json (cho app)
import json, os, random, re, sys
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/claude/work261')
import parse
from exparse import load_ex, has
U, W = parse.load(); E = load_ex()
TITLES = {1: 'The dentist – Nha sĩ và nghề nha', 2: 'Dental specialties – Các chuyên khoa', 3: 'The dental office – Khu vực phòng khám',
          4: 'Dental staff – Nhân sự phòng khám', 5: 'Dental instruments – Dụng cụ nha khoa', 6: 'The mouth – Khoang miệng',
          7: 'Tooth anatomy – Cấu tạo răng', 8: 'Types of teeth – Các loại răng', 9: 'Infection control – Kiểm soát lây nhiễm',
          10: 'Dental technology – Công nghệ nha khoa', 11: 'Appointments – Lịch hẹn', 12: 'Payment and insurance – Thanh toán, bảo hiểm',
          13: 'Patient communication – Giao tiếp bệnh nhân', 14: 'Oral hygiene – Vệ sinh răng miệng', 15: 'Teeth cleaning – Làm sạch răng'}
POS = {'N-COUNT': 'danh từ (đếm được)', 'N-UNCOUNT': 'danh từ (không đếm được)', 'N-PLURAL': 'danh từ số nhiều', 'VERB': 'động từ',
       'ADJ': 'tính từ', 'ADV': 'trạng từ', 'V-T': 'động từ (cần tân ngữ)', 'V-I': 'động từ (không cần tân ngữ)', 'N': 'danh từ', 'ABBREVIATION': 'chữ viết tắt', 'PHRASAL VERB': 'cụm động từ', 'NOUN': 'danh từ'}
LET = 'ABCD'


def blank(term, s):
    return re.sub(r'(?<![A-Za-z])' + re.escape(term) + r'(?![A-Za-z])', '_____', s, count=0, flags=re.I)


def pos_vi(p):
    if not p: return ''
    return ' · '.join(POS.get(x.strip(), x.strip().lower()) for x in p.split('/'))


def word_slide(t):
    w = W[t]
    exs = [[w['ex'], w['exv']]] + E[t]
    return {'k': 'word', 'u': w['u'], 't': t, 'ipa': w['ipa'], 'say': w['say'], 'm': w['m'], 'pos': pos_vi(w.get('pos')), 'hook': w['hook'],
            'ex': exs, 'def': w['en'], 'defv': ' '.join(c[1] for c in w['ch']).replace(' ,', ','), 'kw': w.get('kw', '')}


def cls(t):
    p = (W[t].get('pos') or 'N')[0]
    return 'N' if p == 'N' else 'V' if p == 'V' else 'A'


def question(rng, kind, t, pool, exi=1):
    w = W[t]
    if kind == 'fill' and cls(t) == 'A': kind = 'def'  # tính từ dễ có nhiều đáp án hợp nghĩa
    others = [x for x in pool if x != t]
    if kind == 'fill':
        # đáp án nhiễu lấy ở Unit khác, cùng loại từ, cùng số chữ: tránh câu có hai đáp án hợp nghĩa
        nw = len(t.split())
        cand = [x for x in W if W[x]['u'] != w['u'] and cls(x) == cls(t) and len(x.split()) == nw and not has(x, E[t][exi][0])]
        if len(cand) < 3: cand = [x for x in W if W[x]['u'] != w['u'] and cls(x) == cls(t)]
        others = sorted(cand)
    rng.shuffle(others)
    if kind == 'mean':
        opts = [W[x]['m'] for x in others[:3]] + [w['m']]
    else:
        opts = others[:3] + [t]
    order = list(range(4)); rng.shuffle(order)
    opts = [opts[i] for i in order]; a = order.index(3)
    if kind == 'def':
        q = {'lab': 'Định nghĩa → từ (giống đề thi)', 'p': blank(t, w['en']), 'why': f'{t} = {w["m"]}.' + (f' Dấu hiệu nhận ra: “{w["kw"]}”.' if w.get('kw') else '')}
    elif kind == 'fill':
        en, vi = E[t][exi]
        q = {'lab': 'Điền từ vào câu', 'p': blank(t, en), 'why': f'{en} → {vi}'}
    elif kind == 'vi':
        q = {'lab': 'Nghĩa tiếng Việt → từ tiếng Anh', 'p': f'“{w["m"]}” trong tiếng Anh là từ nào?', 'why': f'{t} {w["ipa"]}: {w["m"]}.'}
    elif kind == 'mean':
        q = {'lab': 'Từ → nghĩa', 'p': f'“{t}” nghĩa là gì?', 'why': f'{t} {w["ipa"]}: {w["m"]}. Mẹo nhớ: {w["hook"]}'}
    elif kind == 'say':
        q = {'lab': 'Nghe cách đọc → từ', 'p': f'Từ nào đọc gần giống “{w["say"]}”?', 'why': f'{t} {w["ipa"]}, đọc gần giống “{w["say"]}”.', 'speak': t}
    q.update({'kind': kind, 't': t, 'o': opts, 'a': a})
    return q


def unit_deck(u):
    rng = random.Random(2630 + u)
    order = U[u]['order']; n = len(order)
    title = TITLES[u]; en, _, vi = title.partition(' – ')
    S = [{'k': 'title', 'u': u, 'en': en, 'vi': vi, 'n': n, 'mins': round(n * 2.2 + 6)},
         {'k': 'intro', 'u': u, 'intro': U[u]['intro'], 'how': [
             'Bấm nút loa để nghe đọc từ. Đọc to theo 3 lần.',
             'Nhìn dòng “Đọc gần giống” nếu chưa quen phiên âm.',
             'Đọc 3 câu ví dụ, rồi đọc câu định nghĩa: đề thi cho định nghĩa, bạn chọn từ.',
             'Cứ 4 từ có một bài trắc nghiệm nhanh. Cuối bài có bài kiểm tra cả Unit.']},
         {'k': 'map', 'u': u, 'words': [[t, W[t]['m']] for t in order]}]
    groups = [order[i:i + 4] for i in range(0, n, 4)]
    if len(groups) > 1 and len(groups[-1]) < 3:  # nhóm cuối quá ít thì gộp
        last = groups.pop(); groups[-1] = groups[-1] + last
    kinds = ['def', 'fill', 'vi', 'mean']
    seen = []
    for gi, g in enumerate(groups):
        for t in g: S.append(word_slide(t))
        seen += g
        pick = g[:]; rng.shuffle(pick); pick = pick[:3]
        ks = kinds[:]; rng.shuffle(ks)
        qs = [question(rng, ks[i], t, order) for i, t in enumerate(pick)]
        S.append({'k': 'quiz', 'u': u, 'title': f'Trắc nghiệm nhanh {gi + 1}', 'sub': 'Ôn ' + ', '.join(g), 'q': qs})
    S.append({'k': 'recap', 'u': u, 'words': [[t, W[t]['ipa'], W[t]['m']] for t in order]})
    asked = [q['t'] for s in S if s['k'] == 'quiz' for q in s['q']]
    rest = [t for t in order if t not in asked]; rng.shuffle(rest)
    again = [t for t in order if t in asked]; rng.shuffle(again)
    pick = (rest + again)[:8]
    done = {(q['t'], q['kind']) for s in S if s['k'] == 'quiz' for q in s['q']}
    fk = ['def', 'def', 'fill', 'say', 'vi', 'mean', 'def', 'fill']
    qs = []
    for i, t in enumerate(pick):
        k = fk[i]
        if (t, k) in done: k = next(x for x in ['def', 'say', 'mean', 'vi', 'fill'] if (t, x) not in done)
        qs.append(question(rng, k, t, order, exi=0))
    S.append({'k': 'quiz', 'u': u, 'final': True, 'title': 'Kiểm tra cuối Unit', 'sub': f'{len(qs)} câu, trộn mọi dạng', 'q': qs})
    S.append({'k': 'end', 'u': u, 'next': TITLES.get(u + 1, '')})
    return S


def with_answers(S):
    out = []
    for s in S:
        if s['k'] != 'quiz': out.append(s); continue
        qs = s['q']
        per = 4 if s.get('final') else 3
        chunks = [qs[i:i + per] for i in range(0, len(qs), per)]
        for ci, ch in enumerate(chunks):
            base = ci * per
            t = s['title'] + (f' ({ci + 1}/{len(chunks)})' if len(chunks) > 1 else '')
            out.append({**s, 'title': t, 'q': ch, 'base': base})
            out.append({'k': 'ans', 'u': s['u'], 'title': 'Đáp án · ' + t, 'q': ch, 'base': base})
    return out


decks = {u: unit_deck(u) for u in sorted(U) if u >= 1}
os.makedirs(os.path.join(D, 'out'), exist_ok=True)
full = {f'avcn2-u{u}': with_answers(S) for u, S in decks.items()}
app = {k: [s for s in S if s['k'] != 'ans'] for k, S in full.items()}  # app: trắc nghiệm bấm chọn, không cần slide đáp án
json.dump(app, open(os.path.join(D, 'out', 'decks-app.json'), 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
json.dump(full, open(os.path.join(D, 'out', 'decks.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print({k: (len(v), len(full[k])) for k, v in app.items()}, os.path.getsize(os.path.join(D, 'out', 'decks-app.json')), 'bytes')
# kiểm tra
for k, S in full.items():
    for s in S:
        if s['k'] in ('quiz', 'ans'):
            for q in s['q']:
                assert len(set(q['o'])) == 4, (k, q)
                if q['kind'] in ('def', 'fill'): assert '_____' in q['p'], (k, q['t'], q['p'])
