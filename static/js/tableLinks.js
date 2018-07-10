$('*[data-href]').on("click",function(){
  window.location = $(this).data('href');
  return false;
});
$('*[data-href]').css('cursor', 'pointer');
$("tr").on("click",function(e){
  e.stopPropagation();
});
$("tr").on("hover",function(e){
  $(this).css('color', 'white');
  e.stopPropagation();
});
