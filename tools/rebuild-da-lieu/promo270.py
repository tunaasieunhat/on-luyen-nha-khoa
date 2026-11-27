# Trang giới thiệu: cập nhật lên 2.7.0 – python3 -I promo270.py <index.html> <MB>
import re, sys
p, mb = sys.argv[1], sys.argv[2]
h = open(p, encoding='utf8').read()
def rep(a, b):
    global h
    assert h.count(a) == 1, a[:70]; h = h.replace(a, b)
rep('56 bài tóm tắt và sơ đồ tư duy. App Android', '67 bài tóm tắt, slide bài giảng, môn Da Liễu mới. App Android')
rep('5 môn, 5.500 câu, Phòng Thi, tóm tắt lý thuyết và sơ đồ tư duy.">', '5 môn, 5.500 câu, Phòng Thi, tóm tắt lý thuyết và slide bài giảng.">')
rep('alt="Sảnh của app: hai mục Ôn Luyện Kiến Thức và Mô Phỏng Nha Khoa"', 'alt="Sảnh của app: mục Ôn Luyện Kiến Thức và Cài đặt"')
a = h.index('      <article class="feat" data-rv>\n        <div class="feat-shot phone"><img src="img/mindmap.webp"')
b = h.index('      <div class="tray" data-rv>')
h = h[:a] + '''      <article class="feat" data-rv>
        <div class="feat-shot phone"><img src="img/da-lieu.webp" alt="Ôn tập lý thuyết môn Da Liễu, bài Sang thương cơ bản: mục tiêu bài học và mục lục" width="600" height="1298" loading="lazy"></div>
        <div class="feat-txt">
          <h3>Lý thuyết dễ hiểu</h3>
          <p class="one">67 bài tóm tắt, đọc ngay trong app hoặc tải về PDF.</p>
          <ul class="facts">
            <li style="--i:0">Mới: môn Da Liễu 11 bài, 77 hình minh hoạ</li>
            <li style="--i:1">Mẹo nhớ, bảng so sánh, liên hệ Răng Hàm Mặt</li>
            <li style="--i:2">Giáo trình trọn bộ 1 file PDF cho từng môn</li>
          </ul>
        </div>
      </article>
      <article class="feat flip" data-rv>
        <div class="feat-shot phone"><img src="img/slide.webp" alt="Slide bài giảng Da Liễu: slide Dát có hình minh hoạ và khung mẹo nhớ" width="600" height="1298" loading="lazy"></div>
        <div class="feat-txt">
          <h3>Slide bài giảng</h3>
          <p class="one">Slide rõ chữ trên điện thoại, có trắc nghiệm ngay trên slide.</p>
          <ul class="facts">
            <li style="--i:0">Vật liệu nha khoa, Anh văn chuyên ngành 2, Da Liễu</li>
            <li style="--i:1">Chạm đáp án là biết đúng sai, có giải thích</li>
            <li style="--i:2">Tải PowerPoint và bản in 4 slide/trang</li>
          </ul>
        </div>
      </article>

''' + h[b:]
rep('<span><b>Flashcard</b>Lật thẻ ôn nhanh</span>', '<span><b>Tải PDF</b>In ra học trên giấy</span>')
rep('<p class="ver">Bản <b>2.6.3</b>, ra ngày 19/11/2026.', '<p class="ver">Bản <b>2.7.0</b>, ra ngày 27/11/2026.')
rep('<span>Tải OnLuyenNhaKhoa.apk<small>Version 2.6.3</small></span>', '<span>Tải OnLuyenNhaKhoa.apk<small>Version 2.7.0</small></span>')
h = re.sub(r'<small>File APK, \d+ MB</small>', f'<small>File APK, {mb} MB</small>', h)
rep('<span class="new">Mới nhất</span>', '')
i = h.index('<ol class="log" reversed>'); j = h.index('</ol>', i)
log = h[i:j]; n = [0]
def renum(m):
    n[0] += 1; return f'<li style="--i:{n[0]}">'
log = re.sub(r'<li style="--i:\d+">', renum, log)
entry = '''<li style="--i:0">
              <div class="when"><b>2.7.0</b><time datetime="2026-11-27">27/11/2026</time><span class="new">Mới nhất</span></div>
              <ul>
                <li>Môn Da Liễu mới: giáo trình 11 bài và slide</li>
                <li>Gọn hơn: bỏ Mô phỏng, Sơ đồ tư duy, Video bài giảng</li>
                <li>Flashcard tạm khóa để làm lại</li>
              </ul>
            </li>
            '''
log = log.replace('<ol class="log" reversed>\n            ', '<ol class="log" reversed>\n            ' + entry, 1)
assert log.count('Mới nhất') == 1 and '<b>2.7.0</b>' in log
h = h[:i] + log + h[j:]
assert 'mindmap.webp' not in h and 'sim.webp' not in h
open(p, 'w', encoding='utf8').write(h)
print('ok promo 2.7.0;', n[0] + 1, 'mục; APK', mb, 'MB')
