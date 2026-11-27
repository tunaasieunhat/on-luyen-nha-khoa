import re,json,unicodedata
def nz(s):
    s=unicodedata.normalize('NFC',s).replace('–','-').replace('–','-').replace(' ',' ')
    return s
def nums(s):
    s=nz(s); s=re.sub(r'\*\*','',s)
    return set(re.findall(r'\d+(?:[.,]\d+)?',s))
decks=json.load(open('sl/out/decks.json'))
for b in range(1,12):
    src=nz(open(f'les/c{b}.txt').read()); srcn=nums(src)
    md=open(f'src/b{b}.md').read()
    dk=json.dumps(decks[f'dl-bai-{b}'],ensure_ascii=False)
    dk=re.sub(r'"(src|n|nq|mins|w|h|a|b)": ?[^,}]+','',dk)
    for name,t in [('bài',md),('slide',dk)]:
        miss=sorted(n for n in nums(t)-srcn if not re.fullmatch(r'[0-9]',n))
        if miss: print(b,name,miss)
