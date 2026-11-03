---
name: quote
description: Produces a price quote with the office crew. Researches the client, builds the quote from ~/knowledge/pricing, has the pricing analyst and the council skeptic challenge it, and hands back the quote and open questions. Use when the user asks for a quote, offer, estimate or "how much should I charge" for a project, or invokes /office:quote.
---

# Quote with the office crew

You, the main session, orchestrate. **Subagents don't see this conversation**, so every brief is self-contained: client, URL, the brief in the user's words, files to read, and what to return.

Brief: $ARGUMENTS

## 0. Triage

- `~/knowledge/pricing/README.md` missing or still a template → run the `/office:setup` interview for pricing first.
- Missing facts that move the price by more than 20 % (pages, languages, integrations, design included, content delivery, deadline) → ask the user in one round first.
- Known client with a profile in `~/knowledge/clients/` younger than 30 days → skip research.

## 1. Research (`office:researcher`, purpose "quote")

Only when there is a company or URL. Brief it with the company, URL and what the project is.

## 2. Build (`office:quote-builder`)

Brief it with the user's brief verbatim, the client profile path, the answers to the triage questions and the output language.

## 3. Challenge, in parallel

- `office:pricing-analyst`: the quote file path and the client profile path.
- `council:skeptic` (when the council plugin is installed): "Attack this quote as the client's procurement person and as the user three weeks into the project. Where is the scope vague, where will the client push back, what will cost more hours than quoted?" plus the quote path.

## 4. Fix (one loop)

Send the 🔴 and 🟠 findings from both back to `office:quote-builder`. One loop only; leftovers go to the user.

## 5. Hand back

- Totals (fixed and hourly), payment split, timeline.
- The analyst's verdict and the skeptic's top objection, one line each.
- Open questions and assumptions.
- File path; offer to render the PDF.

Nothing is sent to the client. The user sends it.
