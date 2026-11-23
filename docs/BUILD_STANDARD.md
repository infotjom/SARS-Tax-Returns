# ERPNext Build Standard

**Applies to every ERPNext build, enhancement, report, print format, workflow, integration, website/Builder page, and upgrade.**

A build is not complete until the code, documentation, tests and deployment evidence are all in Git.

---

## 1. Definition of Done

Every change must satisfy all of these before merge or staging:

- [ ] Scope is written down (what changed and what did not).
- [ ] Code is built and tested in the dev site.
- [ ] Existing tests pass; new tests cover the change.
- [ ] User documentation reflects the new behaviour.
- [ ] Technical documentation reflects the design, configuration and limitations.
- [ ] Deployment/runbook is updated if install, migration, permissions, scheduler or backup behaviour changed.
- [ ] Demo/test workbook is updated with the exact transaction and expected result.
- [ ] README links to the current docs.
- [ ] Version/changelog is updated.
- [ ] Code and docs are committed on the same branch and released at the same tag.
- [ ] Staging is deployed from that exact Git commit.
- [ ] UAT evidence is recorded.
- [ ] Rollback path is known.

If any box is open, the build is not ready for staging.

---

## 2. Documentation set

Each app repo carries:

```text
docs/
├── BUILD_STANDARD.md
├── USER_MANUAL.md
├── TECHNICAL_MANUAL.md
├── STAGING_RUNBOOK.md
├── DEMO_TEST_WORKBOOK.md
└── exports/
    ├── <name>.pdf
    └── <name>.docx
```

### User manual

Written for the bookkeeper/accountant, not the developer.

Must include:

- who can do what (roles)
- exact navigation path
- field-by-field instructions
- example values
- expected result after saving/submitting
- what to do when it fails
- period-end and filing steps
- screenshots or annotated field lists

### Technical manual

Written for the implementer.

Must include:

- versions and dependencies
- architecture and data flow
- DocTypes, fields, hooks and permissions
- configuration values
- install and migrate commands
- backup and restore
- staging/cutover procedure
- troubleshooting and known limitations
- licence and upstream links

### Staging runbook

One page the implementer can follow without asking anyone:

- server/site details
- exact app versions and commits
- install order
- configuration checklist
- smoke tests
- backup/restore command
- rollback
- go/no-go criteria

### Demo/test workbook

One transaction per scenario:

- preconditions
- exact inputs
- expected document status
- expected ledger/report values
- pass/fail
- cleanup
- 15-minute showcase sequence

No test data is shipped in Git. The workbook creates the data live.

---

## 3. Repo and release rules

- **Source of truth:** Git, not a zip, desktop folder, Notion page or chat.
- **Branch:** `main` for releases, `develop` for integration, `staging` for UAT where used.
- **Tag:** every staging/production release has a version tag, e.g. `v0.1.0`.
- **Docs at the same commit:** docs are part of the release, not added later.
- **No secrets:** API keys, AWS credentials, passwords and private keys never enter Git.
- **No test data:** no database dumps, customer data or demo records in Git.
- **No generated caches:** `__pycache__`, `node_modules`, `.env`, local backups excluded.

A deployment is:

```text
Git commit/tag → staging checkout → install/migrate/build → smoke test → UAT
```

Never deploy from a local folder that does not match a Git commit.

---

## 4. Testing standard

Each scenario has:

1. **Given** — company, roles, configuration.
2. **When** — exact document, fields, values.
3. **Then** — expected status, ledger/report value, reconciliation.

Minimum before staging:

- Happy path for every new feature.
- One negative/validation path.
- Permission check.
- Cancellation/amendment path where applicable.
- Backup/restore test for data-affecting changes.
- Mobile/desktop check for website changes.

A screenshot or PDF is not proof of correctness. The expected numeric result must be recorded.

---

## 5. Staging rules

- Staging is **clean**: no preloaded demo transactions.
- The workbook creates the test transactions.
- Disable scheduler and outbound email unless the test explicitly needs them.
- Use a dedicated staging site and separate database.
- Back up before migrate.
- Record versions and commits in `STAGING_RUNBOOK.md`.
- Do not use production credentials or live customer data.
- Tag the exact commit deployed.

---

## 6. Production rules

Before production:

- UAT signed by the business owner/accountant.
- Backup and restore tested.
- Rollback plan written.
- Maintenance window agreed.
- DNS/SSL plan confirmed for website changes.
- Filing/statutory approval obtained where relevant.
- No unresolved high-severity issues.

After production:

- Record deployed tag.
- Run smoke tests.
- Archive the release notes and UAT evidence.
- Monitor logs and scheduled jobs.
- Do not edit filed/submitted statutory records; amend/cancel according to policy.

---

## 7. Change types and required docs

| Change | User manual | Technical manual | Runbook | Workbook |
|---|---|---|---|---|
| New DocType/report | Yes | Yes | If deploy/config | Yes |
| Field/validation change | Yes | Yes | If migration | Yes |
| Print format | Yes | Yes | No | Yes |
| Workflow/permission | Yes | Yes | If roles change | Yes |
| Integration/API | Yes | Yes | Yes | Yes |
| Website/Builder page | Content/page map | Technical/SEO/redirects | Yes | Yes |
| Upgrade/migration | Yes | Yes | Yes | Yes |
| Hotfix | Note in changelog | If design changes | If deploy | Regression test |

---

## 8. Review gate

Before merge, the reviewer checks:

- [ ] Code matches the documented behaviour.
- [ ] No test data or secrets committed.
- [ ] Docs are readable by a non-developer.
- [ ] Numeric examples reconcile.
- [ ] Deployment commands are current.
- [ ] README links resolve.
- [ ] Version/tag is correct.

**No documentation, no release.**
