import os
from PIL import Image, ImageDraw, ImageFont

def render_official_ded_floorplan():
    # 1. Base image from official DED PDF Page 4 (Lantai 03)
    p4_path = "/home/ubuntu/.hermes/profiles/profil-admin-mvp/cache/scratch/denah_upn_page-4.png"
    ifp_path = "/home/ubuntu/.hermes/profiles/profil-admin-mvp/cache/images/img_fe34b56150d0.jpg"
    
    img = Image.open(p4_path).convert("RGBA")
    w, h = img.size
    
    overlay = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    # High-res Fonts (for 2482x1755 canvas)
    try:
        font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        font_card_head = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        font_card_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    except:
        font_bold = ImageFont.load_default()
        font_sub = font_bold
        font_card_head = font_bold
        font_card_sub = font_bold

    # 2. Precise Coordinates on High-Res 2482x1755 Canvas
    rooms_north = [
        {"name": "IFP 75\"", "no": "1.", "wx": 580, "wy": 540, "tx": 470, "ty": 525, "crs": False},
        {"name": "IFP 75\"", "no": "2.", "wx": 810, "wy": 540, "tx": 700, "ty": 525, "crs": False},
        {"name": "IFP 75\"", "no": "3.", "wx": 1035, "wy": 540, "tx": 925, "ty": 525, "crs": False},
        {"name": "IFP 86\" + CRS", "no": "", "wx": 1250, "wy": 540, "tx": 1100, "ty": 525, "crs": True},
        {"name": "IFP 86\" + CRS", "no": "", "wx": 1475, "wy": 540, "tx": 1325, "ty": 525, "crs": True},
        {"name": "IFP 75\"", "no": "4.", "wx": 1700, "wy": 540, "tx": 1590, "ty": 525, "crs": False},
        {"name": "IFP 75\"", "no": "5.", "wx": 1925, "wy": 540, "tx": 1815, "ty": 525, "crs": False},
        {"name": "IFP 75\"", "no": "6.", "wx": 2150, "wy": 540, "tx": 2040, "ty": 525, "crs": False},
    ]

    rooms_south = [
        {"name": "IFP 86\" + CRS", "no": "", "wx": 580, "wy": 1050, "tx": 420, "ty": 1035, "crs": True},
        {"name": "IFP 75\"", "no": "7.", "wx": 810, "wy": 1050, "tx": 700, "ty": 1035, "crs": False},
        {"name": "IFP 75\"", "no": "8.", "wx": 1035, "wy": 1050, "tx": 925, "ty": 1035, "crs": False},
        {"name": "IFP 75\"", "no": "9.", "wx": 1555, "wy": 1050, "tx": 1445, "ty": 1035, "crs": False},
        {"name": "IFP 75\"", "no": "10.", "wx": 1700, "wy": 1050, "tx": 1590, "ty": 1035, "crs": False},
        {"name": "IFP 75\"", "no": "11.", "wx": 1845, "wy": 1050, "tx": 1735, "ty": 1035, "crs": False},
        {"name": "IFP 86\" + CRS", "no": "", "wx": 2150, "wy": 1050, "tx": 1990, "ty": 1035, "crs": True},
    ]

    all_rooms = rooms_north + rooms_south

    # 3. Draw Clean CAD Tags & Display Symbols (Matching DED Style)
    for r in all_rooms:
        tx, ty = r["tx"], r["ty"]
        wx, wy = r["wx"], r["wy"]
        is_crs = r["crs"]
        
        # Color theme: Red for 75" and Blue for 86"+CRS (Standard DED style from Floor 2)
        text_color = (210, 20, 40, 255) if not is_crs else (0, 80, 190, 255)
        border_color = (200, 10, 30, 255) if not is_crs else (0, 75, 180, 255)
        tag_bg = (255, 255, 255, 245)
        
        tag_label = f"{r['no']} {r['name']}" if r['no'] else r['name']
        tw = 145 if is_crs else 105
        th = 44
        
        # Tag Box
        draw.rectangle([tx, ty, tx + tw, ty + th], fill=tag_bg, outline=border_color, width=2)
        draw.text((tx + 6, ty + 4), tag_label, fill=text_color, font=font_bold)
        draw.text((tx + 6, ty + 24), "+SL dll", fill=(70, 70, 70, 255), font=font_sub)
        
        # Physical Display Box on East Wall (Menempel di dinding timur)
        disp_h = 36 if is_crs else 28
        draw.rectangle([wx - 4, wy - disp_h//2, wx + 6, wy + disp_h//2], fill=(20, 20, 20, 255), outline=border_color, width=3)
        draw.line([wx + 1, wy - disp_h//2 + 3, wx + 1, wy + disp_h//2 - 3], fill=(0, 240, 240, 255) if is_crs else (40, 210, 40, 255), width=3)
        
        # Leader line from tag to display
        draw.line([tx + tw, ty + th//2, wx - 5, wy], fill=border_color, width=2)

    # 4. Insert IFP Visual Evidence Card on Clean Left Margin (Outside Building)
    if os.path.exists(ifp_path):
        ifp_raw = Image.open(ifp_path).convert("RGBA")
        
        card_w = 280
        card_h_img = int(ifp_raw.height * ((card_w - 16) / ifp_raw.width))
        ifp_resized = ifp_raw.resize((card_w - 16, card_h_img), Image.Resampling.LANCZOS)
        
        ins_x = 80
        ins_y = 1250
        card_total_h = card_h_img + 65
        
        # Outer Card Frame
        draw.rectangle([ins_x, ins_y, ins_x + card_w, ins_y + card_total_h], fill=(255, 255, 255, 250), outline=(0, 75, 180, 255), width=3)
        # Header Banner
        draw.rectangle([ins_x, ins_y, ins_x + card_w, ins_y + 30], fill=(0, 75, 180, 255))
        draw.text((ins_x + 10, ins_y + 6), "EVIDEN BENTUK IFP (75\" & 86\")", fill=(255, 255, 255, 255), font=font_card_head)
        
        # Paste Image
        overlay.paste(ifp_resized, (ins_x + 8, ins_y + 36), ifp_resized)
        
        # Subtitle
        draw.text((ins_x + 10, ins_y + 36 + card_h_img + 8), "Interactive Flat Panel Display Screen", fill=(40, 40, 40, 255), font=font_card_sub)

    # 5. Composite with official DED
    final_img = Image.alpha_composite(img, overlay).convert("RGB")
    
    out_path = "/home/ubuntu/DENAH_REV_LANTAI_03_UPN_OFFICIAL.png"
    final_img.save(out_path, quality=95)
    print(f"Official DED floorplan generated: {out_path}")
    return out_path

if __name__ == "__main__":
    render_official_ded_floorplan()
