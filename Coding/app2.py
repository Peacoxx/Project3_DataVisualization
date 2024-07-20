from flask import Flask, render_template, request, jsonify
import pandas as pd
import sqlite3
import plotly.express
import jinja2

app = Flask(__name__)

# Load the CSV data into a pandas DataFrame

def get_db_connection():
    conn = sqlite3.connect('fastfood.db')
    conn.row_factory = sqlite3.Row
    return conn  

@app.route('/')
def index():
    conn = get_db_connection()
    df = pd.read_sql('SELECT * FROM menu', conn)
    conn.close()
    columns = df.columns.tolist()
    return render_template('index.html', columns=columns)

@app.route('/scatterplot', methods=['POST'])
def scatterplot():
    x_axis = request.form.get('x_axis')
    y_axis = request.form.get('y_axis')
    restaurant = request.form.get('restaurant')

    conn = get_db_connection()
    query = 'SELECT * FROM menu'
    df = pd.read_sql_query(query, conn)
    conn.close()

    if restaurant:
        df = df[df['Company'] == restaurant]

    fig = px.scatter(df, x=x_axis, y=y_axis, title=f'{x_axis} vs {y_axis} for {restaurant}')
    graphJSON = fig.to_json()

    return jsonify(graphJSON)

if __name__ == '__main__':
    app.run(debug=True)

