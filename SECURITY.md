# Security Policy

## Security Model

The **Samsung Galaxy Tab S9 FE Debloater Toolkit** is designed around safety and reversibility:

1. **Non-Root Operation**:
   - The tool uses official Android Debug Bridge (`adb`) user-level commands:
     - `pm disable-user --user 0 <package>`
     - `pm uninstall -k --user 0 <package>`
   - System partitions (`/system`, `/vendor`, `/product`) remain strictly read-only and unmodified.

2. **Knox Integrity**:
   - No bootloader unlocking is required.
   - **Samsung Knox warranty bit (0x0) is NOT tripped**.
   - Secure folder, Samsung Pass, and banking apps function normally.

3. **100% Reversible**:
   - The original APK binaries remain stored on the system partition.
   - Any package can be instantly reinstalled using:
     `adb shell cmd package install-existing <package>`
     or re-enabled using:
     `adb shell pm enable --user 0 <package>`
     via the built-in **Restore Center**.

4. **S Pen & System Safeguards**:
   - Critical tablet dependencies (S Pen digitizer, Samsung Notes, Samsung Keyboard, and DeX System UI) are tagged as `DANGER` and blocked from automatic removal to prevent soft bricks or loss of stylus functionality.

---

## Reporting Vulnerabilities

If you discover a security issue or a package misclassification that causes a bootloop on supported Samsung tablets, please report it via GitHub Issues or contact the maintainer directly.
