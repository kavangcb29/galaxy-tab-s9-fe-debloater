# Contributing to Samsung Galaxy Tab S9 FE Debloater Toolkit

Thank you for your interest in improving this project! We welcome contributions from the community to help make Samsung Galaxy devices faster, cleaner, and bloat-free while preserving critical tablet features like S Pen and DeX.

---

## 🛠️ How to Contribute

### 1. Adding or Updating Packages
All package definitions live in [`database.py`](database.py). If you find a new bloatware package or a One UI 6 / 6.1 / 7 package that needs classification:
1. Open [`database.py`](database.py).
2. Add the package to the `PACKAGES` list:
   ```python
   {
       "id": "com.example.package",
       "name": "Human-Readable Name",
       "category": "category_key",
       "risk": "safe" | "optional" | "caution" | "danger",
       "description": "Clear explanation of what it does and why it can/cannot be removed."
   }
   ```
3. Make sure to adhere to the safety policy:
   * **`safe`**: Zero functional impact on S Pen, DeX, or core system functionality.
   * **`optional`**: Safe to remove if unused (e.g., Samsung Internet, OneDrive).
   * **`caution`**: Disables an ecosystem feature (e.g., SmartThings, Galaxy Themes).
   * **`danger`**: **Never** assign lightly. Reserved for S Pen digitizer, Samsung Notes, keyboard, and system UI.

### 2. Updating Presets
Presets live in [`presets.json`](presets.json). If you have tested a profile on physical hardware (e.g., Tab S9 FE, Tab S9 FE+, Tab S9):
1. Keep the `safe_debixby_perf` and `safe_recommended` presets non-destructive.
2. Submit test results detailing device model, One UI version, and battery/performance observations.

### 3. Reporting Bugs & Suggesting Features
* Use GitHub Issues to submit bug reports or package requests.
* Use the provided [Issue Templates](.github/ISSUE_TEMPLATE/).

---

## 🧪 Testing Guidelines

Before submitting a Pull Request:
1. Run syntax verification:
   ```bash
   python -c "import debloater, gui, database, adb_manager, utils; print('OK')"
   ```
2. Verify CLI runs without errors:
   ```bash
   python debloater.py --cli
   ```
3. Ensure no local backup files (`backups/*.json`) or ADB binary folders (`bin/platform-tools/`) are staged in git.
