(function($){
$(function(){

	$( '#sub_comment' ).click(function(e){
		e.preventDefault();
		var pid = $( this ).attr( 'rel' ),
			comment = $('#comment_input').val();
		if( comment == '' ){
			return;
		}else{
			$.ajax({
				url: '/ajax/stream/comment/',
				data: {
					pid: pid,
					comment: $('#comment_input').val()
				},
				success: function(result){
					if( result.status ){
						window.location.reload();
					}
				}
			});
		}
	});

})
})(jQuery);