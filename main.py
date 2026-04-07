import os
import telebot
from dotenv import load_dotenv
import scraper
import botoes 

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(
        msg.chat.id, 
        '✨ 🤖 *Bem-vindo ao HealthyBot!* ✨', 
        parse_mode='Markdown',
        reply_markup=botoes.menu_principal()
    )

@bot.callback_query_handler(func=lambda call: True)
def resposta_botao(call):
    bot.answer_callback_query(call.id)

    # Botão SOBRE o projeto
    if call.data == 'botao_sobre':
        texto_sobre = (
            "🤖 *HealthyBot* \n\n"
            "O seu Assistente Virtual para saúde e prevenção! 💉\n\n"
            "Consulta realizada através do site oficial do *Ministério da Saúde:* https://www.gov.br/saude/pt-br/vacinacao"
            "\n🇧🇷\n\n"
            "✅ *Informação oficial na palma da sua mão!*"
        )
        bot.send_message(
            call.message.chat.id,
            texto_sobre,
            parse_mode='Markdown',
            reply_markup=botoes.menu_principal()
        )

    # Escolhe faixa etária
    elif call.data == 'botao_vacinas':
        texto_botao_vacina = '📅 *Escolha uma faixa etária:*'
        bot.send_message(
            call.message.chat.id,
            texto_botao_vacina ,
            parse_mode='Markdown',
            reply_markup=botoes.menu_vacinas()
        )

    # Envia o arquivo
    elif call.data in ['gestante', 'crianca', 'adolescente', 'adulto', 'idoso']:
        bot.answer_callback_query(call.id, "Preparando arquivo...")
        
        arquivo = scraper.busca_calendario(call.data)
        
        if arquivo:
            bot.send_document(
                call.message.chat.id, 
                arquivo, 
                caption=f"📄 *CALENDÁRIO {call.data.upper()}*\n\nEste é o arquivo oficial (2025/2026) do *HealthyBot*. Toque para abrir.",
                parse_mode='Markdown',
                reply_markup=botoes.menu_retorno()
            )
        else:
            bot.send_message(call.message.chat.id, "❌ Erro: Arquivo não disponível.")

    # Voltar para o Menu Principal
    elif call.data == 'voltar_menu':
        start(call.message)

print("🤖 Healthybot em operação!")
bot.infinity_polling()