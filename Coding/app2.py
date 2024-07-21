import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

from flask import Flask, render_template, request, send_file
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    # Load the CSV file
    df = pd.read_csv('cleaned_df.csv')
    # Get unique restaurants (Company)
    restaurants = df['Company'].unique().tolist()
    # Get category columns, excluding the first two assumed non-category columns
    categories = df.columns[2:].tolist()
    return render_template('index.html', restaurants=restaurants, categories=categories)

@app.route('/submit', methods=['POST'])
def submit():
    selected_restaurant = request.form['restaurant']
    selected_category1 = request.form['category1']
    selected_category2 = request.form['category2']
    
    # Load the CSV file
    df = pd.read_csv('cleaned_df.csv')
    # Filter the DataFrame based on the selected restaurant
    filtered_df = df[df['Company'] == selected_restaurant]

    table_data = filtered_df.to_dict(orient='records')

    plot_url = None  # No plot, just display the table

    return render_template('index.html', restaurants=df['Company'].unique().tolist(), categories=df.columns[2:].tolist(), plot_url=plot_url, table_data=table_data, selected_restaurant=selected_restaurant)

if __name__ == '__main__':
    app.run(debug=True)
