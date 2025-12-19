from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "aa4c1c32e87c4b4d80979858c13c78d1"

def convert_currency(amount, source, target):
    url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    rates = data["rates"]

    # Convert source → USD → target
    if source != "USD":
        amount = amount / float(rates[source])

    converted_amount = amount * float(rates[target])
    return round(converted_amount, 2)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()

    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']

    print("Source Currency:", source_currency)
    print("Amount:", amount)
    print("Target Currency:", target_currency)

    try:
        final_amount = convert_currency(amount, source_currency, target_currency)

        return jsonify({
            "fulfillmentText": f"{amount} {source_currency} is equal to {final_amount} {target_currency}"
        })

    except KeyError:
        return jsonify({
            "fulfillmentText": "Sorry, I couldn't convert that currency. Please try again."
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
