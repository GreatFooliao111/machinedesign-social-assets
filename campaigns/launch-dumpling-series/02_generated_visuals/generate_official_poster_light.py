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

tight_crop_path = os.path.join(base_dir, "01_source_material", "images", "konbrit_150_tight_crop.png")
logo_sym_path = r"D:\Machinedesign.ir\branding\logos\logo_symbol_md_metallic_transparent.png"

# Canvas: 1080 x 1350 - Pure White
W, H = 1080, 1350
canvas = Image.new("RGBA", (W, H), (255, 255, 255, 255))
draw = ImageDraw.Draw(canvas)

f_brand_title = ImageFont.truetype(font_segoe_bold, 36)
f_brand_sub = ImageFont.truetype(font_bold, 20)
f_badge = ImageFont.truetype(font_segoe_bold, 22)

f_h1 = ImageFont.truetype(font_black, 50)
f_sub = ImageFont.truetype(font_bold, 25)

f_spec_val = ImageFont.truetype(font_black, 32)
f_spec_lbl = ImageFont.truetype(font_black, 23)
f_spec_desc = ImageFont.truetype(font_bold, 19)

f_cta = ImageFont.truetype(font_black, 28)

PRIMARY_NAVY = (12, 28, 48, 255)
TEAL_DARK = (16, 78, 92, 255)
TEXT_MUTED = (80, 95, 110, 255)
CARD_BG = (246, 249, 252, 255)
CARD_BORDER = (210, 220, 232, 255)

# 1. Header (y: 20 to 118)
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
draw.text((W // 2, 150), fa("دستگاه اتوماتیک تولید پیراشکی و سمبوسه"), fill=PRIMARY_NAVY, font=f_h1, anchor="mm")
draw.text((W // 2, 200), fa("ظرفیت ۸,۰۰۰ تا ۱۰,۰۰۰ عدد در ساعت  |  استاندارد استیل ۳۰۴ غذایی"), fill=TEAL_DARK, font=f_sub, anchor="mm")

# 3. Position Machine: Tightly cropped, HIGHER & SHIFTED LEFT, MAXIMUM SIZE
# Vertical available: 215 to 995
target_h = 765
mach = Image.open(tight_crop_path).convert("RGBA")
target_w = int(mach.width * (target_h / mach.height))
mach = mach.resize((target_w, target_h), Image.Resampling.LANCZOS)

# paste_x shifted left: center would be (1080 - target_w)//2 ~ 128.
# Shifting left to 70 brings the conveyor nicely to the left edge and centers the heavy body!
paste_x = 75
paste_y = 222
canvas.paste(mach, (paste_x, paste_y), mach)

# 4. Spec Cards (y: 1005 to 1235)
specs = [
    ("ظرفیت اسمی خروجی", "۱۰,۰۰۰ عدد/ساعت", "خروجی مداوم با کانوایر اتوماتیک"),
    ("موتور و برق مصرفی", "۱.۸ کیلووات (۲۲۰/۳۸۰V)", "سازگار با برق تک‌فاز شهری و کارگاهی"),
    ("سیستم فرم‌دهی خمیر", "غلتک دوبل متوالی", "حفظ بافت دست‌ساز و کشسانی خمیر"),
    ("کاربرد چندمنظوره", "۵ قالب تعویض‌پذیر", "سمبوسه، پیراشکی، کلمپه، جوشباره")
]

card_w = (W - 130) // 2
card_h = 110
start_y = 1005

for i, (lbl, val, desc) in enumerate(specs):
    col = i % 2
    row = i // 2
    cx = 50 + col * (card_w + 30)
    cy = start_y + row * (card_h + 12)
    
    draw.rounded_rectangle([(cx, cy), (cx + card_w, cy + card_h)], radius=12, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.line([(cx + card_w - 6, cy + 16), (cx + card_w - 6, cy + card_h - 16)], fill=TEAL_DARK, width=6)
    
    draw.text((cx + card_w - 22, cy + 28), fa(val), fill=PRIMARY_NAVY, font=f_spec_val, anchor="rm")
    draw.text((cx + card_w - 22, cy + 62), fa(lbl), fill=TEAL_DARK, font=f_spec_lbl, anchor="rm")
    draw.text((cx + card_w - 22, cy + 88), fa(desc), fill=PRIMARY_NAVY, font=f_spec_desc, anchor="rm")

# 5. Bottom CTA Bar (y: 1245 to 1325)
cta_y = 1248
draw.rounded_rectangle([(50, cta_y), (W - 50, cta_y + 76)], radius=14, fill=TEAL_DARK, outline=PRIMARY_NAVY, width=2)
draw.text((W // 2, cta_y + 38), fa("📩 جهت استعلام قیمت و دریافت کاتالوگ در دایرکت پیام دهید"), fill=(255, 255, 255, 255), font=f_cta, anchor="mm")

# Save outputs
final_path = os.path.join(out_dir, "sample_poster_kbdm150_official.jpg")
canvas.convert("RGB").save(final_path, quality=98)

artifact_dest = r"C:\Users\Admin\.gemini\antigravity\brain\e3418149-99d4-42cc-a948-7446ed093103\sample_poster_kbdm150_official.jpg"
canvas.convert("RGB").save(artifact_dest, quality=98)

print("Generated tight-crop higher & left poster successfully.")
