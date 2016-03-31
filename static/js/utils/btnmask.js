define(['jquery'], function(){

	$.fn.identalk_btnMask = function(opts){
		var open;
		if( opts === 'open' || undefined ){
			open = true;
		}
		if( opts === 'close' ){
			open = false;
		}
		this.each(function(){
			var $this = $( this );
			var width = $this.outerWidth(),
				height = $this.outerHeight(),
				left = $this.offset().left,
				top = $this.offset().top,
				rel = $this.attr('class');
			if( open ){
				var $mask = $('<div class="btn-mask" rel="'+rel+'"></div>');
				$mask.css({
					width: width,
					height: height,
					left: left,
					top: top,
					'position': 'absolute'
				});
				$this.addClass('disabled').after( $mask );
			}else{
				$this.removeClass('disabled').next().remove();
			}

		});
		return this;
	}
	
});