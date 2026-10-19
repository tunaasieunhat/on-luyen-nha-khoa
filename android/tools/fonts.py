# Tải phông chữ (Baloo 2, Be Vietnam Pro, JetBrains Mono) về nằm sẵn trong app để không cần mạng.
# Chạy lúc build trên GitHub Actions: python3 android/tools/fonts.py android/app/src/main/assets/www
# Lỗi mạng thì bỏ qua: app vẫn chạy với phông của máy.
import os, re, sys, urllib.request

WWW = sys.argv[1]
CSS_URL = ('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800'
           '&family=Be+Vietnam+Pro:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap')
UA = 'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36'
KEEP = {'vietnamese', 'latin', 'latin-ext'}
MARK = '<!--FONTS-->'


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def build(css, fetch, outdir):
    """Giữ các khối tiếng Việt / Latin, tải từng file woff2 và đổi link sang file trong app."""
    blocks = re.findall(r'/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{[^}]*\})', css)
    kept, n = [], 0
    for subset, block in blocks:
        if subset not in KEEP:
            continue
        m = re.search(r'url\((https://fonts\.gstatic\.com/[^)]+)\)', block)
        if not m:
            continue
        name = f'f{n:02d}.woff2'; n += 1
        with open(os.path.join(outdir, name), 'wb') as f:
            f.write(fetch(m.group(1)))
        kept.append(f'/* {subset} */\n' + block.replace(m.group(1), 'fonts/' + name))
    return '\n'.join(kept), n


def main():
    idx = os.path.join(WWW, 'index.html')
    html = open(idx, encoding='utf8').read()
    if MARK not in html:
        print('fonts: không thấy chỗ chèn phông, bỏ qua'); return
    try:
        outdir = os.path.join(WWW, 'fonts'); os.makedirs(outdir, exist_ok=True)
        css, n = build(get(CSS_URL).decode('utf8'), get, outdir)
        if not n:
            raise RuntimeError('không có phông nào')
        html = html.replace(MARK, '<style>\n' + css + '\n</style>')
        open(idx, 'w', encoding='utf8').write(html)
        print(f'fonts: đã gói {n} file phông')
    except Exception as e:  # mạng lỗi: dùng phông của máy
        print('::warning::Không tải được phông chữ, app dùng phông của máy:', e)


if __name__ == '__main__':
    main()
