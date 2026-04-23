#!/usr/bin/env python3
"""Write meta-prompt.md by filling the four FILL IN placeholders in the business block (interactive or CLI)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PLACEHOLDER = "<FILL IN>"
# Expected order in meta-prompt.md: business name, website, owner name, owner phone
N_PLACEHOLDERS = 4


def _sanitize_for_backticks(s: str) -> str:
    """User values sit inside `...` in the markdown; strip backticks to avoid broken fences."""
    return s.replace("`", "'").strip()


def _prompt_line(label: str, required: bool) -> str:
    hint = "" if required else " (press Enter to skip — optional)"
    while True:
        try:
            raw = input(f"{label}{hint}: ").strip()
        except EOFError:
            print("", file=sys.stderr)
            raise SystemExit("Input aborted.")
        if raw or not required:
            return raw
        print("This field is required — please enter a value.")


def fill_meta_prompt(
    template: str,
    business_name: str,
    business_website: str,
    owner_name: str,
    owner_phone: str,
) -> str:
    if template.count(PLACEHOLDER) != N_PLACEHOLDERS:
        raise ValueError(
            f"Template must contain exactly {N_PLACEHOLDERS} {PLACEHOLDER!r} markers, "
            f"found {template.count(PLACEHOLDER)}. Restore meta-prompt.md from git or fix the file."
        )

    def opt(s: str) -> str:
        s = _sanitize_for_backticks(s)
        return s if s else "—"

    values = [
        _sanitize_for_backticks(business_name),
        _sanitize_for_backticks(business_website),
        opt(owner_name),
        opt(owner_phone),
    ]
    for v in (values[0], values[1]):
        if not v or v == "—":
            raise ValueError("Business name and business website are required (non-empty).")

    out = template
    for v in values:
        if PLACEHOLDER not in out:
            break
        out = out.replace(PLACEHOLDER, v, 1)
    if PLACEHOLDER in out:
        raise ValueError("Internal error: not all placeholders were replaced.")
    return out.rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Write meta-prompt.md with the business block placeholders filled for a new business."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="Project root (default: directory containing this script)",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=None,
        help="Template file to read (default: <root>/meta-prompt.md, must still contain the fill markers)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output file (default: <root>/meta-prompt.md)",
    )
    parser.add_argument(
        "--name",
        type=str,
        default=None,
        help="Business name (non-interactive; use with --website)",
    )
    parser.add_argument(
        "--website",
        type=str,
        default=None,
        help="Business website (non-interactive; use with --name)",
    )
    parser.add_argument(
        "--owner-name",
        type=str,
        default=None,
        help="Owner name (optional; empty string to omit)",
    )
    parser.add_argument(
        "--owner-phone",
        type=str,
        default=None,
        help="Owner/transfer phone, E.164 (optional; empty to omit)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    in_path = (args.input or (root / "meta-prompt.md")).resolve()
    out_path = (args.output or (root / "meta-prompt.md")).resolve()

    if not in_path.is_file():
        raise SystemExit(f"Template not found: {in_path}")

    template = in_path.read_text(encoding="utf-8")

    use_cli = args.name is not None or args.website is not None
    if use_cli:
        if args.name is None or args.website is None:
            raise SystemExit("With --name/--website, both --name and --website are required.")
        name = args.name
        website = args.website
        owner = args.owner_name if args.owner_name is not None else ""
        phone = args.owner_phone if args.owner_phone is not None else ""
    else:
        print("New AI receptionist — meta prompt (Ctrl+D / EOF to cancel)\n")
        name = _prompt_line("Business name", required=True)
        website = _prompt_line("Business website", required=True)
        owner = _prompt_line("Owner name (optional)", required=False)
        phone = _prompt_line("Owner/transfer phone, E.164 e.g. +16262784934 (optional)", required=False)

    try:
        text = fill_meta_prompt(template, name, website, owner, phone)
    except ValueError as e:
        raise SystemExit(str(e)) from e

    out_path.write_text(text, encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
