define(
['jquery', 'lightbox', 'ajaxform'],
function(){

	var follow = function(target, url, fresh){
		if( url.indexOf('unconnect') !== -1 ){
			if( confirm('Are your sure to unconnect this dentist ?') ){
				$.ajax({
					url: url,
					success: function(result){
						target.attr( 'href', url.replace( 'unconnect','connect')).text('Connect');
						target.prev().show();
						if( fresh ){
							refresh();
						}else{
							loadings.autohide( result.msg );
						}
					}
				});
			}else{
				return;
			}
		}else{
			$.ajax({
				url: url,
				success: function(result){
					if( result.status ){
						if( url.indexOf('follow') !== -1 ){
							target.attr( 'href', url.replace('follow','unfollow')).text( 'Unfollow' );
						}
						if( url.indexOf('unfollow') !== -1 ){
							target.attr( 'href', url.replace('unfollow','follow')).text( 'Follow' );
						}
						if( url.indexOf('cancelrequest') !== -1 ){
							target.attr( 'href', url.replace( 'cancelrequest','connect')).text('Connect');
							target.prev().show();
						}
					}
					if( fresh ){
						refresh();
					}else{
						loadings.autohide( result.msg );
					}
				}
			});
		}
	}

	return function(){
		var fresh = arguments[0] || false;
		$( '.follow-action' ).unbind('click').on('click', function(e){
			e.preventDefault();
			if( $('.userinfo').length == 0 ){
			 	window.location.href = '/signup/p'
			}else{
				var $this = $( this );
				var url = this.href;
				if( url.indexOf('connect') !== -1 && url.indexOf('unconnect') == -1 ){
					$this.identalk_lightbox({
						height: 195,
						width: 372,
						open: true,
						content: '<form class="form" action=""> \
								<div class="control-group"> \
								<div class="controls clearfix ml10"> \
								<textarea class="span4" name="msg" row="10" placeholder="You can leave a message to the dentist"></textarea> \
								</div> \
								<div class="form-actions"><button type="button" class="sub-msg btn btn-success pull-right">OK</button></div> \
								</div> \
								</form>',
						afterLoad: function(){
							var wrapper = $( '.orange-content' )
							wrapper.find('.sub-msg').click(function(){
								wrapper.find( '.form' ).identalk_ajaxform({
									url: url,
									callback: function(result){
										if( result.status ){
											if( url.indexOf('connect') !== -1 ){
												$this.attr( 'href', url.replace( 'connect','cancelrequest')).text('Cancel connect');
												$this.prev().hide();
											}
										}
										$( '.orange-close' ).click();
										if( fresh ){
											refresh();
										}else{
											loadings.autohide( result.msg );
										}
									}
								});
							});
						}
					});
				}else{
					follow($this, url, fresh);
				}
			}
		});	
	}
});