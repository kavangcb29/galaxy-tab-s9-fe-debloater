"""
Samsung Tab S9 FE Debloater - Package Database & Catalog
Curated specifically for Samsung Galaxy Tab S9 FE (SM-X510 / SM-X516B) and One UI 6 / 6.1 / 7 / 8 / 8.5 / 9.
"""

from typing import Dict, List, Any

# Risk Levels:
# 'safe'    : No impact on tablet functionality or S Pen; zero crashes; fully recommended.
# 'optional': Useful for some users, but safe to remove if not used (e.g. Samsung Browser, OneDrive).
# 'caution' : May disable an ecosystem feature (e.g. SmartThings, DeX, Galaxy Store, Phone sync).
# 'danger'  : CRITICAL tablet feature! (S Pen, Samsung Notes, Keyboard, DeX core, System UI). DO NOT REMOVE.

CATEGORIES = {
    "telemetry": "Telemetry, Analytics & Tracking",
    "meta_facebook": "Meta & Facebook Services",
    "microsoft": "Microsoft Pre-installs",
    "ar_emoji": "AR Zone & Emoji Junk",
    "bixby": "Bixby Voice & AI Services",
    "samsung_bloat": "Samsung Pre-installed Bloatware",
    "gos_gaming": "Game Optimizing Service (GOS) & Gaming Hub",
    "wifi_telephony": "Wi-Fi Tablet Telephony Cleanup (Wi-Fi Models)",
    "google_optional": "Google Bloatware & Optional Apps",
    "samsung_optional": "Samsung Ecosystem Apps (Optional)",
    "tablet_critical": "CRITICAL Tablet Features (S Pen, Notes, DeX - DO NOT REMOVE)"
}

PACKAGES: List[Dict[str, Any]] = [
    # ==========================================
    # 1. Telemetry, Analytics & Tracking (SAFE)
    # ==========================================
    {
        "id": "com.samsung.android.rubin.app",
        "name": "Samsung Customization Service (Rubin)",
        "category": "telemetry",
        "risk": "safe",
        "description": "Tracks usage patterns and location to serve personalized Samsung ads and recommendations."
    },
    {
        "id": "com.samsung.android.knox.analytics.uploader",
        "name": "Knox Analytics Uploader",
        "category": "telemetry",
        "risk": "safe",
        "description": "Collects and uploads enterprise and device analytics to Samsung Knox servers in background."
    },
    {
        "id": "com.sec.android.diagmonagent",
        "name": "Samsung Diagnostic Monitor Agent",
        "category": "telemetry",
        "risk": "safe",
        "description": "Background service sending automated diagnostic, crash reports and usage data to Samsung."
    },
    {
        "id": "com.samsung.android.da.daagent",
        "name": "Dual App Analytics Agent",
        "category": "telemetry",
        "risk": "safe",
        "description": "Analytics agent for dual messenger/app configurations."
    },
    {
        "id": "com.samsung.android.bbc.bbcagent",
        "name": "Samsung B2B Agent",
        "category": "telemetry",
        "risk": "safe",
        "description": "Samsung enterprise / business background management agent."
    },
    {
        "id": "com.google.android.feedback",
        "name": "Google Market Feedback Agent",
        "category": "telemetry",
        "risk": "safe",
        "description": "Sends crash feedback and telemetry reports back to Google Play."
    },
    {
        "id": "com.google.android.gms.location.history",
        "name": "Google Location History Tracker",
        "category": "telemetry",
        "risk": "safe",
        "description": "Google location reporting and timeline tracker service."
    },
    {
        "id": "com.samsung.android.ipsgeofence",
        "name": "Samsung Geofence Service",
        "category": "telemetry",
        "risk": "safe",
        "description": "Location fencing service used for location-based Samsung ads and store visit tracking."
    },

    # ==========================================
    # 2. Meta & Facebook Services (SAFE)
    # ==========================================
    {
        "id": "com.facebook.katana",
        "name": "Facebook Client App",
        "category": "meta_facebook",
        "risk": "safe",
        "description": "Preloaded Facebook client app stub."
    },
    {
        "id": "com.facebook.system",
        "name": "Meta App Installer",
        "category": "meta_facebook",
        "risk": "safe",
        "description": "Background system installer for Meta/Facebook updates and stealth downloads."
    },
    {
        "id": "com.facebook.appmanager",
        "name": "Meta App Manager",
        "category": "meta_facebook",
        "risk": "safe",
        "description": "Background daemon managing Facebook apps without Google Play store."
    },
    {
        "id": "com.facebook.services",
        "name": "Meta Services",
        "category": "meta_facebook",
        "risk": "safe",
        "description": "Background background daemon maintaining Meta connectivity and ad profiling."
    },

    # ==========================================
    # 3. Microsoft Pre-installs (SAFE / OPTIONAL)
    # ==========================================
    {
        "id": "com.microsoft.skydrive",
        "name": "Microsoft OneDrive",
        "category": "microsoft",
        "risk": "optional",
        "description": "Pre-installed OneDrive. Note: Samsung Gallery syncs with OneDrive if enabled."
    },
    {
        "id": "com.microsoft.office.officehubrow",
        "name": "Microsoft 365 (Office)",
        "category": "microsoft",
        "risk": "safe",
        "description": "Preloaded Microsoft Office / 365 hub app."
    },
    {
        "id": "com.microsoft.office.outlook",
        "name": "Microsoft Outlook",
        "category": "microsoft",
        "risk": "optional",
        "description": "Pre-installed Microsoft Outlook email client (Preserved and excluded from debloat presets)."
    },
    {
        "id": "com.microsoft.appmanager",
        "name": "Link to Windows Service",
        "category": "microsoft",
        "risk": "optional",
        "description": "Pre-installed daemon for pairing tablet with Windows PC (Your Phone Companion)."
    },

    # ==========================================
    # 4. AR Zone & Emoji Junk (SAFE)
    # ==========================================
    {
        "id": "com.samsung.android.aremoji",
        "name": "AR Emoji",
        "category": "ar_emoji",
        "risk": "safe",
        "description": "Samsung 3D avatar generator. Takes up noticeable storage and RAM."
    },
    {
        "id": "com.samsung.android.aremojieditor",
        "name": "AR Emoji Editor",
        "category": "ar_emoji",
        "risk": "safe",
        "description": "Avatar customization and clothing editor."
    },
    {
        "id": "com.samsung.android.arzone",
        "name": "AR Zone",
        "category": "ar_emoji",
        "risk": "safe",
        "description": "Hub for AR Doodle, Quick Measure, and AR emojis in camera."
    },
    {
        "id": "com.samsung.android.livestickers",
        "name": "Deco Pic / Live Stickers",
        "category": "ar_emoji",
        "risk": "safe",
        "description": "Live sticker and decorative filter overlays for camera."
    },
    {
        "id": "com.sec.android.mimage.avatarstickers",
        "name": "Avatar Stickers",
        "category": "ar_emoji",
        "risk": "safe",
        "description": "Generates animated sticker packs from your AR avatar."
    },
    {
        "id": "com.samsung.android.app.camera.sticker.facearavatar.preload",
        "name": "Face AR Avatar Preload",
        "category": "ar_emoji",
        "risk": "safe",
        "description": "Preloaded avatar facial tracking asset assets."
    },
    {
        "id": "com.samsung.android.stickercenter",
        "name": "Samsung Sticker Center",
        "category": "ar_emoji",
        "risk": "safe",
        "description": "Store for downloading additional keyboard and photo stickers."
    },

    # ==========================================
    # 5. Bixby Voice & AI Services (SAFE TO OPTIONAL)
    # ==========================================
    {
        "id": "com.samsung.android.bixby.agent",
        "name": "Bixby Voice Assistant",
        "category": "bixby",
        "risk": "safe",
        "description": "Samsung's voice assistant background service. Safe to remove if you do not use Bixby."
    },
    {
        "id": "com.samsung.android.bixby.wakeup",
        "name": "Bixby Voice Wakeup",
        "category": "bixby",
        "risk": "safe",
        "description": "Constantly listens in background for 'Hi Bixby' hotword. Disabling saves battery."
    },
    {
        "id": "com.samsung.android.bixby.service",
        "name": "Bixby Service",
        "category": "bixby",
        "risk": "safe",
        "description": "Core background coordination service for Bixby integration."
    },
    {
        "id": "com.samsung.android.visionintelligence",
        "name": "Bixby Vision",
        "category": "bixby",
        "risk": "safe",
        "description": "Visual camera search & translation. Note: Google Lens is faster and more accurate."
    },
    {
        "id": "com.samsung.android.bixbyvision.framework",
        "name": "Bixby Vision Framework",
        "category": "bixby",
        "risk": "safe",
        "description": "Underlying libraries supporting camera image recognition via Bixby."
    },
    {
        "id": "com.samsung.android.app.spage",
        "name": "Samsung Free / Bixby Home",
        "category": "bixby",
        "risk": "safe",
        "description": "Leftmost home screen feed displaying sponsored news, games, and podcasts."
    },

    # ==========================================
    # 6. Samsung Pre-installed Bloatware (SAFE)
    # ==========================================
    {
        "id": "com.samsung.android.kidsinstaller",
        "name": "Samsung Kids Installer",
        "category": "samsung_bloat",
        "risk": "safe",
        "description": "Installer for parental sandbox mode. Safe to remove if you do not have young children."
    },
    {
        "id": "com.sec.android.app.kidshome",
        "name": "Samsung Kids Mode",
        "category": "samsung_bloat",
        "risk": "safe",
        "description": "Kids sandbox environment interface."
    },
    {
        "id": "com.samsung.android.app.tips",
        "name": "Samsung Tips",
        "category": "samsung_bloat",
        "risk": "safe",
        "description": "Sends periodic notifications about One UI tips and feature tutorials."
    },
    {
        "id": "com.samsung.ecomm",
        "name": "Samsung Shop",
        "category": "samsung_bloat",
        "risk": "safe",
        "description": "Samsung storefront app for purchasing Galaxy accessories and hardware."
    },
    {
        "id": "com.samsung.sree",
        "name": "Samsung Global Goals",
        "category": "samsung_bloat",
        "risk": "safe",
        "description": "Ad-supported charity lock screen and promotional app."
    },
    {
        "id": "com.samsung.android.dynamiclock",
        "name": "Dynamic Lock Screen / Glance",
        "category": "samsung_bloat",
        "risk": "safe",
        "description": "Downloads rotating wallpapers and sponsored stories to your lock screen."
    },
    {
        "id": "com.samsung.safetyinformation",
        "name": "Samsung Safety Information",
        "category": "samsung_bloat",
        "risk": "safe",
        "description": "Static regulatory and safety manual documentation."
    },
    {
        "id": "com.samsung.android.app.watchmanagerstub",
        "name": "Galaxy Wearable Stub",
        "category": "samsung_bloat",
        "risk": "safe",
        "description": "Stub installer for Galaxy Watch manager (can be reinstalled from Play Store)."
    },
    {
        "id": "com.samsung.android.forest",
        "name": "Samsung Digital Wellbeing (Digital Care / Forest)",
        "category": "samsung_bloat",
        "risk": "optional",
        "description": "Samsung screen time and digital wellbeing tracking engine (Preserved and excluded from debloat presets)."
    },
    {
        "id": "com.samsung.android.app.sharelive",
        "name": "Quick Share Live / Music Share",
        "category": "samsung_bloat",
        "risk": "safe",
        "description": "Background shared playback broadcast service."
    },
    {
        "id": "com.glance.internet",
        "name": "Glance on Samsung (India Lockscreen Feed)",
        "category": "samsung_bloat",
        "risk": "safe",
        "description": "Lock screen news and sponsored feed pre-installed on Indian firmware. Safe to remove."
    },
    {
        "id": "com.samsung.android.rapps",
        "name": "Samsung Regional App Recommendations (India)",
        "category": "samsung_bloat",
        "risk": "safe",
        "description": "Regional app suggestions and promotional recommendations stub found on Indian devices."
    },

    # ==========================================
    # 7. GOS (Game Optimizing Service) & Gaming Hub (SAFE)
    # ==========================================
    {
        "id": "com.samsung.android.game.gos",
        "name": "Game Optimizing Service (GOS)",
        "category": "gos_gaming",
        "risk": "safe",
        "description": "Throttles Exynos 1380 CPU & GPU performance to prevent heat. Removing unlocks full processor performance!"
    },
    {
        "id": "com.samsung.android.game.gamehome",
        "name": "Gaming Hub (Game Home)",
        "category": "gos_gaming",
        "risk": "safe",
        "description": "Samsung's game aggregation launcher with ads and instant plays."
    },
    {
        "id": "com.samsung.android.game.gametools",
        "name": "Game Booster / Tools",
        "category": "gos_gaming",
        "risk": "safe",
        "description": "In-game floating toolbar and screen recorder."
    },

    # ==========================================
    # 8. Wi-Fi Tablet Telephony Cleanup (SAFE FOR WI-FI SM-X510)
    # ==========================================
    {
        "id": "com.android.calllogbackup",
        "name": "Call Log Backup Service",
        "category": "wifi_telephony",
        "risk": "safe",
        "description": "Backs up cellular phone call history. Totally unneeded on Wi-Fi tablets."
    },
    {
        "id": "com.hiya.star",
        "name": "Hiya Spam Call Protection",
        "category": "wifi_telephony",
        "risk": "safe",
        "description": "Third-party spam call identifier daemon running constantly in memory."
    },
    {
        "id": "com.samsung.android.smartcallprovider",
        "name": "Smart Call Provider",
        "category": "wifi_telephony",
        "risk": "safe",
        "description": "Samsung caller ID and spam lookup engine. Useless on Wi-Fi tablets."
    },

    # ==========================================
    # 9. Google Bloatware & Optional Apps (OPTIONAL)
    # ==========================================
    {
        "id": "com.google.android.videos",
        "name": "Google TV (Play Movies)",
        "category": "google_optional",
        "risk": "safe",
        "description": "Movie store and streaming aggregator. Safe to remove."
    },
    {
        "id": "com.google.android.apps.tachyon",
        "name": "Google Meet (Duo)",
        "category": "google_optional",
        "risk": "safe",
        "description": "Video calling client. Safe to remove if you use Zoom, WhatsApp or Teams."
    },
    {
        "id": "com.google.android.apps.youtube.music",
        "name": "YouTube Music",
        "category": "google_optional",
        "risk": "safe",
        "description": "Pre-installed YT Music app. Safe to remove if using Spotify/Apple Music."
    },
    {
        "id": "com.google.android.youtube",
        "name": "YouTube",
        "category": "google_optional",
        "risk": "optional",
        "description": "Official YouTube app. Remove if using NewPipe, Grayjay, or Revanced."
    },
    {
        "id": "com.google.android.apps.docs",
        "name": "Google Drive",
        "category": "google_optional",
        "risk": "optional",
        "description": "Pre-installed Google Drive client."
    },
    {
        "id": "com.google.android.apps.photos",
        "name": "Google Photos",
        "category": "google_optional",
        "risk": "optional",
        "description": "Google cloud photo backup daemon. Remove if using local gallery or OneDrive."
    },
    {
        "id": "com.google.android.googlequicksearchbox",
        "name": "Google Search App & Assistant",
        "category": "google_optional",
        "risk": "optional",
        "description": "Main Google search bar widget and Google Assistant."
    },
    {
        "id": "com.android.chrome",
        "name": "Google Chrome",
        "category": "google_optional",
        "risk": "optional",
        "description": "Chrome browser. WARNING: Ensure you have another browser (Firefox/Brave) installed!"
    },

    # ==========================================
    # 10. Samsung Ecosystem Apps (OPTIONAL / CAUTION)
    # ==========================================
    {
        "id": "com.sec.android.app.sbrowser",
        "name": "Samsung Internet Browser",
        "category": "samsung_optional",
        "risk": "optional",
        "description": "Samsung web browser. Note: Has excellent tablet S Pen integration, but safe to remove if unused."
    },
    {
        "id": "com.sec.android.app.samsungapps",
        "name": "Galaxy Store",
        "category": "samsung_optional",
        "risk": "caution",
        "description": "Samsung app store. Needed for updating Samsung system apps, S Pen air actions, and Good Lock!"
    },
    {
        "id": "com.samsung.android.oneconnect",
        "name": "SmartThings",
        "category": "samsung_optional",
        "risk": "optional",
        "description": "Samsung Smart Home automation & device tracker. Remove if you do not use Samsung smart home."
    },
    {
        "id": "com.sec.android.app.shealth",
        "name": "Samsung Health",
        "category": "samsung_optional",
        "risk": "optional",
        "description": "Health & fitness tracker. Remove if you do not track workouts on your tablet."
    },
    {
        "id": "com.samsung.android.scloud",
        "name": "Samsung Cloud Sync",
        "category": "samsung_optional",
        "risk": "caution",
        "description": "Syncs Wi-Fi passwords, Bluetooth pairings, and Samsung Notes across devices."
    },
    {
        "id": "com.samsung.android.authfw",
        "name": "Samsung Pass Framework",
        "category": "samsung_optional",
        "risk": "optional",
        "description": "Samsung biometric password autofill."
    },
    {
        "id": "com.samsung.android.samsungpass",
        "name": "Samsung Pass",
        "category": "samsung_optional",
        "risk": "optional",
        "description": "Samsung password manager UI."
    },
    {
        "id": "com.samsung.android.spay",
        "name": "Samsung Wallet / Pay",
        "category": "samsung_optional",
        "risk": "optional",
        "description": "Samsung payment and loyalty card wallet."
    },
    {
        "id": "com.samsung.android.spaymini",
        "name": "Samsung Pay Mini (India Variant)",
        "category": "samsung_optional",
        "risk": "optional",
        "description": "Lightweight payment client pre-installed on Indian variant Galaxy tablets."
    },
    {
        "id": "com.samsung.android.themestore",
        "name": "Galaxy Themes",
        "category": "samsung_optional",
        "risk": "optional",
        "description": "Samsung theme engine and wallpaper store."
    },
    {
        "id": "com.samsung.android.homemode",
        "name": "Daily Board (Desk Dock Mode)",
        "category": "samsung_optional",
        "risk": "optional",
        "description": "Display mode showing clock, weather, and photos while tablet is charging."
    },

    # =========================================================================
    # 11. CRITICAL TABLET & S PEN COMPONENTS (DO NOT REMOVE - TAGGED AS DANGER)
    # =========================================================================
    {
        "id": "com.samsung.android.app.notes",
        "name": "Samsung Notes (CRITICAL S PEN)",
        "category": "tablet_critical",
        "risk": "danger",
        "description": "DO NOT REMOVE! Core handwriting and note-taking app optimized for S Pen low-latency."
    },
    {
        "id": "com.samsung.android.service.aircommand",
        "name": "S Pen Air Command (CRITICAL S PEN)",
        "category": "tablet_critical",
        "risk": "danger",
        "description": "DO NOT REMOVE! S Pen floating menu, button hover shortcuts, and smart select."
    },
    {
        "id": "com.samsung.android.spen.styluspen",
        "name": "Samsung Stylus S Pen Core Driver",
        "category": "tablet_critical",
        "risk": "danger",
        "description": "DO NOT REMOVE! Wacom EMR digitizer and S Pen driver backend."
    },
    {
        "id": "com.samsung.android.honeyboard",
        "name": "Samsung Keyboard (Honeyboard)",
        "category": "tablet_critical",
        "risk": "danger",
        "description": "DO NOT REMOVE! Contains S Pen handwriting-to-text engine. Removing without another keyboard locks tablet!"
    },
    {
        "id": "com.sec.android.desktopmode.uiservice",
        "name": "Samsung DeX System UI",
        "category": "tablet_critical",
        "risk": "danger",
        "description": "DO NOT REMOVE! Enables desktop multi-window mode on your Tab S9 FE screen."
    },
    {
        "id": "com.sec.android.app.desktoplauncher",
        "name": "Samsung DeX Launcher",
        "category": "tablet_critical",
        "risk": "danger",
        "description": "DO NOT REMOVE! Launcher UI for Samsung DeX workspace."
    },
    {
        "id": "com.sec.android.app.launcher",
        "name": "One UI Home (Main Tablet Launcher)",
        "category": "tablet_critical",
        "risk": "danger",
        "description": "DO NOT REMOVE! Default home screen launcher. Removing this will cause bootloop without 3rd party launcher."
    },
    {
        "id": "com.samsung.android.app.cocktailbarservice",
        "name": "Edge Panels & Split Screen Helper",
        "category": "tablet_critical",
        "risk": "danger",
        "description": "Edge panels, app pairs, and multitasking window controller."
    }
]

def get_packages_by_category(category_key: str) -> List[Dict[str, Any]]:
    return [p for p in PACKAGES if p["category"] == category_key]

def get_packages_by_risk(risk_level: str) -> List[Dict[str, Any]]:
    return [p for p in PACKAGES if p["risk"] == risk_level]

def get_package_map() -> Dict[str, Dict[str, Any]]:
    return {p["id"]: p for p in PACKAGES}
