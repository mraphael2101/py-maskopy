# Maskopy MySQL Data Masking Skeleton

This project provides a Dockerized MySQL database with two associated tables (`customers` and `payments`) and a standalone Python script to mask sensitive fields using `maskopy`.

## Project Overview

- **MySQL Database**: A `mysql:8.0` container initialized with a `dummy_db` and two tables:
  - `customers`: Contains `name`, `email`, and `phone`.
  - `payments`: Associated with `customers`, containing `card_number` and `amount`.
- **Standalone Masking Script**: `mask_data.py` is a Python script that connects to the database and masks sensitive fields. It imports masking logic from the local `maskopy` package.
- **Masking Method**: The original `maskopy` tool is built to run on Amazon Web Services (AWS). To make it easy to use on your own computer, we've included a simplified version in the `maskopy` folder that works the same way but doesn't require any cloud setup.

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.x](https://www.python.org/downloads/) (to run the masking script locally)

## Project Structure

```text
.
├── maskopy/               # Local implementation of maskopy core masking logic
│   ├── __init__.py
│   └── masking.py
├── docker-compose.yml      # Orchestration for the MySQL database
├── init.sql                # SQL script to bootstrap the dummy database and tables
├── mask_data.py            # Standalone script for data masking
├── reset_data.py           # Reverts the database to original values
└── requirements.txt        # Python dependencies (mysql-connector-python)
```

## Setup and Usage

1. **Start the database**:
   ```bash
   docker compose up -d
   ```
   This will spin up a MySQL container on port `3307`. On its first start, it automatically runs the `init.sql` script to create the `customers` and `payments` tables and load them with sample data.

2. **Verify the database tables**:
   ```bash
   docker exec -it maskopy-mysql mysql -u root -prootpwd -e "SELECT * FROM dummy_db.customers; SELECT * FROM dummy_db.payments;"
   ```

3. **Install Python dependencies**:
   It is recommended to use a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
   Or install directly using `python3` and `pip3`:
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run the masking script**:
   If using a virtual environment:
   ```bash
   python mask_data.py
   ```
   Otherwise, use `python3`:
   ```bash
   python3 mask_data.py
   ```
   The script will connect to the database (at `127.0.0.1:3307`), mask the sensitive fields, and commit the changes.

5. **Verify masked data**:
   Run the same SQL command as in step 2 to see the masked records.

6. **Reset the database (optional)**:
   If using a virtual environment:
   ```bash
   python reset_data.py
   ```
   Otherwise, use `python3`:
   ```bash
   python3 reset_data.py
   ```
   This will clear the current records and re-insert the original, unmasked data.

7. **Stop the database**:
   ```bash
   docker compose down
   ```
   This will stop and remove the containers. The data in the database will be reset to the original state defined in `init.sql` the next time you start it.

## Troubleshooting

### Connection Issues
If you see an "Access Denied" error when running the script, it's likely a port conflict with a local MySQL server on your machine.
- **Port 3307**: We've configured the container to use `3307` on the host to avoid common conflicts with `3306`.
- **Host IP**: Use `127.0.0.1` in the script instead of `localhost` to ensure a TCP connection is used.

## Key Concepts

### Automatic Table Creation
When you start the database for the first time, Docker automatically uses the `init.sql` file in this project to set up your tables (`customers` and `payments`) and add the initial data. You don't need to run any manual SQL commands to get started.

### Data Association
The `payments` table is linked to the `customers` table via a `customer_id` foreign key. This allows for realistic data masking scenarios where related data might need consistent masking.

## Local vs Official Maskopy

The official [FINRA maskopy framework](https://finraos.github.io/maskopy/docs.html) is an AWS-native tool designed for cloud-based orchestration (using Lambda, RDS, and Step Functions). It is **not** a standalone Python package available via `pip`.

To provide a working demonstration of these masking concepts locally:
1. **Local `maskopy/` folder**: We created a standard Python package directory in the project root.
2. **Implicit Dependency**: Because the folder exists locally, Python can import from it directly (`from maskopy import ...`) without any external installation required.
3. **Core Principles**: The logic inside `maskopy/masking.py` mirrors the types of obfuscation the official framework would apply to your database fields in an AWS environment.

### Masking Strategy
The local package provides functions for:
- **Emails**: Masking local part while keeping the first character (e.g., `j***@example.com`).
- **Phone Numbers**: Masking all but the last 4 digits (e.g., `***-0101`).
- **Credit Cards**: Masking middle digits (e.g., `1234-****-****-3456`).

## Configuration

The database can be configured in `docker-compose.yml`:

| Variable | Description | Default |
|----------|-------------|---------|
| `MYSQL_ROOT_PASSWORD` | Root password for MySQL | `rootpwd` |
| `MYSQL_DATABASE` | Target database name | `dummy_db` |
