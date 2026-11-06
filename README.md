# 🚀 Samsung Galaxy Tab S9 FE Debloater & Optimizer Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-brightgreen.svg)](https://www.python.org/)
[![Platform: Android / One UI](https://img.shields.io/badge/Platform-One%20UI%206%20%7C%207%20%7C%208%20%7C%208.5%20%7C%209-orange.svg)](https://www.samsung.com)
[![Device: Tab S9 FE / FE+](https://img.shields.io/badge/Device-Galaxy%20Tab%20S9%20FE%20%7C%20FE%2B-blueviolet.svg)](#supported-devices)
[![Knox Safe](https://img.shields.io/badge/Knox-Untouched%20(0x0)-success.svg)](#-safety--security-model)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Donate-yellow.svg?logo=buy-me-a-coffee)](https://buymeacoffee.com/kavangcb29)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support-red.svg?logo=ko-fi)](https://ko-fi.com/kavangcb29)
[![PayPal](https://img.shields.io/badge/PayPal-Donate-00457C.svg?logo=paypal&logoColor=white)](https://paypal.me/KavanSudev)
[![UPI Support](https://img.shields.io/badge/UPI-GPay%20%7C%20PhonePe%20%7C%20Paytm-blueviolet.svg)](#-support-the-project)

An intelligent, non-root debloater and performance accelerator designed specifically for the **Samsung Galaxy Tab S9 FE (SM-X510 / SM-X516B)** and **One UI 6, 7, 8, 8.5, and One UI 9** devices. 

Frees up **1.2 GB+ of RAM**, halts standby battery drain, eliminates Exynos 1380 micro-stutters, and safeguards **S Pen, Samsung Notes, and Samsung DeX**.

---

## 📸 Preview

```
  ╔══════════════════════════════════════════════════════════════╗
  ║       SAMSUNG GALAXY TAB S9 FE DEBLOATER TOOLKIT             ║
  ║       Tailored for One UI 6 / 7 / 8 / 8.5 / 9 & Exynos 1380  ║
  ║       Protects S Pen, Samsung Notes & DeX Multitasking       ║
  ╚══════════════════════════════════════════════════════════════╝

┌─[ CONNECTED DEVICE ]─────────────────────────────────────────
│  Model: SM-X510 [★ Galaxy Tab S9 FE (Wi-Fi) [India Variant] DETECTED]
│  Android: 16 | One UI: 8.5 | Region: India (INS/INU) | Battery: 92%
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
* **Samsung Digital Wellbeing** (`com.samsung.android.forest`): Screen time and focus tracking preserved.

---

## 🚀 Quick Start Guide (Setup Page)

### 1. Enable Developer Options on Your Tablet
1. Open **Settings** on your Galaxy Tab S9 FE.
2. Go to **About tablet** ➔ **Software information**.
3. Tap **Build number** **7 times** rapidly until you see *"Developer mode has been enabled"*.

### 2. Configure Samsung Auto Blocker (Crucial for One UI 6.1 / 7 / 8 / 8.5 / 9!)
> [!IMPORTANT]
> Samsung introduced **Auto Blocker** in One UI 6.0 and enforces it strictly in **One UI 6.1, 7.0, 8.0, and 8.5**. Auto Blocker blocks USB cable software commands and ADB by default.
> 
> If your tablet shows "No Device Connected" or ADB commands fail:
> 1. Open **Settings** on your tablet.
> 2. Tap **Security and privacy** ➔ **Auto Blocker**.
> 3. Toggle Auto Blocker **OFF** (or turn off **"Maximum restrictions"** / **"Block software updates by USB cable"**).
> 4. *(You can safely turn Auto Blocker back ON after you finish debloating.)*

### 3. Enable USB Debugging
1. Return to **Settings** ➔ scroll to the very bottom and tap **Developer options**.
2. Locate **USB debugging** and toggle it to **ON**.
3. Tap **OK** on the confirmation prompt.

### 4. Connect to PC & Authorize Tablet
1. Connect your Tab S9 FE to your computer using a USB-C data cable.
2. Unlock your tablet screen.
3. When the prompt *"Allow USB debugging?"* appears, check **"Always allow from this computer"** and tap **Allow**.

> [!NOTE]
> **Indian Variant Verification (SM-X510 / SM-X516B - INS/INU):**
> If you are running the Indian variant of the Galaxy Tab S9 FE on the latest **One UI 8.5** update, the toolkit automatically detects your device, identifies your CSC region (`INS`/`INU`), and includes tailored cleanup for Indian regional bloat (Glance lockscreen stories & ads, Samsung Pay Mini, regional app stubs).

### 5. Launch the Toolkit

#### Option A: Desktop GUI (Recommended)
Double-click **`run.bat`** (or run in terminal):
```powershell
python debloater.py --gui
```
*Tip: Use the **📖 Setup Guide** tab in the GUI sidebar to run live connection diagnostics and verify your One UI version.*

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

## 📱 Supported Devices & Firmware

* **Samsung Galaxy Tab S9 FE** (`SM-X510` Wi-Fi, `SM-X516B` 5G - Indian & Global variants)
* **Samsung Galaxy Tab S9 FE+** (`SM-X610` Wi-Fi, `SM-X616B` 5G)
* **Samsung Galaxy Tab S9 / S9+ / S9 Ultra** (`SM-X710`, `SM-X810`, `SM-X910`)
* **Firmware Compatibility**:
  * **One UI 5.1.1** (Android 13)
  * **One UI 6.0 & 6.1** (Android 14)
  * **One UI 7.0 & 7.1** (Android 15)
  * **One UI 8.0 & 8.5** (Android 16 - Current latest update on Indian Tab S9 FE)
  * **One UI 9.0** (Future-ready architecture)

---

## 🤝 Contributing

Contributions are welcome! Please check [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on adding packages, testing presets, or submitting pull requests.

---

## ☕ Support the Project

If this toolkit helped make your Galaxy Tab S9 FE snappier, reclaimed RAM, improved battery life, or saved you time, consider supporting its maintenance and future One UI updates:

<p align="left">
  <a href="https://buymeacoffee.com/kavangcb29" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="42" width="150">
  </a>
  &nbsp;&nbsp;
  <a href="https://ko-fi.com/kavangcb29" target="_blank">
    <img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="Support on Ko-fi" height="42">
  </a>
  &nbsp;&nbsp;
  <a href="https://paypal.me/KavanSudev" target="_blank">
    <img src="https://img.shields.io/badge/Donate-PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white" alt="Donate with PayPal" height="42">
  </a>
</p>

* **🌍 International Supporters**: [Buy Me a Coffee](https://buymeacoffee.com/kavangcb29), [Ko-fi](https://ko-fi.com/kavangcb29), or [PayPal Direct](https://paypal.me/KavanSudev).
* **🇮🇳 Indian Users (GPay / PhonePe / Paytm / BHIM UPI)**:
  * Transfer directly via UPI ID: **`kavangcb@gmail.com`**

*⭐ Don't forget to star the repository if you found it useful!*

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
