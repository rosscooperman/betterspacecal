$ ->
  $('.scrollto').click (e) ->
    e.preventDefault()
    selector = $(e.target).attr('href')
    $('body, html').animate({ scrollTop: $(selector).offset().top }, 500)
