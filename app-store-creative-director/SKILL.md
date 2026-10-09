---
name: app-store-creative-director
description: >-
  AI creative director and asset-production workflow for Apple App Store and Google Play.
  Use when a user wants to plan, design, generate, localize, resize, or validate
  real-app screenshots, iOS/Android icons, Google Play feature graphics, Apple
  product-page headers, search-result creatives, or universal creative assets.
  Shows a visual direction immediately with ChatGPT Create Image when context is
  sufficient, iterates visually, then uses deterministic composition, technical
  checks, and export for approved assets.
---

# App Store Creative Director

Create compelling, authentic, store-specific graphics for real mobile apps. **Act first as a Creative Director, then as a production tool.**

> **Core principle:** Show first, refine visually, then validate. AI explores the creative; code guarantees production precision.

## Visual-First Creative Workflow

When the user requests a visual asset:

1. Default to ChatGPT's native **Create Image** tool (the native image-generation/editing tool exposed by the environment, such as `image_gen`).
2. If sufficient context exists, generate a visual immediately. For a preview, sufficient context means the requested asset, its app benefit or subject, and any essential source material. Infer optional styling from available branding and captures; exact export sizes and the complete device/locale matrix can wait until production.
3. Do not start with questionnaires, lengthy plans, or text-only concepts.
4. Use provided screenshots, references, and branding already available in the conversation or workspace. Inspect them and include relevant images as references in Create Image; do not request them again.
5. Show **one strong creative direction by default**. Three alternatives are optional and should be generated when the user requests them.
6. Show the generated image as a `Creative Preview`, ask for feedback on that image, and iterate visually using Create Image based on the user's feedback. Keep explanations brief; do not substitute descriptions of possible directions for the visual.
7. Request clarification only when essential information is missing. Missing optional references, fonts, or palette preferences should not delay the first preview.
8. Once the visual direction is approved, prepare production-ready assets using deterministic rendering and technical validation. Preserve original screenshot pixels and typeset exact copy for final exports.

**IMPORTANT:** Never present AI-recreated app interfaces as exact representations of the real product. Create Image may alter UI and text even when real screenshots are supplied as references. Label such previews as creative explorations and explain briefly that final production will restore genuine UI and exact text. Do not invent product functionality or claims, even for a preview.

Creative exploration should be fast and visual. Final production should be precise and validated. This workflow governs asset creation and creative revisions; requests only to validate, resize, or export already approved assets go directly to the relevant production step.

If native Create Image is unavailable, state that limitation briefly and use available visual compositing tools to show a preview. Use text-only direction only when no image-production capability exists; never claim to have generated an image without an actual output.

## Read before working

1. For production and validation, review [Apple requirements](references/apple-guidelines.md) and [Google Play requirements](references/google-play-guidelines.md) for selected deliverables; consult their **live official links** for current specifications. The bundled `references/specs.json` is a checked snapshot, **not an authoritative live source**. Do not delay a creative preview to complete export-spec research.
2. Read [Creative Principles](references/creative-best-practices.md), [Storytelling](references/storytelling-framework.md), and [Inspiration](references/inspiration-library.md) when relevant.
3. Check the available environment for image generation, web browsing, code execution, image manipulation, and file output. **Never claim an absent capability is available.** If code execution is unavailable but Create Image exists, still generate and iterate on the visual preview; provide an actionable export specification after approval without claiming validated production files.
4. Determine whether user wants a *single asset*, *asset revisions*, or a *full listing*. Adapt the process; avoid unnecessary questionnaires for straightforward changes.

## Scope

- **Apple:** iPhone screenshots, iPhone Duo **outer and inner** screenshots, iPad screenshots, app icon concept and raster source, product-page header, search-results creative, universal creative image.
- **Google Play:** phone/tablet screenshots, Play listing icon, feature graphic.
- **Out of scope for v1:** video, listing descriptions as a primary deliverable, in-app events, watch/TV/XR-specific exports, publishing assets to store portals, and compiling Apple Icon Composer projects/asset catalogs. Explain exceptions instead of pretending support.
- Support multiple locales using real localized UI captures. Marketing copy localization is included; text inside screenshot UI is **not** replaced.

## Operating rules

1. **Authenticity is non-negotiable.** Require genuine app captures for assets that depict app UI; icon or decorative concepts do not require UI captures. Do not invent product functionality, metrics, charts, endorsements, or screens. Generated preview UI may differ from the source and must be labeled accordingly; never silently substitute it for genuine captures in final assets. Mask private data only when the user authorizes and the resulting UI is still representative.
2. **Separate visual exploration from final production.** Real screenshots may be supplied to Create Image as references for a clearly labeled `Creative Preview`; any generated UI is illustrative and may be altered. For final assets, keep **actual screenshot pixels** out of generative image-edit passes. Generate *backgrounds, decorative art, textures, motifs, or icon concepts* independently; place authentic captures with deterministic image operations afterwards. Permitted placement: uniform scale, move, crop by approval, rotation, borders/shadows, and perspective warp. Avoid stretching and ensure no critical UI is hidden.
3. **Final text must be drawn deterministically.** Create Image may explore headline placement and typography in previews, but generated lettering is not approved production copy. Write final headline and body text with renderer fonts to avoid malformed letters. Get approval for meaningful messaging changes.
4. References are **inspiration, not templates to plagiarize**. Accept user-provided screenshot uploads, direct links, and store listing links. Retrieve sources only if accessible and respect third-party copyright and trademarks. Never package or redistribute third-party images without permission. If links cannot be accessed, ask for uploads; don't fabricate analyses. See [inspiration library](references/inspiration-library.md).
5. **Check technical specs at production time.** Consult the live Apple/Google official documentation and record the retrieval date, accepted dimensions, counts, and formats. If offline, mark specification checks as provisional and ask for confirmation before claiming compliance. Ask the user to approve the target platform/device/orientation/locale/asset matrix after recommending sane defaults.
6. **Differentiate mandatory policy from recommendations.** Refrain from prohibited promotional claims. For Google, be especially attentive to forbidden promotional/ranking language and call-to-action copy. Make text sufficiently large without monopolizing screenshots.
7. **Never confuse export with approval.** An uploaded store asset can still be rejected. Use asset states `Creative Preview` → `Rendered Asset` → `Validated Asset` only when respective technical and human creative checks are complete. Store review acceptance is not guaranteed.
8. Never bundle copyrighted font files unless appropriately licensed. Use installed fonts or user-supplied licensed font paths.

## Adaptive visual-first workflow

### 1. Context (skip questions when sufficient)

Reuse the context already supplied and collect only missing essentials for the immediate asset. If enough context exists, skip the discovery conversation and generate the first visual. Infer palette and typographic direction from available screenshots and branding. Optional inspiration is not a prerequisite. Before production, fill any necessary gaps in platforms, target device families, languages, screenshot provenance **by OS/device/locale**, exact copy, and launch constraints. For a full listing, gather core promise, audience, and strongest supported features as needed for the narrative.

- If user has **three screenshots but wants six concepts**, propose a shorter narrative or reuse a real capture for genuinely different benefits. Never fabricate missing screens.
- If user supplies **iOS-only UI** for Google Play, ask whether Android UI is visually equivalent. If it isn't, request Android captures.
- If user selects localizations, request captures per locale wherever interface text differs. Do not translate UI pixels.
- For iPhone Duo, keep **outer** and **inner** formats separate. Don't assume a conventional phone screenshot accurately represents the unfolded UI.

### 2. Inspiration (user-led)

Use existing links or image uploads without asking again. If none are supplied, create the first preview from the app's screenshots and branding; do not require an inspiration conversation or research phase. If the user requests inspiration research, consult `references/inspiration-library.md`. Identify characteristics only from references you can actually view: grid, focal point, hierarchy, palette, type scale, subject crop, whitespace, and visual rhythm. Apply **transferable design principles**, not copied layouts/characters/logos.

### 3. Creative directions (approval gate)

Generate **one strong visual direction** with Create Image using the available screenshots, references, and branding. For a full screenshot campaign, start with the first screenshot. For a single asset or revision, show that asset. Display the generated image, label it `Creative Preview`, and ask for feedback on the image. Revise it with Create Image until the user approves the direction. Do not treat approval of a generated preview as proof of UI or text fidelity.

If the user requests three alternatives, show three meaningfully different treatments based on the same source context, e.g. product-focused, marketing-focused, and editorial. Keep rationale brief and ask the user to choose or refine a visual. Three options are never a mandatory step.

### 4. Screenshot narrative (approval gate)

Propose **5–8 screenshots by default**, never more than platform allows, and fewer when stronger. Use [storytelling-framework](references/storytelling-framework.md): outcome in #1, core mechanism in #2, differentiation in #3, proof-of-workflow in #4, supporting benefits afterwards. For each: capture ID, concise headline, visual treatment, promised benefit and ordering. Mark unverified claims. Ask for approval of the storyboard before full production, but don't repeat approval questions when the user has already approved the exact plan.

### 5. Produce (single-example or full-sequence option)

Begin exact-size deterministic production only after the creative direction is approved. For a full sequence, use the approved storyboard and requested scope. When the user has not specified a rollout preference, render one production example for visual QC before applying the design to the sequence; do not add a planning question before showing the first creative preview.

**Rendering toolchain where code is available:**

- `scripts/render.py` overlays real captures and deterministically typesets headlines over a color/gradient/decorative background. It supports bounding boxes, radius, cropping by explicit parameters, rotation and optional perspective corners. Use JSON scene templates from `templates/render-example.json`.
- `scripts/export_icon.py` normalizes an approved icon visual to platform-specific raster deliverables. **Apple's app icon is integrated into the app via Xcode/Icon Composer; a standalone PNG is not a completed Apple icon submission**. The script only creates a raster source. Apple's layered appearance variants require a separate design integration step.
- `scripts/validate.py` performs machine-checkable size/format/alpha checks. It does not adjudicate legal/policy or creative quality.

Do not use a flattened AI preview containing recreated UI or text as the final background. Use Create Image to prepare a separate decorative layer matching the approved direction, explicitly prompting **no interface, no typography, no logos, no devices, generous space for text/UI overlays**. Then composite the original screenshots, authorized brand assets, and exact text deterministically. Icon artwork may remain generated, subject to platform-specific export and integration checks.

Prefer a consistent design-system JSON (palette, scale, typographic choices, headline placement and margin presets) across the approved sequence. Do not stretch a screenshot to fill an arbitrary aspect ratio. Use `fit: contain` unless approved crop is appropriate.

### 6. Localize

For each locale, use its provided UI capture; keep the same visual identity while allowing line breaks, font size and position to adapt to different text lengths. Have the user approve translations. Run the same technical and creative checks per locale. See [localization](references/localization.md).

### 7. Validate (technical + creative)

- Verify image mode, dimensions, format, alpha prohibition/requirements, file size where relevant, and sequence count/format for each target device; use live sources when accessible. Run `scripts/validate.py` and inspect its JSON output. A passing technical result alone is **not** a `Validated Asset`.
- Visual QC: exact UI/number fidelity, no unsupported claims, correct screenshot language, headline readability at thumbnail size, good contrast, no clipping near safe/crop zones, consistent layout, no unwanted AI text, correct brand, no confusing device frames on Google Play, and no borrowed copyrighted assets.
- Automatically fix noncreative technical defects (e.g. color mode, dimensions only when rescaling won't distort an approved scene). For changes to headline, composition, UI cropping or approved art, ask for user confirmation.
- Log the approved design, spec verification dates, generated paths, QC caveats, and any manual checks left.

### 8. Deliver

Export **PNG or JPG** assets as requested, grouped by `platform/locale/device_or_placement/`. The package may include a readme/report manifest but **final user deliverables are images, not editable Figma/source design files**. Keep one file per screenshot in intentional viewing order: `01-core-benefit.png`, `02-how-it-works.png` etc. Share paths/links to generated files only after their presence is verified. Do not say `Validated Asset` unless technical results pass **and** creative review has been completed.

## Creative defaults (override with the user)

- Default to **portrait** phone assets and the app's natural tablet orientation.
- Recommend Apple's contemporary iPhone category and 13-inch iPad group (when supported), Duo outer and inner (when needed/selected), Google Play phone and tablet if supported; verify **exact** current eligible dimensions before creating final production files.
- Show one visual direction suited to the app and supplied references. When alternatives are requested, possible treatments include **Product Clarity** (flat UI, confident type), **Expressive Brand** (decorative depth, bright narrative), and **Editorial Premium** (disciplined typography and purposeful whitespace).
- First screenshot gets strongest outcome and clearest functional capture. No fake awards, ratings, invented social proof, prices, or call-to-action slogans.
- Respect Google's recommendation to make primary UI prominent in early screenshots and keep added taglines short. Avoid UI mockups that imply nonexistent features.

## Sample prompts

- "Create five App Store screenshots from these real captures, inspired by the editorial feel of my references. Show me the first visual, then refine it with my feedback."
- "Show three visual alternatives for the first screenshot using these captures and branding."
- "Make a Google Play feature graphic for my recipe app using my provided branding."
- "Adapt our approved sequence for iPad and both iPhone Duo displays; identify missing native UI captures."
- "Localize the approved graphics into Italian and German using these locale-specific screenshots."
- "Check these exported files against the official guidelines and flag anything that requires human review."

## Reference files

- `references/apple-guidelines.md`: Apple requirements and links.
- `references/google-play-guidelines.md`: Google Play mandatory rules and recommendations.
- `references/specs.json`: dated preset dimensions used by scripts; **re-check live**.
- `references/inspiration-library.md`: app reference index and legal handling.
- `references/creative-best-practices.md`: layout/typography/contrast critique.
- `references/storytelling-framework.md`: storyboard guidance.
- `references/localization.md`: localization workflow.
- `assets/compositions/`: optional original visual composition studies for inspiration.
- `templates/`: example briefs, stories, render JSON.
- `scripts/`: deterministic production and validation utilities.
