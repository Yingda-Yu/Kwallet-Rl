# AGENTS.md merge-conflict resolution proposal (PR #2)

Date: 2026-09-16. **PROPOSAL ONLY — no merge, rebase, or force-push performed.**
PR #2 is `mergeable_state=dirty`: the branch is ahead 14 / behind 2, and the
only textual conflict is `AGENTS.md` (add/add). `TRAE_MASTER_PLAN.md` exists
identically on both sides and does not conflict.

## Sides
- `origin/main` (commits 435e05a, a008658): 148-line "K-Wallet RL — autonomous
  agent instructions" anchored to TRAE_MASTER_PLAN.md (kept as the base).
- `work/icassp2027-reproduce-improve`: 35-line session brief with several
  safety/communication rules.

## Proposed resolution
Take the **main 148-line version verbatim as the base** and append one new
section containing only the work-branch rules that main does not already
cover. Duplicates of main rules (reuse-before-adding packages, validation-only
model selection, keep failed seeds, run manifests, never substitute old-paper
numbers, row-to-CSV traceability, official template usage) are intentionally
NOT appended. Result: 179 lines, pure addition (no deletion of main text).

The only incidental normalization is adding a trailing newline after main's
last line before the appended heading.

## Proposed unified diff (against origin/main:AGENTS.md)

```diff
--- /tmp/agents_merge/main_AGENTS.md	2026-09-16 18:57:35.834314734 +0800
+++ /tmp/agents_merge/proposed_AGENTS.md	2026-09-16 19:06:58.120354548 +0800
@@ -146,4 +146,34 @@
 
 ## Definition of done
 
-The project is done only when all three user-requested stages are complete: (1) old-paper code and experiments are reproducible, (2) the stronger method and expanded experiments are implemented and evaluated with ablations/statistics, and (3) a new TeX Live-compiled paper is built from those verified results, with a clean reproduction command documented for another machine.
\ No newline at end of file
+The project is done only when all three user-requested stages are complete: (1) old-paper code and experiments are reproducible, (2) the stronger method and expanded experiments are implemented and evaluated with ablations/statistics, and (3) a new TeX Live-compiled paper is built from those verified results, with a clean reproduction command documented for another machine.
+## Session operating rules carried from the ICASSP work branch
+
+These rules originate from the ICASSP-2027 reproduction work branch and are
+appended to the master-plan instructions above; they do not replace them.
+
+- Preserve user changes, the original paper PDF, the template archive, frozen
+  benchmarks and historical results. Never use force-push, hard-reset, or
+  working-tree clean to resolve an ordinary conflict; resolve conflicts in a
+  dedicated, reviewed step.
+- Automatic approval is not authorization for credential disclosure, paid
+  resources, destructive operations, manuscript submission, author-registration
+  payment, or copyright signing.
+- Never infer authorship, ORCID, funding, ethics approvals, or a prior
+  submission's status. Missing author metadata blocks submission readiness
+  only; it must not block unrelated engineering.
+- An idle-looking GPU is not permission to use it: honor scheduler allocations
+  and project-specific user authorization. Without a confirmed allocation,
+  continue lightweight CPU work and report the resource blocker; never reset a
+  GPU or terminate another user's process.
+- Use isolated user-level dependencies and the installed TeX Live; do not
+  alter shared drivers, system Python, or global environments without explicit
+  authorization.
+- Parameters absent from the prior manuscript remain missing; a documented
+  re-implementation is acceptable but is not an exact reproduction.
+- Resume from real on-disk state and logs at the start of every agent session;
+  do not launch duplicate experiments.
+- Validate every PDF page by rendering and visual inspection in addition to
+  compilation checks.
+- Communicate progress to the user in Chinese and write the manuscript in
+  English; verify that a remote push actually succeeded before reporting it.
```

## Execution plan (requires explicit author approval; not done yet)
1. On a temporary integration branch (or directly on the work branch in a
   dedicated commit), run `git merge origin/main`; the sole conflict will be
   AGENTS.md.
2. Resolve AGENTS.md exactly as the diff above (main base + appended section).
3. Verify `git diff origin/main...HEAD -- AGENTS.md` equals this proposal;
   confirm paper/ and results/ are untouched by the merge.
4. Build the paper and run pytest once more, then push the merge commit to the
   same work branch (ordinary merge commit; never force-push/reset).
5. Re-check PR #2 becomes mergeable; keep it draft; do not merge into main.
