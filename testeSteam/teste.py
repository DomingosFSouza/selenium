from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
# from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

#utitlizações abaixo corresponderiam ao envio dos dados para o google sheets. o mesmo podes er visto no arquivo 'sheets.py' neste diretório
# from __future__ import print_function
# import os.path
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

#o uso dos imports abaixo seriam destinados a transferência de diretórios em prol da melhoria do profile do navegador e da inserção da extensão utilizada (reCAPTCHA) no mesmo.
# import shutil
# import os

#com as pastas da extensão neste diretório, ajustaria a facilidade da obtenção da extensão utilizada nesta automação no navagador para quem não a teria
# sd='extension' #pega pasta
# dd='dir final' #cria pasta
# shutil.move(sd,dd) #move de um pro outro

#o uso do useragent foi abolido, devido a falta da necessidade de seu uso, neste caso em específico, em que o webdrive estava apresentando um useragent adequado (locaclmente).
# ua=UserAgent()

#devido as atualizações do código e o uso do que se precisava para burlar o captcha, foi preferível usar ChromeOptions a Options
# option = Options()
option = webdriver.ChromeOptions()

#inserção da local presente no meu iniciável chrome, do qual teve auteração em seu código fonte, para fomentar a camuflagem da automação
service = Service(executable_path='/usr/local/bin/chromedriver') #chrome

#seguimento no ajuste da camuflagem da automação
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option("useAutomationExtension", False)
option.add_argument('--no-sandbox')
option.add_argument('disable-blink-features=AutomationControlled')
option.add_argument(f'headleass={None}')

#inserção de um profile com dados que assimilam o de uma pessoa comum
#é de extrema importância que a extensão 'https://chrome.google.com/webstore/detail/recaptcha-autoclick/caahalkghnhbabknipmconmbicpkcopl?hl=en-US' esteja no browser, para concretizar a entrada no site da steam corretamente.
#a extensão citada já estava presente 
option.add_argument('user-data-dir=/home/domingos/.config/google-chrome/Default')
PROXY_HOST = "12.12.12.123"
PROXY_PORT = int(1234)
option.add_argument('network.proxy.type=1')
option.add_argument(f'network.proxy.http={PROXY_HOST}')
option.add_argument(f'network.proxy.http_port={PROXY_PORT}')
option.add_argument('dom.webdriver.enabled=False')

#para que o navegador possa ficar aberto e ajudar na visibilidade do site, ao precisar, em algum momento, da supervisão na automação, que não é o caso.
# option.add_experimental_option("detach", True)

#Abrindo e configurando o navegador 
driver = webdriver.Chrome(service=service, options=option)
#script para ajuste da camuflagem da automação
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

#logando no site desejado
driver.get('https://steamdb.info/sales/')
#esperando pular a captcha para colher os dados requeridos
sleep(3)
bs_obj = bs(driver.page_source, 'html.parser')
#pegando os títulos para as tabelas/datasheet
thtitulos=bs_obj.find_all('th', {'class':'sorting'})
titles=[thtitulos[1].text, thtitulos[2].text, thtitulos[3].text, thtitulos[4].text, thtitulos[5].text, thtitulos[6].text, thtitulos[7].text]

#obtendo os dados dos jogos presentes no site
listGames=[]
trapp=bs_obj.find_all('tr', {'class':'app'})
elementApp=driver.find_elements(By.CLASS_NAME, "app")
count=0

for i in range(len(trapp)):
    if count==17 or count==38 or count==59 or count==70 or count==79:
        ActionChains(driver)\
            .scroll_to_element(elementApp[count+20])\
            .perform()
        sleep(2)
        bs_obj = bs(driver.page_source, 'html.parser')
        trapp=bs_obj.find_all('tr', {'class':'app'})
    game=trapp[i].find_all('td')
    namegame=game[2].find_all('a')
    namegame=namegame[0].text
    precentSale=game[3].text
    price=game[4].text
    rating=game[5].text
    endsIn=game[6].text
    started=game[7].text
    release=game[8].text

    insertingDF=dict({thtitulos[1].text:namegame, thtitulos[2].text:precentSale, thtitulos[3].text:price, thtitulos[4].text:rating, thtitulos[5].text:endsIn, thtitulos[6].text:started, thtitulos[7].text:release})
    listGames.append(insertingDF)
    count=count+1
#inserindo-os em um dataframe
df_games = pd.DataFrame(listGames, columns=titles)

#criando planilha
with pd.ExcelWriter('steamGames.xlsx') as writer:
#ajustando nome do sheet na planilha criada
    df_games.to_excel(writer, sheet_name='games')

#credenciais de acesso ao google big query, para inserção dos dados da planilha no mesmo
#a variavel 'mykey_path' consta o endereço do arquivo de autenticação no site (o que é pessoal)
mykey_path="GBQ.json"
credentials = service_account.Credentials.from_service_account_file(mykey_path, scopes=["https://www.googleapis.com/auth/cloud-platform"])

#enviando o df para o google big query
df_games.to_gbq(credentials=credentials, destination_table='mybigquery.games', if_exists='replace')

#o bloco de código abaixo representa um exemplo do envio dos dados para o sheets. como mencionado no cabeçalho, o mesmo poderá ser encontrado no arquivo 'sheets.py', nesse diretório

# #escopo para autenticação no sheets
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# #ID do arquivo (arquivo real presente no sheets) e Range inicial para modificações do sheets
# SAMPLE_SPREADSHEET_ID = '168CVHJoTguQGztFrMTj9j59B7rE1delk'
# SAMPLE_RANGE_NAME = 'games!A2:H101'


# creds = None
# # ajuste feito para download do token neste diretório, para caso de login do usuário pela primeira vez; caso já tenha logado ou tenha o arquivo token válido, irá logar/autenticar diretamente
# if os.path.exists('token.json'):
#     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# if not creds or not creds.valid:
#     if creds and creds.expired and creds.refresh_token:
#         creds.refresh(Request())
#     else:
#         flow = InstalledAppFlow.from_client_secrets_file(
#             'client_secret.json', SCOPES)
#         creds = flow.run_local_server(port=0)
#     with open('token.json', 'w') as token:
#         token.write(creds.to_json())
# try:
#     service = build('sheets', 'v4', credentials=creds)

#     #bloco de código para criação/envio do sheets
#     # request = service.spreadsheets().create(body={[df_games.columns.values.tolist()] + df_games.values.tolist()})
#     # response = request.execute()

#     # pprint(response)
# except HttpError as err:
#     print(err)

# LINK DO SHEET COLETADO: https://docs.google.com/spreadsheets/d/168CVHJoTguQGztFrMTj9j59B7rE1delk/edit?usp=sharing&ouid=113560417324643837972&rtpof=true&sd=true