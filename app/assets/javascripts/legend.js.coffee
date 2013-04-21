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

  $('.legend').on 'mouseenter', 'li', (event) ->
    d3.selectAll('circle.' + this.className).transition().attr('r', 7).duration(500)

  $('.legend').on 'mouseleave', 'li', (event) ->
    d3.selectAll('circle.' + this.className).transition().attr('r', 5).duration(500)

