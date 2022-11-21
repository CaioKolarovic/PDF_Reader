import PyPDF2 as pyf
from pathlib import Path
import pandas as pd
import numpy as np

#Ler o pdf e criar as variáveis
reader = pyf.PdfFileReader("Example.pdf")
complete_table = []
i = 0
qtd_negociacao = 0

#Enquanto existir páginas
while True:
    try:
        page = reader.pages[i]
        page = page.extractText()
        x = 0
        s = 9
        #Substituir o espaçamento e separar a string
        page = page.replace('\n', ' ;**; ')
        page = page.split(' ;**; ')
        for word in page:
            if 'Data pregão' in word:
                index = page.index(word) + 1
                date = page[index]
                
        
        #Contar quantas linhas serão necessárias e até onde finalizar a lista
        qtd_negociacao_pagina = page.count('1-BOVESPA')
        final_lista = ((qtd_negociacao_pagina+1)*9)
        
        #Limpar a lista com os dados necessários
        page = page[2:5]+page[6:]

        #Acrescentar a 'coluna' extra em casos específicos
        for word in page:
            if 'FII' in word:
                page.insert(((page.index(word))+1),'NM')
            if 'EJ ' in word:
                page.remove('EJ ')

        page = page[:final_lista]
        
        #Separar o cabeçalho dos dados
        header = page[:9]
        header.insert(10, 'Data')
        table = page[9:]

        #Acrescentar a data               
        while x <= qtd_negociacao_pagina:
            table.insert(s, date)
            s += 10
            x += 1

        #Não sei por que acrescentando uma data extra
        table.pop()
                
        #Lista com as negociações de todas as páginas
        complete_table.append(table)
        i += 1

        #Soma de quantas linhas teremos na DF
        qtd_negociacao = qtd_negociacao + qtd_negociacao_pagina

    #Acabaram as páginas    
    except IndexError:
        break

    

#Transforma a lista de listas em uma lista única
flat_list = [item for sublist in complete_table for item in sublist]

#Modificar a lista para criar o DF
table = np.array(flat_list)
reshaped = table.reshape(qtd_negociacao,10)
df = pd.DataFrame(data = reshaped, columns = header)
print(df)
df.to_csv('ExampleControl.csv')