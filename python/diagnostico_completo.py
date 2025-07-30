import psutil
import platform
import os
import subprocess
import smtplib
from typing import Tuple, List, Dict
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF


def verificar_cpu() -> Tuple[float, float, int, int, str]:
    """
    Verifica informações sobre uso da CPU.
    Retorna uso em %, frequência atual em MHz, núcleos físicos, threads lógicas e status.
    """
    uso_cpu: float = psutil.cpu_percent(interval=5)
    frequencia: float = psutil.cpu_freq().current
    nucleos: int = psutil.cpu_count(logical=False)
    threads: int = psutil.cpu_count(logical=True)
    status: str = "NORMAL"

    if uso_cpu > 95:
        status = "CRÍTICO"
    elif uso_cpu > 85:
        status = "ALTO"

    return uso_cpu, frequencia, nucleos, threads, status


def verificar_memoria() -> Tuple[float, float, str]:
    """
    Verifica o uso da memória RAM.
    Retorna uso em %, memória total em GB e status.
    """
    memoria = psutil.virtual_memory()
    uso_memoria: float = memoria.percent
    total_memoria: float = round(memoria.total / (1024 ** 3), 2)
    status: str = "NORMAL"

    if uso_memoria > 95:
        status = "CRÍTICO"
    elif uso_memoria > 85:
        status = "ALTO"

    return uso_memoria, total_memoria, status


def verificar_disco() -> Tuple[float, float, float, str]:
    """
    Verifica o uso do disco principal.
    Retorna uso em %, tamanho total em GB, espaço livre em GB e status.
    """
    disco = psutil.disk_usage('/')
    uso_disco: float = disco.percent
    total_disco: float = round(disco.total / (1024 ** 3), 2)
    espaco_livre: float = round(disco.free / (1024 ** 3), 2)
    status: str = "NORMAL"

    if uso_disco > 95:
        status = "CRÍTICO"
    elif uso_disco > 90:
        status = "QUASE CHEIO"

    return uso_disco, total_disco, espaco_livre, status


def verificar_integridade_sistema() -> List[str]:
    """
    Verifica a integridade do sistema operacional.
    No Windows, executa o comando `sfc /scannow`.
    Retorna lista de problemas encontrados (se houver).
    """
    problemas: List[str] = []
    if os.name == "nt":
        resultado: int = os.system("sfc /scannow >nul 2>&1")
        if resultado != 0:
            problemas.append("Problemas de integridade detectados no Windows.")
    return problemas


def gerar_relatorio_pdf(dados: Dict[str, str], recomendacoes: List[str], avaliacao_final: str) -> str:
    """
    Gera relatório em PDF com os dados do diagnóstico.
    Retorna o nome do arquivo PDF gerado.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Relatório de Diagnóstico do Sistema", ln=True, align="C")
    pdf.ln(10)

    for chave, valor in dados.items():
        pdf.cell(0, 10, f"{chave}: {valor}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Recomendações:", ln=True)
    pdf.set_font("Arial", size=12)
    for recomendacao in recomendacoes:
        pdf.multi_cell(0, 8, f"- {recomendacao}")

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Avaliação Final:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, avaliacao_final)

    nome_arquivo: str = "relatorio_diagnostico.pdf"
    pdf.output(nome_arquivo)
    return nome_arquivo


def enviar_email(arquivo_pdf: str) -> None:
    """
    Envia o relatório gerado por e-mail (necessário configurar credenciais).
    """
    remetente: str = ""       # Seu e-mail
    destinatario: str = ""    # E-mail de destino
    senha: str = ""           # Senha do remetente (ou App Password)

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = "Relatório de Diagnóstico do Sistema"

    with open(arquivo_pdf, "rb") as anexo:
        parte = MIMEBase('application', 'octet-stream')
        parte.set_payload(anexo.read())
        encoders.encode_base64(parte)
        parte.add_header('Content-Disposition', f'attachment; filename={arquivo_pdf}')
        msg.attach(parte)

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.sendmail(remetente, destinatario, msg.as_string())
        servidor.quit()
        print(f"E-mail enviado com sucesso para {destinatario}!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


def diagnostico_geral() -> None:
    """
    Executa o diagnóstico geral do sistema e gera relatório.
    """
    sistema: str = platform.system()
    versao: str = platform.version()
    processador: str = platform.processor()

    cpu, freq, nucleos, threads, status_cpu = verificar_cpu()
    memoria, total_memoria, status_memoria = verificar_memoria()
    disco, total_disco, espaco_livre, status_disco = verificar_disco()
    integridade: List[str] = verificar_integridade_sistema()

    dados: Dict[str, str] = {
        "Sistema Operacional": f"{sistema} - Versão: {versao}",
        "Processador": processador,
        "Uso da CPU": f"{cpu}% - {freq} MHz - {nucleos} núcleos / {threads} threads - Status: {status_cpu}",
        "Uso da Memória RAM": f"{memoria}% de {total_memoria} GB - Status: {status_memoria}",
        "Uso do Disco": f"{disco}% de {total_disco} GB (Espaço livre: {espaco_livre} GB) - Status: {status_disco}",
        "Integridade do Sistema": "OK" if not integridade else "; ".join(integridade)
    }

    recomendacoes: List[str] = []
    problemas_graves: int = sum([
        status_cpu != "NORMAL",
        status_memoria != "NORMAL",
        status_disco != "NORMAL",
        bool(integridade)
    ])

    if problemas_graves >= 3:
        avaliacao_final: str = "Recomendação: SUBSTITUIÇÃO ou DESCARTE SEGURO. O computador apresenta problemas graves."
    elif problemas_graves > 0:
        avaliacao_final = "Recomendação: Melhorias necessárias. Algumas otimizações podem ser feitas."
    else:
        avaliacao_final = "Recomendação: O computador está em boas condições."

    arquivo_pdf: str = gerar_relatorio_pdf(dados, recomendacoes, avaliacao_final)
    enviar_email(arquivo_pdf)


if __name__ == "__main__":
    diagnostico_geral()
