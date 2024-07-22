// Function to calculate net carbs
function calculateNetCarbs(totalCarbs, fiber) {
    return totalCarbs - fiber;
  }
  
  // Function to build the metadata panel
  function buildMetadata(item) {
    d3.json("/data").then((data) => {
      let resultArray = data.filter(sampleObj => sampleObj.Item === item);
      let result = resultArray[0];
  
      let PANEL = d3.select("#sample-metadata");
      PANEL.html("");
  
      // Calculate net carbs and add it to the metadata
      let netCarbs = calculateNetCarbs(result['Carbs (g)'], result['Fiber (g)']);
      result['Net Carbs'] = netCarbs;
  
      Object.entries(result).forEach(([key, value]) => {
        if (key === 'Net Carbs') {
          PANEL.append("h6").html(`<span style="color: green;">${key.toUpperCase()}: ${value}</span>`);
        } else {
          PANEL.append("h6").text(`${key.toUpperCase()}: ${value}`);
        }
      });
    });
  }
  
  // Function to build both charts
  function buildCharts(restaurant) {
    d3.json("/data").then((data) => {
      let samples = data.filter(sampleObj => sampleObj.Company === restaurant);
  
      let top10Calories = samples.sort((a, b) => b.Calories - a.Calories).slice(0, 10);
  
      let barData = [{
        x: top10Calories.map(d => d.Calories),
        y: top10Calories.map(d => d.Item),
        text: top10Calories.map(d => d.Item),
        type: "bar",
        orientation: "h"
      }];
  
      let barLayout = {
        title: "Top 10 High Calorie Items",
        margin: { t: 30, l: 150 }
      };
  
      Plotly.newPlot("bar", barData, barLayout);
  
      let bubbleData = [{
        x: samples.map(d => d['Carbs (g)']),
        y: samples.map(d => d['Total Fat (g)']),
        text: samples.map(d => d.Item),
        mode: "markers",
        marker: {
          size: samples.map(d => d.Calories),
          color: samples.map(d => d.Calories),
          colorscale: "Earth"
        }
      }];
  
      let bubbleLayout = {
        title: "Nutrition Overview",
        margin: { t: 30 },
        hovermode: "closest",
        xaxis: { title: "Carbs (g)" },
        yaxis: { title: "Total Fat (g)" }
      };
  
      Plotly.newPlot("bubble", bubbleData, bubbleLayout);
    });
  }
  
  // Initialize the dashboard
  function init() {
    d3.json("/data").then((data) => {
      let sampleNames = Array.from(new Set(data.map(d => d.Company)));
      let selector = d3.select("#selDataset");
  
      sampleNames.forEach((sample) => {
        selector.append("option").text(sample).property("value", sample);
      });
  
      let firstSample = sampleNames[0];
      buildCharts(firstSample);
  
      let itemSelector = d3.select("#selItem");
      let items = data.filter(d => d.Company === firstSample).map(d => d.Item);
  
      items.forEach((item) => {
        itemSelector.append("option").text(item).property("value", item);
      });
  
      let firstItem = items[0];
      buildMetadata(firstItem);
    });
  }
  
  // Event listener for restaurant selection
  function optionChanged(newSample) {
    buildCharts(newSample);
  
    d3.json("/data").then((data) => {
      let itemSelector = d3.select("#selItem");
      itemSelector.html("");
      let items = data.filter(d => d.Company === newSample).map(d => d.Item);
  
      items.forEach((item) => {
        itemSelector.append("option").text(item).property("value", item);
      });
  
      let firstItem = items[0];
      buildMetadata(firstItem);
    });
  }
  
  // Event listener for item selection
  function itemChanged(newItem) {
    buildMetadata(newItem);
  }
  
  init();
