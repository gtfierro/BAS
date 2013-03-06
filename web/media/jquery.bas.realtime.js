jQuery(function($) {
  // don't actually submit the form
  $('form').submit(function(e) {
    e.preventDefault();
    return false;
  });

  // only make AJAX calls every 250ms
  $('#q').on('keyup', $.debounce(250, false, function() {
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

  function actuate(uuid, command) {
    $.ajax({
      url: 'uuid/'+uuid+'/'+command,
      success: function(data) {
        var $newelem = $('<li>');
        $newelem.html( uuid.substr(0,5) + ':' + data);
        $('#command-results').append($newelem);
      }
    });
  }

  $('#run').on('click', function(e) {
    var uuids = [];
    var command = $("#c").serialize().slice(2).trim();

    $('#results a.uuid').each(function() {
      uuids.push($(this).text());
    });

    for (var i = 0; i < uuids.length; i++) {
      actuate(uuids[i], command);
    }
  });

  $('.results').on('click', 'a.floorplan', function(e) {
    e.preventDefault();
    var url = $(this).attr('href');
    $('#modal-results').attr('src', encodeURI(url.trim())).parents('.modal').modal('show');
  }).on('click', 'a.uuid', function(e) {
    e.preventDefault();
    var url = $(this).attr('href');
    $('#details').load(url);
  });

  // dumb edge-cases
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

  $('.results').on('mouseenter', 'tr', function() {
    var uuid = $(this).find('a.uuid').text();
    var url = 'query?q=%21%20>%20^' + uuid;
    $('.area').each(function(i) {
       $(this).attr('class', $(this).attr('class').substr(0,18));
    });
    $.getJSON(url, function(results) {
      if (results === null) { return; }
      var floor = results[0]['floor'];
      var area = '';
      if (results[0]['type'] === 'Area') {
        area = results[0]['name'];
      }
      var building = results[0]['building'];
      var floorID = floor.replace(' ', '_');
      var areaID = area.replace(' ','_');
      var $areaelem = $('#'+floorID+"__"+areaID);
      var oldclass  = $areaelem.attr('class');
      $areaelem.attr('class',oldclass+" selected");
    });
  });

  $('.results').on('mouseleave', 'tr', function() {
    $('.area').each(function(i) {
       $(this).attr('class', $(this).attr('class').substr(0,18));
    });
  });

  $('#svgstuff').on('click', 'path', function() {
    var zoneid = $(this).attr('id').split('__');
    var floor = zoneid[0].replace('_',' ');
    var area = zoneid[1].replace('_',' ');
    var query = '. < !'+area+' < ! '+floor;
    $('#q').val(query).keyup();
  });
});
