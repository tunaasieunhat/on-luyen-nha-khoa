# Bản in PDF Da Liễu: 11 bài + giáo trình trọn bộ (bìa + mục lục + 11 bài)
# python3 pdfdl.py html ; node print.js print/jobs.json ; python3 pdfdl.py book
import os, sys, json, html, subprocess
D = os.path.dirname(os.path.abspath(__file__)); PR = D + '/print'; PDF = D + '/pdf'
L = json.load(open(D + '/out/lessons.json', encoding='utf8'))
M = json.load(open(D + '/meta.json', encoding='utf8'))
E = lambda s: html.escape(str(s), quote=False)
F = 'Carlito,"DejaVu Sans",sans-serif'
CSS = '''@page{size:A4;margin:14mm 15mm 16mm}*{box-sizing:border-box}
body{margin:0;font-family:%s;font-size:11pt;line-height:1.45;color:#2B1F24;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.hd{border:2px solid #8A3B4E;border-radius:12px;padding:12px 16px;background:#FBF0F2;margin-bottom:12px}
.eb{font-size:8.5pt;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#7A5C64}
h1{margin:4px 0 2px;font-size:20pt;line-height:1.15;color:#7A2E41}
h1 .no{display:inline-block;background:#A8455D;color:#fff;border-radius:7px;padding:1px 8px;font-size:13pt;vertical-align:3px;margin-right:6px}
.meta{font-size:9pt;color:#7A5C64;margin:2px 0 6px}.toc{columns:2;font-size:9.2pt;margin:0;padding-left:18px}
h3{font-size:13.5pt;color:#7A2E41;margin:14px 0 6px;padding-top:6px;border-top:1.5px dashed #EBCBD2;break-after:avoid}
h4{font-size:11.5pt;margin:10px 0 3px;color:#5E2232;break-after:avoid}h5{font-size:11pt;margin:8px 0 2px;break-after:avoid}
p{margin:4px 0}ul,ol{margin:3px 0 6px;padding-left:18px}strong{color:#6E2639}
.th-note{border-left:4px solid #A8455D;background:#F7E3E8;border-radius:8px;padding:6px 10px;margin:7px 0;break-inside:avoid}
.th-note.goal{border-left-color:#7A5C64;background:#FBF0F2}.th-note.tip{border-left-color:#E0B23C;background:#FFF4D1}
.th-note.warn{border-left-color:#CF4C64;background:#FCE4E8}.th-note.why{border-left-color:#3F8C83;background:#EAF5F2}
.th-note.key{border-left-color:#A8455D;background:#F7E3E8}.th-note p{margin:2px 0}
table{border-collapse:collapse;width:100%%;font-size:9.6pt;margin:5px 0}th,td{border:1px solid #EBCBD2;padding:4px 6px;text-align:left;vertical-align:top}
th{background:#F3D9DF;color:#6E2639}tr{break-inside:avoid}
figure{margin:8px auto;text-align:center;break-inside:avoid}figure img{max-width:100%%;max-height:95mm;width:auto;height:auto;border-radius:6px}
figcaption{font-size:9pt;color:#7A5C64;margin-top:3px}
.end{margin-top:14px;font-size:8.5pt;color:#7A5C64;border-top:1px solid #EBCBD2;padding-top:6px}''' % F
FOOT = '<div style="font-family:Carlito,sans-serif;font-size:8px;color:#7A5C64;width:100%%;padding:0 15mm;display:flex;justify-content:space-between"><span>%s</span><span>Trang <span class="pageNumber"></span>/<span class="totalPages"></span></span></div>'

def page(no, title, meta, toc, body, eb):
    tl = ''.join(f'<li>{E(x["t"])}</li>' for x in toc)
    return (f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>{E(title)}</title><style>{CSS}</style></head><body>'
            f'<div class="hd"><div class="eb">{E(eb)}</div><h1>' + (f'<span class="no">{E(no)}</span>' if no else '') + f'{E(title)}</h1><p class="meta">{E(meta)}</p>'
            + (f'<ol class="toc">{tl}</ol>' if toc else '') + f'</div>{body}</body></html>')

if sys.argv[1] == 'html':
    jobs = []
    for m in M:
        k = f'dl-bai-{m["b"]}'; l = L[k]
        meta = f'Biên soạn lại từ giáo trình Da Liễu (trang {m["p1"]}–{m["p2"]}) · {l["note"]} · khoảng {l["mins"]} phút đọc'
        h = page(f'Bài {m["b"]}', m['title'], meta, l['toc'], l['html'] + '<p class="end">Nội dung biên soạn lại, có bổ sung mẹo nhớ và phần liên hệ răng hàm mặt. Hình ảnh trích từ giáo trình gốc. · Ôn Luyện Nha Khoa</p>', 'Lý thuyết · Da Liễu')
        p = f'{PR}/{k}.html'; open(p, 'w', encoding='utf8').write(h)
        jobs.append({'html': p, 'pdf': f'{PDF}/{m["file"]}', 'footer': FOOT % E(f'Da Liễu · Bài {m["b"]}. {m["title"]}')})
    json.dump(jobs, open(PR + '/jobs.json', 'w'), ensure_ascii=False); print(len(jobs))
else:
    from pypdf import PdfReader, PdfWriter
    npg = {m['b']: len(PdfReader(f'{PDF}/{m["file"]}').pages) for m in M}
    start = 3; pages = {}
    for m in M: pages[m['b']] = start; start += npg[m['b']]
    rows = ''.join(f'<tr><td><b>Bài {m["b"]}</b></td><td>{E(m["title"])}</td><td style="text-align:right">{pages[m["b"]]}</td></tr>' for m in M)
    open(PR + '/cover.html', 'w').write('<!doctype html><html><head><meta charset="utf-8"><style>@page{size:A4;margin:0}body{margin:0}img{width:210mm;height:297mm;object-fit:cover;display:block}</style></head><body><img src="cover.jpg"></body></html>')
    toc = (f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="hd"><div class="eb">Giáo trình trọn bộ</div>'
           f'<h1>Da Liễu</h1><p class="meta">Biên soạn lại từ giáo trình lý thuyết Da Liễu · 11 bài · 77 hình minh hoạ</p></div>'
           f'<h3>Mục lục</h3><table><thead><tr><th>Bài</th><th>Tên bài</th><th style="text-align:right">Trang</th></tr></thead><tbody>{rows}</tbody></table>'
           '<div class="th-note tip"><p><strong>Cách dùng:</strong> mỗi bài mở đầu bằng mục tiêu, kết thúc bằng khung Ghi nhớ cả bài. Khung vàng là mẹo nhớ, khung xanh là giải thích nhanh, có thêm phần liên hệ răng hàm mặt.</p></div></body></html>')
    open(PR + '/toc.html', 'w', encoding='utf8').write(toc)
    json.dump([{'html': PR + '/cover.html', 'pdf': PR + '/cover.pdf', 'footer': ''}, {'html': PR + '/toc.html', 'pdf': PR + '/toc.pdf', 'footer': FOOT % 'Da Liễu · Mục lục'}], open(PR + '/jobs2.json', 'w'), ensure_ascii=False)
    subprocess.run(['node', D + '/print.js', PR + '/jobs2.json'], check=True, cwd='/home/claude/work261')
    wr = PdfWriter()
    for f in [PR + '/cover.pdf', PR + '/toc.pdf'] + [f'{PDF}/{m["file"]}' for m in M]:
        for pg in PdfReader(f).pages: wr.add_page(pg)
    try: wr.compress_identical_objects(remove_identicals=True, remove_orphans=True)
    except Exception as e: print('compress', e)
    bp = PDF + '/GiaoTrinh-Da-lieu.pdf'; wr.write(bp)
    n = len(PdfReader(bp).pages); assert n == start - 1
    json.dump({'pages': n, 'size': os.path.getsize(bp), 'lessons': [{'id': f'dl-bai-{m["b"]}', 'page': pages[m['b']]} for m in M]}, open(D + '/out/book.json', 'w'))
    print('book', n, os.path.getsize(bp))
