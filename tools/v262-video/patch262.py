# Version 2.6.2: video bài giảng Vật liệu nha khoa Bài 1–5 (chạy lại được nhiều lần)
# python3 -I patch262.py <file.html>
import os, re, sys, json
D = os.path.dirname(os.path.abspath(__file__))
P = sys.argv[1]
h = open(P, encoding='utf8').read()
VD = json.load(open(os.path.join(D, 'out', 'videos.json'), encoding='utf8'))


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


css = open(os.path.join(D, 'vd.css'), encoding='utf8').read().strip()
js = open(os.path.join(D, 'vd.js'), encoding='utf8').read().strip().replace(
    '__VD_DATA__', json.dumps(VD, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
h = put(h, '/* @@VD-CSS */', '/* @@VD-CSS-END */', '/* @@SL-CSS-END */', css, before=False)
h = put(h, '/* @@VD-JS: ', '/* @@VD-JS-END */', '/* @@SL-JS-END */', js, before=False)

TAB = ('<!-- @@VD-TAB --><button class="th-tab" type="button" role="tab" id="th-tab-vd" data-thtab="vd" aria-selected="false" aria-controls="th-vd" hidden>'
       '<svg class="i" viewBox="0 0 24 24"><rect x="2.5" y="5" width="14" height="14" rx="2.5"/><path d="M16.5 10l5-3v10l-5-3z"/></svg>'
       '<span>Video bài giảng</span><small id="th-tab-vd-n"></small><b class="th-new">Mới</b></button><!-- @@VD-TAB-END -->')
h = put(h, '<!-- @@VD-TAB -->', '<!-- @@VD-TAB-END -->', '<!-- @@SL-TAB-END -->', TAB, before=False)
PANEL = '''<!-- @@VD-PANEL -->
      <section class="th-vd" id="th-vd" role="tabpanel" aria-labelledby="th-tab-vd" hidden>
        <div class="sl-bar">
          <h3 class="sl-title" id="vd-title"></h3>
          <span class="sl-count" id="vd-meta"></span>
        </div>
        <div class="vd-resume" id="vd-resume" hidden>
          <p>Bạn đang xem dở ở phút <b id="vd-resume-t"></b>.</p>
          <button class="btn btn-sm btn-scrub" type="button" data-vdresume="1">Xem tiếp</button>
          <button class="btn btn-sm" type="button" data-vdresume="0">Xem từ đầu</button>
        </div>
        <div class="vd-wrap">
          <div>
            <div class="vd-stage"><video id="vd-video" controls playsinline preload="none" controlslist="nodownload"></video></div>
            <p class="vd-now" id="vd-now" aria-live="polite"></p>
            <div class="vd-tools">
              <div class="seg" id="vd-rate" role="group" aria-label="Tốc độ phát">
                <button class="chip" type="button" data-vdrate="0.75" aria-pressed="false">0.75×</button>
                <button class="chip" type="button" data-vdrate="1" aria-pressed="true">1×</button>
                <button class="chip" type="button" data-vdrate="1.25" aria-pressed="false">1.25×</button>
                <button class="chip" type="button" data-vdrate="1.5" aria-pressed="false">1.5×</button>
              </div>
              <button class="chip" type="button" id="vd-cc" aria-pressed="true">Phụ đề</button>
              <span class="spacer"></span>
              <a class="btn btn-sm" id="vd-dl" href="#" target="_blank" rel="noopener" download><svg class="i" viewBox="0 0 24 24"><path d="M12 4v11M7 10l5 5 5-5"/><path d="M5 20h14"/></svg>Tải video (MP4)</a>
            </div>
          </div>
          <div class="vd-ch" id="vd-ch" aria-label="Danh sách slide trong video"></div>
        </div>
        <p class="fine vd-tip">Video 480p, giọng giảng nữ đọc từng slide, có phụ đề tiếng Việt. Chạm một slide trong danh sách để nhảy tới đoạn đó; phím cách để dừng/phát, ← → để tua 10 giây. Video phát trực tuyến nên cần có mạng.</p>
      </section>
      <!-- @@VD-PANEL-END -->'''
h = put(h, '<!-- @@VD-PANEL -->', '<!-- @@VD-PANEL-END -->', '      <!-- @@SL-PANEL-END -->', PANEL.replace('<!-- @@VD-PANEL -->', '      <!-- @@VD-PANEL -->', 1).lstrip(), before=False)

# chuyển tab
h = once(h, "  if (tab === 'sl' && !slData(S.th.open)) tab = 'sum';\n",
         "  if (tab === 'sl' && !slData(S.th.open)) tab = 'sum';\n  if (tab === 'vd' && !vdData(S.th.open)) tab = 'sum';\n")
h = once(h, "  if (tab === 'sl') renderSL(); else if (SL.full) slSetFull(false);\n",
         "  if (tab === 'sl') renderSL(); else if (SL.full) slSetFull(false);\n  $('#th-vd').hidden = tab !== 'vd';\n  if (tab === 'vd') renderVD(); else vdPause();\n")
h = once(h, "  slReader(l);\n  mmSetTab(S.th.tab || 'sum');", "  slReader(l);\n  vdReader(l);\n  mmSetTab(S.th.tab || 'sum');")
h = once(h, "function closeLesson() {\n  if (MM.full) mmSetFull(false);", "function closeLesson() {\n  vdPause();\n  if (MM.full) mmSetFull(false);")
# bấm
h = once(h, "    if (t.dataset.sldl) { slDownload(t.dataset.sldl); return; }\n",
         "    if (t.dataset.sldl) { slDownload(t.dataset.sldl); return; }\n"
         "    if (t.dataset.thvd) { S.th.tab = 'vd'; openLesson(t.dataset.thvd); return; }\n"
         "    if (t.dataset.vdto) { const v = vdData(VD.id); if (v) vdSeek(v.ch[Number(t.dataset.vdto)][0], true); return; }\n"
         "    if (t.dataset.vdrate) { vdRate(t.dataset.vdrate); return; }\n"
         "    if (t.id === 'vd-cc') { vdCC(true); return; }\n"
         "    if (t.dataset.vdresume) { vdSeek(t.dataset.vdresume === '1' ? Number(vdStore('pos:' + VD.id)) || 0 : 0, true); return; }\n")
h = once(h, "      ${slData(l.id) ? `<button class=\"btn btn-sm\" type=\"button\" data-thsl=\"${esc(l.id)}\">${SL_ICON}Slide bài giảng</button>` : ''}\n",
         "      ${vdData(l.id) ? `<button class=\"btn btn-sm btn-scrub\" type=\"button\" data-thvd=\"${esc(l.id)}\">${VD_ICON}Video bài giảng</button>` : ''}\n"
         "      ${slData(l.id) ? `<button class=\"btn btn-sm\" type=\"button\" data-thsl=\"${esc(l.id)}\">${SL_ICON}Slide bài giảng</button>` : ''}\n")

# phiên bản 2.6.2
NOTE = 'Bản cập nhật 2.6.2: Video bài giảng Vật liệu nha khoa Bài 1–5, giọng giảng nữ và phụ đề tiếng Việt.'
h = re.sub(r'(<span class="beta-txt">)Bản cập nhật 2\.6\.1:[^<]*(</span>)', lambda x: x.group(1) + NOTE + x.group(2), h)
LI = '''    <ul class="v1-new">
      <li><b>Video bài giảng Vật liệu nha khoa Bài 1–5:</b> mỗi bài hơn 20 phút, 480p, giọng giảng nữ đọc từng slide, có <b>phụ đề tiếng Việt</b> (bật/tắt được).</li>
      <li>Danh sách slide bên cạnh video: chạm để <b>nhảy tới slide</b> cần xem; app nhớ chỗ bạn đang xem dở để <b>xem tiếp</b>.</li>
      <li>Chỉnh tốc độ 0.75× đến 1.5×, tải video MP4 về máy. Mở ở nút <b>Video bài giảng</b> trong danh sách bài hoặc tab mới trong trang bài.</li>
'''
i = h.index('    <ul class="v1-new">'); j = h.index('    </ul>', i)
h = h[:i] + LI + h[j:]
h = h.replace('2.6.1', '2.6.2')
open(P, 'w', encoding='utf8').write(h)
print('ok', P, len(h.encode('utf8')), 'bytes')
