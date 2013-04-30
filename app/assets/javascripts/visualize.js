var svg    = null,
    xScale = null,
    yScale = null;


function initMap() {
  buildMap();
  var aspect = 2.0,
      chart  = $("#skymap_svg");

  $(window).on("resize", function() {
    var targetWidth = chart.parent().width();
    chart.attr("width", targetWidth);
    chart.attr("height", targetWidth / aspect);
  });
}


function buildMap() {
  // this setup convention follows Bostock: http://bl.ocks.org/mbostock/3019563
  var margin    = { top: 0, right: 0, bottom: 0, left: 0 },
      div_width = $(".skymap").width(),
      width     = div_width - margin.left - margin.right,
      height    = div_width / 2.0 - margin.top - margin.bottom;

  svg = d3.select(".skymap")
    .append("svg")
    .attr("id", "skymap_svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .attr("preserveAspectRatio", "xMidYMid")
    .attr("viewBox", "0 0 " + div_width + " " + div_width / 2.0)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // With this convention, all subsequent code can ignore margins.
  var minL = -180,
      minB = -90,
      maxL = 180,
      maxB = 90;

  xScale = d3.scale.linear()
    .domain([ minL, maxL ])
    .range([ width, 0 ]);

  yScale = d3.scale.linear()
    .domain([ minB, maxB ])
    .range([ height, 0 ]);

  d3.select("#skymap_svg").on("mousemove", function() {
    m_c = d3.mouse(this);
    updateLocations([ xScale.invert(m_c[0]), yScale.invert(m_c[1]) ]);
  });
}


Handlebars.registerHelper('firstImage', function() {
  return this.images[0];
});


Handlebars.registerHelper('nedUrl', function() {
  var encodedTarget = encodeURIComponent(this.target);
  return "http://ned.ipac.caltech.edu/cgi-bin/imgdata?objname=" + encodedTarget;
});


Handlebars.registerHelper('formatTime', function(date) {
  return strftime("%F @ %T", new Date(date));
});


function modalTop() {
  var center = $(window).scrollTop() + ($(window).height() / 2);
  return (center - ($('#default-popup').height() / 3)).toString() + 'px';
}


var template = null, modalShowing = false;
function showModal(d) {
  if (!template) {
    template = Handlebars.compile($('#modal-template').html());
  }

  var popup = $('#default-popup');
  popup.html(template(d));

  popup.css({ top: modalTop() });

  Avgrund.show( "#default-popup" );
  modalShowing = true;
}


var timer = null;
function moveModal() {
  timer = null;
  $('#default-popup').animate({ top: modalTop() });
}


$(window).scroll(function(evt) {
  clearTimeout(timer);
  timer = setTimeout(moveModal, 250);
});


$(function() {
  $('#default-popup').on('click', '.closeButton', function() { Avgrund.hide(); });
  modalShowing = false;
});


function growCircle(d) {
  d3.select('#' + $(this).attr('id'))
    .transition()
    .attr('r', 7)
    .duration(100);
}


function shrinkCircle(d) {
  d3.select('#' + $(this).attr('id'))
    .transition()
    .attr('r', 5)
    .duration(100);
}


function updateLocations(locations){
  $("#l_coord").html(locations[0].toFixed(1));
  $("#b_coord").html(locations[1].toFixed(1));
}


var loadedCoords = [];
function drawLocs(coords) {
  // svg.selectAll("circle")
  //   .data([])
  //   .exit()
  //   .remove();

  var overall_start = 0,
      max_date      = 0;

  for (var i in coords) {
    var coord = coords[i];
    var date = new Date(coord["start"]) / 1000.0;
    if (date < overall_start || overall_start == 0) {
      overall_start = date;
    }
    if (date > max_date) {
      max_date = date;
    }
    coord["secs"] = date;

    // calculate an element ID for the circle that this coordinate will produce
    var id = (coord['_id'].$oid) ? 'id' + coord['_id'].$oid : coord['_id'];
    coord['id'] = id.toLowerCase().replace(/\|/g, '-').replace(/[ \/]/g, '');
  }
  loadedCoords = loadedCoords.concat(coords);

  var duration = 3000.0 / (1.0 * (max_date - overall_start));
  svg = d3.select("#skymap_svg");

  var selection = svg.selectAll("circle").data(loadedCoords);

  selection.enter().append("circle")
    .attr("cx", function(d) {
      return xScale((d["l"] > 180) ? d["l"] - 360 : d["l"]);
    })
    .attr("cy", function(d) {
      return yScale(d["b"]);
    })
    .attr("class", function(d) {
      return "target " + d["source"].toLowerCase();
    })
    .attr("id", function(d) {
      console.log(d['id']);
      return d['id'];
    })
    .attr("r", 0.5);

  selection.transition()
    .attr("r", 5)
    .ease("elastic")
    .duration(1000)
    .delay(function(d) {
      return (d["secs"] - overall_start) * duration;
    });

  selection.exit().remove();

   svg.selectAll("circle")
     .on("click", showModal)
     .on("mouseover", growCircle)
     .on("mouseout", shrinkCircle)
     .append("title")
     .text(function(d) {
       return d["target"];
     });
}


// Add an onClick callback to the filter button that fires this function
var loadedSats = [];
function getFilters(){
  // Build a jQuery param friendly hash of unfiltered satellites
  loadedSats = $('.legend').find('li a').not('.hidden').map(function(i, el) { return el.className; });
  var unfiltered = loadedSats.map(function(i, sat) {
    return { name: 'source[]', value: sat };
  });

  // Return the form elements serialized
  return $('form').serialize() + '&' + $.param(unfiltered);
}


function fetchData() {
  $.getJSON(document.location, getFilters(), function(data, status, xhr) {
    drawLocs(data);
    initTimeline(data);
  });
}


// The real work -- onload initialize the map and start the process of fetching data from the server
$(function() {
  initMap();
  fetchData();
  $('form').submit(function(e) {
    e.preventDefault();
    fetchData();
  });
});

