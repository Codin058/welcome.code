#Bibliotecas necessárias
import os
import telebot
from dotenv import load_dotenv
import scraper
import botoes 

#Aqui é puxada a variável com o valor do Token
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

#Chama a função /start
@bot.message_handler(commands=['start'])
#Função start
def start(msg):
    #Mensagem da função
    bot.send_message(
        msg.chat.id, 
        '✨ 🤖 *Bem-vindo ao HealthyBot!* ✨', 
        parse_mode='Markdown',
        reply_markup=botoes.menu_principal()
    )

#Handler de botões, qualquer botão apertado passa por aqui
@bot.callback_query_handler(func=lambda call: True)
#Aqui, call contém qual botão foi clicado e de onde veio
def resposta_botao(call):
    #Aqui remove o "loading" do botão
    bot.answer_callback_query(call.id)

    #Botão SOBRE O PROJETO
    if call.data == 'botao_sobre':
        #Texto que explica o BOT
        texto_sobre = (
            "🤖 *HealthyBot* \n\n"
            "O seu Assistente Virtual para saúde e prevenção! 💉\n\n"
            "Consulta realizada através do site oficial do *Ministério da Saúde:* https://www.gov.br/saude/pt-br/vacinacao"
            "\n🇧🇷\n\n"
            "✅ *Informação oficial na palma da sua mão!*"
        )
        #Envia uma mensagem no Telegram
        bot.send_message(
            #Manda a mensagem para a mesma conversa onde o botão foi clicado
            call.message.chat.id,
            #Puxa o conteúdo da mensagem
            texto_sobre,
            #Faz interpretar o texto como Markdown
            parse_mode='Markdown',
            #Puxa a função de um botão
            reply_markup=botoes.menu_principal()
        )

    #Para escolher a FAIXA ETÁRIA
    elif call.data == 'botao_vacinas':
        texto_botao_vacina = '📅 *Escolha uma faixa etária:*'
        bot.send_message(
            call.message.chat.id,
            texto_botao_vacina ,
            parse_mode='Markdown',
            reply_markup=botoes.menu_vacinas()
        )

    #Envia o ARQUIVO PDF
    elif call.data in ['gestante', 'crianca', 'adolescente', 'adulto', 'idoso']:
        bot.answer_callback_query(call.id, "Preparando arquivo...")
        
        #Usa o valor do call.data e passa para a função
        arquivo = scraper.busca_calendario(call.data)
        
        if arquivo:
            #Envia o arquivo se encontrado
            bot.send_document(
                call.message.chat.id, 
                arquivo, 
                caption=f"📄 *CALENDÁRIO {call.data.upper()}*\n\nEste é o arquivo oficial (2025/2026) do *HealthyBot*. Toque para abrir.",
                parse_mode='Markdown',
                reply_markup=botoes.menu_retorno()
            )
        else:
            #Mensagem de erro se não encontra
            bot.send_message(call.message.chat.id, "❌ Erro: Arquivo não disponível.")

    #Voltar para o Menu Principal
    elif call.data == 'voltar_menu':
        start(call.message)

#Mensagem de que o BOT está em execução
print("🤖 Healthybot em operação!")
#executa o BOT
bot.infinity_polling()