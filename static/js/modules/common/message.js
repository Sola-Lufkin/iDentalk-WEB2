define(['jquery','tmpl'],function($){
	var message = {

		_time: 50000,
		listen_url: '/ajax/listener/',

		init: function(){
			this.get_message();
			this.interval();
		},

		get_message: function(){
			var mt = $( '#message' );	
			mt.click(function(e){
				e.preventDefault();
				var url = this.href;
				$.ajax({
					url: url,
					success: function( result ){
						$( '.more-msg' ).before( $('#message_tmpl').tmpl( result.senders) );
					}
				});
			});
		},

		interval: function(){
			setInterval(function(){
				$.ajax({
					url: message.listen_url,
					success: function(result){
						if( result.msg_count > 0 ){
							$( '.message-count' ).text(result.msg_count).show();
						}
						if( result.notice_count > 0 ){
							$( '.notice-count' ).text(result.notice_count).show();
						}
						if( result.cal_count > 0 ) {
							$( '.cal-count' ).text( result.cal_count ).show();	
						}
					}
				})
			},message._time);
		}
	}

	return message;
});