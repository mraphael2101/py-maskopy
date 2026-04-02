# Maskopy MySQL Data Masking Skeleton

This project provides a Dockerized MySQL database with two associated tables (`customers` and `payments`) and a standalone Python script to mask sensitive fields using `maskopy`.

## Project Overview

- **MySQL Database**: A `mysql:8.0` container initialized with a `dummy_db` and two tables:
  - `customers`: Contains `name`, `email`, and `phone`.
  - `payments`: Associated with `customers`, containing `card_number` and `amount`.
- **Standalone Masking Script**: `scripts/mask_data.py` connects to the database and masks sensitive fields. It imports masking logic from the local `maskopy` package.
- **Masking Method**: The original `maskopy` tool is built to run on Amazon Web Services (AWS). To make it easy to use on your own computer, we've included a simplified version in the `maskopy` folder that works the same way but doesn't require any cloud setup.

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.x](https://www.python.org/downloads/) (to run the masking script locally)

## Project Structure

```text
.
├── config/                # Configuration and orchestration files
│   ├── docker-compose.yml # Orchestration for the MySQL database
│   └── setup.py           # Package configuration for local development (optional)
├── db/                    # Database-related files
│   ├── data/              # Original sample data in CSV format
│   │   ├── customers.csv
│   │   └── payments.csv
│   └── init.sql           # SQL script to bootstrap the dummy database
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
python3 -m venv .venv
source .venv/bin/activate
docker compose -f config/docker-compose.yml up -d
python3 -m pip install -e .
python3 scripts/reset_data.py
python3 scripts/mask_data.py
docker compose -f config/docker-compose.yml down
```

Or run from anywhere by setting `MASKOPY_ROOT`:

```bash
MASKOPY_ROOT=/path/to/py-maskopy
python3 -m venv "$MASKOPY_ROOT/.venv"
source "$MASKOPY_ROOT/.venv/bin/activate"
docker compose -f "$MASKOPY_ROOT/config/docker-compose.yml" up -d
python3 -m pip install -e "$MASKOPY_ROOT"
python3 "$MASKOPY_ROOT/scripts/reset_data.py"
python3 "$MASKOPY_ROOT/scripts/mask_data.py"
docker compose -f "$MASKOPY_ROOT/config/docker-compose.yml" down
```

1. **Start the database**:
   Run this command to spin up the MySQL container:
   ```bash
   docker compose -f config/docker-compose.yml up -d
   ```
   *Note: This starts MySQL on port `3307` and automatically sets up the tables.*

2. **Verify the database tables**:
   ```bash
   docker exec -it maskopy-mysql mysql -u root -prootpwd -e "SELECT * FROM dummy_db.customers; SELECT * FROM dummy_db.payments;"
   ```

3. **Install Python dependencies**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python3 -m pip install -e .
   ```

4. **Run the masking script**:
   ```bash
   python3 scripts/mask_data.py
   ```
   The script connects to the database, masks sensitive fields, and shows the results in a table.

5. **Verify masked data**:
   Run the command in step 2 again to see the changes in the database.

6. **Reset the database**:
   ```bash
   python3 scripts/reset_data.py
   ```
   This reloads the original data from the `db/data/` folder.

7. **Stop the database**:
   ```bash
   docker compose -f config/docker-compose.yml down
   ```

## Troubleshooting

### "Press Play" in your IDE
If you are using an IDE like PyCharm or VS Code, you can simply open `scripts/mask_data.py` or `scripts/reset_data.py` and press the "Play" button. The scripts are smart enough to find the project root and the data files automatically.

### "no such file or directory" or "No module named maskopy"
If you see an error like "no such file or directory" or "No module named maskopy," it usually means your current working directory (or `PYTHONPATH`) does not point at the repo.

If you're running commands from the repo root, verify you're in `py-maskopy` by typing `pwd`.

When setting the `PYTHONPATH`, ensure you are in the project root so that `.` adds the correct path. You can also run it as a one-liner:
```bash
cd /path/to/py-maskopy
PYTHONPATH=. python -m pydoc maskopy.masking
```

### Connection Issues
If you see an "Access Denied" error when running the script, it's likely a port conflict with a local MySQL server on your machine.
- **Port 3307**: We've configured the container to use `3307` on the host to avoid common conflicts with `3306`.
- **Host IP**: Use `127.0.0.1` in the script instead of `localhost` to ensure a TCP connection is used.

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
This PoC uses MySQL for demonstration. The masking functions in `maskopy/` are database-agnostic, so it is viable to apply the same masking rules to Oracle.

What is not implemented in this repo yet:
- An Oracle connection layer (for example via the `oracledb` Python driver).
- Oracle-specific SQL and data-type handling.

### Masking Strategy
The local package provides functions for:
- **Emails**: Masking local part while keeping the first character (e.g., `j***@example.com`).
- **Phone Numbers**: Masking all but the last 4 digits (e.g., `***-0101`).
- **Credit Cards**: Masking middle digits (e.g., `1234-****-****-3456`).

## Configuration

The database can be configured in `config/docker-compose.yml`:

| Variable | Description | Default |
|----------|-------------|---------|
| `MYSQL_ROOT_PASSWORD` | Root password for MySQL | `rootpwd` |
| `MYSQL_DATABASE` | Target database name | `dummy_db` |
