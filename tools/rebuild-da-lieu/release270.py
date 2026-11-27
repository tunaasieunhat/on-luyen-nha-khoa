# Version 2.7.0: thông báo cập nhật + Có gì mới trong 3 file HTML (chạy lại được)
import sys, re
NOTE = 'Bản cập nhật 2.7.0: Môn Da Liễu mới (giáo trình 11 bài và slide); app gọn hơn, bỏ Mô phỏng, Sơ đồ tư duy, Video.'
LI = '''    <ul class="v1-new">
      <li><b>Môn Da Liễu mới, 11 bài:</b> giáo trình biên soạn lại dễ hiểu, 77 hình minh hoạ, mẹo nhớ và phần liên hệ Răng Hàm Mặt; tải PDF từng bài hoặc <b>giáo trình trọn bộ</b>.</li>
      <li><b>Slide bài giảng Da Liễu:</b> 11 bộ slide có hình, <b>66 câu trắc nghiệm</b> chạm để xem giải thích; tải PowerPoint và bản in 4 slide/trang.</li>
      <li><b>App gọn nhẹ hơn:</b> bỏ Mô Phỏng Nha Khoa, Sơ đồ tư duy và Video bài giảng để tập trung vào lý thuyết, slide và làm bài.</li>
      <li><b>Flashcard tạm khóa</b> để làm lại, sẽ mở lại ở bản sau.</li>
    </ul>'''
for F in sys.argv[1:]:
    h = open(F, encoding='utf8').read()
    h = re.sub(r'(<span class="beta-txt">)Bản cập nhật [\d.]+:[^<]*(</span>)', lambda x: x.group(1) + NOTE + x.group(2), h)
    i = h.index('    <ul class="v1-new">'); j = h.index('    </ul>', i) + len('    </ul>'); h = h[:i] + LI + h[j:]
    for a, b in [('Version 2.6.3</span>', 'Version 2.7.0</span>'), ('Bản cập nhật 2.6.3', 'Bản cập nhật 2.7.0'), ('Tải app version 2.6.3', 'Tải app version 2.7.0'), ("'2.6.3'", "'2.7.0'")]:
        h = h.replace(a, b)
    open(F, 'w', encoding='utf8').write(h)
    print(F, h.count('2.7.0'), 'chỗ 2.7.0; còn 2.6.3 ngoài chú thích:', len(re.findall(r"(?<!Version )2\.6\.3(?![^\n]*\*/)", h)))
