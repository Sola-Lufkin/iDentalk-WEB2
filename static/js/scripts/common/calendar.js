require.config({
	baseUrl: '/site_static/js',
	paths: {
		'domReady': 'libs/domReady',
		'jquery': 'libs/jquery-1.8.3.min',
		'jquery-ui': 'libs/jquery-plugin/jquery-ui-1.10.1.custom.min',
		'json': 'libs/jquery-plugin/jquery.json-2.3.min',
		'tmpl': 'libs/jquery-plugin/jquery.tmpl.min',
		'validate': 'libs/jquery-plugin/jquery-validate/jquery.validate',
		'fullcalendar': 'libs/jquery-plugin/fullcalendar.min',
		'message': 'modules/common/message',
		'global': 'modules/common/global',
		'dropdown': 'utils/dropdown',
		'lightbox': 'utils/lightbox'
	},
	shim: {
		'jquery-ui': ['jquery'],
		'json': ['jquery'],
		'tmpl': ['jquery'],
		'validate': ['jquery'],
		'message': ['jquery'],
		'dropdown': ['jquery'],
		'lightbox': ['jquery'],
		'fullcalendar': ['jquery', 'jquery-ui'],
		'global': ['message', 'dropdown']
	}
});

require(
['jquery', 'fullcalendar', 'lightbox', 'json', 'global', 'domReady!'], 
function($){
	
	$('#pat_cal').addClass('active');

	var p_url = window.location.href;
	var pid = String(p_url.substring(p_url.indexOf('p/')+2).match(/\d+/g));

	var calendar = $( '#calendar' ).fullCalendar({
		 header: {
			// left: 'month,basicWeek,basicDay',
			left: '',
			center: 'title',
			right: 'today prev,next'
		},
		selectable: true,
		editable: true,
		selectHelper: true,
		select: function(start, end, allDay) {
			$( this ).identalk_lightbox({
				autoheight: true,
				autowidth: true,
				content: $( '#event_form_wrap' ).html(),
				open: true,
				afterLoad: function(){
					var wrap = $( '.orange-content' );
					wrap.find( '.sub-event' ).click(function(e){
						e.preventDefault();
						var data = {
							pid: pid,
							title: wrap.find( 'input[name="title"]' ).val(),
							content: wrap.find( 'textarea[name="event"]' ).val(),
							start: $.fullCalendar.formatDate(start,'yyyy-MM-dd HH:mm:ss'),
							end: $.fullCalendar.formatDate(end,'yyyy-MM-dd HH:mm:ss'),
							allDay: allDay
						}
						$.ajax({
							url: '/p/putcalendar/',
							data: {
								data: $.toJSON(data)
							},
							success: function(result) {
								calendar.fullCalendar('renderEvent', {
									id: result.id,
									content: result.content,
									title: result.title,
									start: result.start,
									end: result.end,
									allDay: result.allDay
								}, true);
								$( '.orange-close' ).click();
								loadings.autohide( 'success' );
							}
						});
					});
				}
			});
		},
		eventDrop: function(event,dayDelta,minuteDelta,allDay,revertFunc) {
			var data = {
				id: event.id,
				title: event.title,
				content: event.content,
				start: $.fullCalendar.formatDate(event.start,'yyyy-MM-dd HH:mm:ss'),
				end: $.fullCalendar.formatDate(event.end,'yyyy-MM-dd HH:mm:ss'),
				allDay: event.allDay
			}
			$.ajax({
				url: '/p/updatecalendar/',
				data: {
					data: $.toJSON( data )
				},
				success: function(result) {
					loadings.autohide( 'success' );
				}
			});
		},
		eventResize: function(event,dayDelta,minuteDelta,revertFunc) {
			var data = {
				id: event.id,
				title: event.title,
				content: event.content,
				start: $.fullCalendar.formatDate(event.start,'yyyy-MM-dd HH:mm:ss'),
				end: $.fullCalendar.formatDate(event.end,'yyyy-MM-dd HH:mm:ss'),
				allDay: event.allDay
			}
			$.ajax({
				url: '/p/updatecalendar/',
				data: {
					data: $.toJSON( data )
				},
				success: function(result) {
					loadings.autohide( 'success' );
				}
			});
		},
		eventSources: [
	        {
				url: '/p/getcalendar/',
				type: 'POST',
				data: {
					pid: pid
				},
				error: function() {
					loadings.show( 'error' );
				},
				color: 'blue',
			}
	    ],
		eventClick: function(calEvent, jsEvent, view) {
			var content = '<form class="form-horizontal event-form" method="POST" action=""> \
							<div class="control-group"> \
							<label class="control-label">Event</label> \
							<div class="controls"> \
								<input type="text" class="input" name="title" value="'+calEvent.title+'" /> \
								<textarea class="span3" name="event">'+calEvent.content+'</textarea> \
							</div> \
							</div> \
							<div class="form-actions"> \
								<button type="submit" class="btn btn-orange update-event pull-right">Add</button> \
								<a href="javascript:;" class="del-event">del</a> \
							</div> \
							</form>';
			$( this ).identalk_lightbox({
				autoheight: true,
				autowidth: true,
				content: content,
				open: true,
				afterLoad: function() {
					var wrap = $( '.orange-content' );
					wrap.find( '.update-event' ).click(function(e){
						e.preventDefault();
						var data = {
							id: calEvent.id,
							title: wrap.find('input[name="title"]').val(),
							content: wrap.find('textarea[name="event"]').val(),
							start: $.fullCalendar.formatDate(calEvent.start,'yyyy-MM-dd HH:mm:ss'),
							end: $.fullCalendar.formatDate(calEvent.end,'yyyy-MM-dd HH:mm:ss'),
							allDay: calEvent.allDay
						}
						$.ajax({
							url: '/p/updatecalendar/',
							data: {
								data: $.toJSON(data)
							},
							success: function(result) {
								calEvent.title = result.title;
								calEvent.content = result.content;
								calendar.fullCalendar('updateEvent', calEvent);
								$( '.orange-close' ).click();
								loadings.autohide( 'success' );
							}
						});
					});

					wrap.find( '.del-event' ).click(function(){
						$.ajax({
							url: '/p/deletecalendar/',
							data: {
								id: calEvent.id 
							},
							success: function(result) {
								calendar.fullCalendar('removeEvents', calEvent.id);
								$( '.orange-close' ).click();
								loadings.autohide( 'success' );
							}
						});
					});
				}
			});
		}
	});

});