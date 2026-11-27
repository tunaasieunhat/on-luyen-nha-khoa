/* @@DLS-JS: slide Da Liễu vẽ bằng HTML (bản dựng lại) */
var DLS_DECKS = __DLS_DATA__;
var DLS_BASE = 'slides/da-lieu/fig/';
var dlsAvs = null;
const dlsB = s => avsEsc(s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');
function dlsSlide(S, i, print) {
  const s = S[i], cls = `avs dl k-${s.k === 'c' ? 'c' : s.k}${print ? ' print' : ''}${s.fig ? ' has-fig' : ''}`, B = `<b>Bài ${s.b}</b>`;
  const items = it => it && it.length ? `<ul class="dl-ul">${it.map(([t, l]) => `<li class="l${l}">${dlsB(t)}</li>`).join('')}</ul>` : '';
  const table = r => r && r.length ? `<div class="dl-tw"><table class="dl-t"><thead><tr>${r[0].map(c => `<th>${dlsB(c)}</th>`).join('')}</tr></thead><tbody>${r.slice(1).map(x => `<tr>${x.map(c => `<td>${dlsB(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>` : '';
  const note = n => n ? `<div class="box dl-n ${n.kind}"><span class="lbl">${avsEsc(n.lab)}</span>${dlsB(n.t)}</div>` : '';
  const fig = f => f ? `<figure class="dl-f"><img src="${DLS_BASE}${f.src}" width="${f.w}" height="${f.h}" alt="${avsEsc(f.cap)}" decoding="async"><figcaption>${avsEsc(f.cap)}</figcaption></figure>` : '';
  if (s.k === 'title') return `<div class="${cls}"><span class="course">Da Liễu · Ôn Luyện Nha Khoa</span>
    <div class="big-u">Bài ${s.b}<small>/11</small></div><h2>${avsEsc(s.t)}</h2>
    <div class="meta"><span>${s.n} slide</span><span>Khoảng ${s.mins} phút</span><span>${s.nq} câu trắc nghiệm</span></div></div>`;
  if (s.k === 'goal') return `<div class="${cls}"><div class="top">${B}<span>Mục tiêu</span></div><h2 class="h">Học xong bài này, bạn cần</h2><ol class="steps">${s.items.map(([t]) => `<li><span>${dlsB(t)}</span></li>`).join('')}</ol></div>`;
  if (s.k === 'c') {
    const txt = (s.tfirst ? table(s.rows) + items(s.items) : items(s.items) + table(s.rows)) + note(s.note);
    return `<div class="${cls}"><div class="top">${B}<span>${avsEsc(s.sec)}</span></div><h2 class="h">${avsEsc(s.h)}</h2>
    ${s.fig ? `<div class="two dl-two"><div class="col">${txt}</div><div class="col">${fig(s.fig)}</div></div>` : `<div class="col">${txt}</div>`}</div>`;
  }
  if (s.k === 'quiz' || s.k === 'ans') {
    const U = s.u; s.u = 0; let h = (dlsAvs || avsSlide)(S, i, print); s.u = U;
    return h.replace('class="avs ', 'class="avs dl ').replace('<b>Unit 0</b>', B);
  }
  if (s.k === 'recap') return `<div class="${cls}"><div class="top">${B}<span>Tổng kết</span></div><h2 class="h">Ghi nhớ cả bài</h2><div class="box teal">${items(s.items)}</div></div>`;
  if (s.k === 'end') return `<div class="${cls}"><div class="top">${B}<span>Hoàn thành</span></div><h2>Xong Bài ${s.b} rồi!</h2>
    <div class="two"><div class="box teal"><span class="lbl">Ôn cho nhớ lâu</span><ol class="steps"><li><span>Mở tab <b>Giáo trình</b> của bài này, đọc lại các khung Mẹo nhớ.</span></li><li><span>Ngày mai mở slide <b>Tổng kết</b>, che lại và tự nói các ý chính.</span></li><li><span>Làm lại các slide <b>Kiểm tra nhanh</b> sau 3 ngày.</span></li></ol></div>
    ${s.next ? `<div class="box"><span class="lbl">Bài tiếp theo</span><b>Bài ${s.b + 1} · ${avsEsc(s.next)}</b></div>` : '<div class="box"><span class="lbl">Chúc mừng</span>Bạn đã học hết 11 bài Da Liễu.</div>'}</div></div>`;
  return `<div class="${cls}"></div>`;
}
function dlsThumb(s) {
  const lab = s.k === 'c' ? s.h : s.k === 'quiz' ? s.title : ({ title: 'Mở đầu', goal: 'Mục tiêu', recap: 'Tổng kết', end: 'Hoàn thành' })[s.k] || '';
  return { c: s.k === 'quiz' ? 'q' : s.k === 'c' ? 'w' : '', html: `<i>${s.k === 'quiz' ? 'Trắc nghiệm' : s.k === 'c' ? (/^\d/.test(s.sec) ? 'Mục ' + s.sec.split(/[.\s–&]/)[0] : 'Slide') : 'Slide'}</i>${avsEsc(lab)}` };
}
/* @@DLS-JS-END */
