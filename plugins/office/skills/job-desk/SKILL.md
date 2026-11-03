---
name: job-desk
description: Job desk. Runs the job scout over the user's job links (or a fresh search on the boards in their profile), has the council debate the borderline offers, and returns only the offers worth applying to, with an angle and an offer to draft the reply. Use when the user asks which jobs to apply for, shares several job links, or invokes /office:job-desk.
---

# Job desk

Input: job URLs, or "search" to look for new offers: $ARGUMENTS

1. **Collect.** URLs from the user, or for "search" one `office:job-scout` that searches the boards in the profile's Job search section.
2. **Scout.** `office:job-scout` over all offers (one agent per 8 offers, in parallel).
3. **Debate MAYBE offers** (when the council plugin is installed). For each MAYBE (at most 3), run `/council:vote` with the question "Should the user apply to <title> at <company>?" and the scout's notes as context, in short mode.
4. **Hand back** a table: offer, verdict, fit, angle, link. APPLY first.
5. Offer `/office:outreach` for the APPLY offers. Nothing is sent.

Log the run to `~/knowledge/jobs/<YYYY-MM-DD>-desk.md` with each agent's verdict.
