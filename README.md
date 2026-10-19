# Ôn Luyện Nha Khoa

Ứng dụng ôn thi Răng Hàm Mặt dạng trò chơi phòng khám: làm trắc nghiệm, đọc tóm tắt lý thuyết, ôn flashcard. Có hai phiên bản.

| | **Ôn Luyện Nha Khoa - Offline** | **Ôn Luyện Nha Khoa - Online** |
| --- | --- | --- |
| Mở ở đâu | Trình duyệt, cài lên màn hình chính hoặc đóng gói APK | Trên Claude (claude.ai) |
| Cần mạng | Chỉ lần mở đầu tiên, sau đó dùng offline | Có |
| AI soạn câu hỏi, flashcard từ PDF/Word | Không | Có (cần đăng nhập Claude) |
| Ngân hàng câu hỏi dùng chung | Không (lưu trên máy) | Có |
| Link | https://tunaasieunhat.github.io/on-luyen-nha-khoa/ | https://claude.ai/artifact/VfrBVHMcBpcCVMh52af7pn |

## Tính năng chung

- **Câu hỏi hệ thống:** 1.550 câu, chia theo môn và theo bài.
  - Vật liệu nha khoa: 11 bài, mỗi bài 100 câu.
  - Anh văn chuyên ngành 2: 15 Unit, mỗi Unit 30 câu.
- **Hình minh hoạ** cho từng câu hỏi, vẽ sẵn trong file nên không cần mạng.
- **Ôn tập lý thuyết:** 26 bài tóm tắt, bài nào cũng tải về được dạng PDF.
- **Sơ đồ tư duy** cho cả 26 bài: xem dạng toả tròn hoặc dạng cây, che ý nhỏ để tự kiểm tra, tải về dạng ảnh PNG.
- **Flashcard và tự soạn câu hỏi.**
- **Màn mở đầu có nhạc nền** (nhạc do trình duyệt tự phát, không cần tải) và **nền phòng khám hoạt hình** có chuyển động.

## Cấu trúc thư mục

```
index.html, 404.html     Bản Offline (trang chính của GitHub Pages)
manifest.json, sw.js     Cài như ứng dụng và lưu để dùng offline
pdf/                     26 file PDF tóm tắt lý thuyết
icon-*.png, og.png       Biểu tượng và ảnh chia sẻ
online/                  Trang mở bản Online: chuyển thẳng vào link Claude
source/                  Mã nguồn hai bản đang chạy trên Claude (mỗi bản một file HTML)
```

## Bật trang web miễn phí (GitHub Pages)

1. Vào **Settings → Pages**.
2. Ở **Build and deployment**, chọn **Source: Deploy from a branch**.
3. Chọn nhánh **main**, thư mục **/ (root)**, bấm **Save**.
4. Đợi 1–2 phút, trang chạy ở:
   - Bản Offline: https://tunaasieunhat.github.io/on-luyen-nha-khoa/
   - Trang mở bản Online: https://tunaasieunhat.github.io/on-luyen-nha-khoa/online/

## Cài lên điện thoại

- **Thêm vào màn hình chính:** mở link bản Offline bằng Chrome → menu ⋮ → **Thêm vào màn hình chính** (hoặc **Cài đặt ứng dụng**).
- **Đóng gói APK:** vào https://www.pwabuilder.com, dán link rồi chọn **Package For Stores → Android → Google Play**.
  - Bản Offline: link gốc, Package ID `io.github.tunaasieunhat.onluyennhakhoa`, tên ngắn `Ôn Luyện NK`.
  - Bản Online: link `online/`, Package ID `io.github.tunaasieunhat.onluyennhakhoa.online`, tên ngắn `NK Online`. Biểu tượng có huy hiệu AI màu xanh để dễ phân biệt.
  - Cất kỹ `signing.keystore` và `signing-key-info.txt` trong gói tải về: sau này làm lại APK phải dùng đúng khoá này.

## Thông báo cập nhật (bản Offline)

- Ở sảnh có khung **Nhận thông báo khi có bản cập nhật**, bấm **Bật thông báo** rồi cho phép.
- Mỗi lần có bản mới: vào [OneSignal](https://dashboard.onesignal.com) → app **Ôn Luyện Nha Khoa** → **Messages → New Push**, điền tiêu đề, nội dung, **Launch URL** `https://tunaasieunhat.github.io/on-luyen-nha-khoa/` → **Send**.
- Mã nguồn: đoạn OneSignal ở cuối `index.html`, service worker riêng ở `push/onesignal/OneSignalSDKWorker.js`.

## Ghi chú

- AI của bản Online chỉ chạy khi mở trong Claude. Trang `online/` và file trong `source/` chỉ để mở app và lưu dự phòng.
- Repo đang để công khai, ai có link cũng xem được câu hỏi và phần tóm tắt. Nội dung soạn theo giáo trình môn học, dùng để ôn tập.
