define(['jquery', 'lightbox'], function($){

	$.fn.confirmbox = function(opts){
		var defaults = {
			title: 'Action',
			msg: 'Are you sure to delete this?',
			btn: ['Close', 'Delete']
		}

		var settings = $.extend({}, defaults, opts);

		function close(){
			$( '.orange-close' ).click();
		}

		this.each(function(events){
			var target = this,
				$this = $( this );
				
			if( $this.data('msg') !== undefined ) {
				settings.msg = $this.data('msg');
			}

			if( $this.data('title') !== undefined ) {
				settings.title = $this.data('title');
			}

			if( $this.data('btn') !== undefined ) {
				settings.btn = $this.data('btn').split(',');
			}

			var saveHandlers = function() {
		        var events =  $._data(target, 'events');
		        if (events) {
		            target._handlers = new Array();
		            $.each(events['click'], function(){
		                target._handlers.push(this);
		            });

		            $this.unbind('click');
		        }
		    };

		    var rebindHandlers = function() {
                if (target._handlers !== undefined) {
                    $.each(target._handlers, function() {
                        $this.bind('click', this);
                    });
                }
            };

            var handler = function(e) {
            	e.stopImmediatePropagation();
				e.preventDefault();
				$this.identalk_lightbox({
					autoheight: true,
					width: 530,
					open: true,
					content: $( '.modal' ).html(),
					afterLoad: function(){
						var wrapper = $( '.orange-wrap' );
						// wrapper.find( '.modal-title' ).text( settings.title );
						wrapper.find( '.modal-body' ).text( settings.msg );
						wrapper.find( '.confirm-save' ).text( settings.btn[1] );
						wrapper.find( '.confirm-close' ).text( settings.btn[0] );
						wrapper.find( '.confirm-close' ).bind('click', function(){
							close();
						});
						wrapper.find( '.confirm-save' ).bind('click', function(){
							$this.unbind('click', handler).click()
							close();
						});
					}
				});
            }

			saveHandlers();

			$this.bind('click', handler);

			rebindHandlers();

		});
		return this;
	}

});