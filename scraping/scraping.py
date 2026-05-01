import pandas as pd
from google.colab import drive
drive.mount('/content/drive')

origem = '/content/drive/MyDrive/Colab Notebooks/'

arquivo = origem + "Calendário de vacinação.csv"
df = pd.read_csv(arquivo,low_memory=False, sep=',',encoding='UTF-8')

df = df.rename(columns=lambda x: x.strip())

flt_gravidez = df[df['Fases'] == 'Gravidez']

flt_semana2 = df[df['Fases'] == '28° semana gestacional']

flt_nascer = df[df['Fases'] == 'Ao nascer']

flt_2meses = df[df['Fases'] == '2 meses']

flt_3meses = df[df['Fases'] == '3 meses']

flt_4meses = df[df['Fases'] == '4 meses']

flt_5meses = df[df['Fases'] == '5 meses']

flt_6meses = df[df['Fases'] == '6 meses']

flt_excessao = df[df['Fases'] == '6 a 8 meses']

flt_7meses = df[df['Fases'] == '7 meses']

flt_9meses = df[df['Fases'] == '9 meses']

flt_12meses = df[df['Fases'] == '12 meses']

flt_15meses = df[df['Fases'] == '15 meses']

flt_4anos = df[df['Fases'] == '4 anos']

flt_9_4anos = df[df['Fases'] == '9 a 14 anos']

flt_10_14anos = df[df['Fases'] == '10 a 14 anos']

flt_11_14anos = df[df['Fases'] == '11 a 14 anos']

flt_10_24anos = df[df['Fases'] == '10 a 24 anos']

flt_25_59anos = df[df['Fases'] == '25 a 59 anos']

flt_60anos = df[df['Fases'] == 'A partir de 60 anos']
