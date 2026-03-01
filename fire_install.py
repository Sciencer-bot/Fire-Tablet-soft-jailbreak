import os
import subprocess
import zipfile
import sys

def run(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip()

def check_adb():
    print("Checking for ADB...")
    if not run(["which", "adb"]):
        print("❌ ADB not found. Install with: sudo apt install adb")
        sys.exit(1)
    print("✅ ADB found")

def check_device():
    print("Checking for connected device...")
    devices = run(["adb", "devices"])
    if "device" not in devices:
        print("❌ No device detected. Enable USB debugging.")
        sys.exit(1)
    print("✅ Device connected")

def extract_apkm():
    for file in os.listdir():
        if file.endswith(".apkm"):
            print(f"Extracting {file}...")
            folder = file.replace(".apkm", "")
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall(folder)
            print("✅ Extracted")

def install_split_folder(folder):
    apks = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".apk"):
                apks.append(os.path.join(root, file))

    if apks:
        print(f"Installing from {folder}...")
        subprocess.run(["adb", "install-multiple", "-r"] + apks)
        print("✅ Installed")

def install_regular_apk(file):
    print(f"Installing {file}...")
    subprocess.run(["adb", "install", "-r", file])
    print("✅ Installed")

def reboot():
    print("Rebooting tablet...")
    subprocess.run(["adb", "reboot"])
    print("🎉 DONE")

def main():
    print("=== Fire Tablet Easy Installer ===")
    check_adb()
    check_device()
    extract_apkm()

    # Install extracted folders
    for folder in os.listdir():
        if os.path.isdir(folder):
            install_split_folder(folder)

    # Install normal APKs
    for file in os.listdir():
        if file.endswith(".apk"):
            install_regular_apk(file)

    reboot()

if __name__ == "__main__":
    main()
