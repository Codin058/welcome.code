import telebot
from telebot import types

bot = telebot.TeleBot('8606077486:AAEkCmMdl5UlX6koTC4s-YR0sR4F48YIJkY')

@bot.message_handler(['start'])
def start(msg:telebot.types.Message):
    markup = types.InlineKeyboardMarkup()

    botao_sobre = types.InlineKeyboardButton('Sobre', callback_data='botao_sobre')
    botao_vacinas = types.InlineKeyboardButton('Vacinas', callback_data='botao_vacinas')

    markup.add(botao_sobre, botao_vacinas)

    bot.send_message(msg.chat.id, 'Bem-vindo!', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def resposta_botao(call: types.CallbackQuery):

    # MENU PRINCIPAL
    if call.data == 'botao_sobre':
        bot.send_message(
            call.message.chat.id,
            'TesteFatec é um Bot que lista as futuras vacinas do usuário'
        )

    elif call.data == 'botao_vacinas':
        markup = types.InlineKeyboardMarkup()

        botao_criancas = types.InlineKeyboardButton('Crianças', callback_data='vacina_criancas')
        botao_adultos = types.InlineKeyboardButton('Adultos', callback_data='vacina_adultos')
        botao_idosos = types.InlineKeyboardButton('Idosos', callback_data='vacina_idosos')
        botao_voltar = types.InlineKeyboardButton('⬅️ Voltar', callback_data='voltar_menu')

        markup.add(botao_criancas, botao_adultos, botao_idosos, botao_voltar)

        bot.edit_message_text(
            'Escolha uma faixa etária:',
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    # SUBMENU VACINAS
    elif call.data == 'vacina_criancas':
        bot.send_message(call.message.chat.id, '''
        👶 Ao nascer:
        Vacina Neonat B (01/01 a 15/01)
        Vacina BCG-Plus (01/01 a 15/01)

        🍼 2 meses:
        Vacina Pentavalente-X (10/02 a 25/02)
        Vacina PolioSafe (VIP-X) (10/02 a 25/02)
        Vacina Pneumo-13X (10/02 a 25/02)

        👶 4 meses:
        2ª dose Pentavalente-X (10/04 a 25/04)
        2ª dose PolioSafe (VIP-X) (10/04 a 25/04)
        2ª dose Pneumo-13X (10/04 a 25/04)

        🧑‍⚕️ 9–10 anos:
        Vacina HPV-Next (01/08 a 15/08)
        Vacina Meningo B-X (01/09 a 15/09)''')

    elif call.data == 'vacina_adultos':
        bot.send_message(call.message.chat.id, '''
        18–29 anos:
        dT-Plus (01/03 a 15/03)
        HPV-Next (10/04 a 25/04)
        HepatoSafe (05/06 a 20/06)

        30–49 anos:
        dT-Plus – reforço (01/03 a 15/03)
        Influenza Nova (01/04 a 30/04)
        Cardiovax (10/07 a 25/07)

        50–59 anos:
        Pneumo-AdultX (05/05 a 20/05)
        Herpezor (10/08 a 25/08)
        Influenza Nova (01/04 a 30/04)

        60+ anos:
        NeuroShield (10/03 a 25/03)
        Pneumo-AdultX – reforço (15/05 a 30/05)
        Influenza Nova (01/04 a 30/04)
        Imunoboost Senior (05/09 a 20/09)''')

    elif call.data == 'vacina_idosos':
        bot.send_message(call.message.chat.id, '''
        60–69 anos:
        NeuroShield (10/03 a 25/03)
        Pneumo-AdultX (05/05 a 20/05)
        Influenza Nova (01/04 a 30/04)
        CardioProtect (10/08 a 25/08)

        70–79 anos:
        NeuroShield – reforço (15/03 a 30/03)
        Pneumo-AdultX – reforço (10/05 a 25/05)
        Influenza Nova (01/04 a 30/04)
        Imunoboost Senior (05/09 a 20/09)

        80+ anos:
        NeuroShield – reforço (20/03 a 05/04)
        Pneumo-AdultX – reforço (15/05 a 30/05)
        Influenza Nova (01/04 a 30/04)
        Imunoboost Senior (10/09 a 25/09)
        VitalAge Plus (01/11 a 15/11)''')

    # VOLTAR
    elif call.data == 'voltar_menu':
        markup = types.InlineKeyboardMarkup()

        botao_sobre = types.InlineKeyboardButton('Sobre', callback_data='botao_sobre')
        botao_vacinas = types.InlineKeyboardButton('Vacinas', callback_data='botao_vacinas')

        markup.add(botao_sobre, botao_vacinas)

        bot.edit_message_text(
            'Bem-vindo!',
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )


bot.infinity_polling()