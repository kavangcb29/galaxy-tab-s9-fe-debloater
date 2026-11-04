# 🚀 Samsung Galaxy Tab S9 FE Debloater & Optimizer Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-brightgreen.svg)](https://www.python.org/)
[![Platform: Android / One UI](https://img.shields.io/badge/Platform-One%20UI%206%20%7C%206.1%20%7C%207-orange.svg)](https://www.samsung.com)
[![Device: Tab S9 FE / FE+](https://img.shields.io/badge/Device-Galaxy%20Tab%20S9%20FE%20%7C%20FE%2B-blueviolet.svg)](#supported-devices)
[![Knox Safe](https://img.shields.io/badge/Knox-Untouched%20(0x0)-success.svg)](#-safety--security-model)

An intelligent, non-root debloater and performance accelerator designed specifically for the **Samsung Galaxy Tab S9 FE (SM-X510 / SM-X516B)** and **One UI 6+** devices. 

Frees up **1.2 GB+ of RAM**, halts standby battery drain, eliminates Exynos 1380 micro-stutters, and safeguards **S Pen, Samsung Notes, and Samsung DeX**.

---

## 📸 Preview

```
  ╔══════════════════════════════════════════════════════════════╗
  ║       SAMSUNG GALAXY TAB S9 FE DEBLOATER TOOLKIT             ║
  ║       Tailored for One UI 6 / 6.1 / 7 & Exynos 1380          ║
  ║       Protects S Pen, Samsung Notes & DeX Multitasking       ║
  ╚══════════════════════════════════════════════════════════════╝

┌─[ CONNECTED DEVICE ]─────────────────────────────────────────
│  Model: SM-X510 [★ Galaxy Tab S9 FE DETECTED]
│  Android: 14 | One UI: 6.1 | Battery: 88%
└──────────────────────────────────────────────────────────────
```

---

## 🌟 Key Features

* **🛡️ S Pen & DeX Protection**: S Pen handwriting, Air Command, Samsung Notes, and Samsung DeX are classified as critical and locked against accidental removal.
* **⚡ 1-Click Optimization Presets**: Instantly apply tested profiles (Safe & Clean + De-Bixby + Exynos Performance Turbo).
* **🎮 Exynos 1380 CPU Unthrottling**: Disables Game Optimizing Service (GOS) to remove artificial thermal throttling and restore consistent 90Hz frame rates.
* **🚀 0.5x UI Speed Tweak**: Accelerates One UI animations by 50% for instantaneous app switching.
* **🔄 100% Reversible & Rootless**: Uses `pm disable-user --user 0` and `pm uninstall -k --user 0`. No root needed, no Knox trip (0x0).
* **💾 Automatic Backup Snapshots**: Automatically records a full JSON snapshot of all installed packages before any action.
* **📦 Auto-Provisioning ADB**: If ADB is not found in your system PATH, the tool auto-downloads Google's official platform-tools.
* **🖥️ Dual Interface**: Features both a sleek dark-themed Desktop GUI and an interactive Terminal CLI.

---

## 🎯 Curated Presets

| Preset | Description | Target Profile |
|---|---|---|
| **Safe & Clean + De-Bixby + Exynos Performance Turbo** *(Recommended)* | Complete setup: Meta/Facebook, AR Zone, telemetry, Samsung promotional bloat + full De-Bixby removal + Exynos 1380 unthrottling (GOS) + Wi-Fi telephony cleanup. | **Best for most users.** Maximizes battery, frees up RAM, and keeps S Pen, Notes, DeX, and Outlook intact. |
| **Safe & Clean Baseline** | Removes Facebook, telemetry, AR Emoji junk, Kids mode, and promotional bloat while preserving Bixby. | Users who still use Bixby voice or routines. |
| **De-Bixby Only** | Removes Bixby Voice assistant, voice wakeup hotword listening, Bixby Vision, and Samsung Free. | Stops microphone listening 24/7. |
| **Wi-Fi Tablet Telephony Cleaner** | Strips cellular phone dialer, spam call detection, and call log daemons (Hiya, Smart Call) on Wi-Fi tablets (SM-X510). | Wi-Fi tablet owners. |
| **Google Bloatware Removal** | Removes non-essential Google apps (Google TV, Meet, YouTube Music). | Users using alternative media apps. |

---

## 🛡️ Critical Features Protected

The following packages are explicitly marked **DANGER / CRITICAL** and protected:

* **Samsung Notes** (`com.samsung.android.app.notes`): Stylus note-taking and low-latency drawing engine.
* **S Pen Air Command** (`com.samsung.android.service.aircommand`): Hover menu, smart select, and pen shortcuts.
* **S Pen Digitizer Driver** (`com.samsung.android.spen.styluspen`): Wacom EMR pen communication.
* **Samsung Keyboard** (`com.samsung.android.honeyboard`): Direct handwriting-to-text input with S Pen.
* **Samsung DeX** (`com.sec.android.desktopmode.uiservice` & `com.sec.android.app.desktoplauncher`): Desktop multitasking mode.
* **Edge Panels** (`com.samsung.android.app.cocktailbarservice`): Multitasking split-screen app launcher.
* **Microsoft Outlook** (`com.microsoft.office.outlook`): Kept intact and excluded from debloat presets.

---

## 🚀 Quick Start Guide

### 1. Enable USB Debugging on Your Tablet
1. Open **Settings** on your Tab S9 FE.
2. Go to **About tablet** ➔ **Software information**.
3. Tap **Build number** **7 times** until you see *"Developer mode has been enabled"*.
4. Return to main **Settings** ➔ scroll to the bottom and tap **Developer options**.
5. Enable **USB debugging**.

### 2. Connect to PC
1. Connect your tablet to your computer with a USB-C cable.
2. Unlock the tablet screen.
3. When prompted with *"Allow USB debugging?"*, check **"Always allow from this computer"** and tap **Allow**.

### 3. Launch the Toolkit

#### Option A: Desktop GUI (Recommended)
Double-click **`run.bat`** (or run in terminal):
```powershell
python debloater.py --gui
```

#### Option B: Terminal CLI
Double-click **`run_cli.bat`** (or run in terminal):
```powershell
python debloater.py --cli
```

---

## 🔄 Restore Center

If you ever want an uninstalled app back:
1. Open the **Restore Center** tab in the GUI (or select Option 3 in the CLI).
2. The tool scans your tablet and lists all packages disabled or uninstalled for User 0.
3. Select any package and click **Restore Selected** (or **Restore ALL**).
4. Packages are restored immediately without internet access or factory reset.

---

## 🔒 Safety & Security Model

* **Knox Warranty Safe**: Does not unlock the bootloader or modify read-only system partitions. Knox status remains **0x0** (Warranty intact, Secure Folder & Samsung Pass work).
* **User 0 Only**: Uninstalls or disables apps only for the current user (`--user 0`). System binaries remain on device storage, making full restoration trivial.
* **Offline & Open Source**: No remote telemetry or third-party servers. All scripts and package mappings are completely transparent and inspectable.

---

## 📱 Supported Devices

* **Samsung Galaxy Tab S9 FE** (`SM-X510`, `SM-X516B`)
* **Samsung Galaxy Tab S9 FE+** (`SM-X610`, `SM-X616B`)
* **Samsung Galaxy Tab S9 / S9+ / S9 Ultra** (`SM-X710`, `SM-X810`, `SM-X910`)
* Compatible with **One UI 5.1.1**, **One UI 6.0**, **One UI 6.1**, and **One UI 7.0**.

---

## 🤝 Contributing

Contributions are welcome! Please check [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on adding packages, testing presets, or submitting pull requests.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
