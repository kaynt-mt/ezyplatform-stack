# EzyPlatform Core Stack

A shared stack for developing multiple EzyPlatform applications, not a single landing-page app. It includes EzyPlatform **1.5.9**, EzyArticle **1.5.6** already activated, Java 11 in the container, and MySQL 8.0. The runtime is built from CPPAI's Dockerfile. The ezy CLI, CPPAI agent plugin repository, and public Young Monkeys skill packages are pinned in `upstream.lock.json`.

## Getting started on a development machine or cloud VM

Requires Git, Bash, curl, Python 3.9+, and Docker Engine or Docker Desktop with Docker Compose V2. Java and MySQL are not required on the host. The EzyPlatform image runs on `linux/amd64`; ARM machines need amd64 emulation. The first run needs Internet access to fetch source code, releases, and base images.

```bash
./scripts/up.sh
```

| Service | Default address |
|---|---|
| Admin | <http://127.0.0.1:9090/login> |
| First-time super admin setup | <http://127.0.0.1:9090/setup-admin> |
| Web | <http://127.0.0.1:8080/> |
| MySQL | `mysql:3306` on the Compose network; no port exposed to the host |

**There is no default Admin account or password.** Open `/setup-admin`, create your super admin, and use that account at `/login`. The startup command generates a random database password in `.env`. Do not commit or share that file, or replace it while reusing the existing MySQL volume.

On a VM, the ports bind only to loopback. From your machine, open a tunnel (replace `user@vm` with the VM's SSH address), then visit the URLs above:

```bash
ssh -N -L 9090:127.0.0.1:9090 -L 8080:127.0.0.1:8080 user@vm
```

Set `EZY_ADMIN_PORT` or `EZY_WEB_PORT` in `.env` if a host port is already in use. For deployments, configure HTTPS and Admin access at a separate reverse proxy; do not expose the Admin port directly to the Internet.

```bash
docker compose ps
docker compose logs -f ezyplatform mysql
docker compose stop   # keep data
./scripts/up.sh       # start again
```

Compose stores the database and runtime in two volumes. Back up both before upgrading; building a new image does not replace the core or modules in an existing runtime volume. `docker compose down -v` **deletes** all local data. Use it only when you deliberately want to start from scratch.

## CLI, plugins, and agent skills

The [catalog of 19 Ezy skills](skills/README.md) explains when to use each skill. All 19 upstream copies are checked in under [`skills/upstream/`](skills/upstream/) for browsing on GitHub. The copies used by agents are still synced into `.agents/skills/`.

```bash
python3 scripts/sync-upstream.py
./scripts/ezy --version
./scripts/ak --version
```

The CLI runs directly from the pinned source or binary in `.upstream/`, without a global install. The sync command fetches the entire [CPPAI Agents Plugins](https://github.com/cppai-vn/agents-plugins) repository into `.upstream/agents-plugins/` and installs skills from that repository and the [EzyPlatform Skill Library](https://ezyplatform.com/ezyai/skill-library?lang=vi) into `.agents/skills/`. It also downloads the pinned [AgentKit](https://docs.agentkit.best/en/stable/getting-started/quickstart) kits (`engineer` and `marketing`, exported in `portable` format) into `.upstream/agentkit/` and loads all `ak-*` skills into `.agents/skills/`.

- **AgentKit authentication:** Set the `AGENTKIT_API_KEY` environment variable, or run `./scripts/ak login` once. Credentials are stored in `~/.agentkit/`, not in the repository. Use `--require-agentkit` to fail the sync when authentication is missing or `--skip-agentkit` to sync only EzyPlatform.
- `.upstream/` and `.agents/skills/` are regenerated from the lock file; do not edit them directly. Choose **one** way to load skills per agent: the synced `.agents/skills/` directory or the marketplace as described in the upstream README, not both. Application runtime plugins are separate from coding-agent plugins. The stack includes EzyArticle; install and activate additional modules as the application needs them rather than enabling every marketplace module by default.
- If the agent runs on another VM, configure the Admin URL through an authorized private connection. Do not use another machine's loopback address.

### Updating pinned versions

1. Check the desired commits for the [CLI](https://github.com/cppai-vn/ezyplatform-cli), [Docker](https://github.com/cppai-vn/ezyplatform-docker), and [Agents Plugins](https://github.com/cppai-vn/agents-plugins) (for example, `git ls-remote https://github.com/cppai-vn/agents-plugins.git HEAD`), then update `git` in the lock file.
2. Public skill catalog: <https://ezyplatform.com/api/v1/skill-library/skills?limit=100>. For each updated package, download it from `https://ezyplatform.com/api/v1/skill-library/skills/<id>/package`, check the contents and the name in `SKILL.md`, then record the ZIP archive's SHA-256 in `skill_library`. The script rejects a changed package unless its checksum has been updated. After changing Ezy pins, run `python3 scripts/sync-upstream.py --refresh-ezy-skills`, review the diff, and commit `skills/upstream/` together with the lock file. This command does not touch AgentKit or `.agents/skills/`.
3. To upgrade AgentKit, check the new versions via `./scripts/ak kit list-kits --json` and update `agentkit.cli_version` and `agentkit.kits` in `upstream.lock.json`. Do not run `ak self-update` directly on the pinned launcher.
4. When changing Docker or the EzyPlatform/EzyArticle version, update the build arguments and image tags in `compose.yaml`. Test with a fresh volume before planning upgrades for volumes that contain data.
5. Run `python3 scripts/sync-upstream.py --require-agentkit` to apply the lock file, then verify the CLI (`./scripts/ezy` and `./scripts/ak`), Admin, and Web.

## Creating a new application on the core

Keep application source code in a separate repository; this core provides the runtime and tools. For example, create a content project that reuses a running Admin instance (CLI `live` mode means **using an existing Admin instance**, not necessarily production):

```bash
./scripts/ezy new ../my-app --mode live --admin-url http://127.0.0.1:9090
cd ../my-app
# Get the access token from /admins/me in Admin and add it to environment.json.
../ezyplatform-stack/scripts/ezy check
```

To test with a separate database and containers for the app, use `ezy new --mode local` instead of connecting to the running core. To create a new Java plugin, use `ezy dev create`, not `ezy new`. See the [plugin build skill](skills/ezy-build-plugin/SKILL.md) for native build setup, packaging, and verification in the Docker development environment. Do not commit `environment.json`, tokens, or passwords.

Documentation: [EzyPlatform Guide](https://youngmonkeys.org/projects/ezyplatform?tab=guide) · [FAQ](https://ezyplatform.com/faq) · [Blog index and background for agents](docs/research/ezyplatform-blogs/README.md).
