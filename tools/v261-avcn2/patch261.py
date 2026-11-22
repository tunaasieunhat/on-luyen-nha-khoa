# Version 2.6.1: vá bản app đã dựng (chạy lại được nhiều lần)
# python3 -I patch261.py <file.html> [android]
import os, re, sys, json
D = os.path.dirname(os.path.abspath(__file__))
P, ANDROID = sys.argv[1], len(sys.argv) > 2 and sys.argv[2] == 'android'
h = open(P, encoding='utf8').read()
L = json.load(open(os.path.join(D, 'out', 'lessons.json'), encoding='utf8'))
VTW = open(os.path.join(D, 'out', 'vt.json'), encoding='utf8').read()
BOOKS = json.load(open(os.path.join(D, 'out', 'books.json'), encoding='utf8'))


def put(h, a, b, anchor, body, before=True):
    if a in h:
        i = h.index(a); j = h.index(b, i) + len(b)
        return h[:i] + body + h[j:]
    assert h.count(anchor) == 1, anchor[:80]
    return h.replace(anchor, body + '\n' + anchor if before else anchor + '\n' + body)


def once(h, old, new):
    if new in h: return h
    assert h.count(old) == 1, old[:100]
    return h.replace(old, new)


# 1) dữ liệu bài lý thuyết
m = re.search(r'(<script type="application/json" id="theory-data">)(.*?)(</script>)', h, re.S)
T = json.loads(m.group(2).replace('<\\/', '</'))
old = T['lessons']; new = {}
for k, v in old.items():
    if k.startswith('avcn2-'):
        if k == 'avcn2-u1':
            for kk in L['order']: new[kk] = L['lessons'][kk]
        continue
    new[k] = v
assert all(k in new for k in L['order'])
T['lessons'] = new
gt = T['books']['avcn2-gt']; gt.update({k: v for k, v in BOOKS['avcn2-gt'].items() if k != 'cover'}); gt['unit'] = 'bài'
T['books']['avcn2-bangtu'] = BOOKS['avcn2-bangtu']
data = json.dumps(T, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
h = h[:m.start(2)] + data + h[m.end(2):]

# 2) CSS, JS
css = open(os.path.join(D, 'vt.css'), encoding='utf8').read().strip()
js = open(os.path.join(D, 'vt.js'), encoding='utf8').read().strip().replace('__VT_DATA__', VTW)
h = put(h, '/* @@VT-CSS */', '/* @@VT-CSS-END */', '/* @@SL-CSS-END */', css, before=False)
h = put(h, '/* @@VT-JS */', '/* @@VT-JS-END */', '/* @@SL-JS */', js, before=True)

# 3) nối vào danh sách bài và trang đọc
h = once(h, "const lessons = (Array.isArray(s.lessons) ? s.lessons : []).filter(l => l && l.id)",
         "const lessons = [...((typeof TH_EXTRA === 'object' && TH_EXTRA && TH_EXTRA[name]) || []), ...(Array.isArray(s.lessons) ? s.lessons : [])].filter(l => l && l.id)")
h = once(h, "      ${slData(l.id) ? `<button class=\"btn btn-sm\" type=\"button\" data-thsl=\"${esc(l.id)}\">${SL_ICON}Slide bài giảng</button>` : ''}\n",
         "      ${slData(l.id) ? `<button class=\"btn btn-sm\" type=\"button\" data-thsl=\"${esc(l.id)}\">${SL_ICON}Slide bài giảng</button>` : ''}\n"
         "      ${vtUnitOf(l.id) ? `<button class=\"btn btn-sm\" type=\"button\" data-vt=\"${vtUnitOf(l.id)}\">${VT_ICON}Luyện từ 5 bậc</button>` : ''}\n")
h = once(h, "  mmReader(l);\n}\nfunction openLesson(id) {", "  mmReader(l);\n  vtReader();\n}\nfunction openLesson(id) {")

# 4) phiên bản 2.6.1
NOTE = 'Bản cập nhật 2.6.1: Anh văn chuyên ngành 2 làm lại cho người mất gốc, có loa đọc từ và Luyện từ 5 bậc.'
h = re.sub(r'(<span class="beta-txt">)Bản cập nhật 2\.6\.0:[^<]*(</span>)', lambda x: x.group(1) + NOTE + x.group(2), h)
LI = '''    <ul class="v1-new">
      <li><b>Anh văn chuyên ngành 2 làm lại cho người mất gốc:</b> mỗi từ có <b>nút loa</b> để nghe đọc, dòng <b>“Đọc gần giống”</b> bằng chữ Việt, nghĩa ngắn, mẹo nhớ, câu ví dụ và câu định nghĩa <b>dịch từng cụm</b>.</li>
      <li>Bài mới <b>U0 · Bắt đầu từ đây</b>: 5 mẫu câu định nghĩa (nhìn đầu câu là biết đáp án loại gì), cách đọc phiên âm, nhãn loại từ, lộ trình 15 ngày. Bài mới <b>Gốc từ</b> giúp đoán nghĩa từ lạ.</li>
      <li><b>Luyện từ 5 bậc</b>: nghe → nghĩa → keyword → định nghĩa (giống đề thi) → điền vào câu. Đúng thì lên bậc, sai thì hỏi lại; app tự nhắc ôn từ sắp quên. Bấm nút <b>Luyện từ 5 bậc</b> ở mỗi Unit.</li>
      <li>Có thêm <b>bảng từ tóm tắt 1 trang mỗi Unit</b> để in (tải ở bài U0).</li>
'''
i = h.index('    <ul class="v1-new">'); j = h.index('    </ul>', i)
h = h[:i] + LI + h[j:]
h = h.replace('2.6.0', '2.6.1')

# 5) Android: nút Quay lại đóng khung Luyện từ trước
if ANDROID:
    h = once(h, "    var sl = q('#th-sl');\n", "    var vt = q('#vt');\n    if (vt && !vt.hidden) { esc(); return true; }\n    var sl = q('#th-sl');\n")

open(P, 'w', encoding='utf8').write(h)
print('ok', P, len(h.encode('utf8')), 'bytes')
