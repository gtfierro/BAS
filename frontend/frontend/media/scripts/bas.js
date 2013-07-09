jQuery(function($) {

  console.log('hi');
  var map = Kartograph.map('#map', 600, 400);
  map.loadMap('/static/map.svg', function(){;
    console.log('map loaded?');
  });

});

