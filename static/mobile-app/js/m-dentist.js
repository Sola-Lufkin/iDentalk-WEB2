$(document).bind('pageinit',function(){
	var Dentist = {
		timeline: function(){
			var that = {};
			var _self = {
				url: '/ajax/d/stream/post/',
				url_post: '/ajax/d/stream/getpost/',
				url_more: '/ajax/d/stream/getmorepost/',
				msg_wrap: '#msg_flow',
				msg_box: '#msg_box',
				tmpl: '#post_tmpl'
			}
			that.init = function(){
				this.openinput();
				this.getpost();
				this.post();
			}
			that.openinput = function(){
				$( '#open_post' ).click(function(){
					$( '.post-wrap' ).show().find( _self.msg_box ).focus();
				});
			}
			that.getpost = function(){
				$.ajax({
					url: _self.url_post,
					success: function(result){
						Dentist.timeline().render(result)	
					}
				});
			}
			that.post = function(){
				$( '#sub_post' ).click(function(e){
					e.preventDefault();
					var data = $( _self.msg_box ).val();
					if( data === '' ){
						return;
					}else{
						$.ajax({
							url: _self.url,
							data: {
								post: data
							},
							success: function(result){
								$( _self.msg_box ).text('').val('');
								$( '.post-wrap' ).hide();
								Dentist.timeline().renderone(result);
							}
						});
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
			that.renderone = function(result){
				if( $( _self.msg_wrap ).children().length > 0 ){
					$( _self.msg_wrap+' .stream:first-child' )
					.before( $( _self.tmpl ).tmpl( result ) );
				}else{
					$( _self.msg_wrap )
					.append( $( _self.tmpl ).tmpl( result ) );
				}
			}
			return that;
		}
	}

	var timeline = Dentist.timeline();
	timeline.init();
});