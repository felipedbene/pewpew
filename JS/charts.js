window.onload = function() {

  var pie = {
    title: {
      text: "Website Traffic Source"
    },
    data: [{
      type: "pie",
      startAngle: 45,
      showInLegend: "true",
      legendText: "{label}",
      indexLabel: "{label} ({y})",
      yValueFormatString: "#,##0.#" % "",
      dataPoints: [{
          label: "Organic",
          y: 36
        },
        {
          label: "Email Marketing",
          y: 31
        },
        {
          label: "Referrals",
          y: 7
        },
        {
          label: "Twitter",
          y: 7
        },
        {
          label: "Facebook",
          y: 6
        },
        {
          label: "Google",
          y: 10
        },
        {
          label: "Others",
          y: 3
        }
      ]
    }]
  };
  var bar = {
    animationEnabled: true,

    title: {
      text: "Fortune 500 Companies by Country"
    },
    axisX: {
      interval: 1
    },
    axisY2: {
      interlacedColor: "rgba(1,77,101,.2)",
      gridColor: "rgba(1,77,101,.1)",
      title: "Number of Companies"
    },
    data: [{
      type: "bar",
      name: "companies",
      axisYType: "secondary",
      color: "#014D65",
      dataPoints: [{
          y: 3,
          label: "Sweden"
        },
        {
          y: 7,
          label: "Taiwan"
        },
        {
          y: 5,
          label: "Russia"
        },
        {
          y: 9,
          label: "Spain"
        },
        {
          y: 7,
          label: "Brazil"
        },
        {
          y: 7,
          label: "India"
        },
        {
          y: 9,
          label: "Italy"
        },
        {
          y: 8,
          label: "Australia"
        },
        {
          y: 11,
          label: "Canada"
        },
        {
          y: 15,
          label: "South Korea"
        },
        {
          y: 12,
          label: "Netherlands"
        },
        {
          y: 15,
          label: "Switzerland"
        },
        {
          y: 25,
          label: "Britain"
        },
        {
          y: 28,
          label: "Germany"
        },
        {
          y: 29,
          label: "France"
        },
        {
          y: 52,
          label: "Japan"
        },
        {
          y: 103,
          label: "China"
        },
        {
          y: 134,
          label: "US"
        }
      ]
    }]
  };
  $(".bot.left").CanvasJSChart(pie);
  $(".bot.mid").CanvasJSChart(bar);

}
