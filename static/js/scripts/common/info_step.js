require.config({
	baseUrl: '/site_static/js',
	paths: {
		'domReady': 'libs/domReady',
		'jquery': 'libs/jquery-1.8.3.min',
		'json': 'libs/jquery-plugin/jquery.json-2.3.min',
		'validate': 'libs/jquery-plugin/jquery-validate/jquery.validate',
		'tmpl': 'libs/jquery-plugin/jquery.tmpl.min',
		'jcrop': 'libs/jquery-plugin/jquery.Jcrop.min',
		'message': 'modules/common/message',
		'global': 'modules/common/global',
		'lightbox': 'utils/lightbox',
		'fileupload': 'utils/fileupload',
		'ajaxform': 'utils/ajaxform',
		'dropdown': 'utils/dropdown'
	},
	shim: {
		'json': ['jquery'],
		'tmpl': ['jquery'],
		'validate': ['jquery'],
		'jcrop': ['jquery'],
		'message': ['jquery', 'tmpl'],
		'global': ['message', 'dropdown'],
	}
});

require(
['jquery','ajaxform','fileupload','validate','jcrop','global','domReady!'],
function($){

	$( '#baseinfo_form' ).validate();

	$( '.next-step' ).each( function( index ){
		$( this ).click( function(){
			if( $('#baseinfo_form').valid() ){
				var count = index + 1;
				$( '.step' ).eq( count ).addClass( 'active' )
				.siblings().removeClass( 'active' );
				$( '.step-icon li' ).eq( count ).addClass( 'active' )
				.siblings().removeClass( 'active' );
			}else{
				return;
			}
		});
	});

	$( '.prev-step' ).each( function( index ){
		$( this ).click( function(){
			$( '.step' ).eq( index ).addClass( 'active' )
			.siblings().removeClass( 'active' );
			$( '.step-icon li' ).eq( index ).addClass( 'active' )
			.siblings().removeClass( 'active' );
		});
	});

	// 基本信息提交 STEP1
	$( '#sub_baseinfo' ).click( function(){
		if( $('#baseinfo_form').valid() ){
			$( '#baseinfo_form' ).identalk_ajaxform({
				callback: function( result ){
					loadings.autohide( result.msg )
				}
			});	
		}else{
			return;
		}
	});


	// 选择图片 STEP2
	$( '#choose_avatar' ).identalk_fileupload({
		form_target: 'file_upload_iframe',
		form_action: '/ajax/saveimg/',
		file_name: 'imagephoto',
		afterLoad: function(data){
			// remove the prev jcrop
			try{
				jcrop_api.destroy();
			}catch(e){}
			var data = data.split(',');
			$( '#ferret' ).attr( 'src', data[0])
				.css({width:data[1],height:data[2]});
			$( '#ferret' ).Jcrop({
				setSelect: [ 50, 10, 200, 200 ],
				aspectRatio: 1,
				onSelect: function(c){
					$('input[name="x1"]').val(c.x);
                    $('input[name="y1"]').val(c.y);
                    $('input[name="x2"]').val(c.x2);
                    $('input[name="y2"]').val(c.y2);  
				}
			},function(){
				jcrop_api = this;
			});
			$( '#upload_avatar' ).show().unbind('click').click(function(e){
        		e.preventDefault();
        		$( '#resize_form' ).identalk_ajaxform({
        			callback: function( result ){
   						loadings.autohide( result.msg );
						window.location.href = '/step-finished/';
        			}
        		});
        	});
		}
	});
}); 