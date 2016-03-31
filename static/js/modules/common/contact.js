define(
['jquery','lightbox','valuecheck','ajaxform'],
function(){
	$( '.contact-btn' ).identalk_lightbox({
		width: 700,
		autoheight: true,
		content: $( '.contact-box' ).html(),
		afterLoad: function(target){
			var den_name = $(target).data( 'name' ),
				den_id = target.rel,
				wrapper = $( '.orange-content' );
			wrapper.find( '.den-name' ).text( den_name ).end().
				find( 'input[name="contact-id"]' ).val( den_id ).end().
				find( '.sub-message' ).click(function(){
					if( !wrapper.find('textarea').identalk_valuecheck() ){
						return;
					}else{
						wrapper.find( 'form' ).identalk_ajaxform({
							url: '/ajax/mydentalk/sendmsg/',
							callback: function(result){
								if( result.status ){
									$( '.orange-close' ).click();
								}
								loadings.autohide( result.msg );
							}
						});
					}
			});
		}
	});
});