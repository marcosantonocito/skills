#!/usr/bin/env python3
"""Read-only version candidates and store-copy structure/length checks."""

import argparse
import json
import re
import sys
from pathlib import Path


def versions(path):
    config = json.loads(path.read_text(encoding="utf-8"))
    version = config.get("expo", {}).get("version")
    if not isinstance(version, str) or not re.fullmatch(
        r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", version, flags=re.ASCII
    ):
        raise ValueError("expo.version must be a stable X.Y.Z; ask for an explicit target")
    major, minor, patch = map(int, version.split("."))
    return {
        "static_version": version,
        "patch": f"{major}.{minor}.{patch + 1}",
        "minor": f"{major}.{minor + 1}.0",
        "major": f"{major + 1}.0.0",
        "verify_effective_source": "Check dynamic Expo config and native overrides before editing",
    }


def check_copy(path, version):
    document = path.read_text(encoding="utf-8")
    headings = list(re.finditer(r"^## \[([^\]\n]+)\][^\n]*$", document, re.MULTILINE))
    matches = [i for i, heading in enumerate(headings) if heading.group(1) == version]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one version heading for {version}")
    index = matches[0]
    # End at the next level-two heading, including unrelated sections.
    tail = document[headings[index].end():]
    boundary = re.search(r"^## ", tail, re.MULTILINE)
    section = tail[:boundary.start()] if boundary else tail
    fields = list(re.finditer(r"^### (.+)$", section, re.MULTILINE))
    contents = {}
    errors = []
    for i, heading in enumerate(fields):
        name = heading.group(1)
        if name in contents:
            errors.append(f"Duplicate field: {name}")
        end = fields[i + 1].start() if i + 1 < len(fields) else len(section)
        body = section[heading.end():end]
        blocks = re.findall(r"^```text\n(.*?)\n```[ \t]*$", body, re.MULTILINE | re.DOTALL)
        if len(blocks) != 1:
            errors.append(f"Expected one text block: {name}")
            contents[name] = ""
        else:
            contents[name] = blocks[0]

    budgets = {
        "App Review Notes": (4000, "utf8_bytes"),
        "Promotional Text": (170, "apple_characters"),
        "What's New": (4000, "apple_characters"),
        "Google Play Release Notes": (500, "unicode_characters"),
    }
    counts = {}
    for field, (limit, measure) in budgets.items():
        for locale in ("en-US", "it-IT"):
            name = f"{field} — {locale}"
            if name not in contents:
                errors.append(f"Missing field: {name}")
                continue
            copy = contents[name]
            chars = len(copy)
            units = len(copy.encode("utf-16-le")) // 2
            bytes_count = len(copy.encode("utf-8"))
            size = {"utf8_bytes": bytes_count, "apple_characters": max(chars, units),
                    "unicode_characters": chars}[measure]
            counts[name] = {"characters": chars, "utf16_units": units,
                            "utf8_bytes": bytes_count, "limit": limit, "measure": measure}
            if not copy.strip():
                errors.append(f"Empty field: {name}")
            if size > limit:
                errors.append(f"Over limit: {name} ({size} > {limit})")
    return {"version": version, "valid": not errors, "fields": counts, "errors": errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    candidate_parser = commands.add_parser("versions")
    candidate_parser.add_argument("config", type=Path)
    copy_parser = commands.add_parser("check-copy")
    copy_parser.add_argument("document", type=Path)
    copy_parser.add_argument("--version", required=True)
    args = parser.parse_args()
    try:
        result = versions(args.config) if args.command == "versions" else check_copy(args.document, args.version)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("valid", True) else 1
    except (OSError, ValueError, TypeError, AttributeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
