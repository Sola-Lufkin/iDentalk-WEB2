define(["jquery","valuecheck","tmpl","json","fileupload","confirmbox"],function(){var e={_constructor:{post:{url:"/ajax/d/stream/post/",url_more:"/ajax/d/stream/getmorepost/",url_del:"/ajax/d/stream/deletepost/",tmpl:"#stream_tmpl",msg_box:"#msg_box",msg:"#msg_flow"},comment:{url_get:"/ajax/d/stream/getcomment/",url_sub:"/ajax/stream/comment/",url_del:"/ajax/d/stream/deletecomment/"}},post:{init:function(){this.post()},render:function(t){if(!t[0].id)return;$("#msg_flow").empty().append($(e._constructor.post.tmpl).tmpl(t)),this.more(),this.zoom_pic()},post:function(){var t=e._constructor.post.msg_box;$(".post-msg").unbind("click").click(function(){var n=$.trim($(t).val());if(!$(t).identalk_valuecheck())return!1;$.ajax({url:e._constructor.post.url,data:{post:n,img:$("#pre_img").children("img").attr("src")},success:function(n){$(t).text("").val(""),$(".post-img").val(""),$("#pre_img").empty().hide(),e.post.renderone(n)}})}),$("#upload_img").identalk_fileupload({form_target:"file_upload_iframe",form_action:"/ajax/d/stream/post_img/",file_name:"img",afterLoad:function(e){var e=$.evalJSON(e);if(e.status){$(".post-img").val(e.post_img_url);var t='<img src="'+e.post_img_url+'" width="200" height="150" />';$("#pre_img").append(t).show(),$(".del-post-img").on("click",function(){$(".post-img").val(""),$("#pre_img").slideUp(1e3,function(){$(this).children("img").remove()})})}if(e.toolarge){loadings.autohide(e.msg);return}}})},zoom_pic:function(){$(".upload-img").unbind("click").click(function(e){e.preventDefault();var t=$(this);t.hasClass("preview-pic")?t.removeClass("preview-pic").children().attr("src",t.attr("href")):t.addClass("preview-pic").children().attr("src",t.data("big-pic"))})},more:function(){var t=1,n=$(".btn-post").data("link");if($(".stream").length>=10){var r=$('<div class="stream get-more-post"><div class="stream-content"><dl class="stream-avatar more-post"><i class="icon-refresh"></i></dl></div></div>');$(".stream:last-child").after(r),$(".more-post").click(function(){t+=1,$.ajax({url:n,data:{page:t},success:function(t){t[0].is_end?$(".more-post").unbind("click").addClass("disabled"):($(".stream").not(".get-more-post").last().after($(e._constructor.post.tmpl).tmpl(t)).nextAll().hide().fadeIn(500),e.post.del(),e.post.zoom_pic(),e.comment.init())}})})}},renderone:function(t){var n=e._constructor.post.tmpl,r=e._constructor.post.msg;$(r).children().length>0?$(r+" .stream:first-child").hide().before($(n).tmpl(t)).fadeIn(500):$(r).hide().append($(n).tmpl(t)).fadeIn(500),e.comment.init(),this.del(),this.zoom_pic()},del:function(){$(".stream").hover(function(){$(this).find(".stream-toolbar").removeClass("invisible")},function(){$(this).find(".stream-toolbar").addClass("invisible")}),$(".post-del").unbind("click").click(function(t){var n=this.rel;$.ajax({url:e._constructor.post.url_del,data:{pid:$(this).attr("rel")},success:function(e){loadings.autohide(e.msg),e.status&&$("#stream_"+n).animate({opacity:0,height:0},1e3,function(){$(this).remove()})}})}).confirmbox()}},comment:{init:function(){this.open(),this.sub()},open:function(){$(".comment").unbind("click").click(function(){var t=$("#comments_"+this.rel),n=this.rel;t.hasClass("hide")?(t.removeClass("hide"),$.ajax({url:e._constructor.comment.url_get,data:{post_id:n},success:function(t){e.comment.render(t,n)}})):(t.addClass("hide"),$("#comments-tree_"+n).empty())})},render:function(e,t){$("#comments-tree_"+t).hide().append($("#comment_tmpl").tmpl(e)).fadeIn(500),this.del()},sub:function(){$(".sub-comment").unbind("click").click(function(){var t=$(this),n=t.attr("rel"),r=t.prev().val();if(!t.prev().identalk_valuecheck())return;t.identalk_btnMask("open"),$.ajax({url:e._constructor.comment.url_sub,data:{pid:n,comment:r},success:function(r){r.status&&(e.comment.render(r,n),$("textarea[name=comment-content]").val("").text(""),$(".comment[rel="+n+"] .comment-count").text(r.comment_count),t.identalk_btnMask("close"))}})})},del:function(){$(".del-comment").unbind("click").click(function(){var t=this.rel;$this=$(this),$.ajax({url:e._constructor.comment.url_del,data:{cid:t},success:function(e){e.status&&($("#comment_"+t).next().remove().end().remove(),$(".comment[rel="+e.pid+"] .comment-count").text(e.comment_count),$this.remove()),loadings.autohide(e.msg)}})}).confirmbox()}}};return e});