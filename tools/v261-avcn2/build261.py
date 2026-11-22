# Version 2.6.1: biên soạn lại AVCN2 cho người mất gốc
#   w1–w3.txt (177 thẻ từ) + glossary.json + bài 2.4 cũ (Từ dễ nhầm, Đọc hiểu, Keyword)
#   -> out/lessons.json (U0, Gốc từ, U1–U15), out/vt.json (dữ liệu Luyện từ 5 bậc), out/print/*.html (bản in)
# python3 -I build261.py
import os, re, json, html, math, importlib.util
D = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('parse', os.path.join(D, 'parse.py')); P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
UNITS, W = P.load(); assert not P.check(UNITS, W)
T = json.load(open(os.path.join(D, 'theory-data.json'), encoding='utf8'))
OLD = T['lessons']
OUT = os.path.join(D, 'out'); os.makedirs(os.path.join(OUT, 'print'), exist_ok=True)
E = lambda s: html.escape(str(s), quote=False)
EA = lambda s: html.escape(str(s), quote=True)
TITLES = {1: 'The dentist – Nha sĩ và nghề nha', 2: 'Dental specialties – Các chuyên khoa', 3: 'The dental office – Khu vực phòng khám',
          4: 'Dental staff – Nhân sự phòng khám', 5: 'Dental instruments – Dụng cụ nha khoa', 6: 'The mouth – Khoang miệng',
          7: 'Tooth anatomy – Cấu tạo răng', 8: 'Types of teeth – Các loại răng', 9: 'Infection control – Kiểm soát lây nhiễm',
          10: 'Dental technology – Công nghệ nha khoa', 11: 'Appointments – Lịch hẹn', 12: 'Payment and insurance – Thanh toán, bảo hiểm',
          13: 'Patient communication – Giao tiếp bệnh nhân', 14: 'Oral hygiene – Vệ sinh răng miệng', 15: 'Teeth cleaning – Làm sạch răng'}
POS = {'N-COUNT': 'danh từ đếm được', 'N-UNCOUNT': 'danh từ không đếm được', 'V-T': 'động từ (có tân ngữ)', 'V-I': 'động từ (không cần tân ngữ)',
       'ADJ': 'tính từ', 'ADV': 'trạng từ'}
PAT = {1: ('A/An ___ is someone…', 'từ chỉ NGƯỜI'), 2: ('A/An/The ___ is a/an…', 'từ chỉ VẬT, NƠI, BỘ PHẬN'),
       3: ('___ is/are… (không có a/an)', 'danh từ KHÔNG ĐẾM ĐƯỢC hoặc số nhiều'), 4: ('To ___ is to… / If something ___s…', 'ĐỘNG TỪ'),
       5: ('If something is ___…', 'TÍNH TỪ (miêu tả)')}


def pattern(en):
    if re.match(r'^(A|An|The)\s[^.]{0,60}?\bis someone\b', en): return 1
    if re.match(r'^To\s', en) or re.match(r'^If something (?!is\b|happens\b)\w+', en): return 4
    if re.match(r'^If something (is|happens)\b', en): return 5
    if re.match(r'^(A|An|The)\s', en): return 2
    return 3


def term_pat(term):
    ws = term.split()
    return r'(?<![A-Za-z])' + r'\s+'.join(re.escape(w) + r'(?:s|es|d|ed|ing)?' for w in ws) + r'(?![A-Za-z-])'


def stem_def(w):
    sents = re.split(r'(?<=[.!?])\s+(?=[A-Z])', w['en'])
    out = sents[0]
    for s in sents[1:]:
        if len(out) + len(s) + 1 > 190: break
        out += ' ' + s
    m = re.sub(term_pat(w['t']), '_____', out, flags=re.I)
    m = re.sub(r'\b(A|a)n? _____', lambda x: x.group(1) + '/' + ('An' if x.group(1) == 'A' else 'an') + ' _____', m)
    return m


def blank_ex(w):
    return re.sub(r'(?<![A-Za-z])' + re.escape(w['t']) + r'(?![A-Za-z])', '_____', w['ex'], count=1, flags=re.I)


SAY_SVG = '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9z"/><path d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12"/></svg>'


def say_btn(t, cls='vw-say'):
    return f'<button class="{cls}" type="button" data-say="{EA(t)}" aria-label="Nghe đọc {EA(t)}">{SAY_SVG}</button>'


def hl(text, term):
    s = E(text)
    return re.sub(r'(?<![A-Za-z])(' + re.escape(E(term)) + r')(?![A-Za-z])', r'<b>\1</b>', s, count=1, flags=re.I)


def card(w):
    p = pattern(w['en'])
    joined = P.norm(' '.join(c[0] for c in w['ch'])); rest = ''
    if P.norm(w['en']) != joined:
        # phần định nghĩa còn lại (câu thứ hai…) giữ nguyên tiếng Anh
        words_en = w['en'].split(); acc = ''
        for i in range(len(words_en) + 1):
            if P.norm(' '.join(words_en[:i])) == joined: rest = ' '.join(words_en[i:]); break
    chips = ''.join(f'<span class="ck"><i>{E(a)}</i><small>{E(b)}</small></span>' for a, b in w['ch'])
    if rest: chips += f'<span class="ck more"><i>{E(rest)}</i><small>(phần sau, đọc thêm)</small></span>'
    return (f'<div class="vw" id="vw-{re.sub(r"[^a-z0-9]+", "-", w["t"].lower())}">'
            f'<div class="vw-h">{say_btn(w["t"])}<div class="vw-hw"><b class="vw-t">{E(w["t"])}</b> <span class="vw-ipa">{E(w["ipa"])}</span>'
            f'<span class="vw-s">Đọc gần giống: <b>{E(w["say"])}</b></span></div></div>'
            f'<p class="vw-m">{E(w["m"])}<span class="vw-pos">{E(POS.get(w["pos"], w["pos"]))}</span></p>'
            f'<p class="vw-hook"><strong>Nhớ nhanh:</strong> {E(w["hook"])}</p>'
            f'<p class="vw-ex"><strong>Ví dụ:</strong> <span lang="en">{hl(w["ex"], w["t"])}</span> {say_btn(w["ex"], "vw-say sm")}<br><span class="vw-exv">→ {E(w["exv"])}</span></p>'
            f'<div class="vw-def"><div class="vw-dl"><strong>Câu định nghĩa trong đề</strong> · Mẫu {p}: {E(PAT[p][0])} → {E(PAT[p][1])}</div><div class="vw-ck" lang="en">{chips}</div></div>'
            f'<p class="vw-kw">Trong đề thấy <b>{E(w["kw"])}</b> → chọn <b class="vw-ans">{E(w["t"])}</b></p></div>')


def tbl(head, rows, cls=None):
    c = cls or f'c{len(head)}'
    return (f'<div class="tbl"><table class="{c}"><thead><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<td>{x}</td>' for x in r) + '</tr>' for r in rows) + '</tbody></table></div>')


def note(kind, label, body):
    return f'<div class="th-note {kind}"><p><strong>{label}</strong> {body}</p></div>'


def old_sections(u):
    """Lấy lại các mục cuối của bài 2.4: Giới từ chỉ thời gian (U11), Từ dễ nhầm, Đọc hiểu tình huống, Keyword làm trắc nghiệm."""
    h = OLD[f'avcn2-u{u}']['html']
    parts = re.split(r'(<h3 id="[^"]+">.*?</h3>)', h)
    out = []
    for i in range(1, len(parts), 2):
        title = re.sub(r'<[^>]+>', '', parts[i]); t = re.sub(r'^\d+\.\s*', '', html.unescape(title))
        if any(k in t for k in ('Giới từ', 'Từ dễ nhầm', 'Đọc hiểu', 'Keyword')):
            out.append((t, parts[i + 1]))
    assert any('Từ dễ nhầm' in t for t, _ in out) and any('Keyword' in t for t, _ in out), u
    return out


class Doc:
    def __init__(self, key): self.key, self.toc, self.html = key, [], []
    def h3(self, t):
        k = len(self.toc) + 1; hid = f'th-{self.key}-{k}'; t = f'{k}. {t}'
        self.toc.append({'id': hid, 't': t}); self.html.append(f'<h3 id="{hid}">{E(t)}</h3>')
    def add(self, s): self.html.append(s)
    def text(self): return ''.join(self.html)


def words_count(h):
    return len(re.findall(r'\w+', re.sub(r'<[^>]+>', ' ', h)))


VT_BTN = lambda u, label: f'<p class="vt-go"><button class="btn btn-sm btn-scrub" type="button" data-vt="{u}">{label}</button></p><div class="vt-prog" data-vtu="{u}"></div>'

lessons = {}
# ---------- U1–U15 ----------
for u in range(1, 16):
    d = Doc(f'u{u}'); ws = [W[t] for t in UNITS[u]['order']]
    d.add(note('goal', 'Unit này học gì:', E(UNITS[u]['intro'])))
    d.add(note('tip', f'Cách học {len(ws)} từ trong 15 phút:', '① Bấm nút loa để nghe từng từ và đọc theo 2–3 lần. ② Nhớ <b>nghĩa ngắn</b> và câu <b>Nhớ nhanh</b>. '
               '③ Đọc câu định nghĩa theo từng cụm, mỗi cụm có nghĩa tiếng Việt ngay bên dưới. ④ Bấm <b>Luyện từ 5 bậc</b> ở cuối bài để tập từ dễ đến khó.'))
    d.h3('Bảng từ nhanh')
    d.add(tbl(['Từ', 'Đọc gần giống', 'Nghĩa'], [[f'<strong>{E(w["t"])}</strong>', E(w['say']), E(w['m'])] for w in ws], 'c3 vw-tb'))
    d.add('<p class="vt-go"><button class="btn btn-sm" type="button" data-thpdf="avcn2-bangtu">Tải bảng từ tóm tắt để in (15 Unit, mỗi Unit 1 trang)</button></p>')
    d.add(note('key', 'Đọc gần giống:', 'chữ IN HOA là âm đọc mạnh (trọng âm). Cách đọc bằng chữ Việt chỉ gần đúng, hãy bấm loa nghe giọng chuẩn rồi đọc theo.'))
    d.h3('Học từng từ')
    for w in ws: d.add(card(w))
    for t, body in old_sections(u):
        d.h3(t); d.add(body)
    d.h3('Luyện tập')
    d.add('<p>Luyện từ 5 bậc đi từ dễ đến khó: <b>nghe và chọn nghĩa</b> → <b>nghĩa Việt ra từ</b> → <b>keyword ra từ</b> → <b>định nghĩa ra từ (giống đề thi)</b> → <b>điền từ vào câu</b>. '
          'Trả lời đúng thì từ lên bậc, sai thì xuống một bậc và sẽ được hỏi lại. Từ nào qua đủ 5 bậc là đã thuộc.</p>')
    d.add(VT_BTN(u, f'Luyện từ 5 bậc · Unit {u}'))
    d.add('<p>Sau đó làm câu hỏi của Unit này trong <b>Câu hỏi hệ thống</b> (môn AVCN2) để quen dạng đề.</p>')
    h = d.text()
    lessons[f'avcn2-u{u}'] = {'pages': '', 'note': f'{len(ws)} từ vựng', 'srcline': f'{len(ws)} từ vựng · có loa đọc, nghĩa ngắn, mẹo nhớ, định nghĩa dịch từng cụm',
                             'pdf': f'pdf/{OLD[f"avcn2-u{u}"]["file"]}', 'file': OLD[f'avcn2-u{u}']['file'], 'cta': 'Học từ vựng',
                             'mins': max(1, math.ceil(words_count(h) / 200)), 'toc': d.toc, 'html': h}

# ---------- U0: Bắt đầu từ đây ----------
cnt = {k: 0 for k in PAT}; ex_pat = {k: [] for k in PAT}
for w in W.values():
    p = pattern(w['en']); cnt[p] += 1
    if len(ex_pat[p]) < 3: ex_pat[p].append(w)
d = Doc('u0')
d.add(note('goal', 'Bài này dành cho bạn nếu:', 'bạn thấy tiếng Anh khó, đọc định nghĩa không hiểu, hoặc không biết bắt đầu học môn này từ đâu. Đọc bài này trước (khoảng 10 phút), rồi học U1–U15 theo lộ trình ở mục 6.'))
d.h3('Môn này thi gì?')
d.add(f'<p>Môn Anh văn chuyên ngành 2 có <b>{len(W)} từ</b> chia trong <b>15 Unit</b>, mỗi Unit 10–14 từ. Mỗi từ có một câu <b>định nghĩa tiếng Anh</b> trong Glossary. '
      'Đề trắc nghiệm thường lấy câu định nghĩa đó, đục một chỗ trống, rồi cho 4 từ để chọn. Ví dụ:</p>')
d.add('<div class="th-note why"><p lang="en"><i>“A _____ is someone whose job it is to care for the health of people\'s teeth.”</i><br>A. dentistry &nbsp; B. dentist &nbsp; C. oral &nbsp; D. advice</p>'
      '<p>Không cần hiểu hết câu. Chỉ cần thấy <b>“someone whose job”</b> (một người mà công việc là…) là biết đáp án chỉ người: <b>dentist</b>.</p></div>')
d.add(note('tip', 'Tin vui:', 'bạn không cần giỏi ngữ pháp. Môn này chủ yếu là <b>nhớ từ</b> và <b>nhận ra vài cụm từ khóa</b> trong câu định nghĩa. Bài này chỉ cho bạn cách làm điều đó.'))
d.h3('Đọc phiên âm (IPA) cho người mới')
d.add('<p>Mỗi từ có phiên âm trong dấu / / và một dòng <b>Đọc gần giống</b> bằng chữ Việt. Dấu <b>ˈ</b> đứng trước âm đọc mạnh; trong dòng Đọc gần giống, âm mạnh viết IN HOA. '
      'Bảng dưới là những ký hiệu hay gặp mà tiếng Việt không có:</p>')
IPA = [('θ', 'đặt đầu lưỡi giữa hai răng rồi thổi hơi, gần như “th” nhẹ', 'health, teeth'), ('ʃ', 'gần “s” uốn lưỡi (như “sh”)', 'polish, cash'),
       ('tʃ', 'gần “ch” bật hơi', 'chew, chisel'), ('dʒ', 'gần “ch” nhưng rung, như “j” trong job', 'surgery, syringe'),
       ('ŋ', 'như “ng” cuối từ', 'tongue, evening'), ('ə', 'âm “ơ” rất nhẹ, lướt qua', 'advice, oral'),
       ('ɪ / iː', '“i” ngắn / “i” kéo dài', 'dentist / teeth'), ('æ', 'giữa “a” và “e”, mở miệng rộng', 'lab, cash'),
       ('ʌ', 'gần “ă”', 'cut, gums'), ('ɜː', 'gần “ơ” kéo dài', 'nerve, surgery'), ('s, z ở cuối từ', 'nhớ đọc âm cuối, đừng nuốt', 'gums, forceps')]
d.add(tbl(['Ký hiệu', 'Đọc gần như', 'Ví dụ trong môn'], [[f'<b>{E(a)}</b>', E(b), f'<span lang="en">{E(c)}</span>'] for a, b, c in IPA]))
d.add(note('key', 'Mẹo:', 'bấm nút loa cạnh mỗi từ để nghe giọng đọc chuẩn. Đọc to theo 2–3 lần giúp nhớ lâu hơn nhiều so với chỉ nhìn.'))
d.h3('Hiểu nhãn loại từ')
d.add('<p>Glossary ghi loại từ bằng chữ viết tắt. Bạn chỉ cần biết 6 nhãn sau:</p>')
d.add(tbl(['Nhãn', 'Nghĩa', 'Ví dụ'], [['<b>N-COUNT</b>', 'danh từ <b>đếm được</b>: có “a/an” phía trước, có số nhiều', 'a dentist, two molars'],
                                        ['<b>N-UNCOUNT</b>', 'danh từ <b>không đếm được</b>: không có “a/an”', 'advice, health, saliva'],
                                        ['<b>V-T</b>', 'động từ <b>có tân ngữ</b> (làm gì <i>cái gì</i>)', 'cancel <i>an appointment</i>'],
                                        ['<b>V-I</b>', 'động từ <b>không cần tân ngữ</b>', 'listen, chew'],
                                        ['<b>ADJ</b>', '<b>tính từ</b>: miêu tả tính chất', 'oral, disposable'],
                                        ['<b>ADV</b>', '<b>trạng từ</b>: miêu tả cách, lúc xảy ra', 'daily']]))
d.h3('5 mẫu câu định nghĩa: chìa khóa của cả môn')
d.add(f'<p>Đọc kỹ thì cả {len(W)} câu định nghĩa chỉ dùng <b>5 mẫu câu</b>. Nhìn mấy chữ đầu câu là biết từ cần chọn thuộc loại nào, rồi loại ngay những đáp án sai loại.</p>')
d.add(tbl(['Mẫu', 'Câu bắt đầu bằng', 'Đáp án là', 'Số từ', 'Ví dụ'],
          [[f'<b>{k}</b>', f'<span lang="en">{E(PAT[k][0])}</span>', E(PAT[k][1]), str(cnt[k]), ', '.join(E(w['t']) for w in ex_pat[k])] for k in PAT], 'c5'))
d.add(note('why', 'Ví dụ:', '<span lang="en"><i>“To _____ is to find out what health issues someone has…”</i></span> bắt đầu bằng <b>To ___ is to</b> nên đáp án phải là <b>động từ</b>. '
           'Trong 4 đáp án dentist, diagnose, oral, health chỉ có <b>diagnose</b> là động từ.'))
d.add('<p>Những cụm hay gặp trong định nghĩa, biết nghĩa là đọc được phần lớn câu:</p>')
CHUNK = [('someone whose job it is to…', 'người mà công việc là…'), ('a tool for… / used to…', 'dụng cụ để…'), ('a space in which…', 'không gian nơi…'),
         ('a branch of dentistry which deals with…', 'nhánh nha khoa chuyên về…'), ('the part of… that…', 'phần của… mà…'),
         ('is made of / is made from…', 'được làm từ…'), ('used for… / used to…', 'dùng để…'), ('in order to… / to…', 'để…'),
         ('such as…', 'chẳng hạn như…'), ('another word / another name for…', 'tên khác của…')]
d.add(tbl(['Cụm tiếng Anh', 'Nghĩa'], [[f'<span lang="en"><b>{E(a)}</b></span>', E(b)] for a, b in CHUNK]))
d.h3('Làm một câu trắc nghiệm trong 3 bước')
d.add('<ol><li><b>Nhìn đầu câu</b> để biết mẫu (người, vật, không đếm được, động từ hay tính từ).</li>'
      '<li><b>Loại đáp án sai loại</b>: hỏi động từ thì gạch danh từ, hỏi người thì gạch dụng cụ…</li>'
      '<li><b>Tìm keyword</b> (cụm in đậm ở cuối mỗi thẻ từ) và chọn từ khớp.</li></ol>')
d.h3('Lộ trình 15 ngày')
d.add('<p>Mỗi ngày khoảng <b>15–20 phút</b>: học Unit mới, rồi vào <b>Luyện từ 5 bậc</b> để ôn cả từ cũ (app tự đưa lại từ sắp quên).</p>')
plan = []
for day in range(1, 16):
    new = f'U{day}' + (' (đọc U0 trước)' if day == 1 else '') + (', đọc bài Gốc từ' if day == 3 else '')
    rev = '—' if day == 1 else ('ôn U1–U' + str(day - 1) if day > 2 else 'ôn U1')
    extra = 'làm Câu hỏi hệ thống U' + str(day) + (' + đề thử 30 câu trong Phòng Thi' if day in (5, 10, 15) else '')
    plan.append([f'<b>Ngày {day}</b>', new, rev, extra])
d.add(tbl(['Ngày', 'Học mới', 'Luyện từ 5 bậc', 'Làm bài'], plan, 'c4'))
d.h3('Luyện từ 5 bậc là gì?')
d.add(tbl(['Bậc', 'Dạng câu hỏi', 'Mục đích'], [['1', 'Nghe từ (có chữ) → chọn nghĩa tiếng Việt', 'làm quen mặt chữ và cách đọc'],
                                              ['2', 'Nghĩa tiếng Việt → chọn từ tiếng Anh', 'nhớ ra từ khi biết nghĩa'],
                                              ['3', 'Keyword → chọn từ', 'nhận ra cụm từ khóa'],
                                              ['4', 'Câu định nghĩa có chỗ trống → chọn từ', 'giống hệt đề thi'],
                                              ['5', 'Câu ví dụ có chỗ trống → điền từ', 'dùng được từ trong câu']]))
d.add('<p>Đúng thì từ lên một bậc và được hẹn ôn lại sau vài ngày; sai thì xuống một bậc và hỏi lại ngay trong buổi. Từ qua đủ 5 bậc được tính là <b>đã thuộc</b>.</p>')
d.add(VT_BTN(0, 'Luyện từ 5 bậc · tất cả Unit'))
d.add('<p class="vt-go"><button class="btn btn-sm" type="button" data-thpdf="avcn2-bangtu">Tải bảng từ tóm tắt để in (15 Unit, mỗi Unit 1 trang)</button></p>')
h = d.text()
lessons['avcn2-u0'] = {'pages': '', 'note': 'bắt đầu từ đây', 'srcline': 'Dành cho người mất gốc: cách học, đọc phiên âm, 5 mẫu câu định nghĩa, lộ trình 15 ngày',
                       'pdf': 'pdf/AVCN2-U00-Bat-dau-tu-day.pdf', 'file': 'AVCN2-U00-Bat-dau-tu-day.pdf', 'cta': 'Đọc trước',
                       'mins': max(1, math.ceil(words_count(h) / 200)), 'toc': d.toc, 'html': h}

# ---------- Gốc từ ----------
ROOTS = [
    ('Răng và miệng', [('dent- / odont-', 'răng', ['dentist', 'dentistry', 'dentin', 'endodontics', 'orthodontics', 'periodontics']),
                       ('or- / oral', 'miệng', ['oral', 'oral cavity', 'intraoral camera']),
                       ('maxill-', 'xương hàm trên', ['maxillofacial']), ('palat- / gloss-', 'khẩu cái / lưỡi', ['hard palate', 'palatoglossal arch'])]),
    ('Đầu từ (tiền tố)', [('endo- / intra-', 'bên trong', ['endodontics', 'intraoral camera']), ('peri-', 'xung quanh', ['periodontics', 'periodontal ligament']),
                          ('ortho-', 'thẳng', ['orthodontics']), ('prosth-', 'thay thế, gắn thêm', ['prosthodontics']),
                          ('pedi-', 'trẻ em', ['pediatric dentistry']), ('pre- / pro-', 'trước', ['premolar', 'prophylaxis']),
                          ('re-', 'lại, lần nữa', ['reschedule', 'reusable', 'reassurance']), ('non-', 'không', ['nonverbal']),
                          ('co-', 'cùng', ['co-payment']), ('inter-', 'ở giữa', ['interrupt']), ('sym-', 'cùng', ['sympathize'])]),
    ('Đuôi từ chỉ người, dụng cụ', [('-ist', 'người làm nghề', ['dentist', 'receptionist', 'dental hygienist', 'dental therapist']),
                                   ('-ician', 'người làm kỹ thuật', ['lab technician']),
                                   ('-er / -or', 'người hoặc dụng cụ làm việc gì', ['office manager', 'financial coordinator', 'burnisher', 'plugger', 'retractor', 'elevator', 'excavator'])]),
    ('Đuôi từ chỉ ngành, việc, vật', [('-ology', 'môn học về…', ['pathology', 'radiology']), ('-ics', 'ngành', ['endodontics', 'orthodontics']),
                                      ('-ry', 'ngành, lĩnh vực', ['dentistry']), ('-ion / -tion', 'việc, sự…', ['instruction', 'communication', 'authorization']),
                                      ('-ment', 'việc, sự…', ['appointment', 'payment']), ('-ance', 'sự…', ['insurance', 'reassurance']),
                                      ('-ant', 'thứ gây ra…', ['contaminant'])]),
    ('Đuôi từ chỉ tính chất', [('-al', 'thuộc về…', ['oral', 'professional', 'verbal', 'maxillofacial']), ('-able', 'có thể…', ['disposable', 'reusable']),
                               ('-ious', 'có tính…', ['infectious']), ('-ly', 'mỗi…, một cách…', ['daily'])]),
    ('Từ ghép dễ đoán', [('tooth- / mouth-', 'răng / miệng + đồ dùng', ['toothbrush', 'toothpaste', 'mouthwash']),
                         ('hard- / soft-', 'cứng / mềm', ['hardware', 'software', 'hard palate', 'soft palate']),
                         ('… room', 'phòng…', ['waiting room', 'treatment room', 'recovery room', 'storage room']),
                         ('front / back', 'phía trước / phía sau', ['front office', 'back office'])]),
]
d = Doc('ug')
d.add(note('goal', 'Vì sao học gốc từ:', 'nhiều từ y khoa ghép từ vài mảnh nhỏ. Biết nghĩa từng mảnh thì gặp từ lạ vẫn đoán được, và nhớ từ lâu hơn vì có lý do. Bài này gom các mảnh xuất hiện trong 177 từ của môn.'))
for grp, rows in ROOTS:
    d.h3(grp)
    for _, _, exs in rows:
        for x in exs: assert x in W, ('gốc từ: không có từ', x)
    d.add(tbl(['Mảnh từ', 'Nghĩa', 'Từ trong môn'], [[f'<b>{E(a)}</b>', E(b), ', '.join(f'<span lang="en">{E(x)}</span> <small>({E(W[x]["m"])})</small>' for x in exs)] for a, b, exs in rows]))
d.h3('Thử đoán nghĩa')
d.add('<ol><li><b>periodontal ligament</b>: peri (quanh) + odont (răng) + ligament (dây chằng) → dây chằng quanh răng.</li>'
      '<li><b>reusable</b>: re (lại) + use (dùng) + able (có thể) → dùng lại được.</li>'
      '<li><b>intraoral camera</b>: intra (trong) + oral (miệng) + camera → camera trong miệng.</li>'
      '<li><b>nonverbal</b>: non (không) + verbal (bằng lời) → không bằng lời.</li></ol>')
d.add(note('tip', 'Mẹo:', 'khi học thẻ từ ở mỗi Unit, dòng <b>Nhớ nhanh</b> đã tách sẵn mảnh từ cho bạn. Bài này giúp nhìn lại tất cả một lần.'))
h = d.text()
lessons['avcn2-ugoc'] = {'pages': '', 'note': 'đoán nghĩa từ lạ', 'srcline': 'Các mảnh từ (đầu từ, đuôi từ) trong 177 từ của môn',
                         'pdf': 'pdf/AVCN2-Goc-tu.pdf', 'file': 'AVCN2-Goc-tu.pdf', 'cta': 'Đọc bài',
                         'mins': max(1, math.ceil(words_count(h) / 200)), 'toc': d.toc, 'html': h}

ORDER = ['avcn2-u0', 'avcn2-ugoc'] + [f'avcn2-u{u}' for u in range(1, 16)]
json.dump({'order': ORDER, 'lessons': lessons}, open(os.path.join(OUT, 'lessons.json'), 'w', encoding='utf8'), ensure_ascii=False)

# ---------- dữ liệu Luyện từ 5 bậc ----------
vt = []
for u in range(1, 16):
    for t in UNITS[u]['order']:
        w = W[t]
        vt.append({'t': t, 'u': u, 'ipa': w['ipa'], 'm': w['m'], 'kw': w['kw'], 'd': stem_def(w), 'x': blank_ex(w), 'xv': w['exv'], 'p': pattern(w['en'])})
        assert '_____' in vt[-1]['x'] and '_____' in vt[-1]['d'], t
json.dump(vt, open(os.path.join(OUT, 'vt.json'), 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
print('bài:', {k: (len(v['toc']), v['mins']) for k, v in lessons.items()}); print('mẫu câu:', cnt, '| vt', len(vt))
