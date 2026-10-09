# Google Play visual requirements (reviewed 2026-10-09)

The distinction between **requirements** and **highly recommended guidelines** matters. Open official pages when producing assets.

- Main preview specs: https://support.google.com/googleplay/android-developer/answer/9866151?hl=en-GB
- Listing best practices: https://support.google.com/googleplay/android-developer/answer/13393723?hl=en-GB
- Play icon specs: https://developer.android.com/distribute/google-play/resources/icon-design-specifications

## Feature graphic (required for store listing)

- Required: **1024×500**, JPEG or **24-bit PNG, no alpha**.
- Recommend placing key message and focal point in the center; edge regions may be cut off, UI overlays vary. Avoid excessive branding duplicating the app icon, tiny text, device imagery, store badges, and third-party logos. No unsupported rating, rank, discount, download, price, or award claims.

## Google Play listing icon (required)

- Required: **512×512**, **32-bit PNG (with alpha)**, max **1024 KB**. This is distinct from Android's adaptive launcher icon. Comply with Google's icon design specs, including safe area/masking; avoid pre-applying a rounded-corner mask for the listing icon.

## Phone screenshots

- **At least two screenshots across device types** required to publish a store listing; up to **8 per device type**.
- Required: JPEG or **24-bit PNG with no alpha**. Minimum side **320 px**, maximum side **3840 px**; longest side must be no more than twice shortest side.
- Highly recommended: **at least 4 app screenshots**, at least **1080×1920** in portrait (9:16) or **1920×1080** landscape (16:9), for recommendation formats. Place actual app UI prominently in the early screenshots. Extra taglines **recommended no more than 20%** of screenshot area.
- Avoid CTA text (install/download now), awards/rankings/sales language, UI unrelated to current app functionality, store badges, distracting status bars, and distorted or unrelated device frames.

## Tablet / large-screen screenshots

- Google identifies tablet-specific placements (7-inch, 10-inch); recommended to supply at least **four captures** for large screens. Page recommends **1080–7680 px** and **16:9 landscape / 9:16 portrait** for these device types. Read the currently published device-specific rules before certifying a custom tablet size; they are not interchangeable with Apple's pixel-exact iPad sizes.
- Do not scale phone UI into a fake tablet layout. Request real large-screen captures.

## Localizations & accessibility

- Localize marketing taglines, feature graphics, and other copy appropriately; use localized real screenshots when available.
- Provide helpful alt text for graphical assets on Play, **up to 140 characters** in Google's recommendations.
- Use verifiable claims only. No guarantees of ranking/featuring/store acceptance.
