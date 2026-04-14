#!/usr/bin/env python3
"""Generate simulation-prompt.md by injecting config/*.md into the master template."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent

HEADER = """---
You are simulating an AI voice receptionist on a live phone call. Below are the SYSTEM PROMPT, KNOWLEDGE BASE, and ACTIONS that define how the agent should behave.

---

[SYSTEM PROMPT]
"""

FOOTER = """---

Your job is to roleplay as that receptionist for the entire conversation. I am the caller.

Rules:
- Stay in character at all times
- Speak naturally and briefly — this is a phone call, not a chat. 1–2 sentences max unless detail is truly needed
- Never break character to explain what you're doing
- When an action triggers, announce it in brackets on its own line — e.g. [ACTION: SMS Sent — Booking Link → caller's number] — then continue the call naturally
- Never invent information not found in the knowledge base
- If you genuinely can't answer, trigger the Call Transfer action

When you're ready to begin, respond only with the agent's opening greeting as defined in the system prompt — then wait for my first message as the caller.
---
"""


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").rstrip() + "\n"


def build_simulation_prompt(
    agent_path: Path,
    knowledge_path: Path,
    actions_path: Path,
) -> str:
    agent = read_text(agent_path)
    knowledge = read_text(knowledge_path)
    actions = read_text(actions_path)

    parts = [
        HEADER,
        agent,
        "\n---\n\n[KNOWLEDGE BASE]\n",
        knowledge,
        "\n---\n\n[ACTIONS]\n",
        actions,
        FOOTER,
    ]
    return "".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Write simulation-prompt.md with config markdown files injected."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="Project root (default: directory containing this script)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output file (default: <root>/simulation-prompt.md)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    out = (args.output or (root / "simulation-prompt.md")).resolve()

    agent_path = root / "config" / "agent.md"
    knowledge_path = root / "config" / "knowledge-base.md"
    actions_path = root / "config" / "actions.md"

    for p in (agent_path, knowledge_path, actions_path):
        if not p.is_file():
            raise SystemExit(f"Missing required file: {p}")

    text = build_simulation_prompt(agent_path, knowledge_path, actions_path)
    out.write_text(text, encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
