![EXPENSE EXPLORER](docs/banner.svg)

# Expense Explorer

A Python desktop learning project for importing CSV/Excel tables, browsing records and plotting expenses with pandas, matplotlib and seaborn.

## Run

```sh
python -m pip install -r requirements.txt
python main.py
```

Create a local account, sign in, import a table and select columns for a histogram or pie chart. Files must include headers. Numeric expense columns are required for meaningful charts.

## Local data

Runtime SQLite defaults to `.data/user_data.db` and creates missing account/table metadata schemas. `EXPENSE_DB_PATH` can select a different file. The historical committed database is not used by default; its provenance has not been certified.

New passwords use salted PBKDF2-SHA256. If an explicitly selected old database has plaintext passwords, a successful login upgrades that account in place. Back up old data before opting into this migration. Unknown users and wrong passwords do not authenticate.

Table access checks the signed-in account against table metadata. Imported values use SQL parameters and identifiers are quoted. This remains a single-user local desktop application, not a hardened multi-user service.

## Validation

```sh
python -m pip install pytest==8.4.1
python -m pytest -q tests
```

Tests cover password verification, SQL-like usernames, unknown accounts, legacy password upgrades and table ownership. An offscreen Qt test imports, browses and deletes a synthetic CSV through the actual controls. Spreadsheet-format and plotting edge cases are not exhaustively covered.

Forecasting and budget planning are not implemented. This repository demonstrates desktop/data tooling rather than a trained prediction model.
