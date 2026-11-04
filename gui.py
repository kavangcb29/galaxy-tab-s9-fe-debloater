"""
Samsung Tab S9 FE Debloater - Modern Graphical User Interface (GUI)
Built with Python Tkinter/ttk with a sleek dark theme and responsive threading.
"""

import os
import sys
import threading
import time
from pathlib import Path

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

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, List, Optional, Set, Any

from adb_manager import ADBManager
import database
import utils

# Modern Dark Theme Palette
BG_DARK = "#121417"
BG_CARD = "#1a1f26"
BG_CARD_LIGHT = "#242b35"
BORDER_COLOR = "#2d3748"
TEXT_PRIMARY = "#f7fafc"
TEXT_SECONDARY = "#a0aec0"
TEXT_MUTED = "#718096"
ACCENT_BLUE = "#3182ce"
ACCENT_BLUE_HOVER = "#2b6cb0"
ACCENT_GREEN = "#38a169"
ACCENT_YELLOW = "#d69e2e"
ACCENT_RED = "#e53e3e"

class DebloaterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Samsung Galaxy Tab S9 FE Debloater Toolkit")
        self.geometry("1020x720")
        self.minsize(860, 580)
        self.configure(bg=BG_DARK)

        self.adb = ADBManager()
        self.device_info: Dict[str, Any] = {}
        self.active_serial: Optional[str] = None
        self.installed_packages: Set[str] = set()
        
        # Package Selection State: package_id -> tk.BooleanVar
        self.package_vars: Dict[str, tk.BooleanVar] = {}
        
        # Setup modern TTK Styles
        self._setup_styles()
        
        # Build UI layout
        self._build_header()
        self._build_notebook()
        self._build_console()

        # Start background device connection monitor
        self.after(300, self.async_refresh_device)

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Configure Base Styles
        style.configure(".", background=BG_DARK, foreground=TEXT_PRIMARY, font=("Segoe UI", 9))
        
        # Tabs Style
        style.configure("TNotebook", background=BG_DARK, borderwidth=0)
        style.configure("TNotebook.Tab", 
                        background=BG_CARD, 
                        foreground=TEXT_SECONDARY, 
                        padding=[16, 8],
                        font=("Segoe UI", 10, "bold"),
                        borderwidth=0)
        style.map("TNotebook.Tab", 
                  background=[("selected", BG_CARD_LIGHT), ("active", BG_CARD_LIGHT)],
                  foreground=[("selected", TEXT_PRIMARY), ("active", TEXT_PRIMARY)])

        # Treeview / Table
        style.configure("Treeview", 
                        background=BG_CARD, 
                        foreground=TEXT_PRIMARY, 
                        fieldbackground=BG_CARD,
                        rowheight=26,
                        font=("Segoe UI", 9),
                        borderwidth=0)
        style.configure("Treeview.Heading",
                        background=BG_CARD_LIGHT,
                        foreground=TEXT_PRIMARY,
                        font=("Segoe UI", 9, "bold"),
                        padding=[8, 6],
                        borderwidth=0)
        style.map("Treeview", background=[("selected", ACCENT_BLUE)])

        # Checkbutton
        style.configure("TCheckbutton", background=BG_CARD, foreground=TEXT_PRIMARY)
        style.map("TCheckbutton", background=[("active", BG_CARD)])

        # Combobox
        style.configure("TCombobox", 
                        fieldbackground=BG_CARD_LIGHT, 
                        background=BG_CARD_LIGHT, 
                        foreground=TEXT_PRIMARY,
                        arrowcolor=TEXT_PRIMARY)

    def _build_header(self):
        self.header_frame = tk.Frame(self, bg=BG_CARD, height=85, highlightbackground=BORDER_COLOR, highlightthickness=1)
        self.header_frame.pack(fill=tk.X, padx=14, pady=(14, 8))
        self.header_frame.pack_propagate(False)

        # Title & Subtitle Container
        left_box = tk.Frame(self.header_frame, bg=BG_CARD)
        left_box.pack(side=tk.LEFT, padx=16, pady=10)

        title_lbl = tk.Label(left_box, text="SAMSUNG TAB S9 FE DEBLOATER", font=("Segoe UI", 13, "bold"), fg=TEXT_PRIMARY, bg=BG_CARD)
        title_lbl.pack(anchor="w")

        subtitle_lbl = tk.Label(left_box, text="One UI 6+ Exynos 1380 Optimizer • S Pen & DeX Safe Protection", 
                                font=("Segoe UI", 8), fg=TEXT_SECONDARY, bg=BG_CARD)
        subtitle_lbl.pack(anchor="w")

        # Right Device Status Card
        self.device_badge_frame = tk.Frame(self.header_frame, bg=BG_CARD_LIGHT, highlightbackground=BORDER_COLOR, highlightthickness=1, padx=12, pady=6)
        self.device_badge_frame.pack(side=tk.RIGHT, padx=16, pady=10)

        self.device_status_lbl = tk.Label(self.device_badge_frame, text="Detecting device...", font=("Segoe UI", 9, "bold"), fg=ACCENT_YELLOW, bg=BG_CARD_LIGHT)
        self.device_status_lbl.pack(anchor="e")

        self.device_detail_lbl = tk.Label(self.device_badge_frame, text="Please connect via USB with USB Debugging enabled", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD_LIGHT)
        self.device_detail_lbl.pack(anchor="e")

        # Refresh button
        self.btn_refresh = tk.Button(self.header_frame, text="↻ Refresh", font=("Segoe UI", 9), 
                                     bg=BG_CARD_LIGHT, fg=TEXT_PRIMARY, activebackground=BORDER_COLOR,
                                     activeforeground=TEXT_PRIMARY, relief=tk.FLAT, bd=0, padx=10, pady=4,
                                     command=self.async_refresh_device)
        self.btn_refresh.pack(side=tk.RIGHT, padx=(0, 10))

    def _build_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=14, pady=6)

        # Tabs
        self.tab_presets = tk.Frame(self.notebook, bg=BG_DARK)
        self.tab_packages = tk.Frame(self.notebook, bg=BG_DARK)
        self.tab_restore = tk.Frame(self.notebook, bg=BG_DARK)
        self.tab_tweaks = tk.Frame(self.notebook, bg=BG_DARK)

        self.notebook.add(self.tab_presets, text="   1-Click Presets   ")
        self.notebook.add(self.tab_packages, text="   Custom Package Manager   ")
        self.notebook.add(self.tab_restore, text="   Restore Center   ")
        self.notebook.add(self.tab_tweaks, text="   Tab S9 FE Tweaks   ")

        self._populate_presets_tab()
        self._populate_packages_tab()
        self._populate_restore_tab()
        self._populate_tweaks_tab()

    def _build_console(self):
        console_frame = tk.Frame(self, bg=BG_CARD, height=130, highlightbackground=BORDER_COLOR, highlightthickness=1)
        console_frame.pack(fill=tk.X, padx=14, pady=(6, 14))
        console_frame.pack_propagate(False)

        top_bar = tk.Frame(console_frame, bg=BG_CARD)
        top_bar.pack(fill=tk.X, padx=10, pady=(4, 2))

        c_title = tk.Label(top_bar, text="EXECUTION LOGS & ADB CONSOLE", font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_CARD)
        c_title.pack(side=tk.LEFT)

        btn_clear = tk.Button(top_bar, text="Clear Logs", font=("Segoe UI", 7), bg=BG_CARD_LIGHT, fg=TEXT_SECONDARY,
                              relief=tk.FLAT, bd=0, command=self.clear_log)
        btn_clear.pack(side=tk.RIGHT)

        self.log_text = tk.Text(console_frame, bg="#0d0f12", fg="#38ef7d", font=("Consolas", 8),
                                bd=0, padx=8, pady=4, state=tk.DISABLED, wrap=tk.CHAR)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 6))

    def log(self, message: str, level: str = "INFO"):
        timestamp = time.strftime("%H:%M:%S")
        formatted = f"[{timestamp}] [{level}] {message}\n"
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, formatted)
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def clear_log(self):
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.configure(state=tk.DISABLED)

    # ==========================================
    # Device Detection & Monitoring
    # ==========================================
    def async_refresh_device(self):
        def worker():
            self.log("Scanning for connected Android devices via ADB...")
            if not self.adb.is_adb_installed():
                self.log("ADB executable not found. Downloading Google platform-tools...")
                try:
                    self.adb.download_platform_tools()
                    self.log("Google platform-tools downloaded and ready!")
                except Exception as e:
                    self.log(f"Failed to auto-download ADB: {e}", "ERROR")
                    self._update_device_ui_disconnected()
                    return

            devices = self.adb.get_connected_devices()
            if not devices:
                self._update_device_ui_disconnected()
                return

            active = [d for d in devices if d["status"] == "device"]
            if not active:
                first = devices[0]
                self._update_device_ui_unauthorized(first["serial"], first["status"])
                return

            serial = active[0]["serial"]
            info = self.adb.get_device_info(serial)
            installed = set(self.adb.get_installed_packages(serial))
            
            self.device_info = info
            self.active_serial = serial
            self.installed_packages = installed

            self._update_device_ui_connected(info)
            self._refresh_package_list_view()
            self._refresh_restore_list_view()

        threading.Thread(target=worker, daemon=True).start()

    def _update_device_ui_disconnected(self):
        self.device_status_lbl.configure(text="No Device Connected", fg=ACCENT_RED)
        self.device_detail_lbl.configure(text="Connect Tab S9 FE with USB Debugging enabled")
        self.log("No device detected. Ensure USB Debugging is ON in Developer Options.", "WARN")

    def _update_device_ui_unauthorized(self, serial: str, status: str):
        self.device_status_lbl.configure(text=f"Device: {status.upper()}", fg=ACCENT_YELLOW)
        self.device_detail_lbl.configure(text="Unlock tablet screen & tap 'Always allow from this computer'")
        self.log(f"Device [{serial}] is unauthorized. Check tablet screen for prompt.", "WARN")

    def _update_device_ui_connected(self, info: Dict[str, Any]):
        market = info.get("market_name", "Samsung Device")
        model = info.get("model", "")
        android_v = info.get("android_version", "?")
        oneui_v = info.get("oneui_version", "?")
        battery = info.get("battery", "?")

        status_txt = f"✓ Connected: {market} ({model})"
        detail_txt = f"Android {android_v} | One UI {oneui_v} | Battery: {battery}"
        
        self.device_status_lbl.configure(text=status_txt, fg=ACCENT_GREEN)
        self.device_detail_lbl.configure(text=detail_txt)
        self.log(f"Connected to {market} [{model}] running One UI {oneui_v} (Android {android_v}).")

    # ==========================================
    # Tab 1: Presets View
    # ==========================================
    def _populate_presets_tab(self):
        presets = utils.load_presets()

        desc_lbl = tk.Label(self.tab_presets, text="Quick-start optimization presets tailored for Samsung tablets:",
                            font=("Segoe UI", 10), fg=TEXT_SECONDARY, bg=BG_DARK)
        desc_lbl.pack(anchor="w", padx=16, pady=(14, 8))

        canvas = tk.Canvas(self.tab_presets, bg=BG_DARK, bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.tab_presets, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG_DARK)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=960)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(16, 0), pady=6)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 16), pady=6)

        for preset in presets:
            self._create_preset_card(scroll_frame, preset)

    def _create_preset_card(self, parent: tk.Widget, preset: Dict[str, Any]):
        card = tk.Frame(parent, bg=BG_CARD, highlightbackground=BORDER_COLOR, highlightthickness=1)
        card.pack(fill=tk.X, expand=True, pady=6, padx=4)

        header = tk.Frame(card, bg=BG_CARD)
        header.pack(fill=tk.X, padx=12, pady=(10, 4))

        title = tk.Label(header, text=preset["name"], font=("Segoe UI", 11, "bold"), fg=TEXT_PRIMARY, bg=BG_CARD)
        title.pack(side=tk.LEFT)

        count_badge = tk.Label(header, text=f"{len(preset['packages'])} packages", font=("Segoe UI", 8),
                               fg=ACCENT_BLUE, bg=BG_CARD_LIGHT, padx=8, pady=2)
        count_badge.pack(side=tk.RIGHT)

        desc = tk.Label(card, text=preset["description"], font=("Segoe UI", 9), fg=TEXT_SECONDARY, bg=BG_CARD,
                        wraplength=700, justify=tk.LEFT)
        desc.pack(anchor="w", padx=12, pady=(0, 10))

        action_row = tk.Frame(card, bg=BG_CARD)
        action_row.pack(fill=tk.X, padx=12, pady=(0, 10))

        # Mode Selector
        mode_var = tk.StringVar(value="disable")
        rb_disable = tk.Radiobutton(action_row, text="Safe Disable (Recommended)", variable=mode_var, value="disable",
                                    font=("Segoe UI", 8), bg=BG_CARD, fg=TEXT_PRIMARY, selectcolor=BG_CARD_LIGHT, activebackground=BG_CARD)
        rb_disable.pack(side=tk.LEFT, padx=(0, 10))

        rb_uninstall = tk.Radiobutton(action_row, text="Full User Uninstall", variable=mode_var, value="uninstall",
                                      font=("Segoe UI", 8), bg=BG_CARD, fg=TEXT_PRIMARY, selectcolor=BG_CARD_LIGHT, activebackground=BG_CARD)
        rb_uninstall.pack(side=tk.LEFT, padx=(0, 12))

        # 0.5x animation speed tweak checkbox for performance presets
        tweak_var = tk.BooleanVar(value="perf" in preset["id"] or "performance" in preset["id"])
        cb_tweak = tk.Checkbutton(action_row, text="⚡ 0.5x Animation Tweak", variable=tweak_var,
                                  font=("Segoe UI", 8, "bold"), bg=BG_CARD, fg=ACCENT_YELLOW,
                                  selectcolor=BG_CARD_LIGHT, activebackground=BG_CARD)
        cb_tweak.pack(side=tk.LEFT)

        btn_run = tk.Button(action_row, text="Apply Preset ➔", font=("Segoe UI", 9, "bold"),
                            bg=ACCENT_BLUE, fg="#ffffff", activebackground=ACCENT_BLUE_HOVER,
                            activeforeground="#ffffff", relief=tk.FLAT, bd=0, padx=14, pady=5,
                            command=lambda p=preset, m=mode_var, t=tweak_var: self._execute_preset_action(p, m.get(), t.get()))
        btn_run.pack(side=tk.RIGHT)

    def _execute_preset_action(self, preset: Dict[str, Any], mode: str, apply_tweak: bool = False):
        if not self.active_serial:
            messagebox.showwarning("Device Not Connected", "Please connect your Samsung Tab S9 FE with USB Debugging enabled first.")
            return

        pkgs = preset["packages"]
        action_text = "Safe Disable" if mode == "disable" else "Full User 0 Uninstall"
        tweak_note = "\n⚡ Will also apply 0.5x Animation Speed Tweak." if apply_tweak else ""
        if not messagebox.askyesno("Confirm Debloat Preset", 
                                   f"Apply preset '{preset['name']}'?\n\nOperation: {action_text}\nTarget packages: {len(pkgs)}{tweak_note}\n\nA safety backup snapshot will be saved automatically."):
            return

        def worker():
            if apply_tweak and self.active_serial:
                self.adb.set_animation_scale(0.5, self.active_serial)
                self.log("⚡ Applied 0.5x Window & Transition Animation Scale tweak.")
            self._perform_debloat_packages(pkgs, mode)

        threading.Thread(target=worker, daemon=True).start()

    # ==========================================
    # Tab 2: Custom Package Manager
    # ==========================================
    def _populate_packages_tab(self):
        # Control Filter Bar
        control_frame = tk.Frame(self.tab_packages, bg=BG_CARD, highlightbackground=BORDER_COLOR, highlightthickness=1)
        control_frame.pack(fill=tk.X, padx=12, pady=(10, 6))

        # Category Filter
        lbl_cat = tk.Label(control_frame, text="Category:", font=("Segoe UI", 9, "bold"), fg=TEXT_PRIMARY, bg=BG_CARD)
        lbl_cat.pack(side=tk.LEFT, padx=(12, 6), pady=8)

        self.cat_var = tk.StringVar(value="All Categories")
        cat_options = ["All Categories"] + list(database.CATEGORIES.values())
        self.cat_combo = ttk.Combobox(control_frame, textvariable=self.cat_var, values=cat_options, state="readonly", width=32)
        self.cat_combo.pack(side=tk.LEFT, padx=(0, 16), pady=8)
        self.cat_combo.bind("<<ComboboxSelected>>", lambda e: self._filter_packages())

        # Search box
        lbl_search = tk.Label(control_frame, text="Search:", font=("Segoe UI", 9, "bold"), fg=TEXT_PRIMARY, bg=BG_CARD)
        lbl_search.pack(side=tk.LEFT, padx=(0, 6), pady=8)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self._filter_packages())
        search_entry = tk.Entry(control_frame, textvariable=self.search_var, bg=BG_CARD_LIGHT, fg=TEXT_PRIMARY,
                                insertbackground=TEXT_PRIMARY, bd=0, relief=tk.FLAT, font=("Segoe UI", 9), width=22)
        search_entry.pack(side=tk.LEFT, padx=(0, 12), pady=8, ipady=3)

        # Quick Select Buttons
        btn_select_safe = tk.Button(control_frame, text="Select All Safe", font=("Segoe UI", 8), bg=BG_CARD_LIGHT,
                                    fg=ACCENT_GREEN, relief=tk.FLAT, bd=0, padx=8, pady=3,
                                    command=lambda: self._set_selection_by_filter(safe_only=True))
        btn_select_safe.pack(side=tk.RIGHT, padx=6)

        btn_clear_sel = tk.Button(control_frame, text="Deselect All", font=("Segoe UI", 8), bg=BG_CARD_LIGHT,
                                  fg=TEXT_SECONDARY, relief=tk.FLAT, bd=0, padx=8, pady=3,
                                  command=lambda: self._set_selection_all(False))
        btn_clear_sel.pack(side=tk.RIGHT, padx=6)

        # Treeview / Table
        table_frame = tk.Frame(self.tab_packages, bg=BG_DARK)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=4)

        columns = ("select", "name", "id", "risk", "status", "category")
        self.pkg_tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="extended")
        
        self.pkg_tree.heading("select", text="✓", anchor=tk.CENTER)
        self.pkg_tree.heading("name", text="Application Name", anchor=tk.W)
        self.pkg_tree.heading("id", text="Package ID", anchor=tk.W)
        self.pkg_tree.heading("risk", text="Risk Level", anchor=tk.CENTER)
        self.pkg_tree.heading("status", text="Current State", anchor=tk.CENTER)
        self.pkg_tree.heading("category", text="Category", anchor=tk.W)

        self.pkg_tree.column("select", width=40, anchor=tk.CENTER, stretch=False)
        self.pkg_tree.column("name", width=220, anchor=tk.W)
        self.pkg_tree.column("id", width=280, anchor=tk.W)
        self.pkg_tree.column("risk", width=90, anchor=tk.CENTER, stretch=False)
        self.pkg_tree.column("status", width=110, anchor=tk.CENTER, stretch=False)
        self.pkg_tree.column("category", width=180, anchor=tk.W)

        tree_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.pkg_tree.yview)
        self.pkg_tree.configure(yscrollcommand=tree_scroll.set)

        self.pkg_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.pkg_tree.bind("<Button-1>", self._on_tree_click)

        # Bottom Action Bar
        bottom_bar = tk.Frame(self.tab_packages, bg=BG_CARD, highlightbackground=BORDER_COLOR, highlightthickness=1)
        bottom_bar.pack(fill=tk.X, padx=12, pady=(6, 10))

        self.lbl_selected_count = tk.Label(bottom_bar, text="Selected: 0 packages", font=("Segoe UI", 9), fg=TEXT_SECONDARY, bg=BG_CARD)
        self.lbl_selected_count.pack(side=tk.LEFT, padx=12, pady=8)

        # Operation Mode
        self.action_mode_var = tk.StringVar(value="disable")
        m_dis = tk.Radiobutton(bottom_bar, text="Safe Disable", variable=self.action_mode_var, value="disable",
                               font=("Segoe UI", 9), bg=BG_CARD, fg=TEXT_PRIMARY, selectcolor=BG_CARD_LIGHT, activebackground=BG_CARD)
        m_dis.pack(side=tk.LEFT, padx=(16, 8))

        m_uni = tk.Radiobutton(bottom_bar, text="User 0 Uninstall", variable=self.action_mode_var, value="uninstall",
                               font=("Segoe UI", 9), bg=BG_CARD, fg=TEXT_PRIMARY, selectcolor=BG_CARD_LIGHT, activebackground=BG_CARD)
        m_uni.pack(side=tk.LEFT)

        # Big Action Button
        self.btn_execute_debloat = tk.Button(bottom_bar, text="Debloat Selected Packages", font=("Segoe UI", 10, "bold"),
                                             bg=ACCENT_RED, fg="#ffffff", activebackground="#c53030",
                                             activeforeground="#ffffff", relief=tk.FLAT, bd=0, padx=18, pady=6,
                                             command=self._execute_selected_debloat)
        self.btn_execute_debloat.pack(side=tk.RIGHT, padx=12, pady=6)

    def _refresh_package_list_view(self):
        # Initialize selection vars
        for p in database.PACKAGES:
            pkg_id = p["id"]
            if pkg_id not in self.package_vars:
                self.package_vars[pkg_id] = tk.BooleanVar(value=False)
        self._filter_packages()

    def _filter_packages(self):
        search_query = self.search_var.get().strip().lower()
        cat_filter = self.cat_var.get()
        
        # Clear existing rows
        for item in self.pkg_tree.get_children():
            self.pkg_tree.delete(item)

        cat_lookup = {v: k for k, v in database.CATEGORIES.items()}

        selected_count = 0
        for p in database.PACKAGES:
            pkg_id = p["id"]
            name = p["name"]
            cat_key = p["category"]
            cat_display = database.CATEGORIES.get(cat_key, cat_key)
            risk = p["risk"]

            # Category filter
            if cat_filter != "All Categories" and cat_display != cat_filter:
                continue

            # Search filter
            if search_query and search_query not in pkg_id.lower() and search_query not in name.lower():
                continue

            # Status check
            is_installed = pkg_id in self.installed_packages
            status_text = "Installed" if is_installed else "Inactive / Removed"

            is_checked = self.package_vars.get(pkg_id, tk.BooleanVar()).get()
            check_mark = "☑" if is_checked else "☐"
            if is_checked:
                selected_count += 1

            self.pkg_tree.insert("", tk.END, iid=pkg_id, values=(
                check_mark, name, pkg_id, risk.upper(), status_text, cat_display
            ))

        self.lbl_selected_count.configure(text=f"Selected: {selected_count} packages")

    def _on_tree_click(self, event):
        region = self.pkg_tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        column = self.pkg_tree.identify_column(event.x)
        row_id = self.pkg_tree.identify_row(event.y)
        if not row_id:
            return

        # Check if row is critical danger (S Pen / Notes / Keyboard)
        pkg_map = database.get_package_map()
        pkg_info = pkg_map.get(row_id, {})
        if pkg_info.get("risk") == "danger":
            if not messagebox.askyesno("Critical Component Warning", 
                                       f"WARNING: '{pkg_info['name']}' is a critical S Pen / Tablet component!\nRemoving it may cause stylus or system issues.\n\nDo you still want to select it?"):
                return

        # Toggle checkmark
        var = self.package_vars.get(row_id)
        if var:
            var.set(not var.get())
            current_vals = list(self.pkg_tree.item(row_id, "values"))
            current_vals[0] = "☑" if var.get() else "☐"
            self.pkg_tree.item(row_id, values=current_vals)

        # Update count
        count = sum(1 for v in self.package_vars.values() if v.get())
        self.lbl_selected_count.configure(text=f"Selected: {count} packages")

    def _set_selection_all(self, state: bool):
        for p in database.PACKAGES:
            # Don't auto-select danger packages
            if state and p["risk"] == "danger":
                continue
            if p["id"] in self.package_vars:
                self.package_vars[p["id"]].set(state)
        self._filter_packages()

    def _set_selection_by_filter(self, safe_only: bool = True):
        for p in database.PACKAGES:
            if safe_only and p["risk"] != "safe":
                if p["id"] in self.package_vars:
                    self.package_vars[p["id"]].set(False)
            else:
                if p["id"] in self.package_vars:
                    # Only select if currently installed on device
                    if p["id"] in self.installed_packages:
                        self.package_vars[p["id"]].set(True)
                    else:
                        self.package_vars[p["id"]].set(False)
        self._filter_packages()

    def _execute_selected_debloat(self):
        if not self.active_serial:
            messagebox.showwarning("Device Not Connected", "Please connect your Samsung tablet with USB Debugging enabled first.")
            return

        selected_ids = [pid for pid, var in self.package_vars.items() if var.get()]
        if not selected_ids:
            messagebox.showinfo("No Packages Selected", "Please check at least one package from the list to debloat.")
            return

        mode = self.action_mode_var.get()
        action_name = "Disable" if mode == "disable" else "Uninstall (User 0)"
        
        if not messagebox.askyesno("Confirm Debloat", 
                                   f"Are you sure you want to {action_name} {len(selected_ids)} selected packages?\n\nA backup snapshot will be saved to your backups folder."):
            return

        def worker():
            self._perform_debloat_packages(selected_ids, mode)

        threading.Thread(target=worker, daemon=True).start()

    def _perform_debloat_packages(self, package_ids: List[str], mode: str):
        self.log(f"Starting batch debloat of {len(package_ids)} packages (Mode: {mode})...")
        
        # 1. Snapshot backup
        installed_list = self.adb.get_installed_packages(self.active_serial)
        snap = utils.create_backup_snapshot(self.device_info, installed_list)
        self.log(f"Safety snapshot created: {snap.name}")

        pkg_map = database.get_package_map()
        success_count = 0

        for i, pkg in enumerate(package_ids, 1):
            name = pkg_map.get(pkg, {}).get("name", pkg)
            self.log(f"[{i}/{len(package_ids)}] Processing: {name} ({pkg})...")
            
            if mode == "disable":
                success, msg = self.adb.disable_package(pkg, self.active_serial)
            else:
                success, msg = self.adb.uninstall_package(pkg, keep_data=True, serial=self.active_serial)

            if success:
                success_count += 1
                utils.log_debloat_action(pkg, mode, True, note=name)
                self.log(f" -> SUCCESS: {pkg}")
            else:
                utils.log_debloat_action(pkg, mode, False, note=msg)
                self.log(f" -> SKIPPED / FAILED: {pkg} ({msg})", "WARN")

        self.log(f"Batch completed: {success_count}/{len(package_ids)} packages processed successfully.", "SUCCESS")
        
        # Refresh state
        self.installed_packages = set(self.adb.get_installed_packages(self.active_serial))
        self.after(0, self._filter_packages)
        self.after(0, self._refresh_restore_list_view)
        
        messagebox.showinfo("Debloat Complete", 
                            f"Successfully processed {success_count} of {len(package_ids)} packages!\n\nRebooting your tablet is recommended to stop residual background daemons.")

    # ==========================================
    # Tab 3: Restore Center
    # ==========================================
    def _populate_restore_tab(self):
        top_box = tk.Frame(self.tab_restore, bg=BG_CARD, highlightbackground=BORDER_COLOR, highlightthickness=1)
        top_box.pack(fill=tk.X, padx=12, pady=(10, 6))

        r_info = tk.Label(top_box, text="Restore any uninstalled or disabled system packages with 1 click without root or data loss.",
                          font=("Segoe UI", 9), fg=TEXT_SECONDARY, bg=BG_CARD)
        r_info.pack(side=tk.LEFT, padx=12, pady=10)

        btn_refresh_restore = tk.Button(top_box, text="↻ Scan Device", font=("Segoe UI", 8), bg=BG_CARD_LIGHT,
                                        fg=TEXT_PRIMARY, relief=tk.FLAT, bd=0, padx=10, pady=4,
                                        command=self._refresh_restore_list_view)
        btn_refresh_restore.pack(side=tk.RIGHT, padx=12, pady=10)

        # Restore Treeview
        r_table_frame = tk.Frame(self.tab_restore, bg=BG_DARK)
        r_table_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=4)

        columns = ("name", "id", "status")
        self.restore_tree = ttk.Treeview(r_table_frame, columns=columns, show="headings", selectmode="extended")
        self.restore_tree.heading("name", text="Application Name", anchor=tk.W)
        self.restore_tree.heading("id", text="Package ID", anchor=tk.W)
        self.restore_tree.heading("status", text="Restore Status", anchor=tk.CENTER)

        self.restore_tree.column("name", width=300, anchor=tk.W)
        self.restore_tree.column("id", width=380, anchor=tk.W)
        self.restore_tree.column("status", width=180, anchor=tk.CENTER)

        r_scroll = ttk.Scrollbar(r_table_frame, orient="vertical", command=self.restore_tree.yview)
        self.restore_tree.configure(yscrollcommand=r_scroll.set)

        self.restore_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        r_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Restore Action Bar
        r_bottom = tk.Frame(self.tab_restore, bg=BG_CARD, highlightbackground=BORDER_COLOR, highlightthickness=1)
        r_bottom.pack(fill=tk.X, padx=12, pady=(6, 10))

        btn_restore_selected = tk.Button(r_bottom, text="Restore Selected", font=("Segoe UI", 9, "bold"),
                                         bg=ACCENT_GREEN, fg="#ffffff", activebackground="#2f855a",
                                         activeforeground="#ffffff", relief=tk.FLAT, bd=0, padx=16, pady=6,
                                         command=self._restore_selected_packages)
        btn_restore_selected.pack(side=tk.RIGHT, padx=12, pady=6)

        btn_restore_all = tk.Button(r_bottom, text="Restore ALL Listed", font=("Segoe UI", 9),
                                    bg=BG_CARD_LIGHT, fg=TEXT_PRIMARY, relief=tk.FLAT, bd=0, padx=14, pady=6,
                                    command=self._restore_all_packages)
        btn_restore_all.pack(side=tk.RIGHT, padx=6, pady=6)

    def _refresh_restore_list_view(self):
        for item in self.restore_tree.get_children():
            self.restore_tree.delete(item)

        if not self.active_serial:
            return

        candidates = self.adb.get_uninstalled_or_disabled_packages(self.active_serial)
        history = utils.load_debloat_history()
        merged = sorted(list(set(candidates + list(history.keys()))))

        pkg_map = database.get_package_map()

        for p in merged:
            name = pkg_map.get(p, {}).get("name", "System Package")
            status_desc = "Uninstalled / Disabled"
            if p in history:
                status_desc = f"Debloated ({history[p].get('mode', 'removed')})"
            
            self.restore_tree.insert("", tk.END, iid=p, values=(name, p, status_desc))

    def _restore_selected_packages(self):
        selected = self.restore_tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select one or more packages from the list to restore.")
            return

        self._execute_restore(list(selected))

    def _restore_all_packages(self):
        all_items = self.restore_tree.get_children()
        if not all_items:
            messagebox.showinfo("Nothing to Restore", "No uninstalled packages found on the device.")
            return

        if messagebox.askyesno("Confirm Full Restore", f"Restore all {len(all_items)} uninstalled packages back to your tablet?"):
            self._execute_restore(list(all_items))

    def _execute_restore(self, package_ids: List[str]):
        def worker():
            self.log(f"Restoring {len(package_ids)} packages...")
            restored = 0
            pkg_map = database.get_package_map()

            for p in package_ids:
                name = pkg_map.get(p, {}).get("name", p)
                self.log(f"Reinstalling / Enabling: {name} ({p})...")
                success, msg = self.adb.restore_package(p, self.active_serial)
                if success:
                    restored += 1
                    utils.remove_from_debloat_history(p)
                    self.log(f" -> RESTORED: {p}")
                else:
                    self.log(f" -> FAILED: {p} ({msg})", "WARN")

            self.log(f"Restoration complete: {restored}/{len(package_ids)} packages active.")
            self.installed_packages = set(self.adb.get_installed_packages(self.active_serial))
            self.after(0, self._refresh_restore_list_view)
            self.after(0, self._filter_packages)
            messagebox.showinfo("Restore Complete", f"Successfully restored {restored} package(s)!")

        threading.Thread(target=worker, daemon=True).start()

    # ==========================================
    # Tab 4: Performance Tweaks & Hardware
    # ==========================================
    def _populate_tweaks_tab(self):
        t_card1 = tk.Frame(self.tab_tweaks, bg=BG_CARD, highlightbackground=BORDER_COLOR, highlightthickness=1)
        t_card1.pack(fill=tk.X, padx=14, pady=10)

        t1_title = tk.Label(t_card1, text="⚡ Exynos 1380 UI Animation Accelerator", font=("Segoe UI", 11, "bold"), fg=TEXT_PRIMARY, bg=BG_CARD)
        t1_title.pack(anchor="w", padx=14, pady=(12, 4))

        t1_desc = tk.Label(t_card1, text="Samsung's One UI animations can feel slightly heavy on the Exynos 1380 chipset.\nAdjusting the window animation scales to 0.5x makes the tablet feel instantaneous while maintaining smooth 90Hz scrolling.",
                           font=("Segoe UI", 9), fg=TEXT_SECONDARY, bg=BG_CARD, justify=tk.LEFT)
        t1_desc.pack(anchor="w", padx=14, pady=(0, 10))

        btn_row = tk.Frame(t_card1, bg=BG_CARD)
        btn_row.pack(anchor="w", padx=14, pady=(0, 14))

        btn_05 = tk.Button(btn_row, text="Set 0.5x (Recommended)", font=("Segoe UI", 9, "bold"),
                           bg=ACCENT_BLUE, fg="#ffffff", relief=tk.FLAT, bd=0, padx=14, pady=6,
                           command=lambda: self._apply_animation_scale(0.5))
        btn_05.pack(side=tk.LEFT, padx=(0, 10))

        btn_025 = tk.Button(btn_row, text="Set 0.25x (Ultra Fast)", font=("Segoe UI", 9),
                            bg=BG_CARD_LIGHT, fg=TEXT_PRIMARY, relief=tk.FLAT, bd=0, padx=14, pady=6,
                            command=lambda: self._apply_animation_scale(0.25))
        btn_025.pack(side=tk.LEFT, padx=(0, 10))

        btn_reset = tk.Button(btn_row, text="Reset to 1.0x (Default)", font=("Segoe UI", 9),
                              bg=BG_CARD_LIGHT, fg=TEXT_MUTED, relief=tk.FLAT, bd=0, padx=14, pady=6,
                              command=lambda: self._apply_animation_scale(1.0))
        btn_reset.pack(side=tk.LEFT)

        # Device Management Card
        t_card2 = tk.Frame(self.tab_tweaks, bg=BG_CARD, highlightbackground=BORDER_COLOR, highlightthickness=1)
        t_card2.pack(fill=tk.X, padx=14, pady=6)

        t2_title = tk.Label(t_card2, text="🔄 Device Maintenance", font=("Segoe UI", 11, "bold"), fg=TEXT_PRIMARY, bg=BG_CARD)
        t2_title.pack(anchor="w", padx=14, pady=(12, 4))

        t2_desc = tk.Label(t_card2, text="After debloating or restoring packages, a quick reboot ensures all system caches and services are clean.",
                           font=("Segoe UI", 9), fg=TEXT_SECONDARY, bg=BG_CARD)
        t2_desc.pack(anchor="w", padx=14, pady=(0, 10))

        btn_reboot = tk.Button(t_card2, text="Reboot Tablet via ADB", font=("Segoe UI", 9, "bold"),
                               bg=ACCENT_YELLOW, fg="#000000", relief=tk.FLAT, bd=0, padx=14, pady=6,
                               command=self._reboot_tablet)
        btn_reboot.pack(anchor="w", padx=14, pady=(0, 14))

    def _apply_animation_scale(self, scale: float):
        if not self.active_serial:
            messagebox.showwarning("Device Not Connected", "Please connect your tablet first.")
            return

        success = self.adb.set_animation_scale(scale, self.active_serial)
        if success:
            self.log(f"Window animation scale set to {scale}x successfully.")
            messagebox.showinfo("Tweak Applied", f"Animation scale successfully set to {scale}x!")
        else:
            self.log("Failed to set animation scale.", "ERROR")
            messagebox.showerror("Error", "Could not set animation scale.")

    def _reboot_tablet(self):
        if not self.active_serial:
            messagebox.showwarning("Device Not Connected", "Please connect your tablet first.")
            return

        if messagebox.askyesno("Confirm Reboot", "Do you want to reboot your tablet now?"):
            self.adb.reboot_device(self.active_serial)
            self.log("Reboot command sent to tablet.")
            self._update_device_ui_disconnected()

def main():
    app = DebloaterGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
