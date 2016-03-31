require.config({
	baseUrl: '/site_static/js',
	paths: {
		'domReady': 'libs/domReady',
		'jquery': 'libs/jquery-1.8.3.min',
		'json': 'libs/jquery-plugin/jquery.json-2.3.min',
		'validate': 'libs/jquery-plugin/jquery-validate/jquery.validate',
		'tmpl': 'libs/jquery-plugin/jquery.tmpl.min',
		'message': 'modules/common/message',
		'global': 'modules/common/global',
		'gallery': 'modules/dentist/gallery',
		'ajaxform': 'utils/ajaxform',
		'btnmask': 'utils/btnmask',
		'dropdown': 'utils/dropdown',
		'lightbox': 'utils/lightbox',
		'confirmbox': 'utils/confirmbox',
		'valuecheck': 'utils/valuecheck'
	},
	shim: {
		'json': ['jquery'],
		'tmpl': ['jquery'],
		'validate': ['jquery'],
		'confirmbox': ['lightbox'],
		'message': ['jquery'],
		'global': ['message', 'dropdown'],
		'gallery': ['jquery', 'validate', 'json']
	}
});

require(
['jquery','gallery','lightbox','confirmbox','global'],
function($, gallery){

	$( '#den_gallery' ).addClass('active');

	gallery.upload( false, '#case_upload' );

	$( '.case_preview' ).hover(function(){
		$( this ).children( '.case_title' ).slideDown()
	},function(){
		$( this ).children( '.case_title' ).slideUp()
	});
	
	$( '#case_del' ).click(function(){
		var uid = $( this ).data( 'uid' );
		$.ajax({
			url: '/ajax/gallery/case/delete/',
			data: {
				case_id: $( this ).attr( 'rel' )
			},
			success: function( result ){
				window.location.href = '/gallery/'+uid+'/case/';
			}
		});
	}).confirmbox();

	$( '#case_edit' ).identalk_lightbox({
		autoheight: true,
		content: $( '.case-info-form' ).html(),
		afterLoad: function(){
			var wrapper = $( '.orange-wrap' );
			wrapper.find( '.update_caseinfo' ).click(function(e){
				e.preventDefault();
				$( this ).identalk_btnMask();
				wrapper.find('form').identalk_ajaxform({
					callback: function(result){
						loadings.autohide(result.msg);
						refresh();
					}
				});
			});
		}	
	});

	$( '.case-img-del' ).each(function(){
		$( this ).click(function(){
			var img_id = $( this ).attr( 'rel' );
			$.ajax({
				url: '/ajax/gallery/case/deleteimg/',
				data: {
					img_id: img_id
				},
				success: function( result ){
					if( result.status ){
						$( '#caseimg-'+img_id ).slideUp('slow');
						loadings.autohide( result.msg )
					}
				}
			});
		}).confirmbox();
	});

}); 