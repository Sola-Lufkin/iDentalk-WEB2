define(['jquery'], function(){
	
	$.fn.identalk_valuecheck = function(){
		var valuechecked = true;
		this.each(function(){
			var $this = $(this);
			var text = $this.val(),
				value = text.replace(/(^\s*)|(\s*$)/g, "");
			if( value == '' || value == null ){
				valuechecked = false;
			}
		});
		return valuechecked;
	}
});