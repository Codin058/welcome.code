import pandas as pd
import os


def busca_vacinas():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    arquivo = os.path.join(BASE_DIR, 'calendario_vacinacao.xlsx')
    

    df = pd.read_excel(arquivo, engine='openpyxl')
    df = df.rename(columns=lambda x: x.strip())

    # ========================
    # FILTROS (SEU CÓDIGO ORIGINAL)
    # ========================
    flt_gravidez = df[df['Fases'] == 'Gravidez']
    flt_semana28 = df[df['Fases'] == '28° semana gestacional']
    flt_nascer = df[df['Fases'] == 'Ao nascer']
    flt_2meses = df[df['Fases'] == '2 meses']
    flt_3meses = df[df['Fases'] == '3 meses']
    flt_4meses = df[df['Fases'] == '4 meses']
    flt_5meses = df[df['Fases'] == '5 meses']
    flt_6meses = df[df['Fases'] == '6 meses']
    flt_excessao = df[df['Fases'] == '6 a 8 meses']
    flt_7meses = df[df['Fases'] == '7 meses']
    flt_9meses = df[df['Fases'] == '9 meses']
    flt_12meses = df[df['Fases'] == '12 meses']
    flt_15meses = df[df['Fases'] == '15 meses']
    flt_4anos = df[df['Fases'] == '4 anos']
    flt_9_4anos = df[df['Fases'] == '9 a 14 anos']
    flt_10_14anos = df[df['Fases'] == '10 a 14 anos']
    flt_11_14anos = df[df['Fases'] == '11 a 14 anos']
    flt_10_24anos = df[df['Fases'] == '10 a 24 anos']
    flt_25_59anos = df[df['Fases'] == '25 a 59 anos']
    flt_60anos = df[df['Fases'] == 'A partir de 60 anos']

    # ========================
    # NOVO: DICIONÁRIO DE ACESSO
    # ========================
    dados = {
        "Gravidez": flt_gravidez,
        "28° semana gestacional": flt_semana28,
        "Ao nascer": flt_nascer,
        "2 meses": flt_2meses,
        "3 meses": flt_3meses,
        "4 meses": flt_4meses,
        "5 meses": flt_5meses,
        "6 meses": flt_6meses,
        "6 a 8 meses": flt_excessao,
        "7 meses": flt_7meses,
        "9 meses": flt_9meses,
        "12 meses": flt_12meses,
        "15 meses": flt_15meses,
        "4 anos": flt_4anos,
        "9 a 14 anos": flt_9_4anos,
        "10 a 14 anos": flt_10_14anos,
        "11 a 14 anos": flt_11_14anos,
        "10 a 24 anos": flt_10_24anos,
        "25 a 59 anos": flt_25_59anos,
        "A partir de 60 anos": flt_60anos
    }

    return dados


# ========================
# FUNÇÃO EXTRA (FACILITA SUA VIDA)
# ========================
def pegar_por_fase(fase):
    dados = busca_vacinas()
    return dados.get(fase)