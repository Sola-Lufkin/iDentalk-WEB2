define(['jquety'], function(){

	$.fn.identalk_minibox = function( opts ){
		var defaults = {
			content: null
		},
			settings = $.extend({}, defaults, opts);

		var show_mask = function(){
			$( '<div class="mask"></div>' ).appendTo( 'body' );
			$( '.mask' ).click(function(){
				end();
			});
		}

		var end = function(){
			$( '.mask' ).remove();
			$( '.minibox' ).remove();
		}

		var open_box = function( target ){
			var position = target.position();
			var $minibox = $( '<div class="minibox"></div>' );
			if( settings.content !== null ){
				$minibox.append( settings.content );
			}
			$minibox.css({
						left: position.left,
						top: position.top
			});
			$minibox.appendTo( 'body' );
		}
		this.each(function(){
			var $this = $( this );
			$this.click(function( e ){
				e.preventDefault();
				show_mask();
				open_box( $this );
				if( settings.callback !== undefined ){
					settings.callback( $this );
				}
			});
		});
		return this;
	}
	
});