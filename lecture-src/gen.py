# Video bài giảng Vật liệu nha khoa (Version 2.6.2): đọc lời giảng bằng VieNeu-TTS (Apache-2.0), giọng nữ "Mai Anh",
# kiểm tra bằng nhận dạng giọng nói (faster-whisper small). Mỗi slide ra một file b<bài>s<slide>.opus + vị trí từng câu.
# python lecture-src/gen.py <thư mục ra> <shard> <số shard>
import json, os, re, subprocess, sys, time, unicodedata
import numpy as np, soundfile as sf
D = os.path.dirname(os.path.abspath(__file__))
OUT, K, N = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
os.makedirs(OUT, exist_ok=True); TMP = os.path.join(OUT, '_tmp'); os.makedirs(TMP, exist_ok=True)
VOICE = os.environ.get('VOICE', 'Mai Anh')
L = json.load(open(os.path.join(D, 'lines.json'), encoding='utf8'))['lines']
OF = os.path.join(D, 'only.txt')  # đọc lại riêng vài slide, vd 3-15,3-16
if os.path.exists(OF):
    ONLY = set(filter(None, open(OF).read().replace('\n', ',').split(',')))
    L = [l for l in L if f"{l['b']}-{l['s']}" in ONLY]
# chia theo slide, cân bằng số ký tự
slides = []
for l in L:
    key = (l['b'], l['s'])
    if not slides or slides[-1][0] != key: slides.append([key, []])
    slides[-1][1].append(l)
tot = sum(len(l['say']) for l in L); acc = 0; mine = []
for key, ls in slides:
    c = sum(len(l['say']) for l in ls)
    if int((acc + c / 2) * N / tot) == K: mine.append((key, ls))
    acc += c
SR = 24000
from vieneu import Vieneu
tts = Vieneu()
TSR = getattr(tts, 'sample_rate', None) or 48000
from faster_whisper import WhisperModel
asr = WhisperModel('small', device='cpu', compute_type='int8')
log = open(os.path.join(OUT, f'log-{K}.txt'), 'a', encoding='utf8')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); log.write(s + '\n'); log.flush()


def words(s):
    s = unicodedata.normalize('NFC', s.lower())
    return re.sub(r'[^\w ]+', ' ', s).split()


def cer(ref, hyp):
    a, b = ' '.join(words(ref)), ' '.join(words(hyp))
    d = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, cb in enumerate(b, 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (ca != cb))
    return d[len(b)] / max(1, len(a))


def ff(args, inp, outp):
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', inp, *args, outp], check=True)


def trim(a, sr, pad=.06):
    fr = int(sr * .01); n = len(a) // fr
    if n < 3: return a
    e = np.sqrt(np.mean(a[:n * fr].reshape(n, fr) ** 2, axis=1) + 1e-12)
    idx = np.where(e > max(e.max() * .03, 1e-4))[0]
    if not len(idx): return a
    return a[max(0, idx[0] * fr - int(pad * sr)):min(len(a), (idx[-1] + 1) * fr + int(pad * sr))]


def level(a, target_db=-19.0, peak=.89):
    fr = int(SR * .02); n = len(a) // fr
    e = np.sqrt(np.mean(a[:n * fr].reshape(n, fr) ** 2, axis=1) + 1e-12)
    act = e[e > e.max() * .1]
    rms = float(np.sqrt(np.mean(act ** 2))) if len(act) else float(np.sqrt(np.mean(a ** 2)) + 1e-9)
    g = min(10 ** (target_db / 20) / max(rms, 1e-6), peak / max(1e-6, float(np.abs(a).max())))
    return a * g


def synth(text, n):
    best = None
    for k in range(3):
        t0 = time.time()
        a = np.asarray(tts.infer(text, voice=VOICE), dtype=np.float32).squeeze()
        raw = os.path.join(TMP, f'{n}-{k}.wav'); sf.write(raw, a, TSR)
        cur = os.path.join(TMP, f'{n}-{k}-24k.wav'); ff(['-ac', '1', '-ar', str(SR)], raw, cur)
        b, _ = sf.read(cur, dtype='float32'); b = trim(b, SR)
        segs, _ = asr.transcribe(cur, language='vi', beam_size=1, vad_filter=False)
        hyp = ' '.join(s.text for s in segs).strip()
        c = cer(text, hyp); cps = len(text) / max(.1, len(b) / SR)
        score = c + (.5 if cps < 8 or cps > 22 else 0)
        r = {'k': k, 'cer': round(c, 3), 'dur': round(len(b) / SR, 2), 'cps': round(cps, 1), 'asr': hyp, 't': round(time.time() - t0, 1)}
        if best is None or score < best[2]: best = (b, r, score)
        if score <= .18: break
    return best


GAP = np.zeros(int(SR * .42), dtype=np.float32)
index, rep = {}, []
t00 = time.time()
for key, ls in mine:
    parts, pos, cues = [], 0, []
    for l in ls:
        a, r, _ = synth(l['say'], f"{l['b']}-{l['s']}-{l['i']}")
        a = level(a)
        if parts: parts.append(GAP); pos += len(GAP)
        cues.append([round(pos / SR, 3), round(len(a) / SR, 3), l['text']])
        parts.append(a); pos += len(a)
        rep.append({'b': l['b'], 's': l['s'], 'i': l['i'], 'say': l['say'], **r})
        P(f"b{l['b']}s{l['s']}.{l['i']} cer={r['cer']} dur={r['dur']} cps={r['cps']} try={r['k'] + 1} t={r['t']} | {r['asr']}")
    name = f'b{key[0]}s{key[1]:02d}'
    wav = os.path.join(TMP, name + '.wav'); sf.write(wav, np.concatenate(parts), SR)
    ff(['-ac', '1', '-c:a', 'libopus', '-b:a', '48k', '-application', 'voip'], wav, os.path.join(OUT, name + '.opus'))
    index[name] = {'dur': round(pos / SR, 3), 'cues': cues}
    P(f'== {name} {round(pos / SR, 1)}s  (đã chạy {round((time.time() - t00) / 60, 1)} phút)')
json.dump(index, open(os.path.join(OUT, f'index-{K}.json'), 'w', encoding='utf8'), ensure_ascii=False)
json.dump(rep, open(os.path.join(OUT, f'report-{K}.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=0)
P('Xong shard', K, 'slide', len(mine), 'tổng', round(sum(v['dur'] for v in index.values()) / 60, 1), 'phút', 'CER tb',
  round(sum(r['cer'] for r in rep) / max(1, len(rep)), 3))
