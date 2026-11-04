---
name: setup
description: Sets up the ~/knowledge base the office and council agents answer from. Copies the templates, then interviews the user to fill in their profile, pricing and voice, and optionally installs the model-routing rules into ~/.claude. Use on first install, when an agent reports a missing or template knowledge file, or when the user invokes /office:setup.
---

# Set up the knowledge base

The templates live in `../../templates/knowledge/` relative to this skill's base directory, and the routing rules in `../../templates/model-routing.md`.

## 1. Copy the templates

- If `~/knowledge/` doesn't exist, copy the whole template folder there.
- If it exists, copy only the files that are missing. Never overwrite an existing file; list what you skipped.

## 2. Interview (one round per file, AskUserQuestion or plain questions, skip what the user doesn't want to fill now)

1. **`profile.md`:** name, what they do in one line, services, stack or skills, 3–5 proof projects with one number each, ideal clients (niches, regions, company size), hard rules (things never to claim or mention), outreach rules (how they may contact people they haven't worked with, in the countries they sell to; say it isn't legal advice), design preferences (optional), languages, and the Job search section if they look for jobs.
2. **`pricing/README.md`:** currency, hourly rate, fixed-price policy, payment terms, revision rounds, quote validity, 3–10 add-ons with prices. Offer to import past quotes: the user points to files, you copy them into `pricing/quotes/` after removing client personal data they don't want stored.
3. **`voice/README.md`:** default language and formality, greeting, sign-off, signature, words they never use. Ask for 1–3 real messages they sent that worked, and save them to `voice/samples/`.

Write the answers into the files, replacing the placeholders. Leave a placeholder in place when the user skips a question.

## 3. Model routing (optional)

Ask whether to install the routing rules. On yes:
- copy `templates/model-routing.md` to `~/.claude/model-routing.md` (ask before overwriting an existing one),
- add the line `@model-routing.md` to `~/.claude/CLAUDE.md` if it isn't there.

## 4. Hand back

The files created or changed, the placeholders still open, and the 3 commands to try first: `/office:quote`, `/council:vote`, `/crew:ship`.

Never store passwords, API keys, bank details or other people's private data in the knowledge base.
