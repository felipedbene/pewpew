var map = new Datamap({

  scope: 'world',
  element: document.getElementById('container1'),
  setProjection: function(element) {
    var projection = d3.geo.mercator()
      .center([-100, 25])
      .rotate([4.4, 0])
      .scale(1000)
      .translate([element.offsetWidth / 2, element.offsetHeight / 2]);
    var path = d3.geo.path()
      .projection(projection);

    return {path: path, projection: projection};
  },
  // change the projection to something else only if you have absolutely no cartographic sense

  fills: {
    defaultFill: 'black',
  },

  geographyConfig: {
    dataUrl: null,
    hideAntarctica: false,
    borderWidth: 3,
    borderColor: '#079a9a',
    popupTemplate: function(geography, data) {
      return '<div class="hoverinfo" style="color:white;background:black">' +
        geography.properties.name + '</div>';
    },
    popupOnHover: true,
    highlightOnHover: true,
    highlightFillColor: '#33ac1a',
    highlightBorderColor: '#33ac1a',
    highlightBorderWidth: 3
  },

})
