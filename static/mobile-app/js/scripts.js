$(document).bind('pageinit',function(){
	$.ajaxSetup({
		type: 'POST',
		cache: false
	});

	$.fn.identalk_dropdown = function( opts ){
		this.each(function(){
			var $this = $( this );
			$this.click(function( e ){
				e.preventDefault();
				if( $this.next().hasClass('hide') ){
					$this.next().slideDown().removeClass('hide');
				}else{
					$this.next().slideUp().addClass('hide');
				}
			});
		});
		return this;
	}

	/* Index */
	$( '.turn-wrap' ).click(function(){
		var t = $( this ).attr('href');
		$( '.section' ).hide();
		$( t ).show();
	});

	$( '.dropable' ).identalk_dropdown();

	/* Send message */
	$( '.sub-message' ).click(function(e){
		e.preventDefault();
		$.ajax({
			url: $( '#message_form' ).attr('action'),
			data: {
				'contact-id': $('input[name="contact-id"]').val(),
				content: $('textarea[name="content"]').val()
			},
			success: function(result){
				window.location.reload();
			}
		});
	});

	/* List type change */
	/* Patient list chage & Dentist list change & Dentist homepage tab change */
	$( '.type-choose' ).each(function(index){
		$( this ).click(function(e){
			e.preventDefault();
			var $this = $( this );
			$( '.type-choose' ).removeClass('ui-btn-active');
			$this.addClass('ui-btn-active');
			var link = $this.data('link'),
				type = $this.attr('id');
			if( link !== undefined ){
				$.ajax({
					url: link,
					success: function(result){
						$( '.type-list' ).hide().eq(index).fadeIn();
						switch(type){
							case 'pro_btn':
								$( '#den_field' ).empty()
								.append( $('#field_degree_tmpl').tmpl(result.choice_feild) );
								$( '#den_degree' ).empty()
								.append( $('#field_degree_tmpl').tmpl(result.choice_degree) );
								$( '#den_local' ).empty()
								.append( $('#local_tmpl').tmpl(result.WorkPlaceList) );
								break;
							case 'post_btn':
								$( '#msg_flow' ).empty()
								.append( $('#post_tmpl').tmpl(result) );
								break;
							case 'case_btn':
								$( '#gallery_list' ).empty()
								.append( $('#gallery_tmpl').tmpl(result) );
								break;
						}
					}
				});
			}else{
				$( '.type-list' ).hide().eq(index).fadeIn();
			}
		});
	});

	/* Dentist profile */
	$( '#pro_btn' ).click();

});