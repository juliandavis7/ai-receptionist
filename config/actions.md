---
# Actions
Triggerable actions available to the Voice AI agent during a call.

---

## Action 1 — Call Transfer

- **Action Name:** Bot can't answer a question
- **Type:** Call Transfer
- **Transfer To:** +16262784934
- **Trigger Condition:** When the caller has a legitimate business-related question that cannot be answered from the knowledge base, has a complaint or issue requiring human judgment, or explicitly asks to speak with a person. Do NOT trigger for general or off-topic questions unrelated to the business.
- **What to say before transferring:** "I'll transfer you to Karl — he's the owner and can help with this. Please hold for a moment."
- **Whisper message on transfer:** No

---

## Action 2 — Send Booking Link

- **Action Name:** Send Booking Link
- **Type:** Send SMS
- **Message Content:** "You can book an appointment yourself here: https://humblebikerentals.com/"
- **Trigger Condition:** When the user wants to book a slot for a bike rental
- **What to say before sending SMS:** "I'm going to send you an SMS right now. Feel free to book directly on our site."
---
