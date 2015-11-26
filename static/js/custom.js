/**
* Created by elmhaidara on 20/11/15.
*/

//http://bl.ocks.org/mbostock/4062045
function d3Graphe(links, div)
{
	var nodes = {};

	// Compute the distinct nodes from the links.
	links.forEach(function(link) {
		link.source = nodes[link.source] || (nodes[link.source] = {name: link.source});
		link.target = nodes[link.target] || (nodes[link.target] = {name: link.target});
	});

	var width = 960,
	height = 500;

	var force = d3.layout.force()
		.nodes(d3.values(nodes))
		.links(links)
		.size([width, height])
		.linkDistance(60)
		.charge(-300)
		.on("tick", tick)
		.start();

	var svg = d3.select(div).append("svg")
		.attr("width", width)
		.attr("height", height);

	var link = svg.selectAll(".link")
		.data(force.links())
		.enter().append("line")
		.attr("class", "link");

	var node = svg.selectAll(".node")
		.data(force.nodes())
		.enter().append("g")
		.attr("class", "node")
		.call(force.drag);

	node.append("circle")
		.attr("r", 8);

	node.append("text")
		.attr("x", 12)
		.attr("dy", ".35em")
		.text(function(d) { return d.name; });

	function tick() {
		link
		  .attr("x1", function(d) { return d.source.x; })
		  .attr("y1", function(d) { return d.source.y; })
		  .attr("x2", function(d) { return d.target.x; })
		  .attr("y2", function(d) { return d.target.y; });

		node
		  .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
	}

}

$(document).ready(function() {
    /*var source = new EventSource("/progress");
    source.onmessage = function(event) {
        $('.progress-bar').css('width', event.data+'%').attr('aria-valuenow', event.data);
    }*/

    $("#searchBtn").bind("click", function(){
        doLongCurtain();
        $.post('/search', {'search': $("#searchInput").val(), 'seuil' : $("#seuilInput").val(),
                                'type' : $('input[name="type"]:checked').val(),
                                'filtre' : $('input[name="filtre"]:checked').val()},
        function(data) {
            data = $.parseJSON(data);
            console.debug(data.graph);
            doCurtain();
            displayGraph(data.graph);

            if($('input[name="type"]:checked').val() == "actors")
                printActors(data.target);
            else if ($('input[name="type"]:checked').val() == "movies")
                printFilms(data.target);
        });
    });
});

function printActors(data)
{
    $.each(data, function(uri, val){
        $("#listeTarget").append(getDivActor(val.alias, val.birth, val.thumbnail, uri, val.resume));
    });
}

function printFilms(data)
{
    $.each(data, function(uri, val){
        $("#listeTarget").append(getDivMovie(val.alias, val.director, val.budget, val.comment, val.runtime));
    });
}

function getDivActor(alias, birth, thumbnail, uri, resume)
{
    var str = '<li> '
    + '<div class="panel panel-default">'
    + '     <div class="panel-heading">'
    + '        <h1 class="panel-title">' + alias + ' - ' + birth + '</h1>'
    + '     </div>'
    + '     <div class="panel-body">'
    + '         <div id="thumbnail" class="col-md-6 col-lg-4">'
    + '            <img src="' + thumbnail + '" />'
    + '            <div class="caption">'
    + '                <h3> ' + alias + '</h3>'
    + '            </div>'
    + '            <b> sources </b> '+ uri
    + '        </div>'
    + '        <div class="col-md-6 col-lg-8 right-padding">'
    + '            <div id="resume" class="row"><b> Histoire :</b> {{ '+ resume + ' }}'
    + '            </div>'
    + '        </div>'
    + '    </div>'
    + '</div>'
    + '</li>';

    return str;
}

function getDivMovie(alias, director, budget, comment, runtime)
{
    var str = '<li>'
    +'  <div class="panel panel-default">'
    +'      <div class="panel-heading">'
    +'          <h1 class="panel-title">' + alias + ' - <a href=' + director + '> Director</a>'
    +'          </h1>'
    +'      </div>'
    +'      <div class="row panel-body">'
    +'          <div id="thumbnail" class="col-md-6">'
    +'          </div>'
    +'          <div class="col-md-6">'
    +'              <div id="budget" class="row">'
    +'                  <b>Budget :</b> '+ budget
    +'              </div>'
    +'              <div id="resume" class="row"><b> Comments :</b> '+ comment
    +'              </div>'
    +'              <div id="source" class="row"><b> runtime :</b> '+ runtime
    +'              </div>'
    +'          </div>'
    +'      </div>'
    +'  </div>'
    +'</li>';

    return str;
}

function displayGraph(graph, minimum)  {
  var matrice = [];
  for (var mySource in graph) {
    for (var myTarget in graph[mySource]) {
      if (graph[mySource][myTarget] > minimum) {
        matrice.push({source: mySource,
                      target: myTarget,
                      type: "licensing"    });
  }}}
  d3Graphe( matrice , "#graph");
}

