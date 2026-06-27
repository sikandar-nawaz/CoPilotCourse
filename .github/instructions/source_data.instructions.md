# Context: Agentic World Architecture Specification (source_data.instructions.md)


---

applyTo: "source/**"

---

# Source Data Provisioning Rules

This document outlines the mandatory rules for verifying, generating, and maintaining source data files inside the repository. It ensures that any local test run or initial pipeline load succeeds out-of-the-box by guaranteeing the presence of clean, joinable datasets.

---

## 1. Directory Storage Policy
- **Mandatory Location:** All raw source datasets must be stored and looked up exclusively inside the root `source/` directory (e.g., `source/customer.csv` and `source/client.csv`).
- **Git Strategy:** The `source/` folder structure must be tracked, but large generated data files should be kept locally or ignored via `.gitignore` based on team data compliance policies.

---

## 2. Dynamic Existence Check (Idempotency Rule)
Before any data pipeline initialization or testing task kicks off, the environment must perform an existence check.
- **Rule:** If `source/customer.csv` and `source/client.csv` already exist, **do not overwrite or recreate them**. Preserve any existing data.
- **Rule:** If either file is missing, the setup scripts must auto-generate them instantly using the predefined dummy data contracts specified below.

---

## 3. Data Schema & Join Contracts

To ensure a seamless first load, both files must share a matching relational column (`client_id`) to allow flawless inner and left joins.

### 3.1 Customer Data Contract (`source/customer.csv`)
This file registers individual consumer profiles associated with corporate clients.

**Required Columns & Types:**
- `customer_id` (Integer): Unique primary identifier for the consumer.
- `client_id` (Integer): Foreign key referencing the parent client organization.
- `customer_name` (String): Full name of the consumer.
- `signup_date` (String/YYYY-MM-DD): The date the customer profile was created.

**Mandatory Dummy Content:**
```csv
customer_id,client_id,customer_name,signup_date
1001,501,Alice Smith,2026-01-15
1002,501,Bob Jones,2026-02-20
1003,502,Charlie Brown,2026-03-05
1004,503,Diana Prince,2026-04-12
```

### 3.2 Client Data Contract (`source/client.csv`)
This file maintains corporate organizational parameters and account statuses.

**Required Columns & Types:**
- `client_id` (Integer): Unique primary identifier for the client company.
- `client_name` (String): Corporate or organization trading name.
- `tier` (String): Service tier level (e.g., Enterprise, Premium, Standard).
- `region` (String): Geographic operating region.

**Mandatory Dummy Content:**
```csv
client_id,client_name,tier,region
501,Acme Corp,Enterprise,EMEA
502,Stark Industries,Premium,AMER
503,Wayne Enterprises,Standard,APAC
```

---

## 4. Blueprint Reference Implementation

When writing or generating the data-verification layer inside `src/extract/readers.py`, use the following logic pattern:

```python
import os
import csv

def AI_VERSION_ensure_source_data_exists(source_dir: str = "source") -> None:
    """
    Verifies existence of source datasets.
    Generates joinable dummy CSV files if they are missing.
    """
    os.makedirs(source_dir, exist_ok=True)
    
    cust_path = os.path.join(source_dir, "customer.csv")
    client_path = os.path.join(source_dir, "client.csv")
    
    # Check and generate customer.csv
    if not os.path.exists(cust_path):
        with open(cust_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["customer_id", "client_id", "customer_name", "signup_date"])
            writer.writerows([
                [1001, 501, "Alice Smith", "2026-01-15"],
                [1002, 501, "Bob Jones", "2026-02-20"],
                [1003, 502, "Charlie Brown", "2026-03-05"],
                [1004, 503, "Diana Prince", "2026-04-12"]
            ])
            
    # Check and generate client.csv
    if not os.path.exists(client_path):
        with open(client_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["client_id", "client_name", "tier", "region"])
            writer.writerows([
                [501, "Acme Corp", "Enterprise", "EMEA"],
                [502, "Stark Industries", "Premium", "AMER"],
                [503, "Wayne Enterprises", "Standard", "APAC"]
            ])
```
