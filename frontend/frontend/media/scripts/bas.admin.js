// hacky fix to allow outside libraries in this namespace
var $ = django.jQuery;
var jQuery = django.jQuery;
(function($) {
  var floorplanid = '';
  var canvascontext = '';
  $('#id_floor').live('change', function() {
    // get floor from dropdown
    var id_floor = $('#id_floor').val();
    //$('#id_buildings').css({'background-color':'#fff','filter':'alpha(opacity=50)','opacity':0.5});
    // hide the other floors
    var floorobj
    $('.floorplan').each(function() {
      floorplanid = 'floorplan_'+id_floor;
      console.log(this.id);
      console.log(id_floor);
      if (this.id != floorplanid) {
        $(this).hide();
      } else {
        $(this).show();
        canvascontext = this.getContext('2d');
        floorobj = this;
      }
    });
    
    // on clicking the image, get image coordinates
    xcoords = new Array();;
    ycoords = new Array();;
    $(floorobj).click( function(e) {
        console.log('canvas?');
        console.log($(this)[0]);
        var ctx = $(this)[0].getContext('2d');
        var offset = $(this).offset();
        console.log(offset);
        var xcoord = e.pageX - offset.left;
        var ycoord = e.pageY - offset.top;
        console.log(xcoord);
        console.log(ycoord);
        ctx.rect(xcoord, ycoord, 8, 8);
        ctx.fillStyle = 'red';
        ctx.fill()
        xcoords.push( xcoord );
        ycoords.push( ycoord );
        if (xcoords.length >= 2) {
            ctx.lineWidth = 5;
            ctx.beginPath();
            ctx.moveTo(xcoords[xcoords.length-2], ycoords[ycoords.length-2]);
            ctx.lineTo(xcoords[xcoords.length-1], ycoords[ycoords.length-1]);
            ctx.strokeStyle = 'red';
            ctx.closePath();
            ctx.stroke();
        }
        $('#id_coordinates').val(xcoords.toString() + ycoords.toString());
        return true;
    });
    return false;
  });

}(django.jQuery));
