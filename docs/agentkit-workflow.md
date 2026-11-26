# AgentKit workflow for bots and Devin sessions

This document summarizes a hands-on review of **AgentKit 3.2.0** (the `engineer` and `marketing` kits, exported in `portable` format) as integrated into `ezyplatform-stack`. It sets out how **`chanht_tt`**, the **bots** (`Chief of Staff` and `Upstream Watcher`), and **Devin sessions** work together on EzyPlatform projects.

---

## 1. AgentKit kits installed in the stack

After running `python3 scripts/sync-upstream.py` with `AGENTKIT_API_KEY` set or after logging in with `./scripts/ak login`, `.agents/skills/` contains **167 skills**:

| Group | Count | Prefix | Main role |
|---|---:|---|---|
| **AgentKit Shared** (`engineer` ∩ `marketing`) | 40 | `ak-*` | Core workflow: `ak-agentkit`, `ak-brainstorm`, `ak-plan`, `ak-cook`, `ak-debug`, `ak-fix`, `ak-test`, `ak-scout`, `ak-git`, `ak-docs`, `ak-journal`, `ak-handoff`, `ak-worktree`, `ak-frontend-design`, `ak-ui-ux-pro-max`, `ak-copywriting`, `ak-design`, `ak-preview`... |
| **AgentKit Engineer-only** | 65 | `ak-*` | Specialized engineering: `ak-review-pr`, `ak-code-review`, `ak-security`, `ak-ship`, `ak-scenario`, `ak-databases`, `ak-web-testing`, `ak-devops`, `ak-deploy`, `ak-github`, `ak-research`, `ak-xia`, `ak-predict`, `ak-retro`, `ak-advise`, `ak-vibe`, `ak-mcp-builder`, `ak-payment-integration`... |
| **AgentKit Marketing-only** | 43 | `ak-*` | Product discovery and go-to-market: `ak-play`, `ak-marketing-research`, `ak-competitor`, `ak-marketing-planning`, `ak-brand`, `ak-launch-strategy`, `ak-pricing-strategy`, `ak-seo`, `ak-onboarding-cro`, `ak-form-cro`, `ak-analytics`, `ak-ab-test-setup`, `ak-campaign`, `ak-email`, `ak-social`... |
| **EzyPlatform Stack** | 19 | `ezy-*`, `ezyplatform-*` | EzyPlatform workflows and tools (`ezy-guide`, `ezy-new`, `ezy-sync`, `ezy-develop`, `ezyplatform-develop`, `ezy-i18n`, `ezy-media`...) plus the local skill `skills/ezy-build-plugin/SKILL.md` |

---

## 2. Key adaptations from the reference workflow

The original workflow was written for a traditional team and does **not** always match AgentKit 3.2.0 or Devin's infrastructure. This version adapts it as follows:

1. **Use the current skill names:**
   - In 3.2.0, `ak-security-scan` is only a legacy alias. The official name is **`ak-security`**, which supports `--secrets-only`, `--deps-only`, `--red-team`, `--fix`, and `--iterations N`.
2. **Use the actual team roles, not the names from the example:**
   - **Owner (`chanht_tt`):** Approves production work, database or volume deletion, changes to `.env` or secrets, high-risk architecture, wide publication, and product decisions.
   - **Chief of Staff (coordination bot):** Manages Devin Boards, splits and assigns tickets with one writer per repository or branch, tracks progress, verifies evidence, and merges PRs in bot-owned repositories (such as `kaynt-mt/ezyplatform-stack`) after CI and Devin Review pass.
   - **Upstream Watcher (upstream monitoring bot):** Tracks new releases of EzyPlatform, CPPAI, and AgentKit.
   - **Devin sessions (Writer / Researcher / Reviewer):** Carry out tickets end to end, run actual tests, and open PRs. They do not merge unless the bot owns the repository and they have been authorized.
3. **Account for the `portable` export on Devin; avoid Claude Code-only features:**
   - **`ak-team` and `ak-orchestrate`:** Designed for Claude Code Agent Teams and headless CLI runtimes. Coordinate parallel sessions through **Chief of Staff and Devin Boards**, or **Dynamic Workflows** when there are at least five independent branches. Use **`ak-worktree`** only to isolate multiple branches on the same VM.
   - **`--advice` (calls the `kongming` subagent) and `--ultra` (wave best-of-five verification):** These are Claude Code extensions; Devin has no `kongming` subagent. When a difficult problem needs critical review, use **`ak-brainstorm`** (compare two or three options and identify the weakest assumption), **`ak-predict`** (architecture, security, performance, UX, and operations), or **`ak-plan red-team`** (four review personas).
   - **Automatic journaling:** `ak-plan`, `ak-cook`, `ak-fix`, and `ak-ship` suggest `ak-journal` by default (entries go to `plans/journals/YYYY-MM-DD-<slug>.md` via `./scripts/ak journal create`). For small or quick tasks, use `--skip-journal` or omit this step to avoid unnecessary files.
   - **Plan and report paths:** AgentKit uses `plans/<timestamp>-<slug>/` for plans (`plan.md`, `phase-NN-<name>.md`, `plans/reports/`, `plans/journals/`). Do not commit drafts or temporary reports unless they are official documentation that belongs in `docs/`.

---

## 3. Rules for all workflows

1. **LOCAL / DEV only by default:** Any work touching **production**, deleting databases or volumes (`docker compose down -v`), editing real `.env` files or secrets, or sending or publishing at scale requires **separate approval from `chanht_tt`**.
2. **One writer at a time:** Only one session may write to a branch or repository at a time; other sessions read, research, or review. Split parallel tickets along non-overlapping file boundaries.
3. **Security and backups:** Create a backup or restore point before publishing or migrating data. Never write or expose tokens, API keys, or passwords in logs, reports, PRs, or chat. If a secret leaks, redact it as `<REDACTED_...>` and request immediate rotation.
4. **Proportionality Gate (from `ak-agentkit`):** Classify the work using **three criteria** before choosing a workflow:
   - **Size:** `trivial` (one or two files, at most 30 minutes, no unknowns → proceed without a plan) · `standard` (one deliverable, a few files) · `epic` (multiple modules or phases → use `ak-plan` and split file ownership).
   - **Risk:** `low` (internal and reversible) · `elevated` (affects users or multiple modules → requires `ak-test` and review) · `high` (auth, security, payments, database migrations, public contracts, destructive actions, or wide publication → requires `ak-test`, `ak-security`, independent review or Devin Review, and approval from `chanht_tt` before any irreversible step).
   - **Collapse Rule:** Skip any intermediate step that neither produces an artifact for a later step nor contributes to the level of verification required by the risk.
5. **Iron Laws:**
   - Start every multistep task with a **Brainstorm Contract** covering four items: *Outcome, Constraints, Non-goals, and Acceptance criteria* (three or four lines for small tasks, full detail for large ones).
   - **Do not fix a bug until you demonstrate its root cause** (`ak-debug` before `ak-fix`). After three consecutive failed fixes, stop, reassess the architecture, and report to Chief of Staff or `chanht_tt`.
   - **Do not report completion without evidence from an actual run on the final revision** (test, build, HTTP/Docker output, or a hands-on check). Never weaken tests or assertions to obtain a pass.

---

## 4. Five standard workflows

### Workflow 1: Quick or simple tasks (`trivial`, `low` risk, up to about one hour, few files)

- **Skill sequence:** `ak-scout` *(if the file locations are unclear)* → `ak-cook --fast --skip-journal` → `ak-test` → `ak-code-review --pending` *(lightweight)*
- **Steps:**
  1. Write four short lines covering Outcome, Constraints, Non-goals, and Acceptance criteria.
  2. Make the smallest change that meets the scope. Preserve out-of-scope behavior.
  3. Run the narrowest test suite that covers the change. Review the diff with `ak-code-review --pending`.
  4. Open a PR and wait for CI and Devin Review to pass. Merge it yourself if the bot owns the repository.

### Workflow 2: Complex, multiphase, or large features (`epic`, `elevated`–`high` risk)

*Example: Building a `makeplane/plane`-style task management plugin on EzyPlatform.*

- **Skill sequence:** `ak-brainstorm` *(with `ak-research` or `ak-xia` when comparing a reference repository)* → `ak-plan --hard` *(plus `ak-plan validate` or `ak-plan red-team`)* → **Chief of Staff splits phases into Devin Boards tickets** → For each phase: **EzyPlatform domain skill** and `ak-cook <plan-path>` → `ak-test` → `ak-security` *(if touching auth, APIs, databases, or input)* → `ak-code-review` → PR and Devin Review → `ak-journal` *(when an architectural decision is worth recording)*
- **Steps:**
  1. Agree on Outcome, Constraints, Non-goals, and Acceptance criteria. Compare up to three options and name the weakest assumption. For high-risk architecture, use `ak-predict` or `ak-plan red-team` and seek approval from `chanht_tt` before coding.
  2. Use `ak-plan` to produce a phased plan (`plans/<ts>-<slug>/plan.md` and `phase-NN-<name>.md`). State which files and acceptance checks belong to each phase.
  3. Chief of Staff assigns each phase as an independent Devin Boards ticket. Run phases in parallel only if they do not edit the same files; use `ak-worktree` when branches need to be isolated on one VM.
  4. Each phase must pass actual tests (unit or integration tests and Admin/Web checks in the Docker development stack for EzyPlatform plugins) and Devin Review before dependent phases proceed.

### Workflow 3: Bug fixes and CI incidents (`fix-defect`)

- **Skill sequence:** `ak-scout` → `ak-debug` → `ak-fix` → `ak-test` → `ak-security` *(for security defects)* → `ak-code-review --pending`
- **Steps:**
  1. Record the symptoms, expected behavior, and reproduction steps (specific commands, logs, or requests).
  2. Use `ak-debug` to **demonstrate the root cause with logs or tests before fixing it**. Do not guess.
  3. Use `ak-fix`: add or extend a reproduction test (red to green), fix the root cause, and do not weaken tests.
  4. Use `ak-test` to check the defect and nearby regressions. For security, auth, injection, or secret issues, also use `ak-security`.
  5. Report the root cause, changes, and before/after evidence. For a recurring incident or a large set of fixes, use `ak-retro` to learn from Git history.

### Workflow 4: PR review (`review-audit`)

- **Skill sequence:** `ak-review-pr <PR>` *(for GitHub PRs)* or `ak-code-review --pending` *(for a local diff or commit)*. Add `ak-security` if the PR touches auth, payments, user input, secrets, or dependencies.
- **Steps:**
  1. Read the PR description, ticket or issue, and related plan. Fetch the diff with `gh` or Git tools.
  2. Review in priority order: correctness and contracts, bugs and regressions, security (what does the PR store, transmit, or expose?), breaking changes, testing, and maintainability.
  3. Classify feedback as **Blocker / Should fix / Suggestion**. Include `file:line`, evidence, and reasoning for each finding.
  4. Run local tests or builds for high-risk changes or changes to public contracts.
  5. Conclude with **Approve / Request changes / Comment**. Reviews are read-only by default: do **not** use `--fix`, `--reply`, or `--merge` unless explicitly assigned in the ticket or command.

### Workflow 5: Product discovery, marketing, and go-to-market (`discover-validate`, `plan-campaign`, `create-content`)

Use the 43 `marketing` skills and 40 `shared` skills when preparing a product, positioning, or launch materials:

- **Discover and validate ideas:** `ak-play create <name> --template product-discovery` (or `ak-marketing-research` → `ak-competitor` → `ak-brainstorm` → `ak-marketing-planning`).
- **Content, SEO, and launch:** `ak-brand` → `ak-copywriting` / `ak-seo` / `ak-launch-strategy` / `ak-onboarding-cro` / `ak-pricing-strategy`.
- **Safety gate:** External publishing (social media, bulk email, paid ads) is **high risk**. Stop at a draft or dry run by default and obtain approval from `chanht_tt`.

---

## 5. Standard closeout report

Each Devin session hands off to Chief of Staff or `chanht_tt` with a short report containing four items:

- **Status:** `DONE` | `DONE_WITH_CONCERNS` | `BLOCKED`
- **Outcome and links:** PRs, commits, or files created or updated.
- **Evidence from actual runs:** Test, build, or hands-on verification commands and their results on the final revision.
- **Unverified or outstanding:** Clearly state anything that could not be tested or any next step.

---

## 6. Combining AgentKit and EzyPlatform skills for the upcoming Plane-style task management plugin

When starting a task management plugin on EzyPlatform Core (using `makeplane/plane` as a reference), combine the relevant skills from both kits:

| Phase or area | EzyPlatform skills | AgentKit skills |
|---|---|---|
| Research and comparison with `makeplane/plane` | `docs/research/plane-plugin-design-notes.md`, `docs/plugins/` | `ak-research`, `ak-xia`, `ak-brainstorm`, `ak-predict` |
| Architecture and phase planning | `ezy-guide`, `docs/research/ezyplatform-deep-research.md` | `ak-plan --hard`, `ak-plan red-team`, `ak-databases` |
| Java plugin development and development builds or deployments | `skills/ezy-build-plugin/SKILL.md`, `ezy-develop`, `ezyplatform-develop` | `ak-cook`, `ak-debug`, `ak-fix`, `ak-worktree` |
| Admin and Web UI/UX, i18n, and media | `ezy-i18n`, `ezy-media`, `ezy-sync` | `ak-frontend-design`, `ak-ui-ux-pro-max`, `ak-enhance-ux-ax` |
| Testing, edge cases, and security | Docker development stack (`./scripts/up.sh`), Admin/Web smoke check | `ak-scenario`, `ak-test`, `ak-web-testing`, `ak-security` |
| Review, documentation, and launch | `AGENTS.md`, `README.md` | `ak-review-pr`, `ak-code-review`, `ak-docs`, `ak-launch-strategy` |
