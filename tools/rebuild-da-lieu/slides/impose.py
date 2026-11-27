# Ghép 4 slide/trang A4 ngang: python3 impose.py <slides.pdf> <ra.pdf> "<tiêu đề>"
import sys, subprocess, json, os, tempfile
from pypdf import PdfReader, PdfWriter, Transformation
SRC, OUT, TITLE = sys.argv[1], sys.argv[2], sys.argv[3]
mm = 72 / 25.4
PW, PH = 297, 210; L, GAPX, TOP, GAPY = 11, 8, 21, 11
CW = (PW - 2 * L - GAPX) / 2; CH = CW * 9 / 16
cells = [(L, TOP), (L + CW + GAPX, TOP), (L, TOP + CH + GAPY), (L + CW + GAPX, TOP + CH + GAPY)]
r = PdfReader(SRC); n = len(r.pages); pages = (n + 3) // 4
# nền: tiêu đề, khung, nhãn (vẽ bằng Chromium)
esc = lambda s: s.replace('&', '&amp;').replace('<', '&lt;')
html = '<meta charset="utf-8"><style>@page{size:297mm 210mm;margin:0}body{margin:0;font-family:Carlito,sans-serif;color:#2B1F24}.pg{position:relative;width:297mm;height:210mm;break-after:page}' \
       '.hd{position:absolute;left:11mm;right:11mm;top:8mm;display:flex;justify-content:space-between;font-size:10.5pt;border-bottom:.35mm solid #EBCBD2;padding-bottom:2mm}.hd b{color:#7A2E41}' \
       f'.c{{position:absolute;width:{CW}mm;height:{CH}mm;border:.3mm solid #D9A9B5;border-radius:1.5mm;box-sizing:border-box}}.lb{{position:absolute;font-size:8.5pt;color:#7A5C64}}</style>'
for k in range(pages):
    html += f'<div class="pg"><div class="hd"><b>{esc(TITLE)}</b><span>Ôn Luyện Nha Khoa · trang {k + 1}/{pages}</span></div>'
    for j in range(4):
        i = k * 4 + j
        if i >= n: break
        x, y = cells[j]
        html += f'<div class="c" style="left:{x}mm;top:{y}mm"></div><div class="lb" style="left:{x}mm;top:{y + CH + 1.2}mm">Slide {i + 1}</div>'
    html += '</div>'
tmp = tempfile.mkdtemp(); hp = os.path.join(tmp, 'bg.html'); bp = os.path.join(tmp, 'bg.pdf')
open(hp, 'w', encoding='utf8').write(html)
subprocess.run(['node', '-e', f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{hp}');await p.pdf({{path:'{bp}',preferCSSPageSize:true,printBackground:true}});await b.close()}})()"], check=True, cwd='/home/claude/work261')
bg = PdfReader(bp); w = PdfWriter()
for k in range(pages):
    page = w.add_page(bg.pages[k])
    for j in range(4):
        i = k * 4 + j
        if i >= n: break
        sp = r.pages[i]; sw = float(sp.mediabox.width); s = CW * mm / sw
        x, y = cells[j]
        page.merge_transformed_page(sp, Transformation().scale(s, s).translate(x * mm, (PH - y - CH) * mm))
w.compress_identical_objects(remove_identicals=True, remove_orphans=True)
w.write(OUT); print(os.path.basename(OUT), pages, 'trang', os.path.getsize(OUT) // 1024, 'KB')
# nén lại (pypdf ghi luồng nội dung chưa nén)
subprocess.run(['qpdf', '--compress-streams=y', '--recompress-flate', '--compression-level=9', '--object-streams=generate', '--replace-input', OUT], check=True)
print('nén:', os.path.getsize(OUT) // 1024, 'KB')
