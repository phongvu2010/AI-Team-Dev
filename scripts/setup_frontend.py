#!/usr/bin/env python3
"""Frontend & Mobile Architecture Configurator (`scripts/setup_frontend.py`).

Allows switching or scaffolding the client architecture across:
1. Web Next.js 15 App Router + Tailwind CSS (Default SSR / SEO)
2. Web React Vite + Tailwind CSS (SPA / Dashboard / PWA)
3. Mobile React Native + Expo + NativeWind (iOS & Android)

Usage:
    python scripts/setup_frontend.py --status
    python scripts/setup_frontend.py --preset vite
    python scripts/setup_frontend.py --preset nextjs
    python scripts/setup_frontend.py --add-mobile
"""

import argparse
import shutil
import sys
from pathlib import Path

# Safe UTF-8 reconfiguration for Windows console
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT_DIR / "src" / "frontend"
MOBILE_DIR = ROOT_DIR / "src" / "mobile"
PRESETS_DIR = ROOT_DIR / "templates" / "presets"


def get_current_web_framework() -> str:
    """Detect current framework in src/frontend/."""
    if not FRONTEND_DIR.exists():
        return "None (Directory missing)"
    pkg_json = FRONTEND_DIR / "package.json"
    if not pkg_json.exists():
        return "Unknown"
    try:
        content = pkg_json.read_text(encoding="utf-8")
        if '"next"' in content:
            return "Next.js 15 (App Router + React 19)"
        elif '"vite"' in content:
            return "React + Vite (SPA + Tailwind CSS)"
    except Exception:
        pass
    return "Custom / Other"


def print_status() -> None:
    print("=" * 65)
    print("📱 AI Team Dev — Frontend & Mobile Architecture Status")
    print("=" * 65)

    web_fw = get_current_web_framework()
    print("\n🌐 Web Client (src/frontend/):")
    print(f"   • Framework: {web_fw}")
    print("   • Styling:   Tailwind CSS")

    print("\n📲 Mobile Client (src/mobile/):")
    if MOBILE_DIR.exists():
        print("   • Framework: React Native (Expo SDK 51+ / 52)")
        print("   • Styling:   NativeWind v4 (Tailwind CSS for Mobile)")
        print("   • Targets:   iOS & Android")
        print("   • Status:    ✅ Active")
    else:
        print("   • Status:    ℹ️ Not initialized (run: python scripts/setup_frontend.py --add-mobile)")

    print("\n" + "=" * 65)


def apply_preset(preset_name: str) -> bool:
    preset_dir = PRESETS_DIR / f"frontend-{preset_name}"
    if not preset_dir.exists():
        print(f"❌ Error: Preset '{preset_name}' not found at {preset_dir}")
        return False

    print(f"🔄 Switching src/frontend/ to preset: {preset_name}...")

    try:
        if FRONTEND_DIR.exists():
            # Remove all files except node_modules to avoid slow re-installs if compatible
            for item in FRONTEND_DIR.iterdir():
                if item.name not in ["node_modules", ".next"]:
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
        else:
            FRONTEND_DIR.mkdir(parents=True, exist_ok=True)

        # Copy preset files into src/frontend/
        for item in preset_dir.iterdir():
            dest = FRONTEND_DIR / item.name
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)

        print(f"✅ Successfully switched Web Client to: {preset_name.upper()}")
        print("👉 Run: npm --prefix src/frontend install (if dependencies changed)")
        print("👉 Run: npm --prefix src/frontend run typecheck")
        return True
    except Exception as e:
        print(f"❌ Error applying preset: {e}")
        return False


def add_mobile() -> bool:
    preset_dir = PRESETS_DIR / "mobile-react-native"
    if not preset_dir.exists():
        print(f"❌ Error: Mobile preset not found at {preset_dir}")
        return False

    print("🚀 Initializing Mobile App at src/mobile/...")
    try:
        MOBILE_DIR.mkdir(parents=True, exist_ok=True)
        for item in preset_dir.iterdir():
            dest = MOBILE_DIR / item.name
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)

        print("✅ React Native (Expo + NativeWind) Mobile App ready at src/mobile/!")
        print("👉 Run: npm --prefix src/mobile install")
        print("👉 Run: npm --prefix src/mobile run start (or 'npx expo start')")
        return True
    except Exception as e:
        print(f"❌ Error setting up mobile: {e}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Configure Frontend & Mobile options")
    parser.add_argument("--status", action="store_true", help="Show current client configuration")
    parser.add_argument("--preset", choices=["nextjs", "vite"], help="Switch Web frontend preset")
    parser.add_argument("--add-mobile", action="store_true", help="Scaffold React Native Mobile App in src/mobile/")

    args = parser.parse_args()

    if args.preset:
        success = apply_preset(args.preset)
        print_status()
        return 0 if success else 1

    if args.add_mobile:
        success = add_mobile()
        print_status()
        return 0 if success else 1

    # Default action
    print_status()
    return 0


if __name__ == "__main__":
    sys.exit(main())
