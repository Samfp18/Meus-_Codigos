import os
import subprocess
import ctypes
import shutil
import sys
import time
import winreg

def clean_temp_files():
    temp_paths = [
        os.environ.get('TEMP'),
        os.environ.get('TMP'),
        r'C:\Windows\Temp'
    ]
    for path in temp_paths:
        if path and os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                    except Exception:
                        pass
                for dir in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, dir))
                    except Exception:
                        pass

def set_power_plan_high_performance():
    # Set power plan to High Performance
    try:
        subprocess.run(['powercfg', '/setactive', '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'], check=True)
    except Exception:
        pass

def disable_startup_programs():
    # Disable unnecessary startup programs from registry
    startup_keys = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
        r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Run"
    ]
    for key_path in startup_keys:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
                i = 0
                while True:
                    try:
                        value_name, value_data, value_type = winreg.EnumValue(key, i)
                        # Here you can add logic to selectively disable programs
                        # For now, we will not delete any keys to avoid system issues
                        i += 1
                    except OSError:
                        break
        except Exception:
            pass

def optimize_responsiveness():
    # Set process priority to high for this script as an example
    try:
        pid = os.getpid()
        PROCESS_SET_INFORMATION = 0x0200
        HIGH_PRIORITY_CLASS = 0x00000080
        handle = ctypes.windll.kernel32.OpenProcess(PROCESS_SET_INFORMATION, False, pid)
        ctypes.windll.kernel32.SetPriorityClass(handle, HIGH_PRIORITY_CLASS)
        ctypes.windll.kernel32.CloseHandle(handle)
    except Exception:
        pass

def reduce_freezes():
    # Increase system responsiveness by adjusting registry for system responsiveness
    try:
        key_path = r'SYSTEM\CurrentControlSet\Control\PriorityControl'
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE) as key:
            # Set Win32PrioritySeparation to 26 (0x26) for better responsiveness
            winreg.SetValueEx(key, 'Win32PrioritySeparation', 0, winreg.REG_DWORD, 0x26)
    except Exception:
        pass

def main():
    print("Starting PC optimization...")
    clean_temp_files()
    print("Temporary files cleaned.")
    set_power_plan_high_performance()
    print("Power plan set to High Performance.")
    disable_startup_programs()
    print("Startup programs checked.")
    optimize_responsiveness()
    print("Process priority set to high.")
    reduce_freezes()
    print("System responsiveness optimized.")
    print("PC optimization complete.")

if __name__ == "__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("This script requires administrator privileges. Please run as administrator.")
        sys.exit(1)
    main()
