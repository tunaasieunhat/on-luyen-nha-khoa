import os, re, sys
sys.path.insert(0, '/home/claude/work261')
D = os.path.dirname(os.path.abspath(__file__))
def load_ex():
    E = {}; cur = None
    for f in ('ex1.txt', 'ex2.txt', 'ex3.txt'):
        for ln in open(os.path.join(D, f), encoding='utf8'):
            ln = ln.strip()
            if not ln or ln.startswith('#'): continue
            if ln.startswith('@'): cur = ln[1:].strip(); assert cur not in E, cur; E[cur] = []; continue
            assert ln.startswith('= '), ln
            en, _, vi = ln[2:].partition(' => '); assert vi, ln
            E[cur].append([en.strip(), vi.strip()])
    return E
def has(term, s): return re.search(r'(?<![A-Za-z])' + re.escape(term) + r'(?![A-Za-z])', s, re.I)
if __name__ == '__main__':
    import parse
    U, W = parse.load(); E = load_ex()
    print(len(E), 'từ có ví dụ thêm /', len(W))
    for t in W:
        if t not in E: print('THIẾU', t); continue
        if len(E[t]) != 2: print('KHÔNG ĐỦ 2', t)
        for en, vi in E[t]:
            if not has(t, en): print('KHÔNG CHỨA TỪ', t, '|', en)
    for t in E:
        if t not in W: print('THỪA', t)
