import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def edit_floorplan_with_evidence():
    # 1. Load source blueprint image
    src_path = "/home/ubuntu/.hermes/profiles/profil-admin-mvp/cache/images/img_57d645ce90ef.jpg"
    ifp_path = "/home/ubuntu/.hermes/profiles/profil-admin-mvp/cache/images/img_fe34b56150d0.jpg"
    
    img = Image.open(src_path).convert("RGBA")
    w, h = img.size
    
    # Overlay layer for drawing crisp vector graphics
    overlay = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Fonts
    try:
        font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 11)
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9)
        font_tiny = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)
    except:
        font_bold = ImageFont.load_default()
        font_large = font_bold
        font_small = font_bold
        font_tiny = font_bold

    # 2. Points configuration based on exact blueprint coordinates and pencil locations
    # Style matches Floor 2 reference: Red text, clean boxes, +SL dll
    points_north = [
        {"name": "IFP 75\"", "wall_x": 263, "wall_y": 150, "tag_x": 212, "tag_y": 140, "type": "75", "crs": False, "mask_w": 46, "mask_h": 26},
        {"name": "IFP 75\"", "wall_x": 334, "wall_y": 150, "tag_x": 283, "tag_y": 140, "type": "75", "crs": False, "mask_w": 46, "mask_h": 26},
        {"name": "IFP 75\"", "wall_x": 405, "wall_y": 150, "tag_x": 354, "tag_y": 140, "type": "75", "crs": False, "mask_w": 46, "mask_h": 26},
        {"name": "IFP 86\" + CRS", "wall_x": 485, "wall_y": 155, "tag_x": 425, "tag_y": 140, "type": "86", "crs": True, "mask_w": 58, "mask_h": 28},
        {"name": "IFP 86\" + CRS", "wall_x": 562, "wall_y": 155, "tag_x": 500, "tag_y": 140, "type": "86", "crs": True, "mask_w": 58, "mask_h": 28},
        {"name": "IFP 75\"", "wall_x": 632, "wall_y": 155, "tag_x": 580, "tag_y": 140, "type": "75", "crs": False, "mask_w": 46, "mask_h": 26},
        {"name": "IFP 75\"", "wall_x": 700, "wall_y": 155, "tag_x": 650, "tag_y": 140, "type": "75", "crs": False, "mask_w": 46, "mask_h": 26},
        {"name": "IFP 75\"", "wall_x": 765, "wall_y": 155, "tag_x": 718, "tag_y": 140, "type": "75", "crs": False, "mask_w": 46, "mask_h": 26},
    ]

    points_south = [
        {"name": "IFP 86\" + CRS", "wall_x": 263, "wall_y": 390, "tag_x": 190, "tag_y": 380, "type": "86", "crs": True, "mask_w": 65, "mask_h": 28},
        {"name": "IFP 75\"", "wall_x": 334, "wall_y": 390, "tag_x": 278, "tag_y": 380, "type": "75", "crs": False, "mask_w": 46, "mask_h": 26},
        {"name": "IFP 75\"", "wall_x": 405, "wall_y": 390, "tag_x": 350, "tag_y": 380, "type": "75", "crs": False, "mask_w": 46, "mask_h": 26},
        {"name": "IFP 75\"", "wall_x": 556, "wall_y": 390, "tag_x": 510, "tag_y": 380, "type": "75", "crs": False, "mask_w": 46, "mask_h": 26},
        {"name": "IFP 75\"", "wall_x": 625, "wall_y": 390, "tag_x": 575, "tag_y": 380, "type": "75", "crs": False, "mask_w": 46, "mask_h": 26},
        {"name": "IFP 75\"", "wall_x": 692, "wall_y": 390, "tag_x": 642, "tag_y": 380, "type": "75", "crs": False, "mask_w": 46, "mask_h": 26},
        {"name": "IFP 86\" + CRS", "wall_x": 760, "wall_y": 390, "tag_x": 700, "tag_y": 380, "type": "86", "crs": True, "mask_w": 65, "mask_h": 28},
    ]

    all_points = points_north + points_south

    # Extra pencil mark cleanups (e.g. CRS written near bottom of room 4 and 5, and handwritten numbers)
    extra_masks = [
        (425, 275, 475, 305), # CRS pencil mark in room 4
        (500, 275, 550, 305), # CRS pencil mark in room 5
        # Clean extra handwritten numbers if any
        (205, 130, 260, 175),
        (275, 130, 330, 175),
        (345, 130, 400, 175),
        (420, 130, 480, 175),
        (495, 130, 555, 175),
        (575, 130, 630, 175),
        (645, 130, 700, 175),
        (715, 130, 765, 175),
        # South rooms pencil regions
        (185, 370, 260, 412),
        (275, 370, 330, 412),
        (345, 370, 400, 412),
        (505, 370, 555, 412),
        (570, 370, 625, 412),
        (638, 370, 690, 412),
        (695, 370, 760, 412),
    ]
    for em in extra_masks:
        draw.rectangle(em, fill=(244, 244, 244, 255))

    # 3. Draw Clean CAD Tags & Display Markers onto each room
    for pt in all_points:
        wx, wy = pt["wall_x"], pt["wall_y"]
        tx, ty = pt["tag_x"], pt["tag_y"]
        is_crs = pt["crs"]
        
        # Color theme: Red for 75" and Blue for 86"+CRS (Floor 2 style)
        text_color = (220, 20, 60, 255) if not is_crs else (0, 90, 180, 255)
        box_border = (200, 0, 0, 255) if not is_crs else (0, 80, 180, 255)
        tag_bg = (255, 255, 255, 250)

        # Draw Physical Display Box menempel di dinding timur
        disp_h = 24 if is_crs else 18
        draw.rectangle([wx - 3, wy - disp_h//2, wx + 4, wy + disp_h//2], fill=(20, 20, 20, 255), outline=box_border, width=2)
        # Inner screen line
        draw.line([wx, wy - disp_h//2 + 2, wx, wy + disp_h//2 - 2], fill=(0, 255, 255, 255) if is_crs else (50, 205, 50, 255), width=2)

        # Text strings
        text_str = pt["name"]
        sub_str = "+SL dll"
        
        tw = pt.get("mask_w", 55)
        th = pt.get("mask_h", 26)
        
        # Clean white wipeout box over pencil handwriting
        draw.rectangle([tx, ty, tx + tw, ty + th], fill=tag_bg, outline=box_border, width=1)
        
        # Text positioning
        draw.text((tx + 3, ty + 2), text_str, fill=text_color, font=font_small if is_crs else font_bold)
        draw.text((tx + 3, ty + 14), sub_str, fill=(80, 80, 80, 255), font=font_tiny)
        
        # Leader line from tag to wall display
        draw.line([tx + tw, ty + th//2, wx - 4, wy], fill=box_border, width=1)

    # 4. Insert IFP Evidence Image (img_fe34b56150d0.jpg) as an Inset on the blueprint
    if os.path.exists(ifp_path):
        ifp_raw = Image.open(ifp_path).convert("RGBA")
        
        # Resize thumbnail to fit nicely on the void / open area or title block area
        thumb_w = 210
        thumb_h = int(ifp_raw.height * (thumb_w / ifp_raw.width))
        ifp_resized = ifp_raw.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        
        # Inset Position in the Central Void area (X: 375, Y: 245) where space is open!
        inset_x = 372
        inset_y = 238
        
        # Draw frame card for the evidence image
        card_w = thumb_w + 14
        card_h = thumb_h + 38
        
        # Shadow
        draw.rectangle([inset_x + 3, inset_y + 3, inset_x + card_w + 3, inset_y + card_h + 3], fill=(0, 0, 0, 80))
        # Card Background
        draw.rectangle([inset_x, inset_y, inset_x + card_w, inset_y + card_h], fill=(255, 255, 255, 245), outline=(0, 102, 204, 255), width=2)
        
        # Header text
        draw.rectangle([inset_x, inset_y, inset_x + card_w, inset_y + 18], fill=(0, 102, 204, 255))
        draw.text((inset_x + 8, inset_y + 3), "EVIDEN BENTUK IFP (75\" & 86\")", fill=(255, 255, 255, 255), font=font_small)
        
        # Paste resized IFP picture
        overlay.paste(ifp_resized, (inset_x + 7, inset_y + 22), ifp_resized)
        
        # Caption below picture
        draw.text((inset_x + 8, inset_y + thumb_h + 24), "Interactive Flat Panel Display Screen", fill=(50, 50, 50, 255), font=font_tiny)

    # 5. Composite overlay with original blueprint image
    final_img = Image.alpha_composite(img, overlay).convert("RGB")
    
    # Save directly
    output_path = "/home/ubuntu/.hermes/profiles/profil-admin-mvp/cache/images/img_57d645ce90ef_EDITED.jpg"
    final_img.save(output_path, quality=95)
    print(f"Successfully edited blueprint image: {output_path}")
    return output_path

if __name__ == "__main__":
    edit_floorplan_with_evidence()
