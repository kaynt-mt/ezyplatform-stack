# AgentKit workflow for bots and Devin sessions

This workflow applies to AgentKit **3.2.0** (the `engineer` and `marketing` kits exported for the `portable` target), the stack owner (`chanht_tt`), and the bots and Devin sessions that work on EzyPlatform.

## 1. Set up and verify the portable skills

From the stack checkout, supply an `AGENTKIT_API_KEY` licensed for both kits, or use an existing `ak` login:

```sh
python3 scripts/sync-upstream.py --require-agentkit
./scripts/ak --version
./scripts/ak kit list-kits --json
```

On a fresh checkout, verify that sync reports both `agentkit/engineer: 3.2.0` and `agentkit/marketing: 3.2.0`. Sync skips unlicensed kits; a successful exit alone does not prove both are present. With both kits installed, expect `167 skills in .agents/skills`:

| Group | Count | Examples |
|---|---:|---|
| Shared AgentKit skills (deduplicated) | 40 | `ak-agentkit`, `ak-brainstorm`, `ak-plan`, `ak-cook`, `ak-debug`, `ak-fix`, `ak-test`, `ak-scout`, `ak-journal`, `ak-worktree` |
| Engineer-only | 65 | `ak-review-pr`, `ak-code-review`, `ak-security`, `ak-ship`, `ak-scenario`, `ak-databases`, `ak-web-testing`, `ak-devops`, `ak-predict` |
| Marketing-only | 43 | `ak-play`, `ak-marketing-research`, `ak-competitor`, `ak-brand`, `ak-launch-strategy`, `ak-seo`, `ak-campaign` |
| EzyPlatform skills | 19 | `ezy-guide`, `ezy-new`, `ezy-sync`, `ezy-develop`, `ezyplatform-develop`, `ezy-i18n`, `ezy-media` |

The stack's own [plugin build skill](../skills/ezy-build-plugin/SKILL.md) is tracked separately and is not part of that count.

**Skills are agent instructions, not shell commands.** In the coding agent, request the skill by its installed name and give its arguments as part of that request. If the host does not register slash commands, ask it to read and follow `.agents/skills/<name>/SKILL.md`. Start with `ak-agentkit` (or `ak-help`) for routing. Use `./scripts/ak <command> --help` only for actual CLI commands such as `kit list-kits` and `journal create`.

## 2. Adapt the workflow to Devin

- Use `ak-security` when performing a defensive security review; `ak-security-scan` is not a skill in this export.
- Coordinate multiple sessions through **Chief of Staff and Devin Boards** (or Dynamic Workflows for five or more independent workstreams). Do not use the Claude Code orchestration skills `ak-team` or `ak-orchestrate` for that on Devin. Use `ak-worktree` when isolating branches in one VM.
- Devin does not provide the Claude Code `kongming` subagent behind `--advice` or the verifier waves behind `--ultra`. Use `ak-brainstorm`, `ak-predict`, or the `red-team` mode of `ak-plan` to challenge a proposal.
- Plans live under `plans/<timestamp>-<slug>/` (`plan.md` and `phase-NN-<name>.md`); reports and journals go under `plans/reports/` and `plans/journals/`. Do not commit scratch artifacts. For a durable decision, use the `ak-journal` skill or run `./scripts/ak journal create "Decision title"` from the intended project. For small tasks, use `--skip-journal` on the invoking skill where supported.

### Roles

- **Owner (`chanht_tt`):** Approves production work, database/volume deletion, real `.env` or secret changes, high-risk architecture, public releases, and product decisions.
- **Chief of Staff:** Splits work on Devin Boards, assigns one writer per branch, checks evidence, and merges PRs for bot-owned repositories after CI and Devin Review pass.
- **Upstream Watcher:** Tracks new versions of EzyPlatform, CPPAI, and AgentKit.
- **Devin sessions:** Run real checks and open PRs. Do not merge unless explicitly delegated for a bot-owned repository.

## 3. Rules for every workflow

Follow the [model routing rule](model-routing.md) for every Bot and Devin session.

1. Default to **local/dev**. Get separate owner approval before production writes, `docker compose down -v`, changes to real credentials, or public publishing. Back up data before publishing or migrating. Keep credentials out of artifacts, logs, and Git; if one is exposed, redact it and request rotation.
2. Assign one writer at a time per branch. Parallel tickets must have non-overlapping file ownership.
3. Before multi-step work, agree on **Outcome, Constraints, Non-goals, and Acceptance criteria**.
4. Choose the smallest workflow that meets the risk. Skip formal planning for bounded, reversible tasks. Use `ak-plan` and split ownership for multi-phase work. Require tests and review for elevated risk. For high risk (auth, payments, data migration, a public contract, destructive operations, public publishing), add defensive security review, independent review, and owner approval before irreversible steps. Drop intermediate steps that produce no artifact and do not reduce verification.
5. Prove the root cause before fixing a defect (`ak-debug` before `ak-fix`). Stop and escalate after three failed fix attempts. Do not weaken tests or claim completion without evidence from the final revision.

## 4. Choose a workflow

### Quick task (trivial, low risk)

`ak-scout` (if needed) → `ak-cook --fast --skip-journal` → `ak-test` → `ak-code-review --pending`.

Confirm the four contract items, make the smallest change, and run the narrowest check that covers it. Open a PR and wait for CI and Devin Review.

### Multi-phase feature (epic, elevated or high risk)

`ak-brainstorm` (with `ak-research` or `ak-xia` if comparing reference projects) → `ak-plan --hard` (use `validate` or `red-team` for higher risk) → Chief of Staff splits tickets on Devin Boards. For each phase: EzyPlatform domain skill + `ak-cook <plan-path>` → `ak-test` → `ak-security` if the change touches auth, APIs, the database, or user input → `ak-code-review` → PR and Devin Review.

Compare at most three designs and call out the assumption most likely to fail. Give each phase its files and verification criteria. Run Admin/Web smoke checks on Docker dev for plugin changes; don't start a dependent phase until the previous one passes review. Use `ak-journal` for architectural decisions worth preserving.

### Bug or CI failure

`ak-scout` → `ak-debug` → `ak-fix` → `ak-test` → `ak-security` for security-sensitive fixes → `ak-code-review --pending`.

Record actual versus expected behavior, reproduce it locally, and prove the root cause. Where possible, show the regression test fail before the fix and pass after it. Report the before/after evidence; use `ak-retro` for recurring issues or after a substantial repair.

### PR review

Use `ak-review-pr <PR>` for a GitHub PR or `ak-code-review --pending` for a local diff. Add `ak-security` for changes to auth, payments, user input, secrets, or dependencies.

Read the PR description, related ticket and diff. Check the contract, regression risk, security, compatibility, tests, and maintainability. Run the necessary local checks for high-risk or public-contract changes. Classify findings as **Blocker / Should fix / Suggestion**, with file and line references and supporting evidence. Recommend **Approve / Request changes / Comment**; do not use `--fix`, `--reply`, or `--merge` unless explicitly authorized.

### Product discovery, marketing, or launch

For discovery, ask the coding agent to use `ak-play` with the arguments `create <name> --template product-discovery`. This is **not** `./scripts/ak play`. The pinned portable skill's `references/create.md` shows named flags for its local `manifest.cjs` helper, but that helper expects positional arguments: `create <name> <template-file>`. The agent should still collect the required inputs and ask for approval at the template's gates. Alternatively, use `ak-marketing-research` → `ak-competitor` → `ak-brainstorm` → `ak-marketing-planning`.

To verify the template and manifest without publishing anything, use Node.js from a **disposable workspace outside the stack checkout**. Set `STACK` to the absolute path of the synced checkout first:

```sh
PLAY="$STACK/.agents/skills/ak-play"
TEMPLATE="$PLAY/templates/product-discovery.json"
node "$PLAY/scripts/template-loader.cjs" validate "$TEMPLATE"
node "$PLAY/scripts/manifest.cjs" create "Fresh clone audit" "$TEMPLATE"
```

This smoke check creates `data/playbooks/fresh-clone-audit/manifest.json`, with template ID `product-discovery@1.0.0` and 10 pending steps. It does not collect inputs or run the playbook. Use the skill to do those steps.

For brand, content, SEO, or launch, use `ak-brand` followed by the relevant skill (`ak-copywriting`, `ak-seo`, `ak-launch-strategy`, `ak-onboarding-cro`, or `ak-pricing-strategy`). Stop at a draft or dry run; public posts, bulk email, and paid ads need owner approval.

## 5. Report the result

- **Status:** `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED`.
- **Result:** Links to PRs, commits, or artifacts.
- **Evidence:** Actual test/build/HTTP results on the final revision.
- **Not verified:** What was not checked and why.

## 6. Example: planning a work-management plugin

For a work-management plugin inspired by `makeplane/plane`, choose the skills by phase:

| Phase | EzyPlatform resource | AgentKit skills |
|---|---|---|
| Research and compare | [Runtime plugin inventory](plugins/README.md) | `ak-research`, `ak-xia`, `ak-brainstorm`, `ak-predict` |
| Design and split the work | `ezy-guide`, [EzyPlatform development research](research/ezyplatform-deep-research.md) | `ak-plan --hard`, `ak-plan red-team`, `ak-databases` |
| Build and deploy locally | [Plugin build skill](../skills/ezy-build-plugin/SKILL.md), `ezy-develop`, `ezyplatform-develop` | `ak-cook`, `ak-debug`, `ak-fix`, `ak-worktree` |
| Design Admin/Web UI, localization, and media | `ezy-i18n`, `ezy-media`, `ezy-sync` | `ak-frontend-design`, `ak-ui-ux-pro-max`, `ak-enhance-ux-ax` |
| Test runtime and security | Docker dev (`./scripts/up.sh`), Admin/Web smoke checks | `ak-scenario`, `ak-test`, `ak-web-testing`, `ak-security` |
| Review, document, and prepare for launch | [Agent instructions](../AGENTS.md), [Stack README](../README.md) | `ak-review-pr`, `ak-code-review`, `ak-docs`, `ak-launch-strategy` |
