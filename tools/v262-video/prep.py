# Tách lời giảng n1..n5.txt thành từng câu (phụ đề giữ nguyên chữ, lời đọc phiên âm thuật ngữ cho TTS)
# python3 prep.py  -> lines.json
import json, re, os
D = os.path.dirname(os.path.abspath(__file__))
SAY = {
 'composite': 'com pô dít', 'amalgam': 'a man gam', 'monome': 'mô nôm', 'polymer': 'pô li me', 'polyme': 'pô li me',
 'copolymer': 'cô pô li me', 'slide': 'xờ lai', 'TEGDMA': 'tê e giê đê em a', 'electron': 'e léc trôn', 'nano': 'na nô',
 'bis GMA': 'bít giê em a', 'bis DMA': 'bít đê em a', 'PMMA': 'pê em em a', 'MMA': 'em em a', 'UDMA': 'u đê em a',
 'inlay': 'in lây', 'onlay': 'on lây', 'silane': 'xi lan', 'acrylic': 'a cờ ri lích', 'hydro': 'hi đờ rô',
 'silicone': 'xi li côn', 'micro': 'mi crô', 'micromét': 'mi crô mét', 'microgam': 'mi crô gam', 'latex': 'la téc',
 'HF': 'hát ép', 'BPO': 'bê pê ô', 'factor': 'phắc tơ', 'labo': 'la bô', 'fluor': 'flo', 'implant': 'im plăng',
 'glass ionomer': 'gờ lát i ô nô me', 'bery': 'be ri', 'methacrylate': 'mê ta cờ ri lát', 'dimethacrylate': 'đi mê ta cờ ri lát',
 'ADA': 'a đê a', 'FDA': 'ép đê a', 'ISO': 'i xô', 'ANSI': 'an xi', 'NIST': 'nít', 'NIOM': 'ni ôm', 'CE': 'xê e', 'TC': 'tê xê',
 'sealant': 'xi lân', 'sealer': 'xi lơ', 'silicat': 'xi li cát', 'silica': 'xi li ca', 'acid': 'a xít', 'video': 'vi đê ô',
 'collagen': 'cô la gien', 'palladium': 'pa la đi um', 'HEMA': 'hê ma', 'gel': 'gien', 'resin': 'rê xin',
 'gutta percha': 'gút ta péc cha', 'camphorquinone': 'cam pho qui nôn', 'Fauchard': 'Phô sa', 'G V Black': 'giê vê Bờ lách',
 'X quang': 'ích quang', 'veneer': 'vơ nia', 'zirconia': 'di cô ni a', 'zirconium': 'di cô ni um', 'zirconi': 'di cô ni',
 'BPA': 'bê pê a', 'gluconat': 'glu cô nát', 'van der Waals': 'van đe van', 'teflon': 'tê phờ lông', 'Bowen': 'Bô oen',
 'Pfaff': 'Pháp', 'compomer': 'com pô me', 'laser': 'la de', 'phosphat': 'phốt phát', 'phosphate': 'phốt phát',
 'phosphoric': 'phốt pho ríc', 'protein': 'prô tê in', 'methyl': 'mê tin', 'ethyl': 'ê tin', 'butyl': 'bu tin', 'APF': 'a pê ép',
 'sulfat': 'sun phát', 'polysulfide': 'pô li sun phít', 'polyether': 'pô li ê te', 'silorane': 'xi lô ran',
 'benzoyl peroxide': 'ben dô in pê rô xít', 'nanohybrid': 'na nô hai brít', 'Taggert': 'Ta gơt', 'ceramic': 'xê ra mích',
 'CAD CAM': 'cát cam', 'hydrofluoric': 'hi đrô flo ríc', 'lympho': 'lim phô', 'adhesion': 'át hi giần',
 'cohesion': 'cô hi giần', 'epoxy': 'e pô xi', 'urethane': 'u rê than', 'hydroquinone': 'hi đrô qui nôn',
 'centipoise': 'xen ti poa', 'Phoenic': 'Phê ni xi', 'Etrusce': 'Ê tơ rút', 'Pierre': 'Pi e', 'Taveau': 'Ta vô',
 'Paré': 'Pa rê', 'Evans': 'Ê van', 'Goodyear': 'Gút y ơ', 'Colorado': 'Cô lô ra đô', 'pH': 'pê hát',
 'Paracelsus': 'Pa ra xen xớt', 'patch test': 'pát tét', 'Streptococcus': 'xờ tép tô cốc', 'polycarboxylat': 'pô li các bô xi lát',
 'carboxylat': 'các bô xi lát', 'eugenol': 'ơ giê nôn', 'Gell và Coombs': 'Gen và Cum', 'IgE': 'i giê e',
 'sodium thiosulfate': 'sô đi um thi ô sun phát', 'lichen': 'li ken', 'Crete': 'Cờ rét', 'acrylate': 'a cờ ri lát',
 'ethylacrylate': 'ê tin a cờ ri lát', 'formaldehyde': 'phoóc man đê hít', 'MSDS': 'em ét đê ét', 'proton': 'prô tôn',
 'neutron': 'nơ trôn', 'atom': 'a tôm', 'a tomos': 'a tô mốt', 'Democritus': 'Đê mô cờ rít', 'alumina': 'a lu mi na',
 'Robert Hooke': 'Rô be Húc', 'dioxit': 'đi ô xít', 'gallium': 'ga li', 'theta': 'tê ta', 'primer': 'prai mơ',
 'celluloid': 'xen lu lô ít', 'PVC': 'pê vê xê', 'carbon': 'các bon', 'imine': 'i min', 'mega pascal': 'mê ga pát xcan',
 'chloroform': 'clo rô phoóc', 'aceton': 'a xê tôn', 'hydroxyl': 'hi đrô xin', 'PENTA P': 'pen ta pê',
 'polyacrylic': 'pô li a cờ ri lích', 'polycarbonate': 'pô li các bô nát', 'siloxan': 'xi lô xan', 'BHT': 'bê hát tê',
 'estrogen': 'e xtrô gien', 'LED': 'lét', 'halogen': 'ha lô gien', 'plasma': 'pờ lát ma', 'xenon': 'xê nông',
 'argon': 'ác gông', 'carbide': 'các bít', 'ormocer': 'oóc mô xe', 'POSS': 'pót', 'T g': 'tê giê', 'độ C': 'độ xê',
 'Ray Bowen': 'Rây Bô oen', 'C factor': 'xê phắc tơ', 'tia X': 'tia ích', 'lympho T': 'lim phô tê', 'nhóm A': 'nhóm a', 'monome B': 'mô nôm bê', 'monome A': 'mô nôm a', 'oxy': 'ô xi', 'crôm': 'crôm', 'cara': 'ca ra', 'mili': 'mi li',
}
KEYS = sorted(SAY, key=len, reverse=True)
RX = re.compile(r'(?<![\wÀ-ỹ])(' + '|'.join(re.escape(k) for k in KEYS) + r')(?![\wÀ-ỹ])', re.I)
LOW = {k.lower(): v for k, v in SAY.items()}
LET = {'A': 'a', 'B': 'bê', 'C': 'xê', 'D': 'đê'}


def say(t):
    t = RX.sub(lambda m: LOW[m.group(1).lower()], t)
    # đáp án trắc nghiệm: "A, ..." "đáp án C:" ; "xoang một" không đụng
    t = re.sub(r'(?<![\wÀ-ỹ])([ABCD])(?=[,:.])', lambda m: LET[m.group(1)], t)
    return t


def chunks(s, lim=150):
    if len(s) <= lim: return [s]
    # cắt ở dấu phẩy / hai chấm gần giữa nhất
    cut = [m.end() for m in re.finditer(r'[,:;] ', s)]
    if not cut: return [s]
    mid = len(s) / 2
    c = min(cut, key=lambda x: abs(x - mid))
    a, b = s[:c].rstrip(' ,;'), s[c:].strip()
    a = a if a.endswith(':') else a + ','
    return chunks(a, lim) + chunks(b[0].upper() + b[1:] if False else b, lim)


out = []
for b in range(1, 6):
    t = open(os.path.join(D, f'n{b}.txt'), encoding='utf8').read()
    parts = re.split(r'^## (\d+)\n', t, flags=re.M)[1:]
    for k in range(0, len(parts), 2):
        s = int(parts[k]); i = 0
        for ln in parts[k + 1].splitlines():
            ln = ln.strip()
            if not ln: continue
            for c in chunks(ln):
                out.append({'b': b, 's': s, 'i': i, 'text': c, 'say': say(c)}); i += 1
json.dump({'lines': out}, open(os.path.join(D, 'lines.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=0)
import collections
print(len(out), 'câu', collections.Counter(x['b'] for x in out), 'dài nhất', max(len(x['say']) for x in out))
left = collections.Counter()
for x in out:
    for w in re.findall(r'[A-Za-z]{2,}', x['say']):
        if re.search(r'[fjwz]|[bcdghklmnprstvx]{3}', w, re.I) or w.isupper(): left[w] += 1
print('còn sót:', left.most_common(40))
