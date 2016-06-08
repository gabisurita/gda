function boxplot(yData, xdt , location, title_default,title_custom) {

  var d3 = Plotly.d3;

  var WIDTH_IN_PERCENT_OF_PARENT = 100,
  HEIGHT_IN_PERCENT_OF_PARENT = 60;

  var gd3 = d3.select(location)
  .append('div')
  .style({
    width: WIDTH_IN_PERCENT_OF_PARENT + '%',
    'margin-left': (100 - WIDTH_IN_PERCENT_OF_PARENT) / 2 + '%',

    height: HEIGHT_IN_PERCENT_OF_PARENT + 'vh'
    //'margin-top': (100 - HEIGHT_IN_PERCENT_OF_PARENT) / 2 + 'vh'
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
        size: 2
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
    showlegend: false,
    marker: { size: 10, color: 'black', symbol: 'diamond'},
    type: 'scatter'
  };
  return trace;
}
