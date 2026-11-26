---
name: ezy-build-plugin
description: Scaffold, develop, build, package, install, or upgrade a Java plugin for EzyPlatform Core Stack. Use for Admin/Web modules, APIs, menus, views, permissions, i18n, migrations, and Marketplace releases.
---

# Build an EzyPlatform plugin

This stack-specific skill complements the upstream skills. Keep the app in a separate repository; the core repo provides the runtime and tooling. For articles, low-code UI, or EzyArticle content, choose a content skill instead of creating a Java plugin.

## 1. Choose a skill

Use the [catalog of 19 Ezy skills](../README.md) to sync skills and choose the relevant `SKILL.md`. After reading `ezy-guide`, choose one Java workflow: `ezy-develop` (the `ezy dev` workflow below) or `ezyplatform-develop` (Young Monkeys scripts). Use `ezyplatform-install` to prepare a native environment, and `ezy-market-submit` or `ezyplatform-market-submit` for Marketplace releases.

## 2. Scaffold in a native build environment

`ezy new --mode live|local|both` creates a **content project** with `environment.json`, not a Java plugin. Scaffold Java modules using the SDK's `ezy.sh create` via the stack helper below. Build in a **separate native install** and test the result in the stack's **Docker runtime**. Do not install native tooling or change shared environments without approval.

Follow `ezyplatform-install` and the [development environment guide](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-setup-development-environment?lang=vi). The native build needs JDK 8, Maven, the development SDK, and development libraries matching the target runtime. The Docker stack pins EzyPlatform **1.5.9**, container Java **11**, and MySQL **8.0**; the SDK and CLI have independent versions. If native and Docker run on the same machine, use separate Admin/Web ports and databases.

Use **`--dir` with the installation root** if the native installer was run with `install --dir`. For instance, pass `--dir /path/to/native-install` when the runtime is `/path/to/native-install/ezyplatform` and its JDK is `/path/to/native-install/jdk`; setup will use the matching `dev/` directory. **`--home` identifies a runtime home containing `cli.sh`**; it does not select the enclosing custom installation root and may use the default development tools directory. Do not pass the core checkout or a Compose volume as either flag.

Example for Linux, WSL, or macOS (replace the paths). On Windows, use the upstream PowerShell instructions for native installation and WSL for the Bash workflow below.

```bash
STACK=/path/to/ezyplatform-stack
NATIVE_DIR=/path/to/native-install
NATIVE_HOME="$NATIVE_DIR/ezyplatform"
OUT="$(dirname "$STACK")"

"$STACK/scripts/ezy" dev check --dir "$NATIVE_DIR"
# Only run setup if tools or libraries are missing; it can download tools and install Maven artifacts.
"$STACK/scripts/ezy" dev setup --dir "$NATIVE_DIR" --no-profile
python3 "$STACK/scripts/ezy-plugin.py" create example-plugin --dir "$NATIVE_DIR" \
  --group com.example --package com.example.plugin \
  --modules admin-plugin,web-plugin --out "$OUT"
cd "$OUT/example-plugin"
```

Use a group and package you own. The helper refuses to overwrite an existing project, creates the empty target expected by SDK 0.2.8, and corrects generated `assembly.xml` exclusions from the project group to `org.youngmonkeys:ezyplatform-*`. If scaffold fails, inspect the newly created directory and use a fresh target when you retry. See the [quickstart](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-plugin-development-quickstart?lang=vi) and [SDK commands](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-sdk-commands?lang=vi).

### Maven download and cache troubleshooting

The pinned upstream `ezy dev setup` helper owns the Maven distribution download. If Maven Central returns HTTP 429, provision Maven separately and put its `bin` directory first on `PATH` before running setup. For Maven 3.9.16, the pilot used the same distribution and SHA-512 from a Maven Central mirror. Run this in a scratch directory outside the stack, and extract only after verification succeeds:

```bash
archive=apache-maven-3.9.16-bin.tar.gz
mirror=https://maven-central.storage-download.googleapis.com/maven2/org/apache/maven/apache-maven/3.9.16
curl -fLO "$mirror/$archive" &&
  curl -fLO "$mirror/$archive.sha512" &&
  printf '%s  %s\n' "$(tr -d '[:space:]' < "$archive.sha512")" "$archive" | sha512sum -c - &&
  tar -xzf "$archive" &&
  export PATH="$PWD/apache-maven-3.9.16/bin:$PATH"
```

Use your approved mirror in Maven's `settings.xml` if artifact downloads also hit the rate limit (for the pilot, a mirror with `mirrorOf` set to `central` and URL `https://maven-central.storage-download.googleapis.com/maven2` worked). To use a non-default local cache, configure **both** Maven and the helper's independent cache check, before setup, verify, and export:

```bash
export MAVEN_LOCAL_REPO=/absolute/path/to/maven-cache
export MAVEN_ARGS="-Dmaven.repo.local=$MAVEN_LOCAL_REPO"
# If needed, append this using the path to your Maven settings file:
# export MAVEN_ARGS="$MAVEN_ARGS -s /absolute/path/to/settings.xml"
```

| Path | Purpose |
| --- | --- |
| Root `pom.xml`, `export.sh` / `export.bat` | Maven reactor, versions, profiles, and generated build/export workflow. Read the actual script before running it. |
| `<project>-sdk` | Shared entities, repositories, services, policies, DTOs, and enums. This is not a separately installed module or the platform's `ezyplatform-common`. |
| `<project>-admin-plugin` | Admin controllers/views, module configuration, menus, and SQL scripts applied by Admin. |
| `<project>-web-plugin` | User-facing controllers/APIs, Web auth, views/fragments compatible with the active theme, and static assets. |
| Deployable module | Runtime type/dependencies in `module.properties`, bundle rules in `assembly.xml`, and templates, static assets, and messages in `src/main/resources/`. `menus.properties` is at the Admin module root. Theme and Socket are optional; only one theme can be active per Web runtime. |

See the [plugin structure guide](https://youngmonkeys.org/ezyplatform/guides/the-structure-of-a-plugin-project?lang=vi) and [book-store example](https://github.com/youngmonkeys/ezyplatform-examples/tree/main/book-store). For managed dependencies, verify the POM coordinates/version, `dependencies` in `module.properties`, and startup test `@ComponentsScan`. Only with approval, use `"$STACK/scripts/ezy" dev link <plugin-name> --dir "$NATIVE_DIR" -m admin-plugin,web-plugin` with the modules that actually need it. This can download, install, and activate missing dependencies. See [linking a plugin](https://youngmonkeys.org/ezyplatform/guides/link-a-plugin?lang=vi).

## 3. Implement a complete slice

1. **Schema and Java:** Use JPA entities and EzyData repositories (for example, `@EzyRepository` and `EzyDatabaseRepository`), plus SDK services and policies. Sequence writes as DTO → validate → authorize → transaction → response DTO. Scope access in queries, index actual filters, and reuse core User identities when appropriate. See [EzyPlatform research](../../docs/research/ezyplatform-deep-research.md).
   - Annotate every custom repository type with `com.tvd12.ezyfox.database.annotation.EzyRepository`, including concrete transactional repositories; otherwise the bean can be silently absent and dependent routes may not register.
   - Use `@EzyQuery` for joins, sorting, and projections; pass `Next` last for offset/limit. Do not assume generated write queries share a transaction: verify the pinned SDK's `EzyJpaRepository` and single-`EntityManager` path, and test rollback between writes. For rollback-critical writes use the core SDK pattern: a concrete `EzyJpaRepository`, one `EntityManager` from `databaseContext`, and explicit `EntityTransaction` commit/rollback. `@EzyTransactional` on an ordinary service method did not roll back in the pilot. See [EzyData](../../docs/research/youngmonkeys/ezydata.md).
   - Verify package scanning and the configuration → bean → after-config order with a startup test. Keep request state out of injected runtime services and do not create a standalone plugin context. See [EzyFox Bean](../../docs/research/youngmonkeys/ezyfox-library.md).
2. **Migration:** Put plugin-prefixed SQL in `<project>-admin-plugin/src/main/resources/scripts/`; see the [example SQL](https://github.com/youngmonkeys/ezyplatform-examples/tree/main/personal/personal-admin-plugin/src/main/resources/scripts). Scripts are applied once by filename. Keep released files unchanged and add a file for each change. Test fresh installs and upgrades; do not assume automatic rollback or that Web-only plugins run Admin migrations. Back up DB and runtime before changes to environments containing data; use expand–migrate–contract for incompatible changes.
3. **Admin:** Define menus in `menus.properties` and use the example convention for hidden detail routes. Place templates under `templates/<project>/` and return a `View` from an EzyHTTP controller. Verify the actual plugin prefix. Use `@Authenticated`, `@AdminId`, and `@EzyFeature` for Admin permissions; hiding UI controls is not server-side authorization. See [Admin pages](https://youngmonkeys.org/ezyplatform/guides/create-an-admin-page?lang=vi) and [menus](https://youngmonkeys.org/ezyplatform/guides/create-menus-for-admin-plugin?lang=vi).
   - Use fragments and `ViewDecorator` to extend layout rather than editing core templates. For example, a toolbar uses `rightToolbarToolFragments` and renders the `content` region; still protect its API. See [Admin toolbar](https://youngmonkeys.org/ezyplatform/guides/add-admin-right-toolbar-tool?lang=vi).
4. **Web:** Use `@UserId` after verifying that the Web auth interceptor covers your route. Namespace views and use Thymeleaf/fragments or the active theme's extension points. Scope service access by user and resource, including downloads, searches, and counts. Do not grant Admin permissions to members. Test anonymous requests, wrong roles, out-of-scope resources, valid members, and revoked access. Remember Admin cookies must not authenticate Web-member routes. For multipart media endpoints use `@Async` and declare `accept="multipart/form-data"` on upload; resource download also needs `@Async`. Docker dev Web has `resources.upload.enable=false` by default in `web/settings/config.properties`; enable it only in the local dev runtime when testing uploads. See [Web authentication](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-web-authentication?lang=vi), [permissions](https://youngmonkeys.org/ezyplatform/guides/permission-in-ezyplatform?lang=vi), and [themes/plugins](https://youngmonkeys.org/ezyplatform/guides/understanding-ezyplatform-themes-and-plugins?lang=vi).
   - Bind DTOs from path/query/body; return `View` for HTML and a DTO or `ResponseEntity` for APIs. Confirm unauthorized requests do not reach business handlers. Defer Socket until after the HTTP MVP, then test subscription, reconnect, and fan-out permissions. See [EzyHTTP](../../docs/research/youngmonkeys/ezyhttp.md) and [EzyFox Server](../../docs/research/youngmonkeys/ezyfox-server.md).
5. **i18n and static assets:** Put menu labels, form errors, and default strings in `messages/messages.properties`; add `messages_vi.properties` and other required locales. Use keys in templates and expose only the keys JS needs. `static/` is accessible via HTTP, so never store secrets there. See [multilingual support](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-multi-languages?lang=vi).

## 4. Verify, export, and check the ZIP

From the plugin repo, review Maven profiles and test database endpoints; use only a dev database. Run the test suite separately because export profiles may skip tests. Read the generated export script and use the ZIP path printed by export:

```bash
"$STACK/scripts/ezy" dev run --dir "$NATIVE_DIR" -- mvn clean verify
"$STACK/scripts/ezy" dev run --dir "$NATIVE_DIR" -- bash export.sh
ZIP=target/project/example-plugin-1.0.0.zip
python3 "$STACK/scripts/ezy-plugin.py" check-zip "$ZIP"
```

The [example export script](https://github.com/youngmonkeys/ezyplatform-examples/blob/main/book-store/export.sh) runs Maven module builds followed by `ezy.sh package` and `ezy.sh export`. This writes to the **native** runtime without implicitly activating or restarting modules. To package without writing to that runtime, run the generated Maven steps and `ezy.sh package`, stopping before `ezy.sh export`. Do not package before building Maven artifacts. The alternative `ezy dev export` **activates native modules and restarts by default**, which can change the active theme; use it only if wanted in a sandbox. See [SDK package/export commands](https://youngmonkeys.org/ezyplatform/guides/ezyplatform-sdk-commands?lang=vi).

The ZIP helper checks integrity and rejects bundled EzyPlatform core JARs, including `ezyplatform-*-sdk`. Also inspect module types and versions, expected templates/messages/SQL, and the absence of test configuration, secrets, or files overriding platform configuration. Record the artifact path, version, and SHA-256 before installing it in Docker.

## 5. Install your artifact in Docker dev

1. From the stack repo, follow the [README](../../README.md) and run `./scripts/up.sh`. For a fresh runtime, create a super admin at <http://127.0.0.1:9090/setup-admin>, then sign in at `/login`. The default Web URL is <http://127.0.0.1:8080/>; use the printed URL if you changed ports. Do not use production Admin.
2. In Admin, go to **Plugins → Add New → Upload** and select your project ZIP. Check the name/version, then **Activate** each intended module (for example, Admin and Web). Verify the action has changed to **Deactivate**; follow any **Apply** prompt before continuing. Use the signature-checked Marketplace workflow for third-party plugins instead. `cli.sh "install <name>"` searches the Marketplace; it does not install a local ZIP. Do not copy JARs into the volume or modify installed plugins directly.
3. Once activation is saved, use the platform **Apply** flow when prompted. Uploading a ZIP alone does not apply it, and a plain `docker compose restart ezyplatform` is not a substitute for Apply. For a versioned upgrade, `python3 scripts/ezy-plugin.py upload-apply <zip> --password-file <local-secret-file>` performs the verified upload/check-dependencies/platform-install API sequence. Application is asynchronous: poll the installed module version, route registrations, migration schema, and plugin smoke routes. Verify the actual Admin menu/view, actual Web route, schema, and data. HTTP 200 on the default home page only shows the core is up. See [installing and activating a plugin](https://youngmonkeys.org/ezyplatform/guides/add-a-plugin-to-your-ezyplatform?lang=vi) and the [37-plugin test report](../../docs/plugins/test-report.md#thứ-tự-phụ-thuộc-đáng-lưu-ý): check dependencies and migration logs/schema before concluding that Web works.

On a first boot, Web `/` can temporarily return 404 even after Admin is ready. Wait for `up.sh` to finish its readiness and restart checks; see the [README](../../README.md). This differs from a plugin route that still returns 404 after activation and restart. Compose starts only Admin/Web by default; enable and start Socket separately if your project uses it, and test the Socket connection and protocol directly.

## 6. Troubleshoot, upgrade, and release

| Symptom | First checks |
| --- | --- |
| Missing parent/Test SDK or `systemPath` | Run `ezy dev check --dir …` and verify JDK/Maven/SDK, native paths, and JAR versions. `ezy dev sync-versions --dir …` updates versions of **installed** dependencies; review the diff and do not upgrade core automatically. |
| Missing menu/JS/i18n or route 404 | Check ZIP, active module type/version, route and menu prefixes, template namespaces, and assets/messages. For IDE `*StartupTest` runs use the module as working directory and avoid runtime port conflicts. |
| 401/403 or absent Web user ID | Check interceptor/theme and annotations. Retest with and without access; do not bypass authentication. |
| Startup, database, class, or linkage errors after install | Check Admin/Web logs, migrations, `dependencies`, versions, and duplicate core JARs. Do not delete volumes to fix data. See [build/export troubleshooting](https://youngmonkeys.org/ezyplatform/guides/nhung-ly-do-khien-ban-khong-the-build-chay-va-export-duoc-du-an-plugin-ezyplatform?lang=vi). |

For native diagnostics, use `"$STACK/scripts/ezy" dev <command> --dir "$NATIVE_DIR"`:

- `status` shows URLs, Admin/Web status, and active modules; see also `$NATIVE_HOME/logs/{admin,web}-server.log`. `restart` restarts native Admin/Web, not Compose.
- `tables core` or `tables <plugin-name>` lists SQL definitions, not the migrated database schema.
- `find-class <class-name>` locates a class in a JAR. Use `decompile <qualified-name-or-JAR-path>` only for local artifacts you are authorized to inspect; prefer public SDK/source and do not copy decompiled code into a plugin.

**Local upgrades:** Bump the bundle version; uploading a changed same-version ZIP can return success without replacing installed JARs. Test fresh install and upgrade with sample data, and back up DB/runtime. In Admin, choose **Update Manually**, upload the new ZIP, and **Apply** as described in the [upgrade guide](https://youngmonkeys.org/ezyplatform/guides/update-a-plugin?lang=vi); the pilot did not require deactivate/delete/upload/activate once Apply was invoked. Check version, schema, and permissions. An image rebuild does not replace plugins stored in an existing runtime volume. Rolling back the artifact does not roll back migrations; restore the verified DB/runtime pair if incompatible. Follow the end-to-end [plugin lifecycle verification recipe](../../docs/plugins/pilot-verification.md), including auth/theme, transaction, media revocation, notification semantics, and isolated restore evidence.

**Marketplace:** Publish only when requested and authorized; obtain separate approval before each write. Read the [FAQ](https://ezyplatform.com/faq) and `ezy-market-submit` or `ezyplatform-market-submit`. Check Java 8 compatibility, locales, asset licenses, reserved namespaces, bundle size/content, and server limits. Prepare icon/banner, metadata, release notes, and `<url-name>-<X.Y.Z>.zip`. Run each wrapper command via `"$STACK/scripts/ezy"`: `market login` (user approves in their browser) → `market projects` / `market categories` → `market create --json …` if needed → `market upload-version --name … --version … --zip … --notes-file …` → `market status --name …` → `market release --name …` **only after** status is `RELEASABLE` and release is approved.

If source is required, submit only an authorized copy via `market upload-source --name … --version … --zip … --notes-file …` as `<url-name>-<version>-sources.zip`. Document installation, configuration, permissions, and upgrades in project Docs (`/account/projects/<url-name>/docs`). The CLI stores its token in `~/.ezyplatform/credentials.json`; keep that file, tokens, passwords, cookies, and database dumps out of logs, ZIPs, and Git. This workflow does not require logging in or publishing.

### Handoff checklist

- [ ] Separate plugin repo; correct modules, dependencies, and versions; commands use the correct native or Docker environment.
- [ ] Domain, cross-scope permissions, fresh migrations, and upgrades tested; not just build success or home-page availability.
- [ ] Clean ZIP and correct installed version in the sandbox; Admin, Web, i18n, logs, and rollback checked.
- [ ] Report artifact path, version, SHA-256, evidence, and anything unverified. Publish only with separate approval.
