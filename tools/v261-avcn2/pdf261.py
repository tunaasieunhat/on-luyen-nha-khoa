# Bản in PDF cho AVCN2 (2.6.1): 17 bài + bảng từ tóm tắt (1 trang/Unit) + giáo trình trọn bộ
# python3 -I pdf261.py html   -> out/print/*.html + out/print/jobs.json
# node print261.js            -> out/pdf/*.pdf
# python3 -I pdf261.py book   -> out/pdf/GiaoTrinh-Anh-van-chuyen-nganh-2.pdf + out/books.json
import os, re, sys, json, html, base64, importlib.util
D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, 'out'); PR = os.path.join(OUT, 'print'); PDF = os.path.join(OUT, 'pdf')
os.makedirs(PR, exist_ok=True); os.makedirs(PDF, exist_ok=True)
L = json.load(open(os.path.join(OUT, 'lessons.json'), encoding='utf8'))
T = json.load(open(os.path.join(D, 'theory-data.json'), encoding='utf8'))
E = lambda s: html.escape(str(s), quote=False)
TITLE = {'avcn2-u0': ('U0', 'Bắt đầu từ đây – Cách học cho người mất gốc'), 'avcn2-ugoc': ('Gốc từ', 'Gốc từ – Đoán nghĩa từ lạ')}
spec = importlib.util.spec_from_file_location('b', os.path.join(D, 'parse.py')); PZ = importlib.util.module_from_spec(spec); spec.loader.exec_module(PZ)
UNITS, W = PZ.load()
UT = {1: 'The dentist – Nha sĩ và nghề nha', 2: 'Dental specialties – Các chuyên khoa', 3: 'The dental office – Khu vực phòng khám',
      4: 'Dental staff – Nhân sự phòng khám', 5: 'Dental instruments – Dụng cụ nha khoa', 6: 'The mouth – Khoang miệng',
      7: 'Tooth anatomy – Cấu tạo răng', 8: 'Types of teeth – Các loại răng', 9: 'Infection control – Kiểm soát lây nhiễm',
      10: 'Dental technology – Công nghệ nha khoa', 11: 'Appointments – Lịch hẹn', 12: 'Payment and insurance – Thanh toán, bảo hiểm',
      13: 'Patient communication – Giao tiếp bệnh nhân', 14: 'Oral hygiene – Vệ sinh răng miệng', 15: 'Teeth cleaning – Làm sạch răng'}
for u, t in UT.items(): TITLE[f'avcn2-u{u}'] = (f'U{u}', t)

CSS = '''
@page{size:A4;margin:14mm 14mm 16mm}
*{box-sizing:border-box}
body{margin:0;font-family:Inter,"DejaVu Sans",sans-serif;font-size:10.2pt;line-height:1.5;color:#12332E;-webkit-print-color-adjust:exact;print-color-adjust:exact}
[lang="en"],.ipa{font-family:Inter,"DejaVu Sans",sans-serif}
.ipa,.vw-ipa{font-family:"DejaVu Sans",sans-serif}
.hd{border:2px solid #0B544C;border-radius:12px;padding:12px 16px;background:#EEF7F3;margin-bottom:12px}
.eb{font-size:8pt;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#4F6D69}
h1{margin:4px 0 2px;font-size:19pt;line-height:1.15;color:#0B544C}
h1 .no{display:inline-block;background:#127B70;color:#fff;border-radius:7px;padding:1px 8px;font-size:12pt;vertical-align:4px;margin-right:6px}
.meta{font-size:8.5pt;color:#4F6D69;margin:2px 0 6px}
.toc{columns:2;font-size:8.6pt;margin:0;padding-left:16px}
h3{font-size:13pt;color:#0B544C;margin:14px 0 6px;padding-top:6px;border-top:1.5px dashed #CFE3DC}
h4{font-size:11pt;margin:10px 0 3px;break-after:avoid}
p{margin:4px 0}
ul,ol{margin:3px 0 6px;padding-left:18px}
strong{color:#0B544C}
.th-note{border-left:4px solid #127B70;background:#DCEEE7;border-radius:8px;padding:6px 10px;margin:7px 0;break-inside:avoid}
.th-note.goal{border-left-color:#4F6D69;background:#EEF7F3}.th-note.tip{border-left-color:#FFD66B;background:#FFF4D1}
.th-note.warn{border-left-color:#CF4C64;background:#FCE4E8}.th-note.why{border-left-color:#127B70;background:#F3FAF7}
.th-note p{margin:2px 0}
table{border-collapse:collapse;width:100%;font-size:9pt;margin:5px 0}
th,td{border:1px solid #CFE3DC;padding:4px 6px;text-align:left;vertical-align:top}
th{background:#D7F1EB;color:#0B544C}
tr{break-inside:avoid}
.vw{border:1.5px solid #CFE3DC;border-radius:10px;padding:7px 10px;margin:7px 0;background:#FFFDF8}
.vw-def,.vw-h,.vw-m{break-inside:avoid}
.vw-h{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.vw-hw{display:flex;flex-wrap:wrap;align-items:baseline;gap:2px 8px}
.vw-t{font-size:13.5pt;font-weight:800;color:#0B544C}
.vw-ipa{font-size:9pt;color:#4F6D69}
.vw-s{font-size:8.6pt;color:#4F6D69}.vw-s b{color:#9E3349}
.vw-m{font-weight:700;font-size:11pt;margin:3px 0}
.vw-pos{font-size:7.5pt;font-weight:700;text-transform:uppercase;background:#EEF7F3;color:#4F6D69;border-radius:5px;padding:1px 6px;margin-left:8px}
.vw-hook,.vw-ex{font-size:9.3pt}
.vw-exv{color:#4F6D69}
.vw-def{background:#EEF7F3;border-radius:8px;padding:5px 7px;margin:4px 0}
.vw-dl{font-size:8pt;color:#4F6D69;margin-bottom:3px}
.vw-ck{display:flex;flex-wrap:wrap;gap:4px}
.ck{display:inline-flex;flex-direction:column;border:1px solid #CFE3DC;border-radius:6px;background:#fff;padding:2px 6px}
.ck i{font-style:normal;font-weight:600;font-size:8.8pt}.ck small{font-size:7.8pt;color:#0B544C}
.ck.more{border-style:dashed}
.vw-kw{font-size:8.8pt;background:#FFF4D1;color:#7A5600;border-radius:6px;padding:3px 7px;margin:3px 0 0}
.vw-kw b{color:#7A5600}.vw-kw b.vw-ans{color:#9E3349}
.vw-say,.vt-go,.vt-prog,button{display:none!important}
.end{margin-top:14px;font-size:8.3pt;color:#4F6D69;border-top:1px solid #CFE3DC;padding-top:6px}
'''


def page(title_no, title, meta, toc, body, eyebrow='Lý thuyết · Anh văn chuyên ngành 2'):
    tl = ''.join(f'<li>{E(x["t"])}</li>' for x in toc)
    return (f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>{E(title)}</title><style>{CSS}</style></head><body>'
            f'<div class="hd"><div class="eb">{E(eyebrow)}</div><h1><span class="no">{E(title_no)}</span>{E(title)}</h1><p class="meta">{E(meta)}</p>'
            + (f'<ol class="toc">{tl}</ol>' if toc else '') + f'</div>{body}'
            '<p class="end">Định nghĩa tiếng Anh giữ nguyên theo Glossary.pdf để làm trắc nghiệm. Phần đọc gần giống, nghĩa ngắn, mẹo nhớ, ví dụ và dịch từng cụm là giải thích bổ sung để dễ học. Trong app có nút loa để nghe đọc và phần Luyện từ 5 bậc. · Ôn Luyện Nha Khoa</p>'
            '</body></html>')


def bangtu():
    css = CSS + '''@page{size:A4;margin:10mm 11mm 12mm}
.sheet{break-after:page}.sheet:last-child{break-after:auto}
.sh-h{display:flex;align-items:baseline;gap:10px;border-bottom:2px solid #0B544C;padding-bottom:4px;margin-bottom:5px}
.sh-h b{font-size:15pt;color:#0B544C}.sh-h span{font-size:9pt;color:#4F6D69}
.sheet table{font-size:8.6pt;margin:0}.sheet td,.sheet th{padding:3px 5px}
.sheet td.t{font-weight:800;color:#0B544C;font-size:9.6pt;white-space:nowrap}
.sheet td.s{color:#9E3349;white-space:nowrap}.sheet td.k{color:#7A5600;font-size:8pt}
.foot{font-size:7.6pt;color:#4F6D69;margin-top:4px}
'''
    out = []
    for u in range(1, 16):
        rows = ''.join(f'<tr><td class="t">{E(W[t]["t"])}</td><td class="ipa">{E(W[t]["ipa"])}</td><td class="s">{E(W[t]["say"])}</td><td>{E(W[t]["m"])}</td><td class="k">{E(W[t]["kw"])}</td></tr>'
                       for t in UNITS[u]['order'])
        out.append(f'<section class="sheet"><div class="sh-h"><b>Unit {u}</b><span>{E(UT[u])} · {len(UNITS[u]["order"])} từ</span></div>'
                   f'<table><thead><tr><th>Từ</th><th>Phiên âm</th><th>Đọc gần giống</th><th>Nghĩa</th><th>Thấy trong đề (keyword)</th></tr></thead><tbody>{rows}</tbody></table>'
                   '<p class="foot">Chữ IN HOA là âm đọc mạnh. Che cột Nghĩa để tự kiểm tra. · Anh văn chuyên ngành 2 · Ôn Luyện Nha Khoa</p></section>')
    return f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Bảng từ AVCN2</title><style>{css}</style></head><body>{"".join(out)}</body></html>'


if sys.argv[1] == 'html':
    jobs = []
    for k in L['order']:
        l = L['lessons'][k]; no, title = TITLE[k]
        hp = os.path.join(PR, k + '.html')
        open(hp, 'w', encoding='utf8').write(page(no, title, f'{l["srcline"]} · khoảng {l["mins"]} phút đọc · Ôn Luyện Nha Khoa', l['toc'], l['html']))
        jobs.append({'html': hp, 'pdf': os.path.join(PDF, l['file']), 'footer': f'Anh văn chuyên ngành 2 · {no}: {title}'})
    hp = os.path.join(PR, 'bangtu.html'); open(hp, 'w', encoding='utf8').write(bangtu())
    jobs.append({'html': hp, 'pdf': os.path.join(PDF, 'AVCN2-Bang-tu-tom-tat.pdf'), 'footer': 'Anh văn chuyên ngành 2 · Bảng từ tóm tắt 15 Unit'})
    json.dump(jobs, open(os.path.join(PR, 'jobs.json'), 'w', encoding='utf8'), ensure_ascii=False)
    print(len(jobs), 'trang in')
else:
    from pypdf import PdfReader, PdfWriter
    gt = T['books']['avcn2-gt']
    cover = base64.b64decode(gt['cover'].split(',', 1)[1])
    open(os.path.join(PR, 'cover.webp'), 'wb').write(cover)
    order = L['order']
    npg = {k: len(PdfReader(os.path.join(PDF, L['lessons'][k]['file'])).pages) for k in order}
    start = 3; pages = {}
    for k in order: pages[k] = start; start += npg[k]
    rows = ''.join(f'<tr><td><b>{E(TITLE[k][0])}</b></td><td>{E(TITLE[k][1])}</td><td style="text-align:right">{pages[k]}</td></tr>' for k in order)
    cov = (f'<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:A4;margin:0}}body{{margin:0}}img{{width:210mm;height:297mm;object-fit:cover;display:block}}</style></head>'
           f'<body><img src="cover.webp"></body></html>')
    toc = (f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="hd"><div class="eb">Giáo trình trọn bộ</div>'
           f'<h1>Anh văn chuyên ngành 2</h1><p class="meta">Bản 2.6.1 · biên soạn lại cho người mất gốc · 177 từ vựng, 15 Unit, kèm bài Bắt đầu từ đây và Gốc từ</p></div>'
           f'<h3>Mục lục</h3><table><thead><tr><th>Bài</th><th>Tên bài</th><th style="text-align:right">Trang</th></tr></thead><tbody>{rows}</tbody></table>'
           '<div class="th-note tip"><p><strong>Cách dùng:</strong> đọc U0 trước, sau đó học mỗi ngày một Unit theo lộ trình 15 ngày. Bảng từ tóm tắt 1 trang mỗi Unit có trong file riêng AVCN2-Bang-tu-tom-tat.pdf.</p></div></body></html>')
    open(os.path.join(PR, 'cover.html'), 'w', encoding='utf8').write(cov); open(os.path.join(PR, 'toc.html'), 'w', encoding='utf8').write(toc)
    json.dump([{'html': os.path.join(PR, 'cover.html'), 'pdf': os.path.join(PR, 'cover.pdf'), 'footer': ''},
               {'html': os.path.join(PR, 'toc.html'), 'pdf': os.path.join(PR, 'toc.pdf'), 'footer': 'Anh văn chuyên ngành 2 · Mục lục'}],
              open(os.path.join(PR, 'jobs2.json'), 'w'), ensure_ascii=False)
    if sys.argv[1] == 'book':
        os.system(f'cd {D} && node print261.js {os.path.join(PR, "jobs2.json")}')
        wr = PdfWriter()
        for f in [os.path.join(PR, 'cover.pdf'), os.path.join(PR, 'toc.pdf')] + [os.path.join(PDF, L['lessons'][k]['file']) for k in order]:
            for pg in PdfReader(f).pages: wr.add_page(pg)
        try: wr.compress_identical_objects(remove_identicals=True, remove_orphans=True)
        except Exception as e: print('compress', e)
        bp = os.path.join(PDF, gt['file']); wr.write(bp)
        n = len(PdfReader(bp).pages); assert n == start - 1, (n, start)
        bt = os.path.join(PDF, 'AVCN2-Bang-tu-tom-tat.pdf')
        json.dump({'avcn2-gt': {'pages': n, 'size': os.path.getsize(bp), 'lessons': [{'id': k, 'page': pages[k]} for k in order]},
                   'avcn2-bangtu': {'name': 'Bảng từ AVCN2', 'file': 'AVCN2-Bang-tu-tom-tat.pdf', 'pdf': 'pdf/AVCN2-Bang-tu-tom-tat.pdf', 'size': os.path.getsize(bt)}},
                  open(os.path.join(OUT, 'books.json'), 'w', encoding='utf8'), ensure_ascii=False)
        print('book', n, 'trang', os.path.getsize(bp), 'bytes')
