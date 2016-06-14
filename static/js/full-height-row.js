$('document').ready(function() {

  function setHeight() {
    $('.full-height-row').css('min-height', $(window).height() - $('.navbar').height());
    $('.full-height-row').css('display', 'flex');
    $('.full-height-row').css('align-items', 'center');
  }

  setHeight();
  $(window).resize(function() {
    setHeight();
  });
});
