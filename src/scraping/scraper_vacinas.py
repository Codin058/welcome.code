import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

# Cache em memória — evita reler o Excel a cada consulta
# Começa como None e é preenchido na primeira chamada de busca_vacinas()
_cache = None


def busca_vacinas():
    global _cache

    # Se já foi carregado antes, retorna direto sem reler o arquivo
    if _cache is not None:
        return _cache

    # Monta o caminho do Excel relativo a este arquivo
    # Assim funciona independente de onde o projeto estiver no computador
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    arquivo = os.path.join(BASE_DIR, 'calendario_vacinacao.xlsx')

    if not os.path.exists(arquivo):
        raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")

    logger.info("Carregando calendario_vacinacao.xlsx...")
    df = pd.read_excel(arquivo, engine='openpyxl')

    # Limpa espaços invisíveis nos nomes das colunas e nos valores da coluna Fases
    # Sem isso, buscas como df['Fases'] == 'Gravidez' podem falhar por espaço extra
    df.columns = df.columns.str.strip()
    df['Fases'] = df['Fases'].astype(str).str.strip()

    # Agrupa as linhas por fase e salva no cache como dicionário
    # Chave: nome da fase | Valor: DataFrame com as vacinas daquela fase
    _cache = {fase: grupo for fase, grupo in df.groupby('Fases')}

    logger.info(f"Cache carregado: {len(_cache)} fases")
    return _cache


def pegar_por_fase(fase):
    # Atalho para buscar as vacinas de uma fase específica
    # Retorna None se a fase não existir no calendário
    return busca_vacinas().get(fase)