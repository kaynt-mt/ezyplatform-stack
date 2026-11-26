# Use this stack as your team's EzyPlatform core

## 1. Create your core repository

The source owner enables **Template repository** in [GitHub repository settings](https://github.com/kaynt-mt/ezyplatform-stack/settings). On the [source repository](https://github.com/kaynt-mt/ezyplatform-stack), a recipient with access then chooses **Use this template → Create a new repository**, selects their own owner and visibility, and leaves **Include all branches** off. This copies the default-branch files, not its history, GitHub secrets, access settings, or Devin Bots.

Keep the source private unless the owner authorizes broader distribution. Enabling the template flag does not grant redistribution rights. Before giving a new audience access or publishing a copy, the owner should confirm rights to the stack and its third-party contents. The stack has no repository-wide license; the [upstream skill notices](../skills/README.md) distinguish the CPPAI MIT notice from the seven Young Monkeys packages with no separate license in their ZIPs. A public download alone does not establish redistribution permission.

## 2. Start the core without AgentKit

Clone your new repository and run this from its root on a machine with the [stack prerequisites](../README.md#start-on-a-development-machine-or-cloud-vm):

```bash
./scripts/up.sh
python3 scripts/sync-upstream.py --skip-agentkit
./scripts/ezy --version
python3 -m unittest discover -s tests -v
```

Create your own Admin account at [local Admin setup](http://127.0.0.1:9090/setup-admin), sign in at [Admin](http://127.0.0.1:9090/login), and check [Web](http://127.0.0.1:8080/). Keep `.env` and Admin credentials local. The generated Ezy skills are in `.agents/skills/`; start with `ezy-guide`. Keep app code in a separate repository and use the [content or Java plugin workflow](../README.md#create-an-application-on-the-core) to build against your core.

## 3. Create your Devin Bot team

Give your Devin workspace access to **your** core and app repositories. Follow [Devin's repo setup guide](https://docs.devin.ai/tutorial-library/repo-setup) to create a blueprint for your core checkout. Include the agent-skill sync in the core blueprint's maintenance steps so every fresh session scans the generated skills before it starts:

```yaml
maintenance:
  - name: sync pinned CLI, plugins and skills
    run: ./scripts/sync-agent-skills.sh
```

Each session has its own VM: run the dev stack in the session that tests it, or use an authorized private route to a shared dev instance. A session's `127.0.0.1` cannot reach another machine's Admin. Start with manual tasks; add chat or PR triggers only after checking what each Bot can access.

In **Bots → Template library**, create the roles below. Use **Start from scratch** when no matching template is available. Give each Bot the common instruction and its role instruction, substituting your actual repo names. GitHub templates do not create Bots; [Devin Bot templates](https://docs.devin.ai/work-with-devin/bots/templates) copy instructions only, not memory, secrets, or connections. Connect and scope each Bot separately.

**Common instruction:** “Our core is OWNER/CORE and our app is OWNER/APP. Read the core's AGENTS.md and docs/agentkit-workflow.md. AgentKit is optional; use the EzyPlatform skills and native Devin tools if it is unavailable. Work in local/dev unless I approve otherwise. Keep credentials out of Git and chat. Report the PR, tested revision, evidence, and any gaps.”

| Role | Starting point | Role instruction |
|---|---|---|
| Chief of Staff | [Chief of Staff](https://devin.ai/bots/templates/chief-of-staff) | “Track work and handoffs on our Devin Board. Route core work to Platform, app work to Product, and independent verification to QA. Keep one writer per branch. Escalate approvals to me.” |
| Platform Engineer | Start from scratch | “Own the core repo, runtime setup, CLI, shared skills, and dependency pins. Prepare and verify core changes on dev before handing off a PR.” |
| Product Engineer | [Product Engineer](https://devin.ai/bots/templates/product-engineer) | “Build app features and fixes in the app repo, against the pinned core. Open tested PRs and hand them to QA.” |
| QA Engineer | [QA Engineer](https://devin.ai/bots/templates/qa-engineer) | “Verify assigned PRs independently on dev. Report what passed, failed, or could not be tested, with evidence. Do not merge.” |
| Upstream Watcher | Start from scratch | “Watch EzyPlatform, CPPAI, and the source stack. Report current and candidate versions, changes, and upgrade risks to Platform. Watch AgentKit stable only if we use it. Do not change pins yourself.” |

For the first handoff, ask Chief of Staff to route a core smoke check to Platform and an independent verification to QA. Follow the [workflow](agentkit-workflow.md) with or without AgentKit; only the `ak-*` instructions depend on the paid kit.

## 4. Optional: add AgentKit

Skip this section if you do not have an AgentKit license. The core, the EzyPlatform skills, and your Devin Bots work without one.

If you own a license, supply your own `AGENTKIT_API_KEY` through your shell's secret mechanism or [Devin's secret store](https://docs.devin.ai/product-guides/secrets). Make it available as an environment variable only to the jobs that need it. For Devin blueprint builds, save it as an organization or repository secret; user- and session-scoped secrets are not available to snapshot builds. Do not put the key in a prompt, blueprint text, or Git.

```bash
./scripts/sync-agent-skills.sh
./scripts/ak --version
```

With the key present, the script requires at least one licensed pinned kit. Without the key, it still completes with the Ezy-only skill set. Check the sync output for each kit you intended to install; sync skips kits your account does not cover. If a Bot cannot use a needed skill, fall back to the native tools or run [the workflow's checks](agentkit-workflow.md#1-set-up-and-verify-the-portable-skills) for your licensed kits.

[AgentKit's Terms of Use §3.2](https://agentkit.best/terms) prohibit redistribution of the kits or their source and forbid sharing keys or downloads with unauthorized users. The template tracks version pins and setup instructions, not paid skill files. Keep `.upstream/` and `.agents/skills/` ignored, and never copy paid kits into Git or any artifact shared with unauthorized users. Blueprint builds may generate the kits inside a private Devin environment only when every user who can access that environment is covered by your license; otherwise use the Ezy-only setup.

## 5. Pull later stack updates

A GitHub template copy has unrelated history. Adding an upstream remote lets you **fetch and compare**; it does not enable merging the source's `main` directly. Add the remote while you still have access, and record the source commit that supplied the copied files before customizing the core. If the source moved during creation, compare the initial copied tree with the candidate source commit before adopting it as the baseline.

```bash
git remote add upstream https://github.com/kaynt-mt/ezyplatform-stack.git
git fetch upstream main
git log -1 --format=%H upstream/main
```

For a later update, start from a clean checkout of your own default branch. Replace `OLD` with the last upstream commit you adopted and review the proposed delta before applying it:

```bash
git fetch upstream main
OLD=REPLACE_WITH_YOUR_RECORDED_SOURCE_SHA
NEW=$(git rev-parse upstream/main)
git diff --stat "$OLD" "$NEW"
git diff "$OLD" "$NEW"
git switch -c update/ezyplatform-core
git diff --binary "$OLD" "$NEW" | git apply --3way --index
```

Review the staged changes and resolve any conflicts in the update branch; never overwrite local app or configuration changes blindly. Re-run the sync and smoke checks above, then open a PR in your own repository. Record the new source commit only after you adopt its changes. Review runtime and database upgrade notes and use test volumes before changing an existing installation.
