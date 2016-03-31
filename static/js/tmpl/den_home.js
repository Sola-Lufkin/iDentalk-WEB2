<script id="stream_tmpl" type="text/x-jquery-tmpl">
    <div class="stream row-fluid" id="stream_${id}">
        <div class="stream-content clearfix">
            <dl class="span3">
                <dt>
                    <div class="stream-avatar-wrap">
                        <img class="stream-avatar" src="${imagephoto}" />
                    </div>
                </dt>
            </dl>
            <div class="span9 mb10 mt10">
                <div class="stream-name">${name}</div>
                <div class="stream-date muted pull-right" title="${date}">${humandate}</div>
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
                <div class="pull-left">
                    <a href="javascript:;" class="comment" rel="${id}">
                        <span class="stream-point comment-point">.</span>
                        <span class="comment-count">${comments}</span> COMMENTS
                    </a>
                </div>
                <div class="stream-toolbar invisible pull-right">
                    {% if is_private %}<a href="javascript:;" data-btn="Close, Delete" data-msg="Are you sure to delete this Post?" title="DELETE" class="icon-trash pull-right post-del" rel="${id}"></a>{% endif %}
                </div>
            </div> 
        </div>
        <div id="comments_${id}" class="comment-box hide row-fluid bg-green">
            <div class="comment-wrap clearfix">
                <div id="comments-tree_${id}" class="span12 comment-table"></div>
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
        <span class="comment-name">${username}</span>
        <div class="stream-date muted small pull-right" title="${date}">
            {% if own %}<a class="del-comment icon-trash" title="DELETE" data-btn="Close, Delete" data-title="Are you sure to delete this Comment?" href="javascript:;" rel="${id}"></a>{% endif %}
            &nbsp
            ${humandate}
        </div>
    </div>
    <div class="mb10 comment-detail">
        ${content}
    </div>
</script>

<script id="field_degree_tmpl" type="text/x-jquery-tmpl">
    <span class="label label-orange pull-left choice-label" data-field_degree_id="${id}">${name}</span>
</script>

<script id="field_degree_unchoice_tmpl" type="text/x-jquery-tmpl">
    <span class="label pull-left choice-label" data-field_degree_id="${id}">${name}</span>
</script>

<script id="local_tmpl" type="text/x-jquery-tmpl">
<div class="local-num"></div>
<table class="table table-striped end-line" id="local_${id}">
    <tr><td>Clinic Name:</td><td>${clinic_name}</td></tr>
    <tr><td>Clinic Location:</td><td>${location}</td></tr>
    <tr><td>TEL:</td><td>${tel}</td></tr>
    <tr><td>Bussiness Hour:</td><td>${business_hour}</td></tr>
    {% if is_private %}
    <tr><td></td><td>
    <a class="worklocation-edit" href="/ajax/d/profile/editclinic/${id}">Edit</a>| 
    <a class="worklocation-del" href="/ajax/d/profile/deleteclinic/${id}" data-btn="Close, Delete" data-msg="Are you sure to delete this wolklocation?" data-localid="${id}">Del<a></td></tr>
    {% endif %}
</table>
</script>

<script id="gallery_tmpl" type="text/x-jquery-tmpl">
    <div class="case_list" data-caseid="${id}">
        <a href="/gallery/${uid}/case/${id}">
        <dt>${case_name}</dt>
        <div class="case_img_wrapper">
            {% templatetag openvariable %}if bef_img{% templatetag closevariable %}
            <dd><img class="case_list_img" src="${bef_img}"></dd>
            {% templatetag openvariable %}else{% templatetag closevariable %}
            <dd><img class="case_list_img" src="/site_static/img/head_50_50.png"></dd>
            {% templatetag openvariable %}/if{% templatetag closevariable %}
        </div>
        </a>
    </div>
</script>
<script id="qa_tmpl" type="text/x-jquery-tmpl">
    <li class="qa-item" data-place="${place}" data-id="${id}">
        {% if is_private %}
        <div class="clearfix" style="height:20px;">
            <div class="qa-toobar pull-right hide">
                <a href="javascript:;" class="del-qa qa-action icon-remove" data-msg="Are you sure to delete this Q&A?" data-id="${id}"></a>
                <a href="javascript:;" class="update-qa qa-action icon-edit" data-id="${id}"></a>
                <a href="javascript:;" class="sort-qa qa-action icon-move" data-id="${id}"></a>
            </div>
        </div>
        {% endif %}
        <h3 class="question">${question}</h3>
        <div class="answer">${answer}</div>
    </li>
</script>
