#Essa função que recebe o parametro da mensagem do bot para devolver o pdf
def busca_calendario(perfil):

    #Esse dicionário armazena os links dos PDFs
    # Para puxar cada link de acordo com o parametro,, usa-se uma chave e um valor correspondente
    #Exemplo:
    #Gestante ==> chave
    #Link do PDF ==> valor
    links = {
        'gestante': 'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-gestante',
        'crianca': 'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-crianca',
        'adolescente': 'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-adolescentes-jovens',
        'adulto': 'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-adulto',
        'idoso': 'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-idoso'
    }
    
    #O método get() procura procura um parametro correspondente a uma chave
    #Se não achar, retorna None
    return links.get(perfil)