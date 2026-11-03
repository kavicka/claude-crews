---
name: lead-desk
description: Lead desk. Finds up to 5 scored client leads, profiles the best ones, drafts outreach for them, has a skeptic and a simulated recipient test each draft, logs the whole discussion and reports only the result. Run on demand with /office:lead-desk, or weekly from a scheduled task. Never sends anything.
---

# Lead desk

Focus for this run (optional niche or city): $ARGUMENTS

This desk can run unattended. Keep a running log of every agent's verdict; it becomes the transcript.

1. **Scout.** `office:lead-scout`: "Find up to 5 leads scored ≥ 14/20. Focus: <focus, or 'rotate niches: check ~/knowledge/leads for the niche used last time and pick another from the profile'>."
2. **Pick.** The top 3 leads by score.
3. **Profile, in parallel.** `office:researcher` per lead, purpose "outreach".
4. **Draft, in parallel.** `office:outreach-writer` per lead with its profile path. Channel: the contact route the scout found.
5. **Challenge, in parallel per draft** (when the council plugin is installed):
   - `council:skeptic`: "Is the claimed pain real and proven? Would this message embarrass the user?"
   - `council:client`: "Would you answer this?"
   Drop a lead when both say no; otherwise one revision by the outreach-writer.
6. **Log.** Write `~/knowledge/leads/<YYYY-MM-DD>-desk.md`: the lead table, each draft, and a transcript section with every agent's verdict in order (`🔎 lead-scout: …`, `🔴 skeptic: …`, `👤 client: …`, `✍️ outreach-writer: …`).
7. **Report**, at most 3 lines: "Lead desk: N drafts ready in ~/knowledge/leads/<file>. Best: <company> (<pain>)." If nothing passed, say so in one line.

Rules: no emails sent, no email drafts, no forms, no contact with anyone. Public sources only.

To run it weekly in the Claude desktop app, create a scheduled task whose prompt is "Run /office:lead-desk".
