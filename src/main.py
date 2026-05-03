import os
import sys
import time
import threading
import logging

import telebot
from dotenv import load_dotenv

# Importa as funções do formulário — cada uma cuida de uma etapa da conversa
from formulario import (
    iniciar_conversa,
    processar_resposta,
    processar_gestante,
    processar_tipo_pessoa,
    processar_bebe,
    obter_usuario,
    remover_usuario
)

# Módulos da pasta scraping: um cuida do PDF, outro da planilha de vacinas
import scraping.scraper_pdf as scraper_pdf
import scraping.scraper_vacinas as scraper_vacinas


# Configura o log para aparecer no terminal e também salvar no arquivo bot.log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def carregar_token():
    # Lê o token do arquivo .env e valida antes de tentar conectar
    load_dotenv()
    token = os.getenv('TELEGRAM_TOKEN')

    if not token or not token.strip():
        logger.error("TELEGRAM_TOKEN não encontrado no arquivo .env")
        print("\n❌ TELEGRAM_TOKEN não encontrado no .env")
        print("Crie ou corrija o arquivo .env na raiz do projeto com:")
        print("TELEGRAM_TOKEN=seu_token_aqui\n")
        raise SystemExit(1)  # Encerra o programa de forma limpa, sem traceback

    return token.strip()


TOKEN = carregar_token()

# threaded=True permite atender vários usuários ao mesmo tempo
# num_threads=4 define quantas conversas paralelas o bot suporta
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=4)
bot.remove_webhook()  # Evita conflito caso o bot tenha sido usado com webhook antes

# Palavras que iniciam uma nova conversa — qualquer uma delas reinicia o fluxo
saudacoes = ['oi', 'olá', 'ola', 'eae', 'opa', 'bom dia', 'boa tarde', 'boa noite']


def responder_callback_seguro(call):
    # Confirma para o Telegram que o botão foi recebido
    # O try/except evita crash caso o callback já tenha expirado (limite de 10s do Telegram)
    try:
        bot.answer_callback_query(call.id)
    except Exception:
        pass


# ====
# Comandos de texto
# ====

@bot.message_handler(commands=['start'])
def start(msg):
    # Ponto de entrada padrão do Telegram ao iniciar o bot pela primeira vez
    iniciar_conversa(bot, msg.chat.id)


@bot.message_handler(commands=['reiniciar'])
def reiniciar(msg):
    # Limpa a sessão atual e começa do zero — útil se o usuário travar no fluxo
    remover_usuario(msg.chat.id)
    iniciar_conversa(bot, msg.chat.id)


@bot.message_handler(func=lambda msg: True)
def responder(msg):
    # Captura todas as mensagens de texto que não são comandos
    if not msg.text:
        return

    texto = msg.text.lower().strip()

    # Se for uma saudação, reinicia a conversa independente da etapa atual
    if any(s in texto for s in saudacoes):
        iniciar_conversa(bot, msg.chat.id)
        return

    # Caso contrário, passa para o formulário tratar conforme a etapa do usuário
    processar_resposta(bot, msg)


# ====
# Handlers de botões (callbacks)
# ====

@bot.callback_query_handler(func=lambda call: call.data == "saiba_mais")
def saiba_mais_callback(call):
    responder_callback_seguro(call)

    # Texto informativo sobre o bot — exibido quando o usuário clica em "Saiba Mais"
    info_texto = (
        "🤖 *Sobre o HealthyBot*\n\n"
        "Consulta realizada através do site oficial do *Ministério da Saúde*:\n"
        "https://www.gov.br/saude/pt-br/vacinacao\n\n"
        "✅ *Informação oficial na palma da sua mão!*\n"
        "• Consulta por faixa etária\n"
        "• Orientações para gestantes\n"
        "• Exibição de calendários oficiais\n\n"
        "Pode digitar seu nome para continuarmos! 👇"
    )

    try:
        bot.send_message(
            call.message.chat.id,
            info_texto,
            parse_mode='Markdown',
            disable_web_page_preview=True  # Evita que o link gere um preview grande na mensagem
        )
    except Exception:
        # Se o Markdown falhar por algum caractere especial, envia sem formatação
        bot.send_message(call.message.chat.id, info_texto)


@bot.callback_query_handler(func=lambda call: call.data in ["user", "outra_pessoa"])
def tipo_pessoa_callback(call):
    responder_callback_seguro(call)
    processar_tipo_pessoa(bot, call)


@bot.callback_query_handler(func=lambda call: call.data.startswith(("bebe", "nao_bebe")))
def bebe_callback(call):
    responder_callback_seguro(call)
    processar_bebe(bot, call)


@bot.callback_query_handler(func=lambda call: call.data.startswith(("gestante", "nao_gestante")))
def gestante_callback(call):
    responder_callback_seguro(call)
    processar_gestante(bot, call)


@bot.callback_query_handler(func=lambda call: call.data == "mais_info")
def mais_info_callback(call):
    responder_callback_seguro(call)

    user_id = call.message.chat.id
    u = obter_usuario(user_id)

    if not u:
        bot.send_message(user_id, "⚠️ Sua sessão expirou.\n\nDigite 'Oi' para iniciar.")
        return

    faixa = u.get('faixa')

    if not faixa:
        bot.send_message(user_id, "⚠️ Não identifiquei sua faixa etária.\n\nDigite 'Oi' para reiniciar.")
        return

    msg_espera = bot.send_message(
        user_id,
        "⏳ Gerando as imagens do calendário oficial...\nAguarde, isso pode levar até 30 segundos."
    )

    def _processar():
        # Roda em thread separada para não travar o bot enquanto baixa e processa o PDF
        try:
            scraper_pdf.enviar_paginas_como_foto(bot, user_id, faixa)

            # Remove a mensagem de "aguarde" após o envio das imagens
            try:
                bot.delete_message(user_id, msg_espera.message_id)
            except Exception:
                pass

            bot.send_message(
                user_id,
                "✅ Espero ter ajudado! 😊\n\nSe precisar, envie um 'Oi' 💙"
            )

            # Limpa a sessão do usuário ao finalizar o fluxo completo
            remover_usuario(user_id)

        except Exception as e:
            logger.error(f"Erro ao enviar PDF para {user_id}: {e}", exc_info=True)

            try:
                bot.delete_message(user_id, msg_espera.message_id)
            except Exception:
                pass

            bot.send_message(
                user_id,
                "❌ Problema ao gerar o calendário.\n\nDigite 'Oi' para recomeçar."
            )

    threading.Thread(target=_processar, daemon=True).start()


# ====
# Inicialização
# ====

if __name__ == "__main__":
    # Pré-carrega o Excel na memória antes de receber qualquer mensagem
    # Assim o primeiro usuário não espera o tempo de leitura da planilha
    try:
        scraper_vacinas.busca_vacinas()
        logger.info("Cache carregado com sucesso!")
    except Exception as e:
        logger.warning(f"Não foi possível pré-carregar o cache: {e}")

    print("Bot Online!")

    while True:
        try:
            bot.polling(none_stop=True, skip_pending=True, interval=0, timeout=60)
        except KeyboardInterrupt:
            # Ctrl+C encerra o bot de forma limpa
            logger.info("Bot encerrado pelo usuário.")
            break
        except telebot.apihelper.ApiTelegramException as e:
            if getattr(e, "error_code", None) == 409:
                # Erro 409 acontece quando duas instâncias do bot rodam ao mesmo tempo
                logger.warning("Erro 409: conflito de instância. Reconectando em 15s...")
                bot.stop_polling()
                time.sleep(15)
            else:
                logger.error(f"Erro Telegram: {e}")
                time.sleep(5)
        except Exception as e:
            # Qualquer outro erro inesperado: loga e tenta reconectar
            logger.error(f"Erro inesperado: {e}", exc_info=True)
            time.sleep(5)