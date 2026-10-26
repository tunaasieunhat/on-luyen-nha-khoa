# Thử VieNeu-TTS trên máy GitHub Actions: liệt kê giọng có sẵn, đọc thử một câu bằng từng giọng, đo cao độ + nhận dạng lại
import inspect, json, os, sys, time, traceback
import numpy as np, soundfile as sf
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
import vieneu
from vieneu import Vieneu
rep = {'version': getattr(vieneu, '__version__', '?')}
t0 = time.time(); tts = Vieneu(); rep['load_s'] = round(time.time() - t0, 1)
rep['infer_sig'] = str(inspect.signature(tts.infer))
rep['infer_doc'] = (tts.infer.__doc__ or '')[:2000]
rep['class_methods'] = [m for m in dir(tts) if not m.startswith('_')]
voices = tts.list_preset_voices(); rep['voices'] = [list(v) if isinstance(v, (list, tuple)) else v for v in voices]
print(json.dumps(rep, ensure_ascii=False, indent=1), flush=True)
TEXT = 'Bác sĩ ơi, em đau răng quá, đêm qua không ngủ được. Em uống thuốc giảm đau rồi mà vẫn không đỡ ạ.'
import parselmouth
from faster_whisper import WhisperModel
asr = WhisperModel('medium', device='cpu', compute_type='int8')
def norm(s):
    import re, unicodedata
    s = unicodedata.normalize('NFC', s.lower()); return re.sub(r'[^\w ]+', ' ', s).split()
def cer(a, b):
    a, b = ' '.join(norm(a)), ' '.join(norm(b))
    d = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, cb in enumerate(b, 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (ca != cb))
    return d[len(b)] / max(1, len(a))
res = []
for v in voices:
    label, vid = (v[0], v[1]) if isinstance(v, (list, tuple)) else (str(v), v)
    r = {'label': label, 'id': vid}
    for key in (vid, label):
        try:
            t0 = time.time(); audio = tts.infer(TEXT, voice=key); r['infer_s'] = round(time.time() - t0, 2); r['key'] = key; break
        except Exception as e:
            r.setdefault('err', []).append(repr(e)[:300])
    else:
        res.append(r); continue
    a = np.asarray(audio, dtype=np.float32).squeeze()
    sr = getattr(tts, 'sample_rate', None) or 48000
    fn = os.path.join(OUT, f'{len(res):02d}.wav'); sf.write(fn, a, sr)
    r['sr'] = sr; r['dur'] = round(len(a) / sr, 2); r['peak'] = float(np.abs(a).max())
    snd = parselmouth.Sound(fn); f0 = snd.to_pitch().selected_array['frequency']; f0 = f0[f0 > 0]
    r['f0_med'] = round(float(np.median(f0)), 1) if len(f0) else 0
    segs, _ = asr.transcribe(fn, language='vi', beam_size=5)
    hyp = ' '.join(s.text for s in segs).strip(); r['asr'] = hyp; r['cer'] = round(cer(TEXT, hyp), 3)
    print(json.dumps(r, ensure_ascii=False), flush=True); res.append(r)
rep['samples'] = res
json.dump(rep, open(os.path.join(OUT, 'discover.json'), 'w'), ensure_ascii=False, indent=1)
