require.config({
	baseUrl: '/site_static/js',
	paths: {
		'jquery': 'libs/jquery-1.8.3.min',
		'json': 'libs/jquery-plugin/jquery.json-2.3.min',
		'tmpl': 'libs/jquery-plugin/jquery.tmpl.min',
		'validate': 'libs/jquery-plugin/jquery-validate/jquery.validate',
		'placeholder': 'libs/jquery-plugin/jquery.placeholder.min',
		'pub_validate': 'modules/common/global-validate',
		'message': 'modules/common/message',
		'global': 'modules/common/global',
		'dropdown': 'utils/dropdown',
		'ajaxform': 'utils/ajaxform',
	},
	shim: {
		'json': ['jquery'],
		'tmpl': ['jquery'],
		'validate': ['jquery'],
		'placeholder': ['jquery'],
		'message': ['jquery', 'tmpl'],
		'dropdown': ['jquery'],
		'ajaxform': ['json'],
		'global': ['message', 'dropdown'],
		'pub_validate':  ['jquery', 'validate']
	}
});

require(
['jquery','pub_validate','ajaxform','placeholder','global'],
function($){

	$(function(){
		$( 'input, textarea' ).placeholder();

		$( '#account_apply' ).click(function(e){
			e.preventDefault();
			loadings.show( 'Processing...' );
			$( '#apply_form' ).identalk_ajaxform({
				callback: function(result) {
					loadings.show( result.msg );
				}
			});
		});
	});
});