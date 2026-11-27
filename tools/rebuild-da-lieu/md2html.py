# Bài lý thuyết Da Liễu: chuyển định dạng soạn nhanh (src/bN.md) -> HTML giống các môn khác
# python3 md2html.py  -> out/lessons.json
import base64, html, json, os, re
D = os.path.dirname(os.path.abspath(__file__))
FIGS = json.load(open(os.path.join(D, 'figs2.json'), encoding='utf8'))
LABEL = {'why': 'Hiểu nhanh:', 'tip': 'Mẹo nhớ:', 'key': 'Ghi nhớ:', 'warn': 'Lưu ý:', 'goal': 'Học xong bài này, bạn cần:'}


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)', r'<i>\1</i>', s)
    s = re.sub(r'\^(\S+?)\^', r'<sup>\1</sup>', s)
    s = re.sub(r'~(\S+?)~', r'<sub>\1</sub>', s)
    return s


def convert(b, src):
    out, toc, figs = [], [], []
    lines = src.split('\n'); i = 0; h3 = 0

    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip(): i += 1; continue
        m = re.match(r'^(#{1,3}) (.+)$', ln)
        if m:
            n = len(m.group(1)); t = m.group(2).strip()
            if n == 1:
                h3 += 1; hid = f'th-dl-bai-{b}-{h3}'; toc.append({'id': hid, 't': t})
                out.append(f'<h3 id="{hid}">{inline(t)}</h3>')
            else: out.append(f'<h{n + 2}>{inline(t)}</h{n + 2}>')
            i += 1; continue
        m = re.match(r'^> ?(why|tip|key|warn|goal)(?:\[(.+?)\])?: ?(.*)$', ln)
        if m:
            kind, lab, txt = m.group(1), m.group(2) or LABEL[m.group(1)], m.group(3)
            i += 1
            while i < len(lines) and lines[i].startswith('>> '): txt += '\n' + lines[i][3:]; i += 1
            paras = ''.join(f'<p>{(f"<strong>{inline(lab)}</strong> " if k == 0 else "") + inline(p)}</p>' for k, p in enumerate(txt.split('\n')))
            out.append(f'<div class="th-note {kind}">{paras}</div>'); continue
        m = re.match(r'^\[fig (\d+)(?:: (.+))?\]$', ln.strip())
        if m:
            f = FIGS[int(m.group(1))]; figs.append(int(m.group(1)))
            cap = m.group(2) or re.sub(r'^Hình\s*\d+\s*\.\s*\d+\.?\s*', '', f['cap']).strip()
            data = base64.b64encode(open(os.path.join(D, f['img']), 'rb').read()).decode()
            w, h = f['size']
            out.append(f'<figure class="th-fig"><img src="data:image/webp;base64,{data}" width="{w}" height="{h}" alt="{html.escape(cap)}" loading="lazy" decoding="async">'
                       f'<figcaption><b>Hình {len(figs)}.</b> {inline(cap)}</figcaption></figure>')
            i += 1; continue
        if ln.lstrip().startswith('|'):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]); i += 1
            nc = len(rows[0]); assert all(len(r) == nc for r in rows), (b, rows)
            head = ''.join(f'<th>{inline(c)}</th>' for c in rows[0])
            body = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in rows[1:])
            out.append(f'<div class="tbl"><table class="c{min(nc, 3)}"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'); continue
        if re.match(r'^\s*- ', ln):
            block = []
            while i < len(lines) and re.match(r'^\s*- ', lines[i]):
                ind = len(lines[i]) - len(lines[i].lstrip()); block.append((ind, lines[i].strip()[2:])); i += 1
            out.append(list_html(block)); continue
        out.append(f'<p>{inline(ln.strip())}</p>'); i += 1
    return ''.join(out), toc, figs


def list_html(block):
    # danh sách lồng nhau theo thụt lề 2 dấu cách
    html_parts = []; depth = -1
    for ind, txt in block:
        lvl = ind // 2
        if lvl > depth:
            for _ in range(lvl - depth): html_parts.append('<ul><li>')
        elif lvl == depth: html_parts.append('</li><li>')
        else:
            for _ in range(depth - lvl): html_parts.append('</li></ul>')
            html_parts.append('</li><li>')
        depth = lvl; html_parts.append(inline(txt))
    for _ in range(depth + 1): html_parts.append('</li></ul>')
    return ''.join(html_parts)


META = json.load(open(os.path.join(D, 'meta.json'), encoding='utf8'))
if __name__ == '__main__':
    L = {}
    for m in META:
        b = m['b']; p = os.path.join(D, 'src', f'b{b}.md')
        if not os.path.exists(p): continue
        h, toc, figs = convert(b, open(p, encoding='utf8').read())
        words = len(re.sub('<[^>]+>', ' ', re.sub(r'data:image[^"]+', '', h)).split())
        note = f'{len(figs)} hình minh hoạ' if figs else f'giáo trình {m["p1"]}–{m["p2"]}'
        L[f'dl-bai-{b}'] = {'pages': f'{m["p1"]}–{m["p2"]}', 'note': note,
                            'srcline': f'Biên soạn lại từ giáo trình lý thuyết Da liễu (bài {b}, trang {m["p1"]}–{m["p2"]})' + (f' · {len(figs)} hình minh hoạ' if figs else ''),
                            'pdf': f'pdf/{m["file"]}', 'file': m['file'], 'mins': max(5, round(words / 180)), 'toc': toc, 'html': h}
        print(b, words, 'chữ', len(toc), 'mục', len(figs), 'hình')
    os.makedirs(os.path.join(D, 'out'), exist_ok=True)
    json.dump(L, open(os.path.join(D, 'out', 'lessons.json'), 'w', encoding='utf8'), ensure_ascii=False)
