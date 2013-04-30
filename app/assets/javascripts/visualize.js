var svg    = null,
    xScale = null,
    yScale = null,
    imXScale=null,
    imYScale=null,
    zoomed_XS=null,
    zoomed_YS=null,
	canvas=null,
	is_zoomed=false,
    ctx=null;

var sky=new Image();
var sky_hi=new Image();

function initMap() {

  // added
  canvas=document.getElementById("sky");
  ctx=canvas.getContext("2d");
  sky.src="http://www.nasahack.jrsandbox.com/static/imgs/visible_sky.jpg";
  sky_hi.src="http://www.nasahack.jrsandbox.com/static/imgs/visible_hires.jpg";
  
  buildMap();
  var aspect = 2.,
      chart = $("#skymap_svg");

  $(window).on("resize", function() {
      var targetWidth = chart.parent().width();
      chart.attr("width", targetWidth);
      chart.attr("height", targetWidth / aspect);
      
      canvas.width=targetWidth;
      canvas.height=targetWidth/aspect;
      resetZoom();
  });
  
  sky.onload=function(){
		drawCanvas(null);
		imXScale = d3.scale.linear()
			.domain([-180,180])
			.range([sky.width,0])
		imYScale = d3.scale.linear()
			.domain([-90,90])
			.range([sky.height,0])
	}
  sky_hi.onload=function(){
		sky=sky_hi;
		imXScale = d3.scale.linear()
			.domain([-180,180])
			.range([sky.width,0])
		imYScale = d3.scale.linear()
			.domain([-90,90])
			.range([sky.height,0])
	}
}


function buildMap() {

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
      .on("dblclick",function(){my_zoom(d3.mouse(this));});
      //.on("dblclick",function(){alert("clicked!");});

  var background=svg.append("rect")
	.attr("class","chart_background")
    .attr("width", width)
    .attr("height", height);

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

	d3.select("#skymap_svg").on("mousemove",function(){
	  m_c=d3.mouse(this);
	  if(is_zoomed){updateLocations([zoomed_XS.invert(m_c[0]),zoomed_YS.invert(m_c[1])]);}
	  else{updateLocations([xScale.invert(m_c[0]),yScale.invert(m_c[1])]);}
	});
}

function drawCanvas(c_in){
	var targetWidth = $("#skymap_svg").parent().width();
	canvas.width = targetWidth;
	canvas.height = targetWidth/2.;
	ctx.fillStyle="black";
	ctx.fillRect(0,0,canvas.width,canvas.height);

	cw=canvas.width;
	ch=canvas.height;
	if(!(is_zoomed)){
		ctx.drawImage(sky,0, 0, sky.width, sky.height, 0, 0, cw, ch);
	}
	else{
		if(c_in==null){
			// this shouldn't be called, but if it is, reset the zoom and redraw
			resetZoom();
		}
		else{
			ctx.drawImage(sky,c_in[0],c_in[1],c_in[2],c_in[3],c_in[4],c_in[5],c_in[6],c_in[7]);
		}
	}
}

function getLCoord(d){
	var l=(d["l"]>180)?d["l"]-360:d["l"];
	if(is_zoomed){
		return zoomed_XS(l);}
	else{
		return xScale(l);}
}
function getBCoord(d){
	var b=d["b"];
	if(is_zoomed){
		return zoomed_YS(b);}
	else{
		return yScale(b);}
}

Handlebars.registerHelper('firstImage', function() {
  return this.images[0];
});


Handlebars.registerHelper('nedUrl', function() {
  //var encodedTarget = encodeURIComponent(this.target);
  //return "http://ned.ipac.caltech.edu/cgi-bin/imgdata?objname=" + encodedTarget;
  return this.reference_url
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
    .attr('r', 5)
    .duration(100);
}


function shrinkCircle(d) {
  d3.select('#' + $(this).attr('id'))
    .transition()
    .attr('r', 3)
    .duration(100);
}


function updateLocations(locations){
  $("#l_coord").html(locations[0].toFixed(1));
  $("#b_coord").html(locations[1].toFixed(1));
}


function clearLocs(){
  svg.selectAll("circle")
     .data([])
     .exit()
     .remove();
  loadedCoords=[];
}

var loadedCoords = [];
function drawLocs(coords) {

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
      return d['id'];
    })
    .attr("r", 0.5);

  selection.transition()
    .attr("r", 3)
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

function imDistToCanvasDist(dist){
	var coordDist=Math.abs(imXScale.invert(0)-imXScale.invert(dist));
	var canvasDist=Math.abs(zoomed_XS(0)-zoomed_XS(coordDist));
	return canvasDist;
}

function getCanvasCoords(center,width){
	var width_in_image=imXScale(-width/2.)-imXScale(width/2.)
	// set up the mapping

	// the central point in image coordinates
	var iCenter=[imXScale(center[0]),imYScale(center[1])];
	var ix=iCenter[0]-width_in_image/2;
	var iy=iCenter[1]-width_in_image/4;
	
	var delIX=0;
	var delIY=0;

	// Now handle under and overflows
	if(ix<0){delIX=ix*-1;}
	if(iy<0){delIY=iy*-1;}

	ix=ix+delIX;
	iy=iy+delIY;	

	var iw=width_in_image-delIX;
	var ih=width_in_image/2.-delIY;

	var overIX=0;
	var overIY=0;
	if(ix+iw>sky.width){
		overIX=(ix+iw)-sky.width;
		iw=sky.width-ix;
	}
	if(iy+ih>sky.height){
		overIY=(iy+ih)-sky.height;
		ih=sky.height-iy;
	}

	// set the canvas mapping	
	var cx=0+imDistToCanvasDist(delIX);
	var cy=0+imDistToCanvasDist(delIY);
	var cw=canvas.width-imDistToCanvasDist(overIX);
	var ch=canvas.height-imDistToCanvasDist(overIY);

	return [ix,iy,iw,ih,cx,cy,cw,ch];	
}

function my_zoom(mouse_coords){
	if(!(is_zoomed)){
		var m=[xScale.invert(mouse_coords[0]),yScale.invert(mouse_coords[1])];
		
		var t_width=$("#skymap_svg").parent().width();
		box_width=60;
		zoomed_XS=d3.scale.linear()
				    .domain([m[0]-box_width/2, m[0]+box_width/2])
				    .range([t_width,0]);
		zoomed_YS=d3.scale.linear()
				    .domain([m[1]-box_width/4, m[1]+box_width/4])
				    .range([t_width/2.,0]);
				    
		is_zoomed=true;
		circles=svg.selectAll("circle")
			.transition()
		   .attr("cx", function(d){return getLCoord(d);})
		   .attr("cy", function(d){return getBCoord(d);})
		   .duration(1000);
		
		d3.select("#sky")
			.style("opacity",0)
			.transition()
			.style("opacity",1)
			.duration(1000);
		drawCanvas(getCanvasCoords(m,box_width));

   }
   else{
		is_zoomed=false;
		circles=svg.selectAll("circle")
			.transition()
		   .attr("cx", function(d){return getLCoord(d);})
		   .attr("cy", function(d){return getBCoord(d);})
		   .duration(1000);
		d3.select("#sky")
			.style("opacity",0)
			.transition()
			.style("opacity",1)
			.duration(1000);
		drawCanvas(null);

   }
}

function resetZoom(){
	is_zoomed=false;
	circles=svg.selectAll("circle")
		.transition()
	   .attr("cx", function(d){return getLCoord(d);})
	   .attr("cy", function(d){return getBCoord(d);})
	   .duration(1000);
	d3.select("#sky")
		.style("opacity",0)
		.transition()
		.style("opacity",1)
		.duration(1000);
	drawCanvas(null);
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
  drawCanvas();

  $("#filter").click(function(){clearLocs();});

  $('form').submit(function(e) {
    e.preventDefault();
    fetchData();
  });
});

