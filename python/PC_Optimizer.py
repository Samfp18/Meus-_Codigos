import os
import subprocess
import ctypes
import shutil
import sys
import winreg
from typing import List, Optional


def clean_temp_files() -> None:
    """Remove arquivos temporários do sistema."""
    temp_paths: List[Optional[str]] = [
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


def set_power_plan_high_performance() -> None:
    """Define o plano de energia para Alto Desempenho."""
    try:
        subprocess.run(
            ['powercfg', '/setactive', '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'],
            check=True
        )
    except Exception:
        pass


def disable_startup_programs() -> None:
    """Desativa programas de inicialização desnecessários (exemplo)."""
    startup_keys: List[str] = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
        r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Run"
    ]
    for key_path in startup_keys:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
                i: int = 0
                while True:
                    try:
                        value_name, value_data, value_type = winreg.EnumValue(key, i)
                        # Aqui você pode adicionar lógica para desativar seletivamente programas
                        i += 1
                    except OSError:
                        break
        except Exception:
            pass


def optimize_responsiveness() -> None:
    """Define a prioridade do processo atual para Alta."""
    try:
        pid: int = os.getpid()
        PROCESS_SET_INFORMATION: int = 0x0200
        HIGH_PRIORITY_CLASS: int = 0x00000080
        handle: int = ctypes.windll.kernel32.OpenProcess(PROCESS_SET_INFORMATION, False, pid)
        ctypes.windll.kernel32.SetPriorityClass(handle, HIGH_PRIORITY_CLASS)
        ctypes.windll.kernel32.CloseHandle(handle)
    except Exception:
        pass


def reduce_freezes() -> None:
    """Ajusta o registro para melhorar a responsividade do sistema."""
    try:
        key_path: str = r'SYSTEM\CurrentControlSet\Control\PriorityControl'
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE) as key:
            # Define Win32PrioritySeparation para 0x26 (melhor responsividade)
            winreg.SetValueEx(key, 'Win32PrioritySeparation', 0, winreg.REG_DWORD, 0x26)
    except Exception:
        pass


def main() -> None:
    """Executa todas as etapas de otimização do PC."""
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
