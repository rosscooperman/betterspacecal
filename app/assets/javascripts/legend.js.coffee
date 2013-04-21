updateLegend = ->
  legend = $('.legend').html('')
  $('input[type=checkbox]').each ->
    checkbox = $(this)
    if checkbox.prop('checked')
      cssClass = checkbox.val().toLowerCase()
      legend.append $('<li/>').addClass(cssClass).html(checkbox.val())

$ ->
  updateLegend()
  $('form').submit(updateLegend)
