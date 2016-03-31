require.config({
	baseUrl: '/site_static/js',
	paths: {
		'domReady': 'libs/domReady',
		'jquery': 'libs/jquery-1.8.3.min',
		'json': 'libs/jquery-plugin/jquery.json-2.3.min',
		'tmpl': 'libs/jquery-plugin/jquery.tmpl.min',
		'validate': 'libs/jquery-plugin/jquery-validate/jquery.validate',
		'ajaxform': 'utils/ajaxform',
		'valuecheck': 'utils/valuecheck',
		'lightbox': 'utils/lightbox',
		'dropdown': 'utils/dropdown',
		'message': 'modules/common/message',
		'global': 'modules/common/global',
		'contact': 'modules/common/contact',
	},
	shim: {
		'json': ['jquery'],
		'tmpl': ['jquery'],
		'validate': ['jquery'],
		'lightbox': ['jquery'],
		'message': ['jquery'],
		'global': ['message'],
		'contact': ['lightbox']
	}
});

require(
['jquery','dropdown','contact','global','domReady!'], 
function($){

	$( '#den_patlist' ).addClass( 'active' );

	$( '.tab' ).click(function(){
		$( this ).addClass( 'active' ).siblings().removeClass( 'active' );
		$( '#'+$(this).data('target') ).show().siblings().hide();
	});

	$( '.list-more' ).identalk_dropdown();
	// 对病人申请的操作
	$( '.rel-control' ).click(function(e){
		e.preventDefault();
		var url = this.href;
		$.ajax({
			url: url,
			success: function(result){
				loadings.show( result.msg );
				if( result.status ){
					refresh();
				}
			}
		});
	});
}); 