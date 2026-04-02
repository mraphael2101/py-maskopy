# Maskopy Oracle Data Masking Skeleton

This project provides a Dockerized Oracle database with two associated tables (`customers` and `payments`) and local Python masking logic (`maskopy/`).

## Project Overview

- **Oracle Database**: A `gvenzl/oracle-free` container initialized with an application schema and two tables:
  - `customers`: Contains `name`, `email`, and `phone`.
  - `payments`: Associated with `customers`, containing `card_number` and `amount`.
- **Standalone Masking Scripts**: `scripts/mask_data.py` and `scripts/reset_data.py` exist for the original MySQL demo flow. They are not yet updated to connect to Oracle.
- **Masking Method**: The original `maskopy` tool is built to run on Amazon Web Services (AWS). To make it easy to use on your own computer, we've included a simplified version in the `maskopy` folder that works the same way but doesn't require any cloud setup.

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.x](https://www.python.org/downloads/) (to run the masking script locally)

## Project Structure

```text
.
├── config/                # Configuration and orchestration files
│   ├── docker-compose.yml # Orchestration for the Oracle database
│   └── setup.py           # Package configuration for local development (optional)
├── db/                    # Database-related files
│   ├── data/              # Original sample data in CSV format
│   │   ├── customers.csv
│   │   └── payments.csv
│   └── init.sql           # SQL script to bootstrap the Oracle schema and sample data
├── docs/                  # Documentation files
│   ├── MASKOPY_CAPABILITIES.md
│   └── README.md (this file)
├── maskopy/               # Local implementation of maskopy core masking logic
│   ├── __init__.py
│   └── masking.py
├── scripts/               # Standalone Python scripts for masking and resetting
│   ├── mask_data.py
│   └── reset_data.py
└── ...
```

## Setup and Usage

To get started, run these commands from the repository root.

```bash
docker compose -f config/docker-compose.yml up -d
docker exec -it maskopy-oracle sqlplus maskopy/maskopypwd@//localhost:1521/FREEPDB1
docker compose -f config/docker-compose.yml down
```

Or run from anywhere by setting `MASKOPY_ROOT`:

```bash
MASKOPY_ROOT=/path/to/py-maskopy
docker compose -f "$MASKOPY_ROOT/config/docker-compose.yml" up -d
docker exec -it maskopy-oracle sqlplus maskopy/maskopypwd@//localhost:1521/FREEPDB1
docker compose -f "$MASKOPY_ROOT/config/docker-compose.yml" down
```

1. **Start the database**:
   Run this command to spin up the Oracle container:
   ```bash
   docker compose -f config/docker-compose.yml up -d
   ```
   *Note: This starts Oracle on port `1521` and automatically sets up the tables. **The first startup may take 2-4 minutes to complete initialization and run the SQL scripts. Check `docker logs -f maskopy-oracle` to see when it's ready.**.*

2. **Verify the database tables**:
   ```bash
   docker exec -it maskopy-oracle sqlplus maskopy/maskopypwd@//localhost:1521/FREEPDB1
   ```
   Then run:
   ```sql
   SELECT * FROM customers;
   SELECT * FROM payments;
   ```

3. **Install Python dependencies**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python3 -m pip install -e .
   ```
   This is optional unless you are running the Python scripts.

4. **Stop the database**:
   ```bash
   docker compose -f config/docker-compose.yml down
   ```

## Troubleshooting

### "Press Play" in your IDE
If you are using an IDE like PyCharm or VS Code, you can open `scripts/mask_data.py` or `scripts/reset_data.py` and press the "Play" button. Those scripts are not yet updated to connect to Oracle.

### "no such file or directory" or "No module named maskopy"
If you see an error like "no such file or directory" or "No module named maskopy," it usually means your current working directory (or `PYTHONPATH`) does not point at the repo.

If you're running commands from the repo root, verify you're in `py-maskopy` by typing `pwd`.

When setting the `PYTHONPATH`, ensure you are in the project root so that `.` adds the correct path. You can also run it as a one-liner:
```bash
cd /path/to/py-maskopy
PYTHONPATH=. python -m pydoc maskopy.masking
```

### Connection Issues
If you have trouble connecting, check that port `1521` is free on your machine and that the container is healthy.

## Key Concepts

### Automatic Table Creation
When you start the database for the first time, Docker automatically uses the `db/init.sql` file in this project to set up your tables (`customers` and `payments`) and add the initial data. You don't need to run any manual SQL commands to get started.

### Data Association
The `payments` table is linked to the `customers` table via a `customer_id` foreign key. This allows for realistic data masking scenarios where related data might need consistent masking.

## Local vs Official Maskopy

The official [FINRA maskopy framework](https://finraos.github.io/maskopy/docs.html) is an AWS-native tool designed for cloud-based orchestration (using Lambda, RDS, and Step Functions). It is **not** a standalone Python package available via `pip`.

To provide a working demonstration of these masking concepts locally:
1. **Local `maskopy/` folder**: We created a standard Python package directory in the project root.
2. **Implicit Dependency**: Because the folder exists locally, Python can import from it directly (`from maskopy import ...`) without any external installation required.
3. **Core Principles**: The logic inside `maskopy/masking.py` mirrors the types of obfuscation the official framework would apply to your database fields in an AWS environment.

### Oracle Integration
The database in this PoC is Oracle. The masking functions in `maskopy/` are database-agnostic, so it is viable to apply the same masking rules to Oracle tables.

What is not implemented in this repo yet:
- Updating `scripts/mask_data.py` and `scripts/reset_data.py` to connect to Oracle (for example via the `oracledb` Python driver).
- Oracle-specific SQL and data-type handling.

### Masking Strategy
The local package provides functions for:
- **Emails**: Masking local part while keeping the first character (e.g., `j***@example.com`).
- **Phone Numbers**: Masking all but the last 4 digits (e.g., `***-0101`).
- **Credit Cards**: Masking middle digits (e.g., `1234-****-****-3456`).
- **Deterministic Hashing**: Masking sensitive data with a salt-based SHA-256 hash to maintain consistency across tables.
- **Date Shifting**: Randomly shifting dates within a specified range to obfuscate exact timestamps while keeping them realistic.
- **Lookup Replacement**: Replacing sensitive values with random but realistic entries from a predefined list (e.g., names, cities).
- **Redaction**: Completely scrubbing data by replacing it with a fixed `[REDACTED]` string.
- **Format-Preserving Encryption (FPE)**: Replacing characters with pseudo-random ones from the same set to maintain the data's original length and structure.

### SQL*Plus Console Formatting
The `db/login.sql` file is used to automatically format the output of `sqlplus` for the `customers` and `payments` tables. Oracle's `sqlplus` looks for a file named exactly `login.sql` in the directory specified by the `ORACLE_PATH` environment variable (set to `/opt/oracle` in our `docker-compose.yml`) and runs it whenever a new session starts. This ensures that the wide `VARCHAR2` columns are displayed neatly on a single line instead of wrapping across multiple lines.

## Configuration

The database can be configured in `config/docker-compose.yml`:

| Variable | Description | Default |
|----------|-------------|---------|
| `ORACLE_PASSWORD` | SYS/SYSTEM password | `rootpwd` |
| `APP_USER` | Application schema user | `maskopy` |
| `APP_USER_PASSWORD` | Application schema password | `maskopypwd` |
