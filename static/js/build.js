({
	baseUrl: '.',
	dir: 'js-build',
	paths: {
		/* Libs */
		'domReady': 'libs/domReady',
		'Modernizr': 'libs/modernizr.custom.14207',
		'jquery': 'libs/jquery-1.8.3.min',
		'jquery-ui': 'libs/jquery-plugin/jquery-ui-1.10.1.custom.min',

		/* Plugins */
		'fullcalendar': 'libs/jquery-plugin/fullcalendar.min',
		'json': 'libs/jquery-plugin/jquery.json-2.3.min',
		'history': 'libs/jquery-plugin/jquery.history',
		'validate': 'libs/jquery-plugin/jquery-validate/jquery.validate',
		'tmpl': 'libs/jquery-plugin/jquery.tmpl.min',
		'jcrop': 'libs/jquery-plugin/jquery.Jcrop.min',
		'gmap3': 'libs/gmap3.min',
		'autocomplete': 'libs/jquery-plugin/jquery-autocomplete.min',
		'datepicker': 'libs/jquery-plugin/bootstrap-datepicker/bootstrap-datepicker',
		'timepicker': 'libs/jquery-plugin/jquery.timepicker.min',
		'placeholder': 'libs/jquery-plugin/jquery.placeholder.min',

		/* Custome plugin */
		'ajaxform': 'utils/ajaxform',
		'btnmask': 'utils/btnmask',
		'dropdown': 'utils/dropdown',
		'fileupload': 'utils/fileupload',
		'lightbox': 'utils/lightbox',
		'scrollspy': 'utils/scrollspy',
		'slide': 'utils/slide',
		'valuecheck': 'utils/valuecheck',
		'confirmbox': 'utils/confirmbox',


		/* Custome modules */
		'pub_validate': 'modules/common/global-validate',
		'message': 'modules/common/message',
		'global': 'modules/common/global',
		'mail': 'modules/common/mail',
		'avatar': 'modules/common/avatar',
		'contact': 'modules/common/contact',
		/* Dentist */
		'd_baseinfo': 'modules/dentist/baseinfo',
		'gallery': 'modules/dentist/gallery',
		'd_stream': 'modules/dentist/stream',
		'qa': 'modules/dentist/qa',
		'd_profile': 'modules/dentist/profile',
		/* Patient */
		'p_baseinfo': 'modules/patient/baseinfo',
		'p_stream': 'modules/patient/stream',
		'followAction': 'modules/patient/follow_action',
	},
	modules: [
		/* Common */
		{
			name: 'scripts/common/index'
		},
		{
			name: 'scripts/common/info_step'
		},
		{
			name: 'scripts/common/notification'
		},
		{
			name: 'scripts/common/settings'
		},
		/* Densit */
		{
			name: 'scripts/dentist/den_homepage'
		},
		{
			name: 'scripts/dentist/den_public'
		},
		{
			name: 'scripts/dentist/gallery_edit'
		},
		{
			name: 'scripts/dentist/manage_pat'
		},
		{
			name: 'scripts/dentist/unique_post'
		},
		{
			name: 'scripts/dentist/worklocation_edit'
		},
		{
			name: 'scripts/dentist/den_mail'
		},
		/* Patient */
		{
			name: 'scripts/patient/pat_edit'
		},
		{
			name: 'scripts/patient/pat_homepage'
		},
		{
			name: 'scripts/patient/search'
		},
		{
			name: 'scripts/common/calendar'
		},
		{
			name: 'scripts/patient/pat_mail'
		}

	]
	// name: 'scripts/common/index',
	// out: 'index-build.js'
})