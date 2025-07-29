import os
import shutil
import ctypes
import subprocess
import win32api
import win32file

def listar_unidades_removiveis():
    unidades = []
    drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
    
    for drive in drives:
        tipo = win32file.GetDriveType(drive)
        if tipo == win32file.DRIVE_REMOVABLE:  # Somente unidades USB
            unidades.append(drive)
    
    return unidades

def limpar_atalhos_e_malware(drive):
    print(f"Removendo arquivos maliciosos de {drive}...")
    try:
        arquivos = os.listdir(drive)
        for arquivo in arquivos:
            caminho_completo = os.path.join(drive, arquivo)
            
            if arquivo.endswith(".lnk") or arquivo.lower() in ["autorun.inf", "desktop.ini"]:
                os.remove(caminho_completo)
                print(f"Removido: {arquivo}")

        # Restaurar arquivos ocultos
        subprocess.run(["attrib", "-h", "-s", "-r", f"{drive}*.*", "/S", "/D"], shell=True)
        print("Arquivos ocultos restaurados.")
    
    except Exception as e:
        print(f"Erro ao limpar pendrive: {e}")

def formatar_pendrive(drive):
    print(f"Formatando {drive}...")
    try:
        # Força a formatação mesmo que o sistema de arquivos esteja corrompido
        subprocess.run(["diskpart"], input=f"SELECT VOLUME {drive[0]}\nFORMAT FS=FAT32 QUICK\n", text=True, shell=True)
        print("Pendrive formatado com sucesso!")
    except Exception as e:
        print(f"Erro ao formatar: {e}")

def main():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Execute este script como administrador!")
        return

    unidades = listar_unidades_removiveis()
    
    if not unidades:
        print("Nenhum pendrive encontrado.")
        return
    
    for drive in unidades:
        print(f"Processando unidade: {drive}")
        limpar_atalhos_e_malware(drive)
        formatar_pendrive(drive)

if __name__ == "__main__":
    main()
