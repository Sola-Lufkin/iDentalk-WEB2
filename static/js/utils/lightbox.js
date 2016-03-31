define(['jquery'], function(){

	$.fn.identalk_lightbox = function( opts ) {
		var defaults = {
			width: 650,
			height: 400,
			content: 'lightbox',
			animate: false,
			autoheight: false,
			autowidth: false,
			fixed: false,
			open: false
		},
			orange_tpl = "<div class='orange-wrap hide'><div class='orange-outer'><a href='javascript:;' class='orange-close'>X</a>" 
						+ "<div class='orange-content'>{{content}}</div></div></div>",
			$orange_wrap = $( '<div class="orange-wrap"></div>' ),
			$orange_outer = $( '<div class="orange-outer"></div>' ),
			$orange_header = $( '<div class="orange-header"><a href="javascript:;" class="orange-close">X</a></div>' ),
			$orange_content = $( '<div class="orange-content"></div>' ),
			settings = $.extend({}, defaults, opts);

		function mask(){
			$( '<div class="mask hide"></div>' ).css({
				width: $(document).width(), height: $(document).height()
			}).appendTo( 'body' );
		};

		function end(){
			$( '.orange-wrap' ).hide().remove();
			$( '.mask' ).fadeOut(300, function(){
				$( this ).remove();
			});
			if( settings.afterClose !== undefined ){
				settings.afterClose();
			}
		};

		function well(target, opts){
			return target.css(opts).animate({
				opacity: 'show',
				top: '+=15'
			}, 300);
		};

		function resize(){
			var newsize = $( '.orange-outer' );
			$( '.orange-wrap' ).css({
				height: newsize.height(),
				width: newsize.width()
			});
		};

		function open(e){
			$this = $( e );
			mask();
			var mask_index = $( '.mask' ).css('z-index');
			if( settings.beforeLoad !== undefined ){
				settings.beforeLoad(e);
			}

			if( settings.type == 'img' ){
				var img =  '<img src="'+$this.attr( 'href' )+'" />';
				// orange_tpl = orange_tpl.replace( '{{content}}', img ); 
				$orange_content.empty().append(img);
			}
			if( settings.type == 'iframe' ){
				var iframe = $( '<iframe  src="'+$this.attr( 'href' )+'"></iframe>' );
			}
			else{
				// orange_tpl = orange_tpl.replace( '{{content}}', settings.content );
				$orange_content.empty().append(settings.content);
			}
			
			// var orange = $( orange_tpl );
			$orange_outer = $orange_outer.append($orange_header).append($orange_content);
			var orange = $orange_wrap.append($orange_outer);
			var height, width, o_top, o_left;

			switch( settings.type ){
				case 'iframe':
					orange.find( '.orange-content' ).html( iframe );
					iframe.load(function(){
						o_top = ( $( window ).height() / 2 ) - ( settings.height / 2 );
						o_left = ( $( window ).width() / 2 ) - ( settings.width / 2 );
						var css1 = {
								'height': settings.height,
								'width': settings.width,
								'overflow-x': 'hidden',
								'overflow-y': 'auto'
								}
						well(iframe, css1);
						var css2 = {
							'z-index':mask_index + 1,
							top: o_top + $(document).scrollTop() - 15,
							left: o_left
						}
						well(orange,css2);
					});
					break;

				case 'img':
					o_top = ( $( window ).height() / 2 ) - ( $( '.orange-wrap' ).height() / 2 );
					o_left = ( $( window ).width() / 2 ) - ( $( '.orange-wrap' ).width() / 2 );
					break;

				default:
					o_top = ( $( window ).height() / 2 ) - ( settings.height / 2 );
					o_left = ( $( window ).width() / 2 ) - (  settings.width / 2 );
					if( settings.autowidth ){
						width = 'auto';
					}else{
						width = settings.width;
					}
					if( settings.autoheight ){
						height = 'auto';
					}else{
						height = settings.height;
					}
					var opts = {
						height: height,
						width: width,
						top: o_top + $(document).scrollTop() - 15,
						left: o_left,
						'z-index': mask_index + 1
					}
					well(orange,opts)
					break;
			}
			if( settings.fixed ){
				orange.css({
					position: 'fixed',
					top: 200
				});
			}
			if( $.browser.msie ){
				orange.addClass( 'orange-wrap-ie' );
			}
			orange.appendTo( 'body' );

			if( settings.afterLoad !== undefined ){
				settings.afterLoad(e);
			}
			if( $( '.orange-wrap' ).length > 1 ){	
				$( '.orange-wrap' ).eq(0).remove();
			}	
			$( '.orange-close' ).click(function(){
				end();
			});
			$( '.mask' ).click(function(){
				end();
			});
		}

		this.each(function() {
			var $this = $( this );
			if( settings.open ){
				open(this);
			}else{
				$this.unbind('click').click(function(e){
					e.preventDefault();
					if( settings.beforeOpen !== undefined && settings.beforeOpen() ) {
						settings.beforeOpen();
						return;
					}
					open(this);
				});
			}
		});
		return this;
	}
	
});