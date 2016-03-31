$(document).bind('pageinit',function(){
	var Patient = {
		timeline: function(){
			var that = {};
			var _self = {
				url_post: '/ajax/p/stream/getpost/',
				msg_wrap: '#msg_flow',
				tmpl: '#post_tmpl'
			}
			that.init = function(){
				this.getpost();	
			}
			that.getpost = function(){
				$.ajax({
					url: _self.url_post,
					success: function(result){
						Patient.timeline().render(result)	
					}
				});
			}
			that.render = function(result){
				if( result[0].id ){
					$( _self.msg_wrap ).empty()
					.append( $( _self.tmpl ).tmpl( result ) );
					this.more();
				}else{
					return;
				}
			}
			that.more = function(){
				var page = 1;
				if( $('.stream').length>=10 ){
					var $more = $('<button class="more-post btn btn-info">More</button>')
					$( '.stream:last-child' ).after( $more );
					$( '.more-post' ).click(function(){
						page += 1;
						$( '.more-post' ).text( 'Loadings...' );
						$.ajax({
							url: _self.url_post, 
							data: {
								page: page
							},
							success: function( result ){
								$( '.more-post' ).text( 'More' );
								if( !result[0].is_end ){
									$( '.stream' ).last().after( $( _self.tmpl ).tmpl( result ) );
								}else{
									$( '.more-post' ).unbind( 'click' ).addClass( 'disabled' );
								}
							}
						});
					});
				}
			}
			return that;
		}
	}

	var timeline = Patient.timeline();
	timeline.init();
});