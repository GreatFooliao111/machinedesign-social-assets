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
out_dir = os.path.join(base_dir, "02_generated_visuals", "carousel_roi")
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

f_card_title = ImageFont.truetype(font_black, 28)
f_card_sub = ImageFont.truetype(font_bold, 21)
f_card_desc = ImageFont.truetype(font_med, 19)

f_swipe = ImageFont.truetype(font_black, 22)
f_cta = ImageFont.truetype(font_black, 27)

PRIMARY_NAVY = (15, 28, 48, 255)
TEAL_DARK = (16, 78, 92, 255)
TEXT_MUTED = (85, 100, 115, 255)

RED_BG = (255, 246, 246, 255)
RED_BORDER = (245, 195, 195, 255)
RED_TEXT = (195, 35, 35, 255)

GREEN_BG = (246, 252, 246, 255)
GREEN_BORDER = (185, 230, 195, 255)
GREEN_TEXT = (25, 140, 60, 255)

GOLD_BG = (255, 251, 235, 255)
GOLD_BORDER = (235, 200, 120, 255)
GOLD_DARK = (160, 105, 10, 255)

def draw_header(canvas, draw, slide_num=None):
    if os.path.exists(logo_sym_path):
        sym = Image.open(logo_sym_path).convert("RGBA")
        sh = 88
        sw = int(sym.width * (sh / sym.height))
        sym = sym.resize((sw, sh), Image.Resampling.LANCZOS)
        canvas.paste(sym, (50, 20), sym)
        
        draw.text((50 + sw + 18, 28), "MachineDesign.ir", fill=TEAL_DARK, font=f_brand_title)
        draw.text((50 + sw + 20, 72), fa("مرکز تخصصی ماشین‌آلات صنایع غذایی"), fill=TEXT_MUTED, font=f_brand_sub)
    
    badge_text = f"SLIDE {slide_num}/4" if slide_num else "MODEL: KBDM-150"
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
    pw = (bbox[2] - bbox[0]) + 90
    draw.rounded_rectangle([(W // 2 - pw // 2, y), (W // 2 + pw // 2, y + 60)], radius=30, fill=PRIMARY_NAVY)
    draw.text((W // 2, y + 30), fa_txt, fill=(255, 255, 255, 255), font=f_swipe, anchor="mm")

# ==========================================================
# SLIDE 1: COVER (Visual Hook)
# ==========================================================
c1 = Image.new("RGBA", (W, H), (255, 255, 255, 255))
d1 = ImageDraw.Draw(c1)
draw_header(c1, d1, slide_num=1)

# Cover Titles
d1.text((W // 2, 160), fa("چرا این دستگاه ظرف ۹۰ روز"), fill=PRIMARY_NAVY, font=f_h1_cover, anchor="mm")
d1.text((W // 2, 225), fa("کل سرمایه خریدش را برمی‌گرداند؟"), fill=TEAL_DARK, font=f_h1_cover, anchor="mm")
d1.text((W // 2, 285), fa("تحلیل اقتصادی و مقایسه هزینه کارگری تولید دستی در برابر صنعتی"), fill=TEXT_MUTED, font=f_h2_cover, anchor="mm")

# Hero Machine: Huge, Beautiful, Centered
if os.path.exists(tight_crop_path):
    target_h = 750
    mach = Image.open(tight_crop_path).convert("RGBA")
    target_w = int(mach.width * (target_h / mach.height))
    mach = mach.resize((target_w, target_h), Image.Resampling.LANCZOS)
    paste_x = (W - target_w) // 2 + 10
    paste_y = 350
    c1.paste(mach, (paste_x, paste_y), mach)

# Swipe Pill at Bottom
draw_swipe_pill(d1, "ورق بزنید  ◀")

# Save Slide 1
s1_path = os.path.join(out_dir, "carousel_roi_slide_01.jpg")
c1.convert("RGB").save(s1_path, quality=98)
c1.convert("RGB").save(os.path.join(artifact_dir, "carousel_roi_slide_01.jpg"), quality=98)

# ==========================================================
# SLIDE 2: THE PROBLEM (Manual Production Pain Points)
# ==========================================================
c2 = Image.new("RGBA", (W, H), (255, 255, 255, 255))
d2 = ImageDraw.Draw(c2)
draw_header(c2, d2, slide_num=2)

d2.text((W // 2, 165), fa("روش سنتی و دستی: هزینه‌های سرسام‌آور ❌"), fill=RED_TEXT, font=f_h1_slide, anchor="mm")
d2.text((W // 2, 218), fa("۳ عامل پنهان که سود کارگاه‌های سنتی پیراشکی و سمبوسه را نابود می‌کند"), fill=TEXT_MUTED, font=f_sub_slide, anchor="mm")

pain_cards = [
    ("هزینه ماهانه سنگین دستمزد کارگری", "نیاز به ۶ تا ۸ کارگر ماهر برای تولید تیراژ متوسط", "پرداخت بیش از ۱۲۰ میلیون تومان حقوق، بیمه و عیدی در هر ماه که سود خالص شما را می‌بلعد."),
    ("نرخ بالای دورریز و ضایعات خمیر (تا ۱۲٪)", "ضایعات ناشی از خطای دست و خستگی اپراتور", "ضخامت غیریکنواخت خمیر، پارگی لبه‌ها و بیرون‌زدگی فیلینگ گوشت در حین سرخ کردن یا پخت."),
    ("محدودیت سرعت و عدم توانایی در پاسخ به بازار", "سقف تولید حداکثر ۶۰۰ عدد در ساعت برای کل تیم", "از دست دادن سفارشات عمده هتل‌ها، رستوران‌ها و سوپرمارکت‌ها به دلیل کندی روش دستی.")
]

card_y = 265
card_h = 275
for idx, (title, sub, desc) in enumerate(pain_cards):
    cy = card_y + idx * (card_h + 30)
    d2.rounded_rectangle([(60, cy), (W - 60, cy + card_h)], radius=18, fill=RED_BG, outline=RED_BORDER, width=2)
    d2.line([(W - 70, cy + 24), (W - 70, cy + card_h - 24)], fill=RED_TEXT, width=8)
    
    d2.text((W - 95, cy + 45), fa(f"۰{idx+1} . {title}"), fill=RED_TEXT, font=f_card_title, anchor="rm")
    d2.text((W - 95, cy + 105), fa(sub), fill=PRIMARY_NAVY, font=f_card_sub, anchor="rm")
    
    d2.line([(90, cy + 145), (W - 95, cy + 145)], fill=RED_BORDER, width=1)
    
    d2.text((W - 95, cy + 195), fa(desc), fill=TEXT_MUTED, font=f_card_desc, anchor="rm")

# Bottom Swipe
draw_swipe_pill(d2, "ورق بزنید: راهکار اتوماسیون  ◀")

s2_path = os.path.join(out_dir, "carousel_roi_slide_02.jpg")
c2.convert("RGB").save(s2_path, quality=98)
c2.convert("RGB").save(os.path.join(artifact_dir, "carousel_roi_slide_02.jpg"), quality=98)

# ==========================================================
# SLIDE 3: THE SOLUTION (KBDM-150 Supercharged Production)
# ==========================================================
c3 = Image.new("RGBA", (W, H), (255, 255, 255, 255))
d3 = ImageDraw.Draw(c3)
draw_header(c3, d3, slide_num=3)

d3.text((W // 2, 165), fa("خط صنعتی KBDM-150: انفجار سودآوری ✅"), fill=GREEN_TEXT, font=f_h1_slide, anchor="mm")
d3.text((W // 2, 218), fa("۳ مزیت رقابتی که هزینه‌های تولید شما را ۸۵٪ کاهش می‌دهد"), fill=TEXT_MUTED, font=f_sub_slide, anchor="mm")

solution_cards = [
    ("کاهش پرسنل به فقط ۱ اپراتور ساده", "۹۵ میلیون تومان پس‌انداز ماهانه دستمزد", "دیگر نگران مرخصی، خطای کارگری یا جابجایی پرسنل نباشید؛ یک نفر کل خط را مدیریت می‌کند."),
    ("جهش سرعت تولید تا ۱۰,۰۰۰ عدد در ساعت", "۱۲ برابر سریع‌تر از کل تیم سنتی شما", "تولید روزانه تا ۸۰,۰۰۰ عدد پیراشکی، سمبوسه یا کلمپه و توانایی عقد قرارداد با فروشگاه‌های زنجیره‌ای."),
    ("ضایعات زیر ۱٪ و کیفیت کاملاً یکنواخت", "نورد غلتکی بدون تنش و حفظ بافت دست‌ساز", "دوخت محکم لبه‌ها بدون وا رفتن، تنظیم دقیق وزن هر قطعه از ۱۰ تا ۳۵ گرم و استاندارد بهداشت ۳۰۴.")
]

for idx, (title, sub, desc) in enumerate(solution_cards):
    cy = card_y + idx * (card_h + 30)
    d3.rounded_rectangle([(60, cy), (W - 60, cy + card_h)], radius=18, fill=GREEN_BG, outline=GREEN_BORDER, width=2)
    d3.line([(W - 70, cy + 24), (W - 70, cy + card_h - 24)], fill=GREEN_TEXT, width=8)
    
    d3.text((W - 95, cy + 45), fa(f"۰{idx+1} . {title}"), fill=GREEN_TEXT, font=f_card_title, anchor="rm")
    d3.text((W - 95, cy + 105), fa(sub), fill=PRIMARY_NAVY, font=f_card_sub, anchor="rm")
    
    d3.line([(90, cy + 145), (W - 95, cy + 145)], fill=GREEN_BORDER, width=1)
    
    d3.text((W - 95, cy + 195), fa(desc), fill=TEXT_MUTED, font=f_card_desc, anchor="rm")

# Bottom Swipe
draw_swipe_pill(d3, "ورق بزنید: محاسبه بازگشت سرمایه  ◀")

s3_path = os.path.join(out_dir, "carousel_roi_slide_03.jpg")
c3.convert("RGB").save(s3_path, quality=98)
c3.convert("RGB").save(os.path.join(artifact_dir, "carousel_roi_slide_03.jpg"), quality=98)

# ==========================================================
# SLIDE 4: ROI SUMMARY & CALL TO ACTION
# ==========================================================
c4 = Image.new("RGBA", (W, H), (255, 255, 255, 255))
d4 = ImageDraw.Draw(c4)
draw_header(c4, d4, slide_num=4)

d4.text((W // 2, 165), fa("نتیجه نهایی محاسبه بازگشت سرمایه (ROI)"), fill=PRIMARY_NAVY, font=f_h1_slide, anchor="mm")
d4.text((W // 2, 218), fa("سرمایه‌گذاری روی KBDM-150 چگونه ظرف ۳ ماه بازمی‌گردد؟"), fill=TEAL_DARK, font=f_sub_slide, anchor="mm")

# Golden Box
d4.rounded_rectangle([(60, 265), (W - 60, 680)], radius=20, fill=GOLD_BG, outline=GOLD_BORDER, width=2)
d4.text((W // 2, 315), fa("خلاصه ارقام مالی و سودآوری خالص"), fill=GOLD_DARK, font=ImageFont.truetype(font_black, 32), anchor="mm")
d4.line([(100, 360), (W - 100, 360)], fill=GOLD_BORDER, width=2)

roi_metrics = [
    ("صرفه‌جویی سالانه دستمزد:", "بیش از ۱.۱ میلیارد تومان"),
    ("مدت زمان استهلاک دستگاه:", "کمتر از ۹۰ روز کاری (۳ ماه)"),
    ("جهش درآمدی از محل تیراژ:", "تا ۳ برابر افزایش فروش ناخالص"),
    ("پوشش گارانتی و خدمات:", "۱ سال گارانتی رسمی + ۱۰ سال خدمات")
]

for idx, (lbl, val) in enumerate(roi_metrics):
    my = 405 + idx * 62
    d4.text((W - 110, my), fa(lbl), fill=PRIMARY_NAVY, font=ImageFont.truetype(font_bold, 24), anchor="rm")
    d4.text((110, my), fa(val), fill=TEAL_DARK, font=ImageFont.truetype(font_black, 24), anchor="lm")

# Action Box
d4.rounded_rectangle([(60, 720), (W - 60, 1180)], radius=20, fill=(244, 248, 254, 255), outline=TEAL_DARK, width=2)

d4.text((W // 2, 790), fa("آیا می‌خواهید محاسبه دقیق کارگاه خود را ببینید؟"), fill=PRIMARY_NAVY, font=ImageFont.truetype(font_black, 32), anchor="mm")
d4.text((W // 2, 855), fa("فایل اکسل محاسباتی بیزینس‌پلن بر اساس ظرفیت و خمیر شما آماده است"), fill=TEXT_MUTED, font=f_h2_cover, anchor="mm")

# Offer Pills
d4.rounded_rectangle([(120, 920), (W - 120, 995)], radius=14, fill=(255, 255, 255, 255), outline=(200, 220, 240, 255), width=2)
d4.text((W // 2, 957), fa("تست حضوری رایگان با خمیر اختصاصی شما در کارخانه"), fill=TEAL_DARK, font=ImageFont.truetype(font_black, 23), anchor="mm")

d4.rounded_rectangle([(120, 1030), (W - 120, 1105)], radius=14, fill=(255, 255, 255, 255), outline=(200, 220, 240, 255), width=2)
d4.text((W // 2, 1067), fa("تحویل فوری + نصب و آموزش کامل اپراتور"), fill=TEAL_DARK, font=ImageFont.truetype(font_black, 23), anchor="mm")

# Final Bottom CTA
d4.rounded_rectangle([(60, 1220), (W - 60, 1310)], radius=16, fill=TEAL_DARK)
d4.text((W // 2, 1265), fa("جهت دریافت بیزینس‌پلن و قیمت، در دایرکت کلمه «سود» را بفرستید"), fill=(255, 255, 255, 255), font=f_cta, anchor="mm")

s4_path = os.path.join(out_dir, "carousel_roi_slide_04.jpg")
c4.convert("RGB").save(s4_path, quality=98)
c4.convert("RGB").save(os.path.join(artifact_dir, "carousel_roi_slide_04.jpg"), quality=98)

print("Generated 4 slides of Carousel ROI successfully!")
