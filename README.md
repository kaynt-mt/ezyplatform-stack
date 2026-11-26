# EzyPlatform Core Stack

A shared foundation for developing multiple EzyPlatform apps, not a landing page app. The stack includes EzyPlatform **1.5.9**, EzyArticle **1.5.6** already active, Java 11 in the container, and MySQL 8.0. The runtime builds from CPPAI's Dockerfile; the ezy CLI, CPPAI agent plugin repository, and Young Monkeys public skill packages are pinned in `upstream.lock.json`.

New team? [Create your own core repository from this template and set up Devin Bots](docs/template-setup.md). Neither Devin nor AgentKit is required to run the core.

## Start on a development machine or cloud VM

Requires Git, Bash, curl, Python 3.9+, and Docker Engine or Docker Desktop with Docker Compose v2.17+. The Docker runtime does not require Java or MySQL on the host. The EzyPlatform image runs on `linux/amd64`; ARM hosts need amd64 emulation. The first run needs internet access to fetch source, releases, and base images.

```bash
./scripts/up.sh
```

On a fresh clone, start the runtime with `up.sh` first, then run the full sync in the [CLI and skills section](#cli-plugins-and-skills-for-agents). Startup already syncs the pinned Docker source and CLI. Full sync populates `.agents/skills/`, which is absent in a fresh clone. If both commands are started in the same checkout concurrently, their sync operations wait for the same file lock.

| Service | Default address |
|---|---|
| Admin | <http://127.0.0.1:9090/login> |
| First super admin setup | <http://127.0.0.1:9090/setup-admin> |
| Web | <http://127.0.0.1:8080/> |
| MySQL | `mysql:3306` on the Compose network; not published on the host |

**There is no default Admin account or password.** Open `/setup-admin`, create a super admin, then sign in at `/login`. Startup generates random database passwords in `.env`; do not commit, share, or replace it while using the same MySQL volume.

On first startup, Web `/` can temporarily return HTTP 404 while Admin is available. Wait for `up.sh` to finish its readiness checks and, if needed, restart EzyPlatform once. After recovery, a fresh core without a custom theme can show a default welcome page; that page does not verify that a plugin has loaded.

### Docker Hub rate limits

External runtime images are digest-pinned. `up.sh` uses a local image when present, otherwise probes Docker Hub before building. If Docker Hub cannot serve a pinned image (for example HTTP 429 on a shared egress IP), that run uses the same digest from Google Cloud's `mirror.gcr.io` cache. The digest is unchanged, so the image content is the same. Set `MYSQL_IMAGE`, `PYTHON_BASE_IMAGE`, or `ECLIPSE_TEMURIN_BASE_IMAGE` before `up.sh` to use an approved internal mirror instead; user-supplied values are never rewritten.

On a VM, ports bind to loopback only. Open a tunnel from your machine (replace `user@vm` with the VM's SSH address), then visit the URLs above:

```bash
ssh -N -L 9090:127.0.0.1:9090 -L 8080:127.0.0.1:8080 user@vm
```

Set `EZY_ADMIN_PORT` or `EZY_WEB_PORT` in `.env` if a host port is taken, or override them for one run:

```bash
EZY_ADMIN_PORT=19090 EZY_WEB_PORT=18080 ./scripts/up.sh
```

Use the URLs printed by `up.sh`. For an actual deployment, configure HTTPS and Admin access controls at a separate reverse proxy; do not expose the Admin port directly to the internet.

```bash
docker compose ps
docker compose logs -f ezyplatform mysql
docker compose stop   # retain data
./scripts/up.sh       # start again
```

Compose stores the database and runtime in separate volumes. Back up both before upgrading; rebuilding the image does not replace core or modules in an existing runtime volume. `docker compose down -v` **deletes** all local data; use only when deliberately starting over.

Run the stack tooling tests from the repository root:

```bash
python3 -m unittest discover -s tests -v
```

## CLI, plugins, and skills for agents

The [catalog of 19 Ezy skills](skills/README.md) explains when to use each skill. All 19 upstream copies are tracked in [`skills/upstream/`](skills/upstream/) for reading on GitHub; the agent copies are synced to `.agents/skills/`.

```bash
python3 scripts/sync-upstream.py --skip-agentkit
./scripts/ezy --version
```

The CLIs run from pinned source or binaries in `.upstream/`, not from a global install. Sync fetches the [CPPAI Agents Plugins](https://github.com/cppai-vn/agents-plugins) repository and installs the pinned skills from that repository and the [EzyPlatform Skill Library](https://ezyplatform.com/ezyai/skill-library?lang=vi) into `.agents/skills/`.

- **EzyPlatform only:** The command above rebuilds the agent skill directory without AgentKit. It does not need an AgentKit account, key, or CLI.
- **Optional AgentKit:** Set your own licensed `AGENTKIT_API_KEY` in the environment and run `python3 scripts/sync-upstream.py --require-agentkit`. Sync exports the licensed `engineer` and/or `marketing` kit to the local `.upstream/agentkit/` cache and loads its `ak-*` skills into `.agents/skills/`. See the [optional setup and license boundaries](docs/template-setup.md#4-optional-add-agentkit).
- `.upstream/` and `.agents/skills/` are generated from the lock; do not edit them by hand. Choose **one** way to load skills per agent: the synced `.agents/skills/` directory or the marketplace described by the upstream README, not both. Application runtime plugins are separate from coding agent plugins: the stack includes EzyArticle; install or activate other modules as needed, not all marketplace modules by default.
- When an agent runs on another VM, configure the Admin URL via an authorized private connection rather than using another machine's loopback address.

See the [runtime plugin catalog](docs/plugins/README.md) and [sandbox installation procedure](docs/plugins/test-report.md) for Marketplace modules, and the [AgentKit workflow](docs/agentkit-workflow.md) for using the installed kits.

### Update upstream pins

1. Verify the desired revisions of the [CLI](https://github.com/cppai-vn/ezyplatform-cli), [Docker](https://github.com/cppai-vn/ezyplatform-docker), and [Agents Plugins](https://github.com/cppai-vn/agents-plugins) (for example, `git ls-remote https://github.com/cppai-vn/agents-plugins.git HEAD`), then update `git` in the lock.
2. Public skill catalog: <https://ezyplatform.com/api/v1/skill-library/skills?limit=100>. For each updated package, download it from `https://ezyplatform.com/api/v1/skill-library/skills/<id>/package`, inspect the contents and name in `SKILL.md`, then record the ZIP's SHA-256 in `skill_library`. Sync rejects changed packages without a matching checksum. After changing Ezy pins, run `python3 scripts/sync-upstream.py --refresh-ezy-skills`, review the diff, and commit `skills/upstream/` with the lock. This command does not touch AgentKit or `.agents/skills/`.
3. To upgrade AgentKit, list versions using `./scripts/ak kit list-kits --json` and update `agentkit.cli_version` / `agentkit.kits` in `upstream.lock.json`. Do not run `ak self-update` on the pinned launcher.
4. When changing Docker or an EzyPlatform/EzyArticle version, update the build arguments and image tag in `compose.yaml`. Check whether the upstream Dockerfile changed its base images; update the matching `additional_contexts` keys and digest-pinned defaults when it does (`docker buildx imagetools inspect <image>` prints the current digest). Test with new volumes before planning an upgrade of volumes containing data.
5. Run `python3 scripts/sync-upstream.py --skip-agentkit` to apply the EzyPlatform pins and verify `./scripts/ezy`, Admin, and Web. For AgentKit changes, also run the licensed sync and verify `./scripts/ak` and the updated kit.

## Create an application on the core

Keep application source in a separate repo; this stack provides the runtime and toolkit. To create a content project and reuse a running Admin, use CLI `live` mode, which means **connect to an existing Admin**, not necessarily production:

```bash
STACK="$PWD"  # Run from the stack checkout.
"$STACK/scripts/ezy" new ../my-app --mode live --admin-url http://127.0.0.1:9090
cd ../my-app
# Reveal the Access Token at /admins/me and enter it in environment.json privately.
"$STACK/scripts/ezy" check
```

For an independent content sandbox, run `./scripts/ezy new ../my-local-app --mode local` from the stack checkout. This starts the pinned CLI's own Compose project, which currently defaults to `cppai/ezyplatform-app:1.5.4`. Use its printed URLs, create the first Admin, and enter its token before running `check` from the generated project. To test against this stack's 1.5.9 runtime, use `--mode live` against the local core started by `./scripts/up.sh`.

For a Java plugin, use the stack's scaffold helper in the [plugin build skill](skills/ezy-build-plugin/SKILL.md), not `ezy new`. The skill covers native builds, packaging, and testing on Docker dev. Do not commit `environment.json`, tokens, or passwords.

Resources: [EzyPlatform Guide](https://youngmonkeys.org/projects/ezyplatform?tab=guide) · [FAQ](https://ezyplatform.com/faq) · [Blog index and background for agents](docs/research/ezyplatform-blogs/README.md).
