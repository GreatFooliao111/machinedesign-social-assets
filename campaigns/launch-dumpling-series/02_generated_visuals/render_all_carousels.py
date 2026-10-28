import os
import time
import socketserver
import http.server
import threading
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_DIR = r"D:\Machinedesign.ir\machinedesign-social-assets\campaigns\launch-dumpling-series"
VISUALS_DIR = os.path.join(BASE_DIR, "02_generated_visuals")

def start_local_server(directory, port=9030):
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)
        def log_message(self, format, *args):
            pass

    for p in range(port, port + 20):
        try:
            server = socketserver.TCPServer(('127.0.0.1', p), QuietHandler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            return server, p
        except OSError:
            continue
    raise RuntimeError("Could not find an available local port.")

def get_shared_head():
    return """
    <meta charset="UTF-8">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800;900&family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
      :root {
        --neon: #8ce70c;
        --neon-dim: rgba(140, 231, 12, 0.12);
        --neon-border: rgba(140, 231, 12, 0.38);
        --bg-card: radial-gradient(circle at 18% 18%, #161a17 0%, #090c0a 65%, #040504 100%);
        --text-white: #ffffff;
        --text-light: #d1d5db;
        --text-muted: #9ca3af;
        --border-subtle: rgba(255, 255, 255, 0.08);
      }
      * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        -webkit-font-smoothing: antialiased;
      }
      body {
        background-color: #040504;
        font-family: 'Vazirmatn', sans-serif;
        padding: 40px;
        color: var(--text-white);
        direction: rtl;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        gap: 40px;
        justify-content: center;
      }
      .slide {
        position: relative;
        width: 360px;
        height: 450px;
        background: var(--bg-card);
        border-top: 4px solid var(--neon);
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.9), 0 0 0 1px rgba(255, 255, 255, 0.08);
        display: flex;
        flex-direction: column;
        user-select: none;
      }
      .bg-tech-grid {
        background-image: 
          linear-gradient(rgba(255, 255, 255, 0.025) 1px, transparent 1px),
          linear-gradient(90deg, rgba(255, 255, 255, 0.025) 1px, transparent 1px),
          var(--bg-card);
        background-size: 20px 20px, 20px 20px, 100% 100%;
      }
      .slide-top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 18px 0;
        flex-shrink: 0;
        z-index: 10;
      }
      .brand-mark {
        font-family: 'Orbitron', sans-serif;
        font-size: 11.5px;
        font-weight: 800;
        letter-spacing: 0.5px;
        color: #fff;
        direction: ltr;
        unicode-bidi: isolate;
      }
      .brand-mark span {
        color: var(--neon);
      }
      .slide-counter {
        font-family: 'Orbitron', sans-serif;
        font-size: 10.5px;
        font-weight: 700;
        color: var(--neon);
        letter-spacing: 1px;
        background: rgba(10, 14, 10, 0.9);
        border: 1px solid var(--neon-border);
        padding: 2.5px 7px;
        line-height: 1;
        direction: ltr;
        unicode-bidi: isolate;
      }
      .slide-bottom-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 7px 18px 10px;
        border-top: 1px solid var(--border-subtle);
        background: rgba(0, 0, 0, 0.45);
        flex-shrink: 0;
        z-index: 10;
        direction: ltr;
        unicode-bidi: isolate;
      }
      .footer-slug {
        font-family: 'Orbitron', sans-serif;
        font-size: 8px;
        font-weight: 600;
        color: var(--text-muted);
        letter-spacing: 0.6px;
      }
      .footer-brand {
        font-family: 'Orbitron', sans-serif;
        font-size: 8.5px;
        font-weight: 700;
        color: var(--neon);
      }
      .slide-body {
        padding: 10px 18px 8px;
        display: flex;
        flex-direction: column;
        flex: 1;
        justify-content: space-between;
      }
      .header-stack {
        margin-bottom: 8px;
        flex-shrink: 0;
      }
      .eyebrow-row {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 4px;
      }
      .category-pill {
        font-size: 8.5px;
        font-weight: 700;
        color: var(--neon);
        background: var(--neon-dim);
        border: 1px solid var(--neon-border);
        padding: 2px 6px;
        border-radius: 2px;
        white-space: nowrap;
      }
      .eyebrow-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 8.5px;
        font-weight: 700;
        color: #9ca3af;
        letter-spacing: 0.5px;
        direction: ltr;
        unicode-bidi: isolate;
      }
      h2.slide-h2 {
        font-size: 14.5px;
        font-weight: 800;
        line-height: 1.35;
        color: #ffffff;
        margin: 0;
      }
      h2.slide-h2 span {
        color: var(--neon);
      }
      .s1-wrap {
        display: flex;
        flex-direction: column;
        height: 100%;
        justify-content: space-between;
      }
      .s1-photo-frame {
        position: relative;
        width: 100%;
        height: 195px;
        border: 1px solid var(--neon-border);
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 10px;
        flex-shrink: 0;
        background: #000;
      }
      .s1-photo-frame img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        filter: contrast(1.08) brightness(0.95);
      }
      .s1-photo-badge {
        position: absolute;
        bottom: 8px;
        left: 8px;
        background: rgba(8, 12, 8, 0.92);
        border-left: 3px solid var(--neon);
        padding: 3px 7px;
        font-family: 'Orbitron', sans-serif;
        font-size: 8.5px;
        font-weight: 700;
        color: var(--neon);
        letter-spacing: 0.5px;
        direction: ltr;
        unicode-bidi: isolate;
      }
      .s1-lead {
        font-size: 11px;
        color: var(--text-light);
        line-height: 1.55;
      }
      .s1-action-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 6px;
        border-top: 1px solid var(--border-subtle);
      }
      .s1-swipe-prompt {
        font-size: 10.5px;
        font-weight: 800;
        color: var(--neon);
      }
      .split-banner {
        width: 100%;
        height: 120px;
        border: 1px solid var(--border-subtle);
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 8px;
        background: #000;
      }
      .split-banner img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      .points-stack {
        display: flex;
        flex-direction: column;
        gap: 6px;
        flex: 1;
      }
      .point-item {
        display: flex;
        gap: 8px;
        align-items: flex-start;
        background: rgba(18, 22, 19, 0.7);
        border: 1px solid var(--border-subtle);
        border-right: 3px solid var(--neon);
        padding: 6px 9px;
        border-radius: 3px;
      }
      .point-num-box {
        font-family: 'Orbitron', sans-serif;
        font-size: 10.5px;
        font-weight: 800;
        color: var(--neon);
        flex-shrink: 0;
        padding-top: 1px;
      }
      .point-detail h4 {
        font-size: 10.5px;
        font-weight: 700;
        color: #fff;
        margin-bottom: 2px;
      }
      .point-detail p {
        font-size: 9.2px;
        color: var(--text-muted);
        line-height: 1.45;
      }
      .kpi-duo {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin-bottom: 8px;
      }
      .kpi-block {
        background: rgba(140, 231, 12, 0.06);
        border: 1px solid var(--neon-border);
        padding: 8px;
        border-radius: 4px;
        text-align: center;
      }
      .kpi-val {
        font-family: 'Orbitron', sans-serif;
        font-size: 18px;
        font-weight: 900;
        color: var(--neon);
        line-height: 1.1;
        direction: ltr;
        unicode-bidi: isolate;
      }
      .kpi-lbl {
        font-size: 9px;
        font-weight: 600;
        color: var(--text-light);
        margin-top: 3px;
      }
      .editorial-box {
        background: rgba(18, 22, 19, 0.65);
        border: 1px solid var(--border-subtle);
        padding: 9px;
        border-radius: 4px;
        font-size: 10px;
        color: var(--text-light);
        line-height: 1.6;
      }
      .pillars-stack {
        display: flex;
        flex-direction: column;
        gap: 6px;
        margin-bottom: 8px;
      }
      .pillar-row {
        display: flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--border-subtle);
        padding: 5px 9px;
        border-radius: 3px;
        font-size: 9.8px;
        color: var(--text-light);
      }
      .pillar-num {
        font-family: 'Orbitron', sans-serif;
        font-size: 9.5px;
        font-weight: 800;
        color: var(--neon);
        flex-shrink: 0;
      }
      .cta-card {
        background: radial-gradient(circle at 50% 0%, rgba(140, 231, 12, 0.18) 0%, rgba(14, 18, 14, 0.95) 100%);
        border: 1px solid var(--neon);
        border-radius: 4px;
        padding: 9px;
        text-align: center;
      }
      .cta-badge {
        font-family: 'Orbitron', sans-serif;
        font-size: 8px;
        font-weight: 800;
        color: #9ca3af;
        letter-spacing: 0.8px;
        margin-bottom: 3px;
        direction: ltr;
        unicode-bidi: isolate;
      }
      .cta-action {
        font-size: 11.5px;
        font-weight: 800;
        color: var(--neon);
        margin-bottom: 2px;
      }
      .cta-web {
        font-family: 'Orbitron', sans-serif;
        font-size: 8.5px;
        font-weight: 700;
        color: #fff;
        direction: ltr;
        unicode-bidi: isolate;
      }
    </style>
    """

# -------------------------------------------------------------
# 1. CAROUSEL 1: DOUGH & ROLLER SHEETING (4 SLIDES)
# -------------------------------------------------------------
def build_html_dough():
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <title>Carousel Dough</title>
  {get_shared_head()}
</head>
<body>
  <!-- Slide 1 -->
  <article class="slide bg-tech-grid" id="slide-1">
    <div class="slide-top-header">
      <div class="brand-mark"><span>Machine</span>Design</div>
      <div class="slide-counter">01 / 04</div>
    </div>
    <div class="slide-body">
      <div class="s1-wrap">
        <div>
          <div class="header-stack">
            <div class="eyebrow-row">
              <span class="category-pill">مهندسی خمیر و نورد</span>
              <span class="eyebrow-text">KBDM-150 TECH</span>
            </div>
            <h2 class="slide-h2">چرا خمیر روی این دستگاه <span>نه پاره میشه</span> و نه می‌چسبه؟ 🥟</h2>
          </div>
          <div class="s1-photo-frame">
            <img src="generated_dough_rollers_macro.jpg" alt="Dough Rollers">
            <div class="s1-photo-badge">SUS304 DUAL ROLLERS // 0.8MM</div>
          </div>
          <p class="s1-lead">برخلاف دستگاه‌های بی‌کیفیت ماردونی که خمیر را داغ و بافتش را متلاشی می‌کنند، در KBDM-150 خمیر با ۳ جفت غلتک کالیبره‌شده، آرام‌آرام مثل دست یک نانوای کهنه‌کار باز می‌شود.</p>
        </div>
        <div class="s1-action-row">
          <span class="s1-swipe-prompt">ورق بزنید ←</span>
          <span style="font-family:'Orbitron',sans-serif; font-size:9.5px; color:#9ca3af; direction:ltr;">@h.vatan.doust</span>
        </div>
      </div>
    </div>
    <div class="slide-bottom-footer">
      <div class="footer-slug">SLOT 01 // DOUGH CALIBRATION</div>
      <div class="footer-brand">machinedesign.ir</div>
    </div>
  </article>

  <!-- Slide 2 -->
  <article class="slide bg-tech-grid" id="slide-2">
    <div class="slide-top-header">
      <div class="brand-mark"><span>Machine</span>Design</div>
      <div class="slide-counter">02 / 04</div>
    </div>
    <div class="slide-body">
      <div class="header-stack">
        <div class="eyebrow-row">
          <span class="category-pill">کالبدشکافی مکانیسم</span>
          <span class="eyebrow-text">STAGE 01 TO 03</span>
        </div>
        <h2 class="slide-h2">نورد ملایم ۳ مرحله‌ای <span>بدون ماردون</span></h2>
      </div>
      <div class="split-banner">
        <img src="asset_06_roller_mechanism.jpg" alt="Roller Mechanism">
      </div>
      <div class="points-stack">
        <div class="point-item">
          <div class="point-num-box">۰۱</div>
          <div class="point-detail">
            <h4>غلتک اول و دوم (فشرده‌سازی و میانی)</h4>
            <p>کاهش پیوسته ضخامت از ۴.۲ به ۱.۸ میلی‌متر بدون ایجاد تنش برشی، بدون حرارت و بدون آسیب به شبکه گلوتن آرد.</p>
          </div>
        </div>
        <div class="point-item">
          <div class="point-num-box">۰۲</div>
          <div class="point-detail">
            <h4>غلتک سوم (کالیبراسیون میکرومتری)</h4>
            <p>تحویل یک نوار خمیر فوق‌العاده صاف، لطیف و یکدست با ضخامت دقیق ۰.۸ میلی‌متر جهت فرم‌دهی بدون چروک در قالب.</p>
          </div>
        </div>
      </div>
    </div>
    <div class="slide-bottom-footer">
      <div class="footer-slug">CONTINUOUS ROLLER SHEETING</div>
      <div class="footer-brand">machinedesign.ir</div>
    </div>
  </article>

  <!-- Slide 3 -->
  <article class="slide bg-tech-grid" id="slide-3">
    <div class="slide-top-header">
      <div class="brand-mark"><span>Machine</span>Design</div>
      <div class="slide-counter">03 / 04</div>
    </div>
    <div class="slide-body">
      <div class="header-stack">
        <div class="eyebrow-row">
          <span class="category-pill">آرامش خاطر و فرمولاسیون</span>
          <span class="eyebrow-text">ZERO DOUGH WASTE</span>
        </div>
        <h2 class="slide-h2">فرمول طلایی خمیر ایرانی + <span>صفر درصد ضایعات</span></h2>
      </div>
      <div class="kpi-duo">
        <div class="kpi-block">
          <div class="kpi-val">۰.۸ mm</div>
          <div class="kpi-lbl">ضخامت یکنواخت و بدون کشش</div>
        </div>
        <div class="kpi-block">
          <div class="kpi-val">۰ %</div>
          <div class="kpi-lbl">ضایعات خمیر با بازگشت خودکار</div>
        </div>
      </div>
      <div class="editorial-box">
        <p><strong>قلق خمیر با ماست!</strong> ما فرمولاسیون دقیق آرد ستاره، آب سرد و نشاسته را متناسب با گندم ایران مهندسی کرده‌ایم و صفر تا صد را به شما آموزش می‌دهیم.</p>
        <p style="margin-top:6px; color:#9ca3af;">علاوه بر این، کناره‌های خمیر با کانوایر بازگشتی به صورت خودکار به غلتک اول برمی‌گردند؛ یعنی حتی یک گرم پرتی خمیر نخواهید داشت!</p>
      </div>
    </div>
    <div class="slide-bottom-footer">
      <div class="footer-slug">GOLDEN RECIPE // ZERO WASTE</div>
      <div class="footer-brand">machinedesign.ir</div>
    </div>
  </article>

  <!-- Slide 4 -->
  <article class="slide bg-tech-grid" id="slide-4">
    <div class="slide-top-header">
      <div class="brand-mark"><span>Machine</span>Design</div>
      <div class="slide-counter">04 / 04</div>
    </div>
    <div class="slide-body">
      <div class="header-stack">
        <div class="eyebrow-row">
          <span class="category-pill">تست حضوری و مشاوره</span>
          <span class="eyebrow-text">WORKSHOP DEMO</span>
        </div>
        <h2 class="slide-h2">با خمیر خودتان <span>در کارگاه ما تست بگیرید!</span></h2>
      </div>
      <div class="pillars-stack">
        <div class="pillar-row">
          <span class="pillar-num">۰۱</span>
          <span>تست حضوری رایگان با فرمول خمیر و مواد خود شما در تهران</span>
        </div>
        <div class="pillar-row">
          <span class="pillar-num">۰۲</span>
          <span>آموزش کامل نسبت‌های اختلاط و زمان استراحت خمیر آماده</span>
        </div>
        <div class="pillar-row">
          <span class="pillar-num">۰۳</span>
          <span>پشتیبانی مستقیم و تامین دائمی قطعات از انبار تهران</span>
        </div>
      </div>
      <div class="cta-card">
        <div class="cta-badge">FREE RECIPE & DEMO IN TEHRAN</div>
        <div class="cta-action">ارسال کلمه «خمیر» در دایرکت</div>
        <div class="cta-web">تماس مستقیم: ۰۹۳۵۸۶۸۹۸۲۹ | machinedesign.ir</div>
      </div>
    </div>
    <div class="slide-bottom-footer">
      <div class="footer-slug">CALL TO ACTION // WORKSHOP</div>
      <div class="footer-brand">@h.vatan.doust</div>
    </div>
  </article>
</body>
</html>
"""

# -------------------------------------------------------------
# 2. CAROUSEL 2: IRANIAN TASTE MOLDS (4 SLIDES)
# -------------------------------------------------------------
def build_html_molds():
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <title>Carousel Molds</title>
  {get_shared_head()}
</head>
<body>
  <!-- Slide 1 -->
  <article class="slide bg-tech-grid" id="slide-1">
    <div class="slide-top-header">
      <div class="brand-mark"><span>Machine</span>Design</div>
      <div class="slide-counter">01 / 04</div>
    </div>
    <div class="slide-body">
      <div class="s1-wrap">
        <div>
          <div class="header-stack">
            <div class="eyebrow-row">
              <span class="category-pill">تنوع محصولات بازار</span>
              <span class="eyebrow-text">IRANIAN CUISINE</span>
            </div>
            <h2 class="slide-h2">از سمبوسه خوزستانی تا <span>پیراشکی دالبری و کلمپه</span></h2>
          </div>
          <div class="s1-photo-frame">
            <img src="generated_iranian_molds_matrix.jpg" alt="Iranian Pastries Matrix">
            <div class="s1-photo-badge">5 MODULAR MOLDS // HERMETIC SEAL</div>
          </div>
          <p class="s1-lead">فکر نکنید این دستگاه فقط برای غذاهای خارجی است! ما قالب‌ها را دقیقاً متناسب با فرهنگ غذایی و سلیقه بازار ایران سفارشی کرده‌ایم تا چندین خط تولید سودآور راه‌اندازی کنید.</p>
        </div>
        <div class="s1-action-row">
          <span class="s1-swipe-prompt">ورق بزنید ←</span>
          <span style="font-family:'Orbitron',sans-serif; font-size:9.5px; color:#9ca3af; direction:ltr;">@h.vatan.doust</span>
        </div>
      </div>
    </div>
    <div class="slide-bottom-footer">
      <div class="footer-slug">SLOT 02 // IRANIAN MOLDS</div>
      <div class="footer-brand">machinedesign.ir</div>
    </div>
  </article>

  <!-- Slide 2 -->
  <article class="slide bg-tech-grid" id="slide-2">
    <div class="slide-top-header">
      <div class="brand-mark"><span>Machine</span>Design</div>
      <div class="slide-counter">02 / 04</div>
    </div>
    <div class="slide-body">
      <div class="header-stack">
        <div class="eyebrow-row">
          <span class="category-pill">ویترین قالب‌های ماژولار</span>
          <span class="eyebrow-text">5 POPULAR PRODUCTS</span>
        </div>
        <h2 class="slide-h2">یک پلتفرم، <span>۵ محصول پرفروش بازار</span></h2>
      </div>
      <div class="split-banner">
        <img src="asset_04_food_matrix_commercial.jpg" alt="Commercial Food Matrix">
      </div>
      <div class="points-stack">
        <div class="point-item">
          <div class="point-num-box">۰۱</div>
          <div class="point-detail">
            <h4>سمبوسه مثلثی خوزستانی و پیتزایی (۲۵ تا ۳۵ گرم)</h4>
            <p>دوخت محکم سنتی با ظاهری ترد، بدون چنگال‌پیچی دستی و مناسب سرخ‌کردن صنعتی.</p>
          </div>
        </div>
        <div class="point-item">
          <div class="point-num-box">۰۲</div>
          <div class="point-detail">
            <h4>پیراشکی دالبری نوستالژیک و گوشتی (۲۰ تا ۳۰ گرم)</h4>
            <p>لبه‌های کنگره‌ای کاملاً یکنواخت، بدون باز شدن در فر یا روغن داغ، با استقبال فوق‌العاده بازار.</p>
          </div>
        </div>
        <div class="point-item">
          <div class="point-num-box">۰۳</div>
          <div class="point-detail">
            <h4>جوشباره، بورک و شیرینی‌های سنتی</h4>
            <p>تولید سریع برای تامین هایپرمارکت‌ها، رستوران‌ها و خطوط تولید منجمد.</p>
          </div>
        </div>
      </div>
    </div>
    <div class="slide-bottom-footer">
      <div class="footer-slug">MODULAR MOLD MATRIX</div>
      <div class="footer-brand">machinedesign.ir</div>
    </div>
  </article>

  <!-- Slide 3 -->
  <article class="slide bg-tech-grid" id="slide-3">
    <div class="slide-top-header">
      <div class="brand-mark"><span>Machine</span>Design</div>
      <div class="slide-counter">03 / 04</div>
    </div>
    <div class="slide-body">
      <div class="header-stack">
        <div class="eyebrow-row">
          <span class="category-pill">دوخت هوابند و بهداشت</span>
          <span class="eyebrow-text">ZERO LEAKAGE</span>
        </div>
        <h2 class="slide-h2">دوخت ۱۰۰٪ هوابند + <span>شستشوی ۵ دقیقه‌ای</span></h2>
      </div>
      <div class="kpi-duo">
        <div class="kpi-block">
          <div class="kpi-val">۱۰۰ %</div>
          <div class="kpi-lbl">آب‌بندی درز در روغن داغ</div>
        </div>
        <div class="kpi-block">
          <div class="kpi-val">&lt; ۵ min</div>
          <div class="kpi-lbl">شستشوی بدون ابزار در پایان شیفت</div>
        </div>
      </div>
      <div class="editorial-box">
        <p><strong>بدون پس دادن روغن!</strong> لبه‌های محصولات با فشار کالیبره‌شده درام چنان تمیز دوخت می‌خورند که موقع سرخ‌شدن حتی یک قطره پس نمی‌دهند.</p>
        <p style="margin-top:6px; color:#9ca3af;">تمامی قطعات در تماس با غذا از استیل ۳۰۴ صنایع غذایی بوده و در کمتر از ۵ دقیقه بدون نیاز به هیچ ابزاری دمونتاژ و شسته می‌شوند.</p>
      </div>
    </div>
    <div class="slide-bottom-footer">
      <div class="footer-slug">HERMETIC SEAL // HYGIENE</div>
      <div class="footer-brand">machinedesign.ir</div>
    </div>
  </article>

  <!-- Slide 4 -->
  <article class="slide bg-tech-grid" id="slide-4">
    <div class="slide-top-header">
      <div class="brand-mark"><span>Machine</span>Design</div>
      <div class="slide-counter">04 / 04</div>
    </div>
    <div class="slide-body">
      <div class="header-stack">
        <div class="eyebrow-row">
          <span class="category-pill">کاتالوگ و استعلام</span>
          <span class="eyebrow-text">MOLD CATALOG</span>
        </div>
        <h2 class="slide-h2">کاتالوگ تصویری قالب‌ها <span>و نمونه محصولات</span></h2>
      </div>
      <div class="pillars-stack">
        <div class="pillar-row">
          <span class="pillar-num">۰۱</span>
          <span>امکان سفارشی‌سازی فرم لبه و وزن قطعه متناسب با خط شما</span>
        </div>
        <div class="pillar-row">
          <span class="pillar-num">۰۲</span>
          <span>تعویض سریع هر قالب در کمتر از ۱۵ دقیقه توسط ۱ اپراتور</span>
        </div>
        <div class="pillar-row">
          <span class="pillar-num">۰۳</span>
          <span>موجودی دائم درام‌های قالب و گارانتی تعویض در تهران</span>
        </div>
      </div>
      <div class="cta-card">
        <div class="cta-badge">MOLD CATALOG & SAMPLES</div>
        <div class="cta-action">ارسال کلمه «قالب» در دایرکت</div>
        <div class="cta-web">تماس مستقیم: ۰۹۳۵۸۶۸۹۸۲۹ | machinedesign.ir</div>
      </div>
    </div>
    <div class="slide-bottom-footer">
      <div class="footer-slug">CALL TO ACTION // MOLDS</div>
      <div class="footer-brand">@h.vatan.doust</div>
    </div>
  </article>
</body>
</html>
"""

# -------------------------------------------------------------
# 3. CAROUSEL 3: EARLY-BIRD LAUNCH (6 SLIDES)
# -------------------------------------------------------------
def build_html_early_bird():
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <title>Carousel Early Bird Launch</title>
  {get_shared_head()}
</head>
<body>
  <!-- Slide 1 -->
  <article class="slide bg-tech-grid" id="slide-1">
    <div class="slide-top-header">
      <div class="brand-mark"><span>Machine</span>Design</div>
      <div class="slide-counter">01 / 06</div>
    </div>
    <div class="slide-body">
      <div class="s1-wrap">
        <div>
          <div class="header-stack">
            <div class="eyebrow-row">
              <span class="category-pill">اعلان رسمی پیش‌فروش</span>
              <span class="eyebrow-text">LIMITED BATCH 01</span>
            </div>
            <h2 class="slide-h2">آغاز ثبت‌نام پارت اول KBDM-150: <span>فقط ۵ سهمیه!</span></h2>
          </div>
          <div class="s1-photo-frame">
            <img src="../01_source_material/images/konbrit_150_source_01.png" alt="Konbrit 150 Launch">
            <div class="s1-photo-badge">SPECIAL PRIVILEGE // 5 UNITS ONLY</div>
          </div>
          <p class="s1-lead">همراه با قالب دوم هدیه به ارزش ۳۵ میلیون تومان و آموزش صفر تا صد فرمولاسیون خمیر آماده؛ یک سرمایه‌گذاری امن با بازگشت سرمایه زیر ۳ ماه.</p>
        </div>
        <div class="s1-action-row">
          <span class="s1-swipe-prompt">ورق بزنید ←</span>
          <span style="font-family:'Orbitron',sans-serif; font-size:9.5px; color:#9ca3af; direction:ltr;">@h.vatan.doust</span>
        </div>
      </div>
    </div>
    <div class="slide-bottom-footer">
      <div class="footer-slug">SLOT 03 // HERO LAUNCH</div>
      <div class="footer-brand">machinedesign.ir</div>
    </div>
  </article>

  <!-- Slide 2 -->
  <article class="slide bg-tech-grid" id="slide-2">
    <div class="slide-top-header">
      <div class="brand-mark"><span>Machine</span>Design</div>
      <div class="slide-counter">02 / 06</div>
    </div>
    <div class="slide-body">
      <div class="header-stack">
        <div class="eyebrow-row">
          <span class="category-pill">شناسنامه مهندسی دستگاه</span>
          <span class="eyebrow-text">PERFORMANCE SPECS</span>
        </div>
        <h2 class="slide-h2">ظرفیت ۱۰,۰۰۰ عددی با <span>برق تک‌فاز شهری</span></h2>
      </div>
      <div class="split-banner">
        <img src="asset_02_full_specs_infographic.jpg" alt="Technical Specs">
      </div>
      <div class="points-stack">
        <div class="point-item">
          <div class="point-num-box">۰۱</div>
          <div class="point-detail">
            <h4>سرعت تولید تا ۱۰,۰۰۰ عدد در ساعت</h4>
            <p>تنظیم مستقل ولوم‌های مغزی، سرعت نورد و درام با اینورتورهای دقیق و کاربری بسیار آسان.</p>
          </div>
        </div>
        <div class="point-item">
          <div class="point-num-box">۰۲</div>
          <div class="point-detail">
            <h4>برق ۲۲۰ ولت تک‌فاز شهری (کم‌مصرف)</h4>
            <p>توان بهینه ۱.۸ کیلووات؛ کاملاً سازگار با مغازه‌ها و کارگاه‌های کوچک بدون نیاز به برق سه‌فاز.</p>
          </div>
        </div>
      </div>
    </div>
    <div class="slide-bottom-footer">
      <div class="footer-slug">TECHNICAL SPECS // 220V POWER</div>
      <div class="footer-brand">machinedesign.ir</div>
    </div>
  </article>

  <!-- Slide 3 -->
  <article class="slide bg-tech-grid" id="slide-3">
    <div class="slide-top-header">
      <div class="brand-mark"><span>Machine</span>Design</div>
      <div class="slide-counter">03 / 06</div>
    </div>
    <div class="slide-body">
      <div class="header-stack">
        <div class="eyebrow-row">
          <span class="category-pill">پکیج طلایی ارلی‌برد</span>
          <span class="eyebrow-text">4 SPECIAL PRIVILEGES</span>
        </div>
        <h2 class="slide-h2">۴ مزیت ویژه برای <span>۵ خریدار پارت اول</span></h2>
      </div>
      <div class="kpi-duo">
        <div class="kpi-block">
          <div class="kpi-val">۳۵ م‌ت</div>
          <div class="kpi-lbl">ارزش قالب دوم ماژولار هدیه</div>
        </div>
        <div class="kpi-block">
          <div class="kpi-val">۰ تا ۱۰۰</div>
          <div class="kpi-lbl">آموزش فرمول خمیر و تست حضوری</div>
        </div>
      </div>
      <div class="editorial-box">
        <p><strong>۱. قالب دوم هدیه (ارزش ۳۵ میلیون تومان):</strong> راه‌اندازی دو خط تولید مجزا با ۱ دستگاه.</p>
        <p style="margin-top:4px;"><strong>۲. آموزش فرمولاسیون طلایی:</strong> تولید خمیر نرم و بدون پارگی از روز اول.</p>
        <p style="margin-top:4px;"><strong>۳. نقشه سه‌بعدی CAD کارگاه:</strong> چیدمان بهینه خط تولید متناسب با فضای شما.</p>
        <p style="margin-top:4px; color:#9ca3af;"><strong>۴. تست حضوری در کارگاه:</strong> پیش از تسویه نهایی، با مواد خودتان تست بگیرید.</p>
      </div>
    </div>
    <div class="slide-bottom-footer">
      <div class="footer-slug">EARLY-BIRD PACKAGE // 4 PILLARS</div>
      <div class="footer-brand">machinedesign.ir</div>
    </div>
  </article>

  <!-- Slide 4 -->
  <article class="slide bg-tech-grid" id="slide-4">
    <div class="slide-top-header">
      <div class="brand-mark"><span>Machine</span>Design</div>
      <div class="slide-counter">04 / 06</div>
    </div>
    <div class="slide-body">
      <div class="header-stack">
        <div class="eyebrow-row">
          <span class="category-pill">اقتصاد کارگاه و توجیه مالی</span>
          <span class="eyebrow-text">ROI BREAKDOWN</span>
        </div>
        <h2 class="slide-h2">صرفه‌جویی ماهیانه <span>۹۰ میلیون تومان حقوق کارگر</span></h2>
      </div>
      <div class="split-banner">
        <img src="asset_05_roi_comparison.jpg" alt="ROI Comparison">
      </div>
      <div class="points-stack">
        <div class="point-item">
          <div class="point-num-box">۰۱</div>
          <div class="point-detail">
            <h4>جایگزینی کار دستی با ۱ اپراتور ساده</h4>
            <p>خداحافظی با چنگال‌پیچی دستی، خستگی نیرو و تاخیر؛ ۱ اپراتور کار ۱۰ کارگر ماهر را انجام می‌دهد.</p>
          </div>
        </div>
        <div class="point-item">
          <div class="point-num-box">۰۲</div>
          <div class="point-detail">
            <h4>بازگشت کامل سرمایه زیر ۳ ماه</h4>
            <p>صرفه‌جویی چشمگیر در دستمزد و حذف ضایعات خمیر، تمام هزینه دستگاه را در کمتر از ۹۰ روز برمی‌گرداند.</p>
          </div>
        </div>
      </div>
    </div>
    <div class="slide-bottom-footer">
      <div class="footer-slug">ROI // LABOR SAVINGS</div>
      <div class="footer-brand">machinedesign.ir</div>
    </div>
  </article>

  <!-- Slide 5 -->
  <article class="slide bg-tech-grid" id="slide-5">
    <div class="slide-top-header">
      <div class="brand-mark"><span>Machine</span>Design</div>
      <div class="slide-counter">05 / 06</div>
    </div>
    <div class="slide-body">
      <div class="header-stack">
        <div class="eyebrow-row">
          <span class="category-pill">گارانتی رسمی و زمان‌بندی</span>
          <span class="eyebrow-text">QUALITY ASSURANCE</span>
        </div>
        <h2 class="slide-h2">۱ سال گارانتی رسمی + <span>۱۰ سال تامین قطعات در تهران</span></h2>
      </div>
      <div class="points-stack" style="margin-top:10px;">
        <div class="point-item">
          <div class="point-num-box">۰۱</div>
          <div class="point-detail">
            <h4>تامین دائمی قطعات و استانداردهای غذایی</h4>
            <p>کلیه قطعات مصرفی، تسمه‌ها، پمپ و درام‌ها در انبار تهران دپو شده و بدنه تمام استیل ۳۰۴ است.</p>
          </div>
        </div>
        <div class="point-item">
          <div class="point-num-box">۰۲</div>
          <div class="point-detail">
            <h4>تحویل و راه‌اندازی در آذرماه ۱۴۰۵</h4>
            <p>پارت اول با نصب، راه‌اندازی و آموزش حضوری توسط تیم فنی ماشین دیزاین در محل کارگاه تحویل می‌شود.</p>
          </div>
        </div>
      </div>
    </div>
    <div class="slide-bottom-footer">
      <div class="footer-slug">WARRANTY // TEHRAN SUPPORT</div>
      <div class="footer-brand">machinedesign.ir</div>
    </div>
  </article>

  <!-- Slide 6 -->
  <article class="slide bg-tech-grid" id="slide-6">
    <div class="slide-top-header">
      <div class="brand-mark"><span>Machine</span>Design</div>
      <div class="slide-counter">06 / 06</div>
    </div>
    <div class="slide-body">
      <div class="header-stack">
        <div class="eyebrow-row">
          <span class="category-pill">رزرو سهمیه پارت اول</span>
          <span class="eyebrow-text">FINAL CALL</span>
        </div>
        <h2 class="slide-h2">ظرفیت پارت اول <span>فقط ۵ دستگاه است</span></h2>
      </div>
      <div class="pillars-stack">
        <div class="pillar-row">
          <span class="pillar-num">۰۱</span>
          <span>تست حضوری رایگان در کارگاه با مواد شما قبل از تسویه</span>
        </div>
        <div class="pillar-row">
          <span class="pillar-num">۰۲</span>
          <span>مشاوره فنی و انتخاب قالب متناسب با نوع خوراک هدف</span>
        </div>
        <div class="pillar-row">
          <span class="pillar-num">۰۳</span>
          <span>امکان پرداخت مرحله‌ای متناسب با پیشرفت تولید</span>
        </div>
      </div>
      <div class="cta-card">
        <div class="cta-badge">EARLY-BIRD REGISTRATION // 5 UNITS</div>
        <div class="cta-action">ارسال کلمه «رزرو» در دایرکت</div>
        <div class="cta-web">تماس مستقیم: ۰۹۳۵۸۶۸۹۸۲۹ | machinedesign.ir</div>
      </div>
    </div>
    <div class="slide-bottom-footer">
      <div class="footer-slug">CALL TO ACTION // RESERVE</div>
      <div class="footer-brand">@h.vatan.doust</div>
    </div>
  </article>
</body>
</html>
"""

def render_decks():
    # 1. Write HTML files into VISUALS_DIR
    f_dough = os.path.join(VISUALS_DIR, "deck_dough.html")
    f_molds = os.path.join(VISUALS_DIR, "deck_molds.html")
    f_early = os.path.join(VISUALS_DIR, "deck_early_bird.html")

    with open(f_dough, "w", encoding="utf-8") as f:
        f.write(build_html_dough())
    with open(f_molds, "w", encoding="utf-8") as f:
        f.write(build_html_molds())
    with open(f_early, "w", encoding="utf-8") as f:
        f.write(build_html_early_bird())

    print("[+] HTML decks created.")

    # 2. Start HTTP server
    server, port = start_local_server(VISUALS_DIR)
    print(f"[*] Local HTTP server listening on port {port}")

    # 3. Setup Headless Chrome at 3x scale factor (360x450 * 3 = 1080x1350)
    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--window-size=2400,3600')
    opts.add_argument('--force-device-scale-factor=3')
    opts.add_argument('--hide-scrollbars')

    driver = webdriver.Chrome(options=opts)

    decks = [
        ("deck_dough.html", "carousel_dough", 4, "carousel_dough_slide"),
        ("deck_molds.html", "carousel_molds", 4, "carousel_molds_slide"),
        ("deck_early_bird.html", "carousel_early_bird", 6, "carousel_early_bird_slide"),
    ]

    try:
        for html_file, folder_name, slide_count, prefix in decks:
            url = f"http://127.0.0.1:{port}/{html_file}"
            print(f"[*] Rendering {url} ({slide_count} slides)...")
            driver.get(url)
            time.sleep(3.5)

            target_dir = os.path.join(VISUALS_DIR, folder_name)
            os.makedirs(target_dir, exist_ok=True)

            for sid in range(1, slide_count + 1):
                elem = driver.find_element(By.ID, f"slide-{sid}")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", elem)
                time.sleep(0.3)
                png_path = os.path.join(target_dir, f"{prefix}_{sid:02d}.png")
                jpg_path = os.path.join(target_dir, f"{prefix}_{sid:02d}.jpg")
                elem.screenshot(png_path)

                # Convert to high-quality JPEG
                im = Image.open(png_path).convert("RGB")
                im.save(jpg_path, "JPEG", quality=95)
                os.remove(png_path)  # Keep clean JPEG
                print(f"    [+] Saved slide {sid:02d} -> {jpg_path}")

        print("\n[OK] All 14 slides across 3 carousels successfully rendered in 1080x1350 resolution!")

    finally:
        driver.quit()
        server.shutdown()

if __name__ == '__main__':
    render_decks()
