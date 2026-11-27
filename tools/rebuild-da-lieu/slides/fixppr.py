# Giữ <a:pPr> đầu tiên trong mỗi đoạn (pptxgenjs ghi pPr cho từng run): python3 fixppr.py file.pptx...
import sys, zipfile, re, shutil, os
PPR = re.compile(r'<a:pPr\b[^>]*?(?:/>|>.*?</a:pPr>)', re.S)
def fixp(m):
    p = m.group(0); seen = [False]
    def r(mm):
        if seen[0]: return ''
        seen[0] = True; return mm.group(0)
    return PPR.sub(r, p)
for f in sys.argv[1:]:
    tmp = f + '.tmp'; n = 0
    with zipfile.ZipFile(f) as zi, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
        for it in zi.infolist():
            data = zi.read(it.filename)
            if re.match(r'ppt/slides/slide\d+\.xml$', it.filename):
                s = data.decode('utf8'); s2 = re.sub(r'<a:p>.*?</a:p>', fixp, s, flags=re.S); n += s != s2; data = s2.encode('utf8')
            zo.writestr(it, data)
    shutil.move(tmp, f); print(os.path.basename(f), n, 'slide sửa')
