import os
from PIL import Image, ImageDraw, ImageFont

def render_corrected_official_ded():
    # Base image from official DED PDF Page 4 (Lantai 03)
    p4_path = "/home/ubuntu/.hermes/profiles/profil-admin-mvp/cache/scratch/denah_upn_page-4.png"
    ifp_path = "/home/ubuntu/.hermes/profiles/profil-admin-mvp/cache/images/img_fe34b56150d0.jpg"
    
    img = Image.open(p4_path).convert("RGBA")
    w, h = img.size
    
    overlay = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Fonts
    try:
        font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
        font_card_head = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        font_card_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    except:
        font_bold = ImageFont.load_default()
        font_sub = font_bold
        font_card_head = font_bold
        font_card_sub = font_bold

    # -------------------------------------------------------------------------
    # CORRECT PLACEMENT RULE (ACUAN RESMI DED LANTAI 02):
    # Seluruh display IFP dipasang di DINDING DEPAN YANG MENGHADAP SELASAR (KORIDOR TENGAH):
    # - Sayap Utara: Di Dinding SELATAN ruangan (menghadap ke selasar tengah).
    # - Sayap Selatan: Di Dinding UTARA ruangan (menghadap ke selasar tengah).
    # -------------------------------------------------------------------------

    # NORTH WING ROOMS (Dinding Selatan / Y ≈ 665)
    rooms_north = [
        {"name": "IFP 75\"", "no": "1.", "wx": 460, "wy": 665, "tx": 405, "ty": 595, "crs": False},
        {"name": "IFP 75\"", "no": "2.", "wx": 690, "wy": 665, "tx": 635, "ty": 595, "crs": False},
        {"name": "IFP 75\"", "no": "3.", "wx": 920, "wy": 665, "tx": 865, "ty": 595, "crs": False},
        {"name": "IFP 86\" + CRS", "no": "", "wx": 1140, "wy": 665, "tx": 1060, "ty": 595, "crs": True},
        {"name": "IFP 86\" + CRS", "no": "", "wx": 1370, "wy": 665, "tx": 1290, "ty": 595, "crs": True},
        {"name": "IFP 75\"", "no": "4.", "wx": 1590, "wy": 665, "tx": 1535, "ty": 595, "crs": False},
        {"name": "IFP 75\"", "no": "5.", "wx": 1815, "wy": 665, "tx": 1760, "ty": 595, "crs": False},
        {"name": "IFP 75\"", "no": "6.", "wx": 2040, "wy": 665, "tx": 1985, "ty": 595, "crs": False},
    ]

    # SOUTH WING ROOMS (Dinding Utara / Y ≈ 940)
    rooms_south = [
        {"name": "IFP 86\" + CRS", "no": "", "wx": 460, "wy": 940, "tx": 380, "ty": 965, "crs": True},
        {"name": "IFP 75\"", "no": "7.", "wx": 690, "wy": 940, "tx": 635, "ty": 965, "crs": False},
        {"name": "IFP 75\"", "no": "8.", "wx": 920, "wy": 940, "tx": 865, "ty": 965, "crs": False},
        {"name": "IFP 75\"", "no": "9.", "wx": 1500, "wy": 940, "tx": 1445, "ty": 965, "crs": False},
        {"name": "IFP 75\"", "no": "10.", "wx": 1640, "wy": 940, "tx": 1585, "ty": 965, "crs": False},
        {"name": "IFP 75\"", "no": "11.", "wx": 1780, "wy": 940, "tx": 1725, "ty": 965, "crs": False},
        {"name": "IFP 86\" + CRS", "no": "", "wx": 2040, "wy": 940, "tx": 1960, "ty": 965, "crs": True},
    ]

    all_rooms = rooms_north + rooms_south

    for r in all_rooms:
        tx, ty = r["tx"], r["ty"]
        wx, wy = r["wx"], r["wy"]
        is_crs = r["crs"]
        
        # Color Theme: Red for 75" and Blue for 86"+CRS (Standard DED style)
        text_color = (210, 20, 40, 255) if not is_crs else (0, 80, 190, 255)
        border_color = (200, 10, 30, 255) if not is_crs else (0, 75, 180, 255)
        tag_bg = (255, 255, 255, 245)
        
        tag_label = f"{r['no']} {r['name']}" if r['no'] else r['name']
        tw = 148 if is_crs else 105
        th = 44
        
        # Draw Tag Box
        draw.rectangle([tx, ty, tx + tw, ty + th], fill=tag_bg, outline=border_color, width=2)
        draw.text((tx + 6, ty + 4), tag_label, fill=text_color, font=font_bold)
        draw.text((tx + 6, ty + 24), "+SL dll", fill=(70, 70, 70, 255), font=font_sub)
        
        # Physical Display Box on FRONT WALL (Horizontal alignment facing corridor)
        disp_w = 38 if is_crs else 30
        draw.rectangle([wx - disp_w//2, wy - 4, wx + disp_w//2, wy + 5], fill=(20, 20, 20, 255), outline=border_color, width=2)
        # Active Screen bar
        screen_y = wy - 1 if wy > 800 else wy + 1
        draw.line([wx - disp_w//2 + 3, screen_y, wx + disp_w//2 - 3, screen_y], fill=(0, 240, 240, 255) if is_crs else (40, 210, 40, 255), width=2)
        
        # Leader line from tag to display
        if wy < 800: # North wing
            draw.line([tx + tw//2, ty + th, wx, wy - 4], fill=border_color, width=2)
        else: # South wing
            draw.line([tx + tw//2, ty, wx, wy + 5], fill=border_color, width=2)

    # Insert IFP Evidence Card on Clean Left Margin
    if os.path.exists(ifp_path):
        ifp_raw = Image.open(ifp_path).convert("RGBA")
        
        card_w = 280
        card_h_img = int(ifp_raw.height * ((card_w - 16) / ifp_raw.width))
        ifp_resized = ifp_raw.resize((card_w - 16, card_h_img), Image.Resampling.LANCZOS)
        
        ins_x = 80
        ins_y = 1250
        card_total_h = card_h_img + 65
        
        draw.rectangle([ins_x, ins_y, ins_x + card_w, ins_y + card_total_h], fill=(255, 255, 255, 250), outline=(0, 75, 180, 255), width=3)
        draw.rectangle([ins_x, ins_y, ins_x + card_w, ins_y + 30], fill=(0, 75, 180, 255))
        draw.text((ins_x + 10, ins_y + 6), "EVIDEN BENTUK IFP (75\" & 86\")", fill=(255, 255, 255, 255), font=font_card_head)
        
        overlay.paste(ifp_resized, (ins_x + 8, ins_y + 36), ifp_resized)
        draw.text((ins_x + 10, ins_y + 36 + card_h_img + 8), "Interactive Flat Panel Display Screen", fill=(40, 40, 40, 255), font=font_card_sub)

    final_img = Image.alpha_composite(img, overlay).convert("RGB")
    
    out_path = "/home/ubuntu/DENAH_REV_LANTAI_03_UPN_CORRECTED.png"
    final_img.save(out_path, quality=95)
    print(f"Corrected official DED floorplan generated: {out_path}")
    return out_path

if __name__ == "__main__":
    render_corrected_official_ded()
