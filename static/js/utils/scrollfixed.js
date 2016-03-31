define(['jquery'], function(){

	$.fn.identalk_scrollfixed = function( opts ){
		var defaults = {},
			settings = $.extend({}, defaults, opts),
			$this = $( this ),
			h = $this.height(),
			w = $this.width(),
			pos = $this.position();
			scroll_holder = $( '<div id="scroll_holder">' ).css({
				width: w,
				height: h
			});
		this.each(function(){
			$( window ).scroll(function(){
				if( $(window).scrollTop() >= h ){
					$this.before( scroll_holder );
					$this.css({
						'position': 'fixed',
						left: pos.left,
						top: pos.top,
						width: '100%',
						'z-index': 10
					});
				}else{
					$this.css({
						position: 'static'
					});
					$( '#scroll_holder' ).remove();
				}
			});
		});
		return this;
	}
});