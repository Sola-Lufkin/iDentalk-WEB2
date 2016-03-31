<script id="message_sender_tmpl" type="text/x-jquery-tmpl">
	<div class="row well">
		{% templatetag openvariable %}if own{% templatetag closevariable %}
		<div class="span10">${content}</div>
		<a href="/d/${uid}" class="span1">
			<img src="${avatar}" alt="${name}" title="${name}">
		</a>
		<div class="pull-right muted">${date}</div>
		{% templatetag openvariable %}else{% templatetag closevariable %}
		<a href="/p/${uid}" class="span1">
			<img src="${avatar}" alt="${name}" title="${name}">
		</a>
		<div class="span10">${content}</div>
		<div class="pull-left muted">${date}</div>
		{% templatetag openvariable %}/if{% templatetag closevariable %}
	</div>
</script>