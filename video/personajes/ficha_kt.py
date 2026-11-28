"""Ficha de personajes KAEN y TAMBO sobre fondo burst."""
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont
items = [('kaen','KAEN','#ff8a1e','#2a1206'),('kaen_brasa','MODO BRASA','#ff8a1e','#2a1206'),('kaen_brasa_golpe','GOLPE','#ff8a1e','#2a1206'),
         ('kaen_rodillas','APAGADO','#8a7a6a','#1a1614'),('tambo','TAMBO','#3fd0c8','#081e1e'),('tambo_tambor','FORMA TAMBOR','#e8ecff','#1c1e2e'),
         ('tambo_tambor_estirado','ESTIRADO','#e8ecff','#1c1e2e'),('tambo_tambor_gigante','PUÑO GIGANTE','#e8ecff','#1c1e2e'),('tambo_anciano','AGOTADO','#bfc3d0','#16171c')]
W,H=720,1280
def hexc(h,a=255): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))+(a,)
F=ImageFont.truetype('../jvb/fonts/Anton.ttf',72)
cards=[]
for f,name,col,dark in items:
    c=Image.new('RGBA',(W,H),hexc(dark)); d=ImageDraw.Draw(c); cx,cy=W//2,560
    for i in range(28):
        a0=i*2*math.pi/28; a1=a0+math.pi/28
        d.polygon([(cx,cy),(cx+1600*math.cos(a0),cy+1600*math.sin(a0)),(cx+1600*math.cos(a1),cy+1600*math.sin(a1))],fill=hexc(col,90))
    ch=Image.open(f+'.png'); ch=ch.resize((int(ch.width*0.6),int(ch.height*0.6)))
    c.alpha_composite(ch,((W-ch.width)//2,80))
    tw=d.textlength(name,font=F); d.text(((W-tw)/2,1150),name,font=F,fill='white',stroke_width=7,stroke_fill='black')
    cards.append(c)
sheet=Image.new('RGB',(W*5,H*2),(10,10,12))
for i,c in enumerate(cards): sheet.paste(c.convert('RGB'),((i%5)*W if i<4 else (i-4)*W,0 if i<4 else H))
sheet.save('ficha_kaen_tambo.png')
