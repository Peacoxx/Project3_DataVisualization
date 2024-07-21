import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

from flask import Flask, render_template, request
import pandas as pd
import plotly.graph_objs as go
import json
import plotly

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
    
    print(f"Selected Restaurant: {selected_restaurant}")
    print(f"Selected Category 1: {selected_category1}")
    print(f"Selected Category 2: {selected_category2}")
    print(f"Filtered DataFrame: {filtered_df.head()}")

    # Generate the bar chart using Plotly
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=filtered_df['Item'],
        y=filtered_df[selected_category1],
        name=selected_category1
    ))
    fig.add_trace(go.Bar(
        x=filtered_df['Item'],
        y=filtered_df[selected_category2],
        name=selected_category2
    ))

    fig.update_layout(
        title=f'{selected_category1} and {selected_category2} for {selected_restaurant}',
        xaxis_title='Food Item',
        yaxis_title='Nutritional Value',
        barmode='group'
    )

    # Convert the plotly figure to JSON
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        'index.html',
        restaurants=df['Company'].unique().tolist(),
        categories=df.columns[2:].tolist(),
        plot_json=plot_json,
        selected_restaurant=selected_restaurant,
        selected_category1=selected_category1,
        selected_category2=selected_category2
    )

if __name__ == '__main__':
    app.run(debug=True)
