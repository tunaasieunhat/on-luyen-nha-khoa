# Bản dựng lại: xoá Mô Phỏng Nha Khoa (kèm lồng tiếng nhân vật), Sơ đồ tư duy, Video bài giảng; tạm khoá Flashcard.
# python3 -I patchrm.py <file.html>   (chạy sau patchdl.py; chạy lại nhiều lần vẫn ra cùng kết quả)
import sys, re, os
F = sys.argv[1]; s = open(F, encoding='utf8').read(); n0 = len(s)
def rep(old, new, need=True):
    global s
    if new and new in s: return
    if old in s: s = s.replace(old, new); return
    assert not need or new in s or new == '', ('không thấy', old[:90])
def cut(a, b):  # xoá khối từ chuỗi a tới hết chuỗi b
    global s
    i = s.find(a)
    if i < 0: return False
    j = s.find(b, i); assert j > i, b; s = s[:i] + s[j + len(b):]; return True
# ---------- HTML ----------
cut('<!-- @@V25-SIM -->', '<!-- @@V25-SIM-END -->')
cut('<!-- @@VD-TAB -->', '<!-- @@VD-TAB-END -->')
cut('<!-- @@VD-PANEL -->', '<!-- @@VD-PANEL-END -->')
cut('<button class="menu-btn sim" id="go-sim"', '</button>\n')
cut('<button class="th-tab" type="button" role="tab" id="th-tab-mm"', '</button>\n')
cut('<section class="th-mm" id="th-mm"', '</section>\n')
s = re.sub(r'<script type="application/json" id="mindmap-data">.*?</script>\n?', '', s, flags=re.S)
# ---------- CSS ----------
cut('/* @@VD-CSS */', '/* @@VD-CSS-END */')
cut('/* @@V255-CSS */', '/* @@V255-CSS-END */')
i = s.find('/* @@V25-CSS */')
if i >= 0:
    a = s.find('/* ---- Màn mô phỏng ---- */', i); b = s.find('/* @@V25-CSS-END */', i)
    if a > 0: assert a < b; s = s[:a] + s[b:]
# ---------- JS: khối tính năng -> phần thay thế nhỏ ----------
STUB = '''/* @@RB-JS: bản dựng lại – đã bỏ Mô Phỏng Nha Khoa, Sơ đồ tư duy, Video bài giảng; tạm khoá Flashcard */
const FLASH_LOCKED = true;
const MINDMAPS = {};
const MM = { full: false };
function mmSetFull() {}
function vdData() { return null; }
function vdPause() {}
function mmSetTab(tab) {
  if (tab === 'sl' && !slData(S.th.open)) tab = 'sum';
  if (tab !== 'sl') tab = 'sum';
  S.th.tab = tab;
  $('#th-sum').hidden = tab !== 'sum';
  $('#th-sl').hidden = tab !== 'sl';
  if (tab === 'sl') renderSL(); else if (SL.full) slSetFull(false);
  $$('#th-read [data-thtab]').forEach(b => b.setAttribute('aria-selected', String(b.dataset.thtab === tab)));
}
function mmReader(l) { slReader(l); mmSetTab(S.th.tab || 'sum'); }
/* Menu chính: Ôn Luyện Kiến Thức (chứa các chức năng) + Cài đặt */
function setLobbyView(v, focus) {
  S.lobbyView = v === 'learn' ? 'learn' : 'main';
  const m = $('#menu-main'), l = $('#menu-learn'); if (!m || !l) return;
  m.hidden = S.lobbyView === 'learn'; l.hidden = S.lobbyView !== 'learn';
  if (focus) setTimeout(() => { try { (S.lobbyView === 'learn' ? $('#go-quiz') : $('#go-learn')).focus({ preventScroll: true }); } catch {} }, 30);
}
document.addEventListener('click', e => {
  const t = e.target.closest && e.target.closest('button'); if (!t) return;
  if (t.id === 'go-learn') { setLobbyView('learn', true); return; }
  if (t.id === 'learn-back') { setLobbyView('main', true); return; }
});
/* @@RB-JS-END */'''
s = re.sub(r'/\* @@RB-JS:.*?@@RB-JS-END \*/\n?', '', s, flags=re.S)
for k in ['V25-JS', 'MM-JS', 'VD-JS', 'V255-VOICE']:
    cut('/* @@%s' % k, '/* @@%s-END */' % k)
assert s.count('/* @@SL-JS */') == 1; s = s.replace('/* @@SL-JS */', STUB + '\n/* @@SL-JS */', 1)
# ---------- chỗ gọi còn sót ----------
rep("const SCREENS = ['start', 'lobby', 'quiz', 'addq', 'flash', 'theory', 'exam', 'sim'];", "const SCREENS = ['start', 'lobby', 'quiz', 'addq', 'flash', 'theory', 'exam'];")
rep("  if (name !== 'start' && !S.player) name = 'start';\n", "  if (name !== 'start' && !S.player) name = 'start';\n  if (name === 'flash' && FLASH_LOCKED) name = 'lobby';\n")
rep("  if (name !== 'theory' && MM.full) mmSetFull(false);\n", '', False)
rep("  if (name !== 'sim') { try { Voice.stop(true); } catch {} }\n", '', False)
rep("  if (name === 'sim') renderSim();\n  if (name !== 'sim') document.body.classList.remove('sim-playing');\n", '', False)
rep("  vdPause();\n  if (MM.full) mmSetFull(false);\n  const id = S.th.open;", "  const id = S.th.open;", False)
for ln in ["    if (t.dataset.thmm) { S.th.tab = 'mm'; openLesson(t.dataset.thmm); return; }\n",
           "    if (t.dataset.thvd) { S.th.tab = 'vd'; openLesson(t.dataset.thvd); return; }\n",
           "    if (t.dataset.vdto) { const v = vdData(VD.id); if (v) vdSeek(v.ch[Number(t.dataset.vdto)][0], true); return; }\n",
           "    if (t.dataset.vdrate) { vdRate(t.dataset.vdrate); return; }\n",
           "    if (t.id === 'vd-cc') { vdCC(true); return; }\n",
           "    if (t.dataset.vdresume) { vdSeek(t.dataset.vdresume === '1' ? Number(vdStore('pos:' + VD.id)) || 0 : 0, true); return; }\n",
           "  if (t.dataset.setsw === 'voice') { Voice.setOn(!S.voice); if (S.voice) voiceSample(); setPaint(); return; }\n",
           "  if (e.target && e.target.id === 'set-voice') { const v = +e.target.value; $('#set-voice-v').textContent = v + '%'; Voice.setVol(v / 100); return; }\n"]:
    rep(ln, '', False)
rep(" if (e.target && e.target.id === 'set-voice') voiceSample();", '', False)
rep("${MINDMAPS[l.id] ? ' · có sơ đồ' : ''}", '', False)
s = re.sub(r"\n\s*\$\{MINDMAPS\[l\.id\] \? `<button[^\n]*?Sơ đồ tư duy</button>` : ''\}", '', s)
s = re.sub(r"\n\s*\$\{vdData\(l\.id\) \? `<button[^\n]*?Video bài giảng</button>` : ''\}", '', s)
s = re.sub(r'\n\s*<section class="set-sec">\s*<h3>\$\{VOICE_ICON\.on\}Lồng tiếng nhân vật</h3>.*?</section>', '', s, flags=re.S)
# ---------- chữ ----------
rep('<span class="d">Làm bài, Phòng Thi, lý thuyết, thêm câu hỏi, flashcard.</span>', '<span class="d">Làm bài, Phòng Thi, lý thuyết, thêm câu hỏi.</span>')
rep("        `Hôm nay thử làm bác sĩ không, <b>${esc(S.player.name)}</b>? Vào “Mô Phỏng Nha Khoa” nhận một ca bệnh nhé!`,\n", "        `Hôm nay ôn bài nào, <b>${esc(S.player.name)}</b>? Mở “Ôn tập lý thuyết” xem slide trước khi làm bài nhé!`,\n")
rep("`Đội ${esc(S.player.school)} cố lên! Ôn ${nC} thẻ ghi nhớ trước khi vào ghế cũng là một ý hay.`", "`Đội ${esc(S.player.school)} cố lên! Đọc lại tóm tắt lý thuyết trước khi vào ghế cũng là một ý hay.`")
rep("    `<span class=\"stat-chip\"><b>${nC}</b> thẻ ghi nhớ</span>`,\n", '', False)
rep("Ôn thêm vài thẻ là hoàn hảo.", "Ôn thêm chút lý thuyết là hoàn hảo.")
rep("Ghé mục Flashcard để ôn lại rồi thử tiếp nhé.", "Đọc lại tóm tắt lý thuyết rồi thử tiếp nhé.")
rep("Hãy ôn bộ thẻ ghi nhớ rồi quay lại ghế khám.", "Hãy ôn lại lý thuyết rồi quay lại ghế khám.")
rep("<small>Tự nhỏ đi một nửa khi vào Mô phỏng và khi trả lời câu hỏi</small>", "<small>Tự nhỏ đi một nửa khi trả lời câu hỏi</small>")
rep("<small>Ở sảnh, khi đọc lý thuyết, mô phỏng và khi làm bài</small>", "<small>Ở sảnh, khi đọc lý thuyết và khi làm bài</small>")
s = s.replace('ôn tập lý thuyết có tóm tắt PDF, flashcard và tự soạn câu hỏi', 'ôn tập lý thuyết có tóm tắt, slide, PDF và tự soạn câu hỏi')
rep('<small>Nhạc nền, lồng tiếng nhân vật, âm lượng, âm thanh</small>', '<small>Nhạc nền, âm lượng, âm thanh</small>')
# ---------- Flashcard: tạm khoá ----------
rep('<button class="menu-btn" id="go-flash" type="button">', '<button class="menu-btn locked" id="go-flash" type="button" aria-disabled="true">')
rep('<strong>Flashcard</strong><span class="d">Lật thẻ ôn nhanh, tự tạo thẻ.</span>', '<strong>Flashcard<span class="new lock">TẠM KHÓA</span></strong><span class="d">Đang được làm lại, sẽ mở sau.</span>')
rep("$('#go-flash').addEventListener('click', () => go('flash', 'Đang xếp bộ thẻ ghi nhớ'));", "$('#go-flash').addEventListener('click', () => { if (FLASH_LOCKED) { toast('Flashcard đang tạm khóa để làm lại. Bạn dùng Ôn tập lý thuyết và slide nhé.'); return; } go('flash', 'Đang xếp bộ thẻ ghi nhớ'); });")
css = '.menu-btn.locked{opacity:.55;filter:saturate(.4);cursor:not-allowed}.menu-btn.locked:hover{transform:none}.menu-btn .new.lock{background:var(--muted,#4F6D69);color:#fff}'
if css not in s: s = s.replace('/* @@AVS-CSS-END */', '/* @@AVS-CSS-END */\n' + css, 1)
# ---------- kiểm tra còn sót ----------
for bad in ['renderSim', 'SIM.', 'Voice.', 'voiceSample', 'VOICE_ICON', 'vdSeek', 'VD.id', 'MM_ICON', 'mmCount', 'id="scr-sim"', 'id="th-vd"', 'id="th-mm"']:
    m = re.search(r'(?<![\w$])' + re.escape(bad), s); assert not m, (bad, s[m.start() - 150:m.start() + 80])
if len(sys.argv) < 3: open(F, 'w', encoding='utf8').write(s)
print(os.path.basename(F), n0, '->', len(s))
