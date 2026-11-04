"""
Samsung Tab S9 FE Debloater - Core CLI & Orchestrator
Cross-platform tool tailored for Samsung Galaxy Tab S9 FE / S9 series and One UI devices.
"""

import os
import sys
import argparse
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

# Ensure UTF-8 output on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from adb_manager import ADBManager
import database
import utils

# ANSI Color Codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def colorize(text: str, color: str) -> str:
    # Check if Windows terminal supports ANSI or enable virtual terminal processing
    if os.name == 'nt':
        os.system('')
    return f"{color}{text}{Colors.RESET}"

class TabS9FEDebloater:
    def __init__(self):
        self.adb = ADBManager()
        self.device_info: Dict[str, Any] = {}
        self.active_serial: Optional[str] = None

    def refresh_connection(self) -> bool:
        """Checks for ADB and connected devices."""
        if not self.adb.is_adb_installed():
            print(colorize("\n[!] ADB executable not detected.", Colors.YELLOW))
            print("Downloading Google Android platform-tools...")
            try:
                self.adb.download_platform_tools()
                print(colorize("[✓] Platform-tools downloaded successfully!", Colors.GREEN))
            except Exception as e:
                print(colorize(f"[X] Failed to setup ADB: {e}", Colors.RED))
                return False

        devices = self.adb.get_connected_devices()
        if not devices:
            self.active_serial = None
            self.device_info = {}
            return False

        # Pick first active device
        active = [d for d in devices if d["status"] == "device"]
        if active:
            self.active_serial = active[0]["serial"]
            self.device_info = self.adb.get_device_info(self.active_serial)
            return True
        else:
            self.active_serial = devices[0]["serial"]
            self.device_info = {"status": devices[0]["status"], "serial": self.active_serial}
            return False

    def print_banner(self):
        banner = """
  ╔══════════════════════════════════════════════════════════════╗
  ║       SAMSUNG GALAXY TAB S9 FE DEBLOATER TOOLKIT             ║
  ║       Tailored for One UI 6 / 6.1 / 7 & Exynos 1380          ║
  ║       Protects S Pen, Samsung Notes & DeX Multitasking       ║
  ╚══════════════════════════════════════════════════════════════╝
"""
        print(colorize(banner, Colors.CYAN))

    def print_device_card(self):
        if not self.active_serial:
            print(colorize("┌─[ DEVICE STATUS ]────────────────────────────────────────────", Colors.YELLOW))
            print(colorize("│  Status: NO DEVICE CONNECTED", Colors.RED))
            print("│  1. Enable 'Developer Options' on your tablet:")
            print("│     Settings -> About Tablet -> Software Info -> Tap 'Build Number' 7 times")
            print("│  2. Enable 'USB Debugging' in Settings -> Developer Options")
            print("│  3. Connect tablet via USB-C cable and tap 'Allow' on tablet screen.")
            print(colorize("└──────────────────────────────────────────────────────────────", Colors.YELLOW))
            return

        status = self.device_info.get("status", "device")
        if status == "unauthorized":
            print(colorize("┌─[ DEVICE STATUS ]────────────────────────────────────────────", Colors.YELLOW))
            print(colorize("│  Status: UNAUTHORIZED", Colors.YELLOW))
            print("│  Please unlock your tablet screen and tap 'Always allow from this computer'.")
            print(colorize("└──────────────────────────────────────────────────────────────", Colors.YELLOW))
            return

        is_s9fe = self.device_info.get("is_tab_s9_fe", False)
        market_name = self.device_info.get("market_name", "Samsung Device")
        badge = colorize(f" [★ {market_name} DETECTED]", Colors.GREEN) if is_s9fe else f" ({market_name})"

        print(colorize("┌─[ CONNECTED DEVICE ]─────────────────────────────────────────", Colors.GREEN))
        print(f"│  Model: {colorize(self.device_info.get('model', 'Unknown'), Colors.BOLD)}{badge}")
        print(f"│  Android: {self.device_info.get('android_version', 'Unknown')} | One UI: {self.device_info.get('oneui_version', 'Unknown')}")
        print(f"│  Battery: {self.device_info.get('battery', 'Unknown')} | Serial: {self.active_serial}")
        print(colorize("└──────────────────────────────────────────────────────────────", Colors.GREEN))

    def run_debloat(self, package_ids: List[str], mode: str = "uninstall"):
        """
        Executes debloat with automatic backup snapshot creation.
        mode: 'uninstall' (pm uninstall -k --user 0) or 'disable' (pm disable-user --user 0)
        """
        if not self.active_serial or self.device_info.get("status") == "unauthorized":
            print(colorize("\n[!] Please connect your tablet with USB Debugging enabled first.", Colors.RED))
            return

        installed = self.adb.get_installed_packages(self.active_serial)
        
        # Filter packages that are actually installed on the device
        target_pkgs = [pkg for pkg in package_ids if pkg in installed]
        
        if not target_pkgs:
            print(colorize("\n[i] None of the selected packages are currently installed or active on this device.", Colors.CYAN))
            return

        # Check for critical S Pen / Notes / DeX packages
        pkg_map = database.get_package_map()
        critical_found = [p for p in target_pkgs if pkg_map.get(p, {}).get("risk") == "danger"]
        if critical_found:
            print(colorize("\n⚠️  CRITICAL WARNING: The following S Pen / Tablet packages were flagged:", Colors.RED))
            for cp in critical_found:
                print(f"    - {cp} ({pkg_map[cp]['name']})")
            confirm = input(colorize("Are you absolutely sure you want to remove critical tablet features? [type 'FORCE' to proceed]: ", Colors.YELLOW))
            if confirm.strip() != "FORCE":
                print(colorize("Aborting operation to protect S Pen & system stability.", Colors.GREEN))
                return

        # Step 1: Automatic backup snapshot
        print(colorize("\n[1/3] Creating safety backup snapshot of installed packages...", Colors.CYAN))
        snapshot_path = utils.create_backup_snapshot(self.device_info, installed)
        print(colorize(f"      Saved backup snapshot to: {snapshot_path.name}", Colors.GREEN))

        # Step 2: Confirmation
        action_verb = "Uninstall (User 0)" if mode == "uninstall" else "Disable"
        print(colorize(f"\n[2/3] Ready to {action_verb} {len(target_pkgs)} packages.", Colors.BOLD))
        confirm = input(f"Proceed with {action_verb}? [Y/n]: ").strip().lower()
        if confirm and confirm != 'y':
            print("Cancelled.")
            return

        # Step 3: Execution
        print(colorize(f"\n[3/3] Executing {action_verb}...", Colors.CYAN))
        success_count = 0
        for i, pkg in enumerate(target_pkgs, 1):
            name = pkg_map.get(pkg, {}).get("name", pkg)
            print(f"  [{i}/{len(target_pkgs)}] {name} ({pkg})... ", end="", flush=True)
            
            if mode == "disable":
                success, msg = self.adb.disable_package(pkg, self.active_serial)
            else:
                success, msg = self.adb.uninstall_package(pkg, keep_data=True, serial=self.active_serial)

            if success:
                success_count += 1
                utils.log_debloat_action(pkg, mode, True, note=name)
                print(colorize("DONE", Colors.GREEN))
            else:
                utils.log_debloat_action(pkg, mode, False, note=msg)
                print(colorize(f"FAILED ({msg})", Colors.RED))

        print(colorize(f"\n[✓] Finished: {success_count}/{len(target_pkgs)} packages successfully processed.", Colors.GREEN))
        print(colorize("[i] All uninstalled packages can be restored at any time in the Restore Center.", Colors.CYAN))
        print("Tip: A reboot is recommended to ensure background daemons are fully stopped.")

    def run_restore(self, package_ids: Optional[List[str]] = None):
        """Restores packages back to user 0."""
        if not self.active_serial:
            print(colorize("\n[!] Tablet not connected.", Colors.RED))
            return

        history = utils.load_debloat_history()
        candidates = self.adb.get_uninstalled_or_disabled_packages(self.active_serial)
        
        # Merge history with uninstalled candidates
        merged = sorted(list(set(list(history.keys()) + candidates)))
        pkg_map = database.get_package_map()

        if not merged:
            print(colorize("\n[i] No uninstalled or disabled packages found to restore.", Colors.CYAN))
            return

        to_restore = package_ids or []
        if not to_restore:
            print(colorize("\n=== RESTORE CENTER: Uninstalled / Disabled Packages ===", Colors.CYAN))
            for i, p in enumerate(merged, 1):
                p_name = pkg_map.get(p, {}).get("name", "Package")
                print(f"  {i}. {p_name} ({p})")
            print("  A. Restore ALL packages")
            print("  0. Back")

            choice = input("\nEnter package number(s) comma separated, or 'A' for all: ").strip().lower()
            if choice == '0' or not choice:
                return
            elif choice == 'a':
                to_restore = merged
            else:
                try:
                    indices = [int(x.strip()) - 1 for x in choice.split(",") if x.strip().isdigit()]
                    to_restore = [merged[idx] for idx in indices if 0 <= idx < len(merged)]
                except Exception:
                    print(colorize("Invalid selection.", Colors.RED))
                    return

        print(colorize(f"\nRestoring {len(to_restore)} package(s)...", Colors.CYAN))
        restored = 0
        for p in to_restore:
            p_name = pkg_map.get(p, {}).get("name", p)
            print(f"  Restoring {p_name} ({p})... ", end="", flush=True)
            success, msg = self.adb.restore_package(p, self.active_serial)
            if success:
                restored += 1
                utils.remove_from_debloat_history(p)
                print(colorize("RESTORED", Colors.GREEN))
            else:
                print(colorize(f"FAILED ({msg})", Colors.RED))

        print(colorize(f"\n[✓] Successfully restored {restored}/{len(to_restore)} package(s).", Colors.GREEN))

    def menu_presets(self):
        presets = utils.load_presets()
        if not presets:
            print(colorize("[!] No presets found in presets.json", Colors.RED))
            return

        print(colorize("\n=== ONE-CLICK OPTIMIZATION PRESETS ===", Colors.CYAN))
        for i, preset in enumerate(presets, 1):
            print(f"\n  {colorize(str(i) + '. ' + preset['name'], Colors.BOLD)}")
            print(f"     {preset['description']}")
            print(f"     Target packages: {len(preset['packages'])}")

        print("\n  0. Return to Main Menu")
        choice = input("\nSelect preset number [1-{}]: ".format(len(presets))).strip()
        if choice == '0' or not choice:
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(presets):
                selected = presets[idx]
                print(f"\nSelected: {colorize(selected['name'], Colors.GREEN)}")
                mode_choice = input("Operation Mode: [1] Safe Disable (Default) | [2] Full User Uninstall: ").strip()
                mode = "uninstall" if mode_choice == "2" else "disable"

                if "perf" in selected["id"] or "performance" in selected["id"]:
                    tweak_choice = input("Apply 0.5x Animation Speed Tweak for Exynos 1380? [Y/n]: ").strip().lower()
                    if not tweak_choice or tweak_choice == 'y':
                        if self.active_serial:
                            self.adb.set_animation_scale(0.5, self.active_serial)
                            print(colorize("[✓] Animation speed set to 0.5x!", Colors.GREEN))

                self.run_debloat(selected["packages"], mode=mode)
            else:
                print("Invalid number.")
        except ValueError:
            print("Invalid input.")

    def menu_categories(self):
        installed = set(self.adb.get_installed_packages(self.active_serial)) if self.active_serial else set()
        
        print(colorize("\n=== PACKAGE CATEGORY BROWSER ===", Colors.CYAN))
        cat_keys = list(database.CATEGORIES.keys())
        for i, k in enumerate(cat_keys, 1):
            pkgs = database.get_packages_by_category(k)
            installed_in_cat = sum(1 for p in pkgs if p["id"] in installed)
            tag = colorize(f"({installed_in_cat}/{len(pkgs)} active)", Colors.YELLOW if installed_in_cat > 0 else Colors.RESET)
            desc = database.CATEGORIES[k]
            if k == "tablet_critical":
                desc = colorize(desc, Colors.RED)
            print(f"  {i}. {desc} {tag}")

        print("  0. Back")
        choice = input(f"\nSelect category [1-{len(cat_keys)}]: ").strip()
        if choice == '0' or not choice:
            return

        try:
            c_idx = int(choice) - 1
            if 0 <= c_idx < len(cat_keys):
                cat_key = cat_keys[c_idx]
                self._browse_category_packages(cat_key, installed)
        except ValueError:
            pass

    def _browse_category_packages(self, category_key: str, installed: set):
        pkgs = database.get_packages_by_category(category_key)
        cat_name = database.CATEGORIES[category_key]
        print(colorize(f"\n=== {cat_name} ===", Colors.CYAN))

        for i, p in enumerate(pkgs, 1):
            status = colorize("[INSTALLED]", Colors.GREEN) if p["id"] in installed else colorize("[NOT ACTIVE]", Colors.RESET)
            risk_color = Colors.GREEN if p["risk"] == "safe" else (Colors.YELLOW if p["risk"] == "optional" else Colors.RED)
            risk_badge = colorize(f"[{p['risk'].upper()}]", risk_color)
            print(f"  {i}. {status} {risk_badge} {colorize(p['name'], Colors.BOLD)}")
            print(f"     Package: {p['id']}")
            print(f"     Details: {p['description']}\n")

        print("  A. Select ALL installed in this category")
        print("  0. Back")
        choice = input("Enter package numbers separated by comma, 'A' for all, or 0 to back: ").strip().lower()
        if choice == '0' or not choice:
            return

        to_debloat = []
        if choice == 'a':
            to_debloat = [p["id"] for p in pkgs if p["id"] in installed]
        else:
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(",") if x.strip().isdigit()]
                to_debloat = [pkgs[idx]["id"] for idx in indices if 0 <= idx < len(pkgs)]
            except Exception:
                print("Invalid input.")
                return

        if to_debloat:
            mode_choice = input("Operation Mode: [1] Safe Disable (Default) | [2] Full User Uninstall: ").strip()
            mode = "uninstall" if mode_choice == "2" else "disable"
            self.run_debloat(to_debloat, mode=mode)

    def menu_tweaks(self):
        print(colorize("\n=== SAMSUNG TAB S9 FE PERFORMANCE TWEAKS ===", Colors.CYAN))
        print("  1. Set Animation Scales to 0.5x (Significantly boosts UI responsiveness on Exynos 1380)")
        print("  2. Reset Animation Scales to 1.0x (Default)")
        print("  3. Set Animation Scales to 0.25x (Lightning speed)")
        print("  4. Reboot Tablet into System")
        print("  0. Back")

        choice = input("\nSelect tweak [1-4]: ").strip()
        if choice == '1':
            success = self.adb.set_animation_scale(0.5, self.active_serial)
            print(colorize("[✓] Animation speed set to 0.5x!" if success else "[X] Failed to set animation scale.", Colors.GREEN if success else Colors.RED))
        elif choice == '2':
            success = self.adb.set_animation_scale(1.0, self.active_serial)
            print(colorize("[✓] Animation speed reset to 1.0x!" if success else "[X] Failed to reset animation scale.", Colors.GREEN if success else Colors.RED))
        elif choice == '3':
            success = self.adb.set_animation_scale(0.25, self.active_serial)
            print(colorize("[✓] Animation speed set to 0.25x!" if success else "[X] Failed.", Colors.GREEN if success else Colors.RED))
        elif choice == '4':
            print("Rebooting tablet...")
            self.adb.reboot_device(self.active_serial)

    def interactive_menu(self):
        while True:
            self.refresh_connection()
            self.print_banner()
            self.print_device_card()

            print(colorize("\n┌─[ MAIN MENU ]────────────────────────────────────────────────┐", Colors.BOLD))
            print("│  1. Presets (Recommended Safe Debloat, Exynos 1380 Optimizer)│")
            print("│  2. Browse Packages by Category (Custom Pick & Choose)       │")
            print("│  3. Restore Center (Reinstall / Re-enable Removed Packages)  │")
            print("│  4. Performance Tweaks (0.5x Animation Speed, Reboot)        │")
            print("│  5. Launch Desktop Graphical User Interface (GUI)            │")
            print("│  S. ☕ Support Project (Buy Me a Coffee)                      │")
            print("│  R. Refresh Device Connection                                │")
            print("│  0. Exit                                                     │")
            print(colorize("└──────────────────────────────────────────────────────────────┘", Colors.BOLD))

            choice = input("\nSelect option [0-5, S, R]: ").strip().upper()
            if choice == '0':
                print("Goodbye!")
                break
            elif choice == 'S':
                import webbrowser
                print(colorize("\nOpening https://buymeacoffee.com/kavangcb29 in your browser... Thank you for your support!", Colors.GREEN))
                webbrowser.open("https://buymeacoffee.com/kavangcb29")
            elif choice == '1':
                self.menu_presets()
            elif choice == '2':
                self.menu_categories()
            elif choice == '3':
                self.run_restore()
            elif choice == '4':
                self.menu_tweaks()
            elif choice == '5':
                launch_gui()
            elif choice == 'R':
                continue
            
            input("\nPress Enter to continue...")

def launch_gui():
    try:
        import gui
        gui.main()
    except Exception as e:
        print(colorize(f"Error launching GUI: {e}", Colors.RED))

def main():
    parser = argparse.ArgumentParser(description="Samsung Galaxy Tab S9 FE Debloater Toolkit")
    parser.add_argument("--gui", action="store_true", help="Launch Graphical User Interface")
    parser.add_argument("--cli", action="store_true", help="Launch Interactive Terminal Interface")
    parser.add_argument("--preset", type=str, help="Run a specific preset (e.g. 'safe_recommended', 'exynos_performance')")
    parser.add_argument("--restore-all", action="store_true", help="Restore all previously debloated packages")
    parser.add_argument("--tweaks", action="store_true", help="Apply 0.5x animation scale tweak for Exynos 1380")
    args = parser.parse_args()

    app = TabS9FEDebloater()
    app.refresh_connection()

    if args.gui:
        launch_gui()
        return

    if args.preset:
        presets = utils.load_presets()
        target = next((p for p in presets if p["id"] == args.preset), None)
        if target:
            print(f"Applying preset: {target['name']}")
            app.run_debloat(target["packages"], mode="disable")
        else:
            print(f"Preset '{args.preset}' not found. Available: {[p['id'] for p in presets]}")
        return

    if args.restore_all:
        app.run_restore()
        return

    if args.tweaks:
        if app.active_serial:
            app.adb.set_animation_scale(0.5, app.active_serial)
            print("[✓] Animation scales set to 0.5x.")
        else:
            print("[!] Tablet not connected.")
        return

    # If no specific flags, launch GUI by default if on Windows desktop or launch CLI
    if args.cli:
        app.interactive_menu()
    else:
        # Default behavior when run directly or double-clicked: launch GUI!
        launch_gui()

if __name__ == "__main__":
    main()
