// // comment this to stop reloading
// setInterval(function() {
//   window.location.reload();
// }, 15 * 60 * 1000); // reloads page every 15 minutes

window.onload = function() {
  var getjson = function(jsonUrl) {
    var defer = $.Deferred();
    d3.json(jsonUrl, function(error, rows) {
      if (error) {
        defer.reject(error);
      }
      defer.resolve(rows);
    });
    return defer.promise();
  };

  $.when(
    getjson("XML/TopCategory.json"),
    getjson("XML/TopCountries.json"),
    // getjson("XML/TotalAttacks.txt"),
    getjson("XML/result.json")
  ).done(function(res1, res2, res3) {
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
        dataPoints: res1
      }]
    };
    var bar = {
      backgroundColor: "transparent",
      theme: "dark2",
      animationEnabled: true,

      title: {
        text: "Países que más nos atacan"
      },
      axisX: {
        reversed: true,
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
        dataPoints: res2
      }]
    };
    $(".bot.left").CanvasJSChart(pie);
    $(".bot.mid").CanvasJSChart(bar);
    document.getElementById('pais').innerText = bar.data[0].dataPoints[0].label;
    document.getElementById('counter').innerText = res3.total;
  }).fail(function(err) {
    console.log(err);
  });


}
