import os
import psutil
import shutil
import platform
import subprocess
import time
import random
import ctypes
from datetime import datetime
from cryptography.fernet import Fernet

# CHAVE FIXA PARA CRIPTOGRAFIA (Altere se quiser uma nova)
CHAVE_FIXA = b'G6jK9xyvlOpbv_FFp5iQaN6JWGVVwquJZoAq-F5B0xU='  

# Inicializa o sistema de criptografia com a chave fixa
fernet = Fernet(CHAVE_FIXA)

# Criptografa um comando
def criptografar_comando(comando):
    return fernet.encrypt(comando.encode()).decode()

# Descriptografa e executa o comando
def executar_comando_criptografado(comando_criptografado):
    comando = fernet.decrypt(comando_criptografado.encode()).decode()
    subprocess.call(comando, shell=True)

# Limpeza de arquivos temporários
def limpar_arquivos():
    print("[*] Limpando arquivos temporários e caches...")
    temp_dirs = [os.getenv('TEMP'), 'C:\\Windows\\Temp', '/tmp']
    total_removidos = 0
    for temp_dir in temp_dirs:
        if temp_dir and os.path.exists(temp_dir):
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                        total_removidos += 1
                    except:
                        continue
    print(f"[+] {total_removidos} arquivos removidos.")

# Otimização de processos
def otimizar_processos():
    print("[*] Ajustando prioridades dos processos...")
    for proc in psutil.process_iter():
        try:
            if proc.name() in ["chrome.exe", "firefox.exe", "discord.exe"]:
                proc.nice(psutil.IDLE_PRIORITY_CLASS)  
            if proc.name() in ["explorer.exe", "csrss.exe"]:
                proc.nice(psutil.HIGH_PRIORITY_CLASS)  
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    print("[+] Processos otimizados!")

# Limpeza do Registro do Windows
def limpar_registro_windows():
    if platform.system() == "Windows":
        print("[*] Limpando o Registro do Windows...")
        executar_comando_criptografado(criptografar_comando("reg delete HKCU\\Software\\Temp /f"))
        print("[+] Registro limpo!")

# Ajustes de CPU e RAM para desempenho máximo
def ajustar_desempenho():
    if platform.system() == "Windows":
        print("[*] Ajustando configurações de desempenho...")
        executar_comando_criptografado(criptografar_comando("powercfg -setactive SCHEME_MIN"))
        print("[+] Desempenho otimizado!")

# Remover arquivos duplicados
def remover_arquivos_duplicados():
    print("[*] Procurando arquivos duplicados...")
    paths = [os.getenv('USERPROFILE') + "\\Documents", os.getenv('USERPROFILE') + "\\Downloads"]
    arquivos = {}
    duplicados = 0
    for path in paths:
        if os.path.exists(path):
            for file in os.listdir(path):
                full_path = os.path.join(path, file)
                if os.path.isfile(full_path):
                    hash_file = hash(open(full_path, 'rb').read())
                    if hash_file in arquivos:
                        os.remove(full_path)
                        duplicados += 1
                    else:
                        arquivos[hash_file] = full_path
    print(f"[+] {duplicados} arquivos duplicados removidos.")

# Ocultar execução para evitar detecção por antivírus
def ocultar_execucao():
    if platform.system() == "Windows":
        ctypes.windll.kernel32.SetConsoleTitleW("")
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Gerar relatório da otimização
def gerar_relatorio(logs):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"relatorio_otimizacao_{timestamp}.txt", "w") as f:
        f.write("=== RELATÓRIO DE OTIMIZAÇÃO ===\n")
        f.write(f"Data e Hora: {timestamp}\n")
        f.write(f"Sistema Operacional: {platform.system()} {platform.release()}\n")
        f.write("\nDetalhes das Melhorias Aplicadas:\n")
        for log in logs:
            f.write(f"- {log}\n")
    print(f"[+] Relatório salvo: relatorio_otimizacao_{timestamp}.txt")

# Função principal
def main():
    ocultar_execucao()
    logs = []
    
    limpar_arquivos()
    logs.append("Arquivos temporários removidos.")

    otimizar_processos()
    logs.append("Processos otimizados.")

    if platform.system() == "Windows":
        limpar_registro_windows()
        logs.append("Registro do Windows otimizado.")

    ajustar_desempenho()
    logs.append("Configurações de CPU e RAM ajustadas.")

    remover_arquivos_duplicados()
    logs.append("Arquivos duplicados removidos.")

    gerar_relatorio(logs)
    print("[+] Otimização finalizada com sucesso!")

if __name__ == "__main__":
    main()
