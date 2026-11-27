import re,base64,io,sys,glob
from PIL import Image
def conv(m):
    im=Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGB')
    b=io.BytesIO(); im.save(b,'JPEG',quality=78,optimize=True,progressive=True)
    return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
for f in glob.glob('print/dl-bai-*.html'):
    s=open(f,encoding='utf8').read(); s=re.sub(r'data:image/webp;base64,([A-Za-z0-9+/=]+)',conv,s); open(f,'w',encoding='utf8').write(s)
# cover
Image.open('print/cover.webp').convert('RGB').save('print/cover.jpg',quality=85)
