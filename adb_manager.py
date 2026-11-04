"""
Samsung Tab S9 FE Debloater - ADB Manager
Handles ADB detection, automatic downloading of Google platform-tools, device discovery,
and safe package execution (uninstall, disable, restore).
"""

import os
import sys
import subprocess
import zipfile
import urllib.request
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Callable

GOOGLE_PLATFORM_TOOLS_URL = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"

class ADBManager:
    def __init__(self, workspace_dir: Optional[Path] = None):
        self.workspace_dir = workspace_dir or Path(__file__).resolve().parent
        self.bin_dir = self.workspace_dir / "bin"
        self.local_adb_path = self.bin_dir / "platform-tools" / "adb.exe"
        self._adb_cmd: Optional[str] = None
        self.locate_adb()

    def locate_adb(self) -> Optional[str]:
        """Finds adb executable in local bin, system PATH, or common Android SDK folders."""
        # 1. Local bin in project
        if self.local_adb_path.is_file():
            self._adb_cmd = str(self.local_adb_path)
            return self._adb_cmd

        # 2. Check if adb is in system PATH
        try:
            res = subprocess.run(
                ["adb", "version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
                timeout=5
            )
            if res.returncode == 0:
                self._adb_cmd = "adb"
                return self._adb_cmd
        except (FileNotFoundError, subprocess.SubprocessError):
            pass

        # 3. Check AppData Android SDK
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        if local_app_data:
            candidate = Path(local_app_data) / "Android" / "Sdk" / "platform-tools" / "adb.exe"
            if candidate.is_file():
                self._adb_cmd = str(candidate)
                return self._adb_cmd

        self._adb_cmd = None
        return None

    def is_adb_installed(self) -> bool:
        return self._adb_cmd is not None

    def download_platform_tools(self, progress_callback: Optional[Callable[[int, int], None]] = None) -> bool:
        """Downloads official Google Android platform-tools zip and unpacks it locally."""
        self.bin_dir.mkdir(parents=True, exist_ok=True)
        zip_dest = self.bin_dir / "platform-tools.zip"

        try:
            req = urllib.request.Request(
                GOOGLE_PLATFORM_TOOLS_URL,
                headers={"User-Agent": "SamsungTabS9FEDebloater/1.0"}
            )
            with urllib.request.urlopen(req, timeout=30) as response, open(zip_dest, "wb") as out_file:
                total_size = int(response.headers.get("Content-Length", 0))
                downloaded = 0
                chunk_size = 1024 * 64

                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    out_file.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback and total_size > 0:
                        progress_callback(downloaded, total_size)

            # Unpack zip
            with zipfile.ZipFile(zip_dest, "r") as zip_ref:
                zip_ref.extractall(self.bin_dir)

            # Clean up zip
            if zip_dest.exists():
                zip_dest.unlink()

            self.locate_adb()
            return self.is_adb_installed()
        except Exception as e:
            if zip_dest.exists():
                try:
                    zip_dest.unlink()
                except Exception:
                    pass
            raise RuntimeError(f"Failed to download platform-tools: {e}")

    def run_command(self, args: List[str], timeout: int = 15) -> Tuple[int, str, str]:
        """Runs an adb command safely without opening command windows."""
        if not self._adb_cmd:
            raise RuntimeError("ADB is not found. Please install or download platform-tools.")

        cmd = [self._adb_cmd] + args
        creation_flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0

        try:
            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=creation_flags,
                timeout=timeout
            )
            return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out."
        except Exception as e:
            return -1, "", str(e)

    def run_shell(self, shell_command: str, serial: Optional[str] = None, timeout: int = 15) -> Tuple[int, str, str]:
        """Runs a command inside `adb shell`."""
        args = []
        if serial:
            args.extend(["-s", serial])
        args.extend(["shell", shell_command])
        return self.run_command(args, timeout=timeout)

    def get_connected_devices(self) -> List[Dict[str, str]]:
        """Returns list of connected devices with status."""
        code, stdout, stderr = self.run_command(["devices"])
        if code != 0:
            return []

        devices = []
        lines = stdout.splitlines()
        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) >= 2:
                serial, status = parts[0], parts[1]
                devices.append({
                    "serial": serial,
                    "status": status  # 'device', 'unauthorized', 'offline', etc.
                })
        return devices

    def get_device_info(self, serial: Optional[str] = None) -> Dict[str, str]:
        """Fetches device model, Android release, One UI version, and battery."""
        info = {
            "model": "Unknown",
            "market_name": "Samsung Device",
            "android_version": "Unknown",
            "oneui_version": "Unknown",
            "battery": "Unknown",
            "is_tab_s9_fe": False,
            "serial": serial or ""
        }

        # Model: e.g. SM-X510 (Wi-Fi), SM-X516B (5G)
        code, out, _ = self.run_shell("getprop ro.product.model", serial=serial)
        if code == 0 and out:
            info["model"] = out.strip()

        # Product name
        code, out, _ = self.run_shell("getprop ro.product.name", serial=serial)
        prod_name = out.strip().lower() if code == 0 else ""

        # CSC / Sales code (e.g. INS, INU for Indian variant)
        code_csc, out_csc, _ = self.run_shell("getprop ro.csc.sales_code", serial=serial)
        if code_csc != 0 or not out_csc.strip():
            code_csc, out_csc, _ = self.run_shell("getprop ro.boot.sales_code", serial=serial)
        csc_val = out_csc.strip().upper() if code_csc == 0 and out_csc else ""
        if csc_val:
            info["csc"] = csc_val
            if csc_val in ("INS", "INU"):
                info["region"] = "India (INS/INU)"
                info["is_indian_variant"] = True
            else:
                info["region"] = csc_val

        # Check Tab S9 FE recognition
        # SM-X510: Tab S9 FE Wi-Fi
        # SM-X516 / SM-X516B: Tab S9 FE 5G (SM-X516B is the Indian 5G variant)
        # SM-X610: Tab S9 FE+ Wi-Fi
        # SM-X616 / SM-X616B: Tab S9 FE+ 5G
        model_upper = info["model"].upper()
        if "X510" in model_upper:
            info["market_name"] = "Galaxy Tab S9 FE (Wi-Fi)"
            info["is_tab_s9_fe"] = True
        elif "X516" in model_upper:
            info["market_name"] = "Galaxy Tab S9 FE (5G)"
            info["is_tab_s9_fe"] = True
        elif "X610" in model_upper:
            info["market_name"] = "Galaxy Tab S9 FE+ (Wi-Fi)"
            info["is_tab_s9_fe"] = True
        elif "X616" in model_upper:
            info["market_name"] = "Galaxy Tab S9 FE+ (5G)"
            info["is_tab_s9_fe"] = True
        elif "gts9fe" in prod_name or "gts9pfe" in prod_name or "X51" in model_upper or "X61" in model_upper:
            info["market_name"] = "Galaxy Tab S9 FE Series"
            info["is_tab_s9_fe"] = True
        elif "X710" in model_upper or "X716" in model_upper:
            info["market_name"] = "Galaxy Tab S9"
        elif "X810" in model_upper or "X816" in model_upper:
            info["market_name"] = "Galaxy Tab S9+"
        elif "X910" in model_upper or "X916" in model_upper:
            info["market_name"] = "Galaxy Tab S9 Ultra"
        else:
            info["market_name"] = f"Samsung ({info['model']})"

        if info.get("is_indian_variant"):
            info["market_name"] += " [India Variant]"

        # Android Version
        code, out, _ = self.run_shell("getprop ro.build.version.release", serial=serial)
        if code == 0 and out:
            info["android_version"] = out.strip()

        # One UI Version (supports One UI 5, 6, 7, 8, 8.5, and 9+)
        info["oneui_version"] = self._detect_oneui_version(serial=serial)

        # Battery percentage
        code, out, _ = self.run_shell("dumpsys battery", serial=serial)
        if code == 0 and out:
            level_match = re.search(r"level:\s*(\d+)", out)
            if level_match:
                info["battery"] = f"{level_match.group(1)}%"

        return info

    def _detect_oneui_version(self, serial: Optional[str] = None) -> str:
        """
        Detects Samsung One UI version across One UI 5, 6, 7, 8, 8.5, and 9+.
        Checks ro.build.version.oneui, ro.build.version.sep, ro.build.version.sem, and ro.sem.version.
        """
        def parse_raw(raw_str: str, is_sep: bool = False) -> Optional[str]:
            raw = raw_str.strip()
            if not raw:
                return None
            if raw.isdigit():
                val = int(raw)
                major = (val // 10000) - (9 if is_sep else 0)
                rem = val % 10000
                minor = rem // 100
                sub = rem % 100
                if major > 0:
                    return f"{major}.{minor}.{sub}" if sub > 0 else f"{major}.{minor}"
            elif "." in raw:
                m = re.search(r"(\d+(?:\.\d+)?)", raw)
                if m:
                    return m.group(1)
            return None

        # 1. Try ro.build.version.oneui (e.g. 80500 for One UI 8.5, 80000 for 8.0, 90000 for 9.0)
        code, out, _ = self.run_shell("getprop ro.build.version.oneui", serial=serial)
        if code == 0 and out.strip():
            ver = parse_raw(out, is_sep=False)
            if ver:
                return ver

        # 2. Try ro.build.version.sep (SEP version offset by 9: 150000=6.0, 150100=6.1, 160000=7.0, 170000=8.0, 170500=8.5, 180000=9.0)
        code, out, _ = self.run_shell("getprop ro.build.version.sep", serial=serial)
        if code == 0 and out.strip():
            ver = parse_raw(out, is_sep=True)
            if ver:
                return ver

        # 3. Fallback to ro.build.version.sem
        code, out_sem, _ = self.run_shell("getprop ro.build.version.sem", serial=serial)
        if code == 0 and out_sem.strip():
            ver = parse_raw(out_sem, is_sep=True)
            if ver:
                return ver

        # 4. Fallback to ro.sem.version
        code, out_rsem, _ = self.run_shell("getprop ro.sem.version", serial=serial)
        if code == 0 and out_rsem.strip():
            ver = parse_raw(out_rsem, is_sep=True)
            if ver:
                return ver

        return "Unknown"

    def get_installed_packages(self, serial: Optional[str] = None) -> List[str]:
        """Returns list of currently active package names for user 0."""
        code, out, _ = self.run_shell("pm list packages --user 0", serial=serial)
        if code != 0:
            # Fallback
            code, out, _ = self.run_shell("pm list packages", serial=serial)
        
        packages = []
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("package:"):
                packages.append(line.replace("package:", "").strip())
        return packages

    def get_uninstalled_or_disabled_packages(self, serial: Optional[str] = None) -> List[str]:
        """Returns list of packages disabled or uninstalled for user 0."""
        # Disabled
        code, out, _ = self.run_shell("pm list packages -d --user 0", serial=serial)
        disabled = []
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("package:"):
                disabled.append(line.replace("package:", "").strip())

        # Uninstalled for user 0:
        # All packages on device (-u) minus active packages
        code, out_all, _ = self.run_shell("pm list packages -u", serial=serial)
        all_pkgs = set()
        for line in out_all.splitlines():
            line = line.strip()
            if line.startswith("package:"):
                all_pkgs.add(line.replace("package:", "").strip())

        active = set(self.get_installed_packages(serial=serial))
        uninstalled_user0 = list(all_pkgs - active)

        # Union of uninstalled and disabled
        return sorted(list(set(disabled + uninstalled_user0)))

    def uninstall_package(self, package_id: str, keep_data: bool = True, serial: Optional[str] = None) -> Tuple[bool, str]:
        """
        Uninstalls package for user 0 (keeps system apk). Fully reversible via restore_package.
        Features multi-layer fallback for One UI 7 / 8 / 8.5 / 9 compatibility.
        """
        kd_flag = "-k " if keep_data else ""
        cmd = f"pm uninstall {kd_flag}--user 0 {package_id}"
        code, stdout, stderr = self.run_shell(cmd, serial=serial)
        
        combined = f"{stdout} {stderr}".lower()
        if "success" in combined:
            return True, "Successfully uninstalled for current user."
        elif "not installed" in combined:
            return True, "Package was already not installed."

        # Fallback 1: If -k failed (newer Android versions sometimes reject -k for system apks)
        if keep_data:
            cmd2 = f"pm uninstall --user 0 {package_id}"
            code2, stdout2, stderr2 = self.run_shell(cmd2, serial=serial)
            comb2 = f"{stdout2} {stderr2}".lower()
            if "success" in comb2:
                return True, "Successfully uninstalled for current user."
            elif "not installed" in comb2:
                return True, "Package was already not installed."

        # Fallback 2: If uninstall is restricted by Knox or Device Policy on One UI 8.5+, disable the package
        cmd3 = f"pm disable-user --user 0 {package_id}"
        code3, stdout3, stderr3 = self.run_shell(cmd3, serial=serial)
        comb3 = f"{stdout3} {stderr3}".lower()
        if "new state: disabled" in comb3 or "disabled-user" in comb3 or code3 == 0:
            return True, "Package disabled for user 0 (uninstall restricted by system)."

        return False, stdout or stderr or "Unknown failure"

    def disable_package(self, package_id: str, serial: Optional[str] = None) -> Tuple[bool, str]:
        """Disables package for user 0. App stops running immediately; reversible via pm enable."""
        cmd = f"pm disable-user --user 0 {package_id}"
        code, stdout, stderr = self.run_shell(cmd, serial=serial)
        combined = f"{stdout} {stderr}".lower()
        if "new state: disabled" in combined or "disabled-user" in combined or code == 0:
            return True, "Package successfully disabled."
        return False, stdout or stderr or "Failed to disable package"

    def restore_package(self, package_id: str, serial: Optional[str] = None) -> Tuple[bool, str]:
        """
        Re-enables and reinstalls an uninstalled or disabled package for user 0.
        Compatible across all One UI & Android versions (One UI 5 - 9+).
        """
        # 1. Try cmd package install-existing
        cmd_install = f"cmd package install-existing {package_id}"
        code_i, out_i, err_i = self.run_shell(cmd_install, serial=serial)

        # 2. Fallback pm install-existing --user 0
        if "installed" not in f"{out_i}".lower() and code_i != 0:
            cmd_pm = f"pm install-existing --user 0 {package_id}"
            self.run_shell(cmd_pm, serial=serial)

        # 3. Enable package for user 0
        cmd_enable = f"pm enable --user 0 {package_id}"
        code_e, out_e, err_e = self.run_shell(cmd_enable, serial=serial)

        # 4. Fallback cmd package enable-user
        if code_e != 0:
            self.run_shell(f"cmd package enable-user --user 0 {package_id}", serial=serial)

        combined = f"{out_i} {err_i} {out_e} {err_e}".lower()
        if "installed" in combined or "enabled" in combined or "success" in combined or code_i == 0 or code_e == 0:
            return True, "Successfully restored/enabled package."
        return False, f"Install: {out_i or err_i} | Enable: {out_e or err_e}"

    def diagnose_device(self, serial: Optional[str] = None) -> Dict[str, Any]:
        """
        Runs comprehensive connection & environment diagnostics for the Setup Guide.
        """
        diag = {
            "adb_installed": self.is_adb_installed(),
            "devices": self.get_connected_devices(),
            "active_device": None,
            "device_info": None,
            "diagnostic_summary": []
        }
        
        if not diag["adb_installed"]:
            diag["diagnostic_summary"].append("ADB executable is missing or not initialized.")
            return diag

        if not diag["devices"]:
            diag["diagnostic_summary"].append("No ADB devices detected over USB.")
            diag["diagnostic_summary"].append("Check: USB-C cable, Developer options > USB Debugging.")
            diag["diagnostic_summary"].append("Samsung Auto Blocker: Settings -> Security and privacy -> Auto Blocker -> Turn OFF.")
            return diag

        unauth = [d for d in diag["devices"] if d["status"] == "unauthorized"]
        if unauth:
            diag["diagnostic_summary"].append(f"Device [{unauth[0]['serial']}] is UNAUTHORIZED.")
            diag["diagnostic_summary"].append("Unlock tablet screen and tap 'Always allow from this computer'.")
            return diag

        active = [d for d in diag["devices"] if d["status"] == "device"]
        if active:
            target_serial = serial or active[0]["serial"]
            diag["active_device"] = target_serial
            info = self.get_device_info(target_serial)
            diag["device_info"] = info
            diag["diagnostic_summary"].append(f"Connected: {info['market_name']} ({info['model']})")
            diag["diagnostic_summary"].append(f"One UI Version: {info['oneui_version']} | Android: {info['android_version']}")
            if info.get("csc"):
                diag["diagnostic_summary"].append(f"Region / Sales Code (CSC): {info['csc']}")
            diag["diagnostic_summary"].append("Device Status: 100% Ready for Optimization!")
        
        return diag

    def set_animation_scale(self, scale: float = 0.5, serial: Optional[str] = None) -> bool:
        """Sets window, transition, and animator scales (e.g. 0.5 for instant responsiveness)."""
        scale_str = str(scale)
        s1, _, _ = self.run_shell(f"settings put global window_animation_scale {scale_str}", serial=serial)
        s2, _, _ = self.run_shell(f"settings put global transition_animation_scale {scale_str}", serial=serial)
        s3, _, _ = self.run_shell(f"settings put global animator_duration_scale {scale_str}", serial=serial)
        return (s1 == 0 and s2 == 0 and s3 == 0)

    def reboot_device(self, serial: Optional[str] = None) -> Tuple[int, str, str]:
        args = []
        if serial:
            args.extend(["-s", serial])
        args.append("reboot")
        return self.run_command(args)
