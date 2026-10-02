import os
from PIL import Image, ImageDraw, ImageFont

def edit_floorplan_perfect():
    src_path = "/home/ubuntu/.hermes/profiles/profil-admin-mvp/cache/images/img_57d645ce90ef.jpg"
    ifp_path = "/home/ubuntu/.hermes/profiles/profil-admin-mvp/cache/images/img_fe34b56150d0.jpg"
    
    img = Image.open(src_path).convert("RGBA")
    w, h = img.size
    
    overlay = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    try:
        font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)
        font_head = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9)
    except:
        font_bold = ImageFont.load_default()
        font_sub = font_bold
        font_head = font_bold

    # 1. Clean All 15 Pencil Handwriting Areas completely
    pencil_boxes = [
        # North Rooms (1 to 8)
        (205, 165, 255, 230),
        (275, 165, 330, 230),
        (350, 165, 405, 240),
        (420, 205, 475, 310), # Room 4 (IFP 86 + CRS)
        (500, 210, 555, 310), # Room 5 (IFP 86 + CRS)
        (575, 195, 630, 270),
        (638, 200, 690, 275),
        (710, 190, 765, 265),
        
        # South Rooms (1 to 7)
        (170, 400, 260, 450), # Kelas Besar Barat (CRS + IFP 86)
        (270, 410, 325, 460),
        (345, 410, 400, 460),
        (525, 410, 570, 460),
        (575, 395, 620, 460),
        (630, 410, 685, 460),
        (700, 405, 790, 450), # Kelas Besar Timur (CRS + IFP 86)
    ]
    
    paper_color = (246, 246, 246, 255)
    for bx in pencil_boxes:
        draw.rectangle(bx, fill=paper_color)

    # 2. Define clean tag positions and wall display locations for each of the 15 rooms
    rooms_data = [
        # NORTH WING
        {"name": "IFP 75\"", "tx": 208, "ty": 175, "wx": 262, "wy": 185, "crs": False},
        {"name": "IFP 75\"", "tx": 278, "ty": 175, "wx": 334, "wy": 185, "crs": False},
        {"name": "IFP 75\"", "tx": 352, "ty": 175, "wx": 405, "wy": 185, "crs": False},
        {"name": "IFP 86\" + CRS", "tx": 422, "ty": 215, "wx": 485, "wy": 215, "crs": True},
        {"name": "IFP 86\" + CRS", "tx": 502, "ty": 220, "wx": 562, "wy": 220, "crs": True},
        {"name": "IFP 75\"", "tx": 580, "ty": 205, "wx": 632, "wy": 205, "crs": False},
        {"name": "IFP 75\"", "tx": 642, "ty": 210, "wx": 700, "wy": 210, "crs": False},
        {"name": "IFP 75\"", "tx": 714, "ty": 200, "wx": 765, "wy": 200, "crs": False},

        # SOUTH WING
        {"name": "IFP 86\" + CRS", "tx": 178, "ty": 412, "wx": 262, "wy": 420, "crs": True},
        {"name": "IFP 75\"", "tx": 275, "ty": 415, "wx": 334, "wy": 425, "crs": False},
        {"name": "IFP 75\"", "tx": 350, "ty": 415, "wx": 405, "wy": 425, "crs": False},
        {"name": "IFP 75\"", "tx": 528, "ty": 415, "wx": 556, "wy": 425, "crs": False},
        {"name": "IFP 75\"", "tx": 578, "ty": 405, "wx": 625, "wy": 425, "crs": False},
        {"name": "IFP 75\"", "tx": 634, "ty": 415, "wx": 692, "wy": 425, "crs": False},
        {"name": "IFP 86\" + CRS", "tx": 708, "ty": 412, "wx": 760, "wy": 420, "crs": True},
    ]

    # 3. Draw Clean CAD Tags & East Wall Displays
    for r in rooms_data:
        tx, ty = r["tx"], r["ty"]
        wx, wy = r["wx"], r["wy"]
        is_crs = r["crs"]
        
        # Color Theme: Red for 75" and Blue for 86"+CRS (Floor 2 standard)
        text_color = (200, 10, 30, 255) if not is_crs else (0, 75, 170, 255)
        border_color = (200, 10, 30, 255) if not is_crs else (0, 75, 170, 255)
        tag_bg = (255, 255, 255, 250)
        
        tw = 58 if is_crs else 44
        th = 23
        
        # Tag box
        draw.rectangle([tx, ty, tx + tw, ty + th], fill=tag_bg, outline=border_color, width=1)
        draw.text((tx + 3, ty + 2), r["name"], fill=text_color, font=font_bold if not is_crs else font_head)
        draw.text((tx + 3, ty + 12), "+SL dll", fill=(70, 70, 70, 255), font=font_sub)
        
        # Physical Display Box on East Wall (menempel di dinding timur)
        disp_h = 20 if is_crs else 16
        draw.rectangle([wx - 2, wy - disp_h//2, wx + 3, wy + disp_h//2], fill=(20, 20, 20, 255), outline=border_color, width=2)
        draw.line([wx, wy - disp_h//2 + 2, wx, wy + disp_h//2 - 2], fill=(0, 240, 240, 255) if is_crs else (30, 200, 30, 255), width=2)
        
        # Leader line from tag to display
        draw.line([tx + tw, ty + th//2, wx - 3, wy], fill=border_color, width=1)

    # 4. Insert IFP Evidence Photo in the Clean Left Margin (Outside the building)
    if os.path.exists(ifp_path):
        ifp_raw = Image.open(ifp_path).convert("RGBA")
        
        # Fit nicely in left outside area: X: 15 to 145, Y: 130 to 320
        inset_w = 125
        inset_h = int(ifp_raw.height * (inset_w / ifp_raw.width))
        ifp_resized = ifp_raw.resize((inset_w, inset_h), Image.Resampling.LANCZOS)
        
        ins_x = 15
        ins_y = 135
        card_w = inset_w + 8
        card_h = inset_h + 34
        
        # Draw frame card
        draw.rectangle([ins_x, ins_y, ins_x + card_w, ins_y + card_h], fill=(255, 255, 255, 250), outline=(0, 75, 170, 255), width=2)
        draw.rectangle([ins_x, ins_y, ins_x + card_w, ins_y + 16], fill=(0, 75, 170, 255))
        draw.text((ins_x + 6, ins_y + 2), "EVIDEN BENTUK IFP", fill=(255, 255, 255, 255), font=font_head)
        
        # Paste IFP image
        overlay.paste(ifp_resized, (ins_x + 4, ins_y + 18), ifp_resized)
        
        draw.text((ins_x + 6, ins_y + inset_h + 20), "Interactive Flat Panel", fill=(50, 50, 50, 255), font=font_sub)

    # 5. Composite overlay with original blueprint image
    final_img = Image.alpha_composite(img, overlay).convert("RGB")
    
    output_path = "/home/ubuntu/DENAH_LANTAI_03_EDITED_ORIGINAL.jpg"
    final_img.save(output_path, quality=95)
    print(f"Successfully edited blueprint image: {output_path}")
    return output_path

if __name__ == "__main__":
    edit_floorplan_perfect()
