require.config({
	baseUrl: '/site_static/js',
	paths: {
		'jquery': 'libs/jquery-1.8.3.min',
		'json': 'libs/jquery-plugin/jquery.json-2.3.min',
		'tmpl': 'libs/jquery-plugin/jquery.tmpl.min',
		'validate': 'libs/jquery-plugin/jquery-validate/jquery.validate',
		'placeholder': 'libs/jquery-plugin/jquery.placeholder.min',
		'message': 'modules/common/message',
		'global': 'modules/common/global',
		'dropdown': 'utils/dropdown',
		'fileupload': 'utils/fileupload',
		'ajaxform': 'utils/ajaxform'
	},
	shim: {
		'json': ['jquery'],
		'tmpl': ['jquery'],
		'fileupload': ['jquery'],
		'placeholder': ['jquery'],
		'validate': ['jquery'],
		'message': ['jquery', 'tmpl'],
		'dropdown': ['jquery'],
		'global': ['message', 'dropdown'],
	}
});

require(
['jquery','validate','placeholder','ajaxform','fileupload','global'],
function($){

	$( '.tab' ).click(function(){
		$( this ).addClass( 'active' ).siblings().removeClass( 'active' );
		$( '.content-inner' ).hide();
		$( '#'+$(this).data('target') ).show();
	});

	$( '.upload-prove' ).identalk_fileupload({
		form_target: 'file_upload_iframe',
		form_action: '/d/profile/addprovepic/',
		file_name: 'prove_pic',
		afterLoad: function(data){
			loadings.autohide( 'Success' );
			$( '.pre-pic' ).html('<img src="'+data+'">'); 
		}
	});

	$( '#identify-panel form' ).validate();

	$( 'textarea' ).placeholder();

	$( '.invite-btn' ).click(function(e){
		var invite_form = $( '#invite-panel form' );
		var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
		e.preventDefault();
		if( invite_form.valid() ) {
			var email_list = invite_form.find( 'textarea' ).val().split(',')
			var valid = false;
			for(var i = 0; i < email_list.length; i++) {
				if( re.test($.trim(email_list[i])) ) {
					valid = true;
				} else {
					valid = false;
				}
			}
			if( valid === true ) {
				loadings.show('Sending...');
				invite_form.identalk_ajaxform({
					callback: function(result){
						loadings.autohide(result.msg)
					}
				});
			} else {
				loadings.autohide( 'Email address not valid');
			}
		} else {
			return;
		}
	});

});