<script id="post_tmpl" type="text/x-jquery-tmpl">
    <div class="stream row-fluid" id="stream_${id}">
        <div class="stream-content clearfix">
            <dl class="span3">
                <dt><img src="${imagephoto}" /></dt>
            </dl>
            <div class="stream-date muted pull-right">${date}</div>
            <div class="span9 clearfix">
                <div class="lead">
                    <strong>${name}:</strong>
                </div> 
                <div class="post-content">${content}</div>
                <div class="stream-toolbar pull-right">
                    <a href="/stream/getpost/${id}" data-ajax="false" class="comment" rel="${id}">Comment(<span class="comment-count">${comments}</span>)</a>
                </div>
            </div>
        </div>
    </div>
</script>