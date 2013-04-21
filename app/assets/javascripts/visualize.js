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
var overall_start=0;
	var max_date=0;

	for(var i in coords){
		var date=new Date(coords[i]["start"]);
		date=date/1000.;
		if(date<overall_start || overall_start==0){overall_start=date;}
		if(date>max_date){max_date=date;}
		coords[i]["secs"]=date;
	}
	var duration=3000/(1.*(max_date-overall_start));

	svg=d3.select("#skymap_svg");
	var c=svg.selectAll("circle")
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
	   .attr("class",function(d){return "target "+d["source"]+"_marker";})
	   .attr("r", 1)
		.transition()
	   .attr("r",  10)
	   .ease("linear")
	   .duration(1000)
	   .delay(function(d) {
	        return (d["secs"]-overall_start)*duration;
	   })
		.transition()
	   .attr("r",  5)
	   .ease("elastic")
	   .duration(500);

	 svg.selectAll("circle")
	   .on("click",function(d){alert("Telescope:\t"+d["source"]+"\nFrom:\t\t"+d["start"]+"\nTo:\t\t\t"+d["end"]);})
     .on("click", showModal)
	   .append("title")
     .text(function(d) {return d["target"]});

}


function clearLocs(){
  svg.selectAll("circle")
    .data([])
    .exit().remove();
}

// Add an onClick callback to the filter button that fires this function
function getFilters(){
  // Return the form elements serialized
  return $('form').serialize();
}

function fetchData(){
  $.getJSON(document.location, getFilters(), function(data, status, xhr) {
    drawLocs(data);
  });
}


$(function() {
  initMap();
  fetchData();
  $('form').submit(function(e){
    e.preventDefault();
    fetchData();
  });
});