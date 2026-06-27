# Context: Agentic World Architecture Specification (agents.md)

# Agent Environment Setup & Pre-requisites (macOS with Homebrew)

This document outlines the step-by-step instructions for preparing a macOS system to run our local modular PySpark environment. Follow these steps to ensure all system-level binaries and virtual environment configurations are identically matched.

---

## 1. System Pre-requisites (macOS)

Apache Spark relies on the Java Virtual Machine (JVM) to execute data processing logic. We use **Homebrew** to automate the installation and management of these dependencies.

### Step 1.1: Install Homebrew
If you do not have Homebrew installed on your macOS system, open your terminal and run:
```bash
/bin/bash -c "$(curl -fsSL https://githubusercontent.com)"
```

### Step 1.2: Install Java (OpenJDK 17)
PySpark supports Java 8, 11, or 17. OpenJDK 17 is highly recommended for stability on Apple Silicon (M1/M2/M3/M4) and Intel-based Macs. Install it via Homebrew:
```bash
brew install openjdk@17
```

### Step 1.3: Set Java Environment Paths
To ensure your macOS system shell and PySpark can locate the Java binary footprint, add the environment configurations to your profile shell (`~/.zshrc`):
```bash
# Link the openjdk system files to the standard macOS Java wrapper
sudo ln -sfn $(brew --prefix)/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk

# Append path environments to your zsh profile
echo 'export JAVA_HOME="/Library/Java/JavaVirtualMachines/openjdk-17.jdk/Contents/Home"' >> ~/.zshrc
echo 'export PATH="$JAVA_HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Step 1.4: Verify Java Installation
Confirm that Java is successfully linked and active in your terminal session:
```bash
java -version
```

---

## 2. Python Virtual Environment Setup

All runtime libraries, Python tools, and PySpark packages must be safely sandboxed inside an isolated virtual environment named **`COPILOTCOURSE_VE_27JUN`**.

### Step 2.1: Create the Environment
Navigate to your project root workspace folder in your terminal and initialize the environment:
```bash
python3 -m venv COPILOTCOURSE_VE_27JUN
```

### Step 2.2: Activate the Environment
Always activate this environment before building, editing, or testing pipeline layers:
```bash
source COPILOTCOURSE_VE_27JUN/bin/activate
```
*Your terminal prompt will change to display `(COPILOTCOURSE_VE_27JUN)` at the beginning.*

### Step 2.3: Upgrade Virtual Core Package Managers
```bash
pip install --upgrade pip setuptools wheel
```

---

## 3. Direct Pip Installation Workflow

No standalone Apache Spark server installation is required. The Python package manager `pip` will download, extract, and provision the complete PySpark execution binary bundle directly into your local sandbox folder.

### Step 3.1: Install PySpark & Native Matrix Dependencies
Run the command below to fetch all core transformation dependencies:
```bash
pip install pyspark==3.5.1 pytest pandas pyarrow
```
- **pyspark**: Bundles the fully-functional local Spark execution engine.
- **pyarrow**: Optimizes memory-efficient column data movement between Spark and Python (crucial for local speeds).
- **pandas**: Used for baseline tabular evaluation tracking.
- **pytest**: Drives our unit verification validation layers.

### Step 3.2: Export Locked Requirements
Lock these dependencies into your tracking catalog file:
```bash
pip freeze > requirements.txt
```

---

## 4. Verification Check

To confirm that your macOS environment paths, Homebrew-linked Java paths, and virtual pip setup are configured perfectly, run this simple test.

1. Ensure your workspace is active: `source COPILOTCOURSE_VE_27JUN/bin/activate`
2. Save the code snippet below into a file named `verify_spark.py`:

```python
# verify_spark.py
from pyspark.sql import SparkSession

def AI_VERSION_verify_local_setup():
    print("Initializing test Spark session via pip-embedded binaries...")
    spark = SparkSession.builder \
        .appName("VerificationApp") \
        .master("local[*]") \
        .getOrCreate()
    
    # Create simple dataframe
    data = [("Agentic", 1), ("World", 2)]
    df = spark.createDataFrame(data, ["Context", "ID"])
    df.show()
    
    print("SUCCESS: local PySpark environment is functional and completely ready!")
    spark.stop()

if __name__ == "__main__":
    AI_VERSION_verify_local_setup()
```

3. Run the verification script:
```bash
python verify_spark.py
```

---

## 5. Agent Execution Sequence & Instruction Hierarchy

When an automated agent or GitHub Copilot initiates a pipeline task, it must parse the markdown rules files in a strict, sequential chain to maintain systemic architectural integrity.

### 5.1 The Instruction Checklist Sequence
Before writing a single line of functional code, the agent must check its compliance pipeline in this exact order:

```text
Step 1: general.instructions.md ──► Validates ASCII banner, AI_VERSION_ prefix, and file rules.
               │
Step 2: source_data.instructions.md ──► Confirms source/ folder paths, schema contracts, and dummy CSV files.
               │
Step 3: copilot-instructions.md  ──► Enforces local Spark configs, performance tuning, and modular code layers.
               │
Step 4: Execute / Generate Code ──► Code is written safely into the correct isolated sub-file.
```

### 5.2 Granular Execution Protocol
1. **Analyze Rule Context:** The agent reads `general.instructions.md` first. It identifies if the incoming task is a *Data Transformation*, a *Utility Setup*, or a *Testing* job.
2. **Verify Data Dependencies:** Next, the agent references `source_data.instructions.md`. It verifies if `customer.csv` and `client.csv` are in place, ensuring it does not overwrite existing data files.
3. **Apply Spark Architecture Standards:** The agent consults `copilot-instructions.md` to map the target code into the correct directory folder structure. It ensures the script uses the `local[*]` session builder, explicitly tracks `StructType` column schemas, and never runs performance-killing Python loops.
4. **Implement the Function Naming Rules:** Finally, the code is generated. Every function signature *must* be prepended with the standard `AI_VERSION_` flag (e.g., `def AI_VERSION_process_data()`).
