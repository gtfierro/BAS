/* AppStack plugin for jQuery */

(function($) { //Hide scope, no $ conflict

  //////////////////////////////// Geo display via SVG ////////////////////////////////

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

	_isAppstack: function(container, type) {
	  var $container = $(container);
	  if ($container.is('svg') && type === 'building'){
		return true;
	  } else if ($container.is('g') && type === 'floor') {
		return true;
	  } else if ($container.is('path')  && type === 'area') {
		return true;
	  } else {
		return false;
	  }
	},

	_nameAppstack: function(container) {
	  var $container = $(container)
	  if ($container.appstack('is', 'floor')) {
		return $container.attr('inkscape:label');
	  } else if ($container.appstack('is', 'area')) {
		return $container.children('title').text();
	  } else {
		return undefined;
	  }
	},

	_area_nameAppstack: function(container) {
	  var $container = $(container)
	  if ($container.appstack('is', 'area')) {
		return $container.children('title').text();
	  } else {
		return undefined;
	  }
	},

	_floor_nameAppstack: function(container) {
	  var $container = $(container)
	  if ($container.appstack('is', 'floor')) {
		return $container.attr('inkscape:label');
	  } else if ($container.appstack('is', 'area')) {
		return $container.parent('g').attr('inkscape:label');
	  } else {
		return undefined;
	  }
	},

	_building_nameAppstack: function(container) {
	  var $container = $(container)
	  if ($container.appstack('is', 'building')) {
		return $container.children('title').text();
	  } else if ($container.appstack('is', 'floor')) {
		return $container.parent('svg').children('title').text();
	  } else if ($container.appstack('is', 'area')) {
		return $container.parent('g').parent('svg').children('title').text();
	  } else {
		return undefined;
	  }
	},

	_queryAppstack: function(container) {
	  var $container = $(container)
	  if ($container.appstack('is', 'building')) {
		return '!' + $container.appstack('building_name')
	  } else if ($container.appstack('is', 'floor')) {
		return '!' + $container.appstack('floor_name')  + '<!' + $container.appstack('building_name')
	  } else if ($container.appstack('is', 'area')) {
		return '!' + $container.appstack('area_name') + '<!' + $container.appstack('floor_name')  + '<!' + $container.appstack('building_name')
	  } else {
		return undefined;
	  }

	},

	_devicesAppstack: function(container, callback) {
	  var $container = $(container)
	  var query = $container.appstack('query');
	  if (query === undefined) {
		return undefined;
	  }
	  query = '. < ' + query;
	  $.q(query, callback);
	  return $container;
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

  //////////////////////////////// Queries ////////////////////////////////


  var appQuery = function( query, fn ) {
	if (typeof query === "object") {
	  return new appQuery.fn.init( query )
	} else if (typeof query === "string" && typeof fn === "function") {
	  $.ajax(appQuery.settings.url + "/webapi/query?" + $.param({'q': query}),
			 {
			 }).done( function ( data ) {
			   fn( new appQuery.fn.init( data ));
			 });
	  return undefined;
	} else {
	  throw "Invalid arguments";
	}
  }

  appQuery.settings = {
	url: "http://127.0.0.1:8000"
  }

  appQuery.fn = appQuery.prototype = {
	constructor: appQuery,
	init: function( objs ) {
	  if ($.isArray(objs)) {
		this.objects = objs;
	  } else {
		this.objects = [objs];
	  }
	  return this;
	},

	setup: function( settings ) {
	  $.extend( appQuery.settings, settings );
	},

	each: function( fn ) {
	  $.each(this.objects, function(i, dev){
		fn(i, appQuery(dev));
	  });
	  return this;
	},

	filter: function( type ) {
	  var keyword = type.slice(0, 1);
	  var match = type.slice(1);
	  if (keyword === '!') {
		this.objects = this.objects.filter( function(obj) {
		  if ( obj.type === 'Area' || obj.type === 'Floor' || obj.type === 'Building') {
			if ( obj.name.search(match) !== -1 ) {
			  return true;
			}
		  }
		  return false;
		});
		return this;
	  } else if (keyword === '.') {
		keyword = 'type';
	  } else if (keyword === '^') {
		keyword = 'uuid';
	  } else if (keyword === '$') {
		keyword = 'name';
	  } else {
		this.objects = [];
		return this;
	  }
	  this.objects = this.objects.filter( function(obj) { return obj[keyword] === match; });
	  return this;
	},

	call: function( method ) {
	  var param;
	  var args = Array.prototype.slice.call(arguments, 1);
	  var callback = function(obj, response) {};
	  if (typeof args.slice(-1)[0] === "function") {
		callback = args.slice(-1)[0];
		args = args.slice(0, -1);
	  }

	  if (args.length === 1 && typeof args[0] === "object") {
		param = $.param(args[0]);
	  } else {
		param = "";
		for (var i = 0, j = args.length; i < j; i++) {
		  param += "," + JSON.stringify(args[i]);
		}
		param = param.slice(1);
	  }
	  $.each(this.objects, function(i, obj) {
		if (obj.hasOwnProperty("methods") && obj.methods.hasOwnProperty(method)) {
		  var url = appQuery.settings.url + "/webapi/uuid/" + obj.uuid + "/" + method + "?" + param;
		  $.ajax(url, {}).done( function( data ) {
			callback(obj, data);
		  });
		}
	  });
	},

	get: function( s ) {
	  if (s === 'uuid') {
		return this.objects[0].uuid;
	  } else if (s === 'name') {
		return this.objects[0].name;
	  } else if (s === 'type') {
		return this.objects[0].type;
	  } else if (s === 'methods') {
		return this.objects[0].methods;
	  }
	}
  }

  appQuery.fn.init.prototype = appQuery.prototype;

  $.q = appQuery;

})(jQuery);