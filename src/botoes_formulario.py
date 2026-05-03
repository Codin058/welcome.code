from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Cada função aqui monta e retorna um teclado inline para ser enviado junto com uma mensagem
# InlineKeyboardMarkup = o teclado | InlineKeyboardButton = cada botão dentro dele
# callback_data é o valor que o main.py recebe quando o usuário clica no botão


def saiba_mais():
    # Botão exibido na tela inicial — abre uma explicação sobre o bot
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("ℹ️ Saiba Mais", callback_data="saiba_mais"))
    return markup


def tipo_pessoa():
    # Pergunta se a consulta é para o próprio usuário ou para outra pessoa
    # .row() coloca os dois botões lado a lado na mesma linha
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("👤 Para mim", callback_data="user"),
        InlineKeyboardButton("👥 Outra pessoa", callback_data="outra_pessoa")
    )
    return markup


def gestante():
    # Pergunta se a pessoa é gestante ou está planejando gestação
    # Só aparece quando a faixa etária identificada é adulto
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🤰 Sim, gestante", callback_data="gestante"),
        InlineKeyboardButton("❌ Não", callback_data="nao_gestante")
    )
    return markup


def bebe():
    # Pergunta se a pessoa para quem é a consulta é um bebê (até 2 anos)
    # Se sim, o fluxo pede a idade em meses em vez de anos
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("👶 Sim, bebê", callback_data="bebe"),
        InlineKeyboardButton("🧒 Não", callback_data="nao_bebe")
    )
    return markup


def mais_informacoes():
    # Botão exibido ao final da consulta — abre o calendário oficial em PDF
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📄 Ver Calendário Oficial", callback_data="mais_info"))
    return markup