#!/usr/bin/env python3
"""Technical validator for store image files. Does not certify content/policy approvals.

Usage: python scripts/validate.py --platform apple --kind iphone_duo_outer --file output.png
Use --creative-reviewed only after an actual authorized human has reviewed the image.
"""
import argparse
import json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
SPEC=json.loads((ROOT/"references"/"specs.json").read_text(encoding="utf-8"))


def check(path:Path, platform:str,kind:str,creative_reviewed:bool=False):
    cfg=SPEC[platform][kind]
    errors=[]; warnings=[]
    with Image.open(path) as im:
        im.load()
        w,h=im.size
        fmt=im.format
        mode=im.mode
        alpha=("A" in im.getbands() or "transparency" in im.info)
    size=(w,h)
    suffix=path.suffix.lower()
    if fmt not in {"PNG","JPEG"} or suffix not in {".png",".jpg",".jpeg"}:
        errors.append("Export must be a PNG or JPEG file with matching extension")
    if fmt=="PNG" and suffix!=".png" or fmt=="JPEG" and suffix not in {".jpg",".jpeg"}:
        errors.append("File extension does not match encoded format")
    if cfg.get("format") and fmt!=cfg["format"]:
        errors.append(f"Must be {cfg['format']}")
    if fmt=="PNG" and mode not in {"RGB","RGBA"}:
        errors.append("PNG must use truecolor RGB (24-bit) or RGBA (32-bit), not palette/grayscale mode")
    if cfg.get("require_rgba") and mode!="RGBA":
        errors.append("Must be 32-bit RGBA PNG (with alpha channel)")
    if cfg.get("alpha") is False and alpha:
        errors.append("Alpha/transparency not allowed")
    if fmt=="JPEG" and cfg.get("require_rgba"):
        errors.append("JPEG cannot meet icon alpha requirement")
    if "size_options" in cfg and list(size) not in cfg["size_options"]:
        if cfg.get("allow_three_two_range") and (1920<=w<=3840 and 1280<=h<=2560 and abs(w/h-1.5)<=0.0005):
            pass
        else:
            errors.append(f"Unexpected size {w}x{h}; accepted sizes in snapshot: {cfg['size_options']}")
    if "min_short" in cfg:
        short,long=min(size),max(size)
        if short<cfg["min_short"] or long>cfg["max_long"]:
            errors.append(f"Sides outside expected range: min {cfg['min_short']}, max {cfg['max_long']}")
        if long>short*cfg.get("max_ratio",99):
            errors.append(f"Aspect ratio exceeds allowed long/short ratio {cfg['max_ratio']}")
        if kind=="tablet_screenshot":
            warnings.append("Google large-screen rules vary by placement; confirm tablet dimensions with current Play Console docs.")
        if kind=="phone_screenshot" and (w,h) not in {(1080,1920),(1920,1080)}:
            warnings.append("Check Google's separate recommendation for >=4 phone screenshots in 9:16 or 16:9 at >=1080px.")
    if cfg.get("max_bytes") and path.stat().st_size>cfg["max_bytes"]:
        errors.append(f"File exceeds maximum byte size {cfg['max_bytes']}")
    if platform=="apple" and kind=="icon_flat_source":
        warnings.append("This is a raster *source*, not a completed layered Icon Composer/Xcode app icon.")
    if not creative_reviewed:
        warnings.append("Manual creative, screenshot authenticity, localization, copyright, claims and store-policy review remains required.")
    warnings.append("Preset specs are a 2026-10-09 snapshot; verify live official store requirements before submission.")
    technical_ok=not errors
    status="TECHNICAL_FAIL" if errors else "TECHNICAL_PASS__CREATIVE_REVIEW_REQUIRED" if not creative_reviewed else "VALIDATED_LOCALLY__STORE_APPROVAL_NOT_GUARANTEED"
    return {"path":str(path),"platform":platform,"kind":kind,"size":[w,h],"format":fmt,"mode":mode,"has_alpha":alpha,"bytes":path.stat().st_size,"snapshot_date":SPEC["snapshot_date"],"status":status,"technical_ok":technical_ok,"errors":errors,"warnings":warnings}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--platform",choices=["apple","google"],required=True)
    p.add_argument("--kind",required=True,help="See keys in references/specs.json")
    p.add_argument("--file",type=Path,required=True)
    p.add_argument("--creative-reviewed",action="store_true",help="Only supply after authorized human creative review")
    p.add_argument("--report",type=Path)
    a=p.parse_args()
    result=check(a.file,a.platform,a.kind,a.creative_reviewed)
    body=json.dumps(result,indent=2,ensure_ascii=False)
    print(body)
    if a.report:
        a.report.parent.mkdir(parents=True,exist_ok=True)
        a.report.write_text(body,encoding="utf-8")
    raise SystemExit(0 if result["technical_ok"] else 2)

if __name__=="__main__":main()
