define(
['jquery','message','dropdown'],
function($, message){

	$.ajaxSetup({
		type: 'POST',
		dataType: 'json',
		cache: false
		// ,
		// error: function(){
		// 	loadings.show( 'error...>_<' );
		// }
	});

	window.loadings = {
		show: function( msg ){
			var m = msg || 'Loading...';

			$( '.window-tip' ).text( m ).animate({
				opacity: 'show',
				top: '10'
			},800);
		},
		hide: function(){
			$( '.window-tip' ).fadeOut().css({top:5});
		},
		autohide: function( msg ){
			loadings.show( msg );
			setTimeout(function(){
				loadings.hide();
			},5000);
		}
	}

	window.refresh = function(){
		window.location.reload();
	}

	window.syncheight = function(){
		$( '.syncbar' ).height( $( '.syncmain').height() );
	}
	// TODO 
	// rewrite confirm
	// oldcomfirm = window.confirm;
	// window.confirm = function(msg){
	// 	sure = false;
	// 	$( 'body' ).identalk_lightbox({
	// 		content: '<h3 class="text-center">'+msg+'</h3> \
	// 				<div class="form-actions"> \
	// 				<button id="comfirm_cancel" class="btn pull-right ml10">Cancel</button> \
	// 				<button id="comfirm_ok" class="btn pull-right">OK</button></div>',
	// 		autoheight: true,
	// 		open:true,
	// 		afterLoad: function(){
	// 			$( '#comfirm_ok' ).click(function(){
	// 				// alert(1)
	// 				// return true;
	// 				sure = true;
	// 			});
	// 			$( '#comfirm_cancel' ).click(function(){
	// 				// return false;
	// 				sure = false;
	// 			});
	// 		}
	// 	});
	// 	return sure;
	// }

	$( '.dropable' ).identalk_dropdown();
	
	if( $('.userinfo').length > 0 ){
	 	var message = message;
	 	message.init();
	}

});
