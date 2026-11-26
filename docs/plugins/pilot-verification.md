# Plugin lifecycle verification recipe

This is the stack's generic pilot recipe for proving that a newly written Java plugin really works in the Docker development runtime. It is not enough to build the ZIP, install a Marketplace plugin, or open the core home page.

The reference run used a fresh clone of this stack, EzyPlatform 1.5.9, EzyArticle 1.5.6, Docker container Java 11, MySQL 8.0, native JDK 8/Maven/SDK 0.2.8, and a disposable probe plugin named `stack-probe`. The final probe ZIP was `stack-probe-1.1.3.zip` with SHA-256 `71a63fa4322a4e9b48dfa2c9aebf233e8c8d8fcaf6457aa049046f85f51772a5`. Substitute your own project name, versions, checksums, users, and ports.

## Evidence the recipe must produce

| Area | Passing evidence from the reference run |
| --- | --- |
| Native build and export | `mvn clean verify` passed, `bash export.sh` produced the ZIP, and `scripts/ezy-plugin.py check-zip` passed. |
| First install | Admin upload plus activation installed the Admin/Web modules; initial SQL created the plugin table. |
| Versioned upgrade | Uploading a **new version** and explicitly applying it replaced the installed JARs and ran the new migration. Existing rows survived. |
| Same-version upload | Uploading a changed ZIP with the same version returned success but did not replace installed JARs. Always bump the version. |
| Web authentication | Anonymous and Admin-cookie requests to the protected Web API returned 401; an activated Web user returned 200 with its Web user id. Admin identity did not substitute for Web identity. |
| Theme wiring | Anonymous/Admin-cookie access to the protected page redirected to `/login`; the signed-in Web user stayed on the page and rendered the probe marker inside the active Freestyle layout, with no core template edits. |
| Transaction rollback | A manual transaction using a concrete `EzyJpaRepository`, one `EntityManager`, and `EntityTransaction` committed on success and rolled back on failure. `@EzyTransactional` on a service method did **not** roll back in the probe. |
| Private media | The owner downloaded private media with 200 and exact bytes. Another user received 404, anonymous and Admin-cookie requests received 401. Granting then deleting a grant row changed the other user's result from 404 to 200 and back to 404. |
| Notifications | Two calls with the same probe key created two notification rows and two receiver rows. There is no built-in idempotency/deduplication key, retry, after-commit, or outbox guarantee in the synchronous service path. |
| Backup/restore | A matched MySQL dump plus runtime-volume archive restored the plugin version, schema/data, Web auth, and private media file in an isolated Compose sandbox. Reinstalling an old ZIP alone is not a database restore. |

## 1. Build and inspect the artifact

Follow `skills/ezy-build-plugin/SKILL.md` for native setup and scaffolding. From the plugin project:

```bash
"$STACK/scripts/ezy" dev run --dir "$NATIVE_DIR" -- mvn clean verify
"$STACK/scripts/ezy" dev run --dir "$NATIVE_DIR" -- bash export.sh
ZIP=target/project/example-plugin-1.0.0.zip
python3 "$STACK/scripts/ezy-plugin.py" check-zip "$ZIP"
sha256sum "$ZIP"
```

Record the plugin revision, stack revision, SDK/runtime versions, ZIP version, and SHA-256 in the verification note.

## 2. Include minimum probe slices

A pilot does not need business features. It needs one vertical slice for each platform capability the real plugin will depend on.

### Repository and transaction slice

Annotate every custom repository type with `com.tvd12.ezyfox.database.annotation.EzyRepository`. This applies both to an interface extending `EzyDatabaseRepository` and to a concrete transactional repository. Without the annotation the bean can be silently absent, causing dependent controllers/routes not to register.

For rollback-critical writes, use the core SDK pattern: a concrete repository extending `EzyJpaRepository`, create one `EntityManager` from `databaseContext`, begin an `EntityTransaction`, write, then commit or roll back in `try/catch/finally`. Test both paths over HTTP:

- success returns 200 and row count 1;
- induced failure returns 500 and row count 0.

Do not treat `@EzyTransactional` on an ordinary service method as proof of rollback.

### Web auth and theme slice

Expose one public API, one `@Authenticated` API using `@UserId`, one public page, and one `@Authenticated` page. Render pages through the active theme contract (for Freestyle the probe used `layout:decorate="~{ezytheme}"`). Verify:

1. public API: anonymous 200;
2. protected API: anonymous 401, signed-in Web user 200 with correct user id, Admin cookies 401;
3. public page: anonymous 200 and the probe marker;
4. protected page: anonymous and Admin cookies redirect to `/login`; signed-in Web user renders the marker and user id in the active theme.

A 200 status alone is not enough for page tests because the login page also returns 200. Check the final URL or page marker.

### Migration slice

Put plugin-prefixed SQL files in the Admin module's `src/main/resources/scripts/`. Scripts run once by filename. Never edit a released migration; add a new file. In the pilot, prove:

1. fresh install creates the table;
2. a versioned upgrade adds a new column/table;
3. rows written before the upgrade survive;
4. a restart does not rerun the same filename;
5. a failed test transaction rolls back independently of migrations.

The reference restart check used `ezy_run_script_histories`: four `stack-probe` rows before and after `docker compose restart ezyplatform`, with every filename count exactly 1. The generic evidence query is:

```sql
SELECT script_name, COUNT(*)
FROM ezy_run_script_histories
WHERE module_name = '<plugin>'
GROUP BY script_name;
```

Admin readiness is not proof that migration SQL ran. Inspect the database schema, this migration history, or a migration-specific read model.

### Private media slice

Multipart upload/download endpoints need `@Async`; upload also needs the multipart accept declaration, for example:

```java
@Async
@Authenticated
@DoPost(value = "/upload", accept = "multipart/form-data")
```

The generated Docker Web configuration currently sets `resources.upload.enable=false` in `web/settings/config.properties`. For a local dev media probe, set it to `true` in the dev runtime volume and restart/apply the runtime. Do not commit runtime volumes or secrets.

Use `MediaControllerService` with `notPublic=true` and a caller-supplied predicate. The service intentionally does not hard-code business authorization. The reference predicate allowed the owner or an explicit grant row. Verify owner 200, other user 404, anonymous 401, then grant → other user 200, revoke grant → other user 404. This proves revocation is evaluated on each request rather than cached at upload time.

### Notification slice

`NotificationService.addNotification` synchronously writes notification and receiver rows. The reference run confirmed creation, but repeated identical keys produced duplicate rows. If a plugin needs exactly-once or retried delivery, it must add its own idempotency key/state machine/outbox/after-commit integration and test duplicate submission, retry, restart, and rollback behavior. Do not claim retry or deduplication from the core service.

## 3. Install and apply the ZIP in Docker dev

Start the stack with `./scripts/up.sh`, create the local super admin, and install any declared Marketplace dependencies. For upgrades, bump the bundle version before exporting. Use the helper to upload the project without copying JARs into volumes:

```bash
python3 "$STACK/scripts/ezy-plugin.py" upload-apply "$ZIP" \
  --admin-url http://127.0.0.1:9090 \
  --username admin \
  --password-file /secure/local/admin-password-file
```

The helper checks the ZIP, logs in through the Admin form, uploads the project, and checks dependencies. If none of the project's modules are active, it activates all reported module types and requests a restart. If you want to activate only some module types on a first install, use the Admin UI instead. For projects with active modules, the helper retains the existing platform Apply flow. Store the password only in a local secret file outside Git.

Application is asynchronous. Poll all of these before declaring success:

- `web/plugins/<project>/module.properties` and `admin/plugins/<project>/module.properties` show the new version;
- old duplicate JARs are gone or inactive and expected new JARs are installed;
- startup logs registered the expected routes;
- migration schema/data changed as expected;
- plugin smoke APIs/pages return the expected results.

A plain `docker compose restart` after upload is not a substitute for the platform Apply/install step. Conversely, the reference versioned upgrades did not require deactivate/delete/upload/activate once Apply was invoked.

## 4. Rehearse backup and restore in an isolated sandbox

Back up the database and the runtime volume as a matched pair while the system is in a known state. Backups contain password hashes, tokens, uploaded private media, and runtime configuration. Write them outside the Git checkout in a private directory; never commit or attach them. Example for the dev Compose project:

```bash
BACKUP_DIR="$HOME/ezyplatform-backups/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR" && chmod 700 "$BACKUP_DIR"
MYSQL_ROOT_PASSWORD="$(docker compose exec -T mysql printenv MYSQL_ROOT_PASSWORD)"

docker compose exec -T mysql mysqldump -uroot -p"$MYSQL_ROOT_PASSWORD" \
  --single-transaction --routines --triggers ezyplatform > "$BACKUP_DIR/ezyplatform-db.sql"

docker run --rm \
  -v <project>_ezyplatform-data:/data:ro \
  -v "$BACKUP_DIR:/backup" \
  alpine sh -c 'tar czf /backup/ezyplatform-runtime.tar.gz -C /data .'
```

Use a separate copy of the checkout and different published ports for the restore sandbox. Do not overwrite or delete the source volumes. In the empty sandbox:

1. create a new empty runtime volume and extract the runtime archive before first platform start;
2. start only MySQL and wait for health;
3. load the SQL dump;
4. start EzyPlatform;
5. verify the same plugin version, rows, routes, login behavior, and media bytes.

The reference restore proved that media metadata and the physical media file both require the matched DB/runtime pair. Rolling back or reinstalling a ZIP does not roll back already-applied SQL.

## 5. Acceptance checklist

- [ ] Fresh clone revision, runtime/SDK versions, plugin revision, ZIP version, and SHA-256 recorded.
- [ ] Native tests/build/export pass and the ZIP passes `check-zip`.
- [ ] First install and at least one versioned upgrade verified after explicit Apply.
- [ ] Public/protected API and page matrix verified for anonymous, signed-in Web user, and Admin-cookie-on-Web.
- [ ] Fresh migration, upgrade migration, data survival, restart/non-rerun, and transaction rollback verified in the database.
- [ ] Private media owner/other/anonymous/revocation matrix verified when media is required.
- [ ] Notification delivery semantics documented; no retry/dedup claimed unless implemented and tested by the plugin.
- [ ] Matched DB/runtime restore rehearsed in an isolated sandbox before relying on rollback.
