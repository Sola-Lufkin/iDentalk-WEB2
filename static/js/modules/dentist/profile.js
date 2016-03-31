define(
['jquery', 'lightbox', 'confirmbox'],
function(){
	var Profile = {
		_constructor: {
			url_pro: '/ajax/d/profile/',
			field: {
				id: '#den_field',
				row: '.field-row',
				tmpl_a: '#field_degree_tmpl',
				unchoice: '#den_field_unchoice',
				tmpl_b: '#field_degree_unchoice_tmpl',
				sub_btn: '#field_sub',
				url: '/ajax/d/profile/editfield/'
			},
			degree: {
				id: '#den_degree',
				row: '.degree-row',
				tmpl_a: '#field_degree_tmpl',
				unchoice: '#den_de_unchoice',
				tmpl_b: '#field_degree_unchoice_tmpl',
				sub_btn: '#degree_sub',
				url: '/ajax/d/profile/editdegree/'
			},
			workplace: {
				id: '#den_local',
				tmpl: '#local_tmpl',
				edit_btn: '.worklocation-edit',
				del_btn: '.worklocation-del',
				add_btn: '#worklocation_add'
			}
		},
		choice_edit: function(){
			$( '.choice-edit' ).each(function(){
				$( this ).click(function(){
					var $this = $( this );
					var type = $this.data( 'choicetype' );
					if( type == 'field' ){ 
						Profile.field.show( $this );
					}
					else{
						Profile.degree.show( $this );
					}
				});
			});
			Profile.field.init();
			Profile.degree.init();
		},
		get: function(url){
			$.ajax({
				url: url,
				success: function(result){
					Profile.degree.render( result );
					Profile.field.render( result );
				}
			});
		},
		field: {
			init: function(){
				this.sub();
			},
			show: function(target){
				var f = Profile._constructor.field;
				if( target.hasClass('open') ){
					this.close(target);
				}else{
					Profile.degree.close( $('.choice-edit.open') );
					target.text( 'Cancel' ).addClass('open')
						.prev().show().animate({right: 80});
					$( f.unchoice ).slideDown();
					$( f.row+' .choice-label' ).toggleClass( 'choiceable-label' );

					$( f.row+' .choice-label' ).unbind('click');
					$( f.row+' .choiceable-label' ).on('click',function(){
						$( this ).toggleClass( 'label-orange' );
					});
				}
			},
			close: function(target){
				var f = Profile._constructor.field;
				target.text('Edit').removeClass('open')
					.prev().hide().css({right: 30});
				$( f.unchoice ).slideUp();
				$( f.row+' .choice-label' ).removeClass( 'choiceable-label' );
			},
			render: function(result){
				var f = Profile._constructor.field;
				$( f.id ).empty();
				$( f.unchoice ).empty();

				$( f.id )
				.append(  $( f.tmpl_a )
				.tmpl( result.choice_feild ) );
				$( f.unchoice )
				.append(  $( f.tmpl_b )
				.tmpl( result.unchoice_feild ) );
			},
			sub: function(){
				var f = Profile._constructor.field;
				$( f.sub_btn ).click(function(){
					var c_list = [];
					var c = $( f.row+' .label-orange' );
					for( var i=0; i<c.length; i++ ){
						c_list.push(c.eq(i).text())
					}
					$.ajax({
						url: f.url,
						data: {
							tags: c_list.toString()
						},
						success: function( result ){
							loadings.autohide( result.msg );
							$( f.unchoice ).hide();
							Profile.field.close( $('.choice-edit.open') );
							Profile.get( Profile._constructor.url_pro );
						}
					});
				});
			}
		},
		degree: {
			init: function(){
				this.sub();
			},
			show: function(target){
				var d = Profile._constructor.degree;
				if( target.hasClass('open') ){
					this.close(target);
				}else{
					Profile.field.close( $('.choice-edit.open') );
					target.text( 'Cancel' ).addClass('open')
						.prev().show().animate({right: 80});
					$( d.unchoice ).slideDown();
					$( d.row+' .choice-label' ).toggleClass( 'choiceable-label' );

					$( d.row+' .choice-label' ).unbind('click');
					$( d.row+' .choiceable-label' ).on('click',function(){
						$( this ).toggleClass( 'label-orange' )
					});
				}
			},
			close: function(target){
				var d = Profile._constructor.degree;
				target.text('Edit').removeClass('open')
					.prev().hide().css({right: 30});
				$( d.unchoice ).slideUp();
				$( d.row+' .choice-label' ).removeClass( 'choiceable-label' );
			},
			render: function(result){
				var d = Profile._constructor.degree;
				$( d.id ).empty();
				$( d.unchoice ).empty();

				$( d.id )
				.append( $( d.tmpl_a )
				.tmpl( result.choice_degree ) );
				$( d.unchoice )
				.append( $( d.tmpl_b )
				.tmpl( result.unchoice_degree ) );
			},
			sub: function(){
				var d = Profile._constructor.degree;
				$( d.sub_btn ).click(function(){
					var c_list = [];
					var c = $( d.row+' .label-orange' );
					for( var i=0; i<c.length; i++ ){
						c_list.push(c.eq(i).text())
					}
					$.ajax({
						url: d.url,
						data: {
							tags: c_list.toString()
						},
						success: function( result ){
							loadings.autohide( result.msg );
							$( d.unchoice ).hide();
							Profile.degree.close( $('.choice-edit.open') );
							Profile.get( Profile._constructor.url_pro );
						}
					});
				});
			}
		},
		workplace: {
			init: function(){
				this.create();
				this.del();
				this.edit();
			},
			create: function(){
				var w = Profile._constructor.workplace;
				$( w.add_btn ).unbind( 'click' );
				$( w.add_btn ).identalk_lightbox({
					type: 'iframe',
					width: 770,
					height: 625,
					beforeOpen: function(e) {
						if( $( '#den_local table' ).length > 2 ) {
							loadings.autohide('Sorry, you hava added three work locations.');
							return true;
						}
					},
					afterClose: function(){
						Profile.get( Profile._constructor.url_pro );
					}
				});
			},
			render: function(result){
				var w = Profile._constructor.workplace;
				$( w.id ).empty()
				.append( $( w.tmpl )
				.tmpl( result.WorkPlaceList ) );
				$( '.local-num' ).each(function(index){
					$( this ).text( '0'+(index+1) );
				});
			},
			edit: function(){
				var w = Profile._constructor.workplace;
				$( w.edit_btn ).identalk_lightbox({
					type: 'iframe',
					width: 850,
					height: 800,
					afterClose: function(){
						Profile.get( Profile._constructor.url_pro );
					}
				});
			},
			del: function(){
				var w = Profile._constructor.workplace;
				$( w.del_btn ).bind('click',function(e){
					e.preventDefault();
					var lid = $( this ).data( 'localid' );
					$.ajax({
						url: $( this ).attr( 'href' ),
						success: function( result ){
							loadings.autohide( result.msg )
							$( '#local_'+lid ).slideUp(800, function(){
								$( this ).prev().remove();
								$( this ).remove();
							});
						}
					});
				}).confirmbox();
			}
		}
	}
	return Profile;
});