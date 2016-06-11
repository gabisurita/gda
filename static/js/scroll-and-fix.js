$(document).ready(function() {

  function debounce(func, wait, immediate) {
  	var timeout;
  	return function() {
  		var context = this, args = arguments;
  		var later = function() {
  			timeout = null;
  			if (!immediate) func.apply(context, args);
  		};
  		var callNow = immediate && !timeout;
  		clearTimeout(timeout);
  		timeout = setTimeout(later, wait);
  		if (callNow) func.apply(context, args);
  	};
  };

  var navbar = $('.navbar').height();
  var scrollMax = $(document).height();

  function scrollAndFixBottom(d) {
    d.each(function() {
      var bottom = $(this).offset().top + $(this).height();
      var scrollBottom = $(window).scrollTop() + $(window).height();
      if((bottom < scrollBottom) && (scrollBottom < scrollMax)) {
        $(this).css('padding-top', (scrollBottom - bottom));
      }
      else if(bottom > scrollBottom) {
        $(this).css('padding-top', 0);
      }
    });
  }

  function scrollAndFixTop(d) {
    d.each(function() {
      var top = $(this).offset().top;
      var scrollTop = $(window).scrollTop() + navbar + 10;
      if((top < scrollTop) && (scrollTop < scrollMax)) {
        $(this).css('padding-top', (scrollTop - top));
      }
      else if(top > scrollTop) {
        $(this).css('padding-top', 0);
      }
    });
  }

  function scrollAndFix(scroll, oldScroll) {
    $('.scroll-and-fix').each(function() {
//      $(this).css('transition', 'all linear 0.2s');
      wHeight = $(window).height() - navbar;
      dHeight = $(this).height();
      if(dHeight < wHeight) {
        scrollAndFixTop($(this));
      }
      else {
        if(scroll < oldScroll) {
          scrollAndFixTop($(this));
        }
        else if(scroll > oldScroll){
          scrollAndFixBottom($(this));
        }
      }
    });
  }

  scrollAndFix();
  oldScroll = 0;
  $(window).scroll(function() {
    scroll = $(window).scrollTop();
//    scrollAndFix(scroll, oldScroll);
    debounce(scrollAndFix(scroll, oldScroll), 1);
    oldScroll = scroll
  });

});
