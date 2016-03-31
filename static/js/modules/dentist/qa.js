define(
['jquery','jquery-ui','ajaxform','validate','lightbox','tmpl','confirmbox'],
function(){
	var QA = {
		_constructor: {
			url_sub: '/ajax/d/putqa/',
			url_del: '/ajax/d/deleteqa/',
			url_update: '/ajax/d/updateqa/',
			url_sort: '/ajax/d/moveqaplace/'
		},
		init: function(){
			$( '.qa-item' ).hover(function(){
				$( '.qa-toobar' ).hide();
				$( this ).find( '.qa-toobar' ).show();
			}, function(){
				$( '.qa-toobar' ).hide();
			});
			this.update();
			this.del();
			this.sort();
		},
		create: function() {
			$( '#new_qa' ).identalk_lightbox({
				height: 385,
				width: 750,
				content: $( '.qa-form-wrap' ).html(),
				afterLoad: function() {
					var wrap = $( '.orange-wrap' );
					wrap.find( '.sub_qa' ).click(function(e){
						e.preventDefault();
						if( wrap.find( '.qa-form' ).valid() ) {
							wrap.find( '.qa-form' ).identalk_ajaxform({
								callback: function(result) {
									$( '.orange-close' ).click();
									loadings.autohide( result.msg );
									$( '#qa_list' ).children('.den-tip').hide().end()
									.append( $('#qa_tmpl').tmpl(result) );
									QA.init();
								}
							});
						}
					});
				}
			});
		},
		render: function(result) {
			if( result.length === 0 ) {
				$( '#qa_list .den-tip' ).show();
			} else {
				$( '#qa_list' ).empty()
				.append( $('#qa_tmpl').tmpl(result) );
			}
			
		},
		update: function() {
			$( '.update-qa' ).unbind('click').on('click', function(){
				var $this = $( this ),
					q = $this.parent().parent().siblings( '.question' ),
					a = $this.parent().parent().siblings( '.answer' ),
					addData = {
						id: $this.data( 'id' )
					};

				$( this ).identalk_lightbox({
					height: 385,
					width: 750,
					open: true,
					content: $( '.qa-form-wrap' ).html(),
					afterLoad: function() {
						var wrap = $( '.orange-wrap' );
						wrap.find('input[name="question"]').val( q.text() );
						wrap.find('textarea[name="answer"]').val( a.text() );
						wrap.find( '.sub_qa' ).click(function(e){
							e.preventDefault();
							wrap.find( '.qa-form' ).identalk_ajaxform({
								url: QA._constructor.url_update,
								addData: addData,
								callback: function(result) {
									$( '.orange-close' ).click();
									loadings.autohide( result.msg );
									q.text( result.question );
									a.text( result.answer );
								}
							});
						});	
					}
				});
			});
		},
		sort: function() {
			$( '#qa_list' ).sortable({ 
				axis: 'y',
				cursor: 'move',
				handle: '.sort-qa',
				opacity: 0.7,
				update: function(e, ui) {
					var $this = ui.item;
					var qa_list = [];
					$( '#qa_list li' ).each(function(){
						qa_list.push( $(this).data('id') );
					});
					var data = {
						ids: qa_list
					}
					$.ajax({
						url: QA._constructor.url_sort, 
						data: {
							ids: qa_list.toString()	
						},
						success: function(result) {
							loadings.autohide( result.msg );
						}
					});
				}
			});
		},
		del: function() {
				$( '.del-qa' ).unbind('click').bind('click', function(){
					var tid = $( this ).data( 'id' ),
						target = $('.qa-item[data-id="'+tid+'"]');
					$.ajax({
						url: QA._constructor.url_del, 
						data: {
							id: tid
						},
						success: function(result) {
							loadings.autohide( result.msg );
							target.slideUp();
						}
					});
				}).confirmbox();
			}
	}
	return QA;
});