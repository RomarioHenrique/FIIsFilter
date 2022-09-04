import pandas as pd
import requests

#Web Scraping que coleta a tabela de Fundos Imobiliários do site Funds Explorer e armaneza em um DF.
header = {'User-Agent': 'Your User-Agent'}

url = 'https://www.fundsexplorer.com.br/ranking'
request = requests.get(url, headers=header)

df = pd.read_html(request.text)

df = pd.DataFrame(df[0])


#Tratamento dos Dados Categóricos.
categorical_columns = ['Códigodo fundo', 'Setor']

idx = df[df['Setor'].isna()].index
df.drop(idx, inplace=True)

df[categorical_columns] = df[categorical_columns].astype('category')


#Tratamento dos Dados Númericos
col_floats = list(df.iloc[:,2:-1].columns)

df[col_floats] = df[col_floats].fillna(value=0)

df[col_floats] = df[col_floats].applymap(lambda x: str(x).replace('R$', '').replace\
    ('.0','').replace('.','').replace('%','').replace(',','.'))

df[col_floats] = df[col_floats].astype('float')

df['P/VPA'] = df['P/VPA']/100


#Verificação do Tipo de Input.
def FloatType(value):
    while True:
        try:
            num = float(input(value))
        except (ValueError, TypeError):
            print('\033[1;31mERRO! Por favor digite um número real válido.\033[m')
            continue
        except KeyboardInterrupt:
            print('\n\033[1;31mUsuário preferiu não digitar este número.')
            return 0
        else:
            return num



print('\nCASO QUEIRA PULAR ALGUM FILTRO, INSIRA 0\n') 
#Transformando o valor informado em seu respectivo setor.
def checkSetor(setor):
    if setor == '1':
        return 'Shoppings'
    elif setor == '2':
        return 'Títulos e Val. Mob.'
    elif setor == '3':
        return 'Lajes Corporativas'
    elif setor == '4':
        return  'Logística'
    elif setor == '5':
        return 'Híbrido'
    elif setor == '6':
        return  'Outros'
    else:
        return  ''

#Recebendo os Parâmetros do Filtro
setor = checkSetor(input('Digite o código do Setor desejado: \n\n 0 = Todos \n 1 = Shoppings \n 2 = Títulos e Val. Mob. \n\
 3 = Lajes Corporativas \n 4 = Logística \n 5 = Híbrido \n 6 = Outros \n\nCódigo:  '))
precoCota = FloatType('\nPreço da Cota MENOR que: ')
pvpa = FloatType('\nP/VPA MENOR que: ')
dvdY = FloatType('\nDividend Yield MAIOR que: ')
lqdD = FloatType('\nLiquidez Diária MAIOR que: ')
qntdA = FloatType('\nQuantidade de Ativos MAIOR que: ')


#Informações que serão retornadas
indicadores = ['Códigodo fundo', 'Setor', 'Preço Atual', 'P/VPA', 'DividendYield',\
                'QuantidadeAtivos','Liquidez Diária']


#Filtro Setor
def filtroSetor(a):
    if setor != '':
        filter_ = \
                 (a['Setor'] == setor )

        return a[filter_]
    else: 
        return a

df1 = filtroSetor(df[indicadores])

#Filtro Preço da Cota
def filtroPreco(b):
    if precoCota != 0.0:
        filter_ = \
                 (b['Preço Atual'] <= precoCota )

        return b[filter_]
    else:
        return b
    
df2 = filtroPreco(df1)

#Filtro P/VPA
def filtroPvpa(c):
    if pvpa != 0.0:
        filter_ = \
                 (c['P/VPA'] <= pvpa )

        return c[filter_]
    else:
        return c

df3 = filtroPvpa(df2)

#Filtro Dividend Yield
def filtroDvdY(d):
    if dvdY != 0.0:
        filter_ = \
                 (d['DividendYield'] >= dvdY )

        return d[filter_]
    else:
        return d

df4 = filtroDvdY(df3)

#Filtro Liquidez Diária
def filtroLqdD(e):
    if lqdD != 0.0:
        filter_ = \
                 (e['Liquidez Diária'] >= lqdD )

        return e[filter_]
    else:
        return e
    
df5 = filtroLqdD(df4)

#Filtro Quantidade de Ativos
def filtroQntdA(f):
    if qntdA != 0.0:
        filter_ = \
                 (f['QuantidadeAtivos'] >= qntdA )

        return f[filter_]
    else:
        return f

pd.set_option('display.max_columns', None)
df6 = filtroQntdA(df5)


#Verificação final e exportação dos dados encontrados.
if df6.empty == True:
    print('\nInfelizmente nenhum Fundo Imobiliário se enquadra nos critérios informados.\n')
else:
    df6.to_excel('Resultados_FIIS.xlsx', sheet_name = 'pag01', index = False)
    print('\nFIIS encontrados com sucesso, os mesmos foram exportados para uma planilha excel na pasta atual.\n')


    
