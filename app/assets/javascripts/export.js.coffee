$ ->
  link = $('#exportLink')
  url  = "#{link.attr('href')}?#{$('form').serialize()}"
  link.attr(href: url)
