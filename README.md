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
generate_meta_prompt.py        ← Fills meta-prompt.md (business name, URL, owner contact)
simulation-prompt.md           ← Generated master prompt to paste into Claude for a simulation
meta-prompt.md                 ← Paste the entire file into Cursor to scaffold; run generate_meta_prompt.py to fill the four business fields
README.md                      ← This file
requirements.txt               ← No pip deps; stdlib only (see script section)
```

---

## Scaffolding a Brand-New Business

Use the **meta prompt** (`meta-prompt.md`) to have Cursor overwrite the three config files (`config/agent.md`, `config/knowledge-base.md`, `config/actions.md`) for a **new** business. When those edits are done, run `generate_simulation_prompt.py` once (final step) to assemble `simulation-prompt.md`. Human workflow:

1. From the repo root, run `python3 generate_meta_prompt.py` (see below). It asks for the business name, website, and optional owner name and transfer phone, then fills the four placeholder lines at the top of `meta-prompt.md`. You can also pass those values with flags. To run the generator again later, restore the template first (e.g. `git restore meta-prompt.md`) or use `-i` with a file that still has all four `FILL IN` tokens (as in the committed template).
2. Start a **new Cursor chat** from the repo root, paste the **entire** contents of `meta-prompt.md` (nothing skipped), and send.
3. Cursor will fetch the website, extract the relevant info, and rewrite the three `config/*.md` files.
4. Review the three config files, then run `python3 generate_simulation_prompt.py` **once** from the repo root (only after all other edits are complete).

The reference implementation to mimic (tone, section order, formatting, quality bar) is the **Humble Bike Rentals** config on `main`. New work should branch from `main` so that reference stays in the tree — treat it as the gold standard.

---

## `generate_meta_prompt.py`

**Purpose:** Fills the four placeholder fields at the top of `meta-prompt.md` (business name, website, owner name, transfer phone) so you do not have to hand-edit them before pasting the full file into Cursor.

**Requirements:** Python 3.9+ and no third-party packages (stdlib only).

**Run from the repo root (interactive):**

```bash
python3 generate_meta_prompt.py
```

**Non-interactive example:**

```bash
python3 generate_meta_prompt.py --name "My Shop" --website "https://example.com" \
  --owner-name "Alex" --owner-phone "+12065551212"
```

Optional: `-o path/to/out.md` to write somewhere other than the default; `-i path/to/template.md` if the template is not the default `meta-prompt.md` (the template must contain exactly four `<FILL IN>` placeholders); `--root` if the project root is not the current directory. Optional owner fields can be omitted in interactive mode (press Enter) or left off the CLI; they are written as `—` in the output when not provided.

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
