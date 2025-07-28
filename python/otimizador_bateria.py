import os
import psutil
import subprocess
import platform
import ctypes

def reduzir_brilho(nivel=20):
    """ Reduz o brilho da tela (Windows) """
    try:
        subprocess.run(f"powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{nivel})", shell=True)
        print(f"[+] Brilho ajustado para {nivel}%")
    except Exception as e:
        print(f"[-] Erro ao ajustar brilho: {e}")

def definir_plano_energia():
    """ Define o plano de energia para o modo de economia máxima """
    os.system("powercfg /setactive a1841308-3541-4fab-bc81-f71556f20b4a")  # Power Saver
    print("[+] Plano de energia ajustado para economia máxima")

def reduzir_taxa_atualizacao():
    """ Reduz a taxa de atualização da tela para economizar energia (se suportado) """
    try:
        os.system('powershell.exe "Set-DisplayResolution -Width 1366 -Height 768"')
        print("[+] Taxa de atualização reduzida para economizar energia")
    except Exception as e:
        print(f"[-] Erro ao reduzir taxa de atualização: {e}")

def reduzir_efeitos_visuais():
    """ Reduz os efeitos visuais do Windows para economizar energia """
    try:
        os.system('reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f')
        print("[+] Efeitos visuais reduzidos")
    except Exception as e:
        print(f"[-] Erro ao reduzir efeitos visuais: {e}")

def reduzir_prioridade_processos():
    """ Reduz a prioridade de processos pesados para economizar energia """
    processos_prioridade_baixa = ["discord.exe", "steam.exe", "obs.exe"]
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if proc.info['name'].lower() in processos_prioridade_baixa:
                p = psutil.Process(proc.info['pid'])
                p.nice(psutil.IDLE_PRIORITY_CLASS)  # Define prioridade baixa
                print(f"[+] Prioridade reduzida: {proc.info['name']}")
        except Exception as e:
            print(f"[-] Erro ao reduzir prioridade de {proc.info['name']}: {e}")

def limitar_uso_cpu():
    """ Reduz o uso da CPU para economizar energia """
    try:
        os.system("powercfg -attributes SUB_PROCESSOR PROCTHROTTLEMAX -ATTRIB_HIDE")
        os.system("powercfg -setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 50")  # 50% do uso máximo da CPU
        os.system("powercfg -setactive SCHEME_CURRENT")
        print("[+] Limite de uso da CPU ajustado para 50%")
    except Exception as e:
        print(f"[-] Erro ao limitar uso da CPU: {e}")

def otimizar_bateria():
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
        if ctypes.windll.shell32.IsUserAnAdmin():  # Verifica se o script está rodando como administrador
            otimizar_bateria()
        else:
            print("[-] Execute o script como administrador para aplicar todas as otimizações.")
    else:
        print("[-] Este script foi desenvolvido apenas para Windows.")
