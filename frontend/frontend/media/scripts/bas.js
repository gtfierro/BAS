jQuery(function($) {
  var yourStartLatLng = new google.maps.LatLng(37.870218, -122.259481);
  $('#map_canvas').gmap({'center': yourStartLatLng, 'zoom': 16});

  $('#map_canvas').on('click', function(e) {
    console.log(e);
  });
});

