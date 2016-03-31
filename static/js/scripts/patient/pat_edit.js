require.config({
	baseUrl: '/site_static/js',
	paths: {
		'domReady': 'libs/domReady',
		'jquery': 'libs/jquery-1.8.3.min',
		'json': 'libs/jquery-plugin/jquery.json-2.3.min',
		'tmpl': 'libs/jquery-plugin/jquery.tmpl.min',
		'validate': 'libs/jquery-plugin/jquery-validate/jquery.validate',
		'gmap3': 'libs/gmap3.min',
		'autocomplete': 'libs/jquery-plugin/jquery-autocomplete.min',
		'datepicker': 'libs/jquery-plugin/bootstrap-datepicker/bootstrap-datepicker',
		'message': 'modules/common/message',
		'global': 'modules/common/global',
		'dropdown': 'utils/dropdown',
		'ajaxform': 'utils/ajaxform',
		'btnmask': 'utils/btnmask',
		'lightbox': 'utils/lightbox',
		'valuecheck': 'utils/valuecheck',
		'p_baseinfo': 'modules/patient/baseinfo'
	},
	shim: {
		'json': ['jquery'],
		'tmpl': ['jquery'],
		'validate': ['jquery'],
		'message': ['jquery'],
		'dropdown': ['jquery'],
		'global': ['message', 'dropdown'],
		'datepicker': ['jquery'],
		'p_baseinfo': ['datepicker','ajaxform'],
		'autocomplete': ['jquery','gmap3']
	}
});

require(
['jquery', 'p_baseinfo', 'gmap3', 'autocomplete', 'global', 'domReady!'],
function($, baseinfo){

	$( '#pat_pro' ).addClass('active');

	$( '.tab' ).click(function(){
		$( this ).addClass( 'active' ).siblings().removeClass( 'active' );
		$( '.content-inner' ).hide();
		$( '#'+$(this).data('target') ).show();
	});

	baseinfo.init();

	var toLatlng = function(latlng_str){
		if( latlng_str === undefined || latlng_str === '' ){
			return '';
		}else{
			var l = latlng_str.substring(1,latlng_str.indexOf(')') ).split(','),
			a = parseFloat(l[0]),
			b = parseFloat(l[1]);
			return [a,b]
		}
	}

	var gmap = $( '#gmap' ),
		marker_green = "http://maps.google.com/mapfiles/marker_green.png";

	var latlng_str = $('#latlng').val(),
		latlng = toLatlng(latlng_str);

	gmap.gmap3({
		map: {
			options: {
				center: latlng,
				zoom: 18
			}
		},
		marker: {
			latLng: latlng || 0,
			options: {
				draggable: true,
				icon: marker_green
			},
			events: {
				dragend: function(marker) {
					$('#latlng').val(marker.getPosition());
					$( this ).gmap3({
						getaddress: {
							latLng: marker.getPosition(),
							callback: function(results) {
								var addr = results && results[0] ? results && results[0].formatted_address : 'no address';
								$('#location').val(addr);
								var map = $(this).gmap3('get'),
									infowindow = $(this).gmap3({get:'infowindow'});

								if(infowindow) {
									infowindow.open(map, marker);
									infowindow.setContent(addr);
								} else {
									$(this).gmap3({
										infowindow: {
											anchor: marker,
											options: {content: addr}
										}
									});
								}
							}
						}
					});
				}
			}
		}
		
	});

	$( '#location' ).autocomplete({
		source : function() {
			gmap.gmap3({
				getaddress: {
					address: $(this).val(),
					callback: function(results){
					if (!results) return;
						$("#location").autocomplete("display", results, false);
					}
				} 
			});
		},
		cb : {
			cast : function(item) {
				return item.formatted_address;
			},
			select : function(item) {
				gmap.gmap3({
					clear: "marker",
					marker: {
						latLng: item.geometry.location,
						options: {
							draggable: true,
							icon: marker_green
						},
						events: {
							dragend: function(marker) {
								$('#latlng').val(marker.getPosition());
								$( this ).gmap3({
									getaddress: {
										latLng: marker.getPosition(),
										callback: function(results) {
											var addr = results && results[0] ? results && results[0].formatted_address : 'no address';
											$('#location').val(addr);
											var map = $(this).gmap3('get'),
												infowindow = $(this).gmap3({get:'infowindow'});

											if(infowindow) {
												infowindow.open(map, marker);
												infowindow.setContent(addr);
											} else {
												$(this).gmap3({
													infowindow: {
														anchor: marker,
														options: {content: addr}
													}
												});
											}
										}
									}
								});
							}
						}
					},
					map:{
						options: {
							center: item.geometry.location,
						}
					},
					getlatlng: {
						address: $('#location').val(),
						callback: function(results){
							var latlng = results[0].geometry.location.toString();
							$( 'input[name="latlng"]' ).val( latlng );
						}
					}
				});
			}
		}
	});
});