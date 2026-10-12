---
name: mobile-release
description: Track completed development tasks in Expo/React Native apps and prepare versioned changelogs and bilingual Apple/Google store copy. Use when modifying an Expo mobile app or explicitly asked to prepare a mobile release.
---

# Mobile Release

Keep a durable record of mobile development, then prepare release files on an explicit command. Skill instructions are in English; store copy is in Italian (`it-IT`) and English (`en-US`).

## Commands and activation

| Request | Behavior |
| --- | --- |
| An Expo app development task, or `$mobile-release` with a task | Perform the requested work and log its completed outcome. |
| `$mobile-release init` | Add the project instruction and initialize the ledger without inventing earlier changes. |
| `$mobile-release release` | Ask for patch/minor/major, showing the resulting versions. |
| `$mobile-release release patch`, `minor`, or `major` | Use the specified increment without asking again. |
| `$mobile-release refresh` | Regenerate the current prepared release's documents without incrementing the version. |

These are agent invocation phrases, not shell commands or an installed CLI. Ordinary edits must never trigger a version bump. Release preparation updates local files; builds, submissions, publishing, commits, and tags require a separate request.

## Locate and initialize the app

Read applicable project instructions and identify the mobile app root from its Expo config. Keep `DEVELOPMENT_LOG.md`, `CHANGELOG.md`, and `APPSTORE.md` at that root. In a monorepo, isolate each app's files; ask which app only if the target cannot be inferred.

On first use, merge the instruction from [references/workflow.md](references/workflow.md#project-instruction) into the app's `AGENTS.md`. Substitute the actual resolved path of this skill's `SKILL.md`; preserve existing instructions and avoid duplicate blocks. If the project already has an equivalent rule, reuse it. This setup is authorized as part of the skill's first use, unless the user has chosen manual setup. Initialize `DEVELOPMENT_LOG.md` using the schema in that reference, preserving any existing history.

Implicit selection makes the skill discoverable; the project instruction makes logging an explicit task requirement. This is not a filesystem watcher: edits made by people or unrelated tools require evidence-based reconciliation before a release.

## During development

Read [references/workflow.md](references/workflow.md#development-ledger) when initializing or updating the ledger.

After each completed app-changing activity, append one entry before the final response. Capture the actual changes, their purpose, user-visible effects, affected files, and checks with their results. Distinguish failures and skipped checks from passes. Log internal refactors, dependencies, configuration, and tests as well as visible features; group related file edits into one activity. Record completed portions of interrupted work honestly and leave unfinished items explicitly deferred.

Use the task's actual diff as evidence, accounting for pre-existing user changes. Never attribute those changes to this task. Do not add entries for read-only discussion, no-op tasks, or this skill's own bookkeeping. Update an entry for a resumed activity instead of duplicating it. Keep credentials, tokens, private customer data, and demo passwords out of these files.

## Prepare a release

Read [references/workflow.md](references/workflow.md#release-preparation) and [references/store-copy.md](references/store-copy.md). Follow the release transaction and file schemas there.

1. Reconcile unreleased ledger entries against the app's changes. Include only completed changes present in this app; identify reverted or deferred work. Recover missing history from reliable diffs/commits without fabricating task dates or successful checks. An empty release must not increment a version.
2. Determine the effective version source. Normally update `expo.version` in `app.json`. Check whether `app.config.js`/`app.config.ts` overrides it; if so, update the actual source and any inherited static value needed for consistency. Do not create a misleading `app.json` when the project uses only dynamic config. In bare projects, inspect native overrides too. Preserve `package.json`'s version unless it is explicitly coupled to the mobile version by the project.
3. For a stable `X.Y.Z`, show all three candidates if the increment is missing: patch `X.Y.(Z+1)`, minor `X.(Y+1).0`, major `(X+1).0.0`. Suggest patch for fixes, minor for new compatible functionality, major for substantial incompatible changes. The user selects when the command does not specify. Ask for an explicit target if the existing version is absent, malformed, or prerelease. Do not silently normalize it.
4. Preserve the existing EAS/native build-number policy. `ios.buildNumber` and `android.versionCode` are separate from the public version. Respect existing local automation if it explicitly runs during preparation; otherwise leave build counters to the build process and report any manual increment needed before upload. Never change remote EAS state or disable its auto-increment. Inspect runtime-version implications without changing the chosen policy.
5. Prepare a complete candidate: version update, a new `CHANGELOG.md` version containing every eligible activity, and `APPSTORE.md` with reviewer notes and both stores' copy in both languages. Retain previous versions and unrelated content. Record missing reviewer information separately as a readiness issue; do not invent an account or access procedure.
6. Validate copy with the helper and inspect version consistency, ledger coverage, existing history, and the final diff. Apply the files and then associate the ledger entries with the prepared version. Only mark the preparation complete after all files agree. If interrupted, recover the same target instead of incrementing again.

Use the standard-library helper when applicable, replacing `SKILL_DIR` with the resolved skill directory:

```sh
python3 SKILL_DIR/scripts/release_tools.py versions /path/to/app/app.json
python3 SKILL_DIR/scripts/release_tools.py check-copy /path/to/app/APPSTORE.md --version 1.3.0
```

The helper reads files only. Its checks cover structure and field lengths; verify factual accuracy, localization, confidentiality, and release coverage yourself. Run appropriate project checks for changed config without repeating unrelated full suites already completed.

Finish with the old/new version, changed file links, validation results, and material readiness gaps. Say that the release is prepared locally; never imply it has reached either store.
