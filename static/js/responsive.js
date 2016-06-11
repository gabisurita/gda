$(document).ready(function() {

  function responsive() {
    var width = $(window).width();
    if(width >= 768) {
      $('.mobile').hide();
      $('.desktop').show();
    }
    else {
      $('.mobile').show();
      $('.desktop').hide();
    }
  }

  responsive();
  $(window).resize(function() {
    responsive();
  });

});
