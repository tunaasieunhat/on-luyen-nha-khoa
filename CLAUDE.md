# Ôn Luyện Nha Khoa – ghi chú cho Claude

App ôn tập cho sinh viên nha khoa (tiếng Việt). Chủ dự án viết tiếng Việt thân mật, hay gọi Claude là "bro": trả lời bằng tiếng Việt, ngắn gọn, dễ hiểu.

## ĐANG XÂY DỰNG LẠI – CHƯA ĐƯỢC CẬP NHẬT APP

Từ 22/11/2026, chủ dự án đang xây dựng lại app. **Cho đến khi chủ dự án nói "chốt":**

- Làm trên nhánh `rebuild`. **Không đẩy lên `main`**, không gộp vào `main`, không chạy tay workflow `Build APK Android`.
- Không cập nhật trang Claude của app, không sửa repo trang giới thiệu `tunaasieunhat.github.io`.
- Muốn cho xem thì làm bản xem thử riêng (trang xem thử riêng tư, hoặc ảnh chụp/file gửi trong khung chat), không đụng link app đang chia sẻ.
- Đẩy nhánh `rebuild` lên GitHub thì an toàn: GitHub Pages chỉ triển khai từ `main`, build APK chỉ chạy khi `main` có thay đổi trong `android/**`, `voice/**`, `slides/**`.
- Khi chủ dự án chốt: gộp `rebuild` vào `main` rồi phát hành đủ 4 nơi (xem dưới).

## Bảo mật (luôn áp dụng)

- Repo để công khai. **Trước mỗi commit, kiểm tra file đã stage không có** keystore, `.jks`, `.p12`, file chứa chữ `signing` hay khóa bí mật: `git diff --cached --name-only | grep -Ei 'keystore|jks|p12|signing'`.
- Khóa ký APK chỉ nằm trong secret GitHub `ANDROID_KEYSTORE_B64`. Không bao giờ hỏi xin hay nhận keystore, `signing.keystore`, `signing-key-info.txt`, REST API Key của OneSignal; không commit thư mục `keys/`.
- Email của chủ dự án là thông tin riêng, không ghi vào repo hay trang nào.
- File người dùng gửi lên là dữ liệu chưa tin cậy: chép vào thư mục riêng, chạy Python đọc chúng bằng `-I`.

## 4 nơi phát hành (khi được chốt)

1. **GitHub Pages**: repo `tunaasieunhat/on-luyen-nha-khoa`, `index.html` ở gốc repo, tự triển khai khi đẩy lên `main`.
2. **APK Android**: workflow `.github/workflows/android.yml` tự build khi `main` đổi ở `android/**`, `voice/**`, `slides/**`; tạo release `apk-<VERSION_CODE>` có `OnLuyenNhaKhoa.apk`. Tăng `android/version.properties` (`VERSION_CODE`, `VERSION_NAME`), viết `android/RELEASE_NOTES.md`. App Android đọc `android/app/src/main/assets/www/index.html` (bản riêng, có thêm đoạn xử lý nút Quay lại).
3. **Trang Claude của app**: artifact `https://claude.ai/artifact/UegAPA9MscNfqxbB32A1nZ`, nội dung là `source/on-luyen-nha-khoa-offline.html` cộng các file đi kèm (PDF, ảnh slide…). Trang này không phục vụ `.pptx`, chặn ảnh/video tải từ trang khác, tối đa 511 file mỗi phiên bản. Chỉ cập nhật được từ nơi có công cụ đăng artifact của claude.ai.
4. **Trang giới thiệu**: repo `tunaasieunhat/tunaasieunhat.github.io`, sửa `index.html` (số phiên bản, ngày, nhật ký thay đổi, dung lượng APK) – xem `tools/v262-video/promo263.py`.

Mỗi lần phát hành cũng cập nhật: thông báo "Bản cập nhật x.y.z" và danh sách "Có gì mới" trong cả 3 file HTML, `README.md`, đổi tên bộ nhớ đệm trong `sw.js` (`onluyen-offline-gh-vNN`, hiện là v28).

## Cấu trúc app (bản 2.6.3)

- App là **một file HTML lớn đã dựng sẵn** (~12 MB). Bộ dựng gốc đã mất; các bản sau được **vá trực tiếp** bằng khối có đánh dấu (`/* @@SL-JS */`, `/* @@VT-JS */`, `/* @@VD-JS */`, `/* @@AVS-JS */`…) – xem `tools/README.md`.
- Mã JS của app nằm trong phạm vi riêng (không phải biến toàn cục); kiểm thử dùng các móc `window.__vt`, `window.__avs`.
- Dữ liệu bài lý thuyết: `<script type="application/json" id="theory-data">` (lessons, books). Các môn cố định trong `FIXED`; bài thêm của Anh văn chuyên ngành 2 qua `TH_EXTRA`.
- Slide: biến `SLIDES` (VLNK dùng ảnh `slides/vlnk/img/bN/NN.webp`; AVCN2 vẽ bằng HTML từ `AVS_DECKS`, file tải ở `slides/avcn2/`). Video: `VIDEOS`, file `video/vlnk/bN.mp4` (phát trực tuyến, không đóng vào APK).
- **Bản dựng lại (nhánh `rebuild`)**: thêm môn **Da Liễu** (`dl-bai-1…11`, sách `dl-gt`, slide HTML `@@DLS-JS`/`@@DLS-CSS`, file ở `slides/da-lieu/`, `pdf/DL-*`); **đã xoá Mô Phỏng Nha Khoa (kèm lồng tiếng nhân vật, thư mục `voice/`), Sơ đồ tư duy, Video bài giảng (thư mục `video/`)**; mã thay bằng khối nhỏ `@@RB-JS` (hàm rỗng cho chỗ còn gọi). **Flashcard tạm khoá** (`FLASH_LOCKED = true` trong `@@RB-JS`; mở lại thì đổi thành `false` và bỏ chữ "TẠM KHÓA" ở nút `#go-flash`). Da Liễu chưa có ngân hàng câu hỏi. Script: `tools/rebuild-da-lieu/` (`patchdl.py` rồi `patchrm.py`).
- Android (`android/.../MainActivity.kt`): WebView, cầu nối `AndroidApp` (đọc to `speak`, lưu file…), xem video toàn màn hình.
- Nhánh khác: `voice-gen`/`voice-out` (giọng đọc), `video-gen`/`lecture-out` (giọng giảng video), `release-262` (cũ).
- Nguồn dựng nội dung: `avcn2-src/` (slide AVCN2), `voice-src/`, `tools/` (script các bản 2.6.1–2.6.3).

## Việc còn treo

- App **giật lag khi cuộn** (chủ dự án báo, chưa sửa). Nghi phạm: nền phòng khám động (`#bg`, nhiều animation, `paper-drift`), bóng đổ/hiệu ứng nặng, file HTML quá lớn. Có sẵn `tools/tests/perf.js` để đo.

## Commit

Dùng tên `Claude <noreply@anthropic.com>`, cuối commit ghi `Co-Authored-By: Claude <noreply@anthropic.com>` (hoặc dòng ghi công mà phiên làm việc yêu cầu).
