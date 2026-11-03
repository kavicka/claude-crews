---
name: outreach
description: Prepares outreach to a company or person with the office crew. Researches the target, drafts the message in the user's voice, has a simulated recipient read it, and returns the final draft. Covers cold client outreach, follow-ups, job-ad replies and LinkedIn messages. Never sends. Use when the user wants to contact, reply to or follow up with someone, or invokes /office:outreach.
---

# Outreach with the office crew

You, the main session, orchestrate. Subagents don't see this conversation: brief them fully.

Target and goal: $ARGUMENTS

## 0. Triage

- **Job ad** → `office:job-scout` first. On DROP, stop and tell the user which filter failed.
- **Company or person without a fresh profile** in `~/knowledge/clients/` → `office:researcher` with purpose "outreach".
- Unclear channel (email, LinkedIn, contact form) or goal (meeting, audit, quote) → ask the user once.

## 1. Draft (`office:outreach-writer`)

Brief: recipient, channel, goal, language, the profile path, and for job replies the ad URL or text.

## 2. Recipient test (`council:client`, when the council plugin is installed)

Brief: "You are <recipient role> at <company>. You get 40 messages like this a week. Would you answer this one? What makes you stop reading?" plus the draft path. One revision by the outreach-writer if the verdict is no.

## 3. Hand back

- The final draft in full, ready to copy.
- One line on the angle and the recipient-test verdict.
- File path.
- An email draft only if the user asked for one in this conversation, with the recipient they confirmed. Never send.
- For job applications: log the entry in `~/knowledge/jobs/applied.md` and say so.
