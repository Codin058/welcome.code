# 💉 HealthyBot - Guia de Vacinação 

>  **Acesse o Bot no Telegram:** https://t.me/HealthyyyBot

Este projeto foi desenvolvido como um trabalho prático para o curso de **Análise e Desenvolvimento de Sistemas (ADS)** na **Fatec São José dos Campos**. O *HealthyBot* é um assistente virtual que automatiza o acesso aos calendários oficiais de vacinação, utilizando dados integrados do **Ministério da Saúde** e do **Programa Nacional de Vacinação (PNI)**.

# 🎯 Objetivo do Projeto
O bot visa facilitar a consulta de saúde pública, entregando documentos técnicos oficiais (PDFs) diretamente no chat do usuário, categorizados por faixas etárias específicas (Prematuros, Crianças, Adolescentes, Adultos e Idosos). O foco principal é a agilidade no acesso à informação oficial.

# 🛠️ Tecnologias e Bibliotecas
- **Python 3.12+**
- **PyTelegramBotAPI (Telebot)**: Integração com a API do Telegram.
- **Python-dotenv**: Gerenciamento seguro do token.
- **Markdown**: Formatação de textos e mensagens no chat.

# 📁 Estrutura do Software
O projeto possui a seguinte estrtura:
- `main.py`: Gerenciamento da lógica e comandos.
- `botoes.py`: Menu de opções. (`InlineKeyboardMarkup`).
- `scraper.py`: Faz a busca dos arquivos pdf com as informações.
- `.env`: Armazena o Token do bot com segurança.