import botoes_formulario
import scraping.scraper_vacinas as vacinas_scraper
import pandas as pd
import threading
import logging

logger = logging.getLogger(__name__)

# Dicionário que guarda os dados de cada usuário durante a conversa
# Chave: user_id do Telegram | Valor: dicionário com etapa, nome, idade, etc.
usuarios = {}

# Lock para evitar conflito quando múltiplos usuários acessam ao mesmo tempo
_usuarios_lock = threading.Lock()


def determinar_faixa_etaria(idade):
    # Classifica a idade em faixas para buscar as vacinas certas
    if idade < 10:
        return 'crianca'
    elif idade < 20:
        return 'adolescente'
    elif idade < 60:
        return 'adulto'
    else:
        return 'idoso'


def fase_por_meses(meses):
    # Mapeia os meses do bebê para as fases do calendário oficial
    MAPA_MESES = {
        0: 'Ao nascer', 2: '2 meses', 3: '3 meses', 4: '4 meses', 5: '5 meses',
        6: '6 meses', 9: '9 meses', 12: '12 meses', 15: '15 meses', 24: '24 meses'
    }
    # Faixa especial: 7 e 8 meses não existem no calendário, mas caem aqui
    if 6 < meses <= 8:
        return '6 a 8 meses'
    return MAPA_MESES.get(meses)


def fase_por_idade(idade):
    # Retorna a fase do calendário com base na idade em anos
    # Cada tupla é (limite_de_idade, nome_da_fase)
    MAPA_IDADES = [
        (4, '4 anos'),
        (14, '9 a 14 anos'),
        (24, '10 a 24 anos'),
        (59, '25 a 59 anos'),
        (float('inf'), 'A partir de 60 anos')
    ]
    for limite, fase in MAPA_IDADES:
        if idade <= limite:
            return fase
    return None


# ====
# Funções de acesso ao dicionário de usuários (thread-safe)
# ====

def atualizar_usuario(user_id, dados):
    # Cria o usuário se não existir, depois atualiza os campos recebidos
    with _usuarios_lock:
        if user_id not in usuarios:
            usuarios[user_id] = {}
        usuarios[user_id].update(dados)

def obter_usuario(user_id):
    # Retorna uma cópia dos dados para não expor o dicionário original
    with _usuarios_lock:
        return usuarios.get(user_id, {}).copy()

def remover_usuario(user_id):
    # Limpa a sessão do usuário ao final da conversa
    with _usuarios_lock:
        usuarios.pop(user_id, None)


# ====
# Início da conversa
# ====

def iniciar_conversa(bot, user_id):
    # Define a etapa inicial e manda a mensagem de boas-vindas com o botão "Saiba Mais"
    atualizar_usuario(user_id, {'etapa': 'nome'})
    texto = (
        '✨ 🤖 *Bem-vindo ao HealthyBot!* ✨\n\n'
        "👋 Oi! Eu sou o *HealthyBot* 😊\n\n"
        "Vou te ajudar a encontrar seu Calendário de Vacinação 💉\n\n"
        "Para começar, qual é o seu nome?\n\n"
    )
    bot.send_message(user_id, texto, parse_mode='Markdown', reply_markup=botoes_formulario.saiba_mais())


# ====
# Processamento das mensagens de texto
# ====

def processar_resposta(bot, msg):
    user_id = msg.chat.id
    texto = msg.text.strip()
    u = obter_usuario(user_id)

    # Se o usuário não tem sessão ativa, pede para começar pelo "Oi"
    if not u:
        bot.send_message(user_id, "👋 Digite 'Oi' para iniciar uma consulta.")
        return

    etapa = u.get('etapa')

    if etapa == 'nome':
        # Salva o nome e avança para a escolha de para quem é a consulta
        atualizar_usuario(user_id, {'nome': texto.title(), 'etapa': 'tipo_pessoa'})
        bot.send_message(
            user_id,
            f"📌 Legal {texto.title()}, para quem é a consulta?",
            reply_markup=botoes_formulario.tipo_pessoa()
        )

    # Nas etapas abaixo o usuário deve usar os botões, não digitar texto
    elif etapa == 'tipo_pessoa':
        bot.send_message(user_id, "👆 Use os botões para responder.",
            reply_markup=botoes_formulario.tipo_pessoa())

    elif etapa == 'bebe_check':
        bot.send_message(user_id, "👆 Use os botões para responder.",
            reply_markup=botoes_formulario.bebe())

    elif etapa == 'gestante':
        bot.send_message(user_id, "👆 Use os botões para responder.",
            reply_markup=botoes_formulario.gestante())

    elif etapa == 'idade':
        if not texto.isdigit():
            bot.send_message(user_id, "❗ Por favor, digite apenas números.")
            return

        idade = int(texto)

        if idade > 150 or idade < 0:
            bot.send_message(user_id, "❗ Digite uma idade válida (0 a 150 anos).")
            return

        # Bebês de 1 ou 2 anos: converte para meses e já busca como bebê
        if idade <= 2:
            meses = 12 if idade == 1 else (24 if idade == 2 else 0)
            atualizar_usuario(user_id, {'meses': meses})
            _enviar_em_thread(bot, user_id, 'bebe')
        else:
            faixa = determinar_faixa_etaria(idade)
            atualizar_usuario(user_id, {'idade': idade})

            # Adultos têm uma pergunta extra sobre gestação
            if faixa == 'adulto':
                atualizar_usuario(user_id, {'etapa': 'gestante'})
                bot.send_message(user_id, "📌 A pessoa está gestante ou planejando gestação?",
                    reply_markup=botoes_formulario.gestante())
            else:
                _enviar_em_thread(bot, user_id, faixa)

    elif etapa == 'idade_meses':
        if not texto.isdigit():
            bot.send_message(user_id, "❗ Por favor, digite apenas números.")
            return

        meses = int(texto)

        if meses < 0 or meses > 24:
            bot.send_message(user_id,
                "❗ Digite uma idade entre 0 e 24 meses.\n"
                "Para crianças acima de 2 anos, digite 'Oi' e reinicie informando a idade em anos.")
            return

        atualizar_usuario(user_id, {'meses': meses})
        _enviar_em_thread(bot, user_id, 'bebe')


# ====
# Processamento dos botões (callbacks)
# ====

def processar_tipo_pessoa(bot, call):
    uid = call.message.chat.id
    if call.data == "user":
        # Consulta para o próprio usuário: pede a idade diretamente
        atualizar_usuario(uid, {'etapa': 'idade'})
        bot.send_message(uid, "Certo! Me diga a sua idade (em anos):")
    else:
        # Consulta para outra pessoa: verifica primeiro se é bebê
        atualizar_usuario(uid, {'etapa': 'bebe_check'})
        bot.send_message(uid, "👶 É um bebê (até 2 anos)?", reply_markup=botoes_formulario.bebe())

def processar_bebe(bot, call):
    uid = call.message.chat.id
    if call.data == "bebe":
        # Bebê confirmado: pede a idade em meses
        atualizar_usuario(uid, {'etapa': 'idade_meses'})
        bot.send_message(uid, "Quantos meses o bebê tem? (0 a 24 meses)")
    else:
        # Não é bebê: pede a idade em anos normalmente
        atualizar_usuario(uid, {'etapa': 'idade'})
        bot.send_message(uid, "Qual a idade da pessoa (em anos)?")

def processar_gestante(bot, call):
    # Define a faixa como gestante ou adulto comum e já busca as vacinas
    faixa = "gestante" if call.data == "gestante" else "adulto"
    _enviar_em_thread(bot, call.message.chat.id, faixa)


# ====
# Busca e envio das vacinas
# ====

def _enviar_em_thread(bot, user_id, faixa):
    # Roda a busca em uma thread separada para não travar o bot
    t = threading.Thread(target=enviar_para_servico, args=(bot, user_id, faixa), daemon=True)
    t.start()

def enviar_para_servico(bot, user_id, faixa):
    try:
        u = obter_usuario(user_id)
        nome = u.get('nome', 'Usuário')

        bot.send_message(user_id, f"Perfeito, {nome}! 👍\n\n⏳ Buscando vacinas recomendadas...")

        # Salva a faixa final (bebe vira crianca para o PDF depois)
        faixa_final = 'crianca' if faixa == 'bebe' else faixa
        atualizar_usuario(user_id, {'faixa': faixa_final})

        # Define quais fases do calendário buscar com base no perfil
        if faixa == "gestante":
            fases = ["Gravidez", "28° semana gestacional"]

        elif faixa == "bebe":
            meses = u.get('meses', 0)
            fase = fase_por_meses(meses)

            # Se não há fase exata, tenta a mais próxima disponível
            if not fase:
                fases_proximas = {
                    1: '2 meses', 7: '6 meses', 8: '9 meses',
                    10: '9 meses', 11: '12 meses', 13: '12 meses',
                    14: '15 meses', 16: '15 meses', 17: '15 meses',
                    18: '15 meses', 19: '15 meses', 20: '15 meses',
                    21: '24 meses', 22: '24 meses', 23: '24 meses'
                }
                fase = fases_proximas.get(meses)
                if fase:
                    bot.send_message(user_id,
                        f"ℹ️ Mostrando vacinas para a fase mais próxima: *{fase}*",
                        parse_mode='Markdown')
            fases = [fase] if fase else []

        else:
            idade = u.get('idade', 0)
            fase = fase_por_idade(idade)
            fases = [fase] if fase else []

        # Se não conseguiu determinar nenhuma fase, oferece o calendário completo
        if not fases or not fases[0]:
            bot.send_message(user_id,
                "⚠️ Não consegui determinar a fase no calendário oficial.\n\n"
                "💡 Acesse o calendário completo:",
                reply_markup=botoes_formulario.mais_informacoes())
            return

        # Carrega os dados do Excel (já em cache após a primeira leitura)
        dados = vacinas_scraper.busca_vacinas()
        if not dados:
            bot.send_message(user_id, "❌ Não foi possível acessar o sistema de vacinas.")
            return

        # Filtra os dados pelas fases encontradas, ignorando diferenças de maiúsculas/espaços
        resultados = []
        for fase_busca in fases:
            if not fase_busca:
                continue
            fase_norm = fase_busca.strip().lower()
            for chave, df in dados.items():
                if chave.strip().lower() == fase_norm and df is not None and not df.empty:
                    resultados.append(df)

        if resultados:
            df_final = pd.concat(resultados)
            linhas = []

            # Monta a mensagem formatada com cada vacina encontrada
            for _, row in df_final.iterrows():
                vacina = str(row.get('Vacina', '')).strip()
                dose = str(row.get('DOSE', '')).strip()
                evita = str(row.get('Evita', '')).strip()
                linhas.append(f"💉 *{vacina}*\n📋 Dose: {dose}\n🛡️ Evita: {evita}")

            texto_vacinas = "\n\n".join(linhas)
            mensagem = f"💉 *Vacinas recomendadas:*\n\n{texto_vacinas}\n\n💡 *Deseja o Calendário Oficial completo?*"
            bot.send_message(user_id, mensagem, parse_mode='Markdown',
                reply_markup=botoes_formulario.mais_informacoes())
        else:
            # Nenhuma vacina encontrada para a fase: oferece o PDF como alternativa
            bot.send_message(user_id,
                "⚠️ Não encontrei vacinas específicas para esta fase.\n\n"
                "📄 Consulte o calendário oficial completo:",
                reply_markup=botoes_formulario.mais_informacoes())

    except Exception as e:
        logger.error(f"Erro em enviar_para_servico (user {user_id}): {e}", exc_info=True)
        bot.send_message(user_id, "😓 Ops! Algo deu errado.\n\nDigite 'Oi' para recomeçar.")