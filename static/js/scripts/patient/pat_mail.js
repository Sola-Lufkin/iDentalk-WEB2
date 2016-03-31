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
		'dropdown': 'utils/dropdown'
	},
	shim: {
		'json': ['jquery'],
		'tmpl': ['jquery'],
		'validate': ['jquery'],
		'message': ['jquery', 'tmpl'],
		'global': ['message', 'dropdown']
	}
});

require(
['jquery','mail','global','domReady!'],
function($, mail){

	$( '#message' ).addClass( 'active' );
	var mail = mail.mail();
	mail.send();
	syncheight();
}); 