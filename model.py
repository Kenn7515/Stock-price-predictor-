import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR

def predict_stock(user_stock, future_days=5):
    stocks = [
        "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS",
        "ICICIBANK.NS", "SBIN.NS", "WIPRO.NS", "LT.NS",
        "AXISBANK.NS", "KOTAKBANK.NS",
        "AAPL", "TSLA", "GOOGL", "MSFT", "AMZN",
        "META", "NFLX", "NVDA", "ORCL", "INTC"
    ]

    if user_stock not in stocks:
        return []

    data = yf.download(user_stock, period="6mo")

    df = data.copy()

    df['Prediction'] = df['Close'].shift(-future_days)
    df.dropna(inplace=True)

    X = np.array(df[['Close']])
    y = np.array(df['Prediction'])

    split = int(len(df) * 0.8)

    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(),
        "Random Forest": RandomForestRegressor(n_estimators=100),
        "SVM": SVR()
    }

    for model in models.values():
        model.fit(X_train, y_train)

    model = models["Random Forest"]

    last_value = df[['Close']].tail(1).values
    future_predictions = []

    for _ in range(future_days):
        next_pred = model.predict(last_value)[0]
        future_predictions.append(round(float(next_pred), 2))
        last_value = np.array([[next_pred]])

    return future_predictions