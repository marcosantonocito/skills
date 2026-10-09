# App Store Creative Director

Portable, English-language AI creative-director skill for visual assets used in Apple App Store and Google Play. The package includes a self-contained `SKILL.md`, guideline snapshots and links, editable JSON inputs, original visual composition examples, and Python production/validation utilities.

## Start here

1. Make this folder available to a skill-capable AI environment and request `app-store-creative-director`. If using ChatGPT without a compatible skill loader, attach `SKILL.md` and relevant references and ask ChatGPT to follow them. **A folder does not automatically install or activate a ChatGPT Plugin.**
2. Supply genuine app screenshots and any available branding or references. With sufficient context, the skill immediately shows **one creative preview using ChatGPT Create Image**. Three alternatives are optional when requested.
3. Give feedback on the image and iterate visually with Create Image. Approve the creative direction and, for a full listing, the screenshot narrative before final production. Generated previews may alter UI or lettering and are not exact product representations.
4. After approval, prepare separate authorized background/decorative artwork (AI generated or original). Use the deterministic renderer to composite original captures and exact text into selected canvas sizes; do not export AI-recreated interfaces as final screenshots.
5. Verify the latest official dimensions from the linked documentation, run validation, inspect the assets, then export/upload yourself.

## Runtime dependencies

- Python >= 3.10
- `Pillow>=10.0` (required)
- `numpy>=1.24` (only required for four-corner perspective placement)

Install with `python -m pip install -r requirements.txt`.

## Example commands

```bash
python scripts/render.py templates/render-example.json --output demo.png
python scripts/validate.py --platform apple --kind iphone_duo_outer --file demo.png
python scripts/export_icon.py icon-source.png --platform google --output app-icon-play.png
python -m unittest discover -s tests -v
```

The example manifest is instructional and references `sample-ui.png` (not included); replace that path with a real user-supplied capture before rendering. Original layout preview images under `assets/compositions/` are **inspiration diagrams, not publishable screenshots**.

## Limitations

- No live app deployment, emulator capture, or store publishing.
- No automated detection that the UI reflects the latest app build; developer must check.
- Apple's layered Liquid Glass icons are **not generated as Icon Composer projects** by a raster export. A 1024px PNG is only a design source/integration asset.
- Technical image validity is not equal to policy/legal approval. The supplied rules are snapshots (reviewed 2026-10-09) and require live verification.
- Native Create Image is the default for creative exploration and visual iteration; availability depends on the hosting environment. If unavailable, the skill uses available visual compositing tools and states the limitation.
- The production scripts support deterministic composition, exact text, and image validation after creative approval.
