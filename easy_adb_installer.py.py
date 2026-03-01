import os
import subprocess
import zipfile
import sys
import shutil

def run(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip()

def check_adb():
    print("🔍 Checking for ADB...")
    if not run(["which", "adb"]):
        print("❌ ADB not found.")
        print("Install it with: sudo apt install adb")
        sys.exit(1)
    print("✅ ADB found")

def check_device():
    print("🔌 Checking for connected device...")
    devices = run(["adb", "devices"])
    lines = devices.splitlines()
    if len(lines) <= 1 or "device" not in devices:
        print("❌ No device detected.")
        print("Enable USB debugging and reconnect.")
        sys.exit(1)
    print("✅ Device connected")

def extract_bundle(file):
    print(f"📦 Extracting {file}...")
    folder = file.replace(".apkm", "").replace(".xapk", "")
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(folder)
    print("✅ Extracted")
    return folder

def install_split_folder(folder):
    apks = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".apk"):
                apks.append(os.path.join(root, file))

    if apks:
        print(f"📲 Installing split package from {folder}...")
        subprocess.run(["adb", "install-multiple", "-r"] + apks)
        print("✅ Installed")

def install_regular_apk(file):
    print(f"📲 Installing {file}...")
    subprocess.run(["adb", "install", "-r", file])
    print("✅ Installed")

def cleanup(folder):
    if os.path.isdir(folder):
        shutil.rmtree(folder)

def main():
    print("=== Easy ADB Installer ===")

    check_adb()
    check_device()

    # First extract bundles
    extracted_folders = []
    for file in os.listdir():
        if file.endswith(".apkm") or file.endswith(".xapk"):
            folder = extract_bundle(file)
            extracted_folders.append(folder)

    # Install extracted bundles
    for folder in extracted_folders:
        install_split_folder(folder)
        cleanup(folder)

    # Install normal APKs
    for file in os.listdir():
        if file.endswith(".apk"):
            install_regular_apk(file)

    print("🎉 All installations complete!")

if __name__ == "__main__":
    main()