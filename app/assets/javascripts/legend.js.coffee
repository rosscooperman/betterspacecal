# updateLegend = ->
#   legend = $('.legend').html('')
#   $('input[type=checkbox]').each ->
#     checkbox = $(this)
#     if checkbox.prop('checked')
#       cssClass = checkbox.val().toLowerCase()
#       legend.append $('<li/>').addClass(cssClass).html(checkbox.val())

$ ->
  $('.legend li a').mouseenter (event) ->
    satName = this.className.replace(/\s*hidden\s*/, '')
    d3.selectAll('circle.' + satName).transition().ease('bounce').attr('r', 7).duration(500)

  $('.legend li a').mouseleave (event) ->
    satName = this.className.replace(/\s*hidden\s*/, '')
    d3.selectAll('circle.' + satName).transition().ease('bounce').attr('r', 5).duration(500)

  $('.legend li a').click (event) ->
    satName = this.className.replace(/\s*hidden\s*/, '')
    if $(this).hasClass('hidden')
      d3.selectAll('circle.' + satName).transition().style('opacity', 1).duration(100)
      $(this).removeClass('hidden')
    else
      d3.selectAll('circle.' + satName).style('opacity', 1).transition().style('opacity', 0).duration(100)
      $(this).addClass('hidden')
