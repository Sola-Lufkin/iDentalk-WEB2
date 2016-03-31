require.config({
	baseUrl: '/site_static/js',
	paths: {
		// 'domReady': 'libs/domReady',
		'jquery': 'libs/jquery-1.8.3.min',
		'jquery-ui': 'libs/jquery-plugin/jquery-ui-1.10.1.custom.min',
		'json': 'libs/jquery-plugin/jquery.json-2.3.min',
		'history': 'libs/jquery-plugin/jquery.history',
		'tmpl': 'libs/jquery-plugin/jquery.tmpl.min',
		'validate': 'libs/jquery-plugin/jquery-validate/jquery.validate',
		'jcrop': 'libs/jquery-plugin/jquery.Jcrop.min',
		'placeholder': 'libs/jquery-plugin/jquery.placeholder.min',
		'message': 'modules/common/message',
		'global': 'modules/common/global',
		'avatar': 'modules/common/avatar',

		'd_baseinfo': 'modules/dentist/baseinfo',
		'gallery': 'modules/dentist/gallery',
		'd_stream': 'modules/dentist/stream',
		'qa': 'modules/dentist/qa',
		'd_profile': 'modules/dentist/profile',


		'ajaxform': 'utils/ajaxform',
		'btnmask': 'utils/btnmask',
		'dropdown': 'utils/dropdown',
		'fileupload': 'utils/fileupload',
		'lightbox': 'utils/lightbox',
		'valuecheck': 'utils/valuecheck',
		'confirmbox': 'utils/confirmbox'
	},
	shim: {
		'jquery-ui': ['jquery'],
		'json': ['jquery'],
		'tmpl': ['jquery'],
		'validate': ['jquery'],
		'jcrop': ['jquery'],
		'confirmbox': ['lightbox'],
		'history': ['jquery'],
		'placeholder': ['jquery'],
		'message': ['jquery', 'dropdown'],
		'global': ['message'],
		'gallery': ['lightbox','json'],
		'd_baseinfo': ['lightbox', 'ajaxform'],
		'd_stream': ['validate'],
		'qa': ['jquery-ui'],
		'd_profile': ['lightbox'],
		'avatar': ['jcrop']
	}
});

require(
['jquery','avatar','d_baseinfo','gallery','d_stream','qa','d_profile','placeholder','history','global'], 
function($, avatar, baseinfo, gallery, stream, qa, profile){
	
	$( '#den_home' ).addClass( 'active' );
	$( '#content' ).addClass( 'den-bg-content' );
	$( '#wrapper' ).addClass( 'den-bg-home' );

	$( 'textarea' ).placeholder();

	var urls = {
		url_pro: '/ajax/d/profile/',
		url_gallery: '/ajax/d/gallery/getcases/',
		url_post: '/ajax/d/stream/getpost/',
		url_qa: $( '.btn-qa' ).data( 'link' )
	}

	var History = window.History;

	// url change use HTML5 history
	var	route_change = function(url){
		var _fadeTime = 500;
		if( !History.enabled ){
			// var url = url;
			// var hash_url = url.replace('#','')
			var url = '/d/home/'+ url.replace('#','') ;
		}
		$.ajax({
			url: url,
			success: function( result ){
				$( '.den-block' ).hide();
				if( url.indexOf('stream') !== -1){
					tab_change( '.btn-post' );
					stream.post.render( result );
					$( '#timeline' ).fadeIn(_fadeTime, function(){
						stream.post.init();
						stream.post.del();
						stream.comment.init();
					});
				}
				if( url.indexOf('profile') !== -1 ){
					tab_change( '.btn-profile' );

					profile.degree.render( result );
					profile.field.render( result );

					profile.workplace.render( result );

					$( '#profile' ).fadeIn(_fadeTime, function(){
						profile.workplace.init();
					});
				}
				if( url.indexOf('qa') !== -1 ) {
					tab_change( '.btn-qa' );
					qa.render( result );
					
					$( '#qa' ).fadeIn(_fadeTime, function(){
						qa.init();	
					});
				}
				if( url.indexOf('gallery') !== -1 ){
					tab_change( '.btn-gallery' );
					gallery.render( result );
					$( '#gallery' ).fadeIn(_fadeTime);
				}
			}
		});
	}

	// Home & Profile & Gallery TAB CHANGE
	var	tab_change = function( opt ){
		$( opt ).addClass( 'disabled active' )
		.siblings().removeClass( 'disabled active' )
	}

	// HTML4 browsers
	if ( !History.enabled ) {
        $( window ).on('hashchange',function(){
        	var hash = window.location.hash;
        	route_change( hash );
        });
    }
    // history改变绑定方法
    History.Adapter.bind(window,'statechange',function(){ // Note: We are using statechange instead of popstate
        var State = History.getState(); // Note: We are using History.getState() instead of event.state
        // History.log(State.data, State.title, State.url);
        route_change( State.data.state )
    });

	var first_load = function(){
		var href = window.location.href,
			d = urls; 
		if( href.indexOf('Profile') !== -1 ){
			route_change( d.url_pro );
			return;
		}
		if( href.indexOf('Gallery') !== -1 ){
			route_change( d.url_gallery );
			return;
		}
		if( href.indexOf('Q&A') !== -1 ) {
			route_change( d.url_qa );
			return;
		}
		else{
			route_change( d.url_post );
		}
	}

	// dentist 主页按钮切换
	var	den_tab = function(){
		$( '.den-tab' ).each(function( index ){
			$( this ).click(function( e ){
				e.preventDefault();
				var $this = $( this );
				if( $this.hasClass('disabled') ){
					return;
				}
				$( '.den-block' ).hide();
				var url = $this.data('link'),
					hash = this.rel,
					title = $this.data( 'title' );

				$this.addClass( 'active' ).siblings()
				.removeClass( 'active' );
				if( !History.enabled ){
					window.location.hash = hash;	
				}else{
					History.pushState({state:url}, title+'-iDentalk', title);
				}
			});
		});
	}

	baseinfo.init();
	profile.choice_edit();
	gallery.newcase.init();
	
	qa.create();

	var popup_avatar = avatar.popup_avatar();
	popup_avatar.init();

	first_load();
	den_tab();

});