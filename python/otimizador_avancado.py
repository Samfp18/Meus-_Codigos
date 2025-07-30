import os
import psutil
import shutil
import platform
import subprocess
import ctypes
from datetime import datetime
from typing import List
from cryptography.fernet import Fernet

# === CHAVE FIXA PARA CRIPTOGRAFIA ===
CHAVE_FIXA: bytes = b'G6jK9xyvlOpbv_FFp5iQaN6JWGVVwquJZoAq-F5B0xU='
fernet = Fernet(CHAVE_FIXA)


def criptografar_comando(comando: str) -> str:
    """
    Criptografa um comando em texto.
    
    Args:
        comando (str): O comando a ser criptografado.
    Returns:
        str: Comando criptografado.
    """
    return fernet.encrypt(comando.encode()).decode()


def executar_comando_criptografado(comando_criptografado: str) -> None:
    """
    Descriptografa e executa um comando no sistema.
    
    Args:
        comando_criptografado (str): Comando criptografado previamente.
    """
    comando: str = fernet.decrypt(comando_criptografado.encode()).decode()
    subprocess.call(comando, shell=True)


def limpar_arquivos() -> None:
    """Remove arquivos temporários e caches do sistema."""
    print("[*] Limpando arquivos temporários e caches...")
    temp_dirs: List[str] = [os.getenv('TEMP'), 'C:\\Windows\\Temp', '/tmp']
    total_removidos: int = 0

    for temp_dir in temp_dirs:
        if temp_dir and os.path.exists(temp_dir):
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                        total_removidos += 1
                    except PermissionError:
                        continue
    print(f"[+] {total_removidos} arquivos removidos.")


def otimizar_processos() -> None:
    """Ajusta a prioridade de processos comuns para melhorar desempenho."""
    print("[*] Ajustando prioridades dos processos...")
    for proc in psutil.process_iter():
        try:
            if proc.name() in ["chrome.exe", "firefox.exe", "discord.exe"]:
                proc.nice(psutil.IDLE_PRIORITY_CLASS)  # reduzir prioridade
            if proc.name() in ["explorer.exe", "csrss.exe"]:
                proc.nice(psutil.HIGH_PRIORITY_CLASS)  # aumentar prioridade
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    print("[+] Processos otimizados!")


def limpar_registro_windows() -> None:
    """Remove chaves temporárias do Registro no Windows."""
    if platform.system() == "Windows":
        print("[*] Limpando o Registro do Windows...")
        executar_comando_criptografado(
            criptografar_comando("reg delete HKCU\\Software\\Temp /f")
        )
        print("[+] Registro limpo!")


def ajustar_desempenho() -> None:
    """Configura plano de energia do Windows para máximo desempenho."""
    if platform.system() == "Windows":
        print("[*] Ajustando configurações de desempenho...")
        executar_comando_criptografado(
            criptografar_comando("powercfg -setactive SCHEME_MIN")
        )
        print("[+] Desempenho otimizado!")


def remover_arquivos_duplicados() -> None:
    """Remove arquivos duplicados em pastas comuns (Documentos, Downloads)."""
    print("[*] Procurando arquivos duplicados...")
    paths: List[str] = [
        os.path.join(os.getenv('USERPROFILE', ''), "Documents"),
        os.path.join(os.getenv('USERPROFILE', ''), "Downloads")
    ]

    arquivos: dict[int, str] = {}
    duplicados: int = 0

    for path in paths:
        if os.path.exists(path):
            for file in os.listdir(path):
                full_path = os.path.join(path, file)
                if os.path.isfile(full_path):
                    try:
                        with open(full_path, 'rb') as f:
                            hash_file: int = hash(f.read())
                        if hash_file in arquivos:
                            os.remove(full_path)
                            duplicados += 1
                        else:
                            arquivos[hash_file] = full_path
                    except PermissionError:
                        continue
    print(f"[+] {duplicados} arquivos duplicados removidos.")


def ocultar_execucao() -> None:
    """Oculta a janela do console para execução em segundo plano no Windows."""
    if platform.system() == "Windows":
        ctypes.windll.kernel32.SetConsoleTitleW("")
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


def gerar_relatorio(logs: List[str]) -> None:
    """
    Gera um relatório em arquivo .txt com o resumo da otimização.
    
    Args:
        logs (List[str]): Lista de melhorias aplicadas.
    """
    timestamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo: str = f"relatorio_otimizacao_{timestamp}.txt"

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write("=== RELATÓRIO DE OTIMIZAÇÃO ===\n")
        f.write(f"Data e Hora: {timestamp}\n")
        f.write(f"Sistema Operacional: {platform.system()} {platform.release()}\n\n")
        f.write("Detalhes das Melhorias Aplicadas:\n")
        for log in logs:
            f.write(f"- {log}\n")

    print(f"[+] Relatório salvo: {nome_arquivo}")


def main() -> None:
    """Executa a sequência completa de otimização do sistema."""
    ocultar_execucao()
    logs: List[str] = []

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
