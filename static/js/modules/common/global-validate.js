define(
['jquery','validate'],
function(){
	
	$( '.require-form' ).each(function(){
		$( this ).validate();
	});
});