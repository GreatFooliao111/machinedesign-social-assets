#!/usr/bin/env python3
"""
MachineDesign.ir - Video Reels Production & Mobile Simulation Template Engine
Builds high-legibility vertical engineering reels (1080x1920) with pure vector/HUD overlays,
smart audio ducking (ambient + voiceover + background music), smooth fadeout,
and automated mobile viewport (390x693) readability inspection.
"""

import os
import sys
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

WIDTH, HEIGHT = 1080, 1920
NEON_GREEN = (140, 231, 12)       # #8ce70c
DARK_BG = (8, 14, 24, 240)         # High-opacity glass dark
CARD_BORDER = (45, 68, 96, 240)    # Crisp tech border
WHITE = (255, 255, 255, 255)
LIGHT_NEON = (210, 255, 140, 255)
TEXT_MUTED = (160, 185, 210, 255)

def shape(text):
    return get_display(arabic_reshaper.reshape(text))

def load_fonts(font_dir):
    return {
        "vazir_black": ImageFont.truetype(os.path.join(font_dir, "Vazirmatn-Black.ttf"), 56),
        "vazir_bold_42": ImageFont.truetype(os.path.join(font_dir, "Vazirmatn-Bold.ttf"), 42),
        "vazir_bold_40": ImageFont.truetype(os.path.join(font_dir, "Vazirmatn-Bold.ttf"), 40),
        "vazir_bold_36": ImageFont.truetype(os.path.join(font_dir, "Vazirmatn-Bold.ttf"), 36),
        "vazir_bold_34": ImageFont.truetype(os.path.join(font_dir, "Vazirmatn-Bold.ttf"), 34),
        "vazir_black_phone": ImageFont.truetype(os.path.join(font_dir, "Vazirmatn-Black.ttf"), 52),
        "vazir_black_cta": ImageFont.truetype(os.path.join(font_dir, "Vazirmatn-Black.ttf"), 48),
        "vazir_black_h1": ImageFont.truetype(os.path.join(font_dir, "Vazirmatn-Black.ttf"), 60),
        "orbitron_30": ImageFont.truetype(os.path.join(font_dir, "Orbitron.ttf"), 30),
        "orbitron_28": ImageFont.truetype(os.path.join(font_dir, "Orbitron.ttf"), 28),
        "orbitron_26": ImageFont.truetype(os.path.join(font_dir, "Orbitron.ttf"), 26),
        "orbitron_24": ImageFont.truetype(os.path.join(font_dir, "Orbitron.ttf"), 24),
        "orbitron_22": ImageFont.truetype(os.path.join(font_dir, "Orbitron.ttf"), 22),
    }

def draw_top_bar(draw, fonts, brand_title, model_id, live_badge="LIVE DEMO"):
    px, py, pw, ph = 50, 110, 980, 105
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(6, 12, 20, 230), outline=CARD_BORDER, width=2)
    draw.text((px + 32, py + 34), brand_title, font=fonts["orbitron_30"], fill=WHITE)
    draw.text((px + 420, py + 34), f"// {model_id}", font=fonts["orbitron_30"], fill=NEON_GREEN)
    draw.ellipse([px + pw - 225, py + 43, px + pw - 205, py + 63], fill=NEON_GREEN)
    draw.text((px + pw - 190, py + 38), live_badge, font=fonts["orbitron_22"], fill=WHITE)

def draw_hud_overlay(fonts, brand_cfg, seg_cfg, out_path):
    im = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    draw_top_bar(draw, fonts, brand_cfg["top_bar_title"], brand_cfg["model_id"])
    
    cx, cy, cw, ch = 40, 1330, 1000, 340
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=28, fill=DARK_BG, outline=CARD_BORDER, width=3)
    draw.line([cx + 40, cy, cx + 220, cy], fill=NEON_GREEN, width=6)
    
    # Badge Pill
    bbox_b = draw.textbbox((0, 0), seg_cfg["badge"], font=fonts["orbitron_24"])
    bw_badge = (bbox_b[2] - bbox_b[0]) + 30
    draw.rounded_rectangle([cx + 35, cy + 24, cx + 35 + bw_badge, cy + 68], radius=12, fill=(18, 32, 22, 220), outline=NEON_GREEN, width=1)
    draw.text((cx + 50, cy + 32), seg_cfg["badge"], font=fonts["orbitron_24"], fill=NEON_GREEN)
    
    # Persian Title (56pt Vazirmatn-Black)
    reshaped_title = shape(seg_cfg["title"])
    bbox_title = draw.textbbox((0, 0), reshaped_title, font=fonts["vazir_black"])
    draw.text((cx + cw - 45 - (bbox_title[2] - bbox_title[0]), cy + 96), reshaped_title, font=fonts["vazir_black"], fill=WHITE)
    
    # Persian Subtitle (40pt Vazirmatn-Bold Pure White)
    reshaped_sub = shape(seg_cfg["subtitle"])
    bbox_sub = draw.textbbox((0, 0), reshaped_sub, font=fonts["vazir_bold_40"])
    draw.text((cx + cw - 45 - (bbox_sub[2] - bbox_sub[0]), cy + 196), reshaped_sub, font=fonts["vazir_bold_40"], fill=WHITE)
    
    # Indicator bar
    draw.line([cx + 45, cy + ch - 20, cx + cw - 45, cy + ch - 20], fill=(25, 42, 60, 200), width=2)
    draw.line([cx + cw - 240, cy + ch - 20, cx + cw - 45, cy + ch - 20], fill=NEON_GREEN, width=2)
    
    im.save(out_path)
    return out_path

def draw_outro_card(fonts, brand_cfg, outro_cfg, out_path):
    im = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    draw.rectangle([0, 0, WIDTH, HEIGHT], fill=(5, 9, 16, 245))
    bx, by, bw, bh = 40, 260, 1000, 1400
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=36, fill=(10, 18, 28, 255), outline=NEON_GREEN, width=3)
    
    # Top Tag
    b_tag = draw.textbbox((0, 0), outro_cfg["tag"], font=fonts["orbitron_24"])
    draw.text((bx + (bw - (b_tag[2]-b_tag[0]))//2, by + 50), outro_cfg["tag"], font=fonts["orbitron_24"], fill=NEON_GREEN)
    
    # H1 Title
    t1 = shape(outro_cfg["title"])
    b1 = draw.textbbox((0, 0), t1, font=fonts["vazir_black_h1"])
    draw.text((bx + (bw - (b1[2]-b1[0]))//2, by + 105), t1, font=fonts["vazir_black_h1"], fill=WHITE)
    
    # Subtitle
    t2 = shape(outro_cfg["subtitle"])
    b2 = draw.textbbox((0, 0), t2, font=fonts["vazir_bold_42"])
    draw.text((bx + (bw - (b2[2]-b2[0]))//2, by + 205), t2, font=fonts["vazir_bold_42"], fill=NEON_GREEN)
    draw.line([bx + 80, by + 290, bx + bw - 80, by + 290], fill=(30, 50, 75), width=2)
    
    # Feature rows
    start_y = by + 340
    row_height = 85
    for i, f_text in enumerate(outro_cfg["features"]):
        fy = start_y + i * row_height
        draw.rounded_rectangle([bx + 50, fy, bx + bw - 50, fy + 70], radius=16, fill=(16, 26, 40, 230), outline=(35, 55, 80), width=1)
        draw.ellipse([bx + bw - 95, fy + 26, bx + bw - 77, fy + 44], fill=NEON_GREEN)
        tf = shape(f_text)
        bf = draw.textbbox((0, 0), tf, font=fonts["vazir_bold_36"])
        draw.text((bx + bw - 120 - (bf[2]-bf[0]), fy + 12), tf, font=fonts["vazir_bold_36"], fill=WHITE)
        
    # Big CTA Button
    btn_x, btn_y, btn_w, btn_h = bx + 50, by + 740, bw - 100, 155
    draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=28, fill=NEON_GREEN)
    t_btn = shape(outro_cfg["cta_button"])
    b_btn = draw.textbbox((0, 0), t_btn, font=fonts["vazir_black_cta"])
    draw.text((btn_x + (btn_w - (b_btn[2]-b_btn[0]))//2, btn_y + 44), t_btn, font=fonts["vazir_black_cta"], fill=(6, 16, 6))
    
    # Phone card
    phone_card_y = by + 940
    draw.rounded_rectangle([bx + 50, phone_card_y, bx + bw - 50, phone_card_y + 260], radius=24, fill=(14, 22, 34, 255), outline=CARD_BORDER, width=2)
    t_consult = shape(outro_cfg["consultation_label"])
    b_consult = draw.textbbox((0, 0), t_consult, font=fonts["vazir_bold_34"])
    draw.text((bx + (bw - (b_consult[2]-b_consult[0]))//2, phone_card_y + 35), t_consult, font=fonts["vazir_bold_34"], fill=LIGHT_NEON)
    
    t_phone = shape(brand_cfg["phone_display"])
    b_phone = draw.textbbox((0, 0), t_phone, font=fonts["vazir_black_phone"])
    draw.text((bx + (bw - (b_phone[2]-b_phone[0]))//2, phone_card_y + 102), t_phone, font=fonts["vazir_black_phone"], fill=NEON_GREEN)
    
    t_phone_en = f"TEL: {brand_cfg['phone_intl']}"
    b_phone_en = draw.textbbox((0, 0), t_phone_en, font=fonts["orbitron_28"])
    draw.text((bx + (bw - (b_phone_en[2]-b_phone_en[0]))//2, phone_card_y + 185), t_phone_en, font=fonts["orbitron_28"], fill=WHITE)
    
    # Footer Channels
    t_chan = outro_cfg["channels_footer"]
    b_chan = draw.textbbox((0, 0), t_chan, font=fonts["orbitron_28"])
    draw.text((bx + (bw - (b_chan[2]-b_chan[0]))//2, by + 1250), t_chan, font=fonts["orbitron_28"], fill=TEXT_MUTED)
    
    t_web = f"WWW.{brand_cfg['domain'].upper()}"
    b_web = draw.textbbox((0, 0), t_web, font=fonts["orbitron_26"])
    draw.text((bx + (bw - (b_web[2]-b_web[0]))//2, by + 1310), t_web, font=fonts["orbitron_26"], fill=NEON_GREEN)
    
    im.save(out_path)
    return out_path

def generate_mobile_simulation(video_or_image_path, out_sim_path, timestamp="5.0"):
    """Scale down to 390x693 for realistic mobile screen readability inspection."""
    if video_or_image_path.endswith((".mp4", ".mov", ".mkv")):
        cmd = [
            "ffmpeg", "-y",
            "-ss", timestamp, "-i", video_or_image_path,
            "-vframes", "1",
            "-vf", "scale=390:693:flags=lanczos",
            "-q:v", "2",
            out_sim_path
        ]
        subprocess.run(cmd, check=True)
    else:
        im = Image.open(video_or_image_path)
        im_sim = im.resize((390, 693), Image.Resampling.LANCZOS)
        im_sim.convert("RGB").save(out_sim_path, quality=95)
    return out_sim_path

if __name__ == "__main__":
    print("MachineDesign Video Reels Template Engine Initialized.")
