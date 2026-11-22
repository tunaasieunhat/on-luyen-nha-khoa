# Trang giới thiệu: cập nhật lên 2.6.2 (phiên bản, nhật ký, dung lượng APK) – python3 -I promo261.py <index.html> <MB>
import re, sys
p, mb = sys.argv[1], sys.argv[2]
h = open(p, encoding='utf8').read()
def rep(a, b):
    global h
    assert h.count(a) == 1, a; h = h.replace(a, b)
rep('<p class="ver">Bản <b>2.6.1</b>, ra ngày 15/11/2026.', '<p class="ver">Bản <b>2.6.2</b>, ra ngày 18/11/2026.')
rep('<span>Tải OnLuyenNhaKhoa.apk<small>Version 2.6.1</small></span>', '<span>Tải OnLuyenNhaKhoa.apk<small>Version 2.6.2</small></span>')
h = re.sub(r'<small>File APK, \d+ MB</small>', f'<small>File APK, {mb} MB</small>', h)
rep('<span class="new">Mới nhất</span>', '')
i = h.index('<ol class="log" reversed>'); j = h.index('</ol>', i)
log = h[i:j]; n = [0]
def renum(m):
    n[0] += 1; return f'<li style="--i:{n[0]}">'
log = re.sub(r'<li style="--i:\d+">', renum, log)
entry = '''<li style="--i:0">
              <div class="when"><b>2.6.2</b><time datetime="2026-11-18">18/11/2026</time><span class="new">Mới nhất</span></div>
              <ul>
                <li>Video bài giảng Vật liệu nha khoa Bài 1–5</li>
                <li>Giọng giảng nữ, phụ đề tiếng Việt</li>
              </ul>
            </li>
            '''
log = log.replace('<ol class="log" reversed>\n            ', '<ol class="log" reversed>\n            ' + entry, 1)
assert log.count('Mới nhất') == 1 and '<b>2.6.2</b>' in log
h = h[:i] + log + h[j:]
open(p, 'w', encoding='utf8').write(h)
print('ok promo 2.6.2;', n[0] + 1, 'mục; APK', mb, 'MB')
