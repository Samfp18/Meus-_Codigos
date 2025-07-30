import os
import psutil
import subprocess
import platform
import ctypes
from typing import List


def reduzir_brilho(nivel: int = 20) -> None:
    """
    Reduz o brilho da tela no Windows.

    Args:
        nivel (int): Percentual de brilho (0 a 100).
    """
    try:
        subprocess.run(
            f"powershell (Get-WmiObject -Namespace root/WMI -Class "
            f"WmiMonitorBrightnessMethods).WmiSetBrightness(1,{nivel})",
            shell=True, check=False
        )
        print(f"[+] Brilho ajustado para {nivel}%")
    except Exception as e:
        print(f"[-] Erro ao ajustar brilho: {e}")


def definir_plano_energia() -> None:
    """Define o plano de energia para modo de economia máxima (Power Saver)."""
    try:
        os.system("powercfg /setactive a1841308-3541-4fab-bc81-f71556f20b4a")
        print("[+] Plano de energia ajustado para economia máxima")
    except Exception as e:
        print(f"[-] Erro ao definir plano de energia: {e}")


def reduzir_taxa_atualizacao() -> None:
    """Reduz resolução/taxa de atualização para economizar energia (se suportado)."""
    try:
        os.system('powershell.exe "Set-DisplayResolution -Width 1366 -Height 768"')
        print("[+] Resolução reduzida para economizar energia")
    except Exception as e:
        print(f"[-] Erro ao reduzir taxa de atualização: {e}")


def reduzir_efeitos_visuais() -> None:
    """Reduz efeitos visuais do Windows para economizar energia."""
    try:
        os.system(
            'reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\'
            'CurrentVersion\\Explorer\\VisualEffects" '
            '/v VisualFXSetting /t REG_DWORD /d 2 /f'
        )
        print("[+] Efeitos visuais reduzidos")
    except Exception as e:
        print(f"[-] Erro ao reduzir efeitos visuais: {e}")


def reduzir_prioridade_processos(processos: List[str] = None) -> None:
    """
    Reduz a prioridade de processos pesados para economizar energia.

    Args:
        processos (List[str]): Lista de processos a reduzir prioridade.
    """
    if processos is None:
        processos = ["discord.exe", "steam.exe", "obs.exe"]

    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if proc.info['name'].lower() in processos:
                psutil.Process(proc.info['pid']).nice(psutil.IDLE_PRIORITY_CLASS)
                print(f"[+] Prioridade reduzida: {proc.info['name']}")
        except Exception as e:
            print(f"[-] Erro ao reduzir prioridade de {proc.info['name']}: {e}")


def limitar_uso_cpu(limite: int = 50) -> None:
    """
    Limita o uso da CPU para economizar energia.

    Args:
        limite (int): Percentual máximo de uso da CPU (0 a 100).
    """
    try:
        os.system("powercfg -attributes SUB_PROCESSOR PROCTHROTTLEMAX -ATTRIB_HIDE")
        os.system(f"powercfg -setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX {limite}")
        os.system("powercfg -setactive SCHEME_CURRENT")
        print(f"[+] Limite de uso da CPU ajustado para {limite}%")
    except Exception as e:
        print(f"[-] Erro ao limitar uso da CPU: {e}")


def otimizar_bateria() -> None:
    """Executa todas as otimizações de economia de bateria no Windows."""
    print("[*] Iniciando otimização máxima da bateria...")
    reduzir_brilho()
    definir_plano_energia()
    reduzir_taxa_atualizacao()
    reduzir_efeitos_visuais()
    reduzir_prioridade_processos()
    limitar_uso_cpu()
    print("[*] Otimização concluída com sucesso!")


if __name__ == "__main__":
    if platform.system() == "Windows":
        if ctypes.windll.shell32.IsUserAnAdmin():
            otimizar_bateria()
        else:
            print("[-] Execute o script como administrador para aplicar todas as otimizações.")
    else:
        print("[-] Este script foi desenvolvido apenas para Windows.")
