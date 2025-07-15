import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
!pip install yfinance

ativo = 'CXSE3.SA'

pd.options.mode.chained_assignment = None

def calcular_rsi(ativo, periodo=14):
    """
    Calcula o RSI de um ativo.

    Args:
        ativo: DataFrame com os dados do ativo.
        periodo: Número de períodos para o cálculo do RSI.

    Returns:
        DataFrame com os dados do ativo e o RSI calculado.
    """

periodo = 14

# Baixar os dados do ativo
dados_ativo = yf.download(ativo)
dados_ativo

# Baixar os dados do ativo
dados_ativo = yf.download(ativo)
# Verificar se a coluna 'Adj Close' existe, se não, usar 'Close'
if 'Adj Close' not in dados_ativo.columns:
    dados_ativo['Adj Close'] = dados_ativo['Close']
dados_ativo

# Calcular os retornos
dados_ativo['retornos'] = dados_ativo['Adj Close'].pct_change()

# Calcular os retornos positivos e negativos
dados_ativo['retornos_positivos'] = dados_ativo['retornos'].apply(lambda x: x if x > 0 else 0)
dados_ativo['retornos_negativos'] = dados_ativo['retornos'].apply(lambda x: abs(x) if x < 0 else 0)

# Calcular os retornos positivos e negativos
dados_ativo['retornos_positivos'] = dados_ativo['retornos'].apply(lambda x: x if x > 0 else 0)
dados_ativo['retornos_negativos'] = dados_ativo['retornos'].apply(lambda x: abs(x) if x < 0 else 0)

# Calcular a média móvel dos retornos positivos e negativos
dados_ativo['media_retornos_positivos'] = dados_ativo['retornos_positivos'].rolling(14).mean()
dados_ativo['media_retornos_negativos'] = dados_ativo['retornos_negativos'].rolling(14).mean()

# Calcular o RSI
dados_ativo['RSI'] = 100 - 100 / (1 + dados_ativo['media_retornos_positivos'] / dados_ativo['media_retornos_negativos'])

# Plotar o preço ajustado
dados_ativo['Adj Close'].plot(title=f'Preço Ajustado de {ativo}', figsize=(12, 6))
plt.show()

# Calcular os retornos positivos e negativos
dados_ativo['retornos_positivos'] = dados_ativo['retornos'].apply(lambda x: x if x > 0 else 0)
dados_ativo['retornos_negativos'] = dados_ativo['retornos'].apply(lambda x: abs(x) if x < 0 else 0)

# Calcular a média móvel dos retornos positivos e negativos
dados_ativo['media_retornos_positivos'] = dados_ativo['retornos_positivos'].rolling(14).mean()
dados_ativo['media_retornos_negativos'] = dados_ativo['retornos_negativos'].rolling(14).mean()

# Calcular o RSI
dados_ativo['RSI'] = 100 - 100 / (1 + dados_ativo['media_retornos_positivos'] / dados_ativo['media_retornos_negativos'])

# Plotar o preço ajustado
dados_ativo['Adj Close'].plot(title=f'Preço Ajustado de {ativo}', figsize=(12, 6))
plt.show()

# Remover valores NaN resultantes do cálculo da média móvel
# The columns are now created, so dropna should work
# Ensure the columns exist before dropping NaNs
if {'media_retornos_positivos', 'media_retornos_negativos'}.issubset(dados_ativo.columns):
    dados_ativo.dropna(subset=['media_retornos_positivos', 'media_retornos_negativos'], inplace=True)
else:
    print("Columns 'media_retornos_positivos' and/or 'media_retornos_negativos' not found in DataFrame.")

# Calcular os retornos positivos e negativos
dados_ativo['retornos_positivos'] = dados_ativo['retornos'].apply(lambda x: x if x > 0 else 0)
dados_ativo['retornos_negativos'] = dados_ativo['retornos'].apply(lambda x: abs(x) if x < 0 else 0)

# Calcular a média móvel dos retornos positivos e negativos
dados_ativo['media_retornos_positivos'] = dados_ativo['retornos_positivos'].rolling(14).mean()
dados_ativo['media_retornos_negativos'] = dados_ativo['retornos_negativos'].rolling(14).mean()

# Calcular o RSI
dados_ativo['RSI'] = 100 - 100 / (1 + dados_ativo['media_retornos_positivos'] / dados_ativo['media_retornos_negativos'])

# Plotar o preço ajustado
dados_ativo['Adj Close'].plot(title=f'Preço Ajustado de {ativo}', figsize=(12, 6))
plt.show()

# Remover valores NaN resultantes do cálculo da média móvel
# The columns are now created, so dropna should work
# Ensure the columns exist before dropping NaNs
# The KeyError happens because 'media_retornos_positivos', 'media_retornos_negativos'
# are not in the DataFrame columns.
# This is likely because the calculation above resulted in NaN values, and the columns were not properly created.
# We can fix this by checking if the columns exist before calling dropna

if {'media_retornos_positivos', 'media_retornos_negativos'}.issubset(dados_ativo.columns):
    dados_ativo.dropna(subset=['media_retornos_positivos', 'media_retornos_negativos'], inplace=True)
else:
    print("Columns 'media_retornos_positivos' and/or 'media_retornos_negativos' not found in DataFrame.")

# Definir sinais de compra e venda
def decisao_compra_venda(rsi):
    if rsi < 30:
        return 'Comprar'
    elif rsi > 70:
        return 'Vender'
    else:
        return 'Manter'

dados_ativo['Sinal'] = dados_ativo['RSI'].apply(decisao_compra_venda)

# Visualizar os primeiros  registros
print(dados_ativo.head(10000))

# Plotar o preço ajustado e os sinais de compra/venda
plt.figure(figsize=(12, 6))
plt.plot(dados_ativo.index, dados_ativo['Adj Close'], label='Preço Ajustado', color='blue')

compras = dados_ativo[dados_ativo['Sinal'] == 'Comprar']
vendas = dados_ativo[dados_ativo['Sinal'] == 'Vender']

plt.scatter(compras.index, compras['Adj Close'], label='Sinal de Compra', marker='^', color='green')
plt.scatter(vendas.index, vendas['Adj Close'], label='Sinal de Venda', marker='v', color='red')

plt.title(f'Sinais de Compra e Venda para {ativo}')
plt.xlabel('Data')
plt.ylabel('Preço Ajustado')
plt.legend()
plt.show()
plt.close()

# Plotar o RSI
plt.figure(figsize=(12, 6))
plt.plot(dados_ativo.index, dados_ativo['RSI'], label='RSI', color='purple')
plt.axhline(30, linestyle='--', alpha=0.5, color='red', label='Sobrevendido (30)')
plt.axhline(70, linestyle='--', alpha=0.5, color='green', label='Sobrecomprado (70)')

plt.title(f'RSI para {ativo}')
plt.xlabel('Data')
plt.ylabel('RSI')
plt.legend()
plt.show()
plt.close()

# Verificar o RSI mais recente e decidir se é um bom momento para comprar, vender ou manter
rsi_recente = dados_ativo['RSI'].iloc[-1]
if rsi_recente < 30:
    print("Sim Comprar")
elif rsi_recente > 70:
    print("Não Comprar")
else:
    print("Manter")
