define(["jquery","validate","lightbox","json","btnmask","ajaxform","tmpl"],function(){var e={_constructor:{url_gallery:"/ajax/d/gallery/getcases/"},get:function(t){$.ajax({url:t,success:function(t){e.render(t)}})},newcase:{init:function(){e.upload(!0,"#new_case")},create:function(e){e.find(".sub_caseinfo").click(function(t){$(this).identalk_btnMask(),t.preventDefault(),e.find(".caseinfo_form").valid()&&e.find(".caseinfo_form").identalk_ajaxform({callback:function(t){e.find(".create_case").hide().next().show(),t.status&&(loadings.autohide(t.msg),e.find(".case_id").val(t.case_id))}})})}},edit:{init:function(){}},upload:function(t,n){$(n).identalk_lightbox({width:500,autowidth:!0,height:200,autoheight:!0,content:$("#uploader_wrap").html(),afterLoad:function(){var n=$(".orange-wrap");$('iframe[name="case_img_iframe"]').length>0&&$('iframe[name="case_img_iframe"]').remove();var r=$("<iframe>").attr("name","case_img_iframe");r.appendTo(".iframe_wrap"),t&&e.newcase.create(n),n.find(".caseimg_form").submit(function(){loadings.show(),r.unbind("load"),r.on("load",function(){$(".sub-case").removeClass("invisible"),loadings.hide(),$(".case_img").val("");var e=$(this).contents().get(0),t=$(e).find("body").html(),r=$.evalJSON(t);if(r.status){loadings.autohide(r.msg);var i='<div class="img-group"> 								<img src="'+r.bef_img+'"><img src="'+r.aft_img+'"> 								<a class="group-img-del newicon newicon-minus" href="javascript:;" rel="'+r.img_id+'" title="delete">X</a></div>';n.find(".preview_case").append(i),$(".group-img-del").on("click",function(){var e=$(this).parent();$.ajax({url:"/ajax/gallery/case/deleteimg/",data:{img_id:$(this).attr("rel")},success:function(t){t.status&&(e.slideUp().remove(),loadings.autohide(t.msg))}})})}if(r.toolarge){loadings.autohide(r.msg);return}})}),n.find(".sub_caseimg").click(function(e){e.preventDefault(),n.find(".caseimg_form").valid()&&n.find(".caseimg_form").submit()}),n.find(".sub-case").click(function(){$(this).identalk_btnMask(),$(".mask").click();try{e.get(e._constructor.url_gallery)}catch(t){refresh()}})}})},render:function(e){e.length===0?$("#gallery_list .den-tip").show():$("#gallery_list").empty().append($("#gallery_tmpl").tmpl(e))}};return e});