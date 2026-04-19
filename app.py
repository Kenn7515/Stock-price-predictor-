from flask import Flask, render_template, request
from model import predict_stock

app = Flask(__name__)

STOCKS = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS",
    "ICICIBANK.NS", "SBIN.NS", "WIPRO.NS", "LT.NS",
    "AXISBANK.NS", "KOTAKBANK.NS",
    "AAPL", "TSLA", "GOOGL", "MSFT", "AMZN",
    "META", "NFLX", "NVDA", "ORCL", "INTC"
]

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = []
    stock = None
    days = None

    if request.method == "POST":
        stock = request.form["stock"]
        days = int(request.form["days"])
        prediction = predict_stock(stock, days)

    return render_template(
        "index.html",
        prediction=prediction,
        stocks=STOCKS,
        selected_stock=stock,
        days=days
    )

if __name__ == "__main__":
    app.run(debug=True)