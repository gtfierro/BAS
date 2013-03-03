jQuery(function($) {
  // don't actually submit the form
  $('form').submit(function(e) {
    e.preventDefault();
    return false;
  });

  // only make AJAX calls every 250ms
  $('#q').on('keyup', $.debounce(250, false, function(e) {
    var url = 'query';
    
    if ($('#format').val() === 'HTML') {
      url += '.html';
    }
      
    var query = $(this).serialize();
    var geourl = url;

    // URL-encode form field
    url += '?' + query;
    geourl += '?q=%21%20>%20' + query.slice(2);

    // load the results into the results <div>
    $('#results').addClass('loading').load(url, function() {
      $(this).removeClass('loading');
    });

    $('#georesults').addClass('loading').load(geourl, function() {
      $(this).removeClass('loading');
    });


    var floors = [];
    $('#georesults tr').each(function() {
      var building = $(this).find('a.building').text();
      var floorfull = $(this).find('a.floor').text();
      
      if ($.inArray(floorfull, floors) > -1) {
        return;
      } else {
        floors.push(floorfull);
      }
      var floor = floorfull.replace(' ', '');
      var div = $('<h5>' + floor + '</h5><div class="svg"></div>').attr('id', floor);

      $('#' + floor).appstack({
        url: 'http://127.0.0.1:8000',
        building: building,
        floors: [floorfull],
        all: false
      });

      $('#svgstuff').append(div);
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
      $('#details').load(url+uuids[i]+"/"+command);
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