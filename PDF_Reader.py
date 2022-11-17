import PyPDF2 as pyf
from pathlib import Path
import pandas as pd
import numpy as np

#Ler o pdf e extrair apenas a primeira página
reader = pyf.PdfFileReader("Example.pdf")
page = reader.pages[0]
page = page.extractText()

#Substituir o espaçamento e separar a string
page = page.replace('\n', ' ;**; ')
page = page.split(' ;**; ')

#Contar quantas linhas serão necessárias e até onde finalizar a lista
qtd_negociacao = page.count('1-BOVESPA')
final_lista = ((qtd_negociacao+1)*9)-1

#Limpar a lista com os dados necessários
page = page[2:5]+page[6:]
page = page[:final_lista]

#Separar o cabeçalho dos dados
header = page[:9]
table = page[9:]

#Acrescentar a 'coluna' extra em caso de FII
for word in table:
    if 'FII' in word:
        table.insert(((table.index(word))+1),'NM')

#Modificar a lista para criar o DF
table = np.array(table)
reshaped = table.reshape(qtd_negociacao,9)
df = pd.DataFrame(data = reshaped, columns = header)
print(df)
df.to_csv('ExampleControl.csv')