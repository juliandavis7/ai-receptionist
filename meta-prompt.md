# New AI Receptionist — Meta Prompt

Use this prompt to scaffold the "brains" for an AI voice receptionist for a **new business**. Cursor will overwrite the three config files (`config/agent.md`, `config/knowledge-base.md`, `config/actions.md`). When those are done, run `generate_simulation_prompt.py` once (final step) to assemble `simulation-prompt.md`.

---

## How to use

1. Start a **new Cursor chat** from the repo root.
2. Paste the **Instructions** block below, filling in `BUSINESS NAME` and `BUSINESS WEBSITE` (and, if you have them, owner name / owner phone).
3. Cursor will fetch the website, extract the relevant info, and rewrite the three `config/*.md` files.
4. Review the three config files, then run `python3 generate_simulation_prompt.py` **once** from the repo root (only after all other edits are complete).

The reference implementation to mimic (tone, section order, formatting, quality bar) is the **Humble Bike Rentals** config on `main`. New work branches from `main`, so that reference stays available in the repo — treat it as the gold standard.

---

## Instructions (paste into Cursor)

> **Business name:** `<FILL IN>`
> **Business website:** `<FILL IN>`
> **Owner name (optional):** `<FILL IN>`
> **Owner/transfer phone (optional, E.164 e.g. +16262784934):** `<FILL IN>`

You are scaffolding a new AI voice receptionist for the business above, deployed on GHL Voice AI. Replace the current contents of `config/agent.md`, `config/knowledge-base.md`, and `config/actions.md` with versions tailored to this business. Do **not** modify `project.md`, `README.md`, or `generate_simulation_prompt.py`. Do not run `generate_simulation_prompt.py` or touch `simulation-prompt.md` until **Step 5** — the script is only for the final assembly step.

Use the Humble Bike Rentals config on `main` as the structural and tonal reference (branch from `main` so it remains in the tree). Only the subject matter should change — section order, delimiters, rule style, and phone-call brevity must match.

### Step 1 — Gather context from the website

Fetch the business website. Also fetch obvious sub-pages when linked: services, pricing, about, contact, hours, FAQ, policies, booking. Extract:

- Business name, tagline / one-line description, phone, email, full address, website
- Hours of operation (including any holiday note)
- Full list of services / products, with prices when publicly listed
- Policies (deposit, cancellation, no-show, late, damage, group, refund, etc.)
- Location & logistics (parking, transit, nearby landmarks, accessibility)
- Candidate FAQs — things the site clearly explains and a caller would plausibly ask
- Tone / personality cues (casual, luxury, clinical, laid-back, high-end, etc.)

If a piece of information is missing from the site, mark it `TBD: <what's missing>` in the knowledge base — **never invent it**.

### Step 2 — Write `config/knowledge-base.md`

Follow this structure (adapted from the Humble Bike Rentals file):

- Opening `---`, then `<BUSINESS NAME> — Knowledge Base`
- `**BUSINESS OVERVIEW**` — name, tagline, phone, email, address, website
- `**Hours:**` — list open days / times, plus holiday note
- `**SERVICES & INVENTORY**` (or `**SERVICES**` if purely service-based) — full list
- `**PRICING**` — items with public prices, one per line; use the **same pricing model the site uses** (e.g. per hour, flat per service, packages, tiers). Preserve symbols and wording from the source (`+`, "from", ranges) so the KB stays faithful — e.g. `$70+` or "from $50" stays as written; do not collapse to a single number unless the site does.
- `**IN-STORE / ON-VISIT PRICING ONLY**` — items without public pricing (only if applicable)
- `**WHAT TO BRING**` — only if relevant (rentals, medical, appointments requiring docs, etc.)
- `**POLICIES**` — grouped subsections with plain-language bullet points
- `**LOCATION & LOGISTICS**` — parking, transit, landmarks, neighborhood
- `**FREQUENTLY ASKED QUESTIONS**` — 8–15 Q&As drawn from the site and common-sense caller questions; short, conversational answers (2 sentences max each)
- Any domain-specific section the business clearly needs (e.g. `POPULAR ROUTES` for a bike shop, `AFTER-CARE` for a nail salon, `ACCEPTED INSURANCE` for a medical office)
- Closing `---`

Formatting rules:

- Plain markdown, wrapped in leading/trailing `---` lines (matches current file)
- No YAML frontmatter
- Phone numbers written in human format (e.g. `818-551-9511`), matching what a caller would hear
- Never invent details; use `TBD: <what>` markers for gaps

### Step 3 — Write `config/agent.md`

Match the section order and structure of the current Humble Bike Rentals `agent.md` exactly:

1. `**AGENT ROLE & OBJECTIVE:**`
   - `Introduction:` line with a persona that fits the business type. Examples: bike shop → laid-back, beach-town; nail salon → warm, polished, attentive; dental office → reassuring and precise; law office → professional and calm. Speak as the business, not a named person.
   - `Your Goal:` identical in shape to the Humble file.
2. `**HANDLING CALLER QUERIES: LOGIC & RULES**` — the 3-rule block:
   1. Answer from KB, 1–2 sentences max, no unsolicited extras.
   2. If it matches a tool trigger, fire the tool immediately.
   3. If it's not in the KB, split into (a) off-topic → warm redirect, no transfer; (b) legitimate business question → Call Transfer.
   Adapt the example redirect line to this business.
3. `**GENERAL RULES:**` — use Humble's rule list as the baseline and adapt. These rules are effectively universal and should be preserved unless the business clearly breaks them:
   - Never ask for further query details; never repeat sentences verbatim.
   - Only use information in this prompt or tool instructions; no inference/guessing.
   - Address rule: always state the **full** address in a clear, spoken format (spell out `CA` as "California", etc.), then offer to repeat it once. Make sure any dashes/unit numbers read cleanly over voice.
   - Tone cues specific to this business (2–4 natural phrases that fit the brand).
   - Never mention competitors, other providers, or external booking platforms.
   - Do not use or invent a personal name; greet and speak as the business.
   - Never say "give us a call" / "call us" — they're already on the line. When referencing the phone number for future use, say "you can reach us at <number>".
   - Never offer callbacks or team follow-up unless the Call Transfer action is being triggered.
   - **Pricing (all models):** Only state prices exactly as they appear in the knowledge base — same numbers, units, and qualifiers (`+`, "from", "starting at", ranges, hourly vs flat). Never round, estimate, or invent a ceiling (e.g. if the KB says `$70+`, say it starts at seventy dollars and can go up with add-ons — do not imply a fixed total). For hourly or per-unit pricing, multiply only when the math is fully defined in the KB; if duration or options are unclear, give the per-unit price and offer transfer or booking for an exact quote. Compute multi-item totals only when every line item has a definite KB price.
   - For items listed under in-store-pricing-only, do NOT list them one-by-one — mention once at the end that a few other items have pricing available when the caller visits.
   - When asked "what do you offer?", list the **full** inventory / service menu — no omissions.
   - Parking, transit, how-to-get-here, what-to-bring — these are BUSINESS questions. Check the KB before treating as off-topic.
   - If the KB has no description for an item, don't invent one — just state its name and price.
   - Don't end every response with filler ("let me know if you need anything", "feel free to ask"). Answer and stop.
   - If the caller misnames the business or seems confused about who they reached, don't correct — just answer normally.
4. `**STRUCTURED CALL FLOW SCRIPT:**`
   - **Step 1 — Handle the Caller's Query:** note that the greeting is handled automatically by GHL; once the caller speaks, answer from the KB or trigger a tool, following rule 3 for gaps.
   - **Step 2 — Call Conclusion:** one warm sign-off line using the business name.

Wrap the file in leading/trailing `---` lines to match the current agent.md.

### Step 4 — Write `config/actions.md`

Always include these two actions (adapt the details to the new business):

1. **Action 1 — Call Transfer**
   - Action Name: `Bot can't answer a question`
   - Type: `Call Transfer`
   - Transfer To: owner phone if provided; otherwise the business main phone in E.164 format (e.g. `+18185519511`); if neither is available, use `TBD: <owner phone>`.
   - Trigger Condition: legitimate business question not in KB, complaint / human-judgment issue, or explicit request to speak with a person. Do NOT trigger for off-topic questions.
   - What to say before transferring: one short line that names the owner if provided (otherwise "our team").
   - Whisper message on transfer: `No`.

2. **Action 2 — Send Booking Link**
   - Action Name: `Send Booking Link`
   - Type: `Send SMS`
   - Message Content: include the business's booking URL if there is one, else the root website URL.
   - Trigger Condition: when the caller wants to book / schedule / reserve.
   - What to say before sending SMS: one short line letting them know it's on the way.

If the business clearly doesn't support appointments or online booking (e.g. a walk-in-only takeout counter), omit Action 2 and add a one-line comment at the bottom of the file explaining why.

Wrap in leading/trailing `---` lines to match the current actions.md.

### Step 5 — Run the generator script & report back

**Only after** `config/agent.md`, `config/knowledge-base.md`, and `config/actions.md` are complete:

- From the repo root, run: `python3 generate_simulation_prompt.py`  
  That script assembles `simulation-prompt.md` from the three config files. Do not hand-edit `simulation-prompt.md`.
- List every `TBD:` marker you introduced so the user can fill them in (group by file).
- Flag any rules in `agent.md` you were unsure about and why.
- Suggest 1–3 business-specific rules that probably belong in `agent.md` but aren't obvious from the website (e.g. a nail salon should probably have a rule for how to handle pricing questions about "sets" vs. "fills", a dental office should have a rule for not giving medical advice).

### Quality bar

- Match the voice and structure of the Humble Bike Rentals config. Only the subject matter changes.
- Answers are phone-call short (1–2 sentences). No walls of text.
- Every price stated in live answers must match the knowledge base — same amounts, qualifiers (`+`, "from", ranges), and units (hourly vs flat). No invented caps or "about" pricing.
- No placeholder strings like `[insert here]` or `<name>` — use explicit `TBD: <what>` markers so they're easy to grep for.
- The persona and tone cues in `agent.md` must feel like a real human at this specific business, not a generic receptionist.
