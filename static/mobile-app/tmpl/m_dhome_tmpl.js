<script id="field_degree_tmpl" type="text/x-jquery-tmpl">
    <span class="label label-orange pull-left choice-label" data-field_degree_id="${id}">${name}</span>
</script>

<script id="local_tmpl" type="text/x-jquery-tmpl">
    <table class="table table-striped" id="${id}">
        <tr><td>Clinic Name:</td><td>${clinic_name}</td></tr>
        <tr><td>Clinic Location:</td><td>${location}</td></tr>
        <tr><td>TEL:</td><td>${tel}</td></tr>
        <tr><td>Bussiness Hour:</td><td>${business_hour}</td></tr>
    </table>
</script>

<script id="gallery_tmpl" type="text/x-jquery-tmpl">
    <div class="case-list" data-caseid="${id}">
        <a data-ajax="false" href="/gallery/${uid}/case/${id}">
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