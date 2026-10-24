import os
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

def fa(text):
    if not text:
        return ""
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

base_dir = r"D:\Machinedesign.ir\social-content\launch-dumpling-series"
out_dir = os.path.join(base_dir, "02_generated_visuals")

font_dir = r"C:\Users\Admin\.gemini\config\skills\machinedesign-artifact-designer\resources\fonts"
font_black = os.path.join(font_dir, "Vazirmatn-Black.ttf")
font_bold = os.path.join(font_dir, "Vazirmatn-Bold.ttf")
font_med = os.path.join(font_dir, "Vazirmatn-Medium.ttf")
font_segoe_bold = r"C:\Windows\Fonts\segoeuib.ttf"
if not os.path.exists(font_segoe_bold):
    font_segoe_bold = r"C:\Windows\Fonts\arialbd.ttf"

logo_sym_path = r"D:\Machinedesign.ir\branding\logos\logo_symbol_md_metallic_transparent.png"

W, H = 1080, 1350
canvas = Image.new("RGBA", (W, H), (255, 255, 255, 255))
draw = ImageDraw.Draw(canvas)

f_brand_title = ImageFont.truetype(font_segoe_bold, 36)
f_brand_sub = ImageFont.truetype(font_bold, 20)
f_badge = ImageFont.truetype(font_segoe_bold, 22)

f_h1 = ImageFont.truetype(font_black, 48)
f_sub = ImageFont.truetype(font_bold, 24)

f_card_title = ImageFont.truetype(font_black, 24)
f_card_sub = ImageFont.truetype(font_bold, 20)
f_card_desc1 = ImageFont.truetype(font_bold, 17)
f_card_desc2 = ImageFont.truetype(font_med, 17)

f_flow_title = ImageFont.truetype(font_black, 25)
f_step_num = ImageFont.truetype(font_black, 20)
f_step_name = ImageFont.truetype(font_bold, 18)
f_step_desc = ImageFont.truetype(font_med, 15)

f_cta = ImageFont.truetype(font_black, 26)

PRIMARY_NAVY = (15, 28, 48, 255)
TEAL_DARK = (16, 78, 92, 255)
TEXT_MUTED = (80, 95, 110, 255)
CARD_BG = (248, 250, 252, 255)
CARD_BORDER = (215, 226, 238, 255)

BLUE_BG = (244, 248, 254, 255)
BLUE_BORDER = (195, 218, 248, 255)

# 1. Header (y: 18 to 118)
if os.path.exists(logo_sym_path):
    sym = Image.open(logo_sym_path).convert("RGBA")
    sh = 92
    sw = int(sym.width * (sh / sym.height))
    sym = sym.resize((sw, sh), Image.Resampling.LANCZOS)
    canvas.paste(sym, (50, 18), sym)
    
    draw.text((50 + sw + 18, 28), "MachineDesign.ir", fill=TEAL_DARK, font=f_brand_title)
    draw.text((50 + sw + 20, 74), fa("مرکز تخصصی طراحی و ساخت ماشین‌آلات صنعتی"), fill=TEXT_MUTED, font=f_brand_sub)

badge_text = "MODEL: KBDM-150"
bbox_badge = draw.textbbox((0, 0), badge_text, font=f_badge)
bw = bbox_badge[2] - bbox_badge[0] + 44
bh = 48
bx1 = W - 50 - bw
by1 = 38
draw.rounded_rectangle([(bx1, by1), (W - 50, by1 + bh)], radius=10, fill=(244, 248, 252, 255), outline=TEAL_DARK, width=2)
draw.text((bx1 + bw // 2, by1 + bh // 2), badge_text, fill=PRIMARY_NAVY, font=f_badge, anchor="mm")

draw.line([(50, 120), (W - 50, 120)], fill=(220, 228, 238, 255), width=2)

# 2. Main Title (y: 130 to 205)
draw.text((W // 2, 150), fa("چک‌لیست راه‌اندازی کارگاه تولید پیراشکی و سمبوسه"), fill=PRIMARY_NAVY, font=f_h1, anchor="mm")
draw.text((W // 2, 198), fa("حداقل پیش‌نیازهای راه‌اندازی یک خط تولید سودآور با دستگاه KBDM-150"), fill=TEAL_DARK, font=f_sub, anchor="mm")

# 3. Four Core Workshop Pillars (y: 228 to 860)
pillars = [
    ("حداقل فضای کارگاهی", "۱۵ تا ۲۵ متر مربع", "بدون نیاز به سوله یا تاسیسات سنگین", "مناسب کارگاه‌های شهری، آشپزخانه صنعتی یا مغازه"),
    ("برق و مصرف انرژی", "۲۲۰ ولت تک‌فاز شهری", "سازگار با برق معمولی شهری و کنتور کارگاهی", "فوق‌العاده کم‌مصرف با توان موتور فقط ۱.۸ کیلووات"),
    ("نیروی انسانی مورد نیاز", "فقط ۱ اپراتور ساده", "بدون نیاز به استخدام کارگر ماهر یا سرآشپز حرفه‌ای", "آموزش کامل کار با دستگاه و تمیزکاری در کمتر از ۲ ساعت"),
    ("ظرفیت فروش و سودآوری", "۲۰,۰۰۰ تا ۵۰,۰۰۰ عدد در روز", "تامین سفارشات فست‌فودها، هایپرمارکت‌ها و کترینگ‌ها", "سودآوری خالص ماهیانه از ۱۲۰ تا ۲۵۰ میلیون تومان")
]

card_w = (W - 130) // 2  # 475 px
card_h = 285
start_y = 230

for i, (title, highlight, d1, d2) in enumerate(pillars):
    col = 0 if (i % 2 == 0) else 1
    row = i // 2
    
    cx = (50 + card_w + 30) if (col == 0) else 50
    cy = start_y + row * (card_h + 20)
    
    draw.rounded_rectangle([(cx, cy), (cx + card_w, cy + card_h)], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.rounded_rectangle([(cx, cy), (cx + card_w, cy + 68)], radius=16, fill=BLUE_BG)
    draw.rectangle([(cx, cy + 45), (cx + card_w, cy + 68)], fill=BLUE_BG)
    
    draw.text((cx + card_w - 22, cy + 34), fa(title), fill=PRIMARY_NAVY, font=f_card_title, anchor="rm")
    draw.text((cx + card_w - 22, cy + 105), fa(highlight), fill=TEAL_DARK, font=f_card_sub, anchor="rm")
    
    draw.line([(cx + 25, cy + 138), (cx + card_w - 22, cy + 138)], fill=CARD_BORDER, width=1)
    
    # Custom drawn bullet dots
    dot1_y = cy + 175
    draw.ellipse([(cx + card_w - 28, dot1_y - 4), (cx + card_w - 20, dot1_y + 4)], fill=TEAL_DARK)
    draw.text((cx + card_w - 38, dot1_y), fa(d1), fill=PRIMARY_NAVY, font=f_card_desc1, anchor="rm")
    
    dot2_y = cy + 225
    draw.ellipse([(cx + card_w - 28, dot2_y - 4), (cx + card_w - 20, dot2_y + 4)], fill=TEXT_MUTED)
    draw.text((cx + card_w - 38, dot2_y), fa(d2), fill=TEXT_MUTED, font=f_card_desc2, anchor="rm")

# 4. Production Flow Architecture Diagram (y: 875 to 1230)
flow_y = 875
flow_h = 350
draw.rounded_rectangle([(50, flow_y), (W - 50, flow_y + flow_h)], radius=16, fill=(255, 255, 255, 255), outline=TEAL_DARK, width=2)

draw.text((W // 2, flow_y + 40), fa("چرخه کامل خط تولید پیراشکی و غذاهای خمیری نیمه‌آماده"), fill=PRIMARY_NAVY, font=f_flow_title, anchor="mm")
draw.line([(80, flow_y + 75), (W - 80, flow_y + 75)], fill=CARD_BORDER, width=1)

# 4 Step Boxes horizontally
steps = [
    ("مرحله ۱", "خمیرگیر صنعتی", "آماده‌سازی خمیر یکنواخت"),
    ("مرحله ۲", "دستگاه KBDM-150", "مغزی‌گذاری و فرم‌دهی"),
    ("مرحله ۳", "انجماد یا سرخ‌کن", "تثبیت بافت و شوک حرارتی"),
    ("مرحله ۴", "بسته‌بندی وکیوم", "عرضه به فروشگاه‌ها")
]

step_w = 210
step_h = 215
spacing = (W - 100 - (4 * step_w)) // 3

for idx, (s_num, s_name, s_desc) in enumerate(steps):
    sx = (W - 50 - step_w) - idx * (step_w + spacing)
    sy = flow_y + 100
    
    is_hero = (idx == 1)
    box_bg = (240, 252, 248, 255) if is_hero else BLUE_BG
    box_border = TEAL_DARK if is_hero else BLUE_BORDER
    
    draw.rounded_rectangle([(sx, sy), (sx + step_w, sy + step_h)], radius=12, fill=box_bg, outline=box_border, width=2 if is_hero else 1)
    
    draw.text((sx + step_w // 2, sy + 35), fa(s_num), fill=TEAL_DARK if is_hero else TEXT_MUTED, font=f_step_num, anchor="mm")
    draw.line([(sx + 20, sy + 65), (sx + step_w - 20, sy + 65)], fill=box_border, width=1)
    
    draw.text((sx + step_w // 2, sy + 110), fa(s_name), fill=PRIMARY_NAVY, font=f_step_name, anchor="mm")
    draw.text((sx + step_w // 2, sy + 165), fa(s_desc), fill=TEXT_MUTED if not is_hero else PRIMARY_NAVY, font=f_step_desc, anchor="mm")
    
    # Custom drawn vector arrow pointing LEFT (<-) in RTL flow
    if idx < len(steps) - 1:
        arrow_cx = sx - spacing // 2
        arrow_cy = sy + step_h // 2
        # Draw clean triangle arrow pointing left
        p1 = (arrow_cx - 8, arrow_cy)
        p2 = (arrow_cx + 8, arrow_cy - 9)
        p3 = (arrow_cx + 8, arrow_cy + 9)
        draw.polygon([p1, p2, p3], fill=TEAL_DARK)

# 5. Bottom CTA Bar (y: 1248 to 1324)
cta_y = 1248
draw.rounded_rectangle([(50, cta_y), (W - 50, cta_y + 76)], radius=14, fill=TEAL_DARK, outline=PRIMARY_NAVY, width=2)
draw.text((W // 2, cta_y + 38), fa("جهت دریافت پروپوزال فنی و جدول برآورد هزینه راه‌اندازی پیام دهید"), fill=(255, 255, 255, 255), font=f_cta, anchor="mm")

final_path = os.path.join(out_dir, "asset_07_workshop_setup.jpg")
canvas.convert("RGB").save(final_path, quality=98)

artifact_dest = r"C:\Users\Admin\.gemini\antigravity\brain\e3418149-99d4-42cc-a948-7446ed093103\asset_07_workshop_setup.jpg"
canvas.convert("RGB").save(artifact_dest, quality=98)

print("Generated asset_07_workshop_setup.jpg with polished dots and arrows successfully!")
