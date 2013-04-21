$(document).ready(function(){
  $(".hotdrop").hover(
    function () {
      $(".opticalDrop").slideToggle(300)
    },
    function () {
      $(".opticalDrop").slideToggle(100)
    }
  );
});