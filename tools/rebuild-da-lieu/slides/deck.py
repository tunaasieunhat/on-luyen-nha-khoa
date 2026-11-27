# Nguồn slide Da Liễu (sl/src/bN.txt) -> sl/out/decks.json
# Cú pháp:
#   @next Tên bài sau            (dòng đầu, tuỳ chọn)
#   @goal                         -> slide mục tiêu, các dòng "- " sau đó
#   # NHÃN MỤC | Tiêu đề slide    -> slide nội dung mới
#   - ý / "  - " ý con             @fig N  (hình bên phải)    ! tip|why|warn|key: chữ   | a | b | bảng
#   ?? Tiêu đề trắc nghiệm         -> slide trắc nghiệm; mỗi câu: ? nhãn | câu hỏi | A | B | C | D | đáp án (A-D) | giải thích
#   @recap                        -> slide tổng kết, các dòng "- "
import json, os, re, sys, glob, random, zlib
D = os.path.dirname(os.path.abspath(__file__))
FIGS = json.load(open(os.path.join(D, '..', 'figs2.json'), encoding='utf8'))
META = {m['b']: m for m in json.load(open(os.path.join(D, '..', 'meta.json'), encoding='utf8'))}

def parse(b, txt):
    S = [{'k': 'title', 'dl': 1, 'b': b, 't': META[b]['title']}]; cur = None; nxt = None; used = []
    for raw in txt.split('\n'):
        ln = raw.rstrip()
        if not ln.strip(): continue
        if ln.startswith('@next '): nxt = ln[6:].strip(); continue
        if ln == '@goal': cur = {'k': 'goal', 'b': b, 'items': []}; S.append(cur); continue
        if ln == '@recap': cur = {'k': 'recap', 'b': b, 'items': []}; S.append(cur); continue
        if ln.startswith('# '):
            sec, h = [x.strip() for x in ln[2:].split('|', 1)]
            cur = {'k': 'c', 'b': b, 'sec': sec, 'h': h}; S.append(cur); continue
        if ln.startswith('?? '):
            cur = {'k': 'quiz', 'b': b, 'title': ln[3:].strip(), 'q': []}; S.append(cur); continue
        if ln.startswith('? '):
            p = [x.strip() for x in ln[2:].split('|')]; assert len(p) == 8, (b, ln)
            o, a = p[2:6], 'ABCD'.index(p[6]); rnd = random.Random(zlib.crc32(p[1].encode()))
            idx = list(range(4)); rnd.shuffle(idx)
            if any(re.search(r'(Cả ba|Không thể nào|Không cần)', x) for x in o): idx = list(range(4))
            cur['q'].append({'lab': p[0], 'p': p[1], 'o': [o[j] for j in idx], 'a': idx.index(a), 'why': p[7]}); continue
        m = re.match(r'^(\s*)- (.+)$', ln)
        if m: cur.setdefault('items', []).append([m.group(2), len(m.group(1)) // 2]); continue
        m = re.match(r'^@fig (\d+)(?:: (.+))?$', ln)
        if m:
            n = int(m.group(1)); f = FIGS[n]; used.append(n)
            cap = m.group(2) or re.sub(r'^Hình\s*\d+\s*\.\s*\d+\.?\s*', '', f['cap']).strip()
            cur['fig'] = {'n': n, 'src': f'f{n:02d}.webp', 'cap': cap, 'w': f['size'][0], 'h': f['size'][1]}; continue
        m = re.match(r'^! (tip|why|warn|key)(?:\[(.+?)\])?: (.+)$', ln)
        if m: cur['note'] = {'kind': m.group(1), 'lab': m.group(2) or {'tip': 'Mẹo nhớ', 'why': 'Hiểu nhanh', 'warn': 'Lưu ý', 'key': 'Ghi nhớ'}[m.group(1)], 't': m.group(3)}; continue
        if ln.lstrip().startswith('|'):
            if 'rows' not in cur and 'items' not in cur: cur['tfirst'] = 1
            cur.setdefault('rows', []).append([c.strip() for c in ln.strip().strip('|').split('|')]); continue
        raise ValueError((b, ln))
    nq = sum(len(s['q']) for s in S if s['k'] == 'quiz')
    S.append({'k': 'end', 'b': b, 'next': nxt})
    S[0].update(n=len(S), nq=nq, mins=max(8, round(len(S) * 1.3)))
    for s in S:
        if s.get('rows'): assert len({len(r) for r in s['rows']}) == 1, (b, s['h'])
    return S, used

if __name__ == '__main__':
    decks, figs = {}, set()
    for f in sorted(glob.glob(os.path.join(D, 'src', 'b*.txt')), key=lambda x: int(re.findall(r'\d+', os.path.basename(x))[0])):
        b = int(re.findall(r'\d+', os.path.basename(f))[0])
        S, used = parse(b, open(f, encoding='utf8').read()); decks[f'dl-bai-{b}'] = S; figs |= set(used)
        print(b, len(S), 'slide', S[0]['nq'], 'câu', 'hình', used)
    json.dump(decks, open(os.path.join(D, 'out', 'decks.json'), 'w', encoding='utf8'), ensure_ascii=False)
    json.dump(sorted(figs), open(os.path.join(D, 'out', 'figs.json'), 'w'))
