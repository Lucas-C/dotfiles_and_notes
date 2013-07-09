d3.select("css-selector").append("elem") // Also: selectAll

// Joins
.data(..) // return 3 virtual selections: enter(), update[no sub-method] & exit()

// Data stored in __data__ property

.text( "hello ")
.text( function (data_elem, index) { return "index = " + index + " data_elem = " + data_elem; } )
// "if the value passed to it (the Text Operator) is a function, then the function is evaluated for each __data__ element in order.
// And the functions result is used to set each element's text context "

var svgContainer = d3.select("body").append("svg").attr("width", 200).attr("height", 100);

.interpolate("<interpolation>")
// linear, step-before, step-after, basis (B-spline), basis-open, basis-closed, bundle (B-spline straightened), cardinal (Cardinal spline), cardinal-open, cardinal-closed, monotone (cubic interpolation)

var scale = d3.scale.linear() // Also: Power, Logarithmic, Quantize, Quantile, Ordinal
                            .domain([d3.min(data), d3.max(data)])
                            .range([0,100]);
var scaledVal = scale(origVal)

var xAxis = d3.svg.axis().scale(scale)
var xAxisGroup = svgContainer.append("g").call(xAxis);

