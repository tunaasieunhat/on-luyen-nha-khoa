# Tạo bản app Android (android/app/src/main/assets/www/index.html) từ bản web (index.html).
# Chỉ cần sửa index.html rồi chạy: python3 android/tools/sync.py
# Khác biệt so với bản web:
#   1. Phần đầu trang: bỏ thẻ chia sẻ/manifest/Google Fonts, chừa chỗ <!--FONTS--> để fonts.py nhúng phông lúc build.
#   2. Chèn cầu nối với Android (android/web-extra/bridge.html) ngay trước </head>.
#   3. Bỏ phần chỉ dùng cho web ở cuối trang (service worker, thông báo OneSignal).
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WEB = os.path.join(ROOT, 'index.html')
OUT = os.path.join(ROOT, 'android', 'app', 'src', 'main', 'assets', 'www', 'index.html')
BRIDGE = os.path.join(ROOT, 'android', 'web-extra', 'bridge.html')


def build(web, bridge):
    # 1) đầu trang
    a = web.index('<meta name="description"'); a2 = web.index('\n', a) + 1
    web = web[:a] + web[a2:]
    a = web.index('<link rel="manifest"')
    b = web.index('display=swap">', a) + len('display=swap">')
    s = web[:a].rstrip('\n') + '\n\n<!--FONTS-->' + web[b:]
    # 2) cầu nối Android
    i = s.index('</style>\n</head>') + len('</style>\n')
    s = s[:i] + bridge + s[i:]
    # 3) phần chỉ dùng cho web: từ khối service worker đến hết các script cuối
    a = s.index('<script>\n  // Lưu sẵn để chơi được khi mất mạng')
    b = s.index('</body>', a)
    s = s[:a].rstrip('\n') + '\n' + s[b:]
    return s


if __name__ == '__main__':
    web = open(WEB, encoding='utf8').read()
    bridge = open(BRIDGE, encoding='utf8').read()
    out = build(web, bridge)
    if '--check' in sys.argv:
        cur = open(OUT, encoding='utf8').read()
        print('khớp' if cur == out else 'KHÁC')
        sys.exit(0 if cur == out else 1)
    open(OUT, 'w', encoding='utf8').write(out)
    print('đã tạo', os.path.relpath(OUT, ROOT))
