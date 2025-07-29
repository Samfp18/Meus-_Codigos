import psutil
import platform
import os
import time
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF
import shutil

# Função para verificar o uso da CPU
def verificar_cpu():
    uso_cpu = psutil.cpu_percent(interval=5)
    frequencia = psutil.cpu_freq().current
    nucleos = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)
    status = "NORMAL"
    if uso_cpu > 85:
        status = "ALTO"
    if uso_cpu > 95:
        status = "CRÍTICO"
    return uso_cpu, frequencia, nucleos, threads, status

# Função para verificar a memória RAM
def verificar_memoria():
    memoria = psutil.virtual_memory()
    uso_memoria = memoria.percent
    total_memoria = round(memoria.total / (1024 ** 3), 2)
    status = "NORMAL"
    if uso_memoria > 85:
        status = "ALTO"
    if uso_memoria > 95:
        status = "CRÍTICO"
    return uso_memoria, total_memoria, status

# Função para verificar o armazenamento
def verificar_disco():
    disco = psutil.disk_usage('/')
    uso_disco = disco.percent
    total_disco = round(disco.total / (1024 ** 3), 2)
    espaco_livre = round(disco.free / (1024 ** 3), 2)
    status = "NORMAL"
    if uso_disco > 90:
        status = "QUASE CHEIO"
    if uso_disco > 95:
        status = "CRÍTICO"
    return uso_disco, total_disco, espaco_livre, status

# Função para verificar a integridade do sistema operacional
def verificar_integridade_sistema():
    problemas = []
    if os.name == "nt":
        resultado = os.system("sfc /scannow >nul 2>&1")
        if resultado != 0:
            problemas.append("Problemas de integridade detectados no Windows.")
    return problemas

# Função para gerar relatório em PDF
def gerar_relatorio_pdf(dados, recomendacoes, avaliacao_final):
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

    nome_arquivo = "relatorio_diagnostico.pdf"
    pdf.output(nome_arquivo)
    return nome_arquivo

# Função para enviar o relatório por e-mail
def enviar_email(arquivo_pdf):
    remetente = ""
    destinatario = ""
    senha = ""

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

# Função principal
def diagnostico_geral():
    sistema = platform.system()
    versao = platform.version()
    processador = platform.processor()

    cpu, freq, nucleos, threads, status_cpu = verificar_cpu()
    memoria, total_memoria, status_memoria = verificar_memoria()
    disco, total_disco, espaco_livre, status_disco = verificar_disco()
    integridade = verificar_integridade_sistema()

    dados = {
        "Sistema Operacional": f"{sistema} - Versão: {versao}",
        "Processador": processador,
        "Uso da CPU": f"{cpu}% - {freq} MHz - Status: {status_cpu}",
        "Uso da Memória RAM": f"{memoria}% de {total_memoria} GB - Status: {status_memoria}",
        "Uso do Disco": f"{disco}% de {total_disco} GB (Espaço livre: {espaco_livre} GB) - Status: {status_disco}",
        "Integridade do Sistema": "OK" if not integridade else "; ".join(integridade)
    }

    recomendacoes = []
    problemas_graves = sum([status_cpu != "NORMAL", status_memoria != "NORMAL", status_disco != "NORMAL", bool(integridade)])
    
    if problemas_graves >= 3:
        avaliacao_final = "Recomendação: SUBSTITUIÇÃO ou DESCARTE SEGURO. O computador apresenta problemas graves."
    elif problemas_graves > 0:
        avaliacao_final = "Recomendação: Melhorias necessárias. Algumas otimizações podem ser feitas."
    else:
        avaliacao_final = "Recomendação: O computador está em boas condições."

    arquivo_pdf = gerar_relatorio_pdf(dados, recomendacoes, avaliacao_final)
    enviar_email(arquivo_pdf)

if __name__ == "__main__":
    diagnostico_geral()





