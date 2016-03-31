define(['jquery'], function($){

	$.fn.identalk_fileupload = function(opts){
		var defaults = {
			ie: $.browser.msie,
			safari: $.browser.safari,
			file_count: 1,
			form_target: '/',
			form_action: '/',
			file_name: 'file',
		};
		var	settings = $.extend({}, defaults, opts);
		
		var file_input = $( '<input type="file">' ),
			form = $( '<form class="fake_upload" method="POST"></form>' ),
		    iframe = $( '<iframe src="javascript:false;" name="'+settings.form_target+'"></iframe>' );

		function iframe_load(){
			iframe.load(function(){
				settings.afterLoad = opts.afterLoad || undefined
				iframe.unbind('load').bind('load', function(){
					loadings.hide();
					var contents = $( this ).contents().get(0);
					var data = $( contents ).find('body').html();
					if( settings.afterLoad !== undefined ){
						settings.afterLoad(data);
					}
				});	
			});
		}

		this.each(function(){

			var $this = $( this );

			if( $this.find('.fake_upload').length > 0 ){
				$this.find('.fake_upload').remove();
			}

			iframe.addClass('hide');
			file_input.prop('name', settings.file_name);

			iframe_load();
			form.unbind('change').bind('change', function(){
				form.submit();
				loadings.show();
			});

			file_input.css({
				'opacity': 0,
				'filter': 'alpha(opacity=0)',
				'position': 'absolute',
				height: $this.outerHeight()*3 || 60,
				right: 0,
				top: 0,
				cursor: 'pointer',
				'font-size': '118px'
			});

			form.css({
					'opacity': 0,
					'filter': 'alpha(opacity=0)',
					'position': 'relative',
					'width': $this.outerWidth() || 200,
					'top': -10,
					'right': -100,
				})
				.prop('target', settings.form_target)
				.prop('action', settings.form_action)
				.prop('enctype', 'multipart/form-data')
				.prop('encoding', 'multipart/form-data')
				.append(file_input)
				.append(iframe);

			$this.css({
				'overflow': 'hidden'
			}).prepend( form );

		});
		return this;
	}
});