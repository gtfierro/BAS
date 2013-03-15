jQuery(function($) {
  // don't actually submit the form
  $('form').submit(function(e) {
    e.preventDefault();
    return false;
  });

  var selected = [];
  var editor = ace.edit("editor");
  editor.setTheme("ace/theme/solarized_light");
  editor.getSession().setMode("ace/mode/python");
  editor.getSession().setUseWrapMode(true);
  editor.setValue('# the object \'bas\' refers to the currently selected objects\n');
  document.getElementById('editor').style.fontSize='10px';
  editor.clearSelection(); // start off not highlighting text
  $('#q').focus();


  // only make AJAX calls every 250ms
  $('#q').on('keyup', $.debounce(500, false, function() {
    selected = []; // clear out the list of selected UUIDs
    $('#actuation-candidates li').remove();
    $('#command-results li').remove();
    if ($(this).text() == '') {
      $('.results td').remove();
      $('#svgstuff div').remove();
      $('#svgstuff h5').remove();
    }

    var query = $(this).serialize();

    // URL-encode form field
    var url = 'query.html?' + query;
    var geourl = 'query?q=%21%20>%20' + query.slice(2); // remove 'q='

    if (query === '') { return; }

    // load the results into the results <div>
    $('#results').addClass('loading').load(url, function(response, status, xhr) {
        $(this).removeClass('loading');
    });

    $.getJSON(geourl, function(results) {
      var $svgstuff = $('#svgstuff'); // cache the target <div>
      $svgstuff.html(''); // clear container

      var floors = [];
      if (results === 'none') { $('#svgstuff').addClass('empty'); return; }
      else { $('#svgstuff').removeClass('empty'); }
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

    $('#actuation-candidates li').each(function() {
      uuids.push($(this).attr('id'));
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
      $('.area').each(function(i) {
         $(this).attr('class', $(this).attr('class').substr(0,18));
      });
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

  $('#results').on('click', 'tr', function(e) {
    if (e.shiftKey) {
        var uuid = $(this).find('a.uuid').text();
        if ($.inArray(uuid, selected) > -1) {
          selected.splice(selected.indexOf(uuid), 1);
          $(this).find('td').removeClass('shift-click');
          $('#actuation-candidates').find('#'+uuid).remove();
        } else {
          selected.push(uuid);
          $('#actuation-candidates').append($('<li>').text(uuid.substr(0,5)).attr('id',uuid));
          $(this).find('td').addClass('shift-click');
        }
    }
  });

  $('#select-all').click(function(e) {
    $('#results tr').each(function(i) {
      var uuid = $(this).find('a.uuid').text();
      selected.push(uuid);
      $('#actuation-candidates').append($('<li>').text(uuid.substr(0,5)).attr('id',uuid));
      $(this).find('td').addClass('shift-click');
    });
  });

  $('#clear').click(function(e) {
    $('#results tr').each(function(i) {
      var uuid = $(this).find('a.uuid').text();
      selected.splice(selected.indexOf(uuid), 1);
      $(this).find('td').removeClass('shift-click');
      $('#actuation-candidates').find('#'+uuid).remove();
    });
  });

  $('.close').click(function(e) {
    $('.alert').hide();
  });
});
