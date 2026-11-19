# Version 2.6.3: slide Anh văn chuyên ngành 2 (15 Unit) vẽ bằng HTML trong khung xem slide (chạy lại được nhiều lần)
# python3 -I patch263.py <file.html>
import os, re, sys, json
D = os.path.dirname(os.path.abspath(__file__))
P = sys.argv[1]
h = open(P, encoding='utf8').read()
DECKS = open(os.path.join(D, 'out', 'decks-app.json'), encoding='utf8').read()
files = [l.strip() for l in open(os.path.join(D, 'out', 'files.txt'), encoding='utf8') if l.strip()]
META = {f'avcn2-u{int(re.search(r"Unit-(\d+)", f).group(1))}': {'pptx': f, 'print': f[:-5] + '-BanIn.pdf'} for f in files}
assert len(META) == 15


def put(h, a, b, anchor, body, before=True):
    if a in h:
        i = h.index(a); j = h.index(b, i) + len(b)
        return h[:i] + body + h[j:]
    assert h.count(anchor) == 1, anchor[:80]
    return h.replace(anchor, body + '\n' + anchor if before else anchor + '\n' + body)


def once(h, old, new):
    if new in h: return h
    assert h.count(old) == 1, old[:100]
    return h.replace(old, new)


css = open(os.path.join(D, 'avs.css'), encoding='utf8').read().strip()
js = (open(os.path.join(D, 'avs.js'), encoding='utf8').read().strip()
      .replace('__AVS_DATA__', DECKS.replace('</', '<\\/'))
      .replace('__AVS_META__', json.dumps(META, ensure_ascii=False)))
h = put(h, '/* @@AVS-CSS:', '/* @@AVS-CSS-END */', '/* @@VD-CSS-END */', css, before=False)
h = put(h, '/* @@AVS-JS:', '/* @@AVS-JS-END */', '/* @@VD-JS-END */', js, before=False)

# khung xem slide: thêm vùng vẽ HTML, lời nhắc đổi theo loại slide
h = once(h, '          <img id="sl-img" alt="" decoding="async">\n', '          <img id="sl-img" alt="" decoding="async">\n          <div class="sl-html" id="sl-html"></div>\n')
h = once(h, '<p class="fine sl-tip">', '<p class="fine sl-tip" id="sl-tip">')
h = once(h, "  $('#sl-title').textContent = `${l.no}: ${l.title || ''}`;\n  if (SL.id !== l.id) { SL.id = l.id; SL.i = 0; }",
         "  $('#sl-title').textContent = `${l.no}: ${l.title || ''}`;\n  if (SL.id !== l.id) { SL.id = l.id; SL.i = 0; }\n"
         "  if (s) $('#sl-tip').textContent = s.deck ? 'Bấm nút loa để nghe đọc từ. Ở slide trắc nghiệm, chạm vào đáp án để biết đúng sai và xem giải thích. Vuốt ngang hoặc dùng phím ← → để chuyển slide. Bản PowerPoint và bản in có thêm slide đáp án.' : 'Vuốt ngang, chạm hai bên ảnh hoặc dùng phím ← → để chuyển slide. Bản PowerPoint có ghi chú người trình bày ở từng slide.';")
h = once(h, "    th.innerHTML = Array.from({ length: s.n }, (_, i) => `<button type=\"button\" data-slto=\"${i}\" aria-label=\"Slide ${i + 1}\"><img src=\"${slSrc(s, i)}\" alt=\"\" loading=\"lazy\" decoding=\"async\"><b>${i + 1}</b></button>`).join('');",
         "    th.innerHTML = s.deck ? AVS_DECKS[SL.id].map((x, i) => { const t = avsThumb(x, i); return `<button type=\"button\" class=\"tx ${t.c}\" data-slto=\"${i}\" aria-label=\"Slide ${i + 1}\">${t.html}<b>${i + 1}</b></button>`; }).join('')\n"
         "      : Array.from({ length: s.n }, (_, i) => `<button type=\"button\" data-slto=\"${i}\" aria-label=\"Slide ${i + 1}\"><img src=\"${slSrc(s, i)}\" alt=\"\" loading=\"lazy\" decoding=\"async\"><b>${i + 1}</b></button>`).join('');")
h = once(h, "  const img = $('#sl-img');\n  img.src = slSrc(s, SL.i);",
         "  const img = $('#sl-img');\n  $('#sl-stage').classList.toggle('html', !!s.deck);\n"
         "  if (s.deck) { const hb = $('#sl-html'); hb.innerHTML = avsSlide(AVS_DECKS[SL.id], SL.i); hb.setAttribute('aria-label', `Slide ${SL.i + 1} trên ${s.n}`); try { if (SL.full) $('#sl-stage').scrollTop = 0; } catch {} }\n"
         "  else img.src = slSrc(s, SL.i);")
h = once(h, "  if (SL.i + 1 < s.n) { const n = new Image(); n.src = slSrc(s, SL.i + 1); }", "  if (!s.deck && SL.i + 1 < s.n) { const n = new Image(); n.src = slSrc(s, SL.i + 1); }")
h = once(h, "url = `slides/vlnk/${file}`", "url = `${s.base || 'slides/vlnk'}/${file}`")

# Video bài giảng trên trang Claude: trang này chặn video tải từ trang khác -> hiện nút mở trang web
h = once(h, "    VD.built = VD.id; VD.remote = !!window.AndroidApp; VD.cur = -1; VD.cue = -1;",
         "    VD.built = VD.id; VD.remote = !!window.AndroidApp; VD.cur = -1; VD.cue = -1;\n"
         "    const vdBlocked = !window.AndroidApp && typeof window.claude === 'object' && window.claude && !/github\\.io$/.test(location.hostname);\n"
         "    $('#vd-blocked').hidden = !vdBlocked; $('#vd-stage').hidden = vdBlocked;")
h = once(h, '<div class="vd-stage"><video id="vd-video"',
         '<div class="vd-blocked box-note" id="vd-blocked" hidden><p>Trang này không phát được video. Mở bản web của app để xem video bài giảng, có đủ phụ đề và danh sách slide.</p>'
         '<a class="btn btn-sm btn-scrub" href="https://tunaasieunhat.github.io/on-luyen-nha-khoa/" target="_blank" rel="noopener">Mở trang web để xem video</a></div>\n'
         '            <div class="vd-stage" id="vd-stage"><video id="vd-video"')
h = once(h, '.vd-tip{margin:0}', '.vd-tip{margin:0}\n.vd-blocked{display:flex;flex-direction:column;gap:10px;align-items:flex-start;padding:16px;border:2px dashed var(--line);border-radius:16px;background:var(--enamel)}\n.vd-blocked[hidden]{display:none}.vd-blocked p{margin:0}')

# phiên bản 2.6.3
NOTE = 'Bản cập nhật 2.6.3: Slide Anh văn chuyên ngành 2 cho người mất gốc, đủ 15 Unit, có ví dụ và trắc nghiệm.'
h = re.sub(r'(<span class="beta-txt">)Bản cập nhật 2\.6\.2:[^<]*(</span>)', lambda x: x.group(1) + NOTE + x.group(2), h)
LI = '''    <ul class="v1-new">
      <li><b>Slide Anh văn chuyên ngành 2, đủ 15 Unit:</b> mỗi từ một slide gồm phát âm, nút loa, cách đọc gần giống, nghĩa, mẹo nhớ, <b>3 câu ví dụ</b> và câu định nghĩa giống đề thi.</li>
      <li><b>Trắc nghiệm ngay trên slide:</b> cứ 4 từ có một bài trắc nghiệm nhanh, cuối mỗi Unit có bài kiểm tra 8 câu. Chạm vào đáp án để biết đúng sai và xem giải thích.</li>
      <li>Tải được <b>PowerPoint</b> (chỉnh sửa được, có ghi chú) và <b>bản in 4 slide/trang</b> có thêm slide đáp án. Mở ở nút <b>Slide bài giảng</b> trong mỗi Unit.</li>
'''
i = h.index('    <ul class="v1-new">'); j = h.index('    </ul>', i)
h = h[:i] + LI + h[j:]
h = h.replace('2.6.2', '2.6.3')
open(P, 'w', encoding='utf8').write(h)
print('ok', P, len(h.encode('utf8')), 'bytes')
