from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    df = pd.read_csv('static/data/cleaned_df.csv')
    df['Net Carbs'] = df['Carbs (g)'] - df['Fiber (g)']
    return df.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)
