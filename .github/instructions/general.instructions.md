################################################################################
#                                                                              #
#    A   GGGGG  EEEEE  N   N  TTTTT  IIIII  CCCC     W   W  OOO  RRRR   L      DDDD   #
#   A A  G      E      NN  N    T      I   C         W   W O   O R   R  L      D   D  #
#  AAAAA G  GG  EEE    N N N    T      I   C         W W W O   O RRRR   L      D   D  #
#  A   A G   G  E      N  NN    T      I   C         WW WW O   O R  R   L      D   D  #
#  A   A  GGGG  EEEEE  N   N    T    IIIII  CCCC     W   W  OOO  R   R  LLLLL  DDDD   #
#                                                                              #
################################################################################

---

applyTo: "**/*.py"

---

# General Coding Standards & File-Level Rules

This document outlines the mandatory file-level configurations, functional design constraints, and specific naming patterns enforced across all repository components.

---

## 1. File Header Requirements
Every script, module, and configuration file generated must begin with a minimal, single-line reference comment pointing back to this structural root layout:
```python
# Context: Agentic World Architecture Specification (general.instructions.md)
```

---

## 2. Naming Standards & Prefix Conventions

### 2.1 Function Naming (The AI_VERSION_ Rule)
To track code evolution and maintain compliance within our automated orchestration layer, every function must follow a specific, rigid prefix rule:
- **Format:** `def AI_VERSION_<FUNCTION_NAME>(...):`
- **Casing:** The `AI_VERSION_` prefix must be strictly uppercase, followed immediately by the descriptive function name in standard Python `snake_case`.

*Good Example:*
```python
def AI_VERSION_clean_customer_records(df: DataFrame) -> DataFrame:
```

*Bad Example:*
```python
def ai_version_CleanCustomerRecords(df):
```

### 2.2 Module and File Casing
- All python code files (`.py`) must use strict snake_case naming conventions (e.g., `business_logic.py`, `column_schemas.py`).
- Configuration schemas or data serialization definitions must reflect their exact structural capability.

---

## 3. Pure Functional Component Engineering

To prevent messy state flags, unpredictable logic updates, or broken pipelines, every file in the script directory must strictly adhere to functional programming constraints:

- **Immutability First:** Functions must never modify input variables or source DataFrames directly. Instead, they must generate and return a brand-new copy or structural clone.
- **Single Responsibility (SRP):** One file must handle exactly one specific capability. If a pipeline requires reading data, filtering rows, and running a calculation, these steps must be split into three separate files (e.g., `readers.py`, `cleaning.py`, and `business_logic.py`).
- **No Global States:** Functions are forbidden from depending on mutable global variables. All external references, parameters, thresholds, and sessions must be passed explicitly into the function signatures as arguments.
- **Deterministic Operations:** Passing identical input values into a functional block must always yield the exact same output array or DataFrame structure without side effects.

---

## 4. Granular Context Controls & Execution Conditions

Rules inside this repository are applied dynamically based on the specific directory or runtime context. Do not force unnecessary constraints when the workflow context does not match.

```text
  [ Incoming Code Task ]
           │
           ├──► Context: Data Pipeline Task?
           │     └──► ACTION: Enforce explicit StructType schemas & local PySpark rules.
           │
           ├──► Context: Configuration/Infrastructure Task?
           │     └──► ACTION: Bypass DataFrame validation; enforce environment variables.
           │
           └──► Context: Local Testing Context?
                 └──► ACTION: Inject conftest execution fixtures; suppress logging noise.
```

### 4.1 Data Transformation Context
- **Triggers When:** Editing files inside `src/transforms/` or `src/schemas/`.
- **Constraint:** Functions must explicitly accept a `pyspark.sql.DataFrame` object, enforce rigorous static type-hint structures, and output a validated DataFrame result.

### 4.2 Utility & Infrastructure Context
- **Triggers When:** Editing files inside `config/` or `src/utils/`.
- **Constraint:** The `AI_VERSION_` function prefix rule still applies, but Spark DataFrame type constraints are dropped. Focus purely on native python data types (`dict`, `str`, `int`) and basic system IO structures.
