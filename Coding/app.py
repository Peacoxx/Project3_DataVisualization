from flask import Flask, render_template, request, send_file
import pandas as pd
import matplotlib.pyplot as plt
import io
import os

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
    
    # Create a scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(filtered_df[selected_category1], filtered_df[selected_category2])
    plt.xlabel(selected_category1)
    plt.ylabel(selected_category2)
    plt.title(f'Scatter Plot of {selected_category1} vs {selected_category2} for {selected_restaurant}')
    
    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
