# Maskopy Library Capabilities: Local vs. Official

This document provides a comprehensive view of the capabilities available in the **Official FINRA Maskopy Framework** and how we have simulated or implemented them in this local PoC.

## 1. Core Masking Algorithms

The following table lists the core algorithms provided by the official framework.

| Capability | Local PoC Implementation | Description |
| :--- | :--- | :--- |
| **Email Masking** | `mask_email` | Obfuscates the local part while preserving the domain for testing. |
| **Phone Masking** | `mask_phone` | Masks all but the last 4 digits to maintain realistic formats. |
| **Credit Card Masking** | `mask_card` | Masks the middle digits, keeping the BIN and last 4 for verification. |
| **Deterministic Hashing** | `mask_hash` | Uses SHA-256 to ensure the same input always yields the same masked output (critical for joining tables). |
| **Date Shifting** | `mask_date_shift` | Shifts dates by a random range (e.g., +/- 10 days) to protect birthdays while keeping ages realistic. |
| **Realistic Lookups** | `mask_lookup` | Replaces values with high-quality fake data (Names, Cities, Companies) for natural-looking test data. |
| **Scrubbing/Redaction** | `mask_scrub` | Completely removes data, replacing it with `[REDACTED]`. |
| **FPE (Simulation)** | `mask_fpe` | *NEW*: Format-Preserving Encryption. Encrypts data while keeping the original string length and character set. |

## 2. Advanced Official Features (AWS Only)

While our PoC handles the **logic**, the official framework handles the **infrastructure**:

1. **Multi-Database Connectors**: Built-in support for **MySQL**, **Oracle**, and **Dataverse**.
2.  **Configuration-Driven**: All masking rules are defined in a simple JSON/YAML configuration. You don't write code to mask; you just list the columns and the algorithm to use.
3.  **Auditing & Logging**: Every masking run is logged with statistics (number of rows masked, duration, success/failure) for compliance.
4.  **Cross-Platform Scope**: The official framework is designed to handle both **Oracle (on AWS)** and **Dataverse (Microsoft Power Platform)**, ensuring consistent masking across different data silos.
5.  **Secrets Management**: Integrates with **AWS Secrets Manager** to rotate and secure database credentials.
6.  **State Management**: Uses **AWS Step Functions** to ensure that if a masking run fails, the database is rolled back or alerted.

## 3. How to Leverage More Capabilities

To use these advanced features in this PoC, simply import the desired method from `maskopy.masking` and apply it to your database columns in `mask_data.py`.

Example of using the new **Format-Preserving Encryption (FPE)**:
```python
from maskopy import mask_fpe
new_value = mask_fpe("Sensitive-Account-123") # Returns "A-V-B-X-0-1-2"
```
