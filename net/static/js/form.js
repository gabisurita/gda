
Pages = $("#section-tabs li:last").text()
 
$("body").on("keyup", "form", function(e){
  if (e.which == 13){
    if ($("#next").is(":visible") && $("fieldset.current").find("input, textarea").valid() ){
      e.preventDefault();
      nextSection();
      return false;
    }
  }
});
 
 
$("#next").on("click", function(e){
  console.log(e.target);
  nextSection();
});
 
$("form").on("submit", function(e){
  if ($("#next").is(":visible") || $("fieldset.current").index() < Pages - 1){
    e.preventDefault();
  }
});
 
function goToSection(i){
  $("fieldset:gt("+i+")").removeClass("current").addClass("next");
  $("fieldset:lt("+i+")").removeClass("current");
  $("#section-tabs li").eq(i).addClass("current").siblings().removeClass("current");
  setTimeout(function(){
    $("fieldset").eq(i).removeClass("next").addClass("current active");
      if ($("fieldset.current").index() == Pages - 1){
        $("#next").hide();
        $("input[type=submit]").show();
        $("input[type=submit]").val("Enviar");
      } else {
        $("#next").show();
        $("input[type=submit]").hide();
      }
  }, 80);
 
}
 
function nextSection(){
  var i = $("fieldset.current").index();
  if (i < Pages -1){
    $("#section-tabs li").eq(i+1).addClass("active");
    goToSection(i+1);
  }
}
 
$("li").on("click", function(e){
  var i = $(this).index();
  if ($(this).hasClass("active")){
    goToSection(i);
  } else {
//    alert("Complete as questões anteriores!");
  }
});
 
 
