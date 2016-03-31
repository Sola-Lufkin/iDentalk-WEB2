define(
['jquery','lightbox','validate','ajaxform'],
function(){
	var Baseinfo = {
		_constructor: {
			
		},
		init: function(){
			this.show();
		},
		show: function(){
			$( '#edit_baseinfo' ).identalk_lightbox({
				// width: 550,
				autowidth: true,
				autoheight: true,
				content: $( '#edit_baseinfo_form' ).html(),
				afterLoad: function(){
					Baseinfo.sub();
				}
			});
		},
		sub: function(){
			var wrapper = $( '.orange-wrap' );
			wrapper.find( 'input[name="same_account_email"]' ).on('click',function(){
				if( this.checked ){
					wrapper.find('input[name="workemail"]').hide().next().show();
				}else{
					wrapper.find('input[name="workemail"]').show().next().hide();
				}
			});
			$( '.sub_base_info' ).on('click', function(e){
				e.preventDefault();
				if( wrapper.find( '.base_info_form' ).valid() ){
					wrapper.find( '.base_info_form' ).identalk_ajaxform({
						callback: function( result ){
							loadings.autohide( result.msg );
							refresh();
						}
					});
				}
			});
		}
	}
	return Baseinfo;
});