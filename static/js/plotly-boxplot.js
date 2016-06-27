function boxplot(yData, xdt , location, title_default,title_custom) {

  var d3 = Plotly.d3;

  var WIDTH_IN_PERCENT_OF_PARENT = 100,
  HEIGHT_IN_PERCENT_OF_PARENT = 50;

  var gd3 = d3.select(location)
  .append('div')
  .style({
    width: WIDTH_IN_PERCENT_OF_PARENT + '%',
    'margin-left': (100 - WIDTH_IN_PERCENT_OF_PARENT) / 2 + '%',

    height: HEIGHT_IN_PERCENT_OF_PARENT + 'vh',
    //'margin-top': (100 - HEIGHT_IN_PERCENT_OF_PARENT) / 2 + 'vh',
  });

  var gd = gd3.node();

  var xData = ['A', 'B', 'C', 'D', 'E', 'F'];
  var data = [];
  var plot_color = ["#2196f3", "#2196f3", "#2196f3", "#2196f3", "#2196f3", "#2196f3"];
  for ( var i = 0; i < xData.length; i ++ ) {
    var result = {
      type: 'box',
      showlegend: false,
      y: yData[i],
      name: xData[i],
      boxpoints: 'all',
      jitter: 0.3,
      whiskerwidth: 0.2,
      fillcolor: 'white',
      marker: {
        color: plot_color[i],
        size: 3
      },
      line: {
        width: 2
      }
    };
    data.push(result);
  };

  var layout = {
    yaxis: {
      autorange: true,
      showgrid: true,
      zeroline: false,
      dtick: 5,
      gridcolor: 'rgb(255, 255, 255)',
      gridwidth: 1
    },
    xaxis: {
      color: 'black'
    },
    margin: {
      l: 40,
      r: 30,
      b: 30,
      t: 10
    },
    legend: {
      x: 1,
      y: 1.05,
      //yanchor: 'middle',
      traceorder: 'normal',
      //tracegroupgap: 100,
      font: {
        family: 'sans-serif',
        size: 14,
        color: '#2196f3'
      },
    }
    //  paper_bgcolor: 'rgb(243, 243, 243)',
    //  plot_bgcolor: 'rgb(243, 243, 243)',
    //  width: 700,
    //  height: 500,
    //  showlegend: true
  };

  Plotly.plot(gd, data, layout, {displaylogo: false, displayModeBar: false});

  var rating = [1,2,3,4,5,6];
  jQuery( ".clickable-row" )
  .mouseover(function() {
    rating[0] = jQuery( this ).find( "#q1" ).text();
    rating[1] = jQuery( this ).find( "#q2" ).text();
    rating[2] = jQuery( this ).find( "#q3" ).text();
    rating[3] = jQuery( this ).find( "#q4" ).text();
    rating[4] = jQuery( this ).find( "#q5" ).text();
    rating[5] = jQuery( this ).find( "#q6" ).text();
    var title_customized = jQuery( this ).find(title_custom[0]).text();
    var arrayLength = title_custom.length;
    for (var i = 1; i < arrayLength; i++) {
      title_customized = title_customized + " - " + jQuery( this ).find(title_custom[i]).text();
    }
    jQuery("#graph_title").find("span").text(title_customized);
    Plotly.addTraces(gd, scatter_trace(rating));
  })
  .mouseout(function() {
    Plotly.deleteTraces(gd,[-1]);
    jQuery("#graph_title").find("span").text(title_default);
  });

  if(xdt){
    Plotly.addTraces(gd, scatter_trace(xdt));
  }

  window.onresize = function() {
    Plotly.Plots.resize(gd);
  };
}

function scatter_trace(yData){
  var xData = ['A', 'B', 'C', 'D', 'E', 'F'];
  var trace = {
    x: xData,
    y: yData,
    mode: 'markers',
    name: ' ',
    showlegend: false,
    marker: { size: 10, color: 'black', symbol: 'diamond'},
    type: 'scatter'
  };
  return trace;
}

function explainplot(location) {

  var yData = [88, 86, 76, 89, 92, 96, 99, 94, 84, 86, 99, 93, 83, 88, 94, 91, 80, 74, 94, 90, 84, 89, 90,
     83, 88, 89, 93, 84, 94, 81, 85, 99, 95, 88, 76, 91, 92, 95, 86, 90, 96, 94, 88, 91, 96, 83, 91, 97, 87,
     91, 79, 82, 91, 96, 94, 85, 73, 94, 95, 92, 82, 86, 85, 97, 91, 87, 89, 96, 76, 94, 99, 94, 92, 92, 85,
     94, 93, 98, 90, 84, 91, 97, 94, 93, 88, 92, 95, 91, 90, 91, 99, 95, 88, 90, 93, 84, 88, 86, 93];

  var data = [{
    type: 'box',
    showlegend: false,
    y: yData,
    boxpoints: 'all',
    jitter: 0.5,
    pointpos: -1.8,
    whiskerwidth: 0.8,
    fillcolor: 'white',
    marker: {
      color: '#2196f3',
      size: 4
    },
    line: {
      width: 2
    }
  }];

  var layout = {
    yaxis: {
      autorange: true,
      showgrid: true,
      zeroline: false,
      dtick: 5,
      gridcolor: 'rgb(255, 255, 255)',
      gridwidth: 1
    },
    xaxis: {
      color: 'white '
    },
    margin: {
      l: 40,
      r: 30,
      b: 30,
      t: 10
    },
    annotations: [
    {
      y: 99,
      yref: 'y',
      text: 'máximo',
      showarrow: true,
      font: {
        family: 'Courier New, monospace',
        size: 16,
        color: '#ffffff'
      },
      align: 'center',
      arrowhead: 2,
      arrowsize: 1,
      arrowwidth: 2,
      arrowcolor: '#636363',
      ax: 20,
      ay: 0,
      bordercolor: '#c7c7c7',
      borderwidth: 2,
      borderpad: 4,
      bgcolor: '#2196f3',
      opacity: 0.8
    },
    {
      y: 94,
      yref: 'y',
      text: '75% dos valores até aqui%',
      showarrow: true,
      font: {
        family: 'Courier New, monospace',
        size: 16,
        color: '#ffffff'
      },
      align: 'center',
      arrowhead: 2,
      arrowsize: 1,
      arrowwidth: 2,
      arrowcolor: '#636363',
      ax: 20,
      ay: 0,
      bordercolor: '#c7c7c7',
      borderwidth: 2,
      borderpad: 4,
      bgcolor: '#2196f3',
      opacity: 0.8
    },
    {
      y: 91,
      yref: 'y',
      text: '50% dos valores até aqui',
      showarrow: true,
      font: {
        family: 'Courier New, monospace',
        size: 16,
        color: '#ffffff'
      },
      align: 'center',
      arrowhead: 2,
      arrowsize: 1,
      arrowwidth: 2,
      arrowcolor: '#636363',
      ax: 20,
      ay: 0,
      bordercolor: '#c7c7c7',
      borderwidth: 2,
      borderpad: 4,
      bgcolor: '#2196f3',
      opacity: 0.8
    },
    {
      y: 86,
      yref: 'y',
      text: '25% dos valores até aqui',
      showarrow: true,
      font: {
        family: 'Courier New, monospace',
        size: 16,
        color: '#ffffff'
      },
      align: 'center',
      arrowhead: 2,
      arrowsize: 1,
      arrowwidth: 2,
      arrowcolor: '#636363',
      ax: 20,
      ay: 0,
      bordercolor: '#c7c7c7',
      borderwidth: 2,
      borderpad: 4,
      bgcolor: '#2196f3',
      opacity: 0.8
    },
    {
      y: 73,
      yref: 'y',
      text: 'mínimo',
      showarrow: true,
      font: {
        family: 'Courier New, monospace',
        size: 16,
        color: '#ffffff'
      },
      align: 'center',
      arrowhead: 2,
      arrowsize: 1,
      arrowwidth: 2,
      arrowcolor: '#636363',
      ax: 20,
      ay: 0,
      bordercolor: '#c7c7c7',
      borderwidth: 2,
      borderpad: 4,
      bgcolor: '#2196f3',
      opacity: 0.8
    }
  ],
    legend: {
      x: 1,
      y: 1.05,
      //yanchor: 'middle',
      traceorder: 'normal',
      //tracegroupgap: 100,
      font: {
        family: 'sans-serif',
        size: 14,
        color: '#2196f3'
      },
    }
    //  paper_bgcolor: 'rgb(243, 243, 243)',
    //  plot_bgcolor: 'rgb(243, 243, 243)',
    //  width: 700,
    //  height: 500,
    //  showlegend: true
  };
  plotlocation = document.getElementById(location);
  Plotly.newPlot(plotlocation, data, layout, {displaylogo: false, displayModeBar: false});


}
