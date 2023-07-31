# **Meu projeto de coleta de dados na Steam**

O projeto construído conta com uma automação produzida para coleta de dados do site de promoções da Steam. Para a produção do mesmo, foi utilizado Selenium e BeautifulSoup4, Pandas, bem como a inserção de sua raspagem de dados no Google BigQuery.

O projeto foi produzido a partir de um modelo de processo espiral e incremental, que passou por várias etapas, devido a sua gestão de tempo necessária para conclusão em período determinado.

## Configurações utilizadas

Tecnologia | Versão | Status
---------- | ------ |----------
Python|3.9.13|Em uso
Selenium|4.10.0|Em uso
Chromedriver|111|Em uso
BeautifulSoup|4.12.2|Em uso

## Arquivos do projeto
1. [Automação de coleta de dados e envio para o Google BigQuery](../testeSteam/teste.py)
1. [CRUD para uso do arquivo no Google Sheets](../testeSteam/sheets.py)
1. [Planilha com os dados coletados no arquivo 1](../testeSteam/steamGames.xlsx)
1. [Link para visualizar o sheets](https://docs.google.com/spreadsheets/d/168CVHJoTguQGztFrMTj9j59B7rE1delk/edit?usp=sharing&ouid=113560417324643837972&rtpof=true&sd=true)