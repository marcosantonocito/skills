#!/usr/bin/env python3
"""Normalize an approved app icon concept to platform-specific raster sources.

Apple raster output is a design/Xcode source, NOT a finished layered Icon Composer deliverable.
Google Play output is a 512x512 RGBA (32-bit) PNG, max 1024 KB.
"""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageColor, ImageOps


def run(src_path: Path, platform: str, output: Path, bg: str = "#FFFFFF"):
    src=ImageOps.exif_transpose(Image.open(src_path)).convert("RGBA")
    size=(1024,1024) if platform=="apple" else (512,512)
    # Fit to square; do not fake already-rounded edges.
    ratio=min(size[0]/src.width,size[1]/src.height)
    src=src.resize((max(1,round(src.width*ratio)),max(1,round(src.height*ratio))),Image.Resampling.LANCZOS)
    base=Image.new("RGBA",size,ImageColor.getrgb(bg)+(255,)) if platform=="apple" else Image.new("RGBA",size,(0,0,0,0))
    base.alpha_composite(src,((size[0]-src.width)//2,(size[1]-src.height)//2))
    output.parent.mkdir(parents=True,exist_ok=True)
    if output.suffix.lower() != ".png":
        raise ValueError("Icon exports must be PNG")
    if platform=="apple":
        base.convert("RGB").save(output,optimize=True)
    else:
        base.save(output,optimize=True)
        if output.stat().st_size>1048576:
            raise ValueError("Google Play icon exceeds 1024 KB; simplify source artwork and re-export")
    return {"platform":platform,"file":str(output),"pixel_dimensions":size,"state":"Rendered Asset", "warning":"Apple requires Xcode/Icon Composer integration" if platform=="apple" else "Check Google safe areas and creative review"}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("input",type=Path)
    p.add_argument("--platform",choices=["apple","google"],required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--background",default="#FFFFFF")
    a=p.parse_args()
    print(json.dumps(run(a.input,a.platform,a.output,a.background),indent=2))

if __name__=="__main__":main()
