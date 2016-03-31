define(
['jquery','valuecheck','tmpl','json','fileupload','confirmbox'],
function(){
	var Timeline = {
		_constructor: {
			post: {
				url: '/ajax/d/stream/post/',
				url_more: '/ajax/d/stream/getmorepost/',
				url_del: '/ajax/d/stream/deletepost/',
				tmpl: '#stream_tmpl',
				msg_box: '#msg_box',
				msg: '#msg_flow'
			},
			comment: {
				url_get: '/ajax/d/stream/getcomment/',
				url_sub: '/ajax/stream/comment/',
				url_del: '/ajax/d/stream/deletecomment/'
			}
		},
		post: {
			init: function(){
				this.post();
			},
			render: function( result ){
				if( result[0].id ){
					$( '#msg_flow' ).empty()
					.append( $( Timeline._constructor.post.tmpl ).tmpl( result ) );
					this.more();
					this.zoom_pic();
				}else{
					return;
				}
			},
			post: function(){
				var msg_box = Timeline._constructor.post.msg_box;
				// $( msg_box ).keyup(function(){
				// 	var len = $.trim( $(this).val() ).length;
				// 	$( '#msg_count' ).text(len);	
				// });

				$( '.post-msg' ).unbind('click').click(function(){
					var data = $.trim( $(msg_box).val() );
					if( !$( msg_box ).identalk_valuecheck() ){
						return false;
					}else{
						$.ajax({
							url: Timeline._constructor.post.url,
							data: {
								post: data,
								img: $('#pre_img').children('img').attr('src')
							},
							success: function( result ){
								$( msg_box ).text('').val('');
								$( '.post-img' ).val('');
								$( '#pre_img' ).empty().hide();
								Timeline.post.renderone( result );
							}
						});
					}
				});
				
				$( '#upload_img' ).identalk_fileupload({
					form_target: 'file_upload_iframe',
					form_action: '/ajax/d/stream/post_img/',
					file_name: 'img',
					afterLoad: function(data) {
						var data = $.evalJSON(data);
						if( data.status ) {
							$( '.post-img' ).val(data.post_img_url);
							var img = '<img src="'+data.post_img_url+'" width="200" height="150" />';
							$( '#pre_img' ).append( img ).show();
							$( '.del-post-img' ).on('click', function(){
								$( '.post-img' ).val('');
								$( '#pre_img' ).slideUp(1000, function(){
									$( this ).children( 'img' ).remove();
								});
							});
						}
						if( data.toolarge ) {
							loadings.autohide( data.msg );
							return;
						}
					}
				});
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
			more: function(){
				var page = 1,
				url = $( '.btn-post' ).data('link');

				if( $('.stream').length>=10 ){
					// var $more = $('<button class="more-post span12 btn btn-small btn-info">More</button>');
					var $more = $( '<div class="stream get-more-post"><div class="stream-content"><dl class="stream-avatar more-post"><i class="icon-refresh"></i></dl></div></div>');
					$( '.stream:last-child' ).after( $more );
					$( '.more-post' ).click(function(){
						page += 1;
						$.ajax({
							url: url,
							data: {
								page: page
							},
							success: function( result ){
								if( !result[0].is_end ){
									$( '.stream' ).not( '.get-more-post' )
									.last().after( $( Timeline._constructor.post.tmpl )
									.tmpl( result ) )
									.nextAll().hide().fadeIn(500);
									Timeline.post.del();
									Timeline.post.zoom_pic();
									Timeline.comment.init();
								}else{
									$( '.more-post' ).unbind( 'click' ).addClass( 'disabled' );
								}
							}
						});
					});
				}
			},
			renderone: function( result ){
				var tmpl = Timeline._constructor.post.tmpl,
					msg = Timeline._constructor.post.msg;
				if( $(msg).children().length > 0 ){
					$( msg+' .stream:first-child' ).hide().
					before( $( tmpl ).tmpl( result ) ).fadeIn(500);
				}else{
					$( msg ).hide()
					.append( $( tmpl ).tmpl( result ) ).fadeIn(500);
				}
				Timeline.comment.init();
				this.del();
				this.zoom_pic();
			},
			del: function(){
				$( '.stream' ).hover(function(){
					$( this ).find( '.stream-toolbar' ).removeClass( 'invisible' );
				},function(){
					$( this ).find( '.stream-toolbar' ).addClass( 'invisible' );
				});

				$( '.post-del' ).unbind('click').click(function(e){
					var pid = this.rel;
					$.ajax({
						url: Timeline._constructor.post.url_del, 
						data: {
							pid: $( this ).attr( 'rel' )
						},
						success: function( result ){
							loadings.autohide( result.msg );
							if( result.status ){
								$( '#stream_'+pid ).animate({
									opacity: 0,
									height: 0
								}, 1000, function(){
									$( this ).remove();
								});
							}
						}
					});
				}).confirmbox();
			}
		},
		comment: {
			init: function(){
				this.open();
				this.sub();
			},
			open: function(){
				$( '.comment' ).unbind( 'click' ).click(function(){
					var comments = $('#comments_'+this.rel);
					var pid = this.rel;
					if( comments.hasClass('hide') ){
						comments.removeClass( 'hide' );
						$.ajax({
							url: Timeline._constructor.comment.url_get, 
							data: {
								post_id: pid
							},
							success: function( result ){
								Timeline.comment.render(result, pid);
							}
						})
					}else{
						comments.addClass( 'hide' );
						$( '#comments-tree_'+pid ).empty();
					}
				});
			},
			render: function(result, pid){
				$( '#comments-tree_'+pid ).hide()
				.append( $('#comment_tmpl').tmpl(result) ).fadeIn(500);
				this.del();
			},
			sub: function(){
				$( '.sub-comment' ).unbind( 'click' ).click(function(){
					var $this = $( this );
					var pid = $this.attr( 'rel' ),
						comment = $this.prev().val();
					if( !$this.prev().identalk_valuecheck() ){
						return;
					}else{
						$this.identalk_btnMask('open');
						$.ajax({
							url: Timeline._constructor.comment.url_sub,
							data: {
								pid: pid,
								comment: comment
							},
							success: function(result){
								if( result.status ){
									Timeline.comment.render(result, pid);
									$( 'textarea[name=comment-content]' ).val('').text('');
									$( '.comment[rel='+pid+'] .comment-count' ).text( result.comment_count );
									$this.identalk_btnMask('close');
								}
							}
						});
					}
				});
			},
			del: function(){
				$( '.del-comment' ).unbind( 'click' ).click(function(){
					var cid = this.rel
					$this = $( this );
					$.ajax({
						url: Timeline._constructor.comment.url_del,
						data: {
							cid: cid 
						},
						success: function( result ){
							if( result.status ){
								$( '#comment_'+cid ).next().remove().end().remove();
								$( '.comment[rel='+result.pid+'] .comment-count' ).text( result.comment_count );
								$this.remove();
							}
							loadings.autohide( result.msg );
						}
					});
				}).confirmbox();
			}
		}
	}
	return Timeline;
});