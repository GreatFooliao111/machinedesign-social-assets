import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import arabic_reshaper
from bidi.algorithm import get_display

def fa(text):
    if not text:
        return ""
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

base_dir = r"D:\Machinedesign.ir\social-content\launch-dumpling-series"
out_dir = os.path.join(base_dir, "02_generated_visuals")
os.makedirs(out_dir, exist_ok=True)

font_dir = r"C:\Users\Admin\.gemini\config\skills\machinedesign-artifact-designer\resources\fonts"
font_black = os.path.join(font_dir, "Vazirmatn-Black.ttf")
font_bold = os.path.join(font_dir, "Vazirmatn-Bold.ttf")
font_med = os.path.join(font_dir, "Vazirmatn-Medium.ttf")
font_orbitron = os.path.join(font_dir, "Orbitron.ttf")

master_img_path = os.path.join(base_dir, "01_source_material", "images", "konbrit_150_source_02.png")
logo_path = r"D:\Machinedesign.ir\branding\logos\logo_horizontal_md_machinedesign.png"

# Canvas: 1080 x 1350
W, H = 1080, 1350
canvas = Image.new("RGBA", (W, H), (10, 12, 16, 255))
draw = ImageDraw.Draw(canvas)

f_brand_tag = ImageFont.truetype(font_orbitron, 20)
f_h1 = ImageFont.truetype(font_black, 48)
f_sub = ImageFont.truetype(font_bold, 25)
f_spec_val = ImageFont.truetype(font_black, 30)
f_spec_lbl = ImageFont.truetype(font_bold, 20)
f_spec_desc = ImageFont.truetype(font_med, 17)
f_cta = ImageFont.truetype(font_black, 26)

NEON = (140, 231, 12, 255)
WHITE = (255, 255, 255, 255)
MUTED = (160, 170, 180, 255)
CARD_BG = (18, 23, 30, 250)
CARD_BORDER = (40, 52, 68, 255)
CARD_BORDER_NEON = (140, 231, 12, 220)

# Subtle background grid
for x in range(0, W, 70):
    draw.line([(x, 0), (x, H)], fill=(22, 28, 36, 255), width=1)
for y in range(0, H, 70):
    draw.line([(0, y), (W, y)], fill=(22, 28, 36, 255), width=1)

# Header Bar
if os.path.exists(logo_path):
    logo = Image.open(logo_path).convert("RGBA")
    lh = 46
    lw = int(logo.width * (lh / logo.height))
    logo = logo.resize((lw, lh), Image.Resampling.LANCZOS)
    canvas.paste(logo, (50, 45), logo)

# Badge
draw.rounded_rectangle([(W - 250, 45), (W - 50, 92)], radius=8, fill=(16, 22, 28, 255), outline=CARD_BORDER_NEON, width=2)
draw.text((W - 150, 68), "MODEL: KBDM-150", fill=NEON, font=f_brand_tag, anchor="mm")

# Title Section
draw.text((W // 2, 145), fa("دستگاه اتوماتیک تولید پیراشکی و سمبوسه"), fill=WHITE, font=f_h1, anchor="mm")
draw.text((W // 2, 200), fa("ظرفیت ۸,۰۰۰ تا ۱۰,۰۰۰ عدد در ساعت | استنلس استیل ۳۰۴"), fill=NEON, font=f_sub, anchor="mm")

# Prepare Transparent Cutout of Machine 02
if os.path.exists(master_img_path):
    mach = Image.open(master_img_path).convert("RGBA")
    
    # Remove white background: convert pixels near white to transparent
    datas = mach.getdata()
    new_data = []
    for item in datas:
        # Check if near white
        if item[0] > 235 and item[1] > 235 and item[2] > 235:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    mach.putdata(new_data)
    
    # Crop to content
    bbox = mach.getbbox()
    if bbox:
        mach = mach.crop(bbox)
        
    # Scale to height 540
    target_h = 550
    target_w = int(mach.width * (target_h / mach.height))
    mach = mach.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Paste centered
    paste_x = (W - target_w) // 2
    paste_y = 240
    canvas.paste(mach, (paste_x, paste_y), mach)

# Engineering Spec Cards
specs = [
    ("ظرفیت اسمی خروجی", "۱۰,۰۰۰ عدد/ساعت", "خروجی مداوم با کانوایر"),
    ("موتور و برق مصرفی", "۱.۸ کیلووات (۲۲۰/۳۸۰V)", "سازگار با برق شهری/کارگاهی"),
    ("سیستم فرم‌دهی خمیر", "غلتک دوبل متوالی", "حفظ بافت سنتی دست‌ساز"),
    ("کاربرد چندمنظوره", "۵ قالب تعویض‌پذیر", "سمبوسه، پیراشکی، کلمپه، جوشباره")
]

card_w = (W - 130) // 2
card_h = 135
start_y = 825

for i, (lbl, val, desc) in enumerate(specs):
    col = i % 2
    row = i // 2
    cx = 50 + col * (card_w + 30)
    cy = start_y + row * (card_h + 20)
    
    # Draw card box
    draw.rounded_rectangle([(cx, cy), (cx + card_w, cy + card_h)], radius=12, fill=CARD_BG, outline=CARD_BORDER, width=2)
    # Accent vertical line on right edge
    draw.line([(cx + card_w - 6, cy + 22), (cx + card_w - 6, cy + card_h - 22)], fill=NEON, width=4)
    
    draw.text((cx + card_w - 24, cy + 35), fa(val), fill=WHITE, font=f_spec_val, anchor="rm")
    draw.text((cx + card_w - 24, cy + 75), fa(lbl), fill=NEON, font=f_spec_lbl, anchor="rm")
    draw.text((cx + card_w - 24, cy + 105), fa(desc), fill=MUTED, font=f_spec_desc, anchor="rm")

# Bottom CTA Bar
cta_y = 1170
draw.rounded_rectangle([(50, cta_y), (W - 50, cta_y + 95)], radius=16, fill=(16, 28, 20, 255), outline=CARD_BORDER_NEON, width=2)
draw.text((W // 2, cta_y + 47), fa("📩 جهت استعلام قیمت و دریافت کاتالوگ در دایرکت پیام دهید"), fill=WHITE, font=f_cta, anchor="mm")

# Save Output
final_path = os.path.join(out_dir, "sample_poster_kbdm150_official.jpg")
canvas.convert("RGB").save(final_path, quality=95)

artifact_dest = r"C:\Users\Admin\.gemini\antigravity\brain\e3418149-99d4-42cc-a948-7446ed093103\sample_poster_kbdm150_official.jpg"
canvas.convert("RGB").save(artifact_dest, quality=95)
print("Updated official poster saved.")
