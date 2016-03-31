define(['jquery'], function(){
	
	$.fn.identalk_scrollspy = function(opts){
		var defaults = {},
			settings = $.extend({}, defaults, opts);

		this.each(function(){
			var $this = $( this ),
				targets = $this.find( 'a' ),
				tops = [],
				tags = [];
			var off = settings.offset || 0;
			for(var i = 0; i<targets.length; i++ ){
				var t = targets[i].href.substring(targets[i].href.indexOf('#'));
				tags.push(t)
			}	
			for(var i = 0; i<tags.length; i++ ){
				var top = $( tags[i] ).offset().top-off;
				tops.push(top);
			}
			$( window ).scroll(function(){
				for(var i = 0; i<tags.length; i++ ){
					if( $(window).scrollTop()>tops[i]*1 ){
						$this.find('a[href="'+tags[i]+'"]')
						.parent().addClass('active')
						.siblings().removeClass('active');
					}else{
						return;
					}
				}
			});
		});
		return this;
	}
});