import os
import sys
from PIL import Image

def slice_2x2_master_sheet(image_path, output_dir, prefix="slide"):
    """
    Slices a 2x2 master sheet into 4 individual 1080x1350 slides.
    Grid order:
      Panel 1: Top-Left (Row 0, Col 0)
      Panel 2: Top-Right (Row 0, Col 1)
      Panel 3: Bottom-Left (Row 1, Col 0)
      Panel 4: Bottom-Right (Row 1, Col 1)
    """
    os.makedirs(output_dir, exist_ok=True)
    with Image.open(image_path) as im:
        w, h = im.size
        print(f"Master sheet loaded: {image_path} ({w}x{h})")
        
        half_w = w / 2.0
        half_h = h / 2.0
        
        boxes = [
            (0, 0, half_w, half_h),           # Slide 01: Top-Left
            (half_w, 0, w, half_h),           # Slide 02: Top-Right
            (0, half_h, half_w, h),           # Slide 03: Bottom-Left
            (half_w, half_h, w, h)            # Slide 04: Bottom-Right
        ]
        
        output_paths = []
        for idx, box in enumerate(boxes, start=1):
            crop_im = im.crop(box)
            # Resize with Lanczos to exact target (1080, 1350)
            final_im = crop_im.resize((1080, 1350), Image.Resampling.LANCZOS)
            out_file = os.path.join(output_dir, f"{prefix}_{idx:02d}.jpg")
            final_im.save(out_file, quality=95)
            print(f"Saved: {out_file} (1080x1350)")
            output_paths.append(out_file)
            
        return output_paths

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python slice_grid.py <input_master_image> <output_dir> [prefix]")
        sys.exit(1)
    
    img_in = sys.argv[1]
    out_dir = sys.argv[2]
    pref = sys.argv[3] if len(sys.argv) > 3 else "slide"
    slice_2x2_master_sheet(img_in, out_dir, pref)
