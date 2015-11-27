/**
* Created by elmhaidara on 20/11/15.
*/
var type = -1;
var search = "";
var seuil = "";

//http://bl.ocks.org/mbostock/4062045

//global
var matriceSimilitude = null;

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

    // empty div
    $( div ).empty()

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
        displayQuote();
        doLongCurtain();
        type = $('input[name="type"]:checked').val();
        search = $("#searchInput").val();
        seuil = $("#seuilInput").val();
        $.post('/search', {'search': $("#searchInput").val(), 'seuil' : $("#seuilInput").val(),
                                'type' : type,
                                'filtre' : "memento"},
        function(data) {
            data = $.parseJSON(data);
            // console.debug(data.graph);
            doCurtain();
            matriceSimilitude = data.graph;
            displayGraph(data.graph, 0.02);

            if($('input[name="type"]:checked').val() == "actors")
                printActors("listeTarget", data.target);
            else if ($('input[name="type"]:checked').val() == "movies")
                printFilms("listeTarget", data.target);
        });
    });

    $( "#similitude" ).change(function() {
      displayGraph(matriceSimilitude, this.value);
    });
});

function ajaxGetSimilar(uri)
{
    $("#listeSimilar").html("");

    $("#loading").fadeIn("slow");
    console.debug(uri);

    $("#menu3").removeClass("in");
    $("#menu3").removeClass("active");
    $("#tab4").removeClass("active");

    $("#tab3").addClass("active");
    $("#menu2").addClass("active");
    $("#menu2").addClass("in");

    $.post('/search', {'search': uri, 'seuil' : seuil, 'type' : type, 'filtre' : 'similar'},
        function(data) {
            $("#loading").fadeOut("slow");

            data = $.parseJSON(data);
            if($('input[name="type"]:checked').val() == "actors")
                printActors("listeSimilar", data.target);
            else if ($('input[name="type"]:checked').val() == "movies")
                printFilms("listeSimilar", data.target);
    });
}

function printActors(ul, data)
{
    $.each(data, function(uri, val){
        $("#"+ul).append(getDivActor(val.alias, val.birth, val.thumbnail, uri, val.resume));
        $("#"+uri.split("/").pop()).bind("click", function(e){
            ajaxGetSimilar($("#"+e.currentTarget.id).data("uri"));
        });
    });
}

function printFilms(ul, data)
{
    $.each(data, function(uri, val){
        $("#"+ul).append(getDivMovie(uri, val.alias, val.director, val.budget, val.comment, val.runtime));

        $("#"+uri.split("/").pop().substr(0, 5)).bind("click", function(e){
            ajaxGetSimilar($("#"+e.currentTarget.id).data("uri"));
        });
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
    +'          <div class="col-md-6">'
    +'              <img src="' + thumbnail + '" />'
    +'              <div>'
    +'                  <button id="' + uri.split("/").pop() + '" class="btnSimilar btn btn-primary" data-uri="' + uri + '">'
    +'                      Résultats similaires '
    +'                  </button>'
    +'              </div>'
    +'          </div>'
    + '         <div class="caption">'
    + '               <h3> ' + alias + '</h3>'
    + '         </div>'
    + '            <b> sources </b> '+ uri
    + '         <div class="col-md-6 right-padding">'
    + '             <div id="resume" class="row"><b> Histoire :</b> '+ resume
    + '              </div>'
    + '         </div>'
    + '       </div>'
    + '    </div>'
    + '</div>'
    + '</li>';

    return str;
}

function getDivMovie(uri, alias, director, budget, comment, runtime)
{
    var str = '<li>'
    +'  <div class="panel panel-default">'
    +'      <div class="panel-heading">'
    +'          <h1 class="panel-title">' + alias + ' - ' + director + '</h1>'
    +'      </div>'
    +'      <div class="row panel-body">'
    +'          <div class="col-md-6">'
    +'              <div id="thumbnail" >'
    +'              </div>'
    +'              <button id="' + uri.split("/").pop().substr(0, 5) + '" class="btnSimilar btn btn-primary" data-uri = "' + uri + '">'
    +'                  Résultats similaires '
    +'              </button>'
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
                      type: "licensing"  });
  }}}
  d3Graphe( matrice , "#graph");

}

function displayQuote(){
    // list of list
    var quote = [[" Houston, we have a problem." , "Apollo 13"],
    ["I'll be back.", "Terminator"],
    ["It really tied the room together.", "The Big Lebowski"],
    ["It's alive! It's alive!", "Frankenstein"],
    ["I've got a feeling we're not in Kansas anymore.", "The Wizard of Oz"],
    ["E.T. phone home.", "E.T."],
    ["I love the smell of napalm in the morning.", "Apocalypse Now"],
    ["I'm gonna make him an offer he can't refuse.", "The Godfather"],
    ["Remember, with great power. comes great responsibility.", "Spiderman"]
    ];
    var rand = Math.floor((Math.random() * (quote.length -1) ) + 1);

    $("#citation").empty();
    $("#citation").append("<q>" + quote[rand][0] + "<q> <cite>" + quote[rand][1] + "</cite>");
}


