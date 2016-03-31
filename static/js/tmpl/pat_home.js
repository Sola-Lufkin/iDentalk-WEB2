<script id="stream_tmpl" type="text/x-jquery-tmpl">
    <div class="stream row-fluid" id="stream_${id}">
    	<div class="stream-content clearfix ">
	    	<dl class="span3">
		    	<dt>
                <div class="stream-avatar-wrap">
                <a href="/d/${dentist_id}"><img class="stream-avatar" src="${imagephoto}" /></a>
                </div>
                </dt>
	    	</dl>
	    	<div class="span9 mb10 mt10">
	    		<div class="stream-name">${name}</div>
	    		<div class="stream-date muted small pull-right" title="${date}">${humandate}</div>
                <div class="span12 mt10 stream-detail">
                    <p>
                    {% templatetag openvariable %}each url{% templatetag closevariable %}
                    <a href="${$value.url}">${$value.name}</a>
                    {% templatetag openvariable %}/each{% templatetag closevariable %}  
                    {% templatetag openvariable %}html content{% templatetag closevariable %}
                    </p>
                    {% templatetag openvariable %}if img_s{% templatetag closevariable %}
                    <a href="${img_s}" class="upload-img zoom-pic" data-big-pic="${img_m}">
                        <img src="${img_s}">
                    </a>
                    {% templatetag openvariable %}/if{% templatetag closevariable %}
                </div>
                <div class="stream-toolbar pull-left">
                    <a href="javascript:;" class="comment" rel="${id}">
                        <span class="stream-point comment-point">.</span>
                        <span class="comment-count">${comments}</span> COMMENTS
                    </a>
                </div>
	    	</div>
        </div>
        <div id="comments_${id}" class="comment-box hide row-fluid bg-green">
            <div class="comment-wrap clearfix">
                <div id="comments-tree_${id}" class="span12 comment-table comment-pa"></div>
                <textarea class="comment-input" name="comment-content" rel="${id}" placeholder="Add a comment..."></textarea>
                <button type="button" class="btn btn-gray pull-right sub-comment" rel="${id}">Reply</button>
                
            </div>
        </div>
    </div>
</script>

<script id="comment_tmpl" type="text/x-jquery-tmpl">
    <div class="comment-list clearfix mb3 mt10" id="comment_${id}">
        {% templatetag openvariable %}if comment_identity=="P"{% templatetag closevariable %}
        <span class="stream-point p-point">.</span>
        {% templatetag openvariable %}else{% templatetag closevariable %} 
        <span class="stream-point d-point">.</span>
        {% templatetag openvariable %}/if{% templatetag closevariable %}
        <span class="comment-name">${username}
        <div class="stream-date muted small pull-right" title="${date}">${humandate}</div>
    </div>
    <div class="mb10">
        ${content}
    </div>
</script>