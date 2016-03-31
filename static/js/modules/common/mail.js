define(
['jquery','valuecheck','ajaxform','tmpl'],
function(){

	Mail = {
		// quicksend: function(){
		// 	var that = {};
		// 	that.init = function(){
		// 		this.open();
		// 		this.sub();
		// 	}
		// 	that.open = function(){
		// 		$( '.send-message' ).click(function(){
		// 			Mail.quicksend().close();
		// 			$( this ).parent().parent().next().removeClass('hide');
		// 		});
		// 	}
		// 	that.close = function(){
		// 		$( '.quickmessage' ).addClass('hide').find( 'textarea' ).val('');
		// 	}
		// 	that.sub = function(){
		// 		$( '.sub-message' ).click(function(){
		// 			var text = $(this).parent().children('.quickmail').val();
		// 			if( !$(this).parent().children('.quickmail').identalk_valuecheck() ){
		// 				return;
		// 			}else{
		// 				$( this ).parent().identalk_ajaxform({
		// 					type: 'POST',
		// 					callback: function(result){
		// 						if( result.status ){
		// 							Mail.quicksend().close();
		// 						}
		// 						window.parent.loadings.autohide( result.msg );
		// 					}
		// 				});
		// 			}
		// 		});
		// 		$( '.cancel-sub' ).click(function(){
		// 			Mail.quicksend().close();
		// 		});
		// 	}
		// 	return that;
		// },
		mail: function(){
			var that = {};
			that.init = function(){
				this.send();
			}
			that.render = function(result){
				$( '#show_message' ).empty()
				.append( $('#message_sender_tmpl').tmpl(result) );
			}
			that.send = function(){
				var uid = $( 'input[name="contact-id"]' ).val();
				$( '.sub-message' ).click(function(){
					if( !$('textarea[name="content"]').identalk_valuecheck() ){
						return;
					}else{
						$( '#message_form' ).identalk_ajaxform({
							callback: function(result){
								$('textarea[name="content"]').val('');
								loadings.autohide( result.msg );
								refresh();
							}
						});
					}
				});
			}
			return that;
		}
	}
	return Mail;
});