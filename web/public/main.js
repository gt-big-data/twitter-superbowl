//Drawing Properties
var margin = {top: 20, right: 20, bottom: 30, left: 50},
	width = 960 - margin.left - margin.right;
	height = 500 - margin.top - margin.bottom;


var svg = d3.select("body").append("svg")
	.attr("width", width + margin.left + margin.right)
	.attr("height", height + margin.bottom + margin.top)
	.append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
function init(filepaths) {
	var colors = d3.scale.category10();

	//First loads the 2 data files
	var q = queue(filepaths.length);
	for(var i = 0; i < filepaths.length; i++) {
		q = q.defer(d3.json, filepaths[i]);	
	}


	//Returns a JavaSrcript Date Object
	var getDate = function(d) {
		return new Date(d * 1000);
	}

	//Scales
	var x = d3.time.scale().range([0, width]);
	var y = d3.scale.linear().range([height, 0]);

	//Axes
	var xAxis = d3.svg.axis()
		.scale(x)
		.orient("bottom");
	var yAxis = d3.svg.axis()
		.scale(y)
		.orient("left");

	var line = d3.svg.line()
		.x (function(d) { return x(d.date.getTime());})
		.y (function(d) {return y(d.frequency)});


	var dataset = [];

	//Then starts graphing everything
	q.awaitAll(function(error, results) {
		//Processes each data file
		for (var i = 0; i < results.length; ++i) {
			var data = results[i];
			var start = +data.start;
			var period = +data.period;
			var className = data.phrase;

			dataset.push(data.frequencies.map(function(x, i) {
				return {"frequency": +x,
					"date": getDate(start + period*i),
					"class": className };
			}));

		}

		//Calculates domains for the axes
		var xExtents = [];
		var yExtents = [];
		for (var i = 0; i < dataset.length; ++i) {
			xExtents = xExtents.concat(d3.extent(dataset[i], function(d) {
				return d.date.getTime();
			}));
			yExtents = yExtents.concat(d3.extent(dataset[i], function(d) {
				return d.frequency;
			}));
		}
		x.domain(d3.extent(xExtents)).nice();
		y.domain(d3.extent(yExtents)).nice();

		//Draws axes and axes labels
		svg.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate(0," + height + ")")
			.call(xAxis);

		svg.append("g")
			.attr("class", "y  axis")
			.call(yAxis)
		.append("text")
			.attr("transform", "rotate(-90)")
			.attr("y", 6)
			.attr("dy", ".71em")
			.style("text-anchor", "end")
			.text("Frequency (# of tweets per 15 seconds)");

		//Draws the lines
		for (var i = 0; i < dataset.length; ++i) {
			svg.append("path")
				.datum(dataset[i])
				.attr("class", "line")
				.attr("d", line)
				.attr("stroke", colors(i));
		}

		//Legend
		var legend = svg.selectAll(".legend")
			.data(colors.domain())
			.enter().append("g")
			.attr("class", "legend")
			.attr("transform", function(d, i) { return "translate(0," + i * 20 + ")";});

		legend.append("rect")
			.attr("x", width - 18)
			.attr("width", 18)
			.attr("height", 18)
			.style("fill", function(d, i) {return colors(i)});

		legend.append("text")
			.attr("x", width - 24)
			.attr("y", 9)
			.attr("dy", ".35em")
			.style("text-anchor", "end")
			.attr("class", "legendTitles")
			.text(function(d, i) {return dataset[i][0].class; });
	});
}

words = "seattle,seahawks,wilson,denver,broncos,manning,sb48,superbowl".split(",");
paths = words.map(function(word) {return "/data/?phrase=" + word});

init(paths);
