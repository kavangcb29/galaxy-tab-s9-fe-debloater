"""
Samsung Galaxy Tab S9 FE Debloater Toolkit - Modern GUI
High-quality, dark-themed native desktop interface inspired by modern design systems.
Includes High-DPI support, sidebar navigation, visual risk badges, and non-blocking threading.
"""

import os
import sys
import threading
import time
import webbrowser
from pathlib import Path

# Enable High-DPI awareness on Windows for razor-sharp typography
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import tkinter as tk
from tkinter import ttk, messagebox

from adb_manager import ADBManager
import database
import utils

# =========================================================================
# Premium Dark Theme Palette (Linear / One UI Dark Inspired)
# =========================================================================
COLOR_BG_ROOT       = "#0b0d13"   # Deep Obsidian
COLOR_SIDEBAR       = "#11141d"   # Sidebar Surface
COLOR_SIDEBAR_HOVER = "#181d2a"   # Sidebar Item Hover
COLOR_SIDEBAR_ACTIVE= "#1e2435"   # Sidebar Item Active
COLOR_CARD          = "#151822"   # Card Surface
COLOR_CARD_BORDER   = "#222736"   # Subtle Card Border
COLOR_CARD_HOVER    = "#1a1f2c"   # Card Hover State
COLOR_CARD_LIGHT    = "#1c2130"   # Secondary Card / Input Background

COLOR_TEXT_PRIMARY   = "#f8fafc"   # High-contrast White
COLOR_TEXT_SECONDARY = "#94a3b8"   # Slate Gray
COLOR_TEXT_MUTED     = "#64748b"   # Muted Meta Text

COLOR_ACCENT_BLUE    = "#3b82f6"   # Electric Blue
COLOR_ACCENT_BLUE_H  = "#2563eb"   # Electric Blue Hover
COLOR_ACCENT_PURPLE  = "#8b5cf6"   # Accent Purple
COLOR_ACCENT_EMERALD = "#10b981"   # Safe Green
COLOR_ACCENT_AMBER   = "#f59e0b"   # Caution Amber
COLOR_ACCENT_ROSE    = "#ef4444"   # Danger Rose / Red

FONT_FAMILY = "Segoe UI"


class ModernButton(tk.Label):
    """A sleek, custom-styled button with smooth hover feedback and hand cursor."""
    def __init__(self, parent, text, command=None, bg=COLOR_ACCENT_BLUE, fg="#ffffff",
                 hover_bg=COLOR_ACCENT_BLUE_H, font=(FONT_FAMILY, 9, "bold"), padx=14, pady=7,
                 bd_color=None, **kwargs):
        super().__init__(parent, text=text, font=font, bg=bg, fg=fg, cursor="hand2",
                         padx=padx, pady=pady, **kwargs)
        self.command = command
        self.default_bg = bg
        self.hover_bg = hover_bg
        self.is_disabled = False

        if bd_color:
            self.configure(highlightbackground=bd_color, highlightthickness=1)

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _on_enter(self, e):
        if not self.is_disabled:
            self.configure(bg=self.hover_bg)

    def _on_leave(self, e):
        if not self.is_disabled:
            self.configure(bg=self.default_bg)

    def _on_click(self, e):
        if not self.is_disabled and self.command:
            self.command()

    def set_disabled(self, disabled: bool):
        self.is_disabled = disabled
        if disabled:
            self.configure(bg="#202430", fg=COLOR_TEXT_MUTED, cursor="arrow")
        else:
            self.configure(bg=self.default_bg, fg="#ffffff", cursor="hand2")


class DebloaterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Samsung Galaxy Tab S9 FE Toolkit")
        self.geometry("1100x740")
        self.minsize(980, 620)
        self.configure(bg=COLOR_BG_ROOT)

        self.adb = ADBManager()
        self.device_info = {}
        self.active_serial = None
        self.installed_packages = set()

        # Selection state
        self.package_vars = {}
        self.current_page = "presets"
        self.log_drawer_visible = False

        # Setup modern ttk styles
        self._setup_ttk_styles()

        # Build Main Layout (Sidebar + Content Container + Bottom Activity Bar)
        self._build_layout()

        # Start device connection scan in background
        self.after(200, self.async_refresh_device)

    def _setup_ttk_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Treeview styling for Package Manager
        style.configure("Custom.Treeview",
                        background=COLOR_CARD,
                        foreground=COLOR_TEXT_PRIMARY,
                        fieldbackground=COLOR_CARD,
                        rowheight=32,
                        font=(FONT_FAMILY, 9),
                        borderwidth=0)
        style.configure("Custom.Treeview.Heading",
                        background=COLOR_CARD_LIGHT,
                        foreground=COLOR_TEXT_SECONDARY,
                        font=(FONT_FAMILY, 9, "bold"),
                        padding=[10, 8],
                        borderwidth=0)
        style.map("Custom.Treeview",
                  background=[("selected", "#222a3d")],
                  foreground=[("selected", "#ffffff")])

        # Scrollbar styling
        style.configure("Vertical.TScrollbar",
                        background=COLOR_SIDEBAR,
                        troughcolor=COLOR_BG_ROOT,
                        borderwidth=0,
                        arrowsize=11)
        style.map("Vertical.TScrollbar",
                  background=[("active", COLOR_CARD_LIGHT)])

    def _build_layout(self):
        # 1. Left Sidebar
        self.sidebar_frame = tk.Frame(self, bg=COLOR_SIDEBAR, width=220, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)

        self._build_sidebar()

        # 2. Main Work Area (Right Side)
        self.main_container = tk.Frame(self, bg=COLOR_BG_ROOT)
        self.main_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Top Header Bar (Device Status + Refresh + Sponsor)
        self._build_top_header()

        # Dynamic Content View Area
        self.content_frame = tk.Frame(self.main_container, bg=COLOR_BG_ROOT)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=22, pady=(10, 8))

        # Bottom Activity & Status Bar (with collapsible Log Drawer)
        self._build_bottom_bar()

        # Initialize and show default page
        self.switch_page("presets")

    # =========================================================================
    # Sidebar
    # =========================================================================
    def _build_sidebar(self):
        # App Branding Header
        brand_box = tk.Frame(self.sidebar_frame, bg=COLOR_SIDEBAR)
        brand_box.pack(fill=tk.X, padx=16, pady=(18, 20))

        logo_row = tk.Frame(brand_box, bg=COLOR_SIDEBAR)
        logo_row.pack(fill=tk.X)

        icon_badge = tk.Label(logo_row, text="⚡", font=(FONT_FAMILY, 14), fg=COLOR_ACCENT_BLUE, bg=COLOR_SIDEBAR)
        icon_badge.pack(side=tk.LEFT, padx=(0, 8))

        app_title = tk.Label(logo_row, text="TAB S9 FE", font=(FONT_FAMILY, 12, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_SIDEBAR)
        app_title.pack(side=tk.LEFT)

        app_subtitle = tk.Label(brand_box, text="Optimizer & Debloater", font=(FONT_FAMILY, 8), fg=COLOR_TEXT_MUTED, bg=COLOR_SIDEBAR)
        app_subtitle.pack(anchor="w", padx=(28, 0))

        # Divider
        div = tk.Frame(self.sidebar_frame, bg=COLOR_CARD_BORDER, height=1)
        div.pack(fill=tk.X, padx=14, pady=(0, 14))

        # Navigation Menu Items
        self.nav_buttons = {}
        nav_items = [
            ("presets", "⚡  1-Click Presets"),
            ("packages", "📦  Package Manager"),
            ("restore", "🔄  Restore Center"),
            ("tweaks", "🚀  Hardware Tweaks"),
            ("logs", "📄  Activity & Logs")
        ]

        for page_id, label in nav_items:
            btn = tk.Label(self.sidebar_frame, text=label, font=(FONT_FAMILY, 9, "bold"),
                           fg=COLOR_TEXT_SECONDARY, bg=COLOR_SIDEBAR, anchor="w",
                           padx=16, pady=10, cursor="hand2")
            btn.pack(fill=tk.X, padx=10, pady=2)
            btn.bind("<Button-1>", lambda e, pid=page_id: self.switch_page(pid))
            self.nav_buttons[page_id] = btn

        # Sidebar Spacer
        tk.Frame(self.sidebar_frame, bg=COLOR_SIDEBAR).pack(fill=tk.BOTH, expand=True)

        # Bottom Sidebar: Support / Sponsor Banner
        sponsor_box = tk.Frame(self.sidebar_frame, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        sponsor_box.pack(fill=tk.X, padx=12, pady=14)

        s_title = tk.Label(sponsor_box, text="Enjoying the speed?", font=(FONT_FAMILY, 8, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD)
        s_title.pack(anchor="w", padx=10, pady=(10, 2))

        s_sub = tk.Label(sponsor_box, text="Support future One UI updates", font=(FONT_FAMILY, 7), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD)
        s_sub.pack(anchor="w", padx=10, pady=(0, 8))

        btn_coffee = ModernButton(sponsor_box, text="☕ Support Developer", font=(FONT_FAMILY, 8, "bold"),
                                  bg="#d97706", hover_bg="#b45309", padx=8, pady=5,
                                  command=self._show_support_modal)
        btn_coffee.pack(fill=tk.X, padx=10, pady=(0, 10))

    def switch_page(self, page_id: str):
        self.current_page = page_id

        # Update sidebar visual selection
        for pid, btn in self.nav_buttons.items():
            if pid == page_id:
                btn.configure(bg=COLOR_SIDEBAR_ACTIVE, fg=COLOR_TEXT_PRIMARY)
            else:
                btn.configure(bg=COLOR_SIDEBAR, fg=COLOR_TEXT_SECONDARY)

        # Clear Content View
        for child in self.content_frame.winfo_children():
            child.destroy()

        # Render selected page
        if page_id == "presets":
            self._render_presets_page()
        elif page_id == "packages":
            self._render_packages_page()
        elif page_id == "restore":
            self._render_restore_page()
        elif page_id == "tweaks":
            self._render_tweaks_page()
        elif page_id == "logs":
            self._render_logs_page()

    # =========================================================================
    # Top Header Bar
    # =========================================================================
    def _build_top_header(self):
        header_bar = tk.Frame(self.main_container, bg=COLOR_BG_ROOT, height=60)
        header_bar.pack(fill=tk.X, padx=22, pady=(16, 4))
        header_bar.pack_propagate(False)

        # Left Page Title & Breadcrumb
        self.page_title_lbl = tk.Label(header_bar, text="Optimization Presets", font=(FONT_FAMILY, 15, "bold"),
                                       fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG_ROOT)
        self.page_title_lbl.pack(side=tk.LEFT)

        # Right Action & Status Container
        right_box = tk.Frame(header_bar, bg=COLOR_BG_ROOT)
        right_box.pack(side=tk.RIGHT)

        # Refresh Button
        btn_refresh = ModernButton(right_box, text="↻ Refresh Device", font=(FONT_FAMILY, 8, "bold"),
                                   bg=COLOR_CARD, hover_bg=COLOR_CARD_HOVER, bd_color=COLOR_CARD_BORDER,
                                   fg=COLOR_TEXT_SECONDARY, padx=12, pady=6,
                                   command=self.async_refresh_device)
        btn_refresh.pack(side=tk.RIGHT, padx=(10, 0))

        # Device Chip Badge
        self.device_chip = tk.Frame(right_box, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        self.device_chip.pack(side=tk.RIGHT)

        self.device_chip_dot = tk.Label(self.device_chip, text="●", font=(FONT_FAMILY, 10), fg=COLOR_ACCENT_AMBER, bg=COLOR_CARD)
        self.device_chip_dot.pack(side=tk.LEFT, padx=(10, 6), pady=6)

        self.device_chip_text = tk.Label(self.device_chip, text="Scanning for device...", font=(FONT_FAMILY, 8, "bold"),
                                         fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD)
        self.device_chip_text.pack(side=tk.LEFT, padx=(0, 12), pady=6)

    # =========================================================================
    # Page 1: Presets
    # =========================================================================
    def _render_presets_page(self):
        self.page_title_lbl.configure(text="Optimization Presets")

        presets = utils.load_presets()

        # Canvas container for smooth scrolling
        canvas = tk.Canvas(self.content_frame, bg=COLOR_BG_ROOT, bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scroll_content = tk.Frame(canvas, bg=COLOR_BG_ROOT)

        scroll_content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_content, anchor="nw", width=820)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Featured Preset Card (Safe & Clean + De-Bixby + Exynos Performance Turbo)
        if presets:
            featured = presets[0]
            self._render_featured_preset_card(scroll_content, featured)

        # Other Presets in a clean list
        section_lbl = tk.Label(scroll_content, text="ADDITIONAL PRESET PROFILES", font=(FONT_FAMILY, 9, "bold"),
                               fg=COLOR_TEXT_MUTED, bg=COLOR_BG_ROOT)
        section_lbl.pack(anchor="w", pady=(18, 8), padx=2)

        for preset in presets[1:]:
            self._render_standard_preset_card(scroll_content, preset)

    def _render_featured_preset_card(self, parent, preset):
        card = tk.Frame(parent, bg=COLOR_CARD, highlightbackground="#3b82f6", highlightthickness=1.5)
        card.pack(fill=tk.X, pady=(4, 12), padx=2)

        # Top Badge Bar
        top_row = tk.Frame(card, bg=COLOR_CARD)
        top_row.pack(fill=tk.X, padx=16, pady=(14, 6))

        badge = tk.Label(top_row, text="★  RECOMMENDED FOR TAB S9 FE", font=(FONT_FAMILY, 8, "bold"),
                         fg="#60a5fa", bg="#1e293b", padx=8, pady=3)
        badge.pack(side=tk.LEFT)

        pkg_pill = tk.Label(top_row, text=f"{len(preset['packages'])} packages targeted", font=(FONT_FAMILY, 8),
                            fg=COLOR_TEXT_MUTED, bg=COLOR_CARD)
        pkg_pill.pack(side=tk.RIGHT)

        # Title & Subtitle
        title = tk.Label(card, text=preset["name"], font=(FONT_FAMILY, 13, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD)
        title.pack(anchor="w", padx=16, pady=(2, 4))

        desc = tk.Label(card, text=preset["description"], font=(FONT_FAMILY, 9), fg=COLOR_TEXT_SECONDARY,
                        bg=COLOR_CARD, wraplength=760, justify=tk.LEFT)
        desc.pack(anchor="w", padx=16, pady=(0, 12))

        # Highlights Row
        pill_row = tk.Frame(card, bg=COLOR_CARD)
        pill_row.pack(fill=tk.X, padx=16, pady=(0, 14))

        pills = [
            ("⚡ Exynos 1380 GOS Unthrottled", COLOR_ACCENT_EMERALD),
            ("🔇 De-Bixby Standby Battery Saver", COLOR_ACCENT_BLUE),
            ("🔒 S Pen, Notes & DeX 100% Protected", "#a855f7"),
            ("📧 Microsoft Outlook Preserved", COLOR_TEXT_MUTED)
        ]
        for p_text, p_color in pills:
            p_lbl = tk.Label(pill_row, text=p_text, font=(FONT_FAMILY, 8, "bold"),
                             fg=p_color, bg=COLOR_CARD_LIGHT, padx=8, pady=3)
            p_lbl.pack(side=tk.LEFT, padx=(0, 8))

        # Bottom Action Divider
        tk.Frame(card, bg=COLOR_CARD_BORDER, height=1).pack(fill=tk.X)

        action_box = tk.Frame(card, bg=COLOR_CARD_LIGHT)
        action_box.pack(fill=tk.X, padx=16, pady=10)

        # Mode Radio
        mode_var = tk.StringVar(value="disable")
        rb1 = tk.Radiobutton(action_box, text="Safe Disable (Recommended)", variable=mode_var, value="disable",
                             font=(FONT_FAMILY, 8), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD_LIGHT,
                             selectcolor=COLOR_CARD, activebackground=COLOR_CARD_LIGHT)
        rb1.pack(side=tk.LEFT, padx=(0, 10))

        rb2 = tk.Radiobutton(action_box, text="Full User Uninstall", variable=mode_var, value="uninstall",
                             font=(FONT_FAMILY, 8), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD_LIGHT,
                             selectcolor=COLOR_CARD, activebackground=COLOR_CARD_LIGHT)
        rb2.pack(side=tk.LEFT, padx=(0, 14))

        # 0.5x speed checkbox
        tweak_var = tk.BooleanVar(value=True)
        cb_tweak = tk.Checkbutton(action_box, text="⚡ Apply 0.5x UI Speed Tweak", variable=tweak_var,
                                  font=(FONT_FAMILY, 8, "bold"), fg=COLOR_ACCENT_AMBER, bg=COLOR_CARD_LIGHT,
                                  selectcolor=COLOR_CARD, activebackground=COLOR_CARD_LIGHT)
        cb_tweak.pack(side=tk.LEFT)

        # Big Action Button
        btn_run = ModernButton(action_box, text="Apply Turbo Preset ➔", font=(FONT_FAMILY, 9, "bold"),
                               bg=COLOR_ACCENT_BLUE, hover_bg=COLOR_ACCENT_BLUE_H, padx=16, pady=6,
                               command=lambda: self._execute_preset(preset, mode_var.get(), tweak_var.get()))
        btn_run.pack(side=tk.RIGHT)

    def _render_standard_preset_card(self, parent, preset):
        card = tk.Frame(parent, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        card.pack(fill=tk.X, pady=5, padx=2)

        header = tk.Frame(card, bg=COLOR_CARD)
        header.pack(fill=tk.X, padx=14, pady=(10, 4))

        t_lbl = tk.Label(header, text=preset["name"], font=(FONT_FAMILY, 10, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD)
        t_lbl.pack(side=tk.LEFT)

        cnt_lbl = tk.Label(header, text=f"{len(preset['packages'])} packages", font=(FONT_FAMILY, 8),
                           fg=COLOR_TEXT_MUTED, bg=COLOR_CARD_LIGHT, padx=6, pady=2)
        cnt_lbl.pack(side=tk.RIGHT)

        desc = tk.Label(card, text=preset["description"], font=(FONT_FAMILY, 8), fg=COLOR_TEXT_SECONDARY,
                        bg=COLOR_CARD, wraplength=720, justify=tk.LEFT)
        desc.pack(anchor="w", padx=14, pady=(0, 10))

        bottom_row = tk.Frame(card, bg=COLOR_CARD)
        bottom_row.pack(fill=tk.X, padx=14, pady=(0, 10))

        mode_var = tk.StringVar(value="disable")
        rb = tk.Radiobutton(bottom_row, text="Safe Disable", variable=mode_var, value="disable",
                            font=(FONT_FAMILY, 8), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD,
                            selectcolor=COLOR_CARD_LIGHT, activebackground=COLOR_CARD)
        rb.pack(side=tk.LEFT, padx=(0, 8))

        btn = ModernButton(bottom_row, text="Apply Preset ➔", font=(FONT_FAMILY, 8, "bold"),
                           bg=COLOR_CARD_LIGHT, hover_bg=COLOR_CARD_HOVER, bd_color=COLOR_CARD_BORDER,
                           fg=COLOR_TEXT_PRIMARY, padx=12, pady=4,
                           command=lambda p=preset, m=mode_var: self._execute_preset(p, m.get(), False))
        btn.pack(side=tk.RIGHT)

    # =========================================================================
    # Page 2: Package Manager
    # =========================================================================
    def _render_packages_page(self):
        self.page_title_lbl.configure(text="Custom Package Manager")

        # Top Filter & Search Bar
        top_filter_box = tk.Frame(self.content_frame, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        top_filter_box.pack(fill=tk.X, pady=(0, 8))

        # Category Dropdown
        cat_lbl = tk.Label(top_filter_box, text="Category:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD)
        cat_lbl.pack(side=tk.LEFT, padx=(12, 6), pady=10)

        self.cat_var = tk.StringVar(value="All Categories")
        cat_options = ["All Categories"] + list(database.CATEGORIES.values())
        self.cat_combo = ttk.Combobox(top_filter_box, textvariable=self.cat_var, values=cat_options, state="readonly", width=28)
        self.cat_combo.pack(side=tk.LEFT, padx=(0, 14), pady=10)
        self.cat_combo.bind("<<ComboboxSelected>>", lambda e: self._filter_packages())

        # Search Box
        search_lbl = tk.Label(top_filter_box, text="Search:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD)
        search_lbl.pack(side=tk.LEFT, padx=(0, 6), pady=10)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self._filter_packages())
        search_entry = tk.Entry(top_filter_box, textvariable=self.search_var, bg=COLOR_CARD_LIGHT, fg=COLOR_TEXT_PRIMARY,
                                insertbackground=COLOR_TEXT_PRIMARY, bd=0, relief=tk.FLAT, font=(FONT_FAMILY, 9), width=20)
        search_entry.pack(side=tk.LEFT, padx=(0, 14), pady=10, ipady=4)

        # Quick Select Action Buttons
        btn_sel_safe = ModernButton(top_filter_box, text="Select Safe", font=(FONT_FAMILY, 8, "bold"),
                                    bg=COLOR_CARD_LIGHT, hover_bg=COLOR_CARD_HOVER, fg=COLOR_ACCENT_EMERALD,
                                    padx=10, pady=4, command=self._select_safe_packages)
        btn_sel_safe.pack(side=tk.RIGHT, padx=8)

        btn_clear = ModernButton(top_filter_box, text="Deselect All", font=(FONT_FAMILY, 8),
                                 bg=COLOR_CARD_LIGHT, hover_bg=COLOR_CARD_HOVER, fg=COLOR_TEXT_MUTED,
                                 padx=10, pady=4, command=self._clear_all_selection)
        btn_clear.pack(side=tk.RIGHT, padx=4)

        # Treeview Table
        table_container = tk.Frame(self.content_frame, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        table_container.pack(fill=tk.BOTH, expand=True)

        columns = ("select", "name", "id", "risk", "status")
        self.pkg_tree = ttk.Treeview(table_container, columns=columns, show="headings",
                                     selectmode="extended", style="Custom.Treeview")

        self.pkg_tree.heading("select", text="✓", anchor=tk.CENTER)
        self.pkg_tree.heading("name", text="Application Name", anchor=tk.W)
        self.pkg_tree.heading("id", text="Package ID", anchor=tk.W)
        self.pkg_tree.heading("risk", text="Risk Rating", anchor=tk.CENTER)
        self.pkg_tree.heading("status", text="Device State", anchor=tk.CENTER)

        self.pkg_tree.column("select", width=42, anchor=tk.CENTER, stretch=False)
        self.pkg_tree.column("name", width=240, anchor=tk.W)
        self.pkg_tree.column("id", width=330, anchor=tk.W)
        self.pkg_tree.column("risk", width=110, anchor=tk.CENTER, stretch=False)
        self.pkg_tree.column("status", width=120, anchor=tk.CENTER, stretch=False)

        tree_scroll = ttk.Scrollbar(table_container, orient="vertical", command=self.pkg_tree.yview, style="Vertical.TScrollbar")
        self.pkg_tree.configure(yscrollcommand=tree_scroll.set)

        self.pkg_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.pkg_tree.bind("<Button-1>", self._on_tree_click)

        # Bottom Action Dock
        dock = tk.Frame(self.content_frame, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        dock.pack(fill=tk.X, pady=(8, 0))

        self.lbl_selected_stats = tk.Label(dock, text="Selected: 0 packages", font=(FONT_FAMILY, 9, "bold"),
                                           fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD)
        self.lbl_selected_stats.pack(side=tk.LEFT, padx=14, pady=10)

        # Mode Selection
        self.custom_mode_var = tk.StringVar(value="disable")
        m1 = tk.Radiobutton(dock, text="Safe Disable", variable=self.custom_mode_var, value="disable",
                            font=(FONT_FAMILY, 8), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD,
                            selectcolor=COLOR_CARD_LIGHT, activebackground=COLOR_CARD)
        m1.pack(side=tk.LEFT, padx=(16, 8))

        m2 = tk.Radiobutton(dock, text="User 0 Uninstall", variable=self.custom_mode_var, value="uninstall",
                            font=(FONT_FAMILY, 8), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD,
                            selectcolor=COLOR_CARD_LIGHT, activebackground=COLOR_CARD)
        m2.pack(side=tk.LEFT)

        btn_execute = ModernButton(dock, text="Debloat Selected Packages ➔", font=(FONT_FAMILY, 9, "bold"),
                                   bg=COLOR_ACCENT_ROSE, hover_bg="#dc2626", padx=16, pady=6,
                                   command=self._execute_custom_debloat)
        btn_execute.pack(side=tk.RIGHT, padx=12, pady=6)

        # Refresh table rows
        self._filter_packages()

    def _filter_packages(self):
        if not hasattr(self, "pkg_tree") or not self.pkg_tree.winfo_exists():
            return

        cat_filter = self.cat_var.get()
        search_term = self.search_var.get().strip().lower()

        for item in self.pkg_tree.get_children():
            self.pkg_tree.delete(item)

        sel_count = 0
        for p in database.PACKAGES:
            pid = p["id"]
            name = p["name"]
            cat_display = database.CATEGORIES.get(p["category"], p["category"])
            risk = p["risk"].upper()

            if cat_filter != "All Categories" and cat_display != cat_filter:
                continue

            if search_term and search_term not in pid.lower() and search_term not in name.lower():
                continue

            is_checked = self.package_vars.get(pid, tk.BooleanVar()).get()
            mark = "☑" if is_checked else "☐"
            if is_checked:
                sel_count += 1

            status = "Installed" if pid in self.installed_packages else "Inactive"
            self.pkg_tree.insert("", tk.END, iid=pid, values=(mark, name, pid, risk, status))

        if hasattr(self, "lbl_selected_stats"):
            self.lbl_selected_stats.configure(text=f"Selected: {sel_count} packages")

    def _on_tree_click(self, event):
        region = self.pkg_tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        row_id = self.pkg_tree.identify_row(event.y)
        if not row_id:
            return

        pkg_map = database.get_package_map()
        p_info = pkg_map.get(row_id, {})
        if p_info.get("risk") == "danger":
            if not messagebox.askyesno("Critical Stylus Component Warning",
                                       f"WARNING: '{p_info['name']}' is vital for S Pen or Samsung DeX functionality.\n\nAre you sure you want to select this?"):
                return

        var = self.package_vars.setdefault(row_id, tk.BooleanVar(value=False))
        var.set(not var.get())

        vals = list(self.pkg_tree.item(row_id, "values"))
        vals[0] = "☑" if var.get() else "☐"
        self.pkg_tree.item(row_id, values=vals)

        sel_count = sum(1 for v in self.package_vars.values() if v.get())
        self.lbl_selected_stats.configure(text=f"Selected: {sel_count} packages")

    def _select_safe_packages(self):
        for p in database.PACKAGES:
            pid = p["id"]
            var = self.package_vars.setdefault(pid, tk.BooleanVar())
            if p["risk"] == "safe" and pid in self.installed_packages:
                var.set(True)
            else:
                var.set(False)
        self._filter_packages()

    def _clear_all_selection(self):
        for var in self.package_vars.values():
            var.set(False)
        self._filter_packages()

    # =========================================================================
    # Page 3: Restore Center
    # =========================================================================
    def _render_restore_page(self):
        self.page_title_lbl.configure(text="Restore Center")

        info_box = tk.Frame(self.content_frame, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        info_box.pack(fill=tk.X, pady=(0, 8))

        i_title = tk.Label(info_box, text="Zero Data Loss • Instant Reversibility", font=(FONT_FAMILY, 10, "bold"),
                           fg=COLOR_ACCENT_EMERALD, bg=COLOR_CARD)
        i_title.pack(anchor="w", padx=14, pady=(10, 2))

        i_sub = tk.Label(info_box, text="All debloated packages remain stored on your system partition. You can re-enable or reinstall any package with 1 click.",
                         font=(FONT_FAMILY, 8), fg=COLOR_TEXT_SECONDARY, bg=COLOR_CARD)
        i_sub.pack(anchor="w", padx=14, pady=(0, 10))

        # Restore Table
        t_container = tk.Frame(self.content_frame, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        t_container.pack(fill=tk.BOTH, expand=True)

        columns = ("name", "id", "state")
        self.restore_tree = ttk.Treeview(t_container, columns=columns, show="headings",
                                         selectmode="extended", style="Custom.Treeview")

        self.restore_tree.heading("name", text="Application Name", anchor=tk.W)
        self.restore_tree.heading("id", text="Package ID", anchor=tk.W)
        self.restore_tree.heading("state", text="Restore Status", anchor=tk.CENTER)

        self.restore_tree.column("name", width=280, anchor=tk.W)
        self.restore_tree.column("id", width=360, anchor=tk.W)
        self.restore_tree.column("state", width=140, anchor=tk.CENTER)

        r_scroll = ttk.Scrollbar(t_container, orient="vertical", command=self.restore_tree.yview, style="Vertical.TScrollbar")
        self.restore_tree.configure(yscrollcommand=r_scroll.set)

        self.restore_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        r_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Restore Dock
        dock = tk.Frame(self.content_frame, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        dock.pack(fill=tk.X, pady=(8, 0))

        btn_res_all = ModernButton(dock, text="Restore ALL Listed Packages", font=(FONT_FAMILY, 9, "bold"),
                                   bg=COLOR_CARD_LIGHT, hover_bg=COLOR_CARD_HOVER, bd_color=COLOR_CARD_BORDER,
                                   fg=COLOR_TEXT_PRIMARY, padx=16, pady=6, command=self._restore_all_action)
        btn_res_all.pack(side=tk.LEFT, padx=12, pady=6)

        btn_res_sel = ModernButton(dock, text="Restore Selected ➔", font=(FONT_FAMILY, 9, "bold"),
                                   bg=COLOR_ACCENT_EMERALD, hover_bg="#059669", padx=16, pady=6,
                                   command=self._restore_selected_action)
        btn_res_sel.pack(side=tk.RIGHT, padx=12, pady=6)

        self._refresh_restore_table()

    def _refresh_restore_table(self):
        if not hasattr(self, "restore_tree") or not self.restore_tree.winfo_exists():
            return
        for item in self.restore_tree.get_children():
            self.restore_tree.delete(item)

        if not self.active_serial:
            return

        candidates = self.adb.get_uninstalled_or_disabled_packages(self.active_serial)
        history = utils.load_debloat_history()
        merged = sorted(list(set(candidates + list(history.keys()))))
        pkg_map = database.get_package_map()

        for pid in merged:
            name = pkg_map.get(pid, {}).get("name", "System Service")
            state = "Disabled / Uninstalled"
            if pid in history:
                state = f"Debloated ({history[pid].get('mode', 'user 0')})"
            self.restore_tree.insert("", tk.END, iid=pid, values=(name, pid, state))

    # =========================================================================
    # Page 4: Hardware Tweaks
    # =========================================================================
    def _render_tweaks_page(self):
        self.page_title_lbl.configure(text="Hardware & One UI Tweaks")

        # Tweak Card 1: Exynos 1380 Animation Speed
        c1 = tk.Frame(self.content_frame, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        c1.pack(fill=tk.X, pady=(0, 10))

        t1 = tk.Label(c1, text="⚡ Exynos 1380 Animation Speed Accelerator", font=(FONT_FAMILY, 11, "bold"),
                      fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD)
        t1.pack(anchor="w", padx=16, pady=(12, 4))

        d1 = tk.Label(c1, text="One UI app launch animations are rendered at 1.0x by default. On the Exynos 1380 processor, this often feels sluggish.\nSetting animation scales to 0.5x makes the tablet feel instantaneous while maintaining smooth 90Hz scrolling.",
                      font=(FONT_FAMILY, 8), fg=COLOR_TEXT_SECONDARY, bg=COLOR_CARD, justify=tk.LEFT)
        d1.pack(anchor="w", padx=16, pady=(0, 12))

        b_row = tk.Frame(c1, bg=COLOR_CARD)
        b_row.pack(anchor="w", padx=16, pady=(0, 14))

        b1 = ModernButton(b_row, text="⚡ Set 0.5x Speed (Recommended)", font=(FONT_FAMILY, 8, "bold"),
                          bg=COLOR_ACCENT_BLUE, hover_bg=COLOR_ACCENT_BLUE_H, padx=14, pady=5,
                          command=lambda: self._set_speed_scale(0.5))
        b1.pack(side=tk.LEFT, padx=(0, 10))

        b2 = ModernButton(b_row, text="Set 0.25x (Ultra Fast)", font=(FONT_FAMILY, 8),
                          bg=COLOR_CARD_LIGHT, hover_bg=COLOR_CARD_HOVER, fg=COLOR_TEXT_PRIMARY, padx=14, pady=5,
                          command=lambda: self._set_speed_scale(0.25))
        b2.pack(side=tk.LEFT, padx=(0, 10))

        b3 = ModernButton(b_row, text="Reset to 1.0x Default", font=(FONT_FAMILY, 8),
                          bg=COLOR_CARD_LIGHT, hover_bg=COLOR_CARD_HOVER, fg=COLOR_TEXT_MUTED, padx=14, pady=5,
                          command=lambda: self._set_speed_scale(1.0))
        b3.pack(side=tk.LEFT)

        # Tweak Card 2: Device Maintenance
        c2 = tk.Frame(self.content_frame, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        c2.pack(fill=tk.X, pady=6)

        t2 = tk.Label(c2, text="🔄 Device Maintenance & Clean Reboot", font=(FONT_FAMILY, 11, "bold"),
                      fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD)
        t2.pack(anchor="w", padx=16, pady=(12, 4))

        d2 = tk.Label(c2, text="After debloating or restoring packages, a quick reboot ensures all background memory caches are freed and residual daemons are stopped.",
                      font=(FONT_FAMILY, 8), fg=COLOR_TEXT_SECONDARY, bg=COLOR_CARD)
        d2.pack(anchor="w", padx=16, pady=(0, 12))

        b_reboot = ModernButton(c2, text="Reboot Tablet via ADB", font=(FONT_FAMILY, 8, "bold"),
                                bg=COLOR_CARD_LIGHT, hover_bg=COLOR_CARD_HOVER, bd_color=COLOR_CARD_BORDER,
                                fg=COLOR_ACCENT_AMBER, padx=14, pady=5, command=self._reboot_action)
        b_reboot.pack(anchor="w", padx=16, pady=(0, 14))

    # =========================================================================
    # Page 5: Activity & Logs
    # =========================================================================
    def _render_logs_page(self):
        self.page_title_lbl.configure(text="Execution Console & Logs")

        log_box = tk.Frame(self.content_frame, bg=COLOR_CARD, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        log_box.pack(fill=tk.BOTH, expand=True)

        tool_bar = tk.Frame(log_box, bg=COLOR_CARD_LIGHT)
        tool_bar.pack(fill=tk.X, padx=12, pady=6)

        lbl = tk.Label(tool_bar, text="REAL-TIME ADB LOGS", font=(FONT_FAMILY, 8, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD_LIGHT)
        lbl.pack(side=tk.LEFT)

        btn_clr = ModernButton(tool_bar, text="Clear Console", font=(FONT_FAMILY, 8),
                               bg=COLOR_CARD, hover_bg=COLOR_CARD_HOVER, fg=COLOR_TEXT_MUTED, padx=8, pady=3,
                               command=self.clear_log)
        btn_clr.pack(side=tk.RIGHT)

        self.full_log_text = tk.Text(log_box, bg="#0d0f14", fg="#34d399", font=("Consolas", 9),
                                     bd=0, padx=12, pady=8, state=tk.NORMAL)
        self.full_log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.full_log_text.insert(tk.END, self.log_buffer)
        self.full_log_text.see(tk.END)
        self.full_log_text.configure(state=tk.DISABLED)

    # =========================================================================
    # Bottom Activity Bar & Collapsible Console
    # =========================================================================
    def _build_bottom_bar(self):
        self.log_buffer = ""

        self.bottom_bar = tk.Frame(self.main_container, bg=COLOR_SIDEBAR, height=36, highlightbackground=COLOR_CARD_BORDER, highlightthickness=1)
        self.bottom_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.bottom_bar.pack_propagate(False)

        self.lbl_status_ticker = tk.Label(self.bottom_bar, text="Ready", font=(FONT_FAMILY, 8),
                                          fg=COLOR_TEXT_MUTED, bg=COLOR_SIDEBAR)
        self.lbl_status_ticker.pack(side=tk.LEFT, padx=16)

        btn_view_logs = ModernButton(self.bottom_bar, text="Console ▾", font=(FONT_FAMILY, 7, "bold"),
                                     bg=COLOR_SIDEBAR, hover_bg=COLOR_SIDEBAR_ACTIVE, fg=COLOR_TEXT_SECONDARY,
                                     padx=8, pady=2, command=lambda: self.switch_page("logs"))
        btn_view_logs.pack(side=tk.RIGHT, padx=12)

    def log(self, message: str, level: str = "INFO"):
        timestamp = time.strftime("%H:%M:%S")
        entry = f"[{timestamp}] [{level}] {message}\n"
        self.log_buffer += entry

        if hasattr(self, "lbl_status_ticker"):
            self.lbl_status_ticker.configure(text=f"● {message}")

        if hasattr(self, "full_log_text") and self.full_log_text.winfo_exists():
            self.full_log_text.configure(state=tk.NORMAL)
            self.full_log_text.insert(tk.END, entry)
            self.full_log_text.see(tk.END)
            self.full_log_text.configure(state=tk.DISABLED)

    def clear_log(self):
        self.log_buffer = ""
        if hasattr(self, "full_log_text") and self.full_log_text.winfo_exists():
            self.full_log_text.configure(state=tk.NORMAL)
            self.full_log_text.delete("1.0", tk.END)
            self.full_log_text.configure(state=tk.DISABLED)

    # =========================================================================
    # Background Device Scanner
    # =========================================================================
    def async_refresh_device(self):
        def worker():
            self.log("Scanning ADB interfaces for connected tablet...")
            if not self.adb.is_adb_installed():
                self.log("Downloading Google Android platform-tools...")
                try:
                    self.adb.download_platform_tools()
                    self.log("Platform-tools initialized successfully.")
                except Exception as e:
                    self.log(f"Platform-tools error: {e}", "ERROR")
                    self._update_device_ui(None, "error")
                    return

            devices = self.adb.get_connected_devices()
            if not devices:
                self._update_device_ui(None, "none")
                return

            active = [d for d in devices if d["status"] == "device"]
            if not active:
                first = devices[0]
                self._update_device_ui(first, "unauthorized")
                return

            serial = active[0]["serial"]
            info = self.adb.get_device_info(serial)
            installed = set(self.adb.get_installed_packages(serial))

            self.device_info = info
            self.active_serial = serial
            self.installed_packages = installed

            self._update_device_ui(info, "connected")

        threading.Thread(target=worker, daemon=True).start()

    def _update_device_ui(self, info, state):
        if state == "connected":
            market = info.get("market_name", "Samsung Device")
            model = info.get("model", "")
            oneui = info.get("oneui_version", "?")
            batt = info.get("battery", "")
            batt_str = f" • Battery {batt}" if batt else ""
            txt = f"{market} ({model}) • One UI {oneui}{batt_str}"
            self.device_chip_dot.configure(fg=COLOR_ACCENT_EMERALD)
            self.device_chip_text.configure(text=txt)
            self.log(f"Device ready: {market} [{model}] running One UI {oneui}")
        elif state == "unauthorized":
            self.device_chip_dot.configure(fg=COLOR_ACCENT_AMBER)
            self.device_chip_text.configure(text="Unlock Tablet & Allow USB Debugging")
            self.log("Device unauthorized. Tap 'Always allow from this computer' on screen.", "WARN")
        else:
            self.device_chip_dot.configure(fg=COLOR_ACCENT_ROSE)
            self.device_chip_text.configure(text="No Device Connected")
            self.log("No device detected. Connect Tab S9 FE with USB Debugging enabled.", "WARN")

        # Auto refresh package lists if on those pages
        if self.current_page == "packages":
            self.after(0, self._filter_packages)
        elif self.current_page == "restore":
            self.after(0, self._refresh_restore_table)

    # =========================================================================
    # Execution Logic
    # =========================================================================
    def _execute_preset(self, preset, mode, apply_tweak):
        if not self.active_serial:
            messagebox.showwarning("Device Not Connected", "Please connect your Samsung Tab S9 FE with USB Debugging enabled.")
            return

        pkgs = preset["packages"]
        action_verb = "Safe Disable" if mode == "disable" else "Full User 0 Uninstall"
        tweak_note = "\n⚡ 0.5x UI Speed Accelerator will also be applied." if apply_tweak else ""

        if not messagebox.askyesno("Confirm Debloat Preset",
                                   f"Apply '{preset['name']}'?\n\nMode: {action_verb}\nTarget Packages: {len(pkgs)}{tweak_note}\n\nA backup snapshot will be recorded automatically."):
            return

        def worker():
            if apply_tweak and self.active_serial:
                self.adb.set_animation_scale(0.5, self.active_serial)
                self.log("⚡ Window & Transition animation scale set to 0.5x.")

            self._run_debloat_batch(pkgs, mode)

        threading.Thread(target=worker, daemon=True).start()

    def _execute_custom_debloat(self):
        if not self.active_serial:
            messagebox.showwarning("Device Not Connected", "Please connect your Samsung tablet first.")
            return

        selected = [pid for pid, var in self.package_vars.items() if var.get()]
        if not selected:
            messagebox.showinfo("No Selection", "Please check at least one package to debloat.")
            return

        mode = self.custom_mode_var.get()
        action_verb = "Safe Disable" if mode == "disable" else "Full User 0 Uninstall"

        if not messagebox.askyesno("Confirm Debloat",
                                   f"Ready to {action_verb} {len(selected)} selected packages?\n\nA backup snapshot will be saved to your backups folder."):
            return

        def worker():
            self._run_debloat_batch(selected, mode)

        threading.Thread(target=worker, daemon=True).start()

    def _run_debloat_batch(self, package_ids, mode):
        self.log(f"Starting batch debloat of {len(package_ids)} packages ({mode} mode)...")

        # Snapshot backup
        installed_list = self.adb.get_installed_packages(self.active_serial)
        snap = utils.create_backup_snapshot(self.device_info, installed_list)
        self.log(f"Backup snapshot saved: {snap.name}")

        pkg_map = database.get_package_map()
        success_count = 0

        for i, pid in enumerate(package_ids, 1):
            name = pkg_map.get(pid, {}).get("name", pid)
            self.log(f"[{i}/{len(package_ids)}] Processing: {name} ({pid})...")

            if mode == "disable":
                ok, msg = self.adb.disable_package(pid, self.active_serial)
            else:
                ok, msg = self.adb.uninstall_package(pid, keep_data=True, serial=self.active_serial)

            if ok:
                success_count += 1
                utils.log_debloat_action(pid, mode, True, note=name)
                self.log(f" -> SUCCESS: {pid}")
            else:
                utils.log_debloat_action(pid, mode, False, note=msg)
                self.log(f" -> SKIPPED / NOT FOUND: {pid} ({msg})", "WARN")

        self.log(f"Batch completed: {success_count}/{len(package_ids)} packages processed successfully.", "SUCCESS")
        self.installed_packages = set(self.adb.get_installed_packages(self.active_serial))

        if self.current_page == "packages":
            self.after(0, self._filter_packages)
        elif self.current_page == "restore":
            self.after(0, self._refresh_restore_table)

        messagebox.showinfo("Debloat Complete",
                            f"Successfully debloated {success_count} of {len(package_ids)} packages!\n\nA quick tablet reboot is recommended to clean background memory.")

    def _restore_selected_action(self):
        if not hasattr(self, "restore_tree"):
            return
        selected = self.restore_tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select one or more packages from the table to restore.")
            return
        self._run_restore_batch(list(selected))

    def _restore_all_action(self):
        if not hasattr(self, "restore_tree"):
            return
        all_items = list(self.restore_tree.get_children())
        if not all_items:
            messagebox.showinfo("Nothing to Restore", "No uninstalled packages found on the device.")
            return
        if messagebox.askyesno("Confirm Full Restore", f"Restore all {len(all_items)} packages back to your tablet?"):
            self._run_restore_batch(all_items)

    def _run_restore_batch(self, package_ids):
        def worker():
            self.log(f"Restoring {len(package_ids)} packages...")
            restored = 0
            pkg_map = database.get_package_map()

            for pid in package_ids:
                name = pkg_map.get(pid, {}).get("name", pid)
                self.log(f"Restoring {name} ({pid})...")
                ok, msg = self.adb.restore_package(pid, self.active_serial)
                if ok:
                    restored += 1
                    utils.remove_from_debloat_history(pid)
                    self.log(f" -> RESTORED: {pid}")
                else:
                    self.log(f" -> FAILED: {pid} ({msg})", "WARN")

            self.log(f"Restoration finished: {restored}/{len(package_ids)} packages active.")
            self.installed_packages = set(self.adb.get_installed_packages(self.active_serial))
            self.after(0, self._refresh_restore_table)
            messagebox.showinfo("Restore Complete", f"Successfully restored {restored} package(s)!")

        threading.Thread(target=worker, daemon=True).start()

    def _set_speed_scale(self, scale: float):
        if not self.active_serial:
            messagebox.showwarning("Device Not Connected", "Please connect your tablet first.")
            return
        ok = self.adb.set_animation_scale(scale, self.active_serial)
        if ok:
            self.log(f"Window animation scale set to {scale}x successfully.")
            messagebox.showinfo("Tweak Applied", f"Animation scale successfully set to {scale}x!")
        else:
            self.log("Failed to set animation scale.", "ERROR")
            messagebox.showerror("Error", "Could not set animation scale.")

    def _reboot_action(self):
        if not self.active_serial:
            messagebox.showwarning("Device Not Connected", "Please connect your tablet first.")
            return
        if messagebox.askyesno("Confirm Reboot", "Do you want to reboot your tablet now?"):
            self.adb.reboot_device(self.active_serial)
            self.log("Reboot command sent to tablet.")
            self._update_device_ui(None, "none")

    # =========================================================================
    # Support Modal
    # =========================================================================
    def _show_support_modal(self):
        modal = tk.Toplevel(self)
        modal.title("Support Tab S9 FE Debloater Toolkit")
        modal.geometry("390x290")
        modal.configure(bg=COLOR_CARD)
        modal.resizable(False, False)
        modal.transient(self)
        modal.grab_set()

        lbl = tk.Label(modal, text="☕ Support & Donations", font=(FONT_FAMILY, 12, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD)
        lbl.pack(pady=(18, 4))

        sub = tk.Label(modal, text="If this toolkit helped make your Tab S9 FE snappier,\nconsider supporting maintenance and future updates!",
                       font=(FONT_FAMILY, 8), fg=COLOR_TEXT_SECONDARY, bg=COLOR_CARD, justify=tk.CENTER)
        sub.pack(pady=(0, 14))

        b_bmac = ModernButton(modal, text="☕ Buy Me a Coffee", font=(FONT_FAMILY, 9, "bold"),
                              bg="#f59e0b", hover_bg="#d97706", fg="#000000", padx=12, pady=6, width=28,
                              command=lambda: [webbrowser.open("https://buymeacoffee.com/kavangcb29"), modal.destroy()])
        b_bmac.pack(pady=4)

        b_kofi = ModernButton(modal, text="❤️ Ko-fi Support", font=(FONT_FAMILY, 9, "bold"),
                              bg="#e53e3e", hover_bg="#dc2626", fg="#ffffff", padx=12, pady=6, width=28,
                              command=lambda: [webbrowser.open("https://ko-fi.com/kavangcb29"), modal.destroy()])
        b_kofi.pack(pady=4)

        b_paypal = ModernButton(modal, text="💳 PayPal (Direct: paypal.me/KavanSudev)", font=(FONT_FAMILY, 9, "bold"),
                                bg="#0070ba", hover_bg="#005ea6", fg="#ffffff", padx=12, pady=6, width=28,
                                command=lambda: [webbrowser.open("https://paypal.me/KavanSudev"), modal.destroy()])
        b_paypal.pack(pady=4)


def main():
    app = DebloaterGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
