from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    csv_path = '/Users/pamala/Documents/GitHub/Project3_DataVisualization/Resources/FastFoodNutritionMenuV2.csv'
    
    if not os.path.exists(csv_path):
        return "CSV file not found!", 404
    
    df = pd.read_csv(csv_path)
    restaurants = df['restaurant'].unique().tolist()
    categories = df.columns[2:].tolist()
    
    return render_template('index.html', restaurants=restaurants, categories=categories)

@app.route('/get_data', methods=['POST'])
def get_data():
    restaurant = request.form['restaurant']
    category1 = request.form['category1']
    category2 = request.form['category2']
    
    csv_path = '/Users/pamala/Documents/GitHub/Project3_DataVisualization/Resources/FastFoodNutritionMenuV2.csv'
    
    df = pd.read_csv(csv_path)
    data = df[df['restaurant'] == restaurant][['item', category1, category2]].to_dict(orient='records')
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
