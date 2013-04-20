resizer = ->
  height = $('.skymap').width() / 2
  $('.skymap').css(height: "#{height}px")

$ ->
  $(window).resize(resizer)
  resizer()
