unhideCircles = (el, satName) ->
  d3.selectAll('circle.' + satName).transition().style('opacity', 1).duration(100)
  $(el).removeClass('hidden')

fetchData = (el, satName) ->
  $('.spinner').show()
  filters = $('form').serialize() + '&' + $.param({ 'source[]': satName })
  $.getJSON document.location, filters, (data, status, xhr) ->
    drawLocs(data)
    $('.spinner').hide()
    $(el).removeClass('hidden')
    window.loadedSats = $.makeArray(window.loadedSats).concat(satName)

$ ->
  $('.legend li a').mouseenter (event) ->
    satName = this.className.replace(/\s*hidden\s*/, '')
    d3.selectAll('circle.' + satName).transition().ease('bounce').attr('r', 7).duration(500)

  $('.legend li a').mouseleave (event) ->
    satName = this.className.replace(/\s*hidden\s*/, '')
    d3.selectAll('circle.' + satName).transition().ease('bounce').attr('r', 5).duration(500)

  $('.legend li a').click (event) ->
    event.preventDefault()
    satName = this.className.replace(/\s*hidden\s*/, '')
    if $(this).hasClass('hidden')
      if satName in window.loadedSats
        unhideCircles(this, satName)
      else
        fetchData(this, satName)
    else
      d3.selectAll('circle.' + satName).style('opacity', 1).transition().style('opacity', 0).duration(100)
      $(this).addClass('hidden')
    reloadTL()
