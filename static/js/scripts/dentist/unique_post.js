require.config({
	baseUrl: '/site_static/js',
	paths: {
		'domReady': 'libs/domReady',
		'jquery': 'libs/jquery-1.8.3.min',
		'json': 'libs/jquery-plugin/jquery.json-2.3.min',
		'tmpl': 'libs/jquery-plugin/jquery.tmpl.min',
		'validate': 'libs/jquery-plugin/jquery-validate/jquery.validate',
		'global': 'modules/common/global',
		'message': 'modules/common/message',
		'lightbox': 'utils/lightbox',
		'confirmbox': 'utils/confirmbox',
		'dropdown': 'utils/dropdown',
		'valuecheck': 'utils/valuecheck',
		'btnmask': 'utils/btnmask',
	},
	shim: {
		'json': ['jquery'],
		'tmpl': ['jquery'],
		'confirmbox':['lightbox'],
		'validate': ['jquery'],
		'message': ['jquery', 'tmpl'],
		'global': ['message', 'dropdown']
	}
});

require(
['jquery','valuecheck','btnmask','lightbox','confirmbox','global','domReady!'], 
function($){

	$( '.del-comment' ).click(function(){
		var cid = this.rel;
		$.ajax({
			url: '/ajax/d/stream/deletecomment/',
			data: {
				cid: cid 
			},
			success: function( result ){
				if( result.status ){
					$( '#comment_'+cid ).fadeOut();
				}
				loadings.autohide( result.msg );
			}
		});
	}).confirmbox();

	$( '.sub-comment' ).click(function(){
		var $this = $( this );
		var pid = $this.attr( 'rel' ),
			comment = $this.prev().val();
		if( !$this.prev().identalk_valuecheck() ){
			return;
		}else{
			$this.identalk_btnMask('open');
			$.ajax({
				url: '/ajax/stream/comment/',
				data: {
					pid: pid,
					comment: $( this ).prev().val()
				},
				success: function(result){
					if( result.status ){
						$( '.comment-input' ).val('')
						refresh();
					}
				}
			});
		}
	});
}); 