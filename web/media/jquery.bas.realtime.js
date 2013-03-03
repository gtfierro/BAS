jQuery(function($) {
  // don't actually submit the form
  $('form').submit(function(e) {
    e.preventDefault();
    return false;
  });

  // only make AJAX calls every 250ms
  $('#q').on('keyup', $.debounce(250, false, function(e) {
    var url = 'query';
    var geourl = url;
    
    if ($('#format').val() === 'HTML') {
      url += '.html';
    }
      
    var query = $(this).serialize();

    // URL-encode form field
    url += '?' + query;
    geourl += '?q=%21%20>%20' + query.slice(2); // remove 'q='

    // load the results into the results <div>
    $('#results').addClass('loading').load(url, function() {
      $(this).removeClass('loading');
    });

    $.getJSON(geourl, function(results) {
      var $svgstuff = $('#svgstuff'); // cache the target <div>
      $svgstuff.html(''); // clear container
      
      var floors = [];
      $.each(results, function(i, result) {
        var building = result['building'];
        var floor = result['floor'];
        
        if ($.inArray(floor, floors) > -1) {
          return true; // continue
        }

        floors.push(floor);

        var floorID = floor.toLowerCase().replace(' ', '-');

        $('<h5>' + floor + '</h5><div id="' + floorID + '" class="svg"></div>').appendTo($svgstuff);

        $('#' + floorID).appstack({
          url: 'http://127.0.0.1:8000',
          building: building,
          floors: [floor],
          all: false
        });
      });
    });
  }));

  $('#run').on('click', function(e) {
    var uuids = [];
    var url = 'uuid/';

    var command = $("#c").serialize().slice(2).trim();

    $('#results a.uuid').each(function() {
      uuids.push($(this).text());
    });

    for (var i = 0; i < uuids.length; i++) {
      $('#details').load(url + uuids[i] + "/" + command);
    }
  });

  $('.results').on('click', 'a.floorplan', function(e) {
    e.preventDefault();
    var url = $(this).attr('href');
    $('#modal-results').attr('src', encodeURI(url.trim())).parents('.modal').modal('show');
  });

  $('.results').on('click', 'a.uuid', function(e) {
    e.preventDefault();
    var url = $(this).attr('href');
    $('#details').load(url);
  });

  // dumb edge-case
  $('#format').change(function() {
    $('#q').keyup();
  });

  $('#all-buildings').on('click', function(e) {
    e.preventDefault();
    $('#q').val('!').keyup(); // trigger AJAX programatically
  });

  $('#all').on('click', function(e) {
    e.preventDefault();
    $('#q').val('.').keyup();
  });

  $('#georesults').on('click', 'a.all-objs-devices', function(e) {
    e.preventDefault();
    var url = $(this).attr('href');
    $('#q').val(decodeURI(url.trim()).slice(21)).keyup();
  });
});