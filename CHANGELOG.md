# Changelog

All notable changes to the **Samsung Galaxy Tab S9 FE Debloater Toolkit** are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v1.3.0] - 2026-11-07

### 🧹 Smart Tutor & Smart Switch Debloat (Added as Defaults)
* **Samsung Smart Tutor Removed & Defaulted**: Added `com.rsupport.rs.activity.rsupport.aas2` (RSupport remote support client) to default debloat presets and removed from the active device.
* **Samsung Smart Switch Suite Removed & Defaulted**: Added Smart Switch main application (`com.sec.android.easyMover`), background agent (`com.sec.android.easyMover.Agent`), and onboarding assistant (`com.samsung.android.smartswitchassistant`) to default debloat presets and stripped from the active device.
* **Resilient SecurityException Fallback**: Enhanced `adb_manager.py`'s `disable_package` to automatically fallback to `pm uninstall -k --user 0` when One UI security policies block shell component state changes.

---

## [v1.2.0] - 2026-11-06

### 🎮 Added & Preserved (Gaming & Media Tablet Focus)
* **Gaming Hub & Game Booster Protected**: Permanently excluded `com.samsung.android.game.gamehome`, `com.samsung.android.game.gametools`, and `com.samsung.android.game.gos` from debloat presets to ensure full Game Center libraries, game organization, and in-game floating tools remain active.
* **Samsung Digital Wellbeing Preserved**: Excluded `com.samsung.android.forest` from presets, allowing screen time, focus modes, and app timers to remain active.
* **Microsoft Outlook Preservation**: Kept `com.microsoft.office.outlook` active while targeting the redundant Microsoft 365 / Office hub app (`com.microsoft.office.officehubrow`).
* **Automated CLI Execution Flags**: Added `-y` / `--yes` (skip interactive prompts) and `--mode {disable, uninstall}` flags to `debloater.py` for headless scripting.
* **Direct PayPal Donation Integration**: Added direct support via `paypal.me/KavanSudev` to `.github/FUNDING.yml`, README donation badges, the Desktop GUI support modal, and CLI Option `S`.

### ⚡ Performance & Hardware Boosts
* **0.5x UI Speed Accelerator**: Integrated global window, transition, and animator scale modifications into performance presets, cutting One UI animation latency in half on the Exynos 1380 processor.
* **Exynos 1380 Throttle Bypass**: Added safe unthrottling profiles while keeping S Pen and Samsung DeX functionality 100% intact.

### 🎨 Desktop GUI Overhaul (`gui.py`)
* **High-DPI Razor-Sharp Typography**: Added native Windows DPI awareness hook (`ctypes.windll.shcore.SetProcessDpiAwareness(1)`), eliminating blurry text and low-resolution scaling on 1080p, 1440p, and 4K monitors.
* **Modern Left Navigation Sidebar**: Replaced legacy notebook tabs with a modern sidebar layout (`1-Click Presets`, `Package Manager`, `Restore Center`, `Hardware Tweaks`, `Activity & Logs`).
* **Interactive Support Modal**: Created a dedicated, multi-platform donation dialog offering 1-click access to Buy Me a Coffee, Ko-fi, and PayPal.
* **Refined Design System**: Deep obsidian palette (`#0b0d13`), custom reactive buttons (`ModernButton`) with hover transitions, and a live device status indicator chip.

### 🐛 Bug Fixes & Stability
* **Windows Terminal Unicode Encoding**: Resolved `UnicodeEncodeError: 'charmap' codec` on Windows command prompts by enforcing UTF-8 stream reconfiguration (`sys.stdout.reconfigure(encoding='utf-8')`).
* **One UI 6+ SecurityException Fallback**: Implemented automatic fallback from `pm disable-user` to `pm uninstall -k --user 0` for packages protected against component state modification by shell on newer Samsung firmware.
* **Indian Variant Firmware Support**: Added recognition and cataloging for regional bloatware including Glance lockscreen feeds (`com.glance.internet`) and regional recommendations (`com.samsung.android.rapps`).

---

## [v1.0.0] - 2026-11-04

### Initial Release
* Rootless package manager leveraging Android's multi-user framework (`pm uninstall -k --user 0` and `pm disable-user --user 0`).
* Automatic pre-flight Google Android platform-tools downloading.
* Domain-specific safety safeguards for S Pen, Samsung Notes, and Samsung DeX.
* 1-Click Restore Center and automated safety backup snapshots.
* Curated catalog of 70+ Samsung One UI packages with risk ratings.
