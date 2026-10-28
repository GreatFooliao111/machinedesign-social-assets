import os
import sys
from PIL import Image

def slice_2x2_master_sheet(image_path, output_dir, prefix="slide", seam_inset=4, outer_inset=2):
    """
    Slices a 2x2 master sheet into 4 individual 1080x1350 slides.
    seam_inset: pixels to shave off the central dividing seams (both vertical and horizontal)
                to completely eliminate divider lines or white borders.
    outer_inset: pixels to shave off outer boundaries.
    """
    os.makedirs(output_dir, exist_ok=True)
    with Image.open(image_path) as im:
        w, h = im.size
        print(f"Master sheet loaded: {image_path} ({w}x{h})")
        
        half_w = w / 2.0
        half_h = h / 2.0
        
        # Calculate bounding boxes that skip the central seam lines and outer edges
        boxes = [
            # Slide 01: Top-Left
            (outer_inset, outer_inset, half_w - seam_inset, half_h - seam_inset),
            # Slide 02: Top-Right
            (half_w + seam_inset, outer_inset, w - outer_inset, half_h - seam_inset),
            # Slide 03: Bottom-Left
            (outer_inset, half_h + seam_inset, half_w - seam_inset, h - outer_inset),
            # Slide 04: Bottom-Right
            (half_w + seam_inset, half_h + seam_inset, w - outer_inset, h - outer_inset)
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
        print("Usage: python slice_grid.py <input_master_image> <output_dir> [prefix] [seam_inset]")
        sys.exit(1)
    
    img_in = sys.argv[1]
    out_dir = sys.argv[2]
    pref = sys.argv[3] if len(sys.argv) > 3 else "slide"
    seam = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    slice_2x2_master_sheet(img_in, out_dir, pref, seam_inset=seam)
