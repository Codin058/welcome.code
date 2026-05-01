import telebot
import scraping.scraper_pdf as scraper_pdf
from dotenv import load_dotenv

from formulario import (
    iniciar_conversa,
    processar_resposta,
    processar_gestante,
    processar_tipo_pessoa,
    processar_bebe,
    usuarios
)

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

saudacoes = ['oi', 'olá', 'ola', 'eae', 'opa', 'bom dia', 'boa tarde', 'boa noite']


@bot.message_handler(commands=['start'])
def start(msg):
    iniciar_conversa(bot, msg.chat.id)


@bot.message_handler(func=lambda msg: True)
def responder(msg):
    if not msg.text:
        return  # evita erro com mídia

    texto = msg.text.lower().strip()

    if any(s in texto for s in saudacoes):
        iniciar_conversa(bot, msg.chat.id)
        return

    processar_resposta(bot, msg)


@bot.callback_query_handler(func=lambda call: call.data in ["user", "outra_pessoa"])
def tipo_pessoa(call):
    bot.answer_callback_query(call.id)
    processar_tipo_pessoa(bot, call)


@bot.callback_query_handler(func=lambda call: call.data.startswith(("bebe", "nao_bebe")))
def bebe(call):
    bot.answer_callback_query(call.id)
    processar_bebe(bot, call)


@bot.callback_query_handler(func=lambda call: call.data.startswith(("gestante", "nao_gestante")))
def resposta_gestante(call):
    bot.answer_callback_query(call.id)
    processar_gestante(bot, call)


@bot.callback_query_handler(func=lambda call: call.data == "mais_info")
def mais_info(call):
    bot.answer_callback_query(call.id)

    user_id = call.message.chat.id

    if user_id not in usuarios:
        return

    faixa = usuarios[user_id].get('faixa')

    if not faixa:
        bot.send_message(user_id, "❌ Não consegui identificar a faixa")
        return

    arquivo = scraper_pdf.busca_calendario(faixa)

    if arquivo:
        bot.send_document(
            user_id,
            arquivo
        )
    else:
        bot.send_message(user_id, "😳 Esssa faixa etária não possue calendário")

    bot.send_message(
        user_id,
        "Para fazer mais consultas, é só mandar um oi💙"
    )

    usuarios.pop(user_id)


print("🤖 HealthyBot em operação!")
bot.infinity_polling()