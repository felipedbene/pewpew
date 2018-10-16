function readTextFile(file, callback) {
  var rawFile = new XMLHttpRequest();
  rawFile.overrideMimeType("application/json");
  rawFile.open("GET", file, true);
  rawFile.onreadystatechange = function() {
    if (rawFile.readyState === 4 && rawFile.status == "200") {
      callback(rawFile.responseText);
    } else {
      $('#attackdiv').html('<h1 style="color:red;font-size:1em">No file found</h1>')
      setTimeout(function() {
        location.reload();
      }, 1500000);
    }
  }
  rawFile.onerror = function(msg) {
    $('#attackdiv').html('<h1 style="color:red;font-size:1em">' + msg + '</h1>')
    setTimeout(function() {
      location.reload();
    }, 1500000);
  }
  rawFile.upload.onerror = function(msg) {
    $('#attackdiv').html('<h1 style="color:red;font-size:1em">' + msg + '</h1>')
    setTimeout(function() {
      location.reload();
    }, 1500000);
  }

  rawFile.send(null);
}

window.onload = function() {

  var pie = {
    backgroundColor: "transparent",
    theme: "dark2",
    title: {
      text: "Severidad de ataques bloqueados"
    },
    data: [{
      type: "pie",
      startAngle: 45,
      showInLegend: "true",
      legendText: "{label}",
      indexLabel: "{label} ({y})",
      yValueFormatString: "#,##0.#" % "",
      dataPoints: [{
          "color": "#f48154",
          "y": 49
        },
        {
          "color": "#ff4660",
          "y": 6
        },
        {
          "color": "#d9ff7f",
          "y": 4
        }
      ]

    }]
  };
  var bar = {
    backgroundColor: "transparent",
    theme: "dark2",
    animationEnabled: true,

    title: {
      text: "Países con mayor número de ataques"
    },
    axisX: {
      interval: 1
    },
    axisY2: {
      interlacedColor: "rgba(1,77,101,.2)",
      gridColor: "rgba(1,77,101,.1)",
    },
    data: [{
      type: "bar",
      name: "companies",
      axisYType: "secondary",
      color: "#014D65",
      dataPoints: [{
          "label": "China",
          "y": 21
        },
        {
          "label": "Mexico",
          "y": 13
        },
        {
          "label": "Viet Nam",
          "y": 10
        },
        {
          "label": "India",
          "y": 5
        },
        {
          "label": "United States",
          "y": 4
        },
        {
          "label": "Russian Federation",
          "y": 3
        },
        {
          "label": "France",
          "y": 2
        },
        {
          "label": "Turkey",
          "y": 1
        }
      ]

    }]
  };
  $(".bot.left").CanvasJSChart(pie);
  $(".bot.mid").CanvasJSChart(bar);

}
