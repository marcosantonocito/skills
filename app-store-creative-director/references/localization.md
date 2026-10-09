# Localization workflow

1. Ask for intended locale tags (`en-US`, `it-IT`, etc.) and the translated app's genuine captures for each OS/device/locale. Do not alter or retranslate screen UI with an image model.
2. Translate marketing copy **for the meaning and the market**, not mechanically. Keep benefits and any verifiable claims equivalent. Ask for user approval.
3. Re-layout text if localized strings expand. Prefer keeping a stable palette, type system, hierarchy, and story order; resizing should stay within legibility thresholds and safe zones.
4. Consider RTL and non-Latin fonts; use user-licensed font families that include needed glyphs. Detect missing glyphs visually. A default system font may not cover all locales.
5. Verify target device assets per locale. If a required source capture is unavailable, label it clearly and do not silently substitute another language's screenshot.
6. Log a locale manifest: capture filename, translated headline, source/approval status, and QC outcome.

Auto-translation is not proof of quality. Human approval remains required for localized taglines and UI consistency.
