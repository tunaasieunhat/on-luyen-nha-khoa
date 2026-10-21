# Ôn Luyện Nha Khoa

Ứng dụng ôn thi Răng Hàm Mặt dạng trò chơi phòng khám: làm trắc nghiệm, đọc tóm tắt lý thuyết, ôn flashcard. **Version 2.4** là phiên bản mới nhất; các môn học sẽ được liên tục thêm vào.

| | Link |
| --- | --- |
| **App Android** (khuyên dùng, chạy offline, không cần Chrome) | [OnLuyenNhaKhoa.apk](https://github.com/tunaasieunhat/on-luyen-nha-khoa/releases/latest/download/OnLuyenNhaKhoa.apk) |
| **Bản web** (iPhone, máy tính; dùng offline sau lần mở đầu) | https://tunaasieunhat.github.io/on-luyen-nha-khoa/ |

Bản Online beta 2.3 (có AI, chạy trên Claude) đã chính thức đóng cửa: link cũ và trang `online/` chỉ còn thông báo kèm link tải app.

Phát hiện lỗi, sai đáp án hay câu hỏi có vấn đề: liên hệ tunaasieunhat@gmail.com.

## Tính năng chung

- **Câu hỏi hệ thống:** 5.500 câu của 5 môn, chia theo môn, theo bài và theo mức độ (Dễ, Vận dụng, Nâng cao).
  - Vật liệu nha khoa: 11 bài, mỗi bài 100 câu Dễ, 50 câu Vận dụng, 50 câu Nâng cao.
  - Anh văn chuyên ngành 2: 15 Unit, mỗi Unit 30 câu Dễ, 15 câu Vận dụng, 15 câu Nâng cao.
  - Nhi khoa: 9 bài, mỗi bài 60 câu Dễ, 30 câu Vận dụng, 30 câu Nâng cao.
  - Mắt: 5 bài, mỗi bài 60 câu Dễ, 30 câu Vận dụng, 30 câu Nâng cao.
  - Tai - Mũi - Họng: 6 bài, mỗi bài 60 câu Dễ, 30 câu Vận dụng, 30 câu Nâng cao.
- **Chọn mức độ** khi làm Câu Hỏi: Tất cả, Dễ, Vận dụng hoặc Nâng cao.
- **Phòng Thi:** thi thử có giờ theo từng môn, đề 60% Dễ, 30% Vận dụng, 10% Nâng cao; chọn 30/60/90 phút và 30/45/60/75/90/105/120 câu; chấm thang 10, xem lại câu sai, lưu lịch sử và làm tiếp bài đang dở. Mở cho cả 5 môn.
- **Hình minh hoạ** cho từng câu hỏi, vẽ sẵn trong file nên không cần mạng.
- **Ôn tập lý thuyết:** 46 bài, bài nào cũng tải về được dạng PDF. Môn Mắt (bản 2.1.1) được biên soạn lại theo lối giảng giải, kèm 30 hình minh hoạ từ bài giảng (nhãn tiếng Việt, chạm để phóng to); môn Nhi khoa (bản 2.1.2) cũng được biên soạn lại, có ví dụ tính toán và phần liên hệ Răng Hàm Mặt. Từ bản 2.3, Mắt và Nhi khoa có thêm **giáo trình trọn bộ**: 1 file PDF gồm bìa, mục lục có số trang (bấm để nhảy trang) và toàn bộ các bài. Bản 2.4 biên soạn lại 15 Unit Anh văn chuyên ngành 2 (phiên âm, cấu tạo từ, ví dụ, từ dễ nhầm, đọc hiểu tình huống) và thêm giáo trình trọn bộ cho môn này.
- **Sơ đồ tư duy** cho cả 46 bài: xem dạng toả tròn hoặc dạng cây, che ý nhỏ để tự kiểm tra, tải về dạng ảnh PNG.
- **Flashcard và tự soạn câu hỏi.**
- **Giao diện mùa đông:** tuyết rơi, đèn nháy, **nhạc nền chill nhẹ nhàng phong cách mùa đông** (do trình duyệt tự phát, không cần tải) và **nền phòng khám hoạt hình** có chuyển động.

## Cấu trúc thư mục

```
index.html, 404.html     Bản web (trang chính của GitHub Pages)
manifest.json, sw.js     Cài như ứng dụng và lưu để dùng offline
pdf/                     46 file PDF tóm tắt lý thuyết
icon-*.png, og.png       Biểu tượng và ảnh chia sẻ
online/                  Thông báo bản Online đã đóng cửa, kèm link tải app
source/                  Mã nguồn hai bản đang chạy trên Claude (mỗi bản một file HTML)
android/                 App Android viết bằng Kotlin (gói sẵn toàn bộ app, không cần trình duyệt)
.github/workflows/       Tự build file APK mỗi khi thư mục android/ thay đổi
```

## Bật trang web miễn phí (GitHub Pages)

1. Vào **Settings → Pages**.
2. Ở **Build and deployment**, chọn **Source: Deploy from a branch**.
3. Chọn nhánh **main**, thư mục **/ (root)**, bấm **Save**.
4. Đợi 1–2 phút, trang chạy ở:
   - Bản web: https://tunaasieunhat.github.io/on-luyen-nha-khoa/

## Cài lên điện thoại

- **App Android (khuyên dùng):** tải [OnLuyenNhaKhoa.apk](https://github.com/tunaasieunhat/on-luyen-nha-khoa/releases/latest/download/OnLuyenNhaKhoa.apk), mở file và cho phép cài. App tên **Ôn Luyện Nha Khoa**, chạy hoàn toàn offline, không cần Chrome; có bản mới thì app tự báo.
  - Mã nguồn ở thư mục `android/` (Kotlin). Mỗi lần đẩy thay đổi lên, GitHub Actions tự build và đăng APK lên **Releases** (tăng `VERSION_CODE` trong `android/version.properties` để app trên máy nhận bản mới).
  - Khóa ký nằm trong **Settings → Secrets and variables → Actions → `ANDROID_KEYSTORE_B64`**, không để trong repo. Cất kỹ bản sao của khóa này.
- **Thêm vào màn hình chính:** mở link bản web bằng Chrome → menu ⋮ → **Thêm vào màn hình chính** (hoặc **Cài đặt ứng dụng**).
- **Đóng gói APK:** vào https://www.pwabuilder.com, dán link rồi chọn **Package For Stores → Android → Google Play**.
  - Bản Offline: link gốc, Package ID `io.github.tunaasieunhat.onluyennhakhoa`, tên ngắn `Ôn Luyện NK`.
  - Cất kỹ `signing.keystore` và `signing-key-info.txt` trong gói tải về: sau này làm lại APK phải dùng đúng khoá này.

## Thông báo cập nhật (bản web)

- Ở sảnh có khung **Nhận thông báo khi có bản cập nhật**, bấm **Bật thông báo** rồi cho phép.
- Mỗi lần có bản mới: vào [OneSignal](https://dashboard.onesignal.com) → app **Ôn Luyện Nha Khoa** → **Messages → New Push**, điền tiêu đề, nội dung, **Launch URL** `https://tunaasieunhat.github.io/on-luyen-nha-khoa/` → **Send**.
- Mã nguồn: đoạn OneSignal ở cuối `index.html`, service worker riêng ở `push/onesignal/OneSignalSDKWorker.js`.

## Ghi chú

- File trong `source/` là mã nguồn lưu dự phòng (bản Online beta 2.3 đã đóng cửa).
- Repo đang để công khai, ai có link cũng xem được câu hỏi và phần tóm tắt. Nội dung soạn theo giáo trình môn học, dùng để ôn tập.
