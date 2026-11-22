#!/bin/bash
# Dựng lại toàn bộ slide AVCN2: dữ liệu -> ảnh kiểm tra -> PowerPoint -> bản in 4 slide/trang
set -e
W=/home/claude/work262s; SK=$(ls -d /root/.claude/skills/synced/*/pptx)
cd $W && python3 deck.py | tail -c 200 && python3 mkrender.py
cd /home/claude/work261 && cp $W/shot.js shot262s.js && sed -i "s#path.join(__dirname, 'render'#path.join('$W', 'render'#; s#path.join(__dirname, 'out'#path.join('$W', 'out'#" shot262s.js
DSF=1.5 node shot262s.js | tail -1
cd $W && rm -rf out/jpg && python3 -c "
from PIL import Image; import glob, os
for f in glob.glob('out/png/u*/*.png'):
    o=f.replace('/png/','/jpg/')[:-4]+'.jpg'; os.makedirs(os.path.dirname(o),exist_ok=True)
    Image.open(f).convert('RGB').resize((1280,720),Image.LANCZOS).save(o,quality=84,optimize=True)"
cd /home/claude/work261 && cp $W/pptx.js pptx262s.js && cp $W/handout.js handout262s.js && sed -i "s/f.endsWith('.png')/f.endsWith('.jpg')/" handout262s.js
rm -rf $W/out/pptx && PPTX_SKILL=$SK node pptx262s.js $W/out/decks.json $W/out/pptx | wc -l
for f in $W/out/pptx/*.pptx; do python3 $SK/scripts/office/validate.py "$f" | tail -1; done | sort | uniq -c
python3 - <<'PY'
import subprocess, glob, json
T = json.load(open('/home/claude/work262s/out/decks.json'))
for k, S in T.items():
    u = S[0]['u']; t = S[0]['en'] + ' – ' + S[0]['vi']
    pp = glob.glob(f'/home/claude/work262s/out/pptx/AVCN2-Slide-Unit-{u:02d}-*.pptx')[0]
    subprocess.run(['node', 'handout262s.js', f'/home/claude/work262s/out/jpg/u{u}', pp[:-5] + '-BanIn.pdf', f'Anh văn chuyên ngành 2 · Unit {u} · {t}'], check=True, capture_output=True)
PY
ls $W/out/pptx/*-BanIn.pdf | wc -l; du -ch $W/out/pptx/*-BanIn.pdf | tail -1
