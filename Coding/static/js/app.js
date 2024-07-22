// Function to build the metadata panel
function buildMetadata(company, item) {
    d3.json("/data").then((data) => {
        let metadata = data.filter(d => d.Company === company && d.Item === item)[0];

        let PANEL = d3.select("#sample-metadata");
        PANEL.html("");

        Object.entries(metadata).forEach(([key, value]) => {
            let displayKey = key === "Net Carbs" ? `<span style="color: green">${key.toUpperCase()}</span>` : key.toUpperCase();
            PANEL.append("h6").html(`${displayKey}: ${value}`);
        });
    });
}

// Function to build the bar chart
function buildCharts(company) {
    d3.json("/data").then((data) => {
        let companyData = data.filter(d => d.Company === company);

        let top10Items = companyData.sort((a, b) => b.Calories - a.Calories).slice(0, 10);

        let barData = [{
            x: top10Items.map(d => d.Calories).reverse(),
            y: top10Items.map(d => d.Item).reverse(),
            text: top10Items.map(d => d.Item).reverse(),
            type: "bar",
            orientation: "h"
        }];

        let barLayout = {
            title: "Top 10 High Calorie Items",
            margin: { t: 30, l: 150 }
        };

        Plotly.newPlot("bar", barData, barLayout);

        // Nutrition Overview Heatmap
        let heatmapData = [{
            z: companyData.map(d => [d.Calories, d["Total Fat (g)"], d["Carbs (g)"], d["Protein (g)"]]),
            x: ["Calories", "Total Fat (g)", "Carbs (g)", "Protein (g)"],
            y: companyData.map(d => d.Item),
            colorscale: "Viridis",
            type: "heatmap"
        }];

        let heatmapLayout = {
            title: "Nutrition Overview",
            margin: { t: 30, l: 150 }
        };

        Plotly.newPlot("bubble", heatmapData, heatmapLayout);
    });
}

// Function to run on page load
function init() {
    d3.json("/data").then((data) => {
        let companyNames = [...new Set(data.map(d => d.Company))];
        let firstCompany = companyNames[0];
        let firstItem = data.filter(d => d.Company === firstCompany)[0].Item;

        let companySelector = d3.select("#selDataset");
        let itemSelector = d3.select("#itemDataset");

        companyNames.forEach((company) => {
            companySelector.append("option").text(company).property("value", company);
        });

        let items = data.filter(d => d.Company === firstCompany).map(d => d.Item);
        items.forEach((item) => {
            itemSelector.append("option").text(item).property("value", item);
        });

        buildCharts(firstCompany);
        buildMetadata(firstCompany, firstItem);
    });
}

// Function for event listener
function optionChanged(newCompany, newItem) {
    buildCharts(newCompany);
    buildMetadata(newCompany, newItem);
}

// Initialize the dashboard
init();
