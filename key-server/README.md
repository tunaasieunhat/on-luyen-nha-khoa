# Máy chủ key kích hoạt

Chỉ người có key mới vào được app Ôn Luyện Nha Khoa. Mỗi người một key, chủ app tạo và quản lý ở trang `/admin`.

Chạy trên **Cloudflare Workers + D1** (gói miễn phí: 100.000 lượt gọi/ngày, đủ cho hàng nghìn người dùng).

## Cách hoạt động

| | |
| --- | --- |
| Nhập key lần đầu | App gửi key + mã máy lên máy chủ (`/api/activate`). Cần có mạng. |
| Mở app những lần sau | Có mạng thì kiểm tra lại (`/api/check`), tối đa mỗi 6 giờ một lần. |
| Mất mạng | Vẫn dùng được 14 ngày kể từ lần kiểm tra cuối, sau đó phải bật mạng để xác minh lại. |
| Key bị khoá / hết hạn / máy bị gỡ | Lần kiểm tra kế tiếp, app đưa người dùng về màn đăng ký. |
| Số máy | Mỗi key có giới hạn số máy (mặc định 1). Xoá dữ liệu app hoặc đổi trình duyệt được tính là máy mới; chủ app gỡ máy cũ ở trang quản lý. |
| Dò key | Nhập sai 10 lần trong 15 phút thì bị chặn 15 phút. Key có 12 ký tự ngẫu nhiên (~10^17 khả năng). |

Key có dạng `NK-XXXX-XXXX-XXXX`, không dùng các ký tự dễ nhầm (0, O, 1, I, L). Người dùng gõ chữ thường hay bỏ gạch nối đều được.

## Đưa lên Cloudflare (làm một lần)

```bash
cd key-server
npm install
npx wrangler login                      # hoặc đặt CLOUDFLARE_API_TOKEN
npx wrangler d1 create onluyen-key      # chép database_id in ra vào wrangler.toml
npm run db:init                         # tạo bảng
npx wrangler secret put ADMIN_PASSWORD  # mật khẩu trang quản lý (ít nhất 8 ký tự)
npm run deploy                          # in ra địa chỉ https://onluyen-key.<tên>.workers.dev
```

Sau đó đổi `KEY_API` trong `index.html` và `android/app/src/main/assets/www/index.html` thành địa chỉ vừa in ra.

## Quản lý key

Mở `https://onluyen-key.<tên>.workers.dev/admin`, đăng nhập bằng mật khẩu quản lý:

- **Tạo key**: tên người dùng, ghi chú, số máy, hạn dùng (vĩnh viễn, 7 ngày… hoặc chọn ngày), tạo nhiều key một lần.
- **Chép tin nhắn gửi**: đoạn tin có sẵn key và hướng dẫn, dán vào Zalo/Messenger.
- **Khoá / Mở khoá**, **Sửa** (tên, số máy, hạn), **Gỡ máy**, **Xoá**.

## Chạy thử trên máy

```bash
printf 'ADMIN_PASSWORD="mat-khau-thu"\n' > .dev.vars
npx wrangler d1 execute onluyen-key --local --file=schema.sql
npm run dev   # http://127.0.0.1:8787/admin
```

## Lưu ý về bảo mật

Key chặn được người dùng bình thường. Nhưng app là web tĩnh và repo đang công khai: người rành kỹ thuật vẫn có thể tải mã nguồn từ GitHub và sửa để bỏ qua bước nhập key. Muốn chặn chặt hơn phải giấu nội dung (repo riêng tư, hoặc mã hoá nội dung và chỉ giải mã khi key hợp lệ).
