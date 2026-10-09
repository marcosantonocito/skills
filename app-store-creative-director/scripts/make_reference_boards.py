#!/usr/bin/env python3
"""Produce original, brand-neutral abstract layout diagrams (no third-party app assets)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parents[1]/'assets'/'compositions'
HERE.mkdir(parents=True,exist_ok=True)

FONTS=[Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'),Path('/System/Library/Fonts/Supplemental/Arial Bold.ttf')]
REGULAR=[Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),Path('/System/Library/Fonts/Supplemental/Arial.ttf')]
def f(sz,bold=True):
    paths=FONTS if bold else REGULAR
    for p in paths:
        if p.exists(): return ImageFont.truetype(str(p),sz)
    return ImageFont.load_default()

def text(d,pos,value,color,size=30,bold=True): d.text(pos,value,font=f(size,bold),fill=color)
def rr(d,box,r,fill,outline=None,width=2): d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)
def mock_phone(im,x,y,w,h,dark=False,rotation=0):
    shell=Image.new('RGBA',(w,h),(0,0,0,0)); a=ImageDraw.Draw(shell)
    rr(a,(1,1,w-2,h-2),round(w*.15),'#171923' if dark else '#141721')
    inset=max(9,round(w*.045)); rr(a,(inset,inset,w-inset,h-inset),round(w*.11),'#171C2E' if dark else '#FFFFFF')
    rr(a,(round(w*.36),inset+5,round(w*.64),inset+14),6,'#10131B')
    left,right=inset+round(w*.09),w-inset-round(w*.09)
    ink='#F5F8FA' if dark else '#243047'
    line='#333C56' if dark else '#EDF1F6'
    accent='#82E0D4' if dark else '#B6A8F9'
    a.rounded_rectangle((left,int(h*.15),right,int(h*.38)),radius=round(w*.055),fill=accent)
    a.rounded_rectangle((left,int(h*.43),left+round(w*.54),int(h*.47)),radius=9,fill=ink)
    a.rounded_rectangle((left,int(h*.49),right,int(h*.515)),radius=8,fill=line)
    a.rounded_rectangle((left,int(h*.53),right-int(w*.10),int(h*.555)),radius=8,fill=line)
    for i in range(3):
        top=int(h*(.61+i*.095))
        a.rounded_rectangle((left,top,right,top+int(h*.073)),radius=12,fill=line)
        a.rounded_rectangle((left+12,top+12,left+50,top+int(h*.073)-12),radius=10,fill=accent)
    if rotation: shell=shell.rotate(rotation,resample=Image.Resampling.BICUBIC,expand=True)
    im.paste(shell,(x,y),shell)

def footer(im, label):
    d=ImageDraw.Draw(im); w,h=im.size
    d.line((35,h-65,w-35,h-65),fill='#999999',width=1)
    text(d,(38,h-51),'ORIGINAL COMPOSITION STUDY', '#606670',size=18)
    text(d,(w-205,h-51),'NOT FOR UPLOAD', '#606670',size=16)
    # small number near top-right
    text(d,(w-260,23),label,'#7C8290',size=17)

# all six images 650 x 900 except banners/tablet. Made independently from real-app UI.
W,H=650,900

im=Image.new('RGB',(W,H),'#F0ECFA');d=ImageDraw.Draw(im)
text(d,(48,68),'Find your', '#27224C',60)
text(d,(48,144),'daily clarity.', '#27224C',60)
rr(d,(48,250,350,266),8,'#9284D1'); rr(d,(48,286,300,301),8,'#C9C0EA')
d.ellipse((360,290,640,590),fill='#D8CEF3')
mock_phone(im,165,340,320,510)
footer(im,'01 / PRODUCT CLARITY');im.save(HERE/'01-product-clarity.png',optimize=True)

im=Image.new('RGB',(W,H),'#F6F1E8');d=ImageDraw.Draw(im)
text(d,(43,53),'EVERY', '#222324',72)
text(d,(43,137),'DETAIL', '#222324',72)
text(d,(43,224),'MATTERS', '#222324',72)
d.line((46,326,602,326),fill='#B55B4D',width=8)
text(d,(46,344),'Make the product the hero.', '#89695C',22,False)
d.polygon([(0,470),(W,410),(W,900),(0,900)],fill='#E7DFD2')
mock_phone(im,200,435,288,430)
footer(im,'02 / EDITORIAL');im.save(HERE/'02-editorial-type.png',optimize=True)

im=Image.new('RGB',(W,H),'#24164C');d=ImageDraw.Draw(im)
d.ellipse((-180,320,350,850),fill='#5D42A0')
d.ellipse((380,320,770,710),fill='#9F5CDC')
d.ellipse((460,165,620,325),fill='#FFBD74')
text(d,(42,68),'MAKE IT', '#FDEEE8',62)
text(d,(42,148),'HAPPEN.', '#FDEEE8',62)
rr(d,(45,260,290,273),6,'#F1C2DD')
mock_phone(im,163,360,315,520,dark=True,rotation=10)
footer(im,'03 / EXPRESSIVE');im.save(HERE/'03-playful-depth.png',optimize=True)

im=Image.new('RGB',(W,H),'#D9EEE8');d=ImageDraw.Draw(im)
text(d,(42,48),'Two moments.', '#154D44',54)
text(d,(42,113),'One flow.', '#154D44',54)
d.ellipse((-150,420,250,820),fill='#B4DBCE')
d.ellipse((410,370,790,760),fill='#9DCABD')
mock_phone(im,45,325,272,475)
mock_phone(im,290,265,300,535)
footer(im,'04 / DUAL SCREEN');im.save(HERE/'04-dual-screen.png',optimize=True)

im=Image.new('RGB',(W,H),'#0F1C38');d=ImageDraw.Draw(im)
d.polygon([(0,620),(650,380),(650,900),(0,900)],fill='#1C3356')
d.ellipse((200,160,560,520),fill='#356A72')
text(d,(42,57),'THE BIG', '#ECF6F3',57)
text(d,(42,130),'PICTURE', '#ECF6F3',57)
mock_phone(im,190,325,265,480,dark=True)
footer(im,'05 / FEATURE');im.save(HERE/'05-feature-banner.png',optimize=True)

im=Image.new('RGB',(W,H),'#EEE9DF');d=ImageDraw.Draw(im)
text(d,(42,49),'SPACE TO', '#2F354D',54)
text(d,(42,110),'EXPLORE', '#2F354D',54)
rr(d,(50,250,600,690),25,'#3A465F')
rr(d,(75,275,575,665),20,'#F7F8FD')
rr(d,(104,307,230,626),12,'#D4E0ED')
rr(d,(252,307,545,420),12,'#CCD8F4')
rr(d,(252,443,381,626),12,'#DDD4F0')
rr(d,(400,443,545,626),12,'#E2E7F3')
footer(im,'06 / TABLET');im.save(HERE/'06-tablet-landscape.png',optimize=True)

# Contact sheet helps user browse inspirations in a single image.
files=sorted(HERE.glob('[0-9][0-9]-*.png'))
thumb_w,thumb_h=320,444
sheet=Image.new('RGB',(1040,980),'#F9FAFC')
d=ImageDraw.Draw(sheet)
text(d,(32,12),'Visual reference library', '#161A2F',34)
text(d,(33,52),'Six original composition studies. Replace all placeholder UI with real captures.', '#5B6272',16,False)
for i,file in enumerate(files):
    small=Image.open(file).resize((thumb_w,thumb_h),Image.Resampling.LANCZOS)
    x=30+(i%3)*340;y=95+(i//3)*435
    sheet.paste(small,(x,y))
sheet.save(HERE/'00-contact-sheet.png',optimize=True)
print('Created',len(files),'studies and contact sheet')
