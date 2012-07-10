/* AppStack plugin for jQuery */

(function($) { //Hide scope, no $ conflict

  function AppstackManager() {
	this.building = null;
	this.floors = [];
	this.types = [];
  }

  $.extend(AppstackManager.prototype, {
	_attachAppstack: function(container, options) {
	  var $container = $(container);

	  var settings = $.extend({
		'url' : 'http://127.0.0.1:8000',
		'building' : null,
		'floors' : [],
		'types' : [],
		'onLoad' : function() {}
	  }, options);

	  if (settings.building === null) {
		throw 'No building name given';
	  }

	  this.building = settings.building;
	  this.floors = settings.floors;
	  this.types = settings.types;

	  var url = settings.url + '/smapgeo/geo.svg?' + $.param({
		'building': this.building,
	   	'floors': this.floors,
	   	'types': this.types});
	  $container.svg({loadURL: url, onLoad: settings.onLoad});
	},

	_floorAppstack: function(container, floor_name) {
	  var $container = $(container);
	  if (floor_name == undefined) {
		return $container.find('g').filter(function(){return $(this).attr('inkscape:label') !== undefined;});
	  } else {
		return $container.find('g').filter(function(){return $(this).attr('inkscape:label')==floor_name;});
	  }
	},

	_areaAppstack: function(container, area_name) {
	  var $container = $(container);
	  if (area_name == undefined) {
		return $container.find('title').parent('path');
	  } else {
		return $container.find('title').filter(function(){return $(this).text() == area_name;}).parent();
	  }
	},

	_nameAppstack: function(container) {
	  var $container = $(container)
	  if ($container.is('g')) {
		// We have a floor
		return $container.attr('inkscape:label');
	  } else if ($container.is('path')) {
		// We have an area
		return $container.children('title').text();
	  } else {
		return undefined;
	  }
	},

	_area_nameAppstack: function(container) {
	  var $container = $(container)
	  if ($container.is('path')) {
		return $container.children('title').text();
	  } else {
		return undefined;
	  }
	},

	_floor_nameAppstack: function(container) {
	  var $container = $(container)
	  if ($container.is('g')) {
		// We have a floor
		return $container.attr('inkscape:label');
	  } else if ($container.is('path')) {
		// We have an area
		return $container.parent('g').attr('inkscape:label');
	  } else {
		return undefined;
	  }
	},

	_building_nameAppstack: function(container) {
	  var $container = $(container)
	  if ($container.is('g')) {
		// We have a floor
		return $container.parent('svg').children('title').text();
	  } else if ($container.is('path')) {
		// We have an area
		return $container.parent('g').parent('svg').children('title').text();
	  } else if ($container.is('svg')){
		return $container.children('title').text();
	  } else {
		return undefined;
	  }
	},

  })

  $.fn.appstack = function(options) {
	var otherArgs = Array.prototype.slice.call(arguments, 1);
	if (typeof options == 'string') {
	  return $.appstack['_' + options + 'Appstack'].apply($.appstack, [this[0]].concat(otherArgs));
	}
	return this.each(function() {
		$.appstack._attachAppstack(this, options);
	});
  }

  $.appstack = new AppstackManager();

})(jQuery);