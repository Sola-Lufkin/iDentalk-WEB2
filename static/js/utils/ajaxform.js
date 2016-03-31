define(['jquery', 'json'], function(){

	$.fn.identalk_ajaxform = function( opts ){
		var defaults = {
			url: undefined,
			type: 'POST',
			dataType: 'json',
			addData: undefined,
			checklist: null
		},
			settings = $.extend({}, defaults, opts);

		this.each(function(){
			var $this = $( this );
			if( settings.url === undefined ){
				settings.url = $this.attr( 'action' );
			}
			var alldata = $this.serializeArray(),
				data = {};
			for (var i=0; i<alldata.length; i++) {
			 	data[alldata[i].name]=alldata[i].value;
			};
			
			if( settings.checklist !== null ){
				var checkbox = settings.checklist.split(',');
				for( var i=0; i<checkbox.length; i++ ){
					var checklist = [];
					var check = $( ':checkbox[name="'+checkbox[i]+'"]:checked' );
					for( var b=0; b<check.length; b++){
						checklist.push( check[b].value )
					}
					data[checkbox[i]] = checklist.toString();
				}
			};
			var addData = settings.addData;
			if( addData !== undefined && typeof addData === 'object' ) {
				data = $.extend( data, addData );
			}
			$.ajax({
				url: settings.url,
				type: settings.type,
				dataType: settings.dataType,
				data: {
					data: $.toJSON(data)
				},
				success: function( result ){
					if( settings.callback !== undefined ){
						settings.callback( result )
					}else{
						return;
					}
				},
				error: function( result ){
					if( settings.onerror !== undefined ){
						settings.onerror( result )
					}else{
						return;
					}
				}
			});
		});
		return this;
	}
	
});