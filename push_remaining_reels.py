#!/usr/bin/env python3
"""
Sequentially commits and pushes reels 2 through 7 to GitHub.
"""

import os
import subprocess
import time

repo_dir = r"D:\Machinedesign.ir\machinedesign-social-assets"
reels = [
    ("reel_02_authentic_iranian_samosa.mp4", "add reel 02 authentic iranian samosa"),
    ("reel_03_jumbo_15cm_pirashki.mp4", "add reel 03 jumbo 15cm pirashki"),
    ("reel_04_labor_vs_machine_roi.mp4", "add reel 04 labor vs machine roi"),
    ("reel_05_chunky_meat_stuffing_pump.mp4", "add reel 05 chunky meat stuffing pump"),
    ("reel_06_single_phase_220v_startup.mp4", "add reel 06 single phase 220v startup"),
    ("reel_07_peace_of_mind_mashhad_test.mp4", "add reel 07 peace of mind mashhad test"),
]

for filename, desc in reels:
    rel_path = f"campaigns/launch-dumpling-series/03_video_reels/{filename}"
    print(f"\n[+] Staging and committing: {filename}...", flush=True)
    subprocess.run(["git", "add", rel_path], cwd=repo_dir, check=True)
    
    # Check if there is anything to commit
    res_status = subprocess.run(["git", "status", "--porcelain", rel_path], cwd=repo_dir, capture_output=True, text=True)
    if res_status.stdout.strip():
        subprocess.run(["git", "commit", "-m", f"feat(reels): {desc}"], cwd=repo_dir, check=True)
    
    # Push with retry
    pushed = False
    for attempt in range(1, 4):
        print(f"  -> Pushing {filename} (attempt {attempt})...", flush=True)
        res_push = subprocess.run(["git", "push", "origin", "main"], cwd=repo_dir, capture_output=True, text=True)
        if res_push.returncode == 0:
            print(f"  [OK] Successfully pushed {filename} to origin/main", flush=True)
            pushed = True
            break
        else:
            print(f"  [!] Push attempt {attempt} failed: {res_push.stderr[-200:].strip()}", flush=True)
            time.sleep(10)
    
    if not pushed:
        print(f"  [ERROR] Failed to push {filename} after 3 attempts!", flush=True)
        break
    
    time.sleep(3)

print("\nAll remaining reels processed successfully!", flush=True)
