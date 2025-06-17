from flask import Flask, render_template_string, request, redirect, url_for
import yfinance as yf

app = Flask(__name__)

# Tickers padrão para buscar — pode ampliar ou alterar
def buscar_tickers_padroes():
    return ["BBAS3.SA", "PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "MGLU3.SA", "ABEV3.SA"]

# Função que usa yfinance para buscar dados da ação
def obter_dados_yfinance(ticker):
    try:
        ativo = yf.Ticker(ticker)
        info = ativo.info
        # yfinance não traz todas corretoras nem datas, mas traz preço atual, targetMeanPrice, etc.
        preco_atual = info.get("regularMarketPrice", "N/D")
        preco_alvo = info.get("targetMeanPrice", "N/D")  # preço-alvo médio dos analistas
        recomendações = []

        # Como exemplo, mostramos preço atual e preço alvo médio — yfinance não traz lista detalhada
        if preco_alvo != "N/D":
            recomendações.append({"fonte": "Consenso Analistas", "preco_alvo": preco_alvo, "data": "Atual"})

        return preco_atual, recomendações
    except Exception as e:
        return None, []

TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Consulta de Preço-Alvo Real com yfinance</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        table { border-collapse: collapse; width: 50%; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        select, button { padding: 8px 12px; font-size: 16px; margin-top: 10px; }
    </style>
</head>
<body>
    <h1>Consulta de Preço-Alvo Real com yfinance</h1>

    <form method="post" action="{{ url_for('scan') }}">
        <button type="submit">🔎 Buscar Preço-Alvo (Carregar lista de ações)</button>
    </form>

    {% if tickers %}
    <form method="get" action="{{ url_for('index') }}">
        <label for="ticker">Selecione o ticker:</label><br>
        <select name="ticker" id="ticker" required>
            {% for t in tickers %}
                <option value="{{ t }}" {% if t == ticker %}selected{% endif %}>{{ t }}</option>
            {% endfor %}
        </select><br>
        <input type="hidden" name="tickers" value="{{ ','.join(tickers) }}">
        <button type="submit">Obter Dados</button>
    </form>
    {% endif %}

    {% if preco_atual is not none %}
        <h2>Dados para {{ ticker }}</h2>
        <p><strong>Preço atual:</strong> R$ {{ preco_atual }}</p>

        {% if resultados %}
            <table>
                <tr>
                    <th>Fonte</th>
                    <th>Preço-Alvo (R$)</th>
                    <th>Data</th>
                </tr>
                {% for item in resultados %}
                <tr>
                    <td>{{ item.fonte }}</td>
                    <td>R$ {{ '%.2f'|format(item.preco_alvo) }}</td>
                    <td>{{ item.data }}</td>
                </tr>
                {% endfor %}
            </table>
        {% else %}
            <p><em>Preço-alvo não disponível para este ativo.</em></p>
        {% endif %}
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    ticker = request.args.get("ticker", "").strip().upper()
    tickers_str = request.args.get("tickers", "")
    tickers = tickers_str.split(",") if tickers_str else []

    preco_atual = None
    resultados = []

    if ticker:
        preco_atual, resultados = obter_dados_yfinance(ticker)

    return render_template_string(
        TEMPLATE,
        tickers=tickers,
        ticker=ticker,
        preco_atual=preco_atual,
        resultados=resultados
    )

@app.route("/scan", methods=["POST"])
def scan():
    # Simula "varredura" retornando a lista de tickers
    tickers = buscar_tickers_padroes()
    tickers_str = ",".join(tickers)
    return redirect(url_for("index", tickers=tickers_str))

if __name__ == "__main__":
    app.run(debug=True)
