define(
['jquery','jcrop','lightbox','fileupload','ajaxform'],
function($){
	var avatar = {
		popup_avatar: function(){
			var that = {};
			that.init = function(){
				$( '.avatar-wrapper' ).hover(function(){
					$( this ).children( '.img-tip' ).removeClass( 'hide' );
				},function(){
					$( this ).children( '.img-tip' ).addClass( 'hide' );
				});
				this.open_panel();
			}

			that.open_panel = function(){
				$( '.avatar' ).identalk_lightbox({
					width: 600,
					autoheight: true,
					content: $( '#upload_avatar_wrapper .well' ).clone().html(),
					afterLoad: function(){
						$( '.orange-wrap .ferret' ).attr( 'src', $('.avatar').attr('src') );
						avatar.popup_avatar().edit();
					}
				});
			}

			that.edit = function(){
				var wrapper = $( '.orange-wrap' );
				wrapper.find( '.choose_avatar' ).identalk_fileupload({
					form_target: 'avatar_upload_iframe',
					form_action: '/ajax/saveimg/',
					file_name: 'imagephoto',
					afterLoad: function(data){
						try{
							jcrop_api.destroy();
						}catch(e){}
						if( data.indexOf('msg') !== -1 ) {
							loadings.autohide(data.split(',')[1]);
							return;
						}
						var data = data.split(',');
						wrapper.find( '.ferret' ).attr( 'src', data[0])
							.css({width:data[1],height:data[2]});
						wrapper.find( '.ferret' ).Jcrop({
							setSelect: [ 50, 10, 200, 200 ],
							aspectRatio: 1,
							onSelect: function(c){
								wrapper.find('input[name="x1"]').val(c.x);
			                    wrapper.find('input[name="y1"]').val(c.y);
			                    wrapper.find('input[name="x2"]').val(c.x2);
			                    wrapper.find('input[name="y2"]').val(c.y2);  
							}
						},function(){
							jcrop_api = this;
						});
						wrapper.find( '.upload_avatar' ).show().unbind('click')
							.click(function(e){
		            		e.preventDefault();
		            		var $this = $( this );
		            		if( $this.hasClass('disabled') ){
		            			return;
		            		}else{
		            			$this.addClass( 'disabled' );
			            		loadings.show();
			            		$( '.orange-wrap' ).find( '.resize_form' ).identalk_ajaxform({
			            			url: '/ajax/cutimg/',
			            			callback: function( result ){
			            				loadings.show( result.msg );
			            				refresh();
			            			},
			            			onerror: function(result){
			            				$this.removeClass( 'disabled' );
			            			}
			            		});
			            		$this.hide();
		            		}
		            	});	
					}
				});
			}
			return that;
		},

		step_avatar: function(){
			var that = {}
			return that;
		}
	}
	return avatar;
});