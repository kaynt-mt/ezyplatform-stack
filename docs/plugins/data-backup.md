# data-backup

Data backups and scheduled snapshots.

- **Marketplace version on core 1.5.9:** `0.0.9`.
- **Verified modules:** `admin-plugin`.
- **Installation:** Passed. See the environment and general limitations in the [test report](test-report.md).

## Module map

| Lane / directory | Declared package | Declared runtime dependencies |
|---|---|---|
| `admin-plugin` — `admin/plugins/data-backup` | `org.youngmonkeys.databackup` | Not declared |

## HTTP, UI, and resources

The paths below come from annotations in the JAR. Mount prefixes and access permissions may differ by lane; the URLs that were actually called are listed in the testing section.

**admin-plugin** — 25 method/URI combinations identified; representative sample:

| Annotation HTTP | Class |
|---|---|
| `GET /settings` | `AdminSettingController` |
| `GET /backup-clients` | `AdminBackupClientController` |
| `GET /api/v1/realtime-backup/status` | `AdminApiRealtimeBackupController` |
| `GET /api/v1/realtime-backup/clients` | `AdminApiRealtimeBackupController` |
| `GET /api/v1/realtime-backup/database/tool-logs` | `AdminApiRealtimeBackupController` |
| `GET /api/v1/realtime-backup/database/privileges` | `AdminApiRealtimeBackupController` |
| `GET /api/v1/realtime-backup/platform-files/deletion-setting` | `AdminApiRealtimeBackupController` |
| `POST /api/v1/realtime-backup/database/snapshots` | `AdminApiRealtimeBackupController` |
| `POST /api/v1/realtime-backup/database/privileges` | `AdminApiRealtimeBackupController` |
| `POST /api/v1/realtime-backup/platform-files/delete` | `AdminApiRealtimeBackupController` |
| `POST /data-backup/api/v1/realtime-backup/client/ping` | `AdminApiRealtimeBackupClientController` |
| `PUT /api/v1/settings/s3` | `AdminApiDataBackSettingController` |
| `PUT /api/v1/settings/scheduler` | `AdminApiDataBackSettingController` |
| `PUT /api/v1/settings/ezyplatform-backup` | `AdminApiDataBackSettingController` |
| `PUT /api/v1/settings/platform-file-deletion` | `AdminApiDataBackSettingController` |
| `DELETE /api/v1/realtime-backup/clients/{clientId}` | `AdminApiRealtimeBackupController` |

- **admin-plugin – Menus (final keys and paths in menus.properties):** `data_backup: /`, `backup_clients: /data-backup/backup-clients`, `settings: /data-backup/settings`.

- **admin-plugin – Template:** `data-backup/backup-clients.html`, `data-backup/settings.html`.

## Data and migrations

- No occurrence of `CREATE TABLE` was found in the package’s standalone SQL files; this does not mean the module stores no data or does not use the core schema.

## JARs, configuration, and extension points

### admin-plugin

- **JARs inspected:** `data-backup-admin-plugin-0.0.9.jar`; 90 top-level classes after deduplicating by package and class name within the lane. The SDK can appear in multiple lanes.
- **Notable packages:** `org.youngmonkeys.databackup.admin.model`, `org.youngmonkeys.databackup.admin.response`, `org.youngmonkeys.databackup.admin.manager` (+14).
- **Controllers, services, and repositories (sample):** `AdminApiDataBackSettingController`, `AdminApiRealtimeBackupClientController`, `AdminApiRealtimeBackupController`, `AdminBackupClientController`, `AdminDataBackSettingValidator`, `AdminDataBackupSettingService`, `AdminPlatformFileDeletionValidator`, `AdminRealtimeBackupClientControllerService`, `AdminRealtimeBackupClientService`.
- **Configuration and permission classes (sample):** `AdminAwsS3ClientConfig`, `AdminEzyPlatformBackupDeletionSchedulerConfig`, `AdminRealtimeBackupConfig`.
- **Potential extension points based on class names:** `AdminAwsS3ClientManager`, `AdminDatabaseSnapshotS3Manager`, `AdminDatabaseToolLogManager`, `AdminDatabaseToolManager`, `AdminEzyPlatformBackupDeletionScheduler`, `AdminRealtimeAsyncResponseManager`, `AdminRealtimeBackupClientFileManager`, `AdminRealtimeBackupClientManager`, `AdminRealtimeBackupScheduler` (+8).

Classes and resources show that extension points are packaged; they do not establish API stability or confirm that every handler path has run.

## Sandbox observations

Admin `/data-backup/backup-clients` returned 200. Automatic backup failed because the application container lacked a MySQL or MariaDB CLI. Restoration was not tested.

## Integration notes

Separate scheduling, backup destinations, and operational configuration. Test restoration to another database; opening Backup Clients does not prove the backup is usable.

[Back to the plugin index](README.md)
