# Choosing an EzyPlatform skill

This repository tracks all **19 upstream skills** in [`skills/upstream/`](upstream/) as pinned in [`upstream.lock.json`](../upstream.lock.json): **7/7** from the Young Monkeys [EzyPlatform Skill Library](https://ezyplatform.com/ezyai/skill-library?lang=vi) (ZIP and SHA-256) and **12/12** from [CPPAI Agents Plugins](https://github.com/cppai-vn/agents-plugins/tree/b34ff7c7b4f1efa2a7a28fbf40e0f53565eb1b52/ezyplatform/skills) (pinned commit). `ezy-shared` contains shared Python code but no `SKILL.md`, so it is not counted as a skill. The [37 runtime plugins](../docs/plugins/test-report.md) are a separate catalog; syncing skills does not install them.

## Sync and locate skills

If `.agents/skills/` is missing in a **workspace that uses only Ezy**, run the following from the core repository:

```bash
python3 scripts/sync-upstream.py --skip-agentkit
find .agents/skills -mindepth 2 -maxdepth 2 -name SKILL.md | sort
```

The current lockfile yields `19 skills in .agents/skills`. In an AgentKit workspace, follow the [stack README](../README.md#cli-plugins-and-agent-skills) instead of passing `--skip-agentkit`. Sync recreates the skills directory, and that flag excludes `ak-*` from the new directory. The tables below link to snapshots you can read on GitHub. When using a skill, read its version in `.agents/skills/` and the accompanying documentation; do not load both copies at once.

To update the snapshots tracked in Git, run `python3 scripts/sync-upstream.py --refresh-ezy-skills` from the core repository. This regenerates only `skills/upstream/` from the pinned sources. It does not install AgentKit or replace `.agents/skills/`. CPPAI files are read directly from Git, independent of checkout line endings. Review the diff before committing; do not hand-edit the snapshots.

The CPPAI source uses the [MIT license (© 2026 CPPAI Co.,LTD)](upstream/LICENSE-CPPAI); retain the notice when redistributing it. The seven Young Monkeys packages are kept as distributed in their ZIPs. No separate license file was found in those ZIPs, so do not apply the CPPAI MIT license to them.

## Reference: all 19 skills

### CPPAI: `ezy-*` skills

| Skill | Use it to | Do not use it to | Related skills |
| --- | --- | --- | --- |
| [`ezy-guide`](upstream/ezy-guide/SKILL.md) | Classify a request, find the project, check roles, and pick a workflow. | Make changes or release anything; this skill only guides the choice. | `ezy-new`, `ezy-sync`, `ezy-develop` |
| [`ezy-new`](upstream/ezy-new/SKILL.md) | Create an EzyArticle content directory or configure a connection when `environment.json` is missing or the token is invalid. | Create a Maven project or Java plugin. | `ezy-sync`, `ezy-develop` |
| [`ezy-sync`](upstream/ezy-sync/SKILL.md) | Compare or pull pages and fragments from the server before editing. This is read-only on the server. | Push changes to the server or build Java code. | `ezy-author`, `ezy-publish` |
| [`ezy-author`](upstream/ezy-author/SKILL.md) | Edit HTML, Thymeleaf, CSS, and JavaScript, or author pages, fragments, and translations in EzyArticle. | Write a Java theme with new controllers or APIs, or manage plugin message bundles. | `ezy-sync`, `ezy-media`, `ezy-verify` |
| [`ezy-media`](upstream/ezy-media/SKILL.md) | Find, upload, or replace media, or manage its public or private visibility. | Package static assets in a JAR or make private files public to bypass permission checks. | `ezy-author`, `ezy-verify` |
| [`ezy-i18n`](upstream/ezy-i18n/SKILL.md) | Compare and sync EzySupport interface keys by language for Admin or Web. | Translate page content or edit `messages*.properties` in plugin source. | `ezy-author`, `ezy-verify`, `ezy-develop` |
| [`ezy-mail`](upstream/ezy-mail/SKILL.md) | Check mail delivery health, review the Contact Us flow, or manage EzyMail templates. | Publish content, install a new SMTP system, or send real email without approval. | `ezy-media`, `ezy-verify` |
| [`ezy-verify`](upstream/ezy-verify/SKILL.md) | Preview pages or fragments locally and verify site content after changes. | Replace Java tests, API authorization tests, or migration checks. | `ezy-author`, `ezy-publish` |
| [`ezy-publish`](upstream/ezy-publish/SKILL.md) | Plan, back up, and push EzyArticle content, or move it to Trash or restore it. | Submit a plugin or theme ZIP, or publish an AI skill. | `ezy-sync`, `ezy-verify`, `ezy-market-submit` |
| [`ezy-develop`](upstream/ezy-develop/SKILL.md) | Use `ezy dev` to prepare the native SDK and scaffold, build, or export a plugin, theme, or Socket module. Use it for Admin pages and Java APIs. | Only edit content pages or adjust shared Admin CSS. | `ezyplatform-develop`, `ezyplatform-install`, [plugin creation skill](ezy-build-plugin/SKILL.md) |
| [`ezy-admin-customize`](upstream/ezy-admin-customize/SKILL.md) | Customize a running Admin through EzySupport, such as its logo, CSS, layout, or buttons. | Add menus, controllers, views, or business permissions to a new plugin. | `ezyplatform-admin-customize`, `ezy-develop` |
| [`ezy-market-submit`](upstream/ezy-market-submit/SKILL.md) | Use `ezy market` to submit packaged plugins or themes, track review, and release approved versions. | Install an internal ZIP, publish EzyArticle content, or publish an AI skill. | `ezy-develop`, `ezyplatform-market-submit` |

### Young Monkeys: `ezyplatform-*` skills

| Skill | Use it to | Do not use it to | Related skills |
| --- | --- | --- | --- |
| [`ezyplatform-install`](upstream/ezyplatform-install/SKILL.md) | Set up EzyPlatform on a new machine. Choose native for SDK development or Docker when you only need a runtime. | Start the existing Compose stack; follow the [README](../README.md#getting-started-on-a-development-machine-or-cloud-vm). | `ezyplatform-develop`, `ezyplatform-reset-admin-password` |
| [`ezyplatform-develop`](upstream/ezyplatform-develop/SKILL.md) | Follow the Young Monkeys workflow to set up the JDK, Maven, and SDK and develop and export a theme or plugin from source. | Follow the equivalent `ezy-develop` workflow or edit content only. | `ezy-develop`, `ezyplatform-install`, `ezyplatform-market-submit` |
| [`ezyplatform-admin-customize`](upstream/ezyplatform-admin-customize/SKILL.md) | Follow the Young Monkeys workflow to change Admin appearance or behavior through EzySupport without creating a Java module. | Add a business screen, route, or plugin-specific permission. | `ezy-admin-customize`, `ezyplatform-develop` |
| [`ezyplatform-landing-page`](upstream/ezyplatform-landing-page/SKILL.md) | Create a standalone landing page from a creative brief, with a lead form, purchase buttons, preview, or a domain as needed. | Build a Java theme for an entire site or a multi-screen or API application. Do not install plugins, switch themes, publish, or change DNS without approval. | `ezy-author`, `ezy-media`, `ezy-verify` |
| [`ezyplatform-market-submit`](upstream/ezyplatform-market-submit/SKILL.md) | Follow the Young Monkeys workflow to submit plugin or theme ZIPs and manage Marketplace releases. | Deploy to a sandbox or publish an AI skill. | `ezy-market-submit`, `ezyplatform-develop` |
| [`ezyplatform-publish-skill`](upstream/ezyplatform-publish-skill/SKILL.md) | Package and submit an AI skill directory with a `SKILL.md` to the Skill Library. | Release a Java plugin or theme, or update this repository's pins. | `ezyplatform-market-submit`, `ezy-guide` |
| [`ezyplatform-reset-admin-password`](upstream/ezyplatform-reset-admin-password/SKILL.md) | Restore access by resetting the Admin password in the database when the owner has approved it and cannot sign in. | Grant member permissions, create a new account, or handle an expired project token. | `ezyplatform-install`, `ezy-new` |

## Choose a workflow

1. **Creating a Java plugin, Java theme, or Socket module?** Start with the [stack's plugin creation skill](ezy-build-plugin/SKILL.md). If you lack a native build runtime, read `ezyplatform-install`. Then choose **one** workflow: `ezy-develop` (the stack CLI) or `ezyplatform-develop` (the Young Monkeys scripts). `ezy dev create` scaffolds Maven modules; `ezy new` does not. Select only the modules you need.
2. **Adding an Admin page, Web API, or migration to an existing plugin?** Follow the Java development skill without scaffolding again. For an Admin page, add a menu, controller, view, and permissions. For an API, enforce authentication and resource scoping on the server. For a migration, add new SQL to the Admin module and test fresh installs and upgrades with data. See the [Admin, database, and API guides](../docs/research/ezyplatform-guide-inventory.md) and the [runtime plugin test notes](../docs/plugins/test-report.md#dependency-order-notes). Enabling several plugins at once caused missing tables when Admin and Web started in parallel; HTTP 200 does not prove the migrations ran. For changes limited to the shared Admin logo or CSS, use a `*-admin-customize` skill.
3. **Editing an existing site's interface or content?** If no content project exists, start with `ezy-new`. Then use `ezy-sync` → `ezy-author` → `ezy-media`, `ezy-i18n`, or `ezy-mail` as needed → preview with `ezy-verify` → obtain user approval → `ezy-publish` → verify again on the site with `ezy-verify`. For a standalone landing page, start with `ezyplatform-landing-page` and keep the page in draft until publication.
4. **Deploying or releasing?** To test an internal plugin, build and package it in the native environment, install your ZIP in Docker dev, then check activation, Admin and Web, logs, permissions, and migrations using the [plugin creation skill](ezy-build-plugin/SKILL.md). For public distribution, use `ezy-market-submit` or `ezyplatform-market-submit` for a plugin or theme, `ezyplatform-publish-skill` for an AI skill, and `ezy-publish` for site content. Obtain separate approval before writes and keep credentials out of Git.
