define(
['jquery','validate','lightbox','json','btnmask','ajaxform','tmpl'],
function(){

	var Gallery = {

		_constructor: {
			url_gallery: '/ajax/d/gallery/getcases/',
		},
		get: function(url){
			$.ajax({
				url: url,
				success: function(result){
					Gallery.render( result );	
				}
			});
		},
		newcase: {
			init: function(){
				Gallery.upload( true, '#new_case' );
			},
			create: function(wrapper){
				wrapper.find( '.sub_caseinfo' ).click(function(e){
					$( this ).identalk_btnMask();
					e.preventDefault();
					if( wrapper.find( '.caseinfo_form' ).valid() ){
						wrapper.find( '.caseinfo_form' ).identalk_ajaxform({
							callback: function( result ){
								wrapper.find( '.create_case' ).hide().next().show();
									if( result.status ){
										loadings.autohide( result.msg );
										wrapper.find( '.case_id' ).val( result.case_id )
									}
							}
						});
					}
				});
			}
		},
		edit: {
			init: function(){

			},
		},
		upload: function(is_new, target){
			$( target ).identalk_lightbox({
				width: 500,
				autowidth: true,
				height: 200,
				autoheight: true,
				content: $('#uploader_wrap').html(),
				afterLoad: function(){
					var wrapper = $( '.orange-wrap' );
					if( $( 'iframe[name="case_img_iframe"]' ).length > 0 ){
						$( 'iframe[name="case_img_iframe"]' ).remove();
					}
					var iframe = $( '<iframe>' ).attr( 'name', 'case_img_iframe' )
					iframe.appendTo( '.iframe_wrap' );

					if( is_new ) {
						Gallery.newcase.create( wrapper );
					}

					wrapper.find( '.caseimg_form' ).submit(function(){
						loadings.show();
						iframe.unbind( 'load' );
						iframe.on('load',function(){
							$( '.sub-case' ).removeClass('invisible');
							loadings.hide();
							$( '.case_img' ).val('');
							var contents = $( this ).contents().get(0);
							var data = $( contents ).find('body').html();
							var j = $.evalJSON(data);
							if( j.status ){
								loadings.autohide( j.msg );
								var img = '<div class="img-group"> \
								<img src="'+j.bef_img+'"><img src="'+j.aft_img+'"> \
								<a class="group-img-del newicon newicon-minus" href="javascript:;" rel="'+j.img_id+'" title="delete">X</a></div>';
								wrapper.find( '.preview_case' ).append( img );
								$( '.group-img-del' ).on('click', function(){
									var target = $( this ).parent();
									$.ajax({
										url: '/ajax/gallery/case/deleteimg/',
										data: {
											img_id: $( this ).attr( 'rel' )
										},
										success: function( result ){
											if( result.status ){
												target.slideUp().remove();
												loadings.autohide( result.msg )
											}
										}
									});
								});
							}
							if( j.toolarge ) {
								loadings.autohide( j.msg );
								return;
							}
	 					});
					});
					wrapper.find( '.sub_caseimg' ).click(function(e){
						e.preventDefault();
						if( wrapper.find( '.caseimg_form' ).valid() ){
							wrapper.find( '.caseimg_form' ).submit();	
						}
					});
					wrapper.find( '.sub-case' ).click(function(){
						$( this ).identalk_btnMask();
						$( '.mask' ).click();
						try	{	 
								Gallery.get( Gallery._constructor.url_gallery );
							}catch(e){
								refresh();
							}
					});
				}
			});
		},
		render: function(result) {
			if( result.length === 0 ) {
				$(　'#gallery_list .den-tip' ).show();
			} else {
				$( '#gallery_list' ).empty()
				.append( $( '#gallery_tmpl' ).tmpl( result ) );
			}
			
		}
	}

	return Gallery;
});