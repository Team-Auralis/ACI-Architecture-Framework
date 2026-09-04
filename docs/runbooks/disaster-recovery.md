# Disaster Recovery Runbook

## Purpose

Back up and restore ORION PostgreSQL state while measuring recovery time objective (RTO).

## Scope

This runbook covers the Phase 1.5 backup/restore script `scripts/dr_backup_restore.py`. It does not replace a production managed backup service, secret manager, or point-in-time recovery plan.

## Required Environment

| Variable | Meaning |
|---|---|
| `DB_HOST` | PostgreSQL host. |
| `DB_PORT` | PostgreSQL port. |
| `DB_USER` | PostgreSQL user. |
| `DB_PASS` | PostgreSQL password supplied from secrets. |
| `DB_NAME` | Database name. Current local default is `keycloak`. |
| `BACKUP_DIR` | Destination directory for backup files. |

## Backup

```powershell
python scripts/dr_backup_restore.py --backup
```

Expected outcome:

- A timestamped custom-format dump is written to `BACKUP_DIR`.
- Runtime and backup size are printed.
- Failure output is captured in the incident or drill report.

## Restore Drill

Only run restore drills against a disposable or approved drill database.

```powershell
python scripts/dr_backup_restore.py --drill
```

The script runs `pg_dump`, waits briefly, then runs `pg_restore -c -1` and reports measured RTO.

## Production Restore Decision

Before restoring production:

1. Declare SEV-0 or SEV-1.
2. Stop API writes or suspend pilot.
3. Preserve the failed database for forensic review if corruption or intrusion is suspected.
4. Identify the exact backup artifact and checksum.
5. Get incident commander approval.
6. Restore.
7. Reconcile NATS/JetStream and outbox state before resuming writes.

## Post-Restore Validation

- API starts and connects to the restored database.
- Incident table row count matches expected restore point.
- Dispatch recommendations and asset states are sane.
- `outbox_events` does not contain stale unpublished rows that would replay unsafe actions.
- CHRONOS includes restore timing, operator, backup artifact, and reason.
- Pilot remains suspended until partner-agency safety checks complete.

## RTO/RPO Notes

- RTO is the measured restore time printed by the script.
- RPO is the age of the selected backup plus any unreplayed event-mesh gap.
- Accepted-but-unpublished events must be reconciled through `outbox_events` and NATS/JetStream before declaring recovery complete.

