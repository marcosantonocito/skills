# Store copy guidance

## Basis and official constraints

Adapted from the user's supplied App Store copywriting brief. Its useful advice is to lead with benefits, put significant changes first, write plainly, and localize naturally. The limits and distinctions below correct conflicting claims in that brief. Official references checked on 2026-10-12; recheck them if a platform rejects a field or policies/limits become uncertain.

| Field | Audience | Limit per locale |
| --- | --- | --- |
| Apple Promotional Text | Prospective users | 170 characters |
| Apple What's New | Users considering an update | 4,000 characters |
| Apple App Review Notes | Apple reviewers; private | 4,000 UTF-8 bytes |
| Google Play Release Notes | Users considering an update | 500 Unicode characters |

Apple's limits, localized version metadata, initial-release exception, and review-note purpose come from [Platform version information](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/). Promotional text can change independently of a version and does not affect search ranking; Apple recommends prioritizing new functionality and may use a CTA in What's New: [Creating your product page](https://developer.apple.com/app-store/product-page/).

Google's release notes should describe updates and must not be used for promotional purposes or to solicit user actions: [Prepare and roll out a release](https://support.google.com/googleplay/android-developer/answer/9859348?hl=en-GB).

Public version versus build counters and EAS local/remote behavior: [Expo app version management](https://docs.expo.dev/build-reference/app-versions/).

## Facts before wording

Use the release snapshot, app behavior, existing product messaging, and any brand instructions as evidence. If necessary, inspect the app to understand the benefit. Never invent discounts, availability dates, performance gains, user-feedback provenance, integrations, reviewer accounts, or features hidden behind an unavailable flag. Describe a backend change as a public benefit only when that benefit is actually present for this release's users.

Internal maintenance belongs in the changelog; it does not automatically imply a faster, more stable, or safer app. For an internal-only release, use a modest factual maintenance statement without fabricated claims. Promotional text can highlight an established, currently available core benefit if this release has no new marketable feature.

## Apple promotional text

Write one clear sentence or two short sentences. Put the main current benefit first; make the opening roughly 70 characters meaningful as an editorial target, not a guaranteed truncation rule. A natural CTA is optional. A useful target is 90–160 characters, with 170 as the hard maximum for each translation separately.

Use plain text without URLs, markup, or emoji as this workflow's house style. The supplied brief's blanket claims about emoji/link bans are not established here as universal platform rules. Avoid keyword stuffing, competitor comparisons, unverifiable superlatives, and invented offers. Keywords are not the purpose of this field. Upcoming features or promotions may be mentioned only when the user explicitly supplies accurate, current details.

Example for a verified new collection feature:

- en-US: `Keep your saved items organized with collections. Find what you need and pick up where you left off.`
- it-IT: `Organizza gli elementi salvati in raccolte. Ritrova ciò che ti serve e riprendi da dove eri rimasto.`

## Apple What's New

Describe significant product changes specifically, in order of user importance. Translate technical details into the behavior the user can observe. Prefer 2–5 short bullets when the release supports them; a single useful sentence is enough for a small patch. Aim for fewer than 500 characters for ordinary releases, while allowing more for substantial updates within 4,000.

A soft CTA can be included when useful. Plain hyphen bullets and line breaks are sufficient; avoid URLs, Markdown emphasis, HTML, and decorative emoji in the copy blocks. Mention a specific fixed symptom when known. Never attribute work to user feedback unless the source supports it. Do not repeat the full listing description or hide important changes behind generic maintenance language.

## Google Play release notes

Draft these independently of the Apple wording: the tighter limit and prohibition on promotional copy/soliciting actions require different text. Describe only recent changes. Do not include invitations to update, download, try, review, buy, or claim a discount. Prefer 1–4 concise factual bullets, usually under 350 characters and always at most 500 per locale. Use plain text without URLs, HTML, or decorative emoji for consistent house style.

Example:

- en-US: `- Organize saved items into collections.\n- Fixed a sign-in issue after restarting the app.`
- it-IT: `- Organizzazione degli elementi salvati in raccolte.\n- Risolto un problema di accesso dopo il riavvio dell'app.`

Use actual newlines in the final field, not literal backslash-n sequences.

## Private App Review notes

Prepare English reviewer instructions plus an Italian equivalent. State what changed and how a reviewer can reach and test it, including non-obvious navigation, necessary permissions, hardware, regional availability, and purchase/restore paths only when relevant and verified. State when no login is required if the app actually works that way.

Read and preserve useful existing reviewer context. If authentication is required, refer to the demo credentials supplied separately in App Store Connect's sign-in fields; do not write passwords or tokens to tracked Markdown. If access details are missing, list the gap outside the copy block and keep readiness incomplete. Do not assert that credentials have been supplied or tested without evidence. The two languages are alternative drafts for Apple's single Notes field, not separate localized App Review submissions.

## Localization and validation

Use natural Italian and US English with the same factual meaning. Preserve product and feature names according to existing branding. Each locale gets its own character budget; do not combine them. Count only exact field text, including spaces, punctuation, and internal line breaks. Review notes use UTF-8 bytes; the helper uses Unicode code-point counts for the other fields and also reports UTF-16 units for conservative checking of Apple's character limits.

Before completing the files, confirm the release version and ledger coverage, verify every public claim against completed work, and check spelling and the limits in both languages. Do not copy private reviewer material into public release notes. Keep sources, counters, missing-information markers, and internal activity IDs outside copy blocks. Do not add unsupported conversion-uplift figures or a mandatory campaign/testing workflow to an ordinary release.
