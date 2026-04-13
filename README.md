# Humble Bike Rentals — AI Receptionist Simulation

## Workflow

1. **Cursor (or any editor)** — Iterate on the live agent config: edit `config/knowledge-base.md`, `config/agent.md` (system prompt), `config/actions.md`, and anything else under `config/` or the generator as needed.
2. **Regenerate the assembled prompt** — From the repo root, run `python3 generate_simulation_prompt.py` so `simulation-prompt.md` reflects your latest changes.
3. **AI chat (Claude or whatever you use)** — Open a new chat, paste the **full** contents of `simulation-prompt.md`, send it, and you’re in a **simulated** call: the model plays the receptionist and you play the caller.

---

## File Structure

```
/config
  agent.md          ← Persona, tone, call flow, conversation rules
  knowledge-base.md ← Business info, pricing, policies, FAQs, routes
  actions.md        ← Triggerable actions with conditions and scripts
generate_simulation_prompt.py  ← Builds simulation-prompt.md from the three config files
simulation-prompt.md           ← Generated master prompt to paste into Claude for a simulation
README.md                      ← This file
requirements.txt               ← No pip deps; stdlib only (see script section)
```

---

## `generate_simulation_prompt.py`

**Purpose:** Regenerates `simulation-prompt.md` automatically by injecting the full contents of `config/agent.md`, `config/knowledge-base.md`, and `config/actions.md` into the simulation template (intro, `[SYSTEM PROMPT]`, `[KNOWLEDGE BASE]`, `[ACTIONS]`, and the roleplay rules footer). That way you edit the config files once and always get a single assembled prompt for testing—no manual copy-paste between files.

**Requirements:** Python 3.9+ and no third-party packages (stdlib only).

**Run from the repo root:**

```bash
python3 generate_simulation_prompt.py
```

Optional: `python3 generate_simulation_prompt.py -o path/to/output.md` to write elsewhere; `--root` if running from another directory.

---

## How to Update Each File

| File | When to edit |
|---|---|
| `agent.md` | Change persona, tone, call flow steps, escalation rules |
| `knowledge-base.md` | Update pricing, hours, policies, FAQs, add/remove inventory |
| `actions.md` | Add, remove, or modify triggerable actions and transfer numbers |
| `simulation-prompt.md` | Do not edit by hand for content—regenerate with the script after config changes |

---

## Tips

- Test edge cases first — frustrated callers, out-of-scope questions, transfer triggers
- Run `generate_simulation_prompt.py` after editing any file in `config/`
- The simulation prompt mirrors the live GHL Voice AI configuration — keep them in sync
