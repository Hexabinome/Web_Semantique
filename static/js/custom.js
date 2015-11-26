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
    target = ($('input[name="type"]:checked').val() == "actors")?0:1;
    filtre = ($('input[name="filtre"]:checked').val() == "memento")?0:1;
    $("#searchBtn").bind("click", function(){
        $.post('/search', {'search': $("#searchInput").val(), 'seuil' : $("#seuilInput").val(),
                                                'type' : $('input[name="type"]:checked').val(),
                                                'filtre' : $('input[name="filtre"]:checked').val()}, function(data) {
            console.debug($.parseJSON(data));
        });
    })

});