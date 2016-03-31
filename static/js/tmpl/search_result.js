<script type="text/x-jquery-tmpl" id="searchresult_tmpl">
    <div class="result-list row-fluid">
        <a href="/d/${dentistid}" class="pull-left"><img class="thumbnail" src="${avatar}" alt=""></a>
        <div class="span10 ml10">
            <h3 class="clearfix">
                <a href="/d/${dentistid}">${dentistname}</a>
                <div class="btn-group pull-right">
                    {% templatetag openvariable %}if status=="-1"{% templatetag closevariable %}
                    <a href="/ajax/relationship/follow/${dentistid}" class="follow-action btn" >Follow</a>
                    <a href="/ajax/relationship/connect/${dentistid}" class="follow-action btn">Connect</a>
                    {% templatetag openvariable %}else status=="0"{% templatetag closevariable %}
                    <a href="/ajax/relationship/unfollow/${dentistid}" class="follow-action btn" >Unfollow</a>
                    <a href="/ajax/relationship/connect/${dentistid}" class="follow-action btn">Connect</a>
                    {% templatetag openvariable %}else status=="1"{% templatetag closevariable %}
                    <a href="/ajax/relationship/cancelrequest/${dentistid}" class="follow-action btn">Cancel Connect</a>
                    {% templatetag openvariable %}else status=="2"{% templatetag closevariable %}
                    <a href="/ajax/relationship/unfollow/${dentistid}" class="follow-action btn" >Unfollow</a>
                    <a href="/ajax/relationship/unconnect/${dentistid}" class="follow-action btn">UnConnect</a>
                    {% templatetag openvariable %}/if{% templatetag closevariable %}
                </div>
            </h3>
            <div class="row-fluid">
                <span class="follow-info">Patient ${patient_count}</span><span class="follow-info">Follow ${follower_count}</span>
            </div>
            <div class="muted span9">Bio:${summary}</div>
            {% templatetag openvariable %}if have_clinic {% templatetag closevariable %}
                <div class="clinic-box span12">
                    <div><span class="orange">Clinic Name:</span>${clinic_name}</div>
                    <div><span class="orange">Business Hour:</span> ${business_hour}</div>
                    <div><span class="orange">Location:</span>${work_location}</div>
                </div>
            {% templatetag openvariable %}/if{% templatetag closevariable %}
        </div> 
    </div>   
</script>