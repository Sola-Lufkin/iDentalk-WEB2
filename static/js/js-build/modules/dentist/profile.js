define(["jquery","lightbox","confirmbox"],function(){var e={_constructor:{url_pro:"/ajax/d/profile/",field:{id:"#den_field",row:".field-row",tmpl_a:"#field_degree_tmpl",unchoice:"#den_field_unchoice",tmpl_b:"#field_degree_unchoice_tmpl",sub_btn:"#field_sub",url:"/ajax/d/profile/editfield/"},degree:{id:"#den_degree",row:".degree-row",tmpl_a:"#field_degree_tmpl",unchoice:"#den_de_unchoice",tmpl_b:"#field_degree_unchoice_tmpl",sub_btn:"#degree_sub",url:"/ajax/d/profile/editdegree/"},workplace:{id:"#den_local",tmpl:"#local_tmpl",edit_btn:".worklocation-edit",del_btn:".worklocation-del",add_btn:"#worklocation_add"}},choice_edit:function(){$(".choice-edit").each(function(){$(this).click(function(){var t=$(this),n=t.data("choicetype");n=="field"?e.field.show(t):e.degree.show(t)})}),e.field.init(),e.degree.init()},get:function(t){$.ajax({url:t,success:function(t){e.degree.render(t),e.field.render(t)}})},field:{init:function(){this.sub()},show:function(t){var n=e._constructor.field;t.hasClass("open")?this.close(t):(e.degree.close($(".choice-edit.open")),t.text("Cancel").addClass("open").prev().show().animate({right:80}),$(n.unchoice).slideDown(),$(n.row+" .choice-label").toggleClass("choiceable-label"),$(n.row+" .choice-label").unbind("click"),$(n.row+" .choiceable-label").on("click",function(){$(this).toggleClass("label-orange")}))},close:function(t){var n=e._constructor.field;t.text("Edit").removeClass("open").prev().hide().css({right:30}),$(n.unchoice).slideUp(),$(n.row+" .choice-label").removeClass("choiceable-label")},render:function(t){var n=e._constructor.field;$(n.id).empty(),$(n.unchoice).empty(),$(n.id).append($(n.tmpl_a).tmpl(t.choice_feild)),$(n.unchoice).append($(n.tmpl_b).tmpl(t.unchoice_feild))},sub:function(){var t=e._constructor.field;$(t.sub_btn).click(function(){var n=[],r=$(t.row+" .label-orange");for(var i=0;i<r.length;i++)n.push(r.eq(i).text());$.ajax({url:t.url,data:{tags:n.toString()},success:function(n){loadings.autohide(n.msg),$(t.unchoice).hide(),e.field.close($(".choice-edit.open")),e.get(e._constructor.url_pro)}})})}},degree:{init:function(){this.sub()},show:function(t){var n=e._constructor.degree;t.hasClass("open")?this.close(t):(e.field.close($(".choice-edit.open")),t.text("Cancel").addClass("open").prev().show().animate({right:80}),$(n.unchoice).slideDown(),$(n.row+" .choice-label").toggleClass("choiceable-label"),$(n.row+" .choice-label").unbind("click"),$(n.row+" .choiceable-label").on("click",function(){$(this).toggleClass("label-orange")}))},close:function(t){var n=e._constructor.degree;t.text("Edit").removeClass("open").prev().hide().css({right:30}),$(n.unchoice).slideUp(),$(n.row+" .choice-label").removeClass("choiceable-label")},render:function(t){var n=e._constructor.degree;$(n.id).empty(),$(n.unchoice).empty(),$(n.id).append($(n.tmpl_a).tmpl(t.choice_degree)),$(n.unchoice).append($(n.tmpl_b).tmpl(t.unchoice_degree))},sub:function(){var t=e._constructor.degree;$(t.sub_btn).click(function(){var n=[],r=$(t.row+" .label-orange");for(var i=0;i<r.length;i++)n.push(r.eq(i).text());$.ajax({url:t.url,data:{tags:n.toString()},success:function(n){loadings.autohide(n.msg),$(t.unchoice).hide(),e.degree.close($(".choice-edit.open")),e.get(e._constructor.url_pro)}})})}},workplace:{init:function(){this.create(),this.del(),this.edit()},create:function(){var t=e._constructor.workplace;$(t.add_btn).unbind("click"),$(t.add_btn).identalk_lightbox({type:"iframe",width:770,height:625,beforeOpen:function(e){if($("#den_local table").length>2)return loadings.autohide("Sorry, you hava added three work locations."),!0},afterClose:function(){e.get(e._constructor.url_pro)}})},render:function(t){var n=e._constructor.workplace;$(n.id).empty().append($(n.tmpl).tmpl(t.WorkPlaceList)),$(".local-num").each(function(e){$(this).text("0"+(e+1))})},edit:function(){var t=e._constructor.workplace;$(t.edit_btn).identalk_lightbox({type:"iframe",width:850,height:800,afterClose:function(){e.get(e._constructor.url_pro)}})},del:function(){var t=e._constructor.workplace;$(t.del_btn).bind("click",function(e){e.preventDefault();var t=$(this).data("localid");$.ajax({url:$(this).attr("href"),success:function(e){loadings.autohide(e.msg),$("#local_"+t).slideUp(800,function(){$(this).prev().remove(),$(this).remove()})}})}).confirmbox()}}};return e});