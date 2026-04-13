---
# Humble Bike Rentals — AI Receptionist Simulation

## File Structure

```
/config
  agent.md          ← Persona, tone, call flow, conversation rules
  knowledge-base.md ← Business info, pricing, policies, FAQs, routes
  actions.md        ← Triggerable actions with conditions and scripts
simulation-prompt.md  ← Master prompt to paste into Claude to run a simulation
README.md             ← This file
```

---

## How to Run a Simulation

1. Open `simulation-prompt.md`
2. Replace the three placeholder comments with the full contents of the corresponding config files
3. Paste the entire assembled prompt into a new Claude chat
4. Claude will open with Declan's greeting — you play the caller

---

## How to Update Each File

| File | When to edit |
|---|---|
| `agent.md` | Change persona, tone, call flow steps, escalation rules |
| `knowledge-base.md` | Update pricing, hours, policies, FAQs, add/remove inventory |
| `actions.md` | Add, remove, or modify triggerable actions and transfer numbers |
| `simulation-prompt.md` | Change simulation behavior rules (not the business content) |

---

## Tips

- Test edge cases first — frustrated callers, out-of-scope questions, transfer triggers
- After making changes to any config file, re-assemble `simulation-prompt.md` before the next simulation
- The simulation prompt mirrors the live GHL Voice AI configuration — keep them in sync
---
