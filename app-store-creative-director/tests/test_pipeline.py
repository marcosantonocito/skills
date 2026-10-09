import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
def module(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/"scripts"/(name+".py"))
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
render=module("render")
export_icon=module("export_icon")
validate=module("validate")

class PipelineTests(unittest.TestCase):
    def test_apple_duo_sizes(self):
        self.assertEqual(render.render_size({"canvas":{"platform":"apple","kind":"iphone_duo_inner"}}),(2007,2853))
        self.assertEqual(render.render_size({"canvas":{"platform":"apple","kind":"iphone_duo_outer"}}),(1398,2034))

    def test_render_and_validate_apple(self):
        with TemporaryDirectory() as d:
            folder=Path(d)
            Image.new("RGB",(120,250),(20,180,150)).save(folder/"real-capture.png")
            scene={"canvas":{"platform":"apple","kind":"iphone_medium"}, "background":{"color":"#FFFFFF"}, "elements":[
                {"type":"screenshot","path":"real-capture.png","box":[120,550,850,1800],"shadow":True,"corner_radius":10},
                {"type":"text","text":"Track your own progress","box":[60,100,1050,350],"font_size":90,"min_font_size":55,"max_lines":3}
            ]}
            (folder/"scene.json").write_text(json.dumps(scene))
            dest=folder/"out.png"
            render.run(folder/"scene.json",dest)
            result=validate.check(dest,"apple","iphone_medium")
            self.assertTrue(result["technical_ok"],result["errors"])
            self.assertEqual(result["status"],"TECHNICAL_PASS__CREATIVE_REVIEW_REQUIRED")

    def test_google_bad_alpha(self):
        with TemporaryDirectory() as d:
            dest=Path(d)/"feat.png"
            Image.new("RGBA",(1024,500),(25,15,240,255)).save(dest)
            result=validate.check(dest,"google","feature_graphic")
            self.assertFalse(result["technical_ok"])

    def test_google_icon(self):
        with TemporaryDirectory() as d:
            src=Path(d)/"src.png"; dst=Path(d)/"play.png"
            Image.new("RGB",(800,800),(36,55,90)).save(src)
            export_icon.run(src,"google",dst)
            result=validate.check(dst,"google","icon")
            self.assertTrue(result["technical_ok"],result["errors"])
            self.assertEqual(result["mode"],"RGBA")

    def test_phone_ratio(self):
        with TemporaryDirectory() as d:
            dest=Path(d)/"too-long.png"
            Image.new("RGB",(1080,2500),(255,255,255)).save(dest)
            self.assertFalse(validate.check(dest,"google","phone_screenshot")["technical_ok"])

    def test_perspective(self):
        try: import numpy
        except ImportError: self.skipTest("numpy not installed")
        img=Image.new("RGBA",(40,80),(255,80,30,255))
        warped=render.perspective_warp(img,[[10,10],[62,3],[66,96],[5,88]],(100,120))
        self.assertEqual(warped.size,(100,120))
        self.assertNotEqual(warped.getpixel((35,50))[3],0)

if __name__=="__main__":unittest.main()
