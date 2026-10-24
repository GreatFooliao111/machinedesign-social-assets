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

f_col_header = ImageFont.truetype(font_black, 28)
f_item_title = ImageFont.truetype(font_black, 22)
f_item_val = ImageFont.truetype(font_bold, 18)

f_roi_title = ImageFont.truetype(font_black, 26)
f_roi_val = ImageFont.truetype(font_bold, 20)

f_cta = ImageFont.truetype(font_black, 26)

PRIMARY_NAVY = (15, 28, 48, 255)
TEAL_DARK = (16, 78, 92, 255)
TEXT_MUTED = (85, 100, 115, 255)

RED_BG = (255, 246, 246, 255)
RED_BORDER = (245, 195, 195, 255)
RED_TEXT = (185, 40, 40, 255)

GREEN_BG = (246, 252, 246, 255)
GREEN_BORDER = (185, 230, 195, 255)
GREEN_TEXT = (25, 135, 60, 255)

GOLD_BG = (255, 251, 235, 255)
GOLD_BORDER = (235, 200, 120, 255)
GOLD_DARK = (160, 105, 10, 255)

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
draw.text((W // 2, 150), fa("مقایسه اقتصادی: تولید دستی در برابر صنعتی"), fill=PRIMARY_NAVY, font=f_h1, anchor="mm")
draw.text((W // 2, 198), fa("بررسی بازگشت سرمایه و کاهش ۸۵٪ هزینه‌های دستمزد کارگری"), fill=TEAL_DARK, font=f_sub, anchor="mm")

# 3. Two-Column Comparison (y: 228 to 938)
col_w = (W - 130) // 2  # 475 px
col_y = 228
col_h = 710

# In RTL Persian: Right column is column 1 (x = cx_right = 50 + col_w + 30 = 555)
# Left column is column 2 (x = 50)
cx_right = 50 + col_w + 30  # 555
cx_left = 50

# --- RIGHT COLUMN: روش سنتی و دستی (قرمز - مشکل) ---
draw.rounded_rectangle([(cx_right, col_y), (cx_right + col_w, col_y + col_h)], radius=16, fill=RED_BG, outline=RED_BORDER, width=2)
draw.rounded_rectangle([(cx_right, col_y), (cx_right + col_w, col_y + 68)], radius=16, fill=(250, 225, 225, 255))
draw.rectangle([(cx_right, col_y + 45), (cx_right + col_w, col_y + 68)], fill=(250, 225, 225, 255))
draw.text((cx_right + col_w // 2, col_y + 34), fa("روش سنتی و دستی ❌"), fill=RED_TEXT, font=f_col_header, anchor="mm")

items_manual = [
    ("نیروی انسانی مورد نیاز", "۶ تا ۸ کارگر ماهر و تمام‌وقت"),
    ("هزینه ماهانه دستمزد", "بیش از ۱۲۰ میلیون تومان ماهانه"),
    ("سرعت و ظرفیت تولید", "حداکثر ۵۰۰ تا ۸۰۰ عدد در ساعت"),
    ("نرخ دورریز و ضایعات خمیر", "۸٪ تا ۱۲٪ به علت خطای انسانی"),
    ("یکنواختی وزن و ظاهر", "تغییر شکل و ضخامت غیریکنواخت"),
    ("استاندارد بهداشت و سلامت", "تماس مکرر دست با مواد و خمیر")
]

item_spacing = 100
for idx, (title, val) in enumerate(items_manual):
    iy = col_y + 90 + idx * item_spacing
    draw.text((cx_right + col_w - 20, iy), fa(title), fill=RED_TEXT, font=f_item_title, anchor="rm")
    draw.text((cx_right + col_w - 20, iy + 32), fa(val), fill=PRIMARY_NAVY, font=f_item_val, anchor="rm")
    if idx < len(items_manual) - 1:
        draw.line([(cx_right + 20, iy + 62), (cx_right + col_w - 20, iy + 62)], fill=(240, 210, 210, 255), width=1)

# --- LEFT COLUMN: خط صنعتی KBDM-150 (سبز - راهکار نجات‌بخش) ---
draw.rounded_rectangle([(cx_left, col_y), (cx_left + col_w, col_y + col_h)], radius=16, fill=GREEN_BG, outline=GREEN_BORDER, width=2)
draw.rounded_rectangle([(cx_left, col_y), (cx_left + col_w, col_y + 68)], radius=16, fill=(225, 248, 230, 255))
draw.rectangle([(cx_left, col_y + 45), (cx_left + col_w, col_y + 68)], fill=(225, 248, 230, 255))
draw.text((cx_left + col_w // 2, col_y + 34), fa("خط صنعتی KBDM-150 ✅"), fill=GREEN_TEXT, font=f_col_header, anchor="mm")

items_auto = [
    ("نیروی انسانی مورد نیاز", "فقط ۱ اپراتور ساده و آموزش‌پذیر"),
    ("صرفه‌جویی دستمزد ماهانه", "بیش از ۹۵ میلیون تومان پس‌انداز خالص"),
    ("سرعت و ظرفیت تولید", "تا ۱۰,۰۰۰ عدد در ساعت (۱۲ برابر!)"),
    ("نرخ دورریز و ضایعات خمیر", "کمتر از ۱٪ با نورد غلتکی یکنواخت"),
    ("یکنواختی وزن و ظاهر", "فرم بی‌نقص مشابه ظاهر دست‌ساز"),
    ("استاندارد بهداشت و سلامت", "استنلس استیل ۳۰۴ بدون دخالت دست")
]

for idx, (title, val) in enumerate(items_auto):
    iy = col_y + 90 + idx * item_spacing
    draw.text((cx_left + col_w - 20, iy), fa(title), fill=GREEN_TEXT, font=f_item_title, anchor="rm")
    draw.text((cx_left + col_w - 20, iy + 32), fa(val), fill=PRIMARY_NAVY, font=f_item_val, anchor="rm")
    if idx < len(items_auto) - 1:
        draw.line([(cx_left + 20, iy + 62), (cx_left + col_w - 20, iy + 62)], fill=(210, 235, 215, 255), width=1)

# 4. Golden ROI Highlight Box (y: 955 to 1230)
gold_y = 955
gold_h = 275
draw.rounded_rectangle([(50, gold_y), (W - 50, gold_y + gold_h)], radius=16, fill=GOLD_BG, outline=GOLD_BORDER, width=2)

draw.text((W // 2, gold_y + 36), fa("نتیجه تحلیل مالی و بازگشت سرمایه‌گذاری (ROI)"), fill=GOLD_DARK, font=f_roi_title, anchor="mm")
draw.line([(80, gold_y + 68), (W - 80, gold_y + 68)], fill=GOLD_BORDER, width=1)

roi_points = [
    "مدت زمان بازگشت کامل هزینه خرید دستگاه: کمتر از ۹۰ روز کاری (۳ ماه)",
    "صرفه‌جویی سالانه از محل کاهش نیروی کارگری: بیش از ۱.۱ میلیارد تومان",
    "جهش تیراژ تولید به ۱۰,۰۰۰ عدد در ساعت: امکان عقد قرارداد با فروشگاه‌های زنجیره‌ای"
]

for idx, pt in enumerate(roi_points):
    ry = gold_y + 104 + idx * 48
    draw.text((W // 2, ry), fa(pt), fill=PRIMARY_NAVY, font=f_roi_val, anchor="mm")

# 5. Bottom CTA Bar (y: 1248 to 1324)
cta_y = 1248
draw.rounded_rectangle([(50, cta_y), (W - 50, cta_y + 76)], radius=14, fill=TEAL_DARK, outline=PRIMARY_NAVY, width=2)
draw.text((W // 2, cta_y + 38), fa("جهت دریافت جدول اکسل بیزینس‌پلن و استعلام در دایرکت پیام دهید"), fill=(255, 255, 255, 255), font=f_cta, anchor="mm")

final_path = os.path.join(out_dir, "asset_05_roi_comparison.jpg")
canvas.convert("RGB").save(final_path, quality=98)

artifact_dest = r"C:\Users\Admin\.gemini\antigravity\brain\e3418149-99d4-42cc-a948-7446ed093103\asset_05_roi_comparison.jpg"
canvas.convert("RGB").save(artifact_dest, quality=98)

print("Generated asset_05_roi_comparison.jpg successfully!")
