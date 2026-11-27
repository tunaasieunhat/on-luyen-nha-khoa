# Bản dựng lại: thêm môn Da Liễu (giáo trình + slide), bỏ Sơ đồ tư duy và Video bài giảng ở mọi môn.
# python3 -I patchdl.py <file.html>   (chạy lại nhiều lần vẫn ra cùng kết quả)
import sys, re, json, base64, os
F = sys.argv[1]; DL = '/home/claude/dl'
s = open(F, encoding='utf8').read(); n0 = len(s)
def once(old, new, cnt=1):
    global s
    if new in s: return
    assert s.count(old) == cnt, (old[:80], s.count(old)); s = s.replace(old, new)
def jscript(id_):
    m = re.search(r'(<script type="application/json" id="%s">)(.*?)(</script>)' % id_, s, re.S); assert m, id_; return m
def jset(id_, txt):
    global s
    m = jscript(id_); s = s[:m.start(2)] + txt + s[m.end(2):]
jdump = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
M = json.load(open(DL + '/meta.json', encoding='utf8'))
# 1. Bỏ sơ đồ tư duy: xoá dữ liệu (tab, nút tự ẩn khi không có dữ liệu)
jset('mindmap-data', '{}')
# 2. Bỏ video bài giảng: xoá dữ liệu VIDEOS
s = re.sub(r'var VIDEOS = \{.*?\};\n', 'var VIDEOS = {};\n', s, count=1, flags=re.S)
assert 'var VIDEOS = {};' in s
once('Đọc bài, xem sơ đồ, tải PDF.', 'Đọc bài, xem slide, tải PDF.')
once('Chọn môn, chọn bài để đọc hoặc xem sơ đồ.', 'Chọn môn, chọn bài để đọc hoặc xem slide.')
once('Ôn lý thuyết và sơ đồ tư duy rồi thi lại nhé.', 'Ôn lý thuyết và slide rồi thi lại nhé.')
# 3. Môn Da Liễu trong danh sách môn
m = jscript('fixed-data'); fd = json.loads(m.group(2))
fd['subjects'] = [x for x in fd['subjects'] if x['name'] != 'Da Liễu'] + [{'name': 'Da Liễu', 'lessons': [
    {'id': f'dl-bai-{x["b"]}', 'name': f'Bài {x["b"]}', 'title': x['title'], 'file': 'Giao_trinh_ly_thuyet_da_lieu.pdf'} for x in M]}]
jset('fixed-data', jdump(fd))
# 4. Bài lý thuyết + giáo trình trọn bộ
m = jscript('theory-data'); td = json.loads(m.group(2))
L = json.load(open(DL + '/out/lessons.json', encoding='utf8')); B = json.load(open(DL + '/out/book.json'))
for k in [k for k in td['lessons'] if k.startswith('dl-bai-')]: del td['lessons'][k]
FIGMAP = {base64.b64encode(open(f'{DL}/fig/{fn}', 'rb').read()).decode(): fn for fn in os.listdir(DL + '/fig') if fn.endswith('.webp')}
def unembed(h):
    return re.sub(r'src="data:image/webp;base64,([A-Za-z0-9+/=]+)"', lambda mm: f'src="slides/da-lieu/fig/{FIGMAP[mm.group(1)]}"', h)
for k, v in L.items(): td['lessons'][k] = {**v, 'mins': int(v['mins']), 'html': unembed(v['html'])}
cover = 'data:image/webp;base64,' + base64.b64encode(open(DL + '/print/cover.webp', 'rb').read()).decode()
td['books']['dl-gt'] = {'name': 'Da Liễu', 'prefix': 'dl-bai-', 'unit': 'bài', 'file': 'GiaoTrinh-Da-lieu.pdf', 'pdf': 'pdf/GiaoTrinh-Da-lieu.pdf',
    'pages': B['pages'], 'lessons': B['lessons'], 'nfig': 77, 'size': B['size'], 'cover': cover, 'cw': 600, 'ch': 850}
jset('theory-data', jdump(td))
# 5. Slide Da Liễu: CSS + JS
css = open(DL + '/sl/dls.css', encoding='utf8').read().strip()
s = re.sub(r'/\* @@DLS-CSS.*?@@DLS-CSS-END \*/\n?', '', s, flags=re.S)
s = s.replace('/* @@AVS-CSS-END */', '/* @@AVS-CSS-END */\n' + css, 1)
decks = json.load(open(DL + '/sl/out/decks.json', encoding='utf8'))
meta = {f'dl-bai-{x["b"]}': {'pptx': x['file'].replace('DL-Bai-', 'DL-Slide-Bai-').replace('.pdf', '.pptx'), 'print': x['file'].replace('DL-Bai-', 'DL-Slide-Bai-').replace('.pdf', '-BanIn.pdf')} for x in M}
js = open(DL + '/sl/dls.js', encoding='utf8').read().strip().replace('__DLS_DATA__', jdump(decks))
js = js.replace('/* @@DLS-JS-END */', '''var DLS_META = %s;
(function () {
  if (typeof SLIDES !== 'object' || !SLIDES || typeof AVS_DECKS !== 'object') return;
  const avs0 = avsSlide, th0 = avsThumb;
  dlsAvs = avs0;
  avsSlide = function (S, i, p) { return S && S[0] && S[0].dl ? dlsSlide(S, i, p) : avs0(S, i, p); };
  avsThumb = function (x, i) { return x && x.b && AVS_DECKS['dl-bai-' + x.b] && AVS_DECKS['dl-bai-' + x.b][0].dl ? dlsThumb(x) : th0(x, i); };
  for (const k in DLS_DECKS) { AVS_DECKS[k] = DLS_DECKS[k]; SLIDES[k] = { n: DLS_DECKS[k].length, deck: true, dl: true, base: 'slides/da-lieu', pptx: DLS_META[k].pptx, print: DLS_META[k].print }; }
  window.__dls = { decks: DLS_DECKS };
  document.addEventListener('click', e => { const im = e.target.closest && e.target.closest('.avs .dl-f img'); if (im && typeof figOpen === 'function') figOpen(im); });
})();
/* @@DLS-JS-END */''' % jdump(meta))
s = re.sub(r'/\* @@DLS-JS:.*?@@DLS-JS-END \*/\n?', '', s, flags=re.S)
assert s.count('/* @@AVS-JS-END */') == 1; s = s.replace('/* @@AVS-JS-END */', '/* @@AVS-JS-END */\n' + js, 1)
once("if (s) $('#sl-tip').textContent = s.deck ?", "if (s) $('#sl-tip').textContent = s.dl ? 'Ở slide Kiểm tra nhanh, chạm vào đáp án để biết đúng sai và xem giải thích. Chạm vào hình để xem lớn. Vuốt ngang hoặc dùng phím ← → để chuyển slide. Bản PowerPoint và bản in có thêm slide đáp án.' : s.deck ?")
once("'Tuyệt vời!' : 'Xem lại các từ chưa đúng rồi làm lại nhé.'", "'Tuyệt vời!' : S[0] && S[0].dl ? 'Đọc lại phần giải thích rồi làm lại nhé.' : 'Xem lại các từ chưa đúng rồi làm lại nhé.'")
open(F, 'w', encoding='utf8').write(s); print(os.path.basename(F), n0, '->', len(s))
