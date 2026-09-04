# R-08 Secret Rotation & History Scrub — Runbook

Status: ROTATION DONE @ current tree (guard tests enforce). HISTORY SCRUB PREPARED,
NOT EXECUTED — it requires a quiesced repo (all writers stopped) and a coordinated
force-push, which cannot be done safely while parallel actors are committing.

## What was rotated (current tree)

| Secret | Old value (leaked) | Action |
|---|---|---|
| Keycloak operator password | `operatorpass` | rotated in `infra/keycloak/realm-export.json` |
| Keycloak citizen password | `citizenpass` | rotated in `infra/keycloak/realm-export.json` |
| Dashboard direct-grant password | hardcoded `citizenpass` | removed; build reads `NEXT_PUBLIC_CITIZEN_PASSWORD` |
| TLS private key | tracked `infra/nginx/certs/key.pem` | untracked + gitignored (`cert.pem` public cert remains) |
| Grafana admin password | `orion_admin` | env-driven `${GRAFANA_ADMIN_PASSWORD}` |
| Audit/chaos script creds | inline passwords | read `ORION_OPERATOR_PASSWORD` / `ORION_CITIZEN_PASSWORD` from env |

Guard tests: `tests/test_no_secrets.py`
(forbidden literals, no tracked private keys, no embedded direct-grant passwords).

## Local dev setup after rotation

```bash
cp .env.example .env
# then set in .env (untracked):
#   ORION_OPERATOR_PASSWORD / ORION_CITIZEN_PASSWORD
#   → copy values from infra/keycloak/realm-export.json
#   NEXT_PUBLIC_CITIZEN_PASSWORD → same as ORION_CITIZEN_PASSWORD
```

Keycloak imports the realm ONLY on first boot with an empty database.
Existing volumes keep OLD passwords: recreate with
`docker compose down -v && docker compose up -d` (destroys local dev data).

## History scrub (prepared, requires quiesced repo)

Tool: `scripts/security/scrub_history.py`

1. Stop ALL writers (humans, agents, CI). Confirm `git status --porcelain` empty.
2. `pip install git-filter-repo`
3. Dry run: `python scripts/security/scrub_history.py`
4. Execute: `python scripts/security/scrub_history.py --execute`
5. Follow printed steps: re-add origin, `git push --force-with-lease origin main`,
   everyone re-clones.
6. GitHub caveat: forks/caches/PR refs may retain old blobs → contact support to
   purge if the repo was ever public, and treat all previously pushed secrets as
   COMPROMISED FOREVER regardless of scrub.

## Non-negotiable follow-ups

- Treat every secret that ever reached `origin` as burned: rotate at the provider
  (Postgres users, Keycloak realm import secrets, TLS keypair re-issue), not just
  in git.
- Production must never rely on tracked realm files: inject credentials from a
  secret manager at deploy time.
