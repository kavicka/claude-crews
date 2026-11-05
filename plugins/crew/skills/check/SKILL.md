---
name: check
description: Verifies the current uncommitted changes, or a branch or PR, with the crew. The tester extends and runs the tests, the reviewer reviews, and the result is a go/no-go. Use when the user asks to check, verify or review changes before committing, or invokes /crew:check.
---

# Check changes with the crew

Scope: $ARGUMENTS. If no scope is given, check the uncommitted changes in the current repo.

1. **Determine the scope.**
   - Uncommitted work: `git status`, `git diff --stat` and `git diff --staged --stat`.
   - A branch: `git diff <base>...HEAD --stat`.
   - A PR: `gh pr diff <n>`.
   - If there is nothing to check, say so and stop.
   - Save the full diff inside the repo's git directory, where it is never committed: `git diff HEAD > "$(git rev-parse --git-dir)/crew-review.diff"` (or the branch or PR diff). List new untracked files with `git ls-files --others --exclude-standard`: a diff doesn't contain them. The reviewer has no shell and works from these.
2. **Run the tester and the reviewer in parallel.** Both briefs must be self-contained: the repo path, the scope and what the change is meant to do (from the user, the commit messages or the diff).
   - `crew:tester`: add the missing tests for the change, run the suites, and run typecheck/lint or `mvn verify`.
   - `crew:reviewer`: review the production diff, with the diff file path, the list of changed files and the new untracked files. It reports the checks it couldn't see as **Not verified**; merge them with the tester's results in the report.
3. **Report** to the user in their language:
   - **GO / NO-GO**
   - 🔴 blockers and 🟠 should-fix items, with `file:line`
   - the test table from the tester, with the tests it added
   - a suggested commit message, matching the `git log` style
4. Don't fix anything unless the user asks. If they do, route each fix to the right coder (`crew:web-coder`, `crew:ui-builder`, or `crew:coder` for any other stack), then re-run this check on the fixes only.
