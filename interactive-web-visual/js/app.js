function buildMetaData(sample) {
    d3.json("https://raw.githubusercontent.com/Ryndine/interactive-web-visual/main/data/samples.json").then((data) => {
      var metadata = data.metadata;
      console.log(metadata);

    var buildArray = metadata.filter(sampleObj => sampleObj.id == sample);
    var result = buildArray[0];
    var panelData = d3.select("#sample-metadata");

    panelData.html("");

    Object.entries(result).forEach(([key, value]) => {
      panelData.append("h6").text(`${key.toUpperCase()}: ${value}`);
    });
  });
}

function buildCharts(sample) {
    d3.json("https://raw.githubusercontent.com/Ryndine/interactive-web-visual/main/data/samples.json").then((data) => {
      var sampleData = data.samples;
      var buildArray = sampleData.filter(sampleObj => sampleObj.id == sample);
      var result = buildArray[0];
  
      var otu_ids = result.otu_ids;
      var otu_labels = result.otu_labels;
      var sample_values = result.sample_values;

    var bubbleChart = {
        title: "Bacteria Cultures Per Sample",
        hovermode: "closest",
        xaxis: { title: "OTU ID" },
      };
      var bubbleData = [
        {
          x: otu_ids,
          y: sample_values,
          text: otu_labels,
          mode: "markers",
          marker: {
            size: sample_values,
            color: otu_ids,
            colorscale: "Earth"
          }
        }
      ];
  
      Plotly.newPlot("bubble", bubbleData, bubbleChart);
      
      var yticks = otu_ids.slice(0, 10).map(otuID => `OTU ${otuID}`).reverse();
      var barData = [
        {
          y: yticks,
          x: sample_values.slice(0, 10).reverse(),
          text: otu_labels.slice(0, 10).reverse(),
          type: "bar",
          orientation: "h",
        }
      ];
  
      var chartLayout = {
        title: "Top 10 Bacteria Cultures Found",
        margin: { t: 30, l: 150 }
      };
  
      Plotly.newPlot("bar", barData, chartLayout);
    });
  };

  function init() {
    var selectDropdown = d3.select("#selDataset");
  
    d3.json("https://raw.githubusercontent.com/Ryndine/interactive-web-visual/main/data/samples.json").then((data) => {
      var name = data.names;
  
      name.forEach((sample) => {
        selectDropdown
          .append("option")
          .text(sample)
          .property("value", sample);
      })
  
      var sampleData = name[0];
      buildCharts(sampleData);
      buildMetaData(sampleData);
    });
  };
  
  function optionChanged(newSample) {
    buildCharts(newSample);
    buildMetaData(newSample);
  };

init()
