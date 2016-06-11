$(document).ready(function() {

  var navbar = $('.navbar').height();
  var width = $('table').width();
  var search = $('.search').offset().top;
  $('.search').css('width', width);

  $(window).resize(function() {
    var navbar = $('.navbar').height();
    var width = $('table').width();
    $('.search').css('width', width);
  });

  function fixSearch() {
    var searchH = $('.search').height();
    var scrollTop = $(window).scrollTop();
    if($('.search').css('position') === 'static') {
      if(search < scrollTop + navbar) {
        $('.search').css('position', 'fixed');
        $('.search').css('top', navbar);
      }
    }
    else {
      if(scrollTop + navbar < search) {
        $('.search').css('position', 'static');
        $('.search').css('top', 'auto');
      }
    }
  }

  fixSearch();
  $(window).scroll(function() {
    fixSearch();
  });
  $(window).resize(function() {
    fixSearch();
  });
});
