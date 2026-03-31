import telebot
from telebot import types

bot = telebot.TeleBot('7880133237:AAHmFbZl4j6NXlRawgidccYdiH-Ia-UYgOA')

# MENU PRINCIPAL
@bot.message_handler(['start'])
def start(msg:telebot.types.Message):
    markup = types.InlineKeyboardMarkup()

    botao_sobre = types.InlineKeyboardButton('Sobre', callback_data='botao_sobre')
    botao_vacinas = types.InlineKeyboardButton('Vacinas', callback_data='botao_vacinas')
    botao_dados = types.InlineKeyboardButton('Dados do usuário', callback_data='botao_dados')

    markup.add(botao_sobre, botao_dados, botao_vacinas)

    bot.send_message(msg.chat.id, 'Bem-vindo(a) ao HealthyBot! Como posso te ajudar hoje?', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'botao_sobre')
def sobre(call):
        bot.send_message(
            call.message.chat.id,
            'HealthyBot é um Bot que lista as futuras vacinas do usuário!'
        )

@bot.callback_query_handler(func=lambda call: call.data == 'botao_dados')
def dados(call):
        def send_welcome_data_collection(message):
            msg = bot.reply_to(message, "Olá! Para começarmos, qual é o seu nome completo?")
            bot.register_next_step_handler(msg, process_name_step_data_collection)

        def process_name_step_data_collection(message):
            nome = message.text
            msg = bot.reply_to(message, f"Prazer, {nome}! Agora, qual a sua idade?")
            bot.register_next_step_handler(msg, process_age_step_data_collection, nome)

        def process_age_step_data_collection(message, nome):
            idade = message.text
            if not idade.isdigit():
                msg = bot.reply_to(message, "Por favor, digite apenas números. Qual sua idade?")
                bot.register_next_step_handler(msg, process_age_step_data_collection, nome)
                return
            bot.reply_to(message, f"Confirmado!\nNome: {nome}\nIdade: {idade}")

        send_welcome_data_collection(call.message)

@bot.callback_query_handler(func=lambda call: call.data == 'botao_vacinas')
def vacinas(call):
        markup = types.InlineKeyboardMarkup()

        botao_crianca = types.InlineKeyboardButton('Criança', callback_data='botao_crianca')
        botao_adolescente = types.InlineKeyboardButton('Adolescente', callback_data='botao_adolescente')
        botao_adulto = types.InlineKeyboardButton('Adulto', callback_data='botao_adulto')
        botao_idoso = types.InlineKeyboardButton('Idoso', callback_data='botao_idoso')
        botao_gestante = types.InlineKeyboardButton('Gestante', callback_data='botao_gestante')
        botao_voltar = types.InlineKeyboardButton('⬅️ Voltar', callback_data='botao_voltar')

        markup.add(botao_crianca, botao_adolescente, botao_adulto, botao_idoso, botao_gestante, botao_voltar)

        bot.edit_message_text(
            'Escolha o seu perfil de vacinação:',
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

# SUBMENU VACINAS
@bot.callback_query_handler(func=lambda call: call.data == 'botao_crianca')
def crianca(call):
        bot.send_message(call.message.chat.id, '''
        TEXTO VACINAS CRIANÇAS TESTE
        TEXTO VACINAS CRIANCAS TESTE
        TEXTO VACINAS CRIANCAS TESTE''')

@bot.callback_query_handler(func=lambda call: call.data == 'botao_adolescente')
def adolescente(call):
        bot.send_message(call.message.chat.id, '''
        TEXTO VACINAS ADOLESCENTES TESTE
        TEXTO VACINAS ADOLESCENTES TESTE
        TEXTO VACINAS ADOLESCENTES TESTE''')

@bot.callback_query_handler(func=lambda call: call.data == 'botao_adulto')
def adulto(call):
        bot.send_message(call.message.chat.id, '''
        TEXTO VACINAS ADULTOS TESTE
        TEXTO VACINAS ADULTOS TESTE
        TEXTO VACINAS ADULTOS TESTE''')

@bot.callback_query_handler(func=lambda call: call.data == 'botao_idoso')
def idoso(call):
        bot.send_message(call.message.chat.id, '''
        TEXTO VACINAS IDOSOS TESTE
        TEXTO VACINAS IDOSOS TESTE
        TEXTO VACINAS IDOSOS TESTE''')

@bot.callback_query_handler(func=lambda call: call.data == 'botao_gestante')
def gestante(call):
        bot.send_message(call.message.chat.id, '''
        TEXTO VACINAS GESTANTES TESTE
        TEXTO VACINAS GESTANTES TESTE
        TEXTO VACINAS GESTANTES TESTE''')

# VOLTAR
@bot.callback_query_handler(func=lambda call: call.data == 'botao_voltar')
def voltar(call):
        markup = types.InlineKeyboardMarkup()

        botao_sobre = types.InlineKeyboardButton('Sobre', callback_data='botao_sobre')
        botao_vacinas = types.InlineKeyboardButton('Vacinas', callback_data='botao_vacinas')
        botao_dados = types.InlineKeyboardButton('Dados do usuário', callback_data='botao_dados')

        markup.add(botao_sobre, botao_dados, botao_vacinas)

        bot.edit_message_text(
            'Bem-vindo(a) ao HealthyBot! Como posso te ajudar hoje?',
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

bot.infinity_polling()
