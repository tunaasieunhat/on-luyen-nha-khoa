# tools/: script đã dùng để làm các bản 2.6.1 – 2.6.3

Các script này được chạy trên một máy làm việc tạm, nên nhiều đường dẫn trong code là đường dẫn tuyệt đối của máy cũ (`/home/claude/work261`, `/home/claude/video262`, `/home/claude/work262s`, `/home/claude/on-luyen-nha-khoa`). Muốn chạy lại thì sửa các đường dẫn đó cho khớp máy mới.

Cách vá chung: app đã dựng (`index.html`, `source/on-luyen-nha-khoa-offline.html`, `android/app/src/main/assets/www/index.html`) được vá trực tiếp bằng các khối có đánh dấu (`/* @@XX-JS */ … /* @@XX-JS-END */`, `<!-- @@XX-PANEL -->`…), hàm `put`/`once` trong mỗi `patchNNN.py` nên chạy lại nhiều lần vẫn ra cùng kết quả. Chạy: `python3 -I patchNNN.py <file.html>`.

| Thư mục | Bản | Nội dung |
|---|---|---|
| `v261-avcn2/` | 2.6.1 | Anh văn chuyên ngành 2 cho người mất gốc: `w1–w3.txt` (177 từ), `build261.py` → `out/lessons.json`, `out/vt.json`; `vt.js`/`vt.css` (loa đọc, Luyện từ 5 bậc); `patch261.py <html> [android]`; `pdf261.py` + `print261.js` (PDF bảng từ); `promo261.py`. `relwait.sh <sha>` chờ build APK xong. |
| `v262-video/` | 2.6.2 | Video bài giảng VLNK Bài 1–5: lời giảng `n1–n5.txt`, `prep.py` → `lines.json` (phiên âm thuật ngữ cho giọng đọc), giọng đọc chạy trên GitHub Actions (nhánh `video-gen`, ra nhánh `lecture-out`), `assemble.py <lecture-out/out> 1 2 3 4 5` dựng MP4 480p, `mkdata.py` → `out/videos.json`, `vd.js`/`vd.css`, `patch262.py`, `rserve.py` (máy chủ thử có hỗ trợ tua). |
| `v263-avcn2-slides/` | 2.6.3 | Phần còn thiếu so với `avcn2-src/`: `build_all.sh` (bản cũ, bản in dạng ảnh), `shot.js` (chụp slide kiểm tra), `handout2.js` (cách in trực tiếp, lỗi cỡ chữ, không dùng), `fixdup.py`. Bản in đang dùng: `avcn2-src/slidepdf.js` + `avcn2-src/impose.py`. |
| `tests/` | | Kiểm thử Playwright (`t261.js`… `t263.js`, `t4.js`, `t5.js`) và `perf.js` (đo giật lag khi cuộn, chưa chạy xong). |
