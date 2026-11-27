# Bản dựng lại: môn Da Liễu + bỏ Sơ đồ tư duy, Video bài giảng

Làm trên nhánh `rebuild` (27/11/2026). Máy làm việc tạm: `/home/claude/dl` (đường dẫn tuyệt đối trong script), giáo trình gốc ở `/home/claude/dl/in/dl.pdf` (không đưa vào repo).

**Giáo trình (11 bài)**
- `src/bN.md`: bài viết lại theo cú pháp gọn (xem đầu `md2html.py`), `[fig N]` lấy hình N trong `figs2.json` (77 hình cắt từ giáo trình, file `fig/fNN.webp`).
- `python3 md2html.py` → `out/lessons.json`.
- `python3 pdfdl.py html` → `python3 jpgprint.py` (hình JPEG cho PDF nhỏ) → `node print.js print/jobs.json` → `python3 pdfdl.py book` (bìa + mục lục + 11 bài = `GiaoTrinh-Da-lieu.pdf`).
- `factnum.py`: so mọi con số trong bài và slide với văn bản nguồn.

**Slide (11 bộ, vẽ bằng HTML trong app)**
- `slides/src/bN.txt`: nguồn slide (cú pháp ở đầu `slides/deck.py`): mục tiêu, slide nội dung (ý, bảng, hình, khung mẹo), `??` trắc nghiệm, tổng kết. Đáp án được xáo cố định theo câu.
- `deck.py` → `out/decks.json`; `dls.js` + `dls.css`: bộ vẽ (dùng lại khung `.avs` của AVCN2, màu hồng đất).
- `mkrender.py` + `shot.js`: chụp kiểm tra; `build_pdf.sh 1 … 11`: bản in 4 slide/trang (`slidepdf.js` + `impose.py`); `pptx_dl.js` rồi `fixppr.py` (pptxgenjs ghi thừa `<a:pPr>` giữa đoạn) → PowerPoint.

**Vá app**: `python3 -I patchdl.py <file.html>` cho 3 file HTML (chạy lại được). Việc làm: xoá dữ liệu `mindmap-data` và `VIDEOS` (tab, nút tự ẩn), sửa 3 câu nhắc tới sơ đồ, thêm môn Da Liễu vào `fixed-data`, bài + sách vào `theory-data` (hình bài học trỏ tới `slides/da-lieu/fig/`, không nhúng), khối `@@DLS-CSS`, `@@DLS-JS` (đăng ký slide vào `SLIDES`/`AVS_DECKS`).

**File phát hành**: `pdf/DL-Bai-*.pdf`, `pdf/GiaoTrinh-Da-lieu.pdf`, `slides/da-lieu/*.pptx`, `*-BanIn.pdf`, `slides/da-lieu/fig/*.webp`. Kiểm thử: `tools/tests/tdl.js`.
