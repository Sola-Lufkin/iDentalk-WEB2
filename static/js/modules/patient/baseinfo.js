define(
['jquery','datepicker','ajaxform','validate'],
function(){
	var Baseinfo = {
		_constructor: {
			sub_btn_case: '#sub_pathology',
			form_case: '#pathology_form',
			sub_btn_base: '#sub_baseinfo',
			form_base: '#base_info_form',
			sub_btn_local: '#sub_locaiton',
			form_local: '#location_form'
		},
		init: function(){
			this.edit();
			this.sub();
			this.navlist();
		},
		navlist: function(){
			$( '.nav-list li' ).click(function(){
				$( this ).addClass( 'active' )
				.siblings().removeClass('active');
			});
		},
		edit: function(){
			$( 'input[name="birthday"]' ).datepicker({
				format: 'mm-dd-yyyy'
			});
			$( '.noneabove' ).each(function(){
				$( this ).click(function(){
					var checklist = $( this ).attr( 'name' );
					if( this.checked ){
						$( 'input[name="'+checklist+'"]' ).not('.noneabove').attr( 'checked', false);
					}
				});
			});
			$( ':checkbox' ).not('.noneabove').each(function(){
				$( this ).click(function(){
					if( this.checked ){
						$( '.'+$(this).attr('name') ).find( '.noneabove' ).attr( 'checked', false )
					}
				});
			});
		},
		sub: function(){
			var b = Baseinfo._constructor;
			$( b.sub_btn_case ).click(function(){
				$( b.form_case ).identalk_ajaxform({
					checklist: 'dental_problem,dental_treatment,oral_habits',
					callback: function(result){
						loadings.autohide( result.msg );	
					}
				});
			});

			$( b.sub_btn_base ).click(function(e){
				e.preventDefault();
				if($( b.form_base ).valid()){
					$( b.form_base ).identalk_ajaxform({
						callback: function(result){
							loadings.autohide( result.msg );
						}
					});
				}else{
					return;
				}
			});

			$( b.sub_btn_local ).click(function(){
				if( $('#latlng').val() === '' ) {
					if(confirm("We can't find you on Google, are you sure to save this address?")) {
						$.ajax({
							url: $( b.form_local ).attr('action'),
							data: {
								location: $( '#location' ).val(),
								latlng: $( 'input[name="latlng"]' ).val()
							},
							success: function(result){
								loadings.autohide( result.msg );
							}
						});
					}
				} else {
					$.ajax({
						url: $( b.form_local ).attr('action'),
						data: {
							location: $( '#location' ).val(),
							latlng: $( 'input[name="latlng"]' ).val()
						},
						success: function(result){
							loadings.autohide( result.msg );
						}
					});
				}
			});
		}
	}
	return Baseinfo;
});