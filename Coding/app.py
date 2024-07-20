from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the CSV data into a pandas DataFrame
file_path = "../Resources/FastFoodNutritionMenuV2.csv"
df = pd.read_csv(file_path)

@app.route('/')
def index():
    # Get unique restaurant names from the 'company' column
    restaurants = df['company'].unique().tolist()
    # Get nutrition categories from all columns except 'company' and 'item'
    nutrition_categories = df.columns.drop(['company', 'item']).tolist()

    # Debug: Print loaded data
    print("Restaurants:", restaurants)
    print("Nutrition Categories:", nutrition_categories)

    return render_template('index.html', restaurants=restaurants, categories=nutrition_categories)

@app.route('/get_data', methods=['POST'])
def get_data():
    restaurant = request.form['restaurant']
    category1 = request.form['category1']
    category2 = request.form['category2']
    
    # Filter the data based on the selected restaurant
    filtered_df = df[df['company'] == restaurant]
    
    # Prepare the data for the scatter plot
    plot_data = filtered_df[['item', category1, category2]].dropna().to_dict(orient='records')
    
    return jsonify(plot_data)

if __name__ == '__main__':
    app.run(debug=True)