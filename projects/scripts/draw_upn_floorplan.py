import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
import numpy as np
import ezdxf
from ezdxf import units

def generate_architectural_drawing():
    # -------------------------------------------------------------------------
    # 1. SETUP CANVAS & FIGURE
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(26, 14.5), dpi=300)
    fig.patch.set_facecolor('#070b14') # Dark architectural blueprint theme
    ax.set_facecolor('#070b14')
    
    # Coordinate system in meters
    ax.set_xlim(-9, 103)
    ax.set_ylim(-9, 44)
    ax.set_aspect('equal')
    ax.axis('off')

    x_offset = 2.0
    y_offset = 2.0
    
    # Subtle Construction Grid Background
    for gx in range(0, 76, 4):
        ax.plot([gx + x_offset, gx + x_offset], [y_offset, 31 + y_offset], color='#131e32', linestyle=':', linewidth=0.5, zorder=1)
    for gy in range(0, 36, 4):
        ax.plot([x_offset, 72 + x_offset], [gy + y_offset, gy + y_offset], color='#131e32', linestyle=':', linewidth=0.5, zorder=1)

    # -------------------------------------------------------------------------
    # 2. DEFINE ROOMS GEOMETRY (LANTAI 03)
    # -------------------------------------------------------------------------
    rooms = [
        # --- SAYAP UTARA (Grid Y: 23 to 31) ---
        {"id": 0, "name": "TANGGA\nBARAT", "sub": "Darurat", "x": 0, "y": 23, "w": 3, "h": 8, "ifp": None, "tag": "", "crs": False, "bg": "#172033"},
        {"id": 1, "name": "RG. KELAS 01", "sub": "Reguler (+13.40)", "x": 3, "y": 23, "w": 8, "h": 8, "ifp": '75"', "tag": "01. IFP 75\"", "crs": False, "bg": "#0f2347"},
        {"id": 2, "name": "RG. KELAS 02", "sub": "Reguler (+13.40)", "x": 11, "y": 23, "w": 8, "h": 8, "ifp": '75"', "tag": "02. IFP 75\"", "crs": False, "bg": "#0f2347"},
        {"id": 3, "name": "RG. KELAS 03", "sub": "Reguler (+13.40)", "x": 19, "y": 23, "w": 8, "h": 8, "ifp": '75"', "tag": "03. IFP 75\"", "crs": False, "bg": "#0f2347"},
        {"id": 4, "name": "RG. KELAS 04", "sub": "Smart Class (+13.40)", "x": 27, "y": 23, "w": 9, "h": 8, "ifp": '86"', "tag": "04. IFP 86\" + CRS", "crs": True, "bg": "#081d3d"},
        {"id": 5, "name": "RG. KELAS 05", "sub": "Smart Class (+13.40)", "x": 36, "y": 23, "w": 9, "h": 8, "ifp": '86"', "tag": "05. IFP 86\" + CRS", "crs": True, "bg": "#081d3d"},
        {"id": 6, "name": "RG. KELAS 06", "sub": "Reguler (+13.40)", "x": 45, "y": 23, "w": 8, "h": 8, "ifp": '75"', "tag": "06. IFP 75\"", "crs": False, "bg": "#0f2347"},
        {"id": 7, "name": "RG. KELAS 07", "sub": "Reguler (+13.40)", "x": 53, "y": 23, "w": 8, "h": 8, "ifp": '75"', "tag": "07. IFP 75\"", "crs": False, "bg": "#0f2347"},
        {"id": 8, "name": "RG. KELAS 08", "sub": "Reguler (+13.40)", "x": 61, "y": 23, "w": 8, "h": 8, "ifp": '75"', "tag": "08. IFP 75\"", "crs": False, "bg": "#0f2347"},
        {"id": 9, "name": "TANGGA\nTIMUR", "sub": "Darurat", "x": 69, "y": 23, "w": 3, "h": 8, "ifp": None, "tag": "", "crs": False, "bg": "#172033"},

        # --- SAYAP SELATAN (Grid Y: 0 to 8) ---
        {"id": 10, "name": "RG. KELAS BESAR BARAT", "sub": "Interactive Smart Class (+13.40)", "x": 0, "y": 0, "w": 11, "h": 8, "ifp": '86"', "tag": "09. IFP 86\" + CRS", "crs": True, "bg": "#081d3d"},
        {"id": 11, "name": "RG. KELAS 09", "sub": "Reguler (+13.40)", "x": 11, "y": 0, "w": 8, "h": 8, "ifp": '75"', "tag": "10. IFP 75\"", "crs": False, "bg": "#0f2347"},
        {"id": 12, "name": "RG. KELAS 10", "sub": "Reguler (+13.40)", "x": 19, "y": 0, "w": 8, "h": 8, "ifp": '75"', "tag": "11. IFP 75\"", "crs": False, "bg": "#0f2347"},
        
        # Center Core Selatan
        {"id": 13, "name": "RUANG PANEL & TANGGA UTAMA", "sub": "Core Lift, MEP & Panel (+13.40)", "x": 27, "y": 0, "w": 18, "h": 8, "ifp": None, "tag": "", "crs": False, "bg": "#223147"},

        {"id": 14, "name": "RG. KELAS 11", "sub": "Reguler (+13.40)", "x": 45, "y": 0, "w": 6, "h": 8, "ifp": '75"', "tag": "12. IFP 75\"", "crs": False, "bg": "#0f2347"},
        {"id": 15, "name": "RG. KELAS 12", "sub": "Reguler (+13.40)", "x": 51, "y": 0, "w": 5, "h": 8, "ifp": '75"', "tag": "13. IFP 75\"", "crs": False, "bg": "#0f2347"},
        {"id": 16, "name": "RG. KELAS 13", "sub": "Reguler (+13.40)", "x": 56, "y": 0, "w": 5, "h": 8, "ifp": '75"', "tag": "14. IFP 75\"", "crs": False, "bg": "#0f2347"},
        {"id": 17, "name": "RG. KELAS BESAR TIMUR", "sub": "Interactive Smart Class (+13.40)", "x": 61, "y": 0, "w": 11, "h": 8, "ifp": '86"', "tag": "15. IFP 86\" + CRS", "crs": True, "bg": "#081d3d"},

        # --- AREA TENGAH / KORIDOR & TOILET (Y: 8 to 23) ---
        {"id": 18, "name": "LAVATORY BARAT", "sub": "Toilet Pria/Wanita", "x": 3, "y": 11, "w": 8, "h": 9, "ifp": None, "tag": "", "crs": False, "bg": "#172033"},
        {"id": 19, "name": "LAVATORY TIMUR", "sub": "Toilet Pria/Wanita", "x": 61, "y": 11, "w": 8, "h": 9, "ifp": None, "tag": "", "crs": False, "bg": "#172033"},
    ]

    # Draw Central Atrium / Void
    void1 = patches.Rectangle((12 + x_offset, 9 + y_offset), 23, 13, linewidth=1.5, edgecolor='#38bdf8', facecolor='#050811', linestyle='--', alpha=0.9, zorder=2)
    ax.add_patch(void1)
    ax.plot([12 + x_offset, 35 + x_offset], [9 + y_offset, 22 + y_offset], color='#38bdf8', linestyle=':', linewidth=0.8, alpha=0.35)
    ax.plot([12 + x_offset, 35 + x_offset], [22 + y_offset, 9 + y_offset], color='#38bdf8', linestyle=':', linewidth=0.8, alpha=0.35)
    ax.text(23.5 + x_offset, 15.5 + y_offset, "OPEN VOID / ATRIUM\n(Sirkulasi Udara & Cahaya)", color='#0284c7', fontsize=8.0, fontweight='bold', ha='center', va='center', bbox=dict(boxstyle="round,pad=0.3", fc="#050811", ec="none"))

    void2 = patches.Rectangle((37 + x_offset, 9 + y_offset), 23, 13, linewidth=1.5, edgecolor='#38bdf8', facecolor='#050811', linestyle='--', alpha=0.9, zorder=2)
    ax.add_patch(void2)
    ax.plot([37 + x_offset, 60 + x_offset], [9 + y_offset, 22 + y_offset], color='#38bdf8', linestyle=':', linewidth=0.8, alpha=0.35)
    ax.plot([37 + x_offset, 60 + x_offset], [22 + y_offset, 9 + y_offset], color='#38bdf8', linestyle=':', linewidth=0.8, alpha=0.35)
    ax.text(48.5 + x_offset, 15.5 + y_offset, "OPEN VOID / ATRIUM\n(Sirkulasi Udara & Cahaya)", color='#0284c7', fontsize=8.0, fontweight='bold', ha='center', va='center', bbox=dict(boxstyle="round,pad=0.3", fc="#050811", ec="none"))

    # Draw Central Bridge / Selasar Penghubung
    bridge = patches.Rectangle((35 + x_offset, 8 + y_offset), 2, 15, linewidth=1.5, edgecolor='#94a3b8', facecolor='#1e293b', zorder=3)
    ax.add_patch(bridge)
    ax.text(36 + x_offset, 15.5 + y_offset, "JEMBATAN SELASAR", color='#94a3b8', fontsize=6.0, rotation=90, ha='center', va='center')

    # Draw Selasar Text
    ax.text(36 + x_offset, 22.5 + y_offset, "SELASAR UTARA (+13.400)", color='#64748b', fontsize=7.5, fontweight='bold', ha='center', va='center', bbox=dict(boxstyle="round,pad=0.2", fc="#070b14", ec="none"))
    ax.text(36 + x_offset, 8.5 + y_offset, "SELASAR SELATAN (+13.400)", color='#64748b', fontsize=7.5, fontweight='bold', ha='center', va='center', bbox=dict(boxstyle="round,pad=0.2", fc="#070b14", ec="none"))

    # -------------------------------------------------------------------------
    # 3. DRAW ROOMS, WALLS, DOORS, AND MEDIA DEVICES (IFP & CRS)
    # -------------------------------------------------------------------------
    ifp_count_75 = 0
    ifp_count_86 = 0
    crs_count = 0

    for r in rooms:
        rx = r["x"] + x_offset
        ry = r["y"] + y_offset
        rw = r["w"]
        rh = r["h"]

        # 1. Room Floor Fill
        edge_c = '#38bdf8' if r["crs"] else '#0284c7'
        rect = patches.Rectangle((rx, ry), rw, rh, linewidth=2.0, edgecolor=edge_c, facecolor=r["bg"], alpha=0.95, zorder=3)
        ax.add_patch(rect)

        # 2. Structural Column markers (Corners)
        col_w = 0.45
        for cx, cy in [(rx, ry), (rx+rw-col_w, ry), (rx, ry+rh-col_w), (rx+rw-col_w, ry+rh-col_w)]:
            col = patches.Rectangle((cx, cy), col_w, col_w, facecolor='#f8fafc', edgecolor='#070b14', zorder=5)
            ax.add_patch(col)

        # 3. Clean Room Labels (Offset with Full Background Mask)
        if rw < 4:
            # Narrow stairs
            label_x = rx + rw/2
            label_y = ry + rh/2
            font_sz = 6.2
            ax.text(label_x, label_y, r["name"], color='#e2e8f0', fontsize=font_sz, fontweight='bold', 
                    ha='center', va='center', zorder=8, bbox=dict(boxstyle="round,pad=0.2", fc=r["bg"], ec="none", alpha=0.98))
        elif rw >= 10:
            # Large 11m corner rooms
            label_x = rx + rw * 0.46
            label_y = ry + rh * 0.65
            font_sz = 7.5
            label_color = '#ffffff' if r["crs"] else '#e2e8f0'
            ax.text(label_x, label_y, r["name"], color=label_color, fontsize=font_sz, fontweight='bold', 
                    ha='center', va='center', zorder=8, bbox=dict(boxstyle="square,pad=0.15", fc=r["bg"], ec="none", alpha=0.98))
            ax.text(label_x, label_y - 1.1, r["sub"], color='#94a3b8', fontsize=font_sz - 1.2, 
                    ha='center', va='center', zorder=8, bbox=dict(boxstyle="square,pad=0.15", fc=r["bg"], ec="none", alpha=0.98))
        elif rw <= 6:
            label_x = rx + (rw * 0.40 if r["ifp"] else rw/2)
            label_y = ry + rh * 0.65
            font_sz = 5.8
            label_color = '#ffffff' if r["crs"] else '#e2e8f0'
            ax.text(label_x, label_y, r["name"], color=label_color, fontsize=font_sz, fontweight='bold', 
                    ha='center', va='center', zorder=8, bbox=dict(boxstyle="square,pad=0.15", fc=r["bg"], ec="none", alpha=0.98))
            ax.text(label_x, label_y - 1.1, r["sub"], color='#94a3b8', fontsize=font_sz - 1.2, 
                    ha='center', va='center', zorder=8, bbox=dict(boxstyle="square,pad=0.15", fc=r["bg"], ec="none", alpha=0.98))
        else:
            # Standard 8-9m rooms
            label_x = rx + (rw * 0.38 if r["ifp"] else rw/2)
            label_y = ry + rh * 0.65
            font_sz = 7.0
            label_color = '#ffffff' if r["crs"] else '#e2e8f0'
            ax.text(label_x, label_y, r["name"], color=label_color, fontsize=font_sz, fontweight='bold', 
                    ha='center', va='center', zorder=8, bbox=dict(boxstyle="square,pad=0.15", fc=r["bg"], ec="none", alpha=0.98))
            ax.text(label_x, label_y - 1.1, r["sub"], color='#94a3b8', fontsize=font_sz - 1.2, 
                    ha='center', va='center', zorder=8, bbox=dict(boxstyle="square,pad=0.15", fc=r["bg"], ec="none", alpha=0.98))

        # 4. IFP / MEDIA DEVICE ANNOTATION (EAST WALL / DINDING TIMUR)
        if r["ifp"]:
            ifp_x = rx + rw
            ifp_y = ry + rh/2
            
            if r["ifp"] == '86"':
                ifp_count_86 += 1
                if r["crs"]:
                    crs_count += 1
                box_color = '#06b6d4' # Cyan
                tag_bg = '#083344'
            else:
                ifp_count_75 += 1
                box_color = '#10b981' # Emerald Green
                tag_bg = '#064e3b'

            badge_text = r["tag"]

            # Physical Display Box Symbol (Kotak Display menempel dinding Timur)
            disp_box = patches.Rectangle((ifp_x - 0.28, ifp_y - 1.3), 0.45, 2.6, facecolor='#020617', edgecolor=box_color, linewidth=2.0, zorder=8)
            ax.add_patch(disp_box)

            # Display Screen Symbol (Glow Bar)
            screen_line = lines.Line2D([ifp_x - 0.12, ifp_x - 0.12], [ifp_y - 1.1, ifp_y + 1.1], color=box_color, linewidth=3.2, zorder=9)
            ax.add_line(screen_line)

            # Tag Box (Positioned clean inside room near east wall)
            tag_x = ifp_x - (2.5 if rw >= 8 else 1.9)
            tag_y = ifp_y - 1.8
            
            # Leader line to tag
            ax.plot([ifp_x - 0.28, tag_x + 0.8], [ifp_y - 0.5, tag_y + 0.4], color=box_color, linestyle='-', linewidth=1.0, zorder=7)

            t_w = 2.6 if "CRS" in badge_text else 2.1
            tbox = patches.FancyBboxPatch((tag_x - t_w/2, tag_y - 0.5), t_w, 1.0,
                                          boxstyle="round,pad=0.15",
                                          facecolor=tag_bg,
                                          edgecolor=box_color,
                                          linewidth=1.2,
                                          zorder=8)
            ax.add_patch(tbox)
            ax.text(tag_x, tag_y, badge_text, color='#ffffff', fontsize=6.6 if "CRS" in badge_text else 7.0, fontweight='bold', ha='center', va='center', zorder=9)

    # -------------------------------------------------------------------------
    # 4. DIMENSION LINES & GRID BUBBLES
    # -------------------------------------------------------------------------
    grid_x_labels = [
        ('A', 0), ('B', 3), ('D', 11), ('F', 19), ('H', 27), 
        ('J', 36), ('L', 45), ('N', 53), ('P', 61), ('R', 69), ('S', 72)
    ]
    for label, gx in grid_x_labels:
        pos_x = gx + x_offset
        # Top Grid Line & Bubble
        ax.plot([pos_x, pos_x], [y_offset + 31, y_offset + 34], color='#0284c7', linewidth=1.0, linestyle='--')
        circ_top = patches.Circle((pos_x, y_offset + 34.5), radius=0.9, facecolor='#0284c7', edgecolor='#ffffff', linewidth=1.2, zorder=10)
        ax.add_patch(circ_top)
        ax.text(pos_x, y_offset + 34.5, label, color='#ffffff', fontsize=8.5, fontweight='bold', ha='center', va='center', zorder=11)
        
        # Bottom Grid Line & Bubble
        ax.plot([pos_x, pos_x], [y_offset, y_offset - 3], color='#0284c7', linewidth=1.0, linestyle='--')
        circ_bot = patches.Circle((pos_x, y_offset - 3.5), radius=0.9, facecolor='#0284c7', edgecolor='#ffffff', linewidth=1.2, zorder=10)
        ax.add_patch(circ_bot)
        ax.text(pos_x, y_offset - 3.5, label, color='#ffffff', fontsize=8.5, fontweight='bold', ha='center', va='center', zorder=11)

    # Total Horizontal Dimension Line (Placed above Grid Bubbles at Y=38.5 so NO overlap with J)
    ax.annotate('', xy=(x_offset, y_offset + 38.5), xytext=(72 + x_offset, y_offset + 38.5),
                arrowprops=dict(arrowstyle='<->', color='#38bdf8', lw=1.2))
    ax.text(36 + x_offset, y_offset + 39.2, "TOTAL LEBAR BANGUNAN = 72.000 mm (72,00 M)", color='#38bdf8', fontsize=8.5, fontweight='bold', ha='center')

    # Grid Y Bubbles (Left)
    grid_y_labels = [('1', 0), ('3', 8), ('4', 11), ('5', 20), ('6', 23), ('8', 31)]
    for label, gy in grid_y_labels:
        pos_y = gy + y_offset
        ax.plot([x_offset - 3, x_offset], [pos_y, pos_y], color='#0284c7', linewidth=1.0, linestyle='--')
        circ = patches.Circle((x_offset - 3.5, pos_y), radius=0.9, facecolor='#0284c7', edgecolor='#ffffff', linewidth=1.2, zorder=10)
        ax.add_patch(circ)
        ax.text(x_offset - 3.5, pos_y, label, color='#ffffff', fontsize=8.5, fontweight='bold', ha='center', va='center', zorder=11)

    # Total Vertical Dimension Line (Left)
    ax.annotate('', xy=(x_offset - 5.5, y_offset), xytext=(x_offset - 5.5, y_offset + 31),
                arrowprops=dict(arrowstyle='<->', color='#38bdf8', lw=1.2))
    ax.text(x_offset - 6.2, 15.5 + y_offset, "PANJANG = 31.000 mm", color='#38bdf8', fontsize=8.5, fontweight='bold', rotation=90, ha='center', va='center')

    # -------------------------------------------------------------------------
    # 5. NORTH ARROW & DRAWING TITLE
    # -------------------------------------------------------------------------
    na_x = x_offset + 1.5
    na_y = y_offset + 40.5
    ax.annotate('U', xy=(na_x, na_y + 1.6), color='#ef4444', fontsize=11, fontweight='bold', ha='center')
    ax.arrow(na_x, na_y - 0.8, 0, 1.8, head_width=0.7, head_length=0.7, fc='#ef4444', ec='#ef4444', lw=1.5, zorder=10)
    ax.text(na_x, na_y - 1.4, "UTARA", color='#94a3b8', fontsize=6.0, fontweight='bold', ha='center')

    ax.text(x_offset, y_offset - 6.0, "DENAH RENCANA PENEMPATAN MEDIA IFP & CRS — LANTAI 03", color='#f8fafc', fontsize=13, fontweight='bold')
    ax.text(x_offset, y_offset - 7.2, "SKALA 1 : 250  |  KONSULTAN PERENCANA: CV. TRINITI WIDI ANOMA  |  TAHUN 2024", color='#38bdf8', fontsize=8)

    # -------------------------------------------------------------------------
    # 6. OFFICIAL TITLE BLOCK & BILL OF QUANTITIES (KOP GAMBAR KANAN)
    # -------------------------------------------------------------------------
    tb_x = 76.5
    tb_y = -7.5
    tb_w = 23.5
    tb_h = 49.0

    # Kop Outer Box
    kop_box = patches.FancyBboxPatch((tb_x, tb_y), tb_w, tb_h, boxstyle="square,pad=0", facecolor='#090d16', edgecolor='#38bdf8', linewidth=2.0, zorder=10)
    ax.add_patch(kop_box)

    # Kop Header (Instansi)
    hdr_box = patches.Rectangle((tb_x, tb_y + tb_h - 6.5), tb_w, 6.5, facecolor='#1e293b', edgecolor='#38bdf8', linewidth=1.0, zorder=11)
    ax.add_patch(hdr_box)
    ax.text(tb_x + tb_w/2, tb_y + tb_h - 2.0, "KEMENTERIAN PENDIDIKAN, KEBUDAYAAN,\nRISET DAN TEKNOLOGI", color='#ffffff', fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=12)
    ax.text(tb_x + tb_w/2, tb_y + tb_h - 4.5, "UNIVERSITAS PEMBANGUNAN NASIONAL\n'VETERAN' YOGYAKARTA", color='#38bdf8', fontsize=8.0, fontweight='bold', ha='center', va='center', zorder=12)

    # Project Info
    ax.text(tb_x + 1.0, tb_y + tb_h - 8.0, "NAMA PEKERJAAN:", color='#94a3b8', fontsize=6.5, fontweight='bold', zorder=12)
    ax.text(tb_x + 1.0, tb_y + tb_h - 9.8, "PEMBUATAN DED DAN REVIEW DED\nGEDUNG FTI UPN 'VETERAN' YOGYAKARTA", color='#f8fafc', fontsize=7.5, fontweight='bold', zorder=12)

    ax.text(tb_x + 1.0, tb_y + tb_h - 12.3, "LOKASI PROYEK:", color='#94a3b8', fontsize=6.5, fontweight='bold', zorder=12)
    ax.text(tb_x + 1.0, tb_y + tb_h - 13.8, "Jl. Babarsari No. 2, Sleman, D.I. Yogyakarta", color='#f8fafc', fontsize=7.0, zorder=12)

    # Divider line
    ax.plot([tb_x, tb_x + tb_w], [tb_y + tb_h - 15.3, tb_y + tb_h - 15.3], color='#38bdf8', linewidth=1.0, zorder=12)

    # LEGENDA SIMBOL & REKAPITULASI BoQ
    ax.text(tb_x + tb_w/2, tb_y + tb_h - 17.0, "LEGENDA SIMBOL & BoQ MEDIA", color='#facc15', fontsize=8.5, fontweight='bold', ha='center', zorder=12)

    # Item 1: IFP 75"
    leg1 = patches.Rectangle((tb_x + 1.0, tb_y + tb_h - 20.8), 1.2, 2.0, facecolor='#020617', edgecolor='#10b981', linewidth=1.5, zorder=12)
    ax.add_patch(leg1)
    ax.text(tb_x + 3.0, tb_y + tb_h - 19.3, "Interactive Flat Panel 75\"", color='#ffffff', fontsize=7.5, fontweight='bold', zorder=12)
    ax.text(tb_x + 3.0, tb_y + tb_h - 20.5, f"Total Terpasang: {ifp_count_75} Unit (Titik 01-03, 06-08, 10-14)", color='#10b981', fontsize=7.0, zorder=12)

    # Item 2: IFP 86" + CRS
    leg2 = patches.Rectangle((tb_x + 1.0, tb_y + tb_h - 24.8), 1.2, 2.0, facecolor='#020617', edgecolor='#06b6d4', linewidth=1.5, zorder=12)
    ax.add_patch(leg2)
    ax.text(tb_x + 3.0, tb_y + tb_h - 23.3, "Interactive Flat Panel 86\" + CRS", color='#ffffff', fontsize=7.5, fontweight='bold', zorder=12)
    ax.text(tb_x + 3.0, tb_y + tb_h - 24.5, f"Total Terpasang: {ifp_count_86} Unit (Titik 04, 05, 09, 15)", color='#06b6d4', fontsize=7.0, zorder=12)

    # Item 3: CRS System
    ax.text(tb_x + 3.0, tb_y + tb_h - 27.0, "Classroom Response System (CRS)", color='#ffffff', fontsize=7.5, fontweight='bold', zorder=12)
    ax.text(tb_x + 3.0, tb_y + tb_h - 28.2, f"Total Terintegrasi: {crs_count} Ruang Smart Class", color='#38bdf8', fontsize=7.0, zorder=12)

    # Divider line
    ax.plot([tb_x, tb_x + tb_w], [tb_y + tb_h - 30.0, tb_y + tb_h - 30.0], color='#38bdf8', linewidth=1.0, zorder=12)

    # Item 4: Mounting Note
    ax.text(tb_x + 1.0, tb_y + tb_h - 31.8, "CATATAN TEKNIS PEMASANGAN:", color='#facc15', fontsize=7.2, fontweight='bold', zorder=12)
    notes_lines = [
        "• Seluruh display dipasang menempel pada",
        "  Dinding Sisi TIMUR di setiap ruangan.",
        "• Elevasi center layar: +1.50 m dari FFL.",
        "• Dilengkapi instalasi stop kontak & data MEE.",
        "• Sistem CRS terkoneksi ke jaringan kampus."
    ]
    for i, nl in enumerate(notes_lines):
        ax.text(tb_x + 1.0, tb_y + tb_h - 33.4 - (i * 1.3), nl, color='#cbd5e1', fontsize=6.5, zorder=12)

    # Divider line
    ax.plot([tb_x, tb_x + tb_w], [tb_y + tb_h - 40.5, tb_y + tb_h - 40.5], color='#38bdf8', linewidth=1.0, zorder=12)

    # Summary Box Table
    sum_box = patches.Rectangle((tb_x + 1.0, tb_y + 3.5), tb_w - 2.0, 4.2, facecolor='#1e293b', edgecolor='#38bdf8', linewidth=1.0, zorder=12)
    ax.add_patch(sum_box)
    ax.text(tb_x + tb_w/2, tb_y + 6.3, "TOTAL TITIK DISPLAY LANTAI 03", color='#f8fafc', fontsize=7.5, fontweight='bold', ha='center', zorder=13)
    ax.text(tb_x + tb_w/2, tb_y + 4.5, "15 TITIK RUANGAN", color='#38bdf8', fontsize=11.0, fontweight='bold', ha='center', zorder=13)

    # Sheet code info
    ax.text(tb_x + 1.0, tb_y + 2.0, "JUDUL GAMBAR: DENAH LANTAI 03", color='#ffffff', fontsize=6.8, fontweight='bold', zorder=12)
    ax.text(tb_x + 1.0, tb_y + 0.8, "KODE LEMBAR: MEE - REV.03", color='#38bdf8', fontsize=6.8, zorder=12)
    ax.text(tb_x + tb_w - 1.0, tb_y + 0.8, "SKALA 1:250", color='#ffffff', fontsize=6.8, fontweight='bold', ha='right', zorder=12)

    # -------------------------------------------------------------------------
    # 7. SAVE PRODUCTION FILES (PNG, SVG, DXF)
    # -------------------------------------------------------------------------
    output_png = "/home/ubuntu/DENAH_LANTAI_03_IFP_UPN_VETERAN.png"
    output_svg = "/home/ubuntu/DENAH_LANTAI_03_IFP_UPN_VETERAN.svg"
    output_dxf = "/home/ubuntu/DENAH_LANTAI_03_IFP_UPN_VETERAN.dxf"

    plt.savefig(output_png, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none', dpi=300)
    plt.savefig(output_svg, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()

    # Generate AutoCAD DXF as well
    doc = ezdxf.new("R2010", setup=True)
    doc.units = units.M
    msp = doc.modelspace()
    doc.layers.add(name="WALLS", color=7)
    doc.layers.add(name="IFP_75", color=3)
    doc.layers.add(name="IFP_86_CRS", color=4)
    doc.layers.add(name="LABELS", color=2)
    doc.layers.add(name="DIMENSIONS", color=1)

    for r in rooms:
        x, y, w, h = r["x"], r["y"], r["w"], r["h"]
        msp.add_lwpolyline([(x, y), (x+w, y), (x+w, y+h), (x, y+h), (x, y)], dxfattribs={"layer": "WALLS"})
        msp.add_text(f"{r['name']}", dxfattribs={"layer": "LABELS", "height": 0.35}).set_placement((x + 0.5, y + h/2))
        if r["ifp"]:
            layer_name = "IFP_86_CRS" if r["crs"] or r["ifp"] == '86"' else "IFP_75"
            msp.add_lwpolyline([(x+w-0.2, y+h/2-1.0), (x+w+0.2, y+h/2-1.0), (x+w+0.2, y+h/2+1.0), (x+w-0.2, y+h/2+1.0), (x+w-0.2, y+h/2-1.0)], dxfattribs={"layer": layer_name})
            badge = r["tag"]
            msp.add_text(badge, dxfattribs={"layer": layer_name, "height": 0.3}).set_placement((x+w-2.5, y+h/2))

    doc.saveas(output_dxf)

    print(f"Generated PNG: {output_png}")
    print(f"Generated SVG: {output_svg}")
    print(f"Generated DXF: {output_dxf}")
    return output_png, output_svg, output_dxf

if __name__ == "__main__":
    generate_architectural_drawing()
