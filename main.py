import yfinance as yf
import pandas as pd

# Lista de tickers
tickers = [
    'ITUB3.SA', 'LREN3.SA', 'WEGE3.SA', 'EGIE3.SA', 'FLRY3.SA',
    'MULT3.SA', 'EZTC3.SA', 'SMTO3.SA', 'RADL3.SA', 'AZZA3.SA',
    'AGRO3.SA', 'TOTS3.SA', 'ODPV3.SA', 'ASAI3.SA', 'EQTL3.SA',
    'VIVA3.SA', 'ITSA3.SA', 'RENT3.SA', 'VALE3.SA', 'CSAN3.SA',
    'SBSP3.SA', 'MILS3.SA', 'RAIL3.SA', 'B3SA3.SA', 'POSI3.SA',
    'KEPL3.SA', 'PRIO3.SA', 'TUPY3.SA', 'MDIA3.SA', 'BBAS3.SA',
    'PETR3.SA', 'GRND3.SA', 'YDUQ3.SA', 'VIVT3.SA', 'SLCE3.SA',
    'ROMI3.SA', 'ABCB4.SA', 'SCAR3.SA', 'DXCO3.SA', 'NTCO3.SA',
    'PTBL3.SA', 'CSNA3.SA', 'TAEE3.SA', 'HYPE3.SA', 'PRNR3.SA',
    'VLID3.SA', 'TIMS3.SA', 'CSUD3.SA', 'SIMH3.SA', 'TGMA3.SA',
    'SAPR3.SA', 'CSMG3.SA', 'JHSF3.SA', 'ELET3.SA', 'PSSA3.SA',
    'CCRO3.SA', 'VBBR3.SA', 'ALOS3.SA', 'SUZB3.SA', 'CPLE3.SA',
    'KNRI11.SA', 'HGLG11.SA', 'XPML11.SA', 'HGRU11.SA', 'RZTR11.SA',
    'SHPH11.SA', 'HGBS11.SA', 'VISC11.SA', 'BRCO11.SA', 'HSML11.SA',
    'TVRI11.SA', 'TRXF11.SA', 'JSRE11.SA', 'MALL11.SA', 'KNCR11.SA',
    'TGAR11.SA'
]

# Função para obter histórico de preços e informações da empresa
def get_stock_history(tickers):
    all_data = []
    
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        
        # Tente obter o histórico de preços
        try:
            price_history = stock.history(period="max")
        except Exception as e:
            print(f"Erro ao obter histórico de preços para {ticker}: {e}")
            price_history = pd.DataFrame()  # DataFrame vazio se falhar

        # Obter informações da empresa
        info = stock.info
        company_name = str(info.get('longName', 'N/A'))  # Garantir que seja string
        website = str(info.get('website', 'N/A'))  # Garantir que seja string
        shares_outstanding = info.get('sharesOutstanding', 'N/A')

        # Adicionar as informações da empresa ao DataFrame de preços
        if not price_history.empty:
            price_history['Company Name'] = company_name
            price_history['Website'] = website
            price_history['Shares Outstanding'] = shares_outstanding
            
            # Adicionar os dados formatados à lista
            all_data.append(price_history)

    # Concatenar todos os DataFrames em um único DataFrame
    combined_data = pd.concat(all_data)
    return combined_data

# Função para formatar dados
def format_data(df):
    for col in ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"{x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    return df

# Obter histórico de preços e informações da empresa
stock_history = get_stock_history(tickers)

# Formatar os dados antes de salvar
formatted_stock_history = format_data(stock_history)

# Salvar todos os dados em um único arquivo CSV com codificação UTF-8
formatted_stock_history.to_csv('all_stocks_data.csv', sep=';', encoding='utf-8-sig', index=True)

print("Dados de todas as ações salvos em: all_stocks_data.csv")