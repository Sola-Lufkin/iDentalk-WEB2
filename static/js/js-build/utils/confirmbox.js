define(["jquery","lightbox"],function(e){e.fn.confirmbox=function(t){function i(){e(".orange-close").click()}var n={title:"Action",msg:"Are you sure to delete this?",btn:["Close","Delete"]},r=e.extend({},n,t);return this.each(function(t){var n=this,s=e(this);s.data("msg")!==undefined&&(r.msg=s.data("msg")),s.data("title")!==undefined&&(r.title=s.data("title")),s.data("btn")!==undefined&&(r.btn=s.data("btn").split(","));var o=function(){var t=e._data(n,"events");t&&(n._handlers=new Array,e.each(t.click,function(){n._handlers.push(this)}),s.unbind("click"))},u=function(){n._handlers!==undefined&&e.each(n._handlers,function(){s.bind("click",this)})},a=function(t){t.stopImmediatePropagation(),t.preventDefault(),s.identalk_lightbox({autoheight:!0,width:530,open:!0,content:e(".modal").html(),afterLoad:function(){var t=e(".orange-wrap");t.find(".modal-body").text(r.msg),t.find(".confirm-save").text(r.btn[1]),t.find(".confirm-close").text(r.btn[0]),t.find(".confirm-close").bind("click",function(){i()}),t.find(".confirm-save").bind("click",function(){s.unbind("click",a).click(),i()})}})};o(),s.bind("click",a),u()}),this}});