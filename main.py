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
    range = request.args.get('range')

    # Fetch the stock data with correct period and interval
    try:
        data = yf.download(ticker, period=range, interval=interval)
        
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
