import os
import subprocess
import ctypes
import win32api
import win32file
from typing import List


def listar_unidades_removiveis() -> List[str]:
    """
    Lista todas as unidades removíveis conectadas ao computador (pendrives).
    
    Returns:
        List[str]: Lista com as letras das unidades removíveis detectadas.
    """
    unidades: List[str] = []
    drives: List[str] = win32api.GetLogicalDriveStrings().split('\x00')[:-1]

    for drive in drives:
        tipo: int = win32file.GetDriveType(drive)
        if tipo == win32file.DRIVE_REMOVABLE:
            unidades.append(drive)

    return unidades


def limpar_atalhos_e_malware(drive: str) -> None:
    """
    Remove arquivos maliciosos comuns (atalhos, autorun.inf, desktop.ini) de um pendrive
    e restaura arquivos ocultos.

    Args:
        drive (str): Letra da unidade do pendrive (ex: 'E:\\').
    """
    print(f"Removendo arquivos maliciosos de {drive}...")
    try:
        arquivos: List[str] = os.listdir(drive)
        for arquivo in arquivos:
            caminho_completo: str = os.path.join(drive, arquivo)

            if arquivo.endswith(".lnk") or arquivo.lower() in ["autorun.inf", "desktop.ini"]:
                os.remove(caminho_completo)
                print(f"Removido: {arquivo}")

        # Restaurar arquivos ocultos
        subprocess.run(
            ["attrib", "-h", "-s", "-r", f"{drive}*.*", "/S", "/D"],
            shell=True,
            check=False
        )
        print("Arquivos ocultos restaurados.")

    except Exception as e:
        print(f"Erro ao limpar pendrive {drive}: {e}")


def formatar_pendrive(drive: str) -> None:
    """
    Formata o pendrive em FAT32 de forma rápida.
    
    Args:
        drive (str): Letra da unidade do pendrive (ex: 'E:\\').
    """
    print(f"Formatando {drive}...")
    try:
        comando_diskpart: str = f"SELECT VOLUME {drive[0]}\nFORMAT FS=FAT32 QUICK\n"
        subprocess.run(
            ["diskpart"],
            input=comando_diskpart,
            text=True,
            shell=True,
            check=False
        )
        print("Pendrive formatado com sucesso!")
    except Exception as e:
        print(f"Erro ao formatar {drive}: {e}")


def main() -> None:
    """Função principal: verifica privilégios, detecta pendrives e os limpa/formata."""
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("⚠️ Execute este script como administrador!")
        return

    unidades: List[str] = listar_unidades_removiveis()

    if not unidades:
        print("Nenhum pendrive encontrado.")
        return

    for drive in unidades:
        print(f"Processando unidade: {drive}")
        limpar_atalhos_e_malware(drive)
        formatar_pendrive(drive)


if __name__ == "__main__":
    main()
