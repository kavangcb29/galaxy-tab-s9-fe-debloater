"""
Samsung Tab S9 FE Debloater - Utilities
Handles backup snapshots, restore history logging, and configuration presets.
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

BACKUP_DIR = Path(__file__).resolve().parent / "backups"
HISTORY_FILE = BACKUP_DIR / "debloat_history.json"
PRESETS_FILE = Path(__file__).resolve().parent / "presets.json"

def ensure_backup_dir() -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    return BACKUP_DIR

def create_backup_snapshot(device_info: Dict[str, Any], installed_packages: List[str]) -> Path:
    """Creates a timestamped snapshot of installed packages before debloating."""
    ensure_backup_dir()
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    model = device_info.get("model", "Device").replace(" ", "_")
    filename = f"backup_{model}_{timestamp}.json"
    dest = BACKUP_DIR / filename

    data = {
        "timestamp": timestamp,
        "date_human": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device_info": device_info,
        "package_count": len(installed_packages),
        "installed_packages": sorted(installed_packages)
    }

    with open(dest, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return dest

def log_debloat_action(package_id: str, mode: str, status: bool, note: str = ""):
    """Logs debloated packages into history for 1-click restoration tracking."""
    ensure_backup_dir()
    history = load_debloat_history()
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "package_id": package_id,
        "mode": mode,
        "success": status,
        "timestamp": timestamp,
        "note": note
    }
    
    # Store or update entry
    history[package_id] = entry
    
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def remove_from_debloat_history(package_id: str):
    """Removes a package from history once successfully restored."""
    history = load_debloat_history()
    if package_id in history:
        del history[package_id]
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

def load_debloat_history() -> Dict[str, Any]:
    """Loads history of packages removed or disabled by this tool."""
    if not HISTORY_FILE.exists():
        return {}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def load_presets() -> List[Dict[str, Any]]:
    """Loads presets from presets.json."""
    if not PRESETS_FILE.exists():
        return []
    try:
        with open(PRESETS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("presets", [])
    except Exception:
        return []
