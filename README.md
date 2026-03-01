# Easy ADB Installer

Install ANY APK, APKM, or XAPK file to your Android device using Linux.

## Requirements

- Linux
- Python 3
- ADB installed:
  sudo apt install adb
- USB debugging enabled

## How To Use

1. Put ANY .apk, .apkm, or .xapk files in this folder.
2. Connect your device via USB.
3. Run:

   python3 easy_adb_installer.py

4. Wait.
5. Done.

The script automatically:
- Extracts bundles
- Installs split APKs properly
- Cleans up temporary files