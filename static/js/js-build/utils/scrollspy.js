define(["jquery"],function(){$.fn.identalk_scrollspy=function(e){var t={},n=$.extend({},t,e);return this.each(function(){var e=$(this),t=e.find("a"),r=[],i=[],s=n.offset||0;for(var o=0;o<t.length;o++){var u=t[o].href.substring(t[o].href.indexOf("#"));i.push(u)}for(var o=0;o<i.length;o++){var a=$(i[o]).offset().top-s;r.push(a)}$(window).scroll(function(){for(var t=0;t<i.length;t++){if(!($(window).scrollTop()>r[t]*1))return;e.find('a[href="'+i[t]+'"]').parent().addClass("active").siblings().removeClass("active")}})}),this}});