import os
import psutil
import ctypes
import time
import subprocess
import sys
from typing import List


def executar_comando(comando: str) -> None:
    """
    Executa um comando no sistema de forma silenciosa.
    
    Args:
        comando (str): O comando a ser executado.
    """
    try:
        subprocess.run(
            comando,
            shell=True,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        pass


def liberar_memoria() -> None:
    """
    Libera memória RAM e otimiza caches do sistema,
    finalizando processos desnecessários e limpando buffers.
    """
    comandos: List[str] = [
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


def acelerar_resposta() -> None:
    """
    Reduz latência e melhora a resposta do sistema
    ajustando configurações avançadas do Windows.
    """
    comandos: List[str] = [
        "powercfg -setactive SCHEME_MIN",
        "fsutil behavior set disablelastaccess 1",
        "bcdedit /set disabledynamictick yes",
        "bcdedit /set useplatformtick yes",
        "bcdedit /set tscsyncpolicy Enhanced"
    ]
    for comando in comandos:
        executar_comando(comando)


def resfriar_computador() -> None:
    """
    Reduz o uso de CPU ajustando a prioridade de processos muito pesados.
    """
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        if proc.info['cpu_percent'] > 40:
            try:
                processo = psutil.Process(proc.info['pid'])
                processo.nice(psutil.IDLE_PRIORITY_CLASS)
            except psutil.NoSuchProcess:
                pass


def configurar_ventoinha() -> None:
    """
    Tenta consultar/ajustar velocidade da ventoinha (quando suportado via WMI).
    """
    executar_comando(
        "wmic /namespace:\\\\root\\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature"
    )


def otimizar_registro() -> None:
    """
    Aplica otimizações avançadas no registro do Windows,
    incluindo cache, mouse e desempenho visual.
    """
    ajustes: List[str] = [
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v LargeSystemCache /t REG_DWORD /d 1 /f',
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\LanmanServer\\Parameters" /v Size /t REG_DWORD /d 3 /f',
        'reg add "HKCU\\Control Panel\\Mouse" /v MouseSpeed /t REG_SZ /d 2 /f',
        'reg add "HKCU\\Control Panel\\Mouse" /v MouseThreshold1 /t REG_SZ /d 0 /f',
        'reg add "HKCU\\Control Panel\\Mouse" /v MouseThreshold2 /t REG_SZ /d 0 /f',
        'reg add "HKCU\\Control Panel\\Desktop" /v MenuShowDelay /t REG_SZ /d 0 /f'
    ]
    for comando in ajustes:
        executar_comando(comando)


def otimizar_bateria() -> None:
    """
    Configura opções avançadas de economia de energia
    para prolongar a duração da bateria em notebooks.
    """
    comandos: List[str] = [
        "powercfg /change monitor-timeout-ac 5",
        "powercfg /change monitor-timeout-dc 3",
        "powercfg /change standby-timeout-ac 15",
        "powercfg /change standby-timeout-dc 10",
        "powercfg /setdcvalueindex SCHEME_BALANCED SUB_PROCESSOR PROCTHROTTLEMAX 50",
        "powercfg /setdcvalueindex SCHEME_BALANCED SUB_VIDEO ADAPTBRIGHT 1",
        "powercfg -setactive SCHEME_BALANCED"
    ]
    for comando in comandos:
        executar_comando(comando)


def adicionar_ao_inicio() -> None:
    """
    Adiciona o executável ao início do Windows via registro,
    garantindo execução automática.
    """
    caminho_exe: str = os.path.abspath(sys.argv[0])
    chave_registro: str = 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run'
    comando: str = f'reg add "{chave_registro}" /v Otimizador /t REG_SZ /d "{caminho_exe}" /f'
    executar_comando(comando)


def aplicar_otimizacoes() -> None:
    """
    Executa todas as otimizações periodicamente a cada 30 segundos.
    """
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
        print("⚠️ Execute este script como administrador!")
    else:
        aplicar_otimizacoes()
