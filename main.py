from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return render_template('chart.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    image_base64 = data['image']
    symbol = data['symbol']

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a stock market analyst."},
            {"role": "user", "content": f"Analyze the following chart for {symbol}:\n![Chart](data:image/png;base64,{image_base64})"}
        ]
    )

    analysis = response['choices'][0]['message']['content']
    return jsonify({'analysis': analysis})

if __name__ == '__main__':
    app.run(debug=True)
