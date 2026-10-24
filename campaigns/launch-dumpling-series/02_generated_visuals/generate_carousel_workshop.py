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
out_dir = os.path.join(base_dir, "02_generated_visuals", "carousel_workshop")
os.makedirs(out_dir, exist_ok=True)

artifact_dir = r"C:\Users\Admin\.gemini\antigravity\brain\e3418149-99d4-42cc-a948-7446ed093103"

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

# Fonts
f_brand_title = ImageFont.truetype(font_segoe_bold, 36)
f_brand_sub = ImageFont.truetype(font_bold, 20)
f_badge = ImageFont.truetype(font_segoe_bold, 22)

f_h1_cover = ImageFont.truetype(font_black, 52)
f_h2_cover = ImageFont.truetype(font_bold, 26)

f_h1_slide = ImageFont.truetype(font_black, 44)
f_sub_slide = ImageFont.truetype(font_bold, 22)

f_card_title = ImageFont.truetype(font_black, 26)
f_card_sub = ImageFont.truetype(font_bold, 22)
f_card_desc = ImageFont.truetype(font_med, 18)

f_flow_title = ImageFont.truetype(font_black, 25)
f_step_num = ImageFont.truetype(font_black, 20)
f_step_name = ImageFont.truetype(font_bold, 18)
f_step_desc = ImageFont.truetype(font_med, 15)

f_swipe = ImageFont.truetype(font_black, 22)
f_cta = ImageFont.truetype(font_black, 26)

PRIMARY_NAVY = (15, 28, 48, 255)
TEAL_DARK = (16, 78, 92, 255)
TEXT_MUTED = (85, 100, 115, 255)

CARD_BG = (248, 250, 252, 255)
CARD_BORDER = (215, 226, 238, 255)
BLUE_BG = (244, 248, 254, 255)
BLUE_BORDER = (195, 218, 248, 255)

def draw_header(canvas, draw, slide_num=None):
    if os.path.exists(logo_sym_path):
        sym = Image.open(logo_sym_path).convert("RGBA")
        sh = 88
        sw = int(sym.width * (sh / sym.height))
        sym = sym.resize((sw, sh), Image.Resampling.LANCZOS)
        canvas.paste(sym, (50, 20), sym)
        
        draw.text((50 + sw + 18, 28), "MachineDesign.ir", fill=TEAL_DARK, font=f_brand_title)
        draw.text((50 + sw + 20, 72), fa("مرکز تخصصی ماشین‌آلات صنایع غذایی"), fill=TEXT_MUTED, font=f_brand_sub)
    
    badge_text = f"SLIDE {slide_num}/3" if slide_num else "MODEL: KBDM-150"
    bbox_badge = draw.textbbox((0, 0), badge_text, font=f_badge)
    bw = bbox_badge[2] - bbox_badge[0] + 40
    bh = 46
    bx1 = W - 50 - bw
    by1 = 40
    draw.rounded_rectangle([(bx1, by1), (W - 50, by1 + bh)], radius=10, fill=(244, 248, 252, 255), outline=TEAL_DARK, width=2)
    draw.text((bx1 + bw // 2, by1 + bh // 2), badge_text, fill=PRIMARY_NAVY, font=f_badge, anchor="mm")
    
    draw.line([(50, 118), (W - 50, 118)], fill=(225, 232, 240, 255), width=2)

def draw_swipe_pill(draw, text, y=1240):
    fa_txt = fa(text)
    bbox = draw.textbbox((0, 0), fa_txt, font=f_swipe)
    pw = (bbox[2] - bbox[0]) + 60
    draw.rounded_rectangle([(W // 2 - pw // 2, y), (W // 2 + pw // 2, y + 60)], radius=30, fill=PRIMARY_NAVY)
    draw.text((W // 2, y + 30), fa_txt, fill=(255, 255, 255, 255), font=f_swipe, anchor="mm")

# ==========================================================
# SLIDE 1: COVER (Visual Hook)
# ==========================================================
c1 = Image.new("RGBA", (W, H), (255, 255, 255, 255))
d1 = ImageDraw.Draw(c1)
draw_header(c1, d1, slide_num=1)

d1.text((W // 2, 160), fa("راهنمای صفر تا صد راه‌اندازی کارگاه"), fill=PRIMARY_NAVY, font=f_h1_cover, anchor="mm")
d1.text((W // 2, 225), fa("تولید پیراشکی، سمبوسه و کلمپه صنعتی"), fill=TEAL_DARK, font=f_h1_cover, anchor="mm")
d1.text((W // 2, 285), fa("حداقل فضا، برق و سرمایه مورد نیاز برای شروع یک کسب‌وکار پرسود"), fill=TEXT_MUTED, font=f_h2_cover, anchor="mm")

if os.path.exists(tight_crop_path):
    target_h = 750
    mach = Image.open(tight_crop_path).convert("RGBA")
    target_w = int(mach.width * (target_h / mach.height))
    mach = mach.resize((target_w, target_h), Image.Resampling.LANCZOS)
    paste_x = (W - target_w) // 2 + 10
    paste_y = 350
    c1.paste(mach, (paste_x, paste_y), mach)

draw_swipe_pill(d1, "ورق بزنید  ◀")

s1_path = os.path.join(out_dir, "carousel_workshop_slide_01.jpg")
c1.convert("RGB").save(s1_path, quality=98)
c1.convert("RGB").save(os.path.join(artifact_dir, "carousel_workshop_slide_01.jpg"), quality=98)

# ==========================================================
# SLIDE 2: 4 CORE REQUIREMENTS (Spacious & Clean)
# ==========================================================
c2 = Image.new("RGBA", (W, H), (255, 255, 255, 255))
d2 = ImageDraw.Draw(c2)
draw_header(c2, d2, slide_num=2)

d2.text((W // 2, 165), fa("۴ پیش‌نیاز کلیدی راه‌اندازی کارگاه"), fill=PRIMARY_NAVY, font=f_h1_slide, anchor="mm")
d2.text((W // 2, 218), fa("بررسی زیرساخت، برق و نیروی انسانی مورد نیاز دستگاه KBDM-150"), fill=TEAL_DARK, font=f_sub_slide, anchor="mm")

pillars = [
    ("حداقل فضای کارگاهی", "۱۵ تا ۲۵ متر مربع", "مناسب کارگاه شهری یا آشپزخانه صنعتی", "بدون نیاز به سوله یا تاسیسات سنگین"),
    ("برق و مصرف انرژی", "۲۲۰ ولت تک‌فاز خانگی", "سازگار با کنتور برق شهری و کارگاهی", "فوق‌العاده کم‌مصرف با توان موتور ۱.۸ کیلووات"),
    ("نیروی انسانی مورد نیاز", "فقط ۱ اپراتور ساده", "بدون نیاز به استخدام نیروی ماهر یا قناد", "آموزش کامل کاربری دستگاه در کمتر از ۲ ساعت"),
    ("ظرفیت فروش و سودآوری", "۲۰,۰۰۰ عدد روزانه", "تامین سفارشات فست‌فودها و فروشگاه‌ها", "سود خالص ماهانه ۱۲۰ تا ۲۵۰ میلیون تومان")
]

card_w = (W - 130) // 2  # 475 px
card_h = 420
start_y = 265

for i, (title, highlight, b1, b2) in enumerate(pillars):
    col = 0 if (i % 2 == 0) else 1
    row = i // 2
    
    cx = (50 + card_w + 30) if (col == 0) else 50
    cy = start_y + row * (card_h + 35)
    
    d2.rounded_rectangle([(cx, cy), (cx + card_w, cy + card_h)], radius=18, fill=CARD_BG, outline=CARD_BORDER, width=2)
    d2.rounded_rectangle([(cx, cy), (cx + card_w, cy + 76)], radius=18, fill=BLUE_BG)
    d2.rectangle([(cx, cy + 50), (cx + card_w, cy + 76)], fill=BLUE_BG)
    
    d2.text((cx + card_w - 24, cy + 38), fa(f"۰{i+1} . {title}"), fill=PRIMARY_NAVY, font=f_card_title, anchor="rm")
    d2.text((cx + card_w - 24, cy + 130), fa(highlight), fill=TEAL_DARK, font=f_card_sub, anchor="rm")
    
    d2.line([(cx + 25, cy + 175), (cx + card_w - 25, cy + 175)], fill=CARD_BORDER, width=1)
    
    # Clean Bullet lines
    d2.text((cx + card_w - 25, cy + 225), fa("✦  " + b1), fill=PRIMARY_NAVY, font=f_card_desc, anchor="rm")
    d2.text((cx + card_w - 25, cy + 285), fa("✦  " + b2), fill=TEXT_MUTED, font=f_card_desc, anchor="rm")

draw_swipe_pill(d2, "ورق بزنید: چرخه خط تولید  ◀")

s2_path = os.path.join(out_dir, "carousel_workshop_slide_02.jpg")
c2.convert("RGB").save(s2_path, quality=98)
c2.convert("RGB").save(os.path.join(artifact_dir, "carousel_workshop_slide_02.jpg"), quality=98)

# ==========================================================
# SLIDE 3: PRODUCTION FLOW & CTA
# ==========================================================
c3 = Image.new("RGBA", (W, H), (255, 255, 255, 255))
d3 = ImageDraw.Draw(c3)
draw_header(c3, d3, slide_num=3)

d3.text((W // 2, 165), fa("چرخه کامل خط تولید پیراشکی صنعتی"), fill=PRIMARY_NAVY, font=f_h1_slide, anchor="mm")
d3.text((W // 2, 218), fa("۴ گام استاندارد از خمیرگیری تا بسته‌بندی نهایی"), fill=TEAL_DARK, font=f_sub_slide, anchor="mm")

# Flow Box
d3.rounded_rectangle([(60, 265), (W - 60, 660)], radius=20, fill=(255, 255, 255, 255), outline=TEAL_DARK, width=2)
d3.text((W // 2, 315), fa("چیدمان پیوسته تجهیزات در کارگاه"), fill=PRIMARY_NAVY, font=f_flow_title, anchor="mm")
d3.line([(100, 355), (W - 100, 355)], fill=CARD_BORDER, width=1)

steps = [
    ("مرحله ۱", "خمیرگیر صنعتی", "آماده‌سازی یکنواخت خمیر"),
    ("مرحله ۲", "دستگاه KBDM-150", "مغزی‌گذاری و فرم‌دهی"),
    ("مرحله ۳", "انجماد یا سرخ‌کن", "تثبیت بافت و فرم لبه‌ها"),
    ("مرحله ۴", "بسته‌بندی وکیوم", "عرضه به فروشگاه‌ها")
]

step_w = 205
step_h = 220
spacing = (W - 120 - (4 * step_w)) // 3

for idx, (s_num, s_name, s_desc) in enumerate(steps):
    sx = (W - 60 - step_w) - idx * (step_w + spacing)
    sy = 390
    
    is_hero = (idx == 1)
    box_bg = (240, 252, 248, 255) if is_hero else BLUE_BG
    box_border = TEAL_DARK if is_hero else BLUE_BORDER
    
    d3.rounded_rectangle([(sx, sy), (sx + step_w, sy + step_h)], radius=12, fill=box_bg, outline=box_border, width=2 if is_hero else 1)
    
    d3.text((sx + step_w // 2, sy + 38), fa(s_num), fill=TEAL_DARK if is_hero else TEXT_MUTED, font=f_step_num, anchor="mm")
    d3.line([(sx + 15, sy + 70), (sx + step_w - 15, sy + 70)], fill=box_border, width=1)
    
    d3.text((sx + step_w // 2, sy + 115), fa(s_name), fill=PRIMARY_NAVY, font=f_step_name, anchor="mm")
    d3.text((sx + step_w // 2, sy + 168), fa(s_desc), fill=TEXT_MUTED if not is_hero else PRIMARY_NAVY, font=f_step_desc, anchor="mm")
    
    if idx < len(steps) - 1:
        arrow_cx = sx - spacing // 2
        arrow_cy = sy + step_h // 2
        p1 = (arrow_cx - 8, arrow_cy)
        p2 = (arrow_cx + 8, arrow_cy - 9)
        p3 = (arrow_cx + 8, arrow_cy + 9)
        d3.polygon([p1, p2, p3], fill=TEAL_DARK)

# Workshop Consulting Box
d3.rounded_rectangle([(60, 700), (W - 60, 1180)], radius=20, fill=(244, 248, 254, 255), outline=TEAL_DARK, width=2)
d3.text((W // 2, 770), fa("می‌خواهید کارگاه اختصاصی خود را راه‌اندازی کنید؟"), fill=PRIMARY_NAVY, font=ImageFont.truetype(font_black, 32), anchor="mm")
d3.text((W // 2, 835), fa("مشاوره تخصصی چیدمان، انتخاب میکسر و برآورد هزینه از صفر تا صد"), fill=TEXT_MUTED, font=f_h2_cover, anchor="mm")

d3.rounded_rectangle([(120, 900), (W - 120, 975)], radius=14, fill=(255, 255, 255, 255), outline=(200, 220, 240, 255), width=2)
d3.text((W // 2, 937), fa("طراحی رایگان پلان چیدمان کارگاه متناسب با متراژ شما"), fill=TEAL_DARK, font=ImageFont.truetype(font_black, 23), anchor="mm")

d3.rounded_rectangle([(120, 1010), (W - 120, 1085)], radius=14, fill=(255, 255, 255, 255), outline=(200, 220, 240, 255), width=2)
d3.text((W // 2, 1047), fa("تامین قالب‌های سفارشی برای محصولات سنتی و خاص"), fill=TEAL_DARK, font=ImageFont.truetype(font_black, 23), anchor="mm")

# Bottom CTA Bar
d3.rounded_rectangle([(60, 1220), (W - 60, 1310)], radius=16, fill=TEAL_DARK)
d3.text((W // 2, 1265), fa("جهت دریافت پروپوزال و قیمت، در دایرکت کلمه «کارگاه» را بفرستید"), fill=(255, 255, 255, 255), font=f_cta, anchor="mm")

s3_path = os.path.join(out_dir, "carousel_workshop_slide_03.jpg")
c3.convert("RGB").save(s3_path, quality=98)
c3.convert("RGB").save(os.path.join(artifact_dir, "carousel_workshop_slide_03.jpg"), quality=98)

print("Generated 3 slides of Carousel Workshop successfully!")
