# Contributing to GalaxyNext

## Where the code lives

This repository versions a whole Frappe bench. Only one part of it is GalaxyNext's own code:

```
frappe-bench/apps/galaxyerp/        ← the GalaxyNext custom app: change things HERE
frappe-bench/apps/frappe/           ← vendored copy of Frappe (upstream code, do not edit)
frappe-bench/apps/erpnext/          ← vendored copy of ERPNext (upstream code, do not edit)
frappe-bench/apps/india_compliance/ ← vendored copy (upstream code, do not edit)
frappe-bench/apps/frappe_openai_integration/
frappe-bench/sites/                 ← site list and common config; per-site secrets are ignored
```

Never modify the vendored apps. If ERPNext needs to behave differently, override it from
`galaxyerp` (hooks, `override_doctype_class`, client scripts, fixtures).

## Workflow

1. Branch off the latest `main`:
   - `feature/<short-name>` for new work
   - `fix/<short-name>` for bug fixes
   - `chore/<short-name>` for maintenance
2. Keep commits small, with a clear message: `area: what changed`
   (e.g. `company-access: restrict app list per company`).
3. Push the branch and open a pull request into `main`. Fill in the template,
   especially **How it was tested** and **Deployment notes**.
4. Merge once it has been tested. The branch is deleted automatically.

`main` is protected: no force-pushes or deletion, and changes land through pull requests.

## Local setup

```bash
pip install frappe-bench
git clone https://github.com/laveshparyani/GalaxyNext.git
cd GalaxyNext/frappe-bench
bench setup env && bench setup requirements
bench setup redis && bench setup procfile
bench new-site galaxynext.localhost
bench --site galaxynext.localhost install-app erpnext galaxyerp india_compliance frappe_openai_integration
bench start
```

## Tests

```bash
bench --site galaxynext.localhost set-config allow_tests true
bench --site galaxynext.localhost run-tests --app galaxyerp
```

## Rules for Frappe changes

- **Everything goes through code.** DocTypes, Custom Fields, Property Setters, reports and
  print formats must be committed (DocType JSON, fixtures or patches) inside `galaxyerp`.
  Changes made only through the Desk UI are lost on a fresh install.
- Data changes to existing records go in a **patch** (`patches.txt`), never in manual SQL.
- **Never commit** `frappe-bench/sites/*/site_config.json`, `sites/*/private/`, backups,
  API keys or database dumps. `.gitignore` already excludes them.

## Reporting issues

Use the **Bug report** or **Feature request** templates. For security problems, see
[SECURITY.md](SECURITY.md).
