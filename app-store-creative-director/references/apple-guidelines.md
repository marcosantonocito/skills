# Apple App Store visual requirements (reviewed 2026-10-09)

**Always open the official pages at production time.** These are a reference snapshot, not a promise of future eligibility.

## Official sources

- Best practices: https://developer.apple.com/app-store/asset-best-practices/
- Screenshots: https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications
- Creative assets: https://developer.apple.com/help/app-store-connect/reference/app-information/creative-assets-specifications
- Manage creative assets: https://developer.apple.com/help/app-store-connect/manage-app-information/manage-your-app-store-assets
- Icons/HIG: https://developer.apple.com/design/human-interface-guidelines/app-icons/
- Icon Composer: https://developer.apple.com/icon-composer/

## Screenshots

- **At least 1** and **at most 10 per device size**; `.jpeg`, `.jpg`, `.png`; **no alpha/transparency**.
- Required group: an iPhone Dynamic Island medium-display screenshot for iPhone apps; **13-inch iPad** for iPad-compatible apps. App Store Connect can scale provided screenshots to other sizes when UI is consistent. Verify requirements and any scaling exceptions for the current app.
- Valid recent iPhone Dynamic Island medium sizes include `1179×2556` or `1206×2622` (and landscape reversals). Accepted Dynamic Island large sizes include `1260×2736`, `1290×2796`, or `1320×2868` (and reversals).
- 13-inch iPad screenshots include `2064×2752`, `2048×2732` (and landscape reversals).
- **iPhone Duo:** outer `1398×2034`; inner `2007×2853` (or landscape reversals). **Apple's published October 2026 notice says screenshots become required from April 2027 for apps using the iOS 27.1 SDK or later.** Treat outer and inner as separate captures/design targets. Confirm SDK and current policy when publishing.
- App screenshots must represent real app usage. Hero copy and supplemental graphic treatment must not mislead about functionality.

## Apple creative images (iOS/iPadOS 27+ placement support)

- Product page header: `3840×1646` (21:9) JPEG/PNG without alpha, or `5244×2950` (16:9 universal PNG).
- Search results: `1920×1280` through `3840×2560` at 3:2 (JPEG/PNG without alpha), or `5244×2950` (16:9 universal PNG).
- A **universal creative asset** uses the 16:9 `5244×2950` format so the same approved image can serve header and search results. Confirm exact use and latest placement controls.
- No alpha/transparency. Safe visual zones can vary by placement; avoid placing must-read text on edges and preview in App Store Connect.
- In-App Events and video are excluded from this version of the skill.

## Apple app icon design

- Apple HIG describes 1024×1024-square icon layouts for iPhone and iPad, with layered appearances (default, dark, clear and tinted). Use the approved PNG export only as a raster source or flat concept, **not as a complete layered icon submission**.
- Apple recommends Icon Composer and proper Xcode integration; **do not claim a PNG uploaded alongside screenshots changes the iOS app icon**.
- Keep the symbol distinct at small sizes. Don't bake system-rounded-corner masks into artwork. Verify current appearance/icon pipeline with Xcode and HIG.
