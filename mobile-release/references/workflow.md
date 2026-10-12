# Workflow and file schemas

## Project instruction

Merge this block into the app root's `AGENTS.md` on first use. Replace `RESOLVED_SKILL_MD` with the actual absolute skill path. Scope the block to this app if `AGENTS.md` must live at a shared repository root.

```markdown
## Mobile development and release tracking

For every task that changes this Expo/React Native app, read and follow the
mobile-release skill at RESOLVED_SKILL_MD. Before finishing the task, record one
completed activity in the app root's DEVELOPMENT_LOG.md, with actual changes,
affected files, user-visible effects, and checks/results. Preserve existing
history and distinguish incomplete work. Read-only tasks need no entry.

Prepare a version only when explicitly requested with `$mobile-release release`
(optionally followed by patch, minor, or major), or an equivalent release request.
Use `$mobile-release refresh` to revise the current prepared documents without
bumping. Ordinary development must not increment versions. Release preparation
updates the Expo version, CHANGELOG.md, and APPSTORE.md and associates completed
ledger entries with that version. Builds and store publication are separate tasks.
```

## Development ledger

One durable file per app. Use the user's local date/time, with an offset if a timestamp is included. Technical notes default to English unless the project already uses another language.

```markdown
# Development Log

## Release preparations

## Activities

### DEV-0001 — Improve saved-session recovery
- Date: 2026-10-12
- Release: unreleased
- Category: Fixed
- Changes: Restore a valid saved session before displaying the sign-in screen.
- User impact: Returning users keep their session after restarting the app.
- Files: src/auth/SessionProvider.tsx; src/auth/session.test.ts
- Verification: Auth tests passed; device restart check not run.
- Deferred: None.
```

Increment IDs from the greatest existing ID; never recycle them. Valid categories: Added, Changed, Fixed, Removed, Security, Internal. Multiple technical bullets are welcome when one activity changes several things. Use `User impact: None (internal change)` when appropriate.

Update an existing entry for corrections or continuation of the same activity. For a reverted entry, explain the reversal and set `Release: excluded (reverted)`; keep any actual reversal activity that itself belongs in the release. Leave deferred changes out of its completed Changes and User impact. Preserve notes about failed checks; a later pass can be added without falsely rewriting what happened.

If an existing ledger uses another schema, preserve it and establish equivalent stable IDs, completed state, and release association rather than rewriting history. Reconstructed history must identify its evidence and uncertain date.

## Release preparation

### Snapshot and recovery

A release is a snapshot of completed, still-present activities. Normally select all eligible unreleased entries in the app; if the user chooses a subset, verify the excluded work is not in the intended build. A changelog is complete even when some entries have no public-facing effect.

An existing completed ledger entry is historical evidence when Git history is unavailable. Retain it unless current evidence contradicts it, and record verification limitations in the preparation record. Current files alone cannot prove an earlier rename or a previously successful test. Do not upgrade that uncertainty into a fresh verification claim; check observable behavior before deriving public benefits.

Add a preparation record before applying the candidate, after all necessary version decisions are settled:

```markdown
### 1.3.0
- Status: preparing
- Base version: 1.2.4
- Prepared date: 2026-10-12
- Activity IDs: DEV-0001, DEV-0002
```

Keep selected activity associations unchanged until the config, changelog, and store documents are coherent and validated. Then set each selected activity's `Release: 1.3.0` and set the preparation status to `prepared`. This means prepared locally, not shipped. Keep subsequent activity entries unreleased.

Before any bump, inspect current version, preparation records, and matching headings in the output files:

- An unfinished preparation resumes its recorded target and snapshot; do not bump again. If there is a conflict with later edits or another release, resolve it explicitly before mutating files.
- A repeated release with no eligible unreleased entries and a matching current prepared record validates or repairs that record without bumping or duplicating sections. If no such record exists, report that there is nothing to release.
- A normal release with new unreleased entries creates the next version. If an earlier preparation is still unfinished, finish or resolve it first.
- `refresh` uses the current record and its activity IDs, preserving version/date and any manually edited reviewer information. It does not silently consume new unreleased work. If the user wants to fold that work into the current preparation, confirm that choice and update the record's snapshot deliberately.

Stage complete candidate text in memory or temporary files before writing. Preserve unrelated working-tree edits. If applying a file fails, leave the preparation recoverable and report which parts are incomplete; do not mark activities consumed. Use narrow edits or atomic per-file replacement as appropriate; never use a Git reset as rollback.

### CHANGELOG.md

Prepend or update one version heading, in the project's existing style. Default:

```markdown
# Changelog

## [1.3.0] - 2026-10-12

### Added
- Allow users to organize saved items into collections. (DEV-0002)

### Fixed
- Restore saved sessions after restarting the app. (DEV-0001)
```

Include every selected activity, combining bullets only if all IDs remain covered. Use the ledger categories; omit empty groups. Include internal work under Internal. Do not claim unfinished work or unresolved bugs are fixed. Preserve existing links and older versions. Respect any existing Unreleased section: move only the included changes and retain the rest.

### APPSTORE.md

Use one version section, newest first, with the exact field headings below. Each field has exactly one `text` fenced block containing only copy suitable for its intended audience. Read [store-copy.md](store-copy.md) for how to write it. Keep readiness issues, character counts, and evidence outside the copy blocks.

````markdown
# Store Release Copy

## [1.3.0] - 2026-10-12

Prepared locally. Readiness: ready / missing reviewer information (describe outside copy).

### App Review Notes — en-US
```text
Reviewer instructions in English.
```

### App Review Notes — it-IT
```text
Istruzioni per la revisione in italiano.
```

### Promotional Text — en-US
```text
Current user benefit in English.
```

### Promotional Text — it-IT
```text
Beneficio attuale per l'utente in italiano.
```

### What's New — en-US
```text
Specific completed user-facing changes in English.
```

### What's New — it-IT
```text
Modifiche completate e visibili all'utente in italiano.
```

### Google Play Release Notes — en-US
```text
Concise factual update notes in English.
```

### Google Play Release Notes — it-IT
```text
Note informative e concise in italiano.
```
````

The outer fence above is illustrative; actual `APPSTORE.md` must use ordinary headings with individual text blocks. Keep `APPSTORE.md` out of published docs surfaces because it includes reviewer-only instructions. Store passwords and tokens in a secure channel, and refer to the separately supplied demo-account fields. For the app's first App Store submission, Apple's What's New field is unavailable: keep a local draft for the schema and mark it as not applicable to that submission outside its block.
