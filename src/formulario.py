import botoes_formulario
import scraping.scraper_vacinas as vacinas_scraper
import pandas as pd

usuarios = {}


# ========================
# CONVERSÃO DE FASE
# ========================
def fase_por_meses(meses):
    if meses == 0:
        return 'Ao nascer'
    elif meses == 2:
        return '2 meses'
    elif meses == 3:
        return '3 meses'
    elif meses == 4:
        return '4 meses'
    elif meses == 5:
        return '5 meses'
    elif meses == 6:
        return '6 meses'
    elif 6 < meses <= 8:
        return '6 a 8 meses'
    elif meses == 9:
        return '9 meses'
    elif meses == 12:
        return '12 meses'
    elif meses == 15:
        return '15 meses'
    else:
        return None


def fase_por_idade(idade):
    if idade == 4:
        return '4 anos'
    elif 9 <= idade <= 14:
        return '9 a 14 anos'
    elif 10 <= idade <= 24:
        return '10 a 24 anos'
    elif 25 <= idade <= 59:
        return '25 a 59 anos'
    elif idade >= 60:
        return 'A partir de 60 anos'
    else:
        return None


def faixa_mais_informacoes(idade):
    if idade < 10:
        return 'crianca'
    elif idade < 18:
        return 'adolescente'
    elif idade <= 59:
        return 'adulto_intermediario'
    else:
        return 'idoso'


# ========================
# UTIL
# ========================
def gerar_texto(df):
    if df is None or df.empty:
        return "❌ Nenhuma informação encontrada."
    return df.to_string(index=False)


# ========================
# INÍCIO
# ========================
def iniciar_conversa(bot, user_id):
    usuarios[user_id] = {'etapa': 'nome'}

    bot.send_message(
        user_id,
        '✨ 🤖 *Bem-vindo ao HealthyBot!* ✨\n\n'
        "👋 Oi! Eu sou o *HealthyBot* 😊\n\n"
        "Vou te ajudar a encontrar seu calendário de vacinação 💉\n\n"
        "Pra começar, qual é o seu nome?",
        parse_mode='Markdown'
    )


# ========================
# RESPOSTAS TEXTO
# ========================
def processar_resposta(bot, msg):
    user_id = msg.chat.id
    texto = msg.text.strip()

    if user_id not in usuarios:
        return

    etapa = usuarios[user_id]['etapa']

    # NOME
    if etapa == 'nome':
        if not texto:
            bot.send_message(user_id, "❗ Me diga seu nome 😊")
            return

        usuarios[user_id]['nome'] = texto
        usuarios[user_id]['etapa'] = 'tipo_pessoa'

        bot.send_message(
            user_id,
            "📌 Para quem você está consultando a vacina?",
            reply_markup=botoes_formulario.tipo_pessoa()
        )
        return

    # IDADE NORMAL
    elif etapa == 'idade':
        if not texto.isdigit():
            bot.send_message(user_id, "❗ Idade precisa ser um número")
            return

        idade = int(texto)

        if idade <= 0 or idade > 120:
            bot.send_message(user_id, "❗ Idade inválida")
            return

        usuarios[user_id]['idade'] = idade
        faixa = faixa_mais_informacoes(idade)

        if faixa == 'adulto_intermediario':
            usuarios[user_id]['etapa'] = 'gestante'

            bot.send_message(
                user_id,
                "📌 Você é gestante?",
                reply_markup=botoes_formulario.gestante()
            )
            return

        enviar_para_servico(bot, user_id, faixa)
        return

    # IDADE EM MESES
    elif etapa == 'idade_meses':
        if not texto.isdigit():
            bot.send_message(user_id, "❗ Digite um número válido")
            return

        meses = int(texto)

        if meses < 0 or meses > 60:
            bot.send_message(user_id, "❗ Valor inválido")
            return

        usuarios[user_id]['meses'] = meses
        enviar_para_servico(bot, user_id, 'bebe')
        return


# ========================
# CALLBACKS
# ========================
def processar_tipo_pessoa(bot, call):
    user_id = call.message.chat.id

    if call.data == "user":
        usuarios[user_id]['etapa'] = 'idade'
        bot.send_message(user_id, "Me diga a idade:")

    elif call.data == "outra_pessoa":
        usuarios[user_id]['etapa'] = 'bebe_check'
        bot.send_message(
            user_id,
            "👶 É um bebê?",
            reply_markup=botoes_formulario.bebe()
        )


def processar_bebe(bot, call):
    user_id = call.message.chat.id

    if call.data == "bebe":
        usuarios[user_id]['etapa'] = 'idade_meses'
        bot.send_message(user_id, "Quantos meses?")
    else:
        usuarios[user_id]['etapa'] = 'idade'
        bot.send_message(user_id, "Me diga a idade:")


def processar_gestante(bot, call):
    user_id = call.message.chat.id

    if call.data == "gestante":
        faixa = "gestante"
    else:
        faixa = "adulto"

    enviar_para_servico(bot, user_id, faixa)


# ========================
# ENVIO
# ========================
def enviar_para_servico(bot, user_id, faixa):
    nome = usuarios[user_id]['nome']

    bot.send_message(
        user_id,
        f"Perfeito, {nome}! 👍\n\nBuscando informações..."
    )

    usuarios[user_id]['faixa'] = faixa

    # definir fases
    if faixa == "gestante":
        fases = ["Gravidez", "28° semana gestacional"]

    elif faixa == "bebe":
        meses = usuarios[user_id].get('meses')
        fase = fase_por_meses(meses)
        fases = [fase] if fase else []

    else:
        idade = usuarios[user_id].get('idade')
        fase = fase_por_idade(idade)
        fases = [fase] if fase else []

    dados = vacinas_scraper.busca_vacinas()

    # DEBUG (se precisar)
    # print("FASES:", fases)
    # print("CHAVES:", list(dados.keys()))

    resultados = []

    for f in fases:
        if not f:
            continue

        f_limpo = f.strip().lower()

        for chave, df in dados.items():
            if chave.strip().lower() == f_limpo:
                if df is not None and not df.empty:
                    resultados.append(df)

    if resultados:
        resultado_final = pd.concat(resultados)
        texto = gerar_texto(resultado_final) + "\nSe precisar de mais informações, clique no botão do calendário⬇️"

        bot.send_message(
            user_id,
            texto,
            reply_markup=botoes_formulario.mais_informacoes()
        )
        bot.send_message(
            user_id,
            "Para fazer mais consultas, é só mandar um oi💙",
        )

    else:
        bot.send_message(
            user_id,
            "Não há nenhuma vacina para essa faixa etária"
        )