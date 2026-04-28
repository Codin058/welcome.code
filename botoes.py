#Aqui se importa o módulo types, que contem as estruturas de botões
from telebot import types

#Função para exibir o Menu Principal
def menu_principal():
    #Aqui se cria um "teclado" com 2 botões por linha
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    #Faz com que cada botão tenha texto visível e callback_data
    #Callback_data é o que o bot recebe
    btn_vacinas = types.InlineKeyboardButton('💉 Consultar Vacinas', callback_data='botao_vacinas')
    btn_sobre = types.InlineKeyboardButton('ℹ️ Sobre o Bot', callback_data='botao_sobre')
    
    #Faz os botões aparecerem na mesma linha
    markup.add(btn_vacinas,btn_sobre)
    return markup

#Função para exibir o Menu de Vacinas
def menu_vacinas():
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn_gestante = types.InlineKeyboardButton('🤰 Gestante', callback_data='gestante')
    btn_crianca = types.InlineKeyboardButton('👶 Criança (<10 anos)', callback_data='crianca')
    btn_adolescente = types.InlineKeyboardButton('🧒 Adolescente/Jovem (10-24 anos)', callback_data='adolescente')
    btn_adulto = types.InlineKeyboardButton('👨‍🦱 Adulto (25-59 anos)', callback_data='adulto')
    btn_idoso = types.InlineKeyboardButton('👴 Idoso (>60 anos)', callback_data='idoso')
    btn_voltar = types.InlineKeyboardButton('⬅️ Voltar', callback_data='voltar_menu')

    markup.add(btn_gestante, btn_crianca)                  
    markup.add(btn_adolescente)   
    markup.add(btn_adulto, btn_idoso)         
    markup.add(btn_voltar)            
    return markup

#Função para exibir o Menu de Retorno
def menu_retorno():
    markup = types.InlineKeyboardMarkup()
    btn_novaConsulta = types.InlineKeyboardButton("🔍 Nova Consulta", callback_data="botao_vacinas")
    btn_inicio = types.InlineKeyboardButton("🏠 Menu Principal", callback_data="voltar_menu")
    
    markup.add(btn_novaConsulta)
    markup.add(btn_inicio)
    return markup
