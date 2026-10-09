#!/usr/bin/env python3
"""Deterministic store graphic compositor. All user-interface pixels come from supplied real captures.

Usage: python scripts/render.py templates/render-example.json --output out.png
The JSON scene may contain images (background / decorative layers), real captures,
shapes, and text. It never invokes an image generation API.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / "references" / "specs.json").read_text())


def locate(path: str, scene_dir: Path) -> Path:
    p = Path(path).expanduser()
    if p.is_absolute():
        return p
    return scene_dir / p


def rgb_color(value: str, default="#FFFFFF"):
    return ImageColor.getrgb(value or default)


def render_size(scene):
    target = scene["canvas"]
    if "width" in target and "height" in target:
        width, height = int(target["width"]), int(target["height"])
    else:
        platform, kind = target["platform"], target["kind"]
        options = SPEC[platform][kind].get("size_options")
        if not options:
            raise ValueError("A canvas width/height is required for variable-size presets")
        index = int(target.get("variant", 0))
        width, height = options[index]
    if not (16 <= width <= 8000 and 16 <= height <= 8000):
        raise ValueError("Canvas size outside supported rendering range")
    return width, height


def canvas_background(bg: dict, size: tuple[int, int], scene_dir: Path):
    color = rgb_color(bg.get("color", "#FFFFFF"))
    canvas = Image.new("RGBA", size, color + (255,))
    if bg.get("gradient_to"):
        finish = rgb_color(bg["gradient_to"])
        ramp = Image.new("RGB", (1, 256))
        for y in range(256):
            t = y / 255
            ramp.putpixel((0, y), tuple(round(color[c] * (1 - t) + finish[c] * t) for c in range(3)))
        canvas = ramp.resize(size, Image.Resampling.BILINEAR).convert("RGBA")
    if bg.get("image"):
        artwork = Image.open(locate(bg["image"], scene_dir))
        artwork = ImageOps.exif_transpose(artwork).convert("RGBA")
        if bg.get("image_fit", "cover") == "contain":
            artwork.thumbnail(size, Image.Resampling.LANCZOS)
            x, y = (size[0] - artwork.width) // 2, (size[1] - artwork.height) // 2
            canvas.alpha_composite(artwork, (x, y))
        else:
            artwork = ImageOps.fit(artwork, size, Image.Resampling.LANCZOS)
            canvas.alpha_composite(artwork)
    return canvas


def font_for(font_path, size: int, scene_dir: Path):
    candidates = [
        locate(font_path, scene_dir) if font_path else None,
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
        Path("/Library/Fonts/Arial.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf"),
    ]
    for candidate in candidates:
        if candidate and candidate.is_file():
            return ImageFont.truetype(str(candidate), size)
    # Fail instead of silently rasterizing text using an unreadable tiny font.
    raise FileNotFoundError("No suitable font found. Supply an installed/licensed font file in the scene's font field.")


def fit_lines(draw, text, font, width, max_lines):
    lines = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        current = ""
        for word in paragraph.split():
            attempt = (current + " " + word).strip()
            if not current or draw.textbbox((0, 0), attempt, font=font)[2] <= width:
                current = attempt
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines if len(lines) <= max_lines else None


def render_text(canvas, element, scene_dir):
    x, y, width, height = map(int, element["box"])
    text = element["text"]
    font_size = int(element.get("font_size", 80))
    min_font = int(element.get("min_font_size", font_size // 2))
    max_lines = int(element.get("max_lines", 3))
    line_spacing = float(element.get("line_spacing", 1.08))
    align = element.get("align", "left")
    if align not in {"left", "center", "right"}:
        raise ValueError("align must be left/center/right")
    draw = ImageDraw.Draw(canvas)
    font = None
    for sz in range(font_size, min_font - 1, -1):
        candidate = font_for(element.get("font"), sz, scene_dir)
        lines = fit_lines(draw, text, candidate, width, max_lines)
        if lines is None:
            continue
        line_h = math.ceil(sz * line_spacing)
        if len(lines) * line_h <= height and all(draw.textbbox((0, 0), line, font=candidate)[2] <= width for line in lines):
            font = candidate
            break
    if font is None:
        raise ValueError("Text doesn't fit. Enlarge text box or reduce min_font_size; don't silently clip")
    line_h = math.ceil(sz * line_spacing)
    offset_y = y + (height - len(lines) * line_h) // 2 if element.get("valign", "center") == "center" else y
    fill = rgb_color(element.get("color", "#222222"))
    for line in lines:
        ink = draw.textbbox((0, 0), line, font=font)
        ink_w = ink[2] - ink[0]
        tx = x if align == "left" else x + (width - ink_w) // (2 if align == "center" else 1)
        # Offset based on actual ink bbox, so glyphs don't have off-center bounding shapes.
        draw.text((tx - ink[0], offset_y - ink[1]), line, font=font, fill=fill)
        offset_y += line_h


def create_capture(element, scene_dir):
    path = locate(element["path"], scene_dir)
    src = Image.open(path)
    src = ImageOps.exif_transpose(src).convert("RGBA")
    crop = element.get("crop")
    if crop:
        if len(crop) != 4 or not all(0 <= float(n) <= 1 for n in crop):
            raise ValueError("crop must be four normalized bounds in [0,1]")
        left, top, right, bottom = crop
        if not (left < right and top < bottom):
            raise ValueError("Invalid crop bounds")
        src = src.crop((round(left*src.width), round(top*src.height), round(right*src.width), round(bottom*src.height)))
    return src


def fitted_capture(src, box_size, mode):
    w, h = box_size
    if mode == "cover":
        return ImageOps.fit(src, box_size, Image.Resampling.LANCZOS)
    if mode != "contain":
        raise ValueError("fit must be contain or cover")
    sw, sh = src.size
    scale = min(w / sw, h / sh)
    return src.resize((max(1,round(sw*scale)), max(1,round(sh*scale))), Image.Resampling.LANCZOS)


def rounded_capture(img, radius):
    if radius <= 0:
        return img
    radius = min(radius, min(img.size)//2)
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,img.width-1,img.height-1), radius=radius, fill=255)
    img.putalpha(Image.composite(img.getchannel("A"), Image.new("L", img.size, 0), mask))
    return img


def perspective_warp(img, corners, canvas_size):
    """Draw exact capture through an approved four-point projective placement."""
    try:
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("Perspective corners require numpy: pip install numpy") from exc
    if len(corners) != 4:
        raise ValueError("perspective_corners requires 4 points: TL, TR, BR, BL")
    src = np.array([[0,0],[img.width,0],[img.width,img.height],[0,img.height]], dtype=float)
    dst = np.array(corners, dtype=float)
    A, b = [], []
    for (x,y),(X,Y) in zip(src,dst):
        A.append([x,y,1,0,0,0,-x*X,-y*X]); b.append(X)
        A.append([0,0,0,x,y,1,-x*Y,-y*Y]); b.append(Y)
    coeff = np.linalg.solve(np.asarray(A),np.asarray(b))
    forward = np.array([[coeff[0],coeff[1],coeff[2]],[coeff[3],coeff[4],coeff[5]],[coeff[6],coeff[7],1.]])
    inverse = np.linalg.inv(forward); inverse /= inverse[2,2]
    values = [float(inverse[r,c]) for r,c in [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1)]]
    return img.transform(canvas_size, Image.Transform.PERSPECTIVE, values, Image.Resampling.BICUBIC)


def render_capture(canvas, el, scene_dir):
    x, y, width, height = map(int, el["box"])
    if width <= 0 or height <= 0:
        raise ValueError("Screenshot boxes need positive dimensions")
    src = create_capture(el, scene_dir)
    img = fitted_capture(src, (width,height), el.get("fit", "contain"))
    img = rounded_capture(img, round(el.get("corner_radius",0) * img.width / width))
    if el.get("perspective_corners"):
        warp = perspective_warp(img, el["perspective_corners"], canvas.size)
        canvas.alpha_composite(warp)
        return
    angle = float(el.get("rotation",0))
    if angle:
        img = img.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    cx, cy = x+width/2, y+height/2
    dst_x, dst_y = round(cx-img.width/2), round(cy-img.height/2)
    if el.get("shadow",False):
        mask = Image.new("L", canvas.size, 0)
        mask.paste(img.getchannel("A"), (dst_x+12,dst_y+24))
        mask = mask.filter(ImageFilter.GaussianBlur(radius=24))
        shadow = Image.new("RGBA",canvas.size,(10,10,22,85))
        shadow.putalpha(mask.point(lambda p: round(p*.38)))
        canvas.alpha_composite(shadow)
    canvas.alpha_composite(img,(dst_x,dst_y))


def render_element(canvas, el, scene_dir):
    typ=el["type"]
    if typ == "text":
        return render_text(canvas,el,scene_dir)
    if typ == "screenshot":
        return render_capture(canvas,el,scene_dir)
    if typ in {"rectangle","circle"}:
        x,y,w,h=map(int,el["box"])
        draw=ImageDraw.Draw(canvas)
        xy=(x,y,x+w,y+h)
        if typ == "circle":
            draw.ellipse(xy,fill=rgb_color(el.get("fill", "#FFFFFF")))
        else:
            draw.rounded_rectangle(xy,fill=rgb_color(el.get("fill", "#FFFFFF")),radius=int(el.get("radius",0)))
        return
    if typ == "decoration":
        img=Image.open(locate(el["path"],scene_dir)).convert("RGBA")
        x,y,w,h=map(int,el["box"])
        mode=el.get("fit","contain")
        img=fitted_capture(img,(w,h),mode)
        canvas.alpha_composite(img,(round(x+(w-img.width)/2),round(y+(h-img.height)/2)))
        return
    raise ValueError(f"Unknown layer type: {typ}")


def run(scene_path: Path, output: Path):
    scene=json.loads(scene_path.read_text(encoding="utf-8"))
    size=render_size(scene)
    canvas=canvas_background(scene.get("background",{}),size,scene_path.parent)
    for layer in scene.get("elements",[]):
        render_element(canvas,layer,scene_path.parent)
    output.parent.mkdir(parents=True,exist_ok=True)
    if output.suffix.lower() in {".jpg",".jpeg"}:
        canvas.convert("RGB").save(output,quality=94,subsampling=0)
    elif output.suffix.lower()==".png":
        # Apple and Google screenshots/feature graphics prohibit alpha.
        canvas.convert("RGB").save(output,optimize=True)
    else:
        raise ValueError("Only .png/.jpg/.jpeg supported")
    return size


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("scene",type=Path)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    size=run(args.scene,args.output)
    print(json.dumps({"file":str(args.output),"size":size,"state":"Rendered Asset", "note":"Technical and human creative validation still required."}))

if __name__=="__main__": main()
