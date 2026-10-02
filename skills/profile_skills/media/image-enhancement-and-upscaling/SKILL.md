---
name: image-enhancement-and-upscaling
description: "Use when upscaling or sharpening images, banners, and docs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: media
    tags: [image-processing, upscaling, lanczos, unsharp-mask, super-resolution, banner-remastering, document-clarity]
    related_skills: [web-asset-deployment-and-caching, claude-design]
---

# Image Enhancement, Super-Resolution & Visual Remastering

A class-level operational skill for upscaling, denoising, sharpening, and remastering digital images, marketing banners, commercial showroom graphics, and low-resolution identity/tender documents into crisp HD, 2K, and 4K assets.

## When to Use

- When the user requests making images HD, 2K, 4K, or clearer/sharper (*"buat gambar jadi HD"*, *"pertajam gambar/dokumen"*).
- When preparing high-resolution hero banners, digital signage graphics, and promotional visuals for production websites.
- When cleaning, deblocking, and restoring low-resolution scans, identity cards (KTP/NPWP), or technical schematics for verification.
- When generating multi-tier responsive resolutions (2K for web/mobile, 4K for high-DPI displays and print).

## Procedure

1. **Inspection & Geometry Profiling:**
   - Measure original dimensions, color space, and compression artifacts using FFprobe or PIL:
     ```bash
     /home/ubuntu/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffprobe -v error -show_entries stream=width,height,codec_name -of default=noprint_wrappers=1 <image_path>
     ```
   - Identify content category:
     - **Marketing / Commercial Banner:** Requires vibrant color grading, high micro-contrast on text, hardware edges, and screen displays.
     - **Identification / Official Document:** Requires legibility optimization, high-contrast monochrome text pass, and structured text transcription.
     - **Web Hero Asset:** Requires strict aspect ratio preservation and WebP/PNG optimization.

2. **Multi-Stage Super-Resolution Pipeline:**
   - **Step A: High-Order Interpolation (Lanczos):**
     Scale 2X (2K: ~2560px width) or 4X (4K: ~3840px-5120px width) using Lanczos filtering:
     ```python
     from PIL import Image, ImageEnhance, ImageFilter

     img = Image.open(src_path)
     w, h = img.size
     img_2k = img.resize((2560, int(h * (2560 / w))), Image.Resampling.LANCZOS)
     ```
   - **Step B: Pre-Sharpening Deblock & Noise Suppression:**
     Apply a light spatial smoothing or deblocking filter before unsharp masking to prevent amplifying JPEG compression ringing:
     ```python
     # Blend with smooth pass to suppress compression grain
     smooth = img_2k.filter(ImageFilter.SMOOTH)
     img_base = Image.blend(img_2k, smooth, 0.15)
     ```
     Or via FFmpeg:
     ```bash
     ffmpeg -y -i input.jpg -vf "deblock=filter=weak:block=4,scale=2560:-1:flags=lanczos,cas=0.5,unsharp=5:5:0.8:5:5:0.0,eq=contrast=1.06:saturation=1.05" output_2k.png
     ```
   - **Step C: Adaptive Unsharp Masking:**
     Sharpen edges with calibrated radius and threshold to isolate structural lines from smooth gradients:
     ```python
     # For commercial graphics
     unsharp = img_base.filter(ImageFilter.UnsharpMask(radius=2.0, percent=170, threshold=2))
     ```
   - **Step D: Dynamic Range & Color Vibrancy Tuning:**
     Enhance contrast and saturation subtly (5%–12%) for rich, showroom-grade display vibrancy:
     ```python
     img_contrast = ImageEnhance.Contrast(unsharp).enhance(1.08)
     img_color = ImageEnhance.Color(img_contrast).enhance(1.06)
     img_final = ImageEnhance.Sharpness(img_color).enhance(1.15)
     img_final.save(out_path, "PNG", optimize=True)
     ```

3. **Specialized Handling for Documents & Identification Cards:**
   - **Full Card Frame + Targeted Text Crops:** When enhancing ID cards (KTP/NPWP), crop both individual cards and high-pass filtered text blocks.
   - **High-Contrast Text-Optimized Pass:** Convert to grayscale and apply high-contrast unsharp masking (`contrast=1.8`, `unsharp radius=2, percent=250, threshold=0`).
   - **Companion Transcription:** Always provide a complete, verified textual transcription of all data fields alongside the enhanced image artifact.

4. **Visual Quality Gate:**
   - Inspect the final output using `vision_analyze` to verify edge crispness, text legibility, and lack of halo artifacts before delivering to the user.
   - Deliver media using native `MEDIA:<absolute_path>` tags.

## Pitfalls

- **Unsharp Masking Raw JPEG Without Deblocking:** Applying heavy sharpening directly to compressed JPEG inputs amplifies block boundary ringing and grain; always apply subtle pre-smoothing or deblocking before unsharp masking.
- **Using Bilinear/Bicubic for Extreme Upscaling:** Using low-order interpolation on vector-like text or sharp display bezels causes blurry edges; always enforce Lanczos (`flags=lanczos` or `Resampling.LANCZOS`).
- **Over-Saturating Flesh Tones and Natural Gradients:** Excessive global saturation enhancements create unnatural color banding in skin tones and sky gradients; keep color boosts bounded between 1.04 and 1.08.
- **Omitting Text Transcriptions on Restored Documents:** Relying solely on visual enhancement without transcribing extracted card data leaves ambiguity for critical verification workflows.
- **Ignoring Aspect Ratio During Canvas Scaling:** Hardcoding target dimensions that distort the original aspect ratio compresses or stretches product hardware; calculate proportional height dynamically from target width.
