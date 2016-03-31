require.config({
	baseUrl: '/site_static/js',
	paths: {
		'domReady': 'libs/domReady',
		'jquery': 'libs/jquery-1.8.3.min',
		'json': 'libs/jquery-plugin/jquery.json-2.3.min',
		'tmpl': 'libs/jquery-plugin/jquery.tmpl.min',
		'validate': 'libs/jquery-plugin/jquery-validate/jquery.validate',
		'message': 'modules/common/message',
		'global': 'modules/common/global',
		'mail': 'modules/common/mail',
		'ajaxform': 'utils/ajaxform',
		'valuecheck': 'utils/valuecheck',
		'dropdown': 'utils/dropdown',
		'datepicker': 'libs/jquery-plugin/bootstrap-datepicker/bootstrap-datepicker',
		'timepicker': 'libs/jquery-plugin/jquery.timepicker.min'
	},
	shim: {
		'json': ['jquery'],
		'tmpl': ['jquery'],
		'validate': ['jquery'],
		'datepicker': ['jquery'],
		'timepicker': ['jquery'],
		'message': ['jquery', 'tmpl'],
		'global': ['message', 'dropdown']
	}
});

require(
['jquery','mail','datepicker','timepicker','global','domReady!'],
function($, mail){

	$( '#message' ).addClass( 'active' );
	var mail = mail.mail();
	mail.send();

	$( '.mail-extend' ).click(function(e){
		if( e.target.checked ) {
			
			$( '#extender' ).removeClass('hide');

			var nowTemp = new Date();
			var nowdate = new Date(nowTemp.getFullYear(), nowTemp.getMonth(), nowTemp.getDate(), 0, 0, 0, 0);
			$( 'input[name="start"]' ).val( '' ).datepicker({
				format: 'yyyy-mm-dd' 
			});
			
			$( 'input[name="time"]' ).val( '' ).timepicker();

			$( '.add-hour' ).click(function(){
				$( this ).hide().next().show();
			});
		} else {
			$( '#extender' ).addClass('hide');
		}
	});

}); 