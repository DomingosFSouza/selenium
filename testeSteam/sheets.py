#arquivo base coletado e modificado de acordo com o sugerido pelas documentações do Google
from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#escopo para autenticação
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

#ID do arquivo (arquivo real presente no sheets) e Range inicial para modificações do sheets
SAMPLE_SPREADSHEET_ID = '168CVHJoTguQGztFrMTj9j59B7rE1delk'
SAMPLE_RANGE_NAME = 'games!A2:H101'


def main():

    creds = None
    # ajuste feito para download do token neste diretório, para caso de login do usuário pela primeira vez; caso já tenha logado ou tenha o arquivo token válido, irá logar/autenticar diretamente
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        #bloco de código para criação/envio do sheets
        # spreadsheet_body = {
        # 
        # }

        # request = service.spreadsheets().create(body=spreadsheet_body)
        # response = request.execute()

        # pprint(response)

        #Visualização do sheet
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        #bloco de código resultado de alterações a serem feitas no sheet. o bloco 'changes' repesenta as mudanças a serem adicionadas (terá que se alterar o range para o mesmo)
        # changes=[

        # ]
        # result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
        #                             range=SAMPLE_RANGE_NAME, valueInputOptions='USER_ENTERED', body={"values":changes}).execute()

        if not values:
            print('No data found.')
            return

        print(values)
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()