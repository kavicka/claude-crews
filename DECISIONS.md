# Design decisions

Why claude-crews is built the way it is, what backs each choice, and what would change it. **Evidence** names only what exists in this repository; where there is none, it says so.

## 1. Teams of role agents instead of one long prompt

- **Decision:** each role (planner, skeptic, coder, tester, reviewer) is its own subagent with its own context, and the main session only orchestrates.
- **Why:** an agent that reviews code it didn't write, without the author's reasoning in its context, reads the diff the way a colleague would. A plan written down before the code is something the user can check.
- **Evidence:** mixed. In the [coupon benchmark](examples/coupon-demo) (5 runs per variant) the crew passed 10.2 of 12 hidden tests on average, one prompt at `xhigh` 10.6, one prompt at `medium` 10.0. The crew wrote more tests (21 against 14) and always listed the decisions it took without the user, but it was not more correct on that small task.
- **Cost:** about $1.46 and 7 minutes per crew run, against $0.25 and 1 minute for one prompt at `xhigh`, on the coupon task.
- **Would change it:** the crew is only worth its cost if it wins on tasks with real open questions and more files. That is not measured yet; the [bakery example](examples/bakery) shows what the process looks like on such a task, but it is one run.

## 2. A skeptic attacks the plan before any code

- **Decision:** `crew:skeptic` reviews the plan, not the code, and every objection needs `file:line` or a quote.
- **Why:** a wrong plan is cheapest to fix before it is code. The evidence rule keeps the skeptic from inventing objections to look useful.
- **Evidence:** in the [original run](examples/coupon-demo/crew-run/2-skeptic.md) the skeptic found that typecheck wasn't in the done criteria, and that two coupons can make a cart free. In the benchmark it cut both ways: in two of five runs the skeptic held the plan to "a single string must keep working", which blocked rounding and the zero cap and cost three hidden tests each. Both runs flagged it as a decision for the user, but in unattended mode nobody answered.
- **Would change it:** transcripts showing the skeptic's objections are rarely folded in, or mostly restate the planner's open questions.

## 3. One human checkpoint

- **Decision:** `/crew:ship` stops exactly once, after the plan and the skeptic's verdict.
- **Why:** product decisions ("compound or add coupons?") belong to the user, and asking them once, early, is cheaper than after the code. More stops would make the crew unusable for anything but small tasks.
- **Evidence:** none measured. In the benchmark the checkpoint is answered by a fixed operator note, so the benchmark can't show its value.

## 4. Model and effort per role

- **Decision:** Opus at `xhigh` for the planner, skeptic, reviewer and moderator; Opus at `high` for coders; Sonnet for the tester, research and council members; Haiku for lookups.
- **Why:** judgement-heavy roles that gate everything else get the most reasoning; well-specified work gets cheaper models.
- **Evidence:** weak. The tiers are a hypothesis and have not been ablated role by role. The benchmark compares one agent at `medium` and `xhigh`: at `medium`, 4 of 5 runs made the price depend on the order of the coupon codes, at `xhigh` none did, for about $0.03 more per run. That says effort matters, not which role needs it.
- **Next test:** the crew with the skeptic and reviewer on `high`, and on Sonnet, five runs each.

## 5. The council debates in rounds and votes

- **Decision:** five members answer independently, rebut each other by name in round 2, vote with a confidence; a moderator checks the evidence and passes the motion only when both the simple and the confidence-weighted YES share reach 60 %.
- **Why:** forcing independent positions before anyone sees the others avoids anchoring on the first answer, and the moderator's evidence check is where wrong numbers get caught.
- **Evidence:** one run, [council-demo](examples/council-demo). Its main value came from the moderator's check: it rejected five wrong or unsupported numbers, including the skeptic's own headline figure.
- **Known weaknesses:** the members are the same model with different instructions, so they are not independent voters; their confidence numbers are not calibrated; the 60 % threshold is a convention, not a measured optimum.
- **Next test:** the same questions answered by one agent listing pros and cons plus one verifier, against the full council, judged blind.

## 6. Safety is enforced by tool lists, not by prompts (1.1.0)

- **Decision:** read-only agents get a `tools:` allowlist without Write, Edit or Bash. Office and council agents get an explicit list with no MCP tools.
- **Before:** 1.0.0 used `disallowedTools: Write, Edit, …` and prompt rules such as "never send". That left Bash open to the "read-only" agents, and every connected MCP tool, including sending email, open to agents that read untrusted web pages. A review of the repository found it.
- **Why tool lists:** a prompt rule can be talked around by a web page's injected text; a missing tool can't. Subagent `hooks` and per-command Bash rules aren't available to plugin agents, so the allowlist is the strongest control a plugin has.
- **Trade-offs:** the reviewer no longer runs checks itself (the main session hands it a diff file, the tester runs checks), and office agents need the main session to call connected services for them.

## 7. Agents answer from a plain-file knowledge base

- **Decision:** `~/knowledge/` is Markdown files (profile, pricing, past quotes, voice samples), not a database or embeddings.
- **Why:** the user can read and fix it, it can live in git, and agents can cite a file path for every claim.
- **Would change it:** once it grows past what an agent can grep in a few calls.

## 8. Benchmarks are scripted and keep raw evidence

- **Decision:** results come from [bench/run.py](examples/coupon-demo/bench/run.py): fresh repo per run, real `git diff`, transcript, scripted scoring, hidden tests copied in last.
- **Before:** the original demo saved diffs through a compacting diff tool. They were not valid patches and one was truncated, so the published result couldn't be reproduced ([original-run](examples/coupon-demo/original-run)).

## 9. One general coder next to the TypeScript specialists

- **Decision:** `web-coder` and `ui-builder` stay specialists for TypeScript web and visual UI; `coder` (1.1.0) covers every other stack, Java and Kotlin included.
- **Why:** most work in the author's projects is TypeScript web, where a specialist pays off. Other stacks are too varied for one specialist each, so a general coder that reads the project's conventions handles them.
