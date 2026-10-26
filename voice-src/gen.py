# Đọc toàn bộ lời thoại Mô phỏng bằng VieNeu-TTS (chạy trên GitHub Actions), kiểm tra lại bằng nhận dạng giọng nói,
# gộp mỗi ca thành một file voice/<ca>.mp3 và ghi vị trí từng câu vào voice/index.json
# python voice-src/gen.py <thư mục ra>
import json, os, re, subprocess, sys, time, unicodedata
import numpy as np, soundfile as sf
D = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
TMP = os.path.join(OUT, '_tmp'); os.makedirs(TMP, exist_ok=True)
job = json.load(open(os.path.join(D, 'lines.json'), encoding='utf8'))
LINES = job['lines']
ONLY = set(filter(None, os.environ.get('ONLY_CASES', '').split(',')))
if ONLY: LINES = [l for l in LINES if l['case'] in ONLY]
SR = 24000
from vieneu import Vieneu
tts = Vieneu()
TSR = getattr(tts, 'sample_rate', None) or 48000
from faster_whisper import WhisperModel
asr = WhisperModel('medium', device='cpu', compute_type='int8')
log = open(os.path.join(OUT, 'gen-log.txt'), 'a', encoding='utf8')
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


def trim(a, sr, pad=.08):
    # bỏ khoảng lặng đầu/cuối (ngưỡng theo năng lượng khung 10 ms), chừa lại pad giây mỗi bên
    fr = int(sr * .01); n = len(a) // fr
    if n < 3: return a
    e = np.sqrt(np.mean(a[:n * fr].reshape(n, fr) ** 2, axis=1) + 1e-12)
    thr = max(e.max() * .03, 1e-4)
    idx = np.where(e > thr)[0]
    if not len(idx): return a
    s = max(0, idx[0] * fr - int(pad * sr)); t = min(len(a), (idx[-1] + 1) * fr + int(pad * sr))
    return a[s:t]


def level(a, target_db=-20.0, peak=.89):
    # chuẩn hóa độ to theo RMS của phần có tiếng, giới hạn đỉnh
    fr = int(SR * .02); n = len(a) // fr
    e = np.sqrt(np.mean(a[:n * fr].reshape(n, fr) ** 2, axis=1) + 1e-12)
    act = e[e > e.max() * .1]
    rms = float(np.sqrt(np.mean(act ** 2))) if len(act) else float(np.sqrt(np.mean(a ** 2)) + 1e-9)
    g = 10 ** (target_db / 20) / max(rms, 1e-6)
    g = min(g, peak / max(1e-6, float(np.abs(a).max())))
    return a * g


FX = {
    '': [],
    # trẻ con: cao giọng (đổi cả âm sắc), nói nhanh hơn một chút
    'kid': ['-af', f'asetrate={SR}*1.22,aresample={SR},atempo=0.9'],
    # người lớn tuổi: trầm hơn một chút, chậm hơn
    'old': ['-af', f'asetrate={SR}*0.94,aresample={SR},atempo=0.98'],
    'slow': ['-af', 'atempo=0.94'],
}


def synth(line, n):
    best = None
    for k in range(3):
        t0 = time.time()
        audio = tts.infer(line['say'], voice=line['voice'])
        a = np.asarray(audio, dtype=np.float32).squeeze()
        raw = os.path.join(TMP, f'{n:03d}-{k}.wav'); sf.write(raw, a, TSR)
        cur = os.path.join(TMP, f'{n:03d}-{k}-24k.wav')
        ff(['-ac', '1', '-ar', str(SR)] + FX[line['fx']], raw, cur)
        b, _ = sf.read(cur, dtype='float32'); b = trim(b, SR)
        segs, _ = asr.transcribe(cur, language='vi', beam_size=5, vad_filter=False)
        hyp = ' '.join(s.text for s in segs).strip()
        c = cer(line['say'], hyp)
        cps = len(line['say']) / max(.1, len(b) / SR)
        bad = c > .25 or cps < 7 or cps > 24
        r = {'k': k, 'cer': round(c, 3), 'dur': round(len(b) / SR, 2), 'cps': round(cps, 1), 'asr': hyp, 't': round(time.time() - t0, 1)}
        if best is None or (r['cer'] < best[1]['cer']): best = (b, r)
        if not bad and c <= .12: break
    return best


rep = {'lines': [], 'tsr': TSR}
by_case = {}
for n, line in enumerate(LINES):
    a, r = synth(line, n)
    a = level(a)
    by_case.setdefault(line['case'], []).append((line, a))
    rep['lines'].append({'case': line['case'], 'key': line['key'], 'w': line['w'], 'voice': line['voice'], 'fx': line['fx'], 'say': line['say'], **r})
    P(f"{n + 1}/{len(LINES)} {line['case']} {line['w']} {line['voice']} cer={r['cer']} dur={r['dur']} cps={r['cps']} try={r['k'] + 1} | {r['asr']}")
GAP = np.zeros(int(SR * .3), dtype=np.float32)
index = {'cases': {}, 'sample': job.get('sample')}
for cid, items in by_case.items():
    parts, pos, l = [GAP], len(GAP), {}
    for line, a in items:
        l[line['key']] = [round(pos / SR, 3), round(len(a) / SR, 3)]
        parts += [a, GAP]; pos += len(a) + len(GAP)
    wav = os.path.join(TMP, cid + '.wav'); sf.write(wav, np.concatenate(parts), SR)
    ff(['-ac', '1', '-ar', str(SR), '-c:a', 'libmp3lame', '-b:a', '48k', '-write_xing', '1'], wav, os.path.join(OUT, cid + '.mp3'))
    index['cases'][cid] = {'l': l, 'dur': round(pos / SR, 2)}
json.dump(index, open(os.path.join(OUT, 'index.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
json.dump(rep, open(os.path.join(OUT, 'report.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
worst = sorted(rep['lines'], key=lambda r: -r['cer'])[:12]
P('Tệ nhất:'); [P(' ', r['case'], r['cer'], r['say'], '|', r['asr']) for r in worst]
P('Trung bình CER', round(sum(r['cer'] for r in rep['lines']) / max(1, len(rep['lines'])), 3), 'tổng', round(sum(r['dur'] for r in rep['lines']) / 60, 1), 'phút')
