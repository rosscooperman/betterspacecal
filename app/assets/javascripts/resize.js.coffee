resizer = ->
  height = $('.skymap').width() / 2
  console.log height
  $('.skymap').css(height: "#{height}px")

$ ->
  $(window).resize(resizer)
  resizer()
