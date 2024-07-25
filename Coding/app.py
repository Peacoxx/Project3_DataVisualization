from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    csv_path = os.path.join(app.root_path, 'static', 'data', 'cleaned_df.csv')
    # csv_path = ("../static/data/cleaned_df.csv")
    df = pd.read_csv(csv_path)
    df['Carbs (g)'] = pd.to_numeric(df['Carbs (g)'], errors='coerce')
    df['Fiber (g)'] = pd.to_numeric(df['Fiber (g)'], errors='coerce')
    df['Net Carbs'] = df['Carbs (g)'] - df['Fiber (g)']
    return df.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)
