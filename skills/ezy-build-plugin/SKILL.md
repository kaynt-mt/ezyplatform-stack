---
name: ezy-build-plugin
description: Scaffold, develop, build, package, test-install, or upgrade a Java plugin on EzyPlatform Core Stack. Use this skill to scaffold Admin and Web modules, add APIs, menus, views, permissions, i18n, or migrations, or prepare a Marketplace release.
---

# Create an EzyPlatform plugin

This skill is specific to **this stack** and does not replace the upstream skills. Keep the application in a separate repository; the core repository provides the runtime and tools. For changes to articles, low-code interfaces, or EzyArticle content, use the content skills below instead of creating a Java plugin.

## 1. Choose the right skill

See the [catalog of all 19 Ezy skills](../README.md) to sync them, locate their `SKILL.md` files, and distinguish Java plugins from EzyArticle content or Admin customization through EzySupport. After reading `ezy-guide`, choose **one** Java workflow: `ezy-develop` (the stack's `ezy dev` wrapper, used below) or `ezyplatform-develop` (the Young Monkeys scripts). Read `ezyplatform-install` if you need a native environment, and `ezy-market-submit` or `ezyplatform-market-submit` if you need to submit a plugin to Marketplace.

## 2. Create a Maven project in a native build environment

Do not confuse `./scripts/ezy new` with the plugin generator: `new --mode live|local|both` creates a **content project** with `environment.json`, not a Java module. `./scripts/ezy dev create` calls the **SDK** command `ezy.sh create` and needs a native `EZYPLATFORM_HOME` with `cli.sh`, JDK 8, Maven, the SDK, and development libraries. Do not point `--home` at the core checkout or a Compose volume. Use **a separate native environment to build** and **the stack's Docker environment for acceptance testing**. Do not install natively or modify shared environments without approval.

This example is for Linux, WSL, or macOS. Replace both absolute paths before running it. If needed, read `ezyplatform-install` and the [development environment setup guide](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-setup-development-environment?lang=vi) to prepare a separate native environment compatible with the target core. Do not replace the existing Compose setup. Check runtime and SDK versions, core artifacts in the POM, and the dependencies actually needed. The stack pins runtime **1.5.9**, **Java 11**, and **MySQL 8.0**; the SDK and CLI are versioned separately. On Windows, follow the upstream skill's PowerShell instructions. If native and Compose run on the same machine, use different Admin and Web ports and separate databases.

```bash
STACK=/path/to/ezyplatform-stack
NATIVE_HOME=/path/to/separate-native-runtime
OUT="$(dirname "$STACK")"

"$STACK/scripts/ezy" dev check --home "$NATIVE_HOME"
# Run setup only if tools are missing; it may download the JDK, Maven, and SDK and install artifacts in ~/.m2.
"$STACK/scripts/ezy" dev setup --home "$NATIVE_HOME" --no-profile
"$STACK/scripts/ezy" dev create example-plugin --home "$NATIVE_HOME" \
  --group com.example --package com.example.plugin \
  --modules admin-plugin,web-plugin --out "$OUT"
cd "$OUT/example-plugin"
```

Use a group and package namespace owned by the project. Choose a new directory instead of overwriting an existing project. In an installed SDK environment, the equivalent direct command is `ezy.sh cp example-plugin -g com.example -p com.example.plugin -i admin-plugin,web-plugin -o "$OUT"`. See the [quickstart](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-plugin-development-quickstart?lang=vi) and [SDK commands](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-sdk-commands?lang=vi).

| Directory or file | Purpose |
| --- | --- |
| Root `pom.xml`, `export.sh`/`export.bat` | Maven reactor, versions and profiles, and the scaffold's build and export workflow. Read the actual script before running it. |
| `<project>-sdk` | The plugin's **shared** entities, repositories, domain services and policies, DTOs, and enums. This is not installed separately. Do not create another `*-common` unless needed or confuse it with the core's `ezyplatform-common`. |
| `<project>-admin-plugin` | Operations controllers and views, module configuration, menus, and SQL scripts applied by Admin. |
| `<project>-web-plugin` | User-facing controllers and APIs, Web authentication, theme-compatible views and fragments, and static files as needed. |
| Deployable module | `module.properties` declares the type and runtime dependencies; `assembly.xml` controls the bundle; `src/main/resources/{templates,static,messages}` holds UI assets. `menus.properties` belongs at the root of the Admin module. Theme and Socket are optional; enable them only if needed. Each Web runtime has only one active theme. |

See the [plugin project structure](https://youngmonkeys.org/ezyplatform/guides/the-structure-of-a-plugin-project?lang=vi) and the [book-store example](https://github.com/youngmonkeys/ezyplatform-examples/tree/main/book-store). For dependencies on managed modules, check the dependencies and versions in the POM, `dependencies` in `module.properties`, and `@ComponentsScan` in the startup test. Only with approval, run `"$STACK/scripts/ezy" dev link <plugin-name> --home "$NATIVE_HOME" -m admin-plugin,web-plugin` for the modules you actually use. **The command can download, install, and activate missing dependencies.** Do not run it just to look something up. See the [linking guide](https://youngmonkeys.org/ezyplatform/guides/link-a-plugin?lang=vi).

## 3. Implement a complete vertical slice

1. **Schema and Java:** Put JPA entities, EzyData repositories (for example, `@EzyRepository` and `EzyDatabaseRepository`), services, and policies in the SDK. Write flow: DTO → validate → authorize → transaction → response DTO. Enforce access scope in the query, index for real filters, and reuse the core User as the identity when appropriate. See [EzyPlatform research](../../docs/research/ezyplatform-deep-research.md).
   - Use `@EzyQuery` for joins, sorting, and projections. When using `Next` for offset and limit, make it the final argument. For multistep mutations, do not assume generated write queries share a transaction: verify the `EzyJpaRepository` path and use of a single `EntityManager` on the pinned SDK, then test rollback between steps. See [EzyData](../../docs/research/youngmonkeys/ezydata.md).
   - To let the runtime inject services without retaining request state, check package scanning and the configuration → bean → after-config order in a startup test. Do not create a standalone context inside the plugin. See [EzyFox Bean](../../docs/research/youngmonkeys/ezyfox-library.md).
2. **Migrations:** Put plugin-prefixed SQL in `<project>-admin-plugin/src/main/resources/scripts/`; see the [SQL examples](https://github.com/youngmonkeys/ezyplatform-examples/tree/main/personal/personal-admin-plugin/src/main/resources/scripts). The development skill describes scripts applied once per filename. Leave released files intact and add a new file for each change. Verify fresh installs and upgrades. Do not assume automatic rollback or that a Web-only plugin runs Admin scripts. Back up both the database and runtime before writing to an environment with data. For incompatible changes, use expand–migrate–contract.
3. **Admin:** Add menus in `menus.properties`. For detail screens, declare a hidden route following the example's convention. Place templates in `templates/<project>/` and use an EzyHTTP controller returning a `View`. Check the actual plugin prefix. Use `@Authenticated`, `@AdminId`, and `@EzyFeature` for Admin permissions. Hiding a button in the UI is not server-side authorization. See [Admin pages](https://youngmonkeys.org/ezyplatform/guides/create-an-admin-page?lang=vi) and [menus](https://youngmonkeys.org/ezyplatform/guides/create-menus-for-admin-plugin?lang=vi).
   - To extend the shared layout, use fragments and a `ViewDecorator` instead of editing core templates. For example, pass the fragment name through `rightToolbarToolFragments` and render the `content` region. Protect the API behind the button as well. See the [Admin toolbar guide](https://youngmonkeys.org/ezyplatform/guides/add-admin-right-toolbar-tool?lang=vi).
4. **Web:** In API controllers, use `@UserId` after confirming the Web auth interceptor is registered for your route. For views, use a dedicated namespace and Thymeleaf fragments, or mount the UI at an extension point in the active theme. Check user and resource permissions in the service, including downloads, searches, and counts. Do not grant system Admin privileges to members. Test anonymous users, wrong roles, out-of-scope resources, authorized members, and access after revocation. See [Web authentication](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-web-authentication?lang=vi), [permissions](https://youngmonkeys.org/ezyplatform/guides/permission-in-ezyplatform?lang=vi), and [themes and plugins](https://youngmonkeys.org/ezyplatform/guides/understanding-ezyplatform-themes-and-plugins?lang=vi).
   - Bind DTOs from the path, query, or body. Use `View` for HTML and a DTO or `ResponseEntity` for APIs. Verify auth errors never reach business handlers. Defer Socket until after the HTTP MVP, then test subscriptions, reconnections, and fan-out permissions. See [EzyHTTP](../../docs/research/youngmonkeys/ezyhttp.md) and [EzyFox Server](../../docs/research/youngmonkeys/ezyfox-server.md).
5. **i18n and static resources:** Put menu labels, form errors, and default strings in `messages/messages.properties`. Add `messages_vi.properties` and bundles for other supported languages. Use keys instead of hard-coded text in templates; expose only the keys JavaScript needs. `static/` is accessible over HTTP; do not put secrets there. See the [localization guide](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-multi-languages?lang=vi).

## 4. Test, build, export, and inspect the ZIP

From the plugin repository, check Maven profiles and test database addresses. Use only development databases. Run Maven checks and tests in the helper's environment, then use the scaffold script to package it. Example export profiles may skip tests, so a successful export **does not replace** a separate test suite run.

```bash
"$STACK/scripts/ezy" dev run --home "$NATIVE_HOME" -- mvn clean verify
"$STACK/scripts/ezy" dev run --home "$NATIVE_HOME" -- bash export.sh
```

The [example script](https://github.com/youngmonkeys/ezyplatform-examples/blob/main/book-store/export.sh) builds each module using its POM profile, then runs `ezy.sh package` followed by `ezy.sh export`. Export writes to the **native** runtime but does not activate or restart it. To package without writing to the native runtime, run the scaffold's Maven steps up to the export line and call `ezy.sh package`; do not run package without Maven artifacts. If you use `ezy dev export` instead, the helper **activates native modules and restarts by default** and can change the active theme. Use it only in a sandbox where you want that behavior.

Locate the project ZIP in `target/project/` using the actual output. Check the ZIP structure and contents: correct module types and versions, expected templates, messages, and SQL, and no test configs, tokens, duplicate core JARs, or files that override platform configuration. Record the artifact name, version, and SHA-256 before transferring it to Docker. See [package and export commands](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-sdk-commands?lang=vi).

## 5. Install your artifact in the Docker development stack

1. Follow the [core repository README](../../README.md) and run `./scripts/up.sh`. On a fresh installation, open `http://127.0.0.1:9090/setup-admin`, create a super admin, and sign in at `/login`. Web defaults to `http://127.0.0.1:8080/`; if you changed the port, use the URL reported by the script. Do not use production Admin.
2. In **Modules** in local Admin, select **Upload Project** for your own project ZIP. Verify the name and version, then select **Active** for the correct Admin or Web module. Do not use Upload Project instead of signature-verified Marketplace installation for third-party plugins. `cli.sh "install <name>"` searches Marketplace; it does not install a local ZIP. Do not copy JARs directly into the volume or edit an installed plugin.
3. If the UI saved activation without restarting, run `docker compose restart ezyplatform` from the core repository. Verify with `docker compose ps` and `docker compose logs --tail=100 ezyplatform mysql`. If the UI shows **Apply** as pending, finish it before assuming the module is running. Verify the active version, Admin menus and views, Web routes, schema, and data. HTTP 200 on the homepage only shows that the core is alive. See [installing and activating modules](https://youngmonkeys.org/ezyplatform/guides/add-a-plugin-to-your-ezyplatform?lang=vi). The [report on 37 plugin tests](../../docs/plugins/test-report.md#dependency-order-notes) notes missing tables when many plugins were enabled together and Admin and Web started in parallel. Verify dependencies first, then check migrations in the logs and schema before concluding Web works.

Compose starts only Admin and Web by default. If you add a Socket module, enable and start Socket and verify the connection and protocol separately. Running Admin and Web does not prove Socket is working.

## 6. Troubleshoot, upgrade, and release

| Symptom | First checks |
| --- | --- |
| Missing parent or Test SDK, or missing `systemPath` | Check `ezy dev check --home …`, the JDK, Maven, SDK, native path, and JAR versions. `ezy dev sync-versions --home …` updates versions of **installed** dependencies. Review the diff; it does not upgrade the core. |
| Missing menus, JS, or i18n, or a 404 | Check ZIP contents, activation and version by module type, controller and menu prefixes, template namespaces, and asset/message bundles. For `*StartupTest` in the IDE, set the working directory to the module and avoid port conflicts with the runtime. |
| HTTP 401 or 403, or Web receives an empty user ID | Check interceptor or theme setup and annotations. Test authorized and unauthorized cases; do not remove authentication to get around an error. |
| App fails after install, database error, or class/linkage error | Start with Admin and Web logs, then compare SQL and migrations, `dependencies`, versions, and duplicated core JARs. Do not delete the volume to “fix” data. See [build and export errors](https://youngmonkeys.org/ezyplatform/guides/nhung-ly-do-khien-ban-khong-the-build-chay-va-export-duoc-du-an-plugin-ezyplatform?lang=vi). |

In the native environment, run diagnostic commands through `"$STACK/scripts/ezy" dev <command> --home "$NATIVE_HOME"`:

- `status` shows URLs, Admin and Web status, and active modules. See also `$NATIVE_HOME/logs/{admin,web}-server.log`. `restart` restarts native Admin and Web, not Compose.
- `tables core` or `tables <plugin-name>` catalogs table creation SQL; it does not inspect a migrated database schema.
- `find-class <class-name>` identifies the JAR containing a class. Use `decompile <fully-qualified-name-or-JAR-path>` only on local artifacts you are authorized to inspect; prefer the public SDK or source. Do not copy decompiled code into the plugin.

**Local upgrade:** Bump the bundle version, test fresh installs and upgrades with sample data, and back up the database and runtime. In Admin, select **Update Manually**, upload the new ZIP, and select **Apply** as described in the [upgrade guide](https://youngmonkeys.org/ezyplatform/guides/update-a-plugin?lang=vi). Verify the actual version, schema, and permissions. Rebuilding the image does not replace plugins in an existing volume. Rolling back an artifact does not undo migrations; for an incompatible change, restore a verified database and runtime pair.

**Marketplace:** Proceed only when requested and authorized. Obtain separate approval before each write. Read the [FAQ](https://ezyplatform.com/faq) and `ezy-market-submit` or `ezyplatform-market-submit`. Check compatibility from Java 8 onward, i18n, asset licenses, reserved namespaces, and bundle size and contents against actual server limits. Prepare an icon, banner, metadata, release notes, and a ZIP named `<url-name>-<X.Y.Z>.zip`. With the wrapper, the sequence is `ezy market login` (the user approves in the browser) → `projects`/`categories` → `create --json …` if the project does not exist → `upload-version --name … --version … --zip … --notes-file …` → `status --name …` → `release --name …` **only after** the version is `RELEASABLE` and release approval has been granted. Run each command through `"$STACK/scripts/ezy"`.

If Marketplace requires source code, submit only an approved distributable copy using `upload-source --name … --version … --zip … --notes-file …` with an archive named `<url-name>-<version>-sources.zip`. Document installation, configuration, permissions, and upgrades in the project's Docs section (`/account/projects/<url-name>/docs`). The CLI stores tokens in `~/.ezyplatform/credentials.json`; keep that file, tokens, passwords, cookies, and database dumps out of logs, ZIPs, and Git. This guide does not require an actual login or publication.

### Handoff checklist

- [ ] Separate plugin repository; correct modules, dependencies, and versions; commands run in the intended native or Docker environment.
- [ ] Test domain behavior, cross-scope permissions, and migrations for fresh installs and upgrades. Do not rely on build results or the homepage.
- [ ] Clean ZIP; correct version installed in a sandbox; Admin, Web, i18n, logs, and rollback checked.
- [ ] Report the artifact path, version, SHA-256, verified results, and what could not be checked. Publish to Marketplace only with separate approval.
