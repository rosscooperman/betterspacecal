$ ->
  $('.scrollto').click (e) ->
    e.preventDefault()
    selector = $(e.target).attr('href')
    $('body').animate({ scrollTop: $(selector).offset().top }, 500)
