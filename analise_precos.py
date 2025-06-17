from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Simula busca de tickers disponíveis em corretoras
def buscar_tickers_padroes():
    return ["BBAS3", "PETR4", "VALE3", "ITUB4", "BBDC4", "MGLU3", "ABEV3"]

# Dados simulados de recomendação
def obter_precos_alvo(ticker):
    dados = {
        "BBAS3": [
            {"fonte": "XP Investimentos", "preco_alvo": 41.00, "data": "11/04/2025"},
            {"fonte": "BTG Pactual", "preco_alvo": 35.00, "data": "23/01/2025"},
            {"fonte": "Genial Analisa", "preco_alvo": 34.00, "data": "2025"},
        ],
        "PETR4": [
            {"fonte": "BTG Pactual", "preco_alvo": 45.00, "data": "2025"},
            {"fonte": "Itaú BBA", "preco_alvo": 43.50, "data": "2025"},
            {"fonte": "Credit Suisse", "preco_alvo": 40.00, "data": "2025"},
        ],
        "VALE3": [
            {"fonte": "XP Investimentos", "preco_alvo": 72.00, "data": "2025"},
            {"fonte": "Bradesco BBI", "preco_alvo": 68.00, "data": "2025"},
            {"fonte": "Safra", "preco_alvo": 70.00, "data": "2025"},
        ],
        "ITUB4": [
            {"fonte": "Santander", "preco_alvo": 34.00, "data": "2025"},
            {"fonte": "BTG Pactual", "preco_alvo": 36.00, "data": "2025"},
        ],
        "BBDC4": [
            {"fonte": "BTG Pactual", "preco_alvo": 27.50, "data": "2025"},
            {"fonte": "Goldman Sachs", "preco_alvo": 28.00, "data": "2025"},
        ],
        "MGLU3": [
            {"fonte": "XP Investimentos", "preco_alvo": 3.20, "data": "2025"},
            {"fonte": "BTG Pactual", "preco_alvo": 4.00, "data": "2025"},
        ],
        "ABEV3": [
            {"fonte": "Itaú BBA", "preco_alvo": 17.00, "data": "2025"},
            {"fonte": "XP Investimentos", "preco_alvo": 18.50, "data": "2025"},
        ]
    }
    return dados.get(ticker.upper(), [])

# Cálculo da média dos preços-alvo
def calcular_media(valores):
    precos = [item["preco_alvo"] for item in valores if item["preco_alvo"]]
    return round(sum(precos) / len(precos), 2) if precos else 0.0

# HTML com placeholders Jinja
TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Preço-Alvo de Ações</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        input[type=text], select { padding: 6px; width: 200px; }
        button { padding: 6px 12px; margin-left: 10px; }
    </style>
</head>
<body>
    <h1>Consulta de Preço-Alvo</h1>

    <form method="post" action="{{ url_for('scan') }}">
        <button type="submit">🔎 Buscar Preço-Alvo</button>
    </form>

    {% if tickers %}
    <form method="get" action="{{ url_for('index') }}">
        <label for="ticker">Escolha o ticker:</label>
        <select name="ticker" id="ticker">
            {% for t in tickers %}
                <option value="{{ t }}" {% if t == ticker %}selected{% endif %}>{{ t }}</option>
            {% endfor %}
        </select>
        <input type="hidden" name="tickers" value="{{ ','.join(tickers) }}">
        <button type="submit">Obter dados</button>
    </form>
    {% endif %}

    {% if resultados %}
        <h2>Resultados para {{ ticker.upper() }}</h2>
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
            <tr>
                <td colspan="3"><strong>Média: R$ {{ media }}</strong></td>
            </tr>
        </table>
    {% elif ticker %}
        <p><em>Nenhum dado encontrado para o ticker informado.</em></p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    ticker = request.args.get("ticker", "").strip().upper()
    tickers_str = request.args.get("tickers", "")
    tickers = tickers_str.split(",") if tickers_str else []
    resultados = obter_precos_alvo(ticker) if ticker else []
    media = calcular_media(resultados) if resultados else 0.0
    return render_template_string(TEMPLATE, ticker=ticker, resultados=resultados, media=media, tickers=tickers)

@app.route("/scan", methods=["POST"])
def scan():
    tickers = buscar_tickers_padroes()
    tickers_str = ",".join(tickers)
    return redirect(url_for('index', tickers=tickers_str))

if __name__ == "__main__":
    app.run(debug=True)
