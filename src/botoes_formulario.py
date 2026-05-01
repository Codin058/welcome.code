from telebot import types

def tipo_pessoa():
    markup = types.InlineKeyboardMarkup(row_width=2)

    btn_user = types.InlineKeyboardButton('Eu', callback_data='user')
    btn_outra_pessoa = types.InlineKeyboardButton('Outra pessoa', callback_data='outra_pessoa')
    
    markup.add(btn_user,btn_outra_pessoa)
    return markup

def bebe():
    markup = types.InlineKeyboardMarkup(row_width=2)

    btn_bebe = types.InlineKeyboardButton('Sim', callback_data='bebe')
    btn_nao_bebe = types.InlineKeyboardButton('Não', callback_data='nao_bebe')
    
    markup.add(btn_bebe,btn_nao_bebe)
    return markup

def gestante():
    markup = types.InlineKeyboardMarkup(row_width=2)

    btn_gestante = types.InlineKeyboardButton('Sim', callback_data='gestante')
    btn_nao_gestante = types.InlineKeyboardButton('Não', callback_data='nao_gestante')
    
    markup.add(btn_gestante,btn_nao_gestante)
    return markup

def mais_informacoes():
    markup = types.InlineKeyboardMarkup(row_width=1)

    bnt_mais_informacoes = types.InlineKeyboardButton("📄 Acessar calendário de vacinação", callback_data="mais_info")
    
    markup.add(bnt_mais_informacoes)
    return markup