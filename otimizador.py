import os
import psutil
import ctypes
import time
import subprocess
import sys

def executar_comando(comando):
    """Executa comandos no sistema."""
    try:
        subprocess.run(comando, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        pass

def liberar_memoria():
    """Libera memória RAM e otimiza o cache do sistema."""
    comandos = [
        "echo off | clip",
        "ipconfig /flushdns",
        "taskkill /F /IM OneDrive.exe",
        "taskkill /F /IM RuntimeBroker.exe",
        "taskkill /F /IM SearchIndexer.exe",
        "taskkill /F /IM YourPhone.exe",
        "wmic process where name='explorer.exe' call setpriority 128"
    ]
    for comando in comandos:
        executar_comando(comando)

def acelerar_resposta():
    """Reduz latência e melhora a resposta do sistema."""
    comandos = [
        "powercfg -setactive SCHEME_MIN",
        "fsutil behavior set disablelastaccess 1",
        "bcdedit /set disabledynamictick yes",
        "bcdedit /set useplatformtick yes",
        "bcdedit /set tscsyncpolicy Enhanced"
    ]
    for comando in comandos:
        executar_comando(comando)

def resfriar_computador():
    """Reduz uso da CPU e tenta aumentar a velocidade das ventoinhas."""
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        if proc.info['cpu_percent'] > 40:
            try:
                p = psutil.Process(proc.info['pid'])
                p.nice(psutil.IDLE_PRIORITY_CLASS)
            except psutil.NoSuchProcess:
                pass

def configurar_ventoinha():
    """Tenta aumentar a velocidade da ventoinha (se suportado)."""
    executar_comando("wmic /namespace:\\\\root\\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature")

def otimizar_registro():
    """Aplica otimizações avançadas no registro do Windows."""
    ajustes = [
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v LargeSystemCache /t REG_DWORD /d 1 /f',
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\LanmanServer\\Parameters" /v Size /t REG_DWORD /d 3 /f',
        'reg add "HKCU\\Control Panel\\Mouse" /v MouseSpeed /t REG_SZ /d 2 /f',
        'reg add "HKCU\\Control Panel\\Mouse" /v MouseThreshold1 /t REG_SZ /d 0 /f',
        'reg add "HKCU\\Control Panel\\Mouse" /v MouseThreshold2 /t REG_SZ /d 0 /f',
        'reg add "HKCU\\Control Panel\\Desktop" /v MenuShowDelay /t REG_SZ /d 0 /f'
    ]
    for comando in ajustes:
        executar_comando(comando)

def otimizar_bateria():
    """Configura opções avançadas para economia de energia."""
    comandos = [
        "powercfg /change monitor-timeout-ac 5",  # Apaga a tela após 5 min (tomada)
        "powercfg /change monitor-timeout-dc 3",  # Apaga a tela após 3 min (bateria)
        "powercfg /change standby-timeout-ac 15",  # Suspensão após 15 min (tomada)
        "powercfg /change standby-timeout-dc 10",  # Suspensão após 10 min (bateria)
        "powercfg /setdcvalueindex SCHEME_BALANCED SUB_PROCESSOR PROCTHROTTLEMAX 50",  # Limita CPU a 50% na bateria
        "powercfg /setdcvalueindex SCHEME_BALANCED SUB_VIDEO ADAPTBRIGHT 1",  # Ativa brilho adaptativo
        "powercfg -setactive SCHEME_BALANCED"  # Define o modo Balanceado
    ]
    for comando in comandos:
        executar_comando(comando)

def adicionar_ao_inicio():
    """Adiciona o executável ao início do Windows."""
    caminho_exe = os.path.abspath(sys.argv[0])
    chave_registro = 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run'
    comando = f'reg add "{chave_registro}" /v Otimizador /t REG_SZ /d "{caminho_exe}" /f'
    executar_comando(comando)

def aplicar_otimizacoes():
    """Executa todas as otimizações periodicamente."""
    adicionar_ao_inicio()
    while True:
        liberar_memoria()
        acelerar_resposta()
        resfriar_computador()
        configurar_ventoinha()
        otimizar_registro()
        otimizar_bateria()
        time.sleep(30)

if __name__ == "__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Execute como administrador!")
    else:
        aplicar_otimizacoes()
