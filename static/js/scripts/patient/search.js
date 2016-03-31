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
		'followAction': 'modules/patient/follow_action',
		'autocomplete': 'libs/jquery-plugin/jquery-autocomplete.min',
		'lightbox': 'utils/lightbox',
		'ajaxform': 'utils/ajaxform',
		'dropdown': 'utils/dropdown'
	},
	shim: {
		'json': ['jquery'],
		'tmpl': ['jquery'],
		'validate': ['jquery'],
		'message': ['jquery'],
		'followAction': ['lightbox', 'ajaxform'],
		'global': ['jquery', 'message','dropdown'],
		'autocomplete': ['jquery','gmap3']
	}
});

require(
['jquery','followAction','gmap3','autocomplete','global','domReady!'],
function($, followAction){
	
	var marker_green = "http://maps.google.com/mapfiles/marker_green.png";

	var more = function(opts){
		var page = 1;
		if( $('.result-list').length >= 10 ){
			$( '.more-wrap' ).show();
			$( '#more_result' ).removeClass( 'disabled' )
			.unbind('click').click(function(){
				page += 1;
				var data;
				if( opts.keyword !== undefined ){
					data = {
						page: page,
						keyword: opts.keyword
					}
					data = {
						data: $.toJSON(data)
					}
				}else{
					data = {
						page: page,
						latlng: $('#latlng').val(),
						distance: $( '.distance.active' ).text()
					}
				}
				$.ajax({
					url: opts.url,
					type: opts.type,
					data: data,
					success: function( result ){
						if( !result.searchresult[0].is_end ){
							$( '.result-list' ).last().after( $( '#searchresult_tmpl' ).tmpl( result.searchresult ) );
							followAction();
						}else{
							$( '#more_result' ).unbind( 'click' ).addClass( 'disabled' );
						}
					}
				});
			});
		}
	}
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

	if( gmap.length > 0 ){
		$(function(){
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
											$('#id_location').val(addr);
											$('#save_loc').click();
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
										$('#latlng').val(marker.getPosition());
										$( this ).gmap3({
											getaddress: {
												latLng: marker.getPosition(),
												callback: function(results) {
													var addr = results && results[0] ? results && results[0].formatted_address : 'no address';
													$('#id_location').val(addr);
													$('#save_loc').click();
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
			}).focus();

			$( '#change_loc' ).click(function(){
			    $('#mylocation_show').hide();
			    $( '#new_location' ).show();
			});

			$( '#cancel_save' ).click(function(){
			    $('#new_location').hide();
			    $( '#mylocation_show' ).show();
			});


			$( '#save_loc' ).click(function(){
			    var latlng = $( 'input[name="latlng"]' ).val();
			    var location = $( 'input[name="location"]').val();
			    $.ajax({
				    url:'/ajax/p/profile/editlocation/',
				    data: {
				        	latlng: latlng,
				        	location: location
				    },
				    success: function(result){
				    	loadings.autohide( result.msg );
				    	$( '#mylocation' ).text(location);
				    	$( '#new_location' ).hide();
			    		$( '#mylocation_show' ).show();
				    }
				});
			});

			$( '.distance' ).each(function(){
				$( this ).click(function(){
					var $this = $( this );
					var zoom = $this.data('zoom');
					$this.addClass('active').siblings().removeClass('active');
					var distance = $this.text();
					var latlng = $( 'input[name="latlng"]' ).val();
					$.ajax({
					    url:'/ajax/geoloc-range/',
					    data: {
					        distance: distance,
					        latlng: latlng
					    },
					    success: function(result){
					    	var searchresult = result.searchresult;
					    	$( '#result_box' ).empty()
					    	.append( $( '#searchresult_tmpl' )
					    	.tmpl(searchresult) );
					    	if( searchresult[0].status === undefined ){
					    		$( '#result_box' ).empty()
					    		.append( '<h3 class="text-center muted">No results</h3>' );
					    		$( '.more-wrap' ).hide();
					    	}else{
					    		followAction();
						    	more({url:'/ajax/geoloc-range/',type:'POST'});
						    	var locations = [];
						    	for( var i = 0; i<searchresult.length; i++ ){
						    		if( searchresult.is_end ){
						    			return;
						    		}else{
						    			var latlng = toLatlng(searchresult[i].latlng),
						    			c = {
							    			latLng: latlng,
							    			data: {
						    					name: searchresult[i].clinic,
						    					work_location: searchresult[i].work_location
						    				}
						    			}
						    			locations.push(c);
						    		}
						    		
						    	}
						    	var myloc = toLatlng($('#latlng').val());
						    	locations.push(
						    		{
						    			latLng: myloc,
						    			data: {
						    				name: 'I am here',
						    				work_location: ''
						    			},
						    			options:{icon: marker_green}
						    		}
						    	);
						    	if( searchresult.length > 0 ){
						    		gmap.gmap3({
						    			map: {
						    				options: {
						    					// center: myloc,
						    					zoom: zoom
						    				}
						    			},
						    			clear: 'marker',
						    			marker: {
						    				clear: 'marker',
						    				values: locations, 
						    				events: {
					    						mouseover: function(marker, event, context){
													var map = $(this).gmap3('get'),
						                      			infowindow = $(this).gmap3({get:{name:"infowindow"}});
								                  	if(infowindow){
								                    	infowindow.open(map, marker);
								                    	var clinicinfo = "<div>"+context.data.name+"</div>"+
								                    					"<div>"+context.data.work_location+"</div>";
								                    	infowindow.setContent(clinicinfo);
								                  	}else{
								                    	$(this).gmap3({infowindow:{anchor:marker,options:{content: clinicinfo}}})
								                  	}
												},
												mouseout: function(){
													var infowindow = $(this).gmap3({get:{name:"infowindow"}});
											      	if(infowindow){
												        infowindow.close();
											      	}
												}
						    				}
						    			}
						    		});
						    	}else{
						    		gmap.gmap3({
						    			map: {
						    				options: {
						    					zoom: zoom
						    				}
						    			},
						    			clear: 'marker'
						    		})
						    	}
					    	}
					    }
					});
				});
			});
		});
	}else{
		$( '#search' ).click(function(e){
			e.preventDefault();
			$( '#search_keywords' ).text( '"'+$('.big-search-input').val()+'"' );
			$( '#search_name' ).identalk_ajaxform({
				type: 'GET',
				callback: function( result ){
					if( result.searchresult[0].status === undefined ){
						$( '#result_box' ).empty()
						.append( '<h3 class="text-center muted">No results</h3>' );
						$( '.more-wrap' ).hide();
					}else{
						$( '#result_box' ).empty()
				    	.append( $( '#searchresult_tmpl' )
				    	.tmpl(result.searchresult) );
				    	followAction();
				    	more({url:'/name-search/',type:'GET',keyword:$('.big-search-input').val()});
					}
				}
			});
		});
		var keyword = $( '.big-search-input' ).val();
		if( keyword !== '' ){
			$( '#search' ).click();
		}
	}
	
});