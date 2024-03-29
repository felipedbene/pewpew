var map = new Datamap({

  scope: 'world',
  element: document.getElementById('container1'),
  projection: 'mercator',
  // change the projection to something else only if you have absolutely no cartographic sense

  fills: {
    defaultFill: 'black',
  },

  geographyConfig: {
    dataUrl: null,
    hideAntarctica: false,
    borderWidth: 2,
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
