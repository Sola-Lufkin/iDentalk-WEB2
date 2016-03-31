require.config({
	baseUrl: '/site_static/js',
	paths: {
		'domReady': 'libs/domReady',
		'jquery': 'libs/jquery-1.8.3.min',
		'json': 'libs/jquery-plugin/jquery.json-2.3.min',
		'tmpl': 'libs/jquery-plugin/jquery.tmpl.min',
		'datepicker': 'libs/jquery-plugin/bootstrap-datepicker/bootstrap-datepicker',
		'validate': 'libs/jquery-plugin/jquery-validate/jquery.validate',
		'jcrop': 'libs/jquery-plugin/jquery.Jcrop.min',
		'avatar': 'modules/common/avatar',
		'global': 'modules/common/global',
		'followAction': 'modules/patient/follow_action',
		'message': 'modules/common/message',
		'contact': 'modules/common/contact',
		'p_stream': 'modules/patient/stream',

		'ajaxform': 'utils/ajaxform',
		'btnmask': 'utils/btnmask',
		'dropdown': 'utils/dropdown',
		'fileupload': 'utils/fileupload',
		'lightbox': 'utils/lightbox',
		'valuecheck': 'utils/valuecheck'
	},
	shim: {
		'json': ['jquery'],
		'tmpl': ['jquery'],
		'validate': ['jquery'],
		'jcrop': ['jquery'],
		'message': ['jquery'],
		'followAction': ['jquery', 'lightbox', 'ajaxform'],
		'global': ['message', 'dropdown'],
		'datepicker': ['jquery'],
		'avatar': ['jcrop']
	}
});

require(
['jquery','p_stream','avatar','followAction','contact','global','domReady!'],
function($, stream, avatar, followAction){

	$( '#pat_home' ).addClass( 'active' );
	var popup_avatar = avatar.popup_avatar();
	popup_avatar.init();
	
	stream.init();

	// follow tab
	$( '.follow-type .span4').each(function(index){
		$( this ).click(function(){
			$( this ).addClass( 'active' ).siblings().removeClass( 'active' );
			$( '.den-list' ).addClass('hide')
			.eq( index ).removeClass('hide')
		});
	});

	$( '.den-list .row-fluid' ).hover(function(){
		$( this ).find('.list-more').show();
	},function(){
		$( this ).find('.list-more').hide();
	});

	followAction(true);

});