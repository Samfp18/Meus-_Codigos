import os
import subprocess
import shutil
import ctypes
import platform
import psutil
from typing import Optional


def clean_temp_files() -> None:
    """Remove arquivos temporários do Windows (TEMP e Windows\Temp)."""
    temp_paths = [
        os.getenv('TEMP'),
        os.getenv('TMP'),
        r'C:\Windows\Temp'
    ]
    for path in temp_paths:
        if path and os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                    except PermissionError:
                        continue
                for name in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, name))
                    except PermissionError:
                        continue


def clear_dns_cache() -> None:
    """Limpa cache DNS do Windows."""
    if platform.system() == 'Windows':
        subprocess.run(['ipconfig', '/flushdns'], shell=True)


def optimize_startup() -> None:
    """
    Lista programas configurados para iniciar junto com o Windows.
    (Por segurança, não remove nada automaticamente).
    """
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run"
        )
        i = 0
        while True:
            try:
                name, value, _ = winreg.EnumValue(key, i)
                print(f"Startup: {name} -> {value}")
                i += 1
            except OSError:
                break
    except ImportError:
        pass


def clear_event_logs() -> None:
    """Limpa logs de eventos do Windows."""
    if platform.system() == 'Windows':
        logs = ['Application', 'System', 'Security']
        for log in logs:
            subprocess.run(['wevtutil', 'cl', log], shell=True)


def disk_defragment() -> None:
    """Executa desfragmentação no disco C:."""
    if platform.system() == 'Windows':
        subprocess.run(['defrag', 'C:', '/U', '/V'], shell=True)


def check_disk_errors() -> None:
    """Executa verificação de disco (CHKDSK) em C:."""
    if platform.system() == 'Windows':
        subprocess.run(['chkdsk', 'C:', '/F', '/R'], shell=True)


def clear_browser_cache() -> None:
    """Remove cache dos navegadores Chrome e Firefox."""
    chrome_cache = os.path.expandvars(
        r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache'
    )
    firefox_cache = os.path.expandvars(r'%APPDATA%\Mozilla\Firefox\Profiles')

    def remove_cache(path: str) -> None:
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
            except PermissionError:
                pass

    remove_cache(chrome_cache)

    if os.path.exists(firefox_cache):
        for profile in os.listdir(firefox_cache):
            cache_path = os.path.join(firefox_cache, profile, 'cache2')
            remove_cache(cache_path)


def free_memory() -> None:
    """Tenta liberar memória standby no Windows."""
    if platform.system() == 'Windows':
        try:
            ctypes.windll.kernel32.SetProcessWorkingSetSize(-1, -1, -1)
        except Exception:
            pass


def clean_registry() -> None:
    """Placeholder para futuras limpezas de registro."""
    print("[!] Função de limpeza de registro não implementada.")


def manage_services() -> None:
    """Placeholder para gerenciamento de serviços do Windows."""
    print("[!] Função de gerenciamento de serviços não implementada.")


def check_updates() -> None:
    """Placeholder para verificação de atualizações do Windows."""
    print("[!] Função de verificação de updates não implementada.")


def network_optimizations() -> None:
    """Placeholder para otimizações de rede."""
    print("[!] Função de otimização de rede não implementada.")


def clean_prefetch() -> None:
    """Remove arquivos de prefetch do Windows."""
    prefetch_path = r'C:\Windows\Prefetch'
    if os.path.exists(prefetch_path):
        for file in os.listdir(prefetch_path):
            try:
                os.remove(os.path.join(prefetch_path, file))
            except PermissionError:
                continue


def monitor_system() -> None:
    """Exibe uso atual de CPU e disco."""
    cpu = psutil.cpu_percent(interval=1)
    disk = psutil.disk_usage('/')
    print(f"CPU: {cpu}% | Disco: {disk.percent}%")


def schedule_maintenance() -> None:
    """Placeholder para agendamento de tarefas de manutenção."""
    print("[!] Função de agendamento não implementada.")


def system_info() -> None:
    """Mostra informações básicas do sistema."""
    print(f"Sistema: {platform.system()} {platform.release()}")
    print(f"Processador: {platform.processor()}")
    print(f"RAM total: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB")


def optimize_battery() -> None:
    """Ativa plano de economia de energia no Windows."""
    if platform.system() == 'Windows':
        try:
            subprocess.run(
                ['powercfg', '/setactive', 'a1841308-3541-4fab-bc81-f71556f20b4a'],
                shell=True
            )
            print("[+] Modo de economia de bateria ativado.")
        except Exception as e:
            print(f"[!] Falha ao aplicar otimização de bateria: {e}")
    else:
        print("Bateria só pode ser otimizada no Windows.")


def main() -> None:
    """Executa todas as funções de otimização disponíveis."""
    clean_temp_files()
    clear_dns_cache()
    optimize_startup()
    clear_event_logs()
    disk_defragment()
    check_disk_errors()
    clear_browser_cache()
    free_memory()
    optimize_battery()
    clean_registry()
    manage_services()
    check_updates()
    network_optimizations()
    clean_prefetch()
    monitor_system()
    schedule_maintenance()
    system_info()


if __name__ == "__main__":
    main()
