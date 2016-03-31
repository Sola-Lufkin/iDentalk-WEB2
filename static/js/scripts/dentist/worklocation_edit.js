require.config({
	baseUrl: '/site_static/js',
	paths: {
		'domReady': 'libs/domReady',
		'jquery': 'libs/jquery-1.8.3.min',
		'json': 'libs/jquery-plugin/jquery.json-2.3.min',
		'tmpl': 'libs/jquery-plugin/jquery.tmpl.min',
		'validate': 'libs/jquery-plugin/jquery-validate/jquery.validate',
		'message': 'modules/common/message',
		'global': 'modules/common/global',
		'gmap3': 'libs/gmap3.min',
		'autocomplete': 'libs/jquery-plugin/jquery-autocomplete.min',
		'dropdown': 'utils/dropdown',
		'ajaxform': 'utils/ajaxform',
		'valuecheck': 'utils/valuecheck'
	},
	shim: {
		'json': ['jquery'],
		'tmpl': ['jquery'],
		'validate': ['jquery'],
		'message': ['jquery'],
		'global': ['message', 'dropdown'],
		'autocomplete': ['jquery', 'gmap3']
	}
});

require(
['jquery','gmap3','autocomplete','validate','ajaxform','global','domReady!'],
function($){

	$(function(){
		var marker_green = "http://maps.google.com/mapfiles/marker_green.png";

		$( '#content' ).remove();
		$( '#footer' ).remove();

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

		var gmap = $( '#gmap' );
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
						$( 'input[name="latlng"]' ).val( marker.getPosition() );
						$( this ).gmap3({
							getaddress: {
								latLng: marker.getPosition(),
								callback: function(results) {
									var addr = results && results[0] ? results && results[0].formatted_address : 'no address';
									var map = $(this).gmap3('get'),
										infowindow = $(this).gmap3({get:'infowindow'});
									$('#id_location').val(addr);
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

		$('#id_location').autocomplete({
			source : function() {
				gmap.gmap3({
					getaddress: {
						address: $(this).val(),
						callback: function(results){
						if (!results) return;
							$("#id_location").autocomplete("display", results, false);
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
									$( 'input[name="latlng"]' ).val(marker.getPosition());
									$( this ).gmap3({
										getaddress: {
											latLng: marker.getPosition(),
											callback: function(results) {
												var addr = results && results[0] ? results && results[0].formatted_address : 'no address';
												$('#id_location').val(addr);
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
							address: $('#id_location').val(),
							callback: function(results){
								var latlng = results[0].geometry.location.toString();
								$( 'input[name="latlng"]' ).val( latlng );
							}
						}
					});
				}
			}
		});

		$( '#sub_location' ).click(function(e) {
			e.preventDefault();
			if( $('#latlng').val() === '' ) {
				if( confirm('We Can not find you on google, are you sure to save this address?') ) {
					if ( $('#location_form').valid() ) {
							$( '#location_form' ).identalk_ajaxform({
							callback : function( result ) {
								window.parent.location.reload();
							}
						});
					}
				}
			} else {
				if ( $('#location_form').valid() ) {
						$( '#location_form' ).identalk_ajaxform({
						callback : function( result ) {
							window.parent.location.reload();
						}
					});
				}
			}
		});
	});
	
});