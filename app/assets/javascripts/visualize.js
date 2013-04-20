var svg=null;
var xScale=null;
var yScale=null;

function initMap(){
  buildMap();
  var aspect = 2.,
      chart = $("#skymap_svg");
  $(window).on("resize", function() {
      var targetWidth = chart.parent().width();
      chart.attr("width", targetWidth);
      chart.attr("height", targetWidth / aspect);
  });
}

function buildMap(){

  // this setup convention follows Bostock: http://bl.ocks.org/mbostock/3019563
  var margin = {top: 0, right: 0, bottom: 0, left: 0};
  var div_width=$(".skymap").width();
  var width = div_width - margin.left - margin.right,
      height = div_width/2. - margin.top - margin.bottom;

  svg = d3.select(".skymap").append("svg")
      .attr("id","skymap_svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .attr("preserveAspectRatio","xMidYMid")
      .attr("viewBox","0 0 "+div_width+" "+div_width/2.)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // With this convention, all subsequent code can ignore margins.
  var minL=-180;
  var minB=-90;
  var maxL=180;
  var maxB=90;


  xScale = d3.scale.linear()
                       .domain([minL,maxL])
                       .range([width, 0]);          // using astronomical convention - increasing to the left

  yScale = d3.scale.linear()
                       .domain([minB,maxB])
                       .range([height,0]);

  var xAxis = d3.svg.axis()
                    .scale(xScale)
                    .orient("bottom")
                    .ticks(19);  //Set rough # of ticks

  //Define Y axis
  var yAxis = d3.svg.axis()
                    .scale(yScale)
                    .orient("left")
                    .ticks(10);

}


function showModal(d) {
  // alert("Telescope:\t"+d["source"]+"\nFrom:\t\t"+d["start"]+"\nTo:\t\t\t"+d["end"]);
  $('#obsTarget').html(d["target"]);
  $('#obsSource').html(d["source"]);
  $('#obsStartDate').html(d["start"]);
  $('#obsEndDate').html(d["end"]);
  Avgrund.show( "#default-popup" );
}

$(function() {
  $('.closeButton').click(function() { Avgrund.hide(); });
});

function drawLocs(coords){
  clearLocs();
  svg=d3.select("#skymap_svg");
  svg.selectAll("circle")
     .data(coords)
     .enter()
     .append("circle")
     .attr("cx", function(d) {var local_l=d["l"];
         if(local_l>180){ local_l-=360;}
          return xScale(local_l);
     })
     .attr("cy", function(d) {
          return yScale(d["b"]);
     })
     .attr("r", 5)
     .attr("class",function(d){return "target "+d["source"]+"_marker";})
     .on("click", showModal)
     .append("title")
     .text(function(d) {return d["target"]});

}


function clearLocs(){
  svg.selectAll("circle")
    .data([])
    .exit().remove();
}


$(function() {
  initMap();
  $.getJSON(document.location, null, function(data, status, xhr) {
    drawLocs(data);
  });
});
