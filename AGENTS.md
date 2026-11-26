# Working with EzyPlatform Core

- On a fresh clone, run `./scripts/up.sh` to start Admin/Web/MySQL; it syncs the pinned Docker source and CLI. Then run `python3 scripts/sync-upstream.py` to fetch all pinned plugins and skills (including the AgentKit `engineer` and `marketing` kits when `AGENTKIT_API_KEY` is set or `ak` is logged in). Sync operations in the same checkout are serialized if run concurrently. The stack CLIs are `./scripts/ezy` and `./scripts/ak`.
- Start with `.agents/skills/ezy-guide/SKILL.md` for EzyPlatform tasks and `.agents/skills/ak-agentkit/SKILL.md` (or `ak-help`) for AgentKit skills (`ak-*`). Use `ezy-new` and `ezy-sync` for content projects; use `ezy-develop` and `ezyplatform-develop` for themes and plugins. Official skills use the `ezyplatform-` prefix; workflows can change, so read `SKILL.md` before running its scripts.
- Read the [EzyPlatform background and blog index](docs/research/ezyplatform-blogs/README.md), then open the relevant topic notes and original articles before proposing operations, deployments, or features. Verify the steps against the skills, the Guide, and the current stack version.
- Consult the [full Ezy skill catalog](skills/README.md) and read the tracked copies in [`skills/upstream/`](skills/upstream/) to choose the right skill. For a new Java plugin, follow the [stack's plugin build skill](skills/ezy-build-plugin/SKILL.md) to build natively and verify the artifact on Docker dev.
- Keep new apps in separate repositories. Use `ezy new --mode live --admin-url URL` to connect to an existing core, or `--mode local` for an isolated sandbox. Use least privilege, do not commit `.env` or `environment.json`, and do not write to production without permission.
- Do not hand-edit generated files under `.upstream/`, `.agents/skills/`, or `skills/upstream/`. Update pins as described in the README and verify Admin/Web in dev. Run `python3 scripts/sync-upstream.py --refresh-ezy-skills` to update the tracked Ezy snapshot.

## AgentKit workflow (for Bots and Devin sessions)

Follow the [model routing rule](docs/model-routing.md) for every Bot and Devin session.

See the [AgentKit workflow](docs/agentkit-workflow.md) for details. These rules are mandatory for all sessions:

- **Proportionality gate and iron rule:** Before any multi-step task, agree on four items: *Outcome, Constraints, Non-goals, Acceptance criteria*. Do not fix a bug before proving its root cause (`ak-debug` before `ak-fix`; stop and report after three unsuccessful fix attempts). Do not declare work done without real execution evidence on the final revision; do not weaken tests.
- **LOCAL / DEV only by default:** Production, deleting a database or volumes (`docker compose down -v`), editing real `.env` files or secrets, or publishing publicly requires separate approval from `chanht_tt`. Only one writer per branch/repository at a time; redact all tokens and secrets in logs, reports, and chat.
- **Choose the actual skill sequence (AgentKit 3.2.0):**
  - Quick task (`trivial`, `low` risk): `ak-scout` (if needed) → `ak-cook --fast --skip-journal` → `ak-test` → `ak-code-review --pending`.
  - Large or multi-phase task (`epic`): `ak-brainstorm` → `ak-plan --hard` (`validate`/`red-team` for high risk) → split into tickets with non-overlapping files through Chief of Staff and Devin Boards → use the EzyPlatform domain skill and `ak-cook` in each phase → `ak-test` → `ak-security` (when touching auth, APIs, DB, or input) → `ak-code-review`.
  - Bug or CI fix: `ak-scout` → `ak-debug` → `ak-fix` (red-to-green reproduction test) → `ak-test` → `ak-security` (for security bugs) → `ak-code-review --pending`.
  - PR review: `ak-review-pr <PR>` (read-only by default; do not use `--fix`, `--reply`, or `--merge` unless assigned) or `ak-code-review --pending`; add `ak-security` when touching auth, payments, input, or secrets. Classify findings as `Blocker / Should fix / Suggestion` and include `file:line`.
- **Differences in Devin's `portable` distribution:** Use `ak-security` (not the old `ak-security-scan` name). Coordinate multiple sessions through **Chief of Staff and Devin Boards** (not Claude Code's `ak-team`/`ak-orchestrate`; use `ak-worktree` only for separate branches in one VM). There is no `kongming` subagent (`--advice`); use `ak-brainstorm`, `ak-predict`, or `ak-plan red-team` to challenge a plan.
- **Final report:** Always include `Status` (`DONE` | `DONE_WITH_CONCERNS` | `BLOCKED`), PR/artifact links, real execution evidence, and anything unverified or outstanding.
