# Model and effort routing for subagents

This is the user's standing instruction for choosing `model` and `effort` on every subagent: Agent tool calls, `agent()` calls in workflows, and agent definition frontmatter. Pass both parameters explicitly on ad-hoc Agent calls according to the table below.

Effort levels: low < medium < high < xhigh < max. Coding and long agentic work gain the most from higher effort; chat, lookups and classification don't. Check current model prices at https://www.anthropic.com/pricing before changing tiers.

| Tier | Model · effort | Use for | Agents with this tier set |
|---|---|---|---|
| **Critical** | opus · xhigh | Security review, final code review, challenging a plan, architecture decisions, final verdicts | crew:planner, crew:skeptic, crew:reviewer, council:skeptic, council:moderator |
| **Build** | opus · high | Writing or changing production code, money decisions (quotes) | crew:web-coder, crew:coder, crew:ui-builder, office:quote-builder |
| **Craft** | opus · medium | Writing in the user's voice | office:outreach-writer, office:copywriter |
| **Analyst** | sonnet · medium (high for tests) | Research, scoring, debate, docs, data analysis, writing tests | crew:tester (high), crew:docs-writer, office:researcher, office:pricing-analyst, office:job-scout, office:lead-scout, office:librarian, council:optimist, council:engineer, council:business, council:client |
| **Fast** | haiku · low (medium when it must judge) | Code and file search, grep across repos, link and sitemap checks, screenshots, extracting fields, formatting, summarising one file | Explore and other lookups |
| **Escalation** | opus · max | Opus at xhigh failed twice on the same hard problem, or the user asks for maximum effort. Say so before using it | none by default |

## Ad-hoc Agent calls

- `Explore`, quick code or file lookups → `haiku`, `low`.
- `general-purpose` web or doc research → `sonnet`, `medium`. Research that ends in a recommendation the user acts on → `sonnet`, `high`.
- `general-purpose` that writes or fixes code → `opus`, `high`.
- `Plan` → `opus`, `high`; architecture or security-sensitive plans → `opus`, `xhigh`.
- Any security work (security review, auth, payments, secrets, licence checks) → `opus`, `xhigh`, never lower.
- `claude-code-guide` → `sonnet`, `low`.
- Defined agents (crew:, office:, council:) already carry their tier; pass nothing unless this file says to override.

## Rules

1. **Escalate, don't retry.** When a haiku or sonnet result is wrong, thin or contradicts the evidence, re-run one tier up instead of repeating the same tier.
2. **Never downgrade** Critical work or anything touching money, security or production data, even to save cost.
3. **Fan-out goes cheap.** Many parallel readers (one per file, page, video or offer) run on haiku or sonnet; the step that merges their results runs one tier higher.
4. **Context beats model.** A cheaper model with a complete brief beats an expensive one with a vague brief. Fix the brief first.
5. **Main session** model is the user's choice. Suggest Opus for coding sessions and Sonnet for chat, planning and writing sessions.
6. When the user names a model or effort for a task, that wins over this file for that task.
