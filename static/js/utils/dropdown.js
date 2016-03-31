define(['jquery'], function(){

	// FIXME
	$.fn.identalk_dropdown = function( opts ){
		this.each(function(){
			var $this = $( this );
			var open_menu = function(){
				$this.addClass( 'open' ).next( '.dropdown-menu' ).show();
			}
			var close_menu = function(){
				$this.removeClass( 'open' ).next( '.dropdown-menu' ).hide();
			}
			if( $this.data('droptype') == 'hover' ){
				$this.hover(function(){
					open_menu();
				},function(){
					close_menu();	
				});
			}else{
				$this.click(function( e ){
					e.preventDefault();
					open_menu();
					$( 'html' ).on('click', function( e ){
						if( !$( e.target ).hasClass( 'open' ) ){
							close_menu();
						}
						// if( $('.open').length > 1 ){
						// 	$( '.open' ).eq(0).removeClass( 'open' ).next( '.dropdown-menu' ).hide();
						// }
					});
				});
			}
			
		});
		return this;
	}
	
});