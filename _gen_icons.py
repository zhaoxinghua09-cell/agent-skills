# -*- coding: utf-8 -*-
"""生成 4 个爆款技能的 512 图标（LGD 视觉系统 v2：藏青底 + 青绿强调）。"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

OUT = pathlib.Path("D:/Workbuddy/05-工具/agent-skills")
NAVY = (11, 31, 58)        # #0B1F3A
TEAL = (20, 184, 166)      # #14B8A6
INK = (235, 240, 248)
FONT = "C:/Windows/Fonts/msyh.ttc"

def font(sz):
    try:
        return ImageFont.truetype(FONT, sz)
    except Exception:
        return ImageFont.load_default()

def base():
    im = Image.new("RGBA", (512, 512), NAVY)
    d = ImageDraw.Draw(im)
    # 外青绿细环
    d.ellipse([18, 18, 494, 494], outline=TEAL, width=6)
    return im, d

def save(im, name):
    p = OUT / name / "icon.png"
    p.parent.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").save(p, "PNG")
    print("saved", p)

# ① context-engineering: 嵌套上下文窗口
im, d = base()
for i, (x0, y0, x1, y1) in enumerate([(120,120,392,392),(150,150,362,362),(180,180,332,332)]):
    d.rectangle([x0,y0,x1,y1], outline=TEAL if i%2==0 else INK, width=5)
d.rectangle([210,210,302,302], fill=TEAL)
save(im, "context-engineering")

# ② ai-cost-cutter: 剪刀 + 币
im, d = base()
# 币
d.ellipse([150,150,362,362], outline=TEAL, width=10)
d.text((256, 250), "¥", fill=TEAL, font=font(150), anchor="mm")
# 剪刀两刃
d.line([(150,150),(300,300)], fill=INK, width=8)
d.line([(362,150),(212,300)], fill=INK, width=8)
save(im, "ai-cost-cutter")

# ③ prompt-injection-shield: 盾 + 叉
im, d = base()
pts = [(256,120),(380,170),(380,300),(256,400),(132,300),(132,170)]
d.polygon(pts, outline=TEAL, width=8)
d.line([(200,210),(312,330)], fill=(220,80,80), width=12)
d.line([(312,210),(200,330)], fill=(220,80,80), width=12)
save(im, "prompt-injection-shield")

# ④ eu-ai-act-companion: 天平 / 对勾
im, d = base()
d.line([(256,160),(256,360)], fill=TEAL, width=8)
d.line([(150,180),(362,180)], fill=TEAL, width=8)
d.ellipse([120,160,200,240], outline=INK, width=6)
d.ellipse([312,160,392,240], outline=INK, width=6)
d.polygon([(256,250),(236,300),(256,300),(256,360),(276,300),(256,300)], fill=TEAL)
save(im, "eu-ai-act-companion")

print("done")
