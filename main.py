from flask import Flask, render_template, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('chart.html')

@app.route('/stock-data')
def stock_data():
    ticker = request.args.get('ticker')
    interval = request.args.get('interval')

    # Determine the period based on the interval
    if interval == '1m':
        period = '5d'  # Yahoo Finance allows only 7 days for 1m interval
    elif interval in ['5m', '15m', '30m', '1h']:
        period = '60d'  # Yahoo Finance allows up to 60 days for these intervals
    elif interval == '1d':
        period = 'max'
    elif interval in ['1wk', '1mo']:
        period = 'max'
    else:
        return jsonify({"error": "Invalid interval"}), 400

    try:
        # Fetch the stock data
        data = yf.download(ticker, period=period, interval=interval)

        if data.empty:
            return jsonify({"error": "No data available for this interval"}), 400

        # Format the data for the response
        formatted_data = [{"time": str(d), "value": v} for d, v in zip(data.index, data['Close'])]
        return jsonify(formatted_data)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
