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
tight_crop_path = os.path.join(base_dir, "01_source_material", "images", "konbrit_150_tight_crop.png")

W, H = 1080, 1350
canvas = Image.new("RGBA", (W, H), (255, 255, 255, 255))
draw = ImageDraw.Draw(canvas)

f_brand_title = ImageFont.truetype(font_segoe_bold, 36)
f_brand_sub = ImageFont.truetype(font_bold, 20)
f_badge = ImageFont.truetype(font_segoe_bold, 22)

f_h1 = ImageFont.truetype(font_black, 48)
f_sub = ImageFont.truetype(font_bold, 24)

f_card_title = ImageFont.truetype(font_black, 23)
f_card_sub = ImageFont.truetype(font_bold, 18)
f_card_desc = ImageFont.truetype(font_med, 17)

f_callout = ImageFont.truetype(font_bold, 17)
f_cta = ImageFont.truetype(font_black, 26)

PRIMARY_NAVY = (15, 28, 48, 255)
TEAL_DARK = (16, 78, 92, 255)
TEXT_MUTED = (80, 95, 110, 255)
CARD_BG = (248, 250, 252, 255)
CARD_BORDER = (215, 226, 238, 255)

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
draw.text((W // 2, 150), fa("سیستم نورد دوبل متوالی و فرم‌دهی خمیر"), fill=PRIMARY_NAVY, font=f_h1, anchor="mm")
draw.text((W // 2, 198), fa("تکنولوژی حفظ بافت دست‌ساز، کشسانی و عدم پارگی شبکه گلوتن خمیر"), fill=TEAL_DARK, font=f_sub, anchor="mm")

# 3. Machine Hero Visual (y: 220 to 730)
target_h = 475
mach = Image.open(tight_crop_path).convert("RGBA")
target_w = int(mach.width * (target_h / mach.height))
mach = mach.resize((target_w, target_h), Image.Resampling.LANCZOS)
paste_x = (W - target_w) // 2 + 5
paste_y = 225
canvas.paste(mach, (paste_x, paste_y), mach)

# Symmetrical Architectural Callout Badges with Clean Leader Lines
# Left Badges
left_callouts = [
    ("قیف استیل تزریق مواد میانی", 280, (paste_x + 65, 305)),
    ("قالب مدولار فرم‌دهی بدون درز", 435, (paste_x + 90, 460))
]

for label, by, (target_px, target_py) in left_callouts:
    bx1 = 40
    bx2 = 295
    draw.rounded_rectangle([(bx1, by), (bx2, by + 50)], radius=10, fill=(255, 255, 255, 248), outline=TEAL_DARK, width=2)
    draw.text(((bx1 + bx2) // 2, by + 25), fa(label), fill=PRIMARY_NAVY, font=f_callout, anchor="mm")
    
    line_start = (bx2, by + 25)
    draw.line([line_start, (target_px, target_py)], fill=TEAL_DARK, width=2)
    draw.ellipse([(target_px - 4, target_py - 4), (target_px + 4, target_py + 4)], fill=TEAL_DARK, outline=(255, 255, 255, 255), width=2)

# Right Badges
right_callouts = [
    ("غلتک‌های نورد پیوسته خمیر", 280, (paste_x + 295, 305)),
    ("پنل کنترل سرعت اینورتوردار", 435, (paste_x + 360, 460))
]

for label, by, (target_px, target_py) in right_callouts:
    bx1 = W - 295
    bx2 = W - 40
    draw.rounded_rectangle([(bx1, by), (bx2, by + 50)], radius=10, fill=(255, 255, 255, 248), outline=TEAL_DARK, width=2)
    draw.text(((bx1 + bx2) // 2, by + 25), fa(label), fill=PRIMARY_NAVY, font=f_callout, anchor="mm")
    
    line_start = (bx1, by + 25)
    draw.line([line_start, (target_px, target_py)], fill=TEAL_DARK, width=2)
    draw.ellipse([(target_px - 4, target_py - 4), (target_px + 4, target_py + 4)], fill=TEAL_DARK, outline=(255, 255, 255, 255), width=2)

# 4. Four Detailed Technical Feature Cards (y: 755 to 1230)
features = [
    ("۰۱", "نورد غلتکی چندمرحله‌ای", "حفظ کشسانی و عدم ایجاد تنش حرارتی در بافت خمیر", "جلوگیری از لاستیکی شدن خمیر و حفظ تردی پس از پخت"),
    ("۰۲", "تنظیم میکرومتری ضخامت", "پیچ‌های ورنیه‌دار تنظیم فاصله بین ۰.۵ تا ۳ میلی‌متر", "انطباق دقیق با خمیرهای نازک پیراشکی، سمبوسه یا کلمپه"),
    ("۰۳", "سیستم تزریق فیلینگ دقیق", "پشتیبانی از انواع مغزی‌های مرطوب، گوشتی و خرمایی", "تنظیم وزن مواد میانی از ۵ تا ۳۵ گرم با خطای زیر ۰.۵ گرم"),
    ("۰۴", "سیستم دوخت پرس مکانیکی", "قالب‌های آلیاژی استیل با استاندارد بهداشتی ۳۰۴", "دوخت محکم و فرم‌دار لبه‌ها بدون وا رفتن در سرخ‌کن یا فر")
]

card_w = (W - 130) // 2  # 475 px
card_h = 225
start_y = 755

for i, (num, title, sub, desc) in enumerate(features):
    col = 0 if (i % 2 == 0) else 1
    row = i // 2
    
    cx = (50 + card_w + 30) if (col == 0) else 50
    cy = start_y + row * (card_h + 15)
    
    draw.rounded_rectangle([(cx, cy), (cx + card_w, cy + card_h)], radius=14, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.line([(cx + card_w - 6, cy + 18), (cx + card_w - 6, cy + card_h - 18)], fill=TEAL_DARK, width=6)
    
    draw.text((cx + card_w - 22, cy + 34), fa(f"{num} . {title}"), fill=PRIMARY_NAVY, font=f_card_title, anchor="rm")
    draw.text((cx + card_w - 22, cy + 85), fa(sub), fill=TEAL_DARK, font=f_card_sub, anchor="rm")
    draw.text((cx + card_w - 22, cy + 145), fa(desc), fill=TEXT_MUTED, font=f_card_desc, anchor="rm")

# 5. Bottom CTA Bar (y: 1248 to 1324)
cta_y = 1248
draw.rounded_rectangle([(50, cta_y), (W - 50, cta_y + 76)], radius=14, fill=TEAL_DARK, outline=PRIMARY_NAVY, width=2)
draw.text((W // 2, cta_y + 38), fa("جهت هماهنگی تست حضوری کارکرد با خمیر اختصاصی شما پیام دهید"), fill=(255, 255, 255, 255), font=f_cta, anchor="mm")

final_path = os.path.join(out_dir, "asset_06_roller_mechanism.jpg")
canvas.convert("RGB").save(final_path, quality=98)

artifact_dest = r"C:\Users\Admin\.gemini\antigravity\brain\e3418149-99d4-42cc-a948-7446ed093103\asset_06_roller_mechanism.jpg"
canvas.convert("RGB").save(artifact_dest, quality=98)

print("Generated asset_06_roller_mechanism.jpg with symmetrical callouts successfully!")
