require.config({
	baseUrl: '/site_static/js',
	paths: {
		'domReady': 'libs/domReady',
		'jquery': 'libs/jquery-1.8.3.min',
		'json': 'libs/jquery-plugin/jquery.json-2.3.min',
		'tmpl': 'libs/jquery-plugin/jquery.tmpl.min',
		'message': 'modules/common/message',
		'global': 'modules/common/global',
		'dropdown': 'utils/dropdown',
	},
	shim: {
		'json': ['jquery'],
		'tmpl': ['jquery'],
		'message': ['jquery', 'tmpl'],
		'global': ['message', 'dropdown']
	}
});

require(
['jquery','global','domReady!'],
function($){

	$(function(){
		$( '.notice' ).addClass( 'active' );

		$( '.relation-action' ).click(function(e){
			e.preventDefault();
			var url = this.href;
			$.ajax({
				url: url,
				success: function(result){
					$( this ).parent().parent().fadeOut('fast');
					loadings.autohide( result.msg );
					refresh();	
				}
			});
		});
	});
});