# Original run (2026-11-03): recovered code

The first version of this demo shipped its two diffs as `vibe.diff` and `crew.diff`. They were not patches: they were the compact output of a diff summariser (indented hunks, no file headers, context lines dropped), and the crew one was cut off after 100 lines. `git apply` refused both, so the "run it yourself" steps did not work. They are kept unchanged in [raw/](raw/) as the record of what was published.

This folder holds what could be recovered from them.

| File | What | Status |
|---|---|---|
| [vibe/checkout.ts](vibe/checkout.ts), [vibe/checkout.test.ts](vibe/checkout.test.ts) | the vibe run's code and tests | complete |
| [vibe.patch](vibe.patch) | real `git diff` against [../base](../base) | applies with `git apply` |
| [crew/checkout.ts](crew/checkout.ts) | the crew run's production code | complete (its hunk was before the cut) |
| [crew.patch](crew.patch) | real `git diff` of `checkout.ts` against the base | applies with `git apply` |
| crew `checkout.test.ts` | the crew's 19 new tests | **lost**: only the first ~100 of 168 added lines survive in [raw/crew.compact.txt](raw/crew.compact.txt) |
| [vibe.score.json](vibe.score.json), [crew.score.json](crew.score.json) | the recovered code scored by [../bench/score.py](../bench/score.py) | |

## What the recovered code confirms

- **Hidden tests:** vibe 11 / 12 (fails C1, duplicates), crew 12 / 12. Both typecheck.
- **Vibe tests:** 11, as originally reported. The crew's reported 23 tests can't be checked, because the test file is lost.
- **Order bug in the vibe code:** with WELCOME10 and SUMMER15 both valid, 822 of 2 786 sampled carts (5.00 to 200.00) get a total that depends on the order of the codes, by 1 cent. The original report's example (1035 vs 1036 cents on a 4405-cent cart) is one of them. The crew code has none.

The recovery was a one-off: lines were re-indented, file headers added, and the hunks applied with fuzz, then the result checked by running it. Treat this run as an anecdote. The repeated runs in [../bench](../bench) are the evidence.
