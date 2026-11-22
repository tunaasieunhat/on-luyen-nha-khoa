# Dựng video bài giảng 480p từ ảnh slide + giọng đọc (lecture-out)
# python3 assemble.py <thư mục lecture-out/out> <bài> [<bài> ...]
import json, os, subprocess, sys, glob
import numpy as np, wave


class sf:
    @staticmethod
    def read(p, dtype='float32'):
        with wave.open(p) as w:
            a = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype('float32') / 32768
            return a, w.getframerate()

    @staticmethod
    def write(p, a, sr):
        with wave.open(p, 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
            w.writeframes((np.clip(a, -1, 1) * 32767).astype('<i2').tobytes())
D = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1]; BS = [int(x) for x in sys.argv[2:]]
IMG = '/home/claude/on-luyen-nha-khoa/slides/vlnk/img'
W, H, FPS, SR = 854, 480, 30, 24000
LEAD, TAIL, XF = .7, .9, .45
idx = {}
for f in glob.glob(os.path.join(SRC, 'index-*.json')): idx.update(json.load(open(f, encoding='utf8')))
X264 = ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22', '-tune', 'stillimage', '-pix_fmt', 'yuv420p',
        '-r', str(FPS), '-g', str(FPS * 10), '-keyint_min', str(FPS * 10), '-sc_threshold', '0', '-an']


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-2000:]); raise SystemExit(1)


def png(b, s):
    p = os.path.join(D, 'frames', f'b{b}', f'{s:02d}.png'); os.makedirs(os.path.dirname(p), exist_ok=True)
    if not os.path.exists(p):
        run(['ffmpeg', '-loglevel', 'error', '-y', '-i', os.path.join(IMG, f'b{b}', f'{s:02d}.webp'),
             '-vf', f'scale={W}:{H}:flags=lanczos,format=rgb24', p])
    return p


for b in BS:
    names = sorted(k for k in idx if k.startswith(f'b{b}s'))
    n_img = len(glob.glob(os.path.join(IMG, f'b{b}', '*.webp')))
    assert len(names) == n_img, (b, len(names), n_img)
    wd = os.path.join(D, 'build', f'b{b}'); os.makedirs(wd, exist_ok=True)
    audio, cues, lst, t = [], [], [], 0.0
    for k, name in enumerate(names):
        s = int(name.split('s')[1]); e = idx[name]
        lead = 1.0 if k == 0 else LEAD
        # giải mã opus -> 24 kHz mono
        wav = os.path.join(wd, name + '.wav')
        run(['ffmpeg', '-loglevel', 'error', '-y', '-i', os.path.join(SRC, name + '.opus'), '-ac', '1', '-ar', str(SR), wav])
        a, _ = sf.read(wav, dtype='float32')
        dur = round((lead + len(a) / SR + TAIL) * FPS) / FPS  # khớp khung hình
        seg = np.zeros(int(round(dur * SR)), dtype=np.float32)
        o = int(lead * SR); seg[o:o + len(a)] = a[:len(seg) - o]
        audio.append(seg)
        for c0, cd, txt in e['cues']:
            cues.append([round(t + lead + c0, 2), round(t + lead + c0 + cd, 2), txt])
        clip = os.path.join(wd, f'{name}.mp4'); tmp = os.path.join(wd, f'{name}.part.mp4')
        if not os.path.exists(clip) or os.path.getsize(clip) < 1000 or json.load(open(clip + '.json')) != dur:
            cur = png(b, s)
            if k == 0:
                run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', str(FPS), '-i', cur,
                     '-vf', f'format=yuv420p,loop=-1:1,trim=duration={dur},fade=t=in:st=0:d=0.6', *X264, tmp])
            else:
                prev = png(b, int(names[k - 1].split('s')[1]))
                run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', str(FPS), '-i', prev, '-framerate', str(FPS), '-i', cur,
                     '-filter_complex',
                     f'[0]format=yuv420p,loop=-1:1,trim=duration={XF},settb=AVTB[a];'
                     f'[1]format=yuv420p,loop=-1:1,trim=duration={dur},settb=AVTB[b];'
                     f'[a][b]xfade=transition=fade:duration={XF}:offset=0,trim=duration={dur}', *X264, tmp])
            os.replace(tmp, clip); json.dump(dur, open(clip + '.json', 'w'))
        lst.append(f"file '{clip}'"); t += dur
    open(os.path.join(wd, 'list.txt'), 'w').write('\n'.join(lst) + '\n')
    full = np.concatenate(audio)
    full[-int(SR * .5):] *= np.linspace(1, 0, int(SR * .5), dtype=np.float32)
    sf.write(os.path.join(wd, 'audio.wav'), full, SR)
    vid = os.path.join(wd, 'video.mp4')
    run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(wd, 'list.txt'), '-c', 'copy', vid])
    out = os.path.join(D, 'out', f'b{b}.mp4'); os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = out[:-4] + '.part.mp4'
    run(['ffmpeg', '-loglevel', 'error', '-y', '-i', vid, '-i', os.path.join(wd, 'audio.wav'), '-map', '0:v', '-map', '1:a',
         '-c:v', 'copy', '-c:a', 'aac', '-b:a', '64k', '-ac', '1', '-ar', '24000', '-movflags', '+faststart', '-shortest', tmp])
    os.replace(tmp, out)
    # mốc thời gian từng slide (để nhảy tới slide trong app)
    marks, tt = [], 0.0
    for seg in audio: marks.append(round(tt, 2)); tt += len(seg) / SR
    json.dump({'dur': round(t, 2), 'slides': marks, 'cues': cues}, open(os.path.join(D, 'out', f'b{b}.json'), 'w', encoding='utf8'),
              ensure_ascii=False, separators=(',', ':'))
    print(f'b{b}: {round(t / 60, 1)} phút, {len(cues)} câu, {round(os.path.getsize(out) / 1e6, 1)} MB')
