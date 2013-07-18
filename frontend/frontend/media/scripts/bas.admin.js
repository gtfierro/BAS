// hacky fix to allow outside libraries in this namespace
var $ = django.jQuery;
var jQuery = django.jQuery;
(function($) {
  $('#id_floor').live('change', function() {
    // get floor from dropdown
    var id_floor = $('#id_floor').val();
    //$('#id_buildings').css({'background-color':'#fff','filter':'alpha(opacity=50)','opacity':0.5});
    // hide the other floors
    var floorobj
    $('.floorplan').each(function() {
      console.log(this.id);
      console.log(id_floor);
      if (this.id != 'floorplan_'+id_floor) {
        $(this).hide();
      } else {
        $(this).show();
        floorobj = this;
      }
    });
    
    console.log($(floorobj));
    
    // on clicking the image, get image coordinates
    $(floorobj).click( function(e) {
        var offset = $(this).offset();
        console.log(e.clientX - offset.left);
        console.log(e.clientY - offset.top);
        return true;
    });
    return false;
  });
}(django.jQuery));
