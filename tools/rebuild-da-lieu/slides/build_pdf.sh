set -e
cd /home/claude/work261
for b in "$@"; do
  slug=$(python3 -c "import json;m={x['b']:x for x in json.load(open('/home/claude/dl/meta.json'))}[$b];print(m['file'].replace('DL-Bai-','DL-Slide-Bai-').replace('.pdf',''))")
  title=$(python3 -c "import json;m={x['b']:x for x in json.load(open('/home/claude/dl/meta.json'))}[$b];print('Da Liễu · Bài $b. '+m['title'])")
  node /home/claude/dl/sl/slidepdf.js dl-bai-$b /home/claude/dl/sl/pdf/raw$b.pdf
  python3 /home/claude/dl/sl/impose.py /home/claude/dl/sl/pdf/raw$b.pdf "/home/claude/dl/sl/pdf/$slug-BanIn.pdf" "$title" | tail -1
done
