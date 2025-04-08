import pandas as pd

df = pd.read_csv('all_stocks_data.csv', sep=';', index_col=0)

#Converter Dividends para float
df['Dividends'] = df['Dividends'].str.replace(',', '.').str.replace('R\$', '').astype(float)

#Selecionar Date, Close Dividends (onde eles são maiores que 0) do Ticker MULT3.SA
df_dividendo_mult = df.loc[df['Ticker'] == 'ITUB3.SA', ['Close', 'Dividends']]
df_dividendo_mult = df_dividendo_mult[df_dividendo_mult['Dividends'] > 0]


#Somar Dividends no período de Date 2010-01-01 a 2024-12-31
dividendo_mult = df_dividendo_mult['Dividends'].sum()
print(dividendo_mult)

