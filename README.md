# welcome.code
! pip install pytelegrambotapi

import telebot

API_TOKEN = '7880133237:AAHmFbZl4j6NXlRawgidccYdiH-Ia-UYgOA'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg = bot.reply_to(message, "Olá! Para começarmos, qual é o seu nome completo?")
    # O próximo passo será a função 'process_name_step'
    bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    nome = message.text
    msg = bot.reply_to(message, f"Prazer, {nome}! Agora, qual a sua idade?")
    bot.register_next_step_handler(msg, process_age_step, nome)

def process_age_step(message, nome):
    idade = message.text
    if not idade.isdigit():
        msg = bot.reply_to(message, "Por favor, digite apenas números. Qual sua idade?")
        bot.register_next_step_handler(msg, process_age_step, nome)
        return
    bot.reply_to(message, f"Confirmado!\nNome: {nome}\nIdade: {idade}")

bot.polling()
