import fitz      # PyMuPDF — converte páginas do PDF em imagens
import requests  # Faz o download do PDF direto do site do governo
import io        # Permite trabalhar com os bytes do PDF/imagem sem salvar em disco
import logging

logger = logging.getLogger(__name__)

# Cache em memória — guarda o PDF baixado para não precisar baixar de novo
# Chave: perfil ('gestante', 'crianca', etc.) | Valor: bytes do PDF
_pdf_cache = {}

# Links oficiais do Ministério da Saúde para cada perfil de vacinação
LINKS_PDF = {
    'gestante':    'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-gestante',
    'crianca':     'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-crianca',
    'adolescente': 'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-adolescentes-jovens',
    'adulto':      'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-adulto',
    'idoso':       'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-idoso'
}

# Cabeçalho simulando um navegador Chrome — alguns servidores bloqueiam requisições
# que se identificam como scripts Python, então isso evita possíveis bloqueios
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.124 Safari/537.36'
}


def _baixar_pdf(perfil):
    # Se o PDF desse perfil já foi baixado antes, retorna do cache
    if perfil in _pdf_cache:
        logger.info(f"PDF '{perfil}' do cache")
        return _pdf_cache[perfil]

    url = LINKS_PDF.get(perfil)
    if not url:
        return None

    logger.info(f"Baixando PDF: {url}")
    response = requests.get(url, timeout=30, headers=HEADERS, allow_redirects=True)

    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}")

    conteudo = response.content

    # Verifica se o que veio é realmente um PDF — todo PDF começa com os bytes %PDF
    # Sem essa checagem, o bot tentaria abrir uma página de erro HTML como se fosse PDF
    if len(conteudo) < 4 or conteudo[:4] != b'%PDF':
        raise Exception("Arquivo retornado não é um PDF válido")

    _pdf_cache[perfil] = conteudo
    logger.info(f"PDF '{perfil}' cacheado ({len(conteudo)} bytes)")
    return conteudo


def enviar_paginas_como_foto(bot, chat_id, perfil):
    url = LINKS_PDF.get(perfil)
    if not url:
        bot.send_message(chat_id, "⚠️ Calendário não disponível para este perfil.")
        return

    try:
        pdf_bytes = _baixar_pdf(perfil)

        # Abre o PDF direto da memória, sem precisar salvar nenhum arquivo no disco
        doc = fitz.open(stream=io.BytesIO(pdf_bytes), filetype="pdf")
        total = len(doc)

        if total == 0:
            raise Exception("PDF está vazio")

        for i in range(total):
            try:
                # Matrix(2, 2) dobra a resolução da imagem gerada — sem isso fica pixelado
                pix = doc.load_page(i).get_pixmap(matrix=fitz.Matrix(2, 2))

                # Converte a página para JPEG em memória e envia direto para o Telegram
                img_io = io.BytesIO(pix.tobytes("jpeg"))
                img_io.name = f'calendario_{perfil}_pg{i+1}.jpg'
                bot.send_photo(chat_id, img_io,
                    caption=f"📄 Calendário {perfil.capitalize()} - Página {i+1}/{total}")

            except Exception as e:
                # Se uma página falhar, avisa e continua para a próxima em vez de parar tudo
                logger.error(f"Erro na página {i+1}: {e}")
                bot.send_message(chat_id, f"⚠️ Não foi possível processar a página {i+1}")

        doc.close()

    except requests.exceptions.Timeout:
        # Timeout separado do erro genérico para dar uma mensagem mais útil ao usuário
        bot.send_message(chat_id, "❌ O site do Ministério da Saúde está demorando.\n\nTente novamente em alguns minutos.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro de rede ({perfil}): {e}")
        bot.send_message(chat_id, "❌ Erro ao conectar com o site do Ministério da Saúde.")
    except Exception as e:
        logger.error(f"Erro ao processar PDF ({perfil}): {e}", exc_info=True)
        # No erro final, manda o link direto para o usuário não ficar sem resposta
        bot.send_message(chat_id, f"❌ Erro ao processar o calendário.\n\nAcesse diretamente:\n{url}")