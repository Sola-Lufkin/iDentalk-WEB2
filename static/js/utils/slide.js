define(['jquery'], function(){

	$.fn.identalk_slide = function( opts ){
		var defaults = {
			interval: 3000,
			duration: 500
		},
			settings = $.extend({}, defaults, opts);

		this.each(function(){
			var $this = $( this );

			var slides = $( 'img', $this ),
				current = 0,
				next = current + 1;
			
			slides.hide().eq(current).fadeIn(settings.duration).addClass('active');
			var rotate = function(){
					slides.eq(current).fadeOut(settings.duration).removeClass('active')
					.end().eq(next).fadeIn(settings.duration).addClass('active').queue(function(){
						rotateTimer();
						$(this).dequeue();
					});
					current = next;
					next = current >= slides.length-1 ? 0 : current+1;
			}

			var rotateTimer = function(){
				$this.play = setTimeout(function(){
					rotate();
				}, settings.interval);
			};

			rotateTimer();

		});
		return this;
	}
	
});