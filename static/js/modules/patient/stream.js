define(
['jquery','valuecheck','btnmask'],
function(){
	var Stream = {
		_constructor: {
			url_get_post: '/ajax/p/stream/getpost/',
			url_get_comment: '/ajax/p/stream/getcomment/',
			url_comment: '/ajax/stream/comment/'
		},
		init: function(){
			this.get();
			this.comment.init();
		},
		get: function(){
			var c = Stream._constructor;
			$.ajax({
				url: c.url_get_post,
				success: function( result ){
					Stream.render( result );
				}
			});
		},
		render: function(result){
			if( result[0].id ){
				$( '#msg_flow' ).empty().hide()
				.append( $( '#stream_tmpl' ).tmpl( result ) ).fadeIn(500);
				this.more();
				this.zoom_pic();
				Stream.comment.init();
			}else{
				$( '#msg_flow' ).remove();
				$( '.timeline-footer' ).remove();
				$( '#timeline' ).append( '<h3 class="text-center"><a href="/geoloc-search/myloc/">Search</a> for a Dentist</h3>');
			}
		},
		more: function(){
			var c = Stream._constructor;
			var page = 1;
			if( $('.stream').length>=10 ){
				// var $more = $('<button class="more-post span12 btn btn-small btn-info">More</button>')
				var $more = $( '<div class="stream get-more-post"><div class="stream-content"><dl class="stream-avatar more-post"><i class="icon-refresh"></i></dl></div></div>');
				$( '.stream:last-child' ).after( $more );
				$( '.more-post' ).click(function(){
					page += 1;
					$.ajax({
						url: c.url_get_post,
						data: {
							page: page
						},
						success: function( result ){
							if( !result[0].is_end ){
								$( '.stream' ).not( '.get-more-post' )
								.last().after( $( '#stream_tmpl' ).tmpl( result ) )
								.nextAll().hide().fadeIn(500);
								Stream.zoom_pic();
								Stream.comment.init();
							}else{
								$( '.more-post' ).unbind( 'click' ).addClass( 'disabled' );
							}
						}
					});
				});
			}	
		},
		zoom_pic: function(){
			$( '.upload-img' ).unbind( 'click' ).click(function(e){
				e.preventDefault();
				var $this = $( this );
				if(	!$this.hasClass('preview-pic') ) {
					$this.addClass( 'preview-pic' )
					.children().attr('src', $this.data('big-pic'));
				}else{
					$this.removeClass( 'preview-pic' )
					.children().attr('src', $this.attr('href'));
				}
			});
		},
		comment: {
			init: function(){
				this.get();
				this.sub();
			},
			get: function(){
				var c = Stream._constructor;
				$( '.comment' ).unbind( 'click' ).click(function(){
					var comments = $('#comments_'+this.rel);
					var pid = $( this ).attr( 'rel' );
					if( comments.hasClass('hide') ){
						comments.removeClass( 'hide' );
						$.ajax({
							url: c.url_get_comment,
							data: {
								post_id: pid
							},
							success: function(result){
								$( '#comments-tree_'+pid ).hide()
								.append( $('#comment_tmpl').tmpl(result) ).fadeIn(500);
							}
						})
					}else{
						comments.addClass( 'hide' );
						$( '#comments-tree_'+pid ).empty();
					}
				});
			},
			sub: function(){
				var c = Stream._constructor;
				$( '.sub-comment' ).unbind( 'click' ).click(function(){
					var $this = $( this );
					var pid = $this.attr( 'rel' ),
						comment = $this.prev().val();
					if( !$this.prev().identalk_valuecheck() ){
						return;
					}else{
						$this.identalk_btnMask('open');
						$.ajax({
							url: c.url_comment,
							data: {
								pid: pid,
								comment: comment 
							},
							success: function(result){
								if( result.status ){
									$( '#comments-tree_'+pid )
									.append( $('#comment_tmpl').tmpl(result) );
									$( 'textarea[name=comment-content]' ).val('').text('');
									$( '.comment[rel='+pid+'] .comment-count' ).text( result.comment_count );
									$this.identalk_btnMask('close');
								}
							}
						});
					}
				});
			}
		}
	}
	return Stream;
});