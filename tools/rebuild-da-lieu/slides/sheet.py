import sys,glob
from PIL import Image
d=sys.argv[1];fs=sorted(glob.glob(d+'/*.png'));ims=[Image.open(f).resize((640,360)) for f in fs]
cols=3;rows=(len(ims)+cols-1)//cols;s=Image.new('RGB',(640*cols,360*rows),'#888')
for k,im in enumerate(ims): s.paste(im,((k%cols)*640+0,(k//cols)*360))
s.save(sys.argv[2])
