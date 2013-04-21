$(document).ready(function(){
  
  // show/hide filter fields
  $('#filterdata').click(function(){
    $('.filters').slideToggle();
  });
  
  // dropdown functionality on the filters
  $(".hotdrop").hover(
    function () {
      $(".opticalDrop").slideToggle(300)
    },
    function () {
      $(".opticalDrop").slideToggle(100)
    }
  );
  var viewportHeight = $(window).height();
  
  
  
});
