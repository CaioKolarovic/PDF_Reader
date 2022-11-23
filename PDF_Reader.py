import PyPDF2 as pyf
from pathlib import Path
import pandas as pd
import numpy as np
import os

#Criação de tabelas secundárias
complete_table = []
complete_table2 = []
flat_list2 = []
inter_list = []

#Ler todos os pdfs da pasta e criar as variáveis
for file in os.listdir():
        if file.endswith('.pdf'):
            reader = pyf.PdfFileReader(file)
            complete_table = []
            i = 0
            qtd_negociacao = 0
            w = 0 

            #Enquanto existir páginas, ler cada uma, extrair e criar as variáveis de colunas
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
                            date = date[-10:]
                            
                    #Contar quantas linhas serão necessárias e até onde finalizar a lista
                    qtd_negociacao_pagina = page.count('1-BOVESPA')
                    final_lista = ((qtd_negociacao_pagina+1)*9)
                    
                    #Limpar a lista com os dados necessários
                    page = page[2:5]+page[6:]
                    
                    #Acrescentar a 'coluna' extra em casos específicos
                    #Melhorar essa análise
                    for word in page:
                        inter_list.append(word)
                        if 'FII ' in word:
                            inter_list.append('NM')
                        if 'SCHULZ' in word:
                             inter_list.append('NM')
                        if 'TELEF' in word:
                             inter_list.append('NM')

                    #Remover a 'coluna' extra em casos específicos
                    #Melhorar essa análise
                    for word in inter_list:          
                         if 'EJ ' in word:
                             inter_list.remove('EJ ')
                         if 'ER' in word:
                             if word == 'ER':
                                 inter_list.remove('ER')
                         if '#' in word:
                             if word == '#':
                                 inter_list.remove('#')

                    page = inter_list
                    inter_list = []
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

                    #Vai para a próxima página
                    i += 1

                    #Soma de quantas linhas teremos na DF
                    qtd_negociacao = qtd_negociacao + qtd_negociacao_pagina

                #Acabaram as páginas    
                except IndexError:
                    break

                except PermissionError:
                    print('Feche o arquivo')
                    break

            #Transforma a lista de listas em uma lista única
            flat_list = [item for sublist in complete_table for item in sublist]
           
            #Lista com as negociações de todos os pdfs
            complete_table2.append(flat_list)

            #Transforma a lista de listas em uma lista única
            flat_list2 = [item for sublist in complete_table2 for item in sublist]

            #Modificar a lista para criar o DF
            table2 = np.array(flat_list2)
            reshaped2 = table2.reshape(int((len(flat_list2))/10),10)
            df2 = pd.DataFrame(data = reshaped2, columns = header)
            df2.to_excel('Example.xlsx')

print('Relatório Completo salvo em excel')  